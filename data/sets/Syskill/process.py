import pandas as pd
import numpy as np
import os

cols = ['id','label','url','date','title']

bands = pd.read_csv("SW/Bands/index", header=None, names=cols, sep="|")
biod = pd.read_csv("SW/BioMedical/index", header=None, names=cols, sep="|")
goats = pd.read_csv("SW/Goats/index", header=None, names=cols, sep="|")
sheep = pd.read_csv("SW/Sheep/index", header=None, names=cols, sep="|")

def convert_to_ord(x):
    if x=='cold': return 0
    if x=='medium': return 1
    if x=='hot': return 2
    return np.nan

bands['rating'] = bands['label'].apply(convert_to_ord)
biod['rating'] = biod['label'].apply(convert_to_ord)
goats['rating'] = goats['label'].apply(convert_to_ord)
sheep['rating'] = sheep['label'].apply(convert_to_ord)

total_df = bands.append(biod, ignore_index=True)
total_df = total_df.append(goats, ignore_index=True)
total_df = total_df.append(sheep, ignore_index=True)
total_df.sort_values(by="url",inplace=True)

store_df = total_df.loc[:,['url','label']]
store_df.to_csv("dataset.csv",header=True,index=False)


