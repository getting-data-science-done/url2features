Usage Guide
===========

Command Line Utility
^^^^^^^^^^^^^^^^^^^^

After installation with pip, url2features can be invoked from the command line:

.. code-block:: bash

    >url2features


Without parameters it will print out an error and the following usage :


.. code-block:: bash

   ERROR: MISSING ARGUMENTS
   USAGE 
   url2features  [ARGS] <PATH TO DATASET>
     <PATH TO DATASET> - Supported file types: csv, tsv, xls, xlsx, odf
     [ARGS] In most cases these are switches that turn on the feature type
     -columns=<COMMA SEPARATED LIST>. REQUIRED
     -simple            Default: False. Features derived from the URL string: length, depth
     -domain            Default: False. Features derived from the domain registration.
     -extension         Default: False. Features about the domain extension and structure.



The list of columns to process and the path to the dataset are both mandatory.

The rest of the options turn on or off particular groups of features.

Python Package Usage
^^^^^^^^^^^^^^^^^^^^

You can import the url2features package within python and then make use of the
SciKit Learn Compatible Transformer for your ML Pipeline.
In the example below we initialise a URLTransform object that will generate
the domain and extension features for any
dataframe that has a column of data named 'URL_COL_NAME'


.. code-block:: python

    from url2features.pipeline import URLTransform
    from sklearn.linear_model import SGDClassifier
    from sklearn.pipeline import Pipeline

    pipeline = Pipeline([
        ('urltransform', URLTransform(['URL_COL_NAME'],['domain','extension']) ),
        ('clf', SGDClassifier(loss='log') ),
    ])

Note that the transformer version of url2features will remove the original URL columns
so that the resulting data set can be fed into an algorithm that requires numerical 
columns only. This means that if you need to do any other text feature engineering it
be placed earlier in the pipeline.

 
