url2features
----------

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/getting-data-science-done/url2features/actions/workflows/python-package.yml/badge.svg)](https://github.com/getting-data-science-done/url2features/actions/workflows/python-package.yml)
[![PyPI](https://img.shields.io/pypi/v/url2features.svg)](https://pypi.org/project/url2features)
[![Documentation Status](https://readthedocs.org/projects/url2features/badge/?version=latest)](https://url2features.readthedocs.io/en/latest/?badge=latest)

```
Status - Non-Functional In development
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

For Domain Age data we use the python package : 

This is used to build a local cached library of domain registration dates. 

## Features

Each type of feature can be unlocked through the use of a specific command line switch:

```
  -domain            Default: False. Information about the domain and its registration.
  -extension         Default: False. Information about the domain extension
```

## Usage

You can use this application multiple ways

### Runner

Use the runner without installing the application. 
The following example will generate all features on the test data.

```
./url2features-runner.py -columns=referrer -domain -extension data/test.csv > data/output.csv
```

This will send the time performance profile to STDERR as shown below:
```
Computation Time Profile for each Feature Set
---------------------------------------------
simple               0:00:00.498634
domain               0:00:00.536637
extension            0:00:00.496018
```  

### Directory as package 

Alternatively, you can invoke the directory as a package:
 
```
python -m url2features -columns=referrer -domain -extension data/test.csv > data/output.csv
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
url2features -columns=referrer data/test.csv > data/output.csv
```

This will take the Input CSV, calculate some simple summary features and 
produce an Output CSV with features appended as new columns.

For more complicated features see the additional options (outlined above).

# Acknowledgements

Python package built using the
[bootstrap cmdline template](https://github.com/jgehrcke/python-cmdline-bootstrap)
 by [jgehrcke](https://github.com/jgehrcke)


