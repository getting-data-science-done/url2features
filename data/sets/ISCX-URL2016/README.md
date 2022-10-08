ISCX-URL2016
============

Download the file from here

http://205.174.165.80/CICDataset/ISCX-URL-2016/

You will need to fill in a form to access the data.

Citation:

Mohammad Saiful Islam Mamun, Mohammad Ahmad Rathore, Arash Habibi Lashkari, Natalia Stakhanova and Ali A. Ghorbani, "Detecting Malicious URLs Using Lexical Analysis", Network and System Security, Springer International Publishing, P467--482, 2016.

Once you extract the archive it will contain a directory called [FinalDataset](FinalDataset/)

The SPAM dataset is plagued by the carriage return problem.
So runn the following to repalce those with new lines.

```
cat FinalDataset/URL/spam_dataset.csv | tr "^M" "\\n" > FinalDataset/URL/spam_dataset2.csv
```

Use the script [process.py](process.py) to create datasets for the Phishing, Malware and SPAM  problems


