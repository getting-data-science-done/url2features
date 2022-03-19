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
    url2features.domain: Domain domain feature flags

    Generate features for domains

"""

########################################################################################
domain_pat = load_word_pattern('domain.dat')
domain_re = re.compile(domain_pat)
 
########################################################################################
def domain_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the domain features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_domain_features(rez, col)
    return rez

########################################################################################
def add_domain_features(df, col):
    """
        Given a pandas dataframe and a column name.
        add simple text match features for domain.
    """

    def ext_features(x, col):
        freq = 0
        type = 0
        if x[col]!=x[col]:
            freq = 0
            type = 0
        else:
            url = (x[col])
            exts = domain_re.findall(url)
            if len(exts) > 0:
                freq, type = domain_lookup(ext[0])
        return freq, type

    df[[ col+'_ext_freq', col+'_ext_type' ]] = df.apply(ext_features, col=col, axis=1, result_type="expand")

    return df
 
########################################################################################
def domain_lookup(ext):
    """
        Given an domain returns its frequency and type
    """
    return 0, 0

