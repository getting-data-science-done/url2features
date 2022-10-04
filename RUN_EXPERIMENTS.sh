#!/bin/bash

python  experiments/recipes/01_NBayes.py syskill
python  experiments/recipes/01_NBayes.py malware
python  experiments/recipes/01_NBayes.py phishing
python  experiments/recipes/01_NBayes.py webkb

python  experiments/recipes/02_LogReg.py syskill
python  experiments/recipes/02_LogReg.py malware
python  experiments/recipes/02_LogReg.py phishing
python  experiments/recipes/02_LogReg.py webkb

python  experiments/recipes/03_ExtraTrees.py syskill
python  experiments/recipes/03_ExtraTrees.py malware
python  experiments/recipes/03_ExtraTrees.py phishing
python  experiments/recipes/03_ExtraTrees.py webkb

python  experiments/recipes/04_LGBM.py syskill
python  experiments/recipes/04_LGBM.py malware
python  experiments/recipes/04_LGBM.py phishing
python  experiments/recipes/04_LGBM.py webkb

#python tabulate_results.py

