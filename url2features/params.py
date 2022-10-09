# -*- coding: utf-8 -*-
from urllib import parse
import pkg_resources
import pandas as pd
import numpy as np
import string
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
count = lambda l1,l2: sum([1 for x in l1 if x in l2])

########################################################################################
def add_params_features(df, col, add_prefix):
    """
        Given a pandas dataframe and a column name.
        calculate the params features 
    """
    def get_params_features(x, col):
        f_length = 0
        f_sections = 0
        f_enc_char = 0
        p_length = 0
        p_count = 0
        p_match = np.nan
        p_has_url = 0
        p_enc_url = 0
        p_enc_char = 0
        key_count = 0
        key_len = 0
        key_numeric = 0
        val_count = 0
        val_len = 0
        val_numeric = 0
        if x[col]==x[col]:
            url = add_protocol_if_missing(x[col])
            protocol, host, path, params, query, fragment = parse.urlparse(url.strip())
            f_length = len(fragment)
            if f_length>0:
               fparts = re.split(r'[?=&]', fragment)
               f_sections = len(fparts)
               f_enc_char = detect_encoded_chars(fragment)
            p_length = len(query)
            if p_length>0:
               param_set = query.split("&")
               p_count = len(param_set)
               p_has_url = detect_embedded_url(query)
               p_enc_url = detect_encoded_link(query)
               p_enc_char = detect_encoded_chars(query)
               keys = []
               vals = []
               for pair in param_set:
                   brok = pair.split("=")
                   keys.append(brok[0])
                   if len(brok)>1:
                      vals.append(brok[1])
               if len(keys)>0:
                 key_count = len(keys)
                 key_len = np.mean([len(k) for k in keys])
                 all_keys = "".join(keys)
                 if len(all_keys)>0:
                    key_numeric = count(all_keys, string.digits)/len(all_keys)  
               if len(vals)>0:
                 val_count = len(vals)
                 val_len = np.mean([len(v) for v in vals])
                 all_vals = "".join(vals)
                 if len(all_vals)>0:
                    val_numeric = count(all_vals, string.digits)/len(all_vals)
            p_match = int( val_count == key_count )  
        return p_length, p_count, p_match, p_has_url, p_enc_url, p_enc_char, f_length, f_sections, f_enc_char, key_count, key_len, key_numeric, val_count, val_len, val_numeric

    if add_prefix:
        col_names = [ col+"_params_len", col+"_params_count", col+"_params_match", col+"_params_has_url", 
                      col+"_params_enc_url", col+"_params_enc_char", 
                      col+"_frag_len", col+"_frag_secs",  col+"_frag_enc_char", 
                      col+"_keys_count", col+"_keys_len", col+"_keys_numeric", 
                      col+"_value_count", col+"_values_len", col+"_values_numeric"  ] 
    else:
        col_names = [ "params_len", "params_count", col+"_params_match", "params_has_url", 
                      "params_enc_url", "params_enc_char", 
                      "frag_len", "frag_secs", "frag_enc_char", 
                      "keys_count", "keys_len", "keys_numeric", 
                      "values_count", "values_len", "values_numeric" ]

    df[ col_names ] = df.apply(get_params_features, col=col, axis=1, result_type="expand")

    return df

###################################################################
def add_protocol_if_missing(x):
    """
    Determine if the URL begins with any form of protocol
    and add a default protocol if it is absent.
    """
    p = re.findall(r"^[a-zA-Z]{2,8}://", x)
    if len(p) > 0: 
        return x
    else:
        return "http://"+x


