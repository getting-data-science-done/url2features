#!/bin/bash

echo "SySkill"
python  experiments/recipes/01_NBayes.py syskill
python  experiments/recipes/02_LogReg.py syskill
python  experiments/recipes/03_ExtraTrees.py syskill
python  experiments/recipes/04_LGBM.py syskill

echo "WebKb"
python  experiments/recipes/01_NBayes.py webkb
python  experiments/recipes/02_LogReg.py webkb
python  experiments/recipes/03_ExtraTrees.py webkb
python  experiments/recipes/04_LGBM.py webkb

echo "SPAM"
python  experiments/recipes/01_NBayes.py spam
python  experiments/recipes/02_LogReg.py spam
python  experiments/recipes/03_ExtraTrees.py spam
python  experiments/recipes/04_LGBM.py spam

echo "Malware"
python  experiments/recipes/01_NBayes.py malware
python  experiments/recipes/02_LogReg.py malware
python  experiments/recipes/03_ExtraTrees.py malware
python  experiments/recipes/04_LGBM.py malware

echo "Phishing"
python  experiments/recipes/01_NBayes.py phishing
python  experiments/recipes/02_LogReg.py phishing
python  experiments/recipes/03_ExtraTrees.py phishing
python  experiments/recipes/04_LGBM.py phishing

echo "DMOZ"
python  experiments/recipes/01_NBayes.py dmoz
python  experiments/recipes/02_LogReg.py dmoz
python  experiments/recipes/03_ExtraTrees.py dmoz
python  experiments/recipes/04_LGBM.py dmoz

#python tabulate_results.py

