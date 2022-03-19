# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os
import re

from .process import load_word_list
from .process import load_word_pattern

"""
    url2features.extension: Domain extension feature flags

    Generate features for common domain extensions

"""

########################################################################################
tld_pat =  "\.[a-z]+(?:/|$)" 
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
                freq, type = top_level_domain_lookup(ext[0])
        return freq, type

    df[[ col+'_tld_freq', col+'_tld_type' ]] = df.apply(ext_features, col=col, axis=1, result_type="expand")

    return df
 
########################################################################################
def top_level_domain_lookup(ext):
    """
        Given a top level domain returns its frequency and type
    """
    return 0, 0

