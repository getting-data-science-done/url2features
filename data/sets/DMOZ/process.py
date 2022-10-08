import pandas as pd
import numpy as np
import os

df = pd.read_csv("archive/URL Classification.csv", header=None, names=['id','URL','label'])
df = df.loc[:,['URL','label']]
df.sort_values(by="URL",inplace=True)
df.to_csv("dmoz_dataset.csv",header=True,index=False)

