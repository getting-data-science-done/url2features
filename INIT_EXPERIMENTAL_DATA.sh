#!/bin/bash

./url2features-runner.py -columns=URL -simple -host -tld -protocol -path -file -params data/sets/Syskill/dataset.csv  > data/sets/Syskill/syskill_processed.csv

./url2features-runner.py -columns=URL -simple -host -tld -protocol -path -file -params  data/sets/ISCX-URL2016/malware_dataset.csv  >  data/sets/ISCX-URL2016/malware_processed.csv
./url2features-runner.py -columns=URL -simple -host -tld -protocol -path -file -params  data/sets/ISCX-URL2016/phishing_dataset.csv  >  data/sets/ISCX-URL2016/phishing_processed.csv

./url2features-runner.py -columns=URL -simple -host -tld -protocol -path -file -params data/sets/WebKb_4Unis/webkb.csv  > data/sets/WebKb_4Unis/webkb_processed.csv


projit add dataset syskill data/sets/Syskillprocessed.csv
projit add dataset malware data/sets/ISCX-URL2016/malware_dataset_processed.csv
projit add dataset phishing data/sets/ISCX-URL2016/phishing_dataset_processed.csv
projit add dataset webkb data/sets/WebKb_4Unis/webkb_processed.csv


