#!/bin/bash

python malware/00_analysis.py
python malware/01_baseline.py
python malware/02_log_regression.py
python malware/03_extra_trees.py
python malware/04_lgbm.py

python phishing/00_analysis.py
python phishing/01_baseline.py
python phishing/02_log_regression.py
python phishing/03_extra_trees.py
python phishing/04_lgbm.py

python webkb/00_analysis.py
python webkb/01_baseline.py
python webkb/02_log_regression.py
python webkb/03_extra_trees.py
python webkb/04_lgbm.py

python sw/00_analysis.py
python sw/01_baseline.py
python sw/02_log_regression.py
python sw/03_extra_trees.py
python sw/04_lgbm.py

python tabulate_results.py

