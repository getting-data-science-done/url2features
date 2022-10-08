#!/bin/bash

./url2features-runner.py -columns=URL -simple -host -tld -protocol -path -file -params data/sets/Syskill/syskill_dataset.csv  > data/sets/Syskill/syskill_processed.csv

./url2features-runner.py -columns=URL -simple -host -tld -protocol -path -file -params  data/sets/ISCX-URL2016/malware_dataset.csv  >  data/sets/ISCX-URL2016/malware_processed.csv
./url2features-runner.py -columns=URL -simple -host -tld -protocol -path -file -params  data/sets/ISCX-URL2016/phishing_dataset.csv  >  data/sets/ISCX-URL2016/phishing_processed.csv

./url2features-runner.py -columns=URL -simple -host -tld -protocol -path -file -params  data/sets/ISCX-URL2016/spam_dataset.csv  >  data/sets/ISCX-URL2016/spam_processed.csv

./url2features-runner.py -columns=URL -simple -host -tld -protocol -path -file -params data/sets/WebKb_4Unis/webkb.csv  > data/sets/WebKb_4Unis/webkb_processed.csv
 
./url2features-runner.py -columns=URL -simple -host -tld -protocol -path -file -params data/sets/DMOZ/dmoz_dataset.csv > data/sets/DMOZ/dmoz_processed.csv

projit add dataset syskill data/sets/Syskill/syskill_processed.csv
projit add dataset malware data/sets/ISCX-URL2016/malware_processed.csv
projit add dataset phishing data/sets/ISCX-URL2016/phishing_processed.csv
projit add dataset spam data/sets/ISCX-URL2016/spam_processed.csv
projit add dataset webkb data/sets/WebKb_4Unis/webkb_processed.csv
projit add dataset dmoz data/sets/DMOZ/dmoz_processed.csv

