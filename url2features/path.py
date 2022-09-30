# -*- coding: utf-8 -*-
from urllib import parse
import pkg_resources
import pandas as pd
import numpy as np
import math
import os
import re

"""
    url2features.path: Features based on the URL path between host and file
"""
from .process import load_dictionary
from .process import add_protocol_if_missing

########################################################################################
def path_features(df, columns, add_prefix=True):
    """
        Given a pandas dataframe and a set of column names.
        calculate the path summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_path_features(rez, col, add_prefix)
    return rez


########################################################################################
def extract_word_count(path):
   wds = re.split("[-_/~]+", path)
   return sum([1 for w in wds if len(w)>2])


########################################################################################
date_in_string = re.compile(r'([0-9]{4}[-_][0-9]{2})|[0-9]{2}[-_][0-9]{4}')
def contains_date(x):
    url = date_in_string.search(x)
    if url is not None and url.group(0) is not None:
       return 1
    else:
       return 0


########################################################################################
def clean_path(path):
    path = path[1:]
    if len(path)==0:
       return path
    elif path[-1] == "/":
       return path[0:-1]
    else:
       return path


########################################################################################
def add_path_features(df, col, add_prefix):
    """
        Given a pandas dataframe and a column name.
        calculate the path features 
    """
    def get_path_features(x, col):
        p_length = 0
        p_depth = 0
        p_words = 0
        p_has_date = 0
        p_is_home = 0
        if x[col]==x[col]:
            url = add_protocol_if_missing(x[col])
            protocol, host, path, params, query, fragment = parse.urlparse(url.strip())
            path = clean_path(path)
            p_length = len(path)
            if p_length>0:
               path_set = path.split("/")
               p_depth = len(path_set)
               p_words = extract_word_count(path)
               p_has_date = contains_date(path)
               p_is_home = int(path[0] == "~")
        return p_length, p_depth, p_words, p_has_date, p_is_home 

    if add_prefix:
        col_names = [ col+"_path_len", col+"_path_depth", col+"_path_words", col+"_path_has_date", col+"_path_is_home" ] 
    else:
        col_names = [ "path_len", "path_depth","path_words", "path_has_date", "path_is_home" ]

    df[ col_names ] = df.apply(get_path_features, col=col, axis=1, result_type="expand")

    return df

