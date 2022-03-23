# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os
import re

from .process import load_dictionary

tld = load_dictionary('tld.dat')
domains = load_dictionary('domains.dat')

from .process import load_word_list
from .process import load_word_pattern

"""
    url2features.extension: Domain extension feature flags

    Generate features for common domain extensions

"""

########################################################################################
tld_pat = r"\.[a-z]+(?:/|$)" 
tld_re = re.compile(tld_pat)

extensions_pat = load_word_pattern('extensions.dat')
 
########################################################################################
def extension_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the extension features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_extension_features(rez, col)
    return rez

########################################################################################
def add_extension_features(df, col):
    """
        Given a pandas dataframe and a column name.
        add simple text match features for extension.
    """

    def ext_features(x, col):
        freq = 0
        type = 0
        if x[col]!=x[col]:
            freq = 0
            type = 0
        else:
            url = (x[col])
            exts = tld_re.findall(url)
            if len(exts) > 0:
                temp = ext[0].replace('.', '').replace('/','')
                freq, type = top_level_domain_lookup(temp)
        return freq, type

    df[[ col+'_tld_freq', col+'_tld_type' ]] = df.apply(ext_features, col=col, axis=1, result_type="expand")

    return df
 
########################################################################################
def top_level_domain_lookup(ext):
    """
        Given a top level domain returns its frequency and type
    """
    if ext in tld:
       freq = tld[ext]
    else:
       freq = min(lookup.values())

    if ext in domains:
       typer = domains[ext]
       if typer == "generic":
           type=4
       elif typer == "country-code":
           type=3
       else:
           type=2
    else:
       type = 1
    
    return freq, type

