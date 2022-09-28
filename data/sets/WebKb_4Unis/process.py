from os.path import isfile, join
import pandas as pd
import numpy as np
import os

rez = pd.DataFrame(columns=['URL','label'])

dir = "webkb"

cat_dirs = [f for f in os.listdir(dir) if not isfile(join(dir,f))]

def clean_url(url):
   url = url.replace("/", ":")
   url = url.replace("^", "/")
   return url

for cat in cat_dirs:
   mypath = join(dir,cat)
   files = []
   for (dirpath, dirnames, filenames) in os.walk(mypath):
      myfiles = [f for f in filenames if (f!=".DS_Store")]
      files.extend(myfiles)
   
   labels = [cat for f in files]
   urls = [clean_url(s) for s in files]
   temp = pd.DataFrame({"URL":urls, "label":labels})
   rez = rez.append(temp, ignore_index=True)

rez.to_csv("webkb.csv", index=False, header=True)

