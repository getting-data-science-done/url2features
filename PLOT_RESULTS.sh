#!/bin/bash

mkdir results/final

cp results/webkb_03_ExtraTrees.csv  results/final/WebKb.csv
cp results/syskill_01_NBayes_SHAP.csv  results/final/Syskill.csv
cp results/phishing_04_LGBM_SHAP.csv  results/final/Phishing.csv
cp results/malware_04_LGBM_SHAP.csv  results/final/Malware.csv 
cp results/dmoz_03_ExtraTrees.csv  results/final/DMOZ.csv
cp results/spam_03_ExtraTrees.csv  results/final/Spam.csv

python scripts/plot_url_importance.py "URL_" "col_name" "feature_importance_vals" results/final/Syskill.csv,results/final/WebKb.csv,results/final/Spam.csv,results/final/Phishing.csv,results/final/Malware.csv,results/final/DMOZ.csv

