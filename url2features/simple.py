# -*- coding: utf-8 -*-
import pandas as pd 
import numpy as np
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
def simple_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the simple text summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_simple_features(rez, col)
    return rez

########################################################################################
def add_simple_features(df, col):
    """
        Given a pandas dataframe and a column name.
        calculate the simple features 
    """
    col_name = col + "_length"
    df[col_name] = df[col].apply(null_tolerant_len)
    col_name = col + "_depth"
    df[col_name] = df[col].apply(null_tolerant_depth)

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


