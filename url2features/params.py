# -*- coding: utf-8 -*-
from urllib import parse
import pkg_resources
import pandas as pd
import numpy as np
import math
import os
import re


"""
    url2features.params: Features based on the any params in the URL string
"""
from .process import load_dictionary


########################################################################################
def params_features(df, columns, add_prefix=True):
    """
        Given a pandas dataframe and a set of column names.
        calculate the params summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_params_features(rez, col, add_prefix)
    return rez



########################################################################################
regex = r'('
regex += r'(?:[A-Z][A-Z]+:\/\/)?'
regex += r'('
regex += r'(?:(?:[A-Z0-9][A-Z0-9-]{0,61}[A-Z0-9]\.)+)'
regex += r'|(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
regex += r'|(?:([A-Z0-9]{2,4}:){3,12}[A-Z0-9]{2,4})'
regex += r')'
regex += r'(?::(\d{1,5}))?'
regex += r'(?:(\/\S+)*)'
regex += r')'
find_urls_in_string = re.compile(regex, re.IGNORECASE)

def detect_embedded_url(x):
    url = find_urls_in_string.search(x)
    if url is not None and url.group(0) is not None:
       return 1
    else:
       return 0

########################################################################################
def detect_encoded_link(x):
    return x.count("%3A%2F%2F")

########################################################################################
enc_chars_in_string = re.compile(r'(%[0-9A-F][0-9A-F])')
def detect_encoded_chars(x):
    url = enc_chars_in_string.search(x)
    if url is not None and url.group(0) is not None:
       return 1
    else:
       return 0


########################################################################################
def add_params_features(df, col, add_prefix):
    """
        Given a pandas dataframe and a column name.
        calculate the params features 
    """
    def get_params_features(x, col):
        f_length = 0
        p_length = 0
        p_count = 0
        p_has_url = 0
        p_enc_url = 0
        p_enc_char = 0
        if x[col]==x[col]:
            url = (x[col])
            protocol, host, path, params, query, fragment = parse.urlparse(url.strip())
            f_length = len(fragment)
            p_length = len(query)
            if p_length>0:
               param_set = query.split("&")
               p_count = len(param_set)
               p_has_url = detect_embedded_url(query)
               p_enc_url = detect_encoded_link(query)
               p_enc_char = detect_encoded_chars(query)
        return f_length, p_length, p_count, p_has_url, p_enc_url, p_enc_char 

    if add_prefix:
        col_names = [ col+"_frag_len", col+"_params_len", col+"_params_count", 
                      col+"_params_has_url", col+"params_enc_url", col+"params_enc_char" ] 
    else:
        col_names = [ "frag_len", "params_len", "params_count", "params_has_url", "params_enc_url", "params_enc_char" ]

    df[ col_names ] = df.apply(get_params_features, col=col, axis=1, result_type="expand")

    return df

