from lightgbm import LGBMClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from feature_engine.encoding import RareLabelEncoder
from feature_engine.imputation import AddMissingIndicator
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import projit as pit
import pandas as pd
import numpy as np
import argparse
import shap
import sys

def main(dataset):
    experiment_name = "04 - LGBM"
    target = "label"

    project = pit.projit_load()
    exec_id = project.start_experiment(experiment_name, sys.argv[0], params={})

    train_df = pd.read_csv( project.get_dataset(dataset), low_memory=False )

    labels = train_df[target].to_list()
    labels = [str(l) for l in labels]
    label_enc = LabelEncoder()
    label_enc.fit(labels)
    y = label_enc.transform(labels)

    drop_cols = ['URL', 'label', 'URL_domain_reg_year']
    X = train_df.drop(drop_cols, axis=1)

    percent = 0.005
    while (percent * len(train_df))<80:
        percent += 0.005
    print("Test Percent:", (percent*100))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percent, stratify=y, random_state=0)

    numeric_cols = list( X_train.select_dtypes(include="number").columns)
    categorical_cols = list( X_train.select_dtypes(exclude="number").columns)

    numMissingIndicators = AddMissingIndicator(
        variables=numeric_cols
    )

    numeric_transformer = make_pipeline(
        numMissingIndicators,
        SimpleImputer(strategy='mean'),
        StandardScaler()
    )

    categorical_transformer = make_pipeline(
        SimpleImputer(strategy='constant', fill_value='missing'),
        RareLabelEncoder(tol=0.01, n_categories=2, replace_with='rare'),
        OrdinalEncoder()
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols)
        ]
    )

    clf = LGBMClassifier()

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('clf', clf )
    ])

    model.fit(X_train, y_train)

    temp = model.predict(X_test)

    ba = balanced_accuracy_score(y_test, temp)
    f1 = f1_score(y_test, temp, average='weighted')

    project.add_result(experiment_name, "BAcc", ba, dataset)
    project.add_result(experiment_name, "F1", f1, dataset)

    print("Finished [%s] - Bal Acc:"%dataset, ba)
    print("                     F1:", ba)

    print("Explaining")

    feature_names = X.columns
    def model_predict(data_asarray):
        data_asframe =  pd.DataFrame(data_asarray, columns=feature_names)
        return model.predict(data_asframe)

    mydata = shap.sample(X_train, 200)
    shap_kernel_explainer = shap.KernelExplainer(model_predict, mydata)
    if len(X_test)>100:
        mytest = shap.sample(X_test, 100)
    else:
        mytest = X_test
    shap_values = shap_kernel_explainer.shap_values(mytest)
    shap.summary_plot(shap_values, mytest, plot_type="bar", show=False)
    plot_name = "results/"+dataset+"_04_LGBM_SHAP.png"
    plt.savefig(plot_name)
    write_shap_values(shap_values,feature_names, "results/"+dataset+"_04_LGBM_SHAP.csv")
    project.end_experiment(experiment_name, exec_id, hyperparams={})

def write_shap_values(shap_values,feature_names, filename):
    shap_df = pd.DataFrame(shap_values, columns=feature_names)
    vals = np.abs(shap_df.values).mean(0)
    shap_importance = pd.DataFrame(list(zip(feature_names, vals)), columns=['col_name', 'feature_importance_vals'])
    shap_importance.sort_values(by=['feature_importance_vals'], ascending=False, inplace=True)
    shap_importance.to_csv(filename, index=False, header=True)

#########################################################################
if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='Execute Naive Bayes Model')
    my_parser.add_argument('data',
                       metavar='data',
                       type=str,
                       help='name of the dataset')

    args = my_parser.parse_args()
    data = args.data

    main(data)


