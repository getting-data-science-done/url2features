Introduction
============

``url2features`` is a Python package which aims to provide an easy and intuitive way 
of generating features from columns containing URLs in a dataset. 

The current implementation has been developed in Python 3 and tested on a variety of
CSV files. 


Motivation
**********

URLs are strings with a very specific structure and relationship to the entities
that they describe. But it is not always obvious how to make best use of them.

This package is intended to provide a quick, as well as easily extensible framework to
add columns to a dataset using a wide variety of feature engineering approaches.

It can be as either a CLI utility to process a tabular dataset, or as python package
that can be included within your ML projects. We include a SciKit Learn Compatible
Transformer for using in machine learning pipelines.


