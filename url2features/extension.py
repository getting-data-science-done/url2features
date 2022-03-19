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
extension_pat = load_word_pattern('extension.dat')
extension_re = re.compile(extension_pat)
 
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
            exts = extension_re.findall(url)
            if len(exts) > 0:
                freq, type = extension_lookup(ext[0])
        return freq, type

    df[[ col+'_ext_freq', col+'_ext_type' ]] = df.apply(ext_features, col=col, axis=1, result_type="expand")

    return df
 
########################################################################################
def extension_lookup(ext):
    """
        Given an extension returns its frequency and type
    """
    return 0, 0

