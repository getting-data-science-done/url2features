url2features
----------

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/getting-data-science-done/url2features/actions/workflows/python-package.yml/badge.svg)](https://github.com/getting-data-science-done/url2features/actions/workflows/python-package.yml)
[![PyPI](https://img.shields.io/pypi/v/url2features.svg)](https://pypi.org/project/url2features)
[![Documentation Status](https://readthedocs.org/projects/url2features/badge/?version=latest)](https://url2features.readthedocs.io/en/latest/?badge=latest)

```
Status - Functional - Beta Release
```

This is an application to add features to a dataset that are derived from processing
the content of columns that contain URLs.

It will accept a CSV, TSV or XLS file and output an extended version of
the dataset with additional columns appended. When run with default settings
it will produce a small number of very simple numerical summaries. 

Additional feature flags unlock features that are more computationally intensive.

Released and distributed via setuptools/PyPI/pip for Python 3.

Additional detail available in the [documentation](https://url2features.readthedocs.io)

### Distribution

Released and distributed via setuptools/PyPI/pip for Python 3.

### Resources & Dependencies

For Domain Registration data we use the python package : whois.
However, rather than constantly hit that API endpoint we create a local dataset
of domain registration dates. This data is installed with the package.

The data was initialised with the following script:
```
python scripts/init_dom_reg_data.py
```

We then updated the data file using multiple datasets of common
domains and some specific to the requirements of our project.
These update script runs were executed as follows:
```
python scripts/update_dom_reg_data.py data/top_50_domains.csv Domain
```

```
python scripts/update_dom_reg_data.py data/top_50_domains_v2.csv site
```


This is used to build a local cached library of domain registration dates. 

## Features

Each type of feature can be unlocked through the use of a specific command line switch:

```
  -simple	     Default: False. Basic string derived features
  -protocol          Default: False. Features derives from the URL protocol.
  -host              Default: False. Features describing the host, including domain structure and registration.
  -tld               Default: False. Information about the Top Level Domain
  -path              Default: False. Features extracted from the path between host and file
  -file              Default: False. The file extension and type referenced by the URL
  -params            Default: False. The query parameters at the end of the URL
  -dns               Default: False. DNS related information.
```

## Usage

You can use this application multiple ways

### Runner

Use the runner without installing the application. 
The following example will generate all features on the test data.

```
./url2features-runner.py -columns=url -simple -host -tld -protocol -file -params data/test.csv > data/output.csv
```

This will send the time performance profile to STDERR as shown below:
```
Computation Time Profile for each Feature Set
---------------------------------------------
simple               0:00:00.002620
protocol             0:00:00.001280
host                 0:00:00.002900
tld                  0:00:00.001703
file                 0:00:00.002157
params               0:00:00.002215
```

### Directory as package 

Alternatively, you can invoke the directory as a package:
 
```
python -m url2features -columns=url -host -tld data/test.csv > data/output.csv
```

### From Install

Or you can simply install the package and use the command line application directly

```
url2features -h
```
Will print out the help


# Installation
Installation from the source tree:

```
python setup.py install
```

(or via pip from PyPI):

```
pip install url2features
```

Now, the ``url2features`` command is available::

```
url2features -columns=url -simple data/test.csv > data/output.csv
```

This will take the Input CSV, calculate some simple summary features and 
produce an Output CSV with features appended as new columns.

For more complicated features see the additional options (outlined above).

# Acknowledgements

Python package built using the
[bootstrap cmdline template](https://github.com/jgehrcke/python-cmdline-bootstrap)
 by [jgehrcke](https://github.com/jgehrcke)

Datasets for calculating features taken from the following sources 
* https://github.com/tb0hdan/domains
* https://datahub.io/core/top-level-domain-names#resource-top-level-domain-names_zip
* https://datahub.io/core/top-level-domain-names/r/top-level-domain-names.csv.csv
 
Some features ideas taken and adapted from the following:

* [URL Feature Extractor](https://github.com/lucasayres/url-feature-extractor)



