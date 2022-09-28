# -*- coding: utf-8 -*-
import pandas as pd 
import numpy as np
import string
import math
import os
import re

from .process import load_word_list

"""
    url2features.simple: Basic text feature calculation.

    Calculate simple informative statistics about the URL.
    Such as the inferred depth using slash chars, presence of dates or
    indicators of common CMS 
"""

########################################################################################
def simple_features(df, columns, add_prefix=True):
    """
        Given a pandas dataframe and a set of column names.
        calculate the simple text summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_simple_features(rez, col, add_prefix)
    return rez

########################################################################################
def add_simple_features(df, col, add_prefix=True):
    """
        Given a pandas dataframe and a column name.
        calculate the simple features 
    """

    count = lambda l1,l2: sum([1 for x in l1 if x in l2])

    def simp_feats(x, col):
        if x[col]!=x[col]:
            length = -1
            punct = -1
            numeric = -1
            capital = -1
            depth = -1
        else:
            length = len(x[col])
            punct = count(x[col], string.punctuation)/length
            numeric = count(x[col], string.digits)/length
            capital = sum(1 for c in x[col] if c.isupper())/length
            depth = null_tolerant_depth(x[col])
        return length, punct, numeric, capital, depth

    if add_prefix:
        col_names = [col+"_length", col+"_punct", col+"_numeric", col+"_capital", col+"_path_depth"]
    else:
        col_names = ["url_length","url_punct", "url_numeric", "url_capital", "path_depth"]

    df[ col_names ] = df.apply(simp_feats, col=col, axis=1, result_type="expand")

    return df

########################################################################################

def null_tolerant_len(x):
    if x != x:
        return 0
    else:
        return len(x)

########################################################################################

def null_tolerant_depth(x):
    if x != x:
        return 0
    else:
        x = remove_protocol_and_trim(x)
        return len( str(x).split("/") )

########################################################################################

def remove_protocol_and_trim(url):
    p = re.findall(r"^https?://", url)
    if len(p) > 0:
        url = url[len(p[0]):]
    e = re.findall(r"/\s*$", url)
    if len(e) > 0:
        url = url[:0-len(e[0])]
    return url


