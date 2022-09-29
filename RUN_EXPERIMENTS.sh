#!/bin/bash

python experiments/malware/00_analysis.py
python experiments/malware/01_baseline.py
python experiments/malware/02_log_regression.py
python experiments/malware/03_extra_trees.py
python experiments/malware/04_lgbm.py

python experiments/phishing/00_analysis.py
python experiments/phishing/01_baseline.py
python experiments/phishing/02_log_regression.py
python experiments/phishing/03_extra_trees.py
python experiments/phishing/04_lgbm.py

python experiments/webkb/00_analysis.py
python experiments/webkb/01_baseline.py
python experiments/webkb/02_log_regression.py
python experiments/webkb/03_extra_trees.py
python experiments/webkb/04_lgbm.py

python experiments/tabulate_results.py

