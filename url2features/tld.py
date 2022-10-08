# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os
import re

from .process import load_dictionary

tld_freqs = load_dictionary('tld_freqs.dat')
tld_types = load_dictionary('tld_types.dat')

"""
    url2features.tld: Host Top Level Domain feature flags

    Generate features for common domain tlds

"""

########################################################################################
tld_pat = r"\.[a-z]+(?:/|$)" 
tld_re = re.compile(tld_pat)
 
########################################################################################
def tld_features(df, columns, add_prefix=True):
    """
        Given a pandas dataframe and a set of column names.
        calculate the tld features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_tld_features(rez, col, add_prefix)
    return rez

########################################################################################
def add_tld_features(df, col, add_prefix=True):
    """
        Given a pandas dataframe and a column name.
        add simple text match features for tld.
    """

    def ext_features(x, col):
        freq = 0
        type = 0
        tld = ""
        if x[col]!=x[col]:
            freq = 0
            type = 0
        else:
            url = (x[col])
            exts = tld_re.findall(url)
            if len(exts) > 0:
                tld = exts[0].replace('.', '').replace('/','')
                freq, type = top_level_domain_lookup(tld)
        return tld, freq, type


    if add_prefix:
        col_names = [ col+'_tld_name', col+'_tld_freq', col+'_tld_type' ]
    else:
        col_names = [  'tld_name', 'tld_freq', 'tld_type' ]

    df[ col_names ] = df.apply(ext_features, col=col, axis=1, result_type="expand")

    return df
 
########################################################################################
def top_level_domain_lookup(ext):
    """
        Given a top level domain returns its frequency and type
    """
    if ext in tld_freqs:
       freq = tld_freqs[ext]
    else:
       freq = min(tld_freqs.values())

    if ext in tld_types:
       typer = tld_types[ext]
       if typer == "generic":
           type=4
       elif typer == "country-code":
           type=3
       else:
           type=2
    else:
       type = 1
    
    return freq, type

