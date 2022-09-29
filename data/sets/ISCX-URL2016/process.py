import pandas as pd
import numpy as np
import os

benign = pd.read_csv("FinalDataset/URL/Benign_list_big_final.csv", header=None, names=['URL'])
phishing = pd.read_csv("FinalDataset/URL/phishing_dataset.csv", header=None, names=['URL'])
malware = pd.read_csv("FinalDataset/URL/Malware_dataset.csv", header=None, names=['URL'])
benign['label']=0
phishing['label']=1
malware['label']=1

malware_df = benign.append(malware, ignore_index=True)
malware_df.sort_values(by="URL",inplace=True)
malware_df.to_csv("malware_dataset.csv",header=True,index=False)

phish_df = benign.append(phishing, ignore_index=True)
phish_df.sort_values(by="URL",inplace=True)
phish_df.to_csv("phishing_dataset.csv",header=True,index=False)


