# -*- coding: utf-8 -*-
from urllib import parse
import pkg_resources
import pandas as pd
import numpy as np
import math
import os
import re


"""
    url2features.file: Features based on the file type.
"""
from .process import load_dictionary

extension_types = load_dictionary('file_extensions.dat')

########################################################################################
def file_features(df, columns, add_prefix=True):
    """
        Given a pandas dataframe and a set of column names.
        calculate the file type summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_file_features(rez, col, add_prefix)
    return rez

########################################################################################
def add_file_features(df, col, add_prefix):
    """
        Given a pandas dataframe and a column name.
        calculate the file features 
    """
    def get_file_features(x, col):
        ext = ""
        type = ""
        existance = 0
        if x[col]==x[col]:
            url = (x[col])
            protocol, host, path, params, query, fragment = parse.urlparse(url.strip())
            sections = path.split(".")
            if len(sections) > 1:
                ext = sections[1]
                type = file_extension_lookup(ext)
                existance = 1
        return ext, type, existance

    if add_prefix:
        col_names = [ col+'_file_extn', col+'_file_extn_type', col+'_file_extn_exists', ] 
    else:
        col_names = [ 'file_extn', 'file_extn_type', 'file_extn_exists' ]

    df[ col_names ] = df.apply(get_file_features, col=col, axis=1, result_type="expand")

    return df

########################################################################################
def file_extension_lookup(ext):
    """
        Given a file extension returns the type
    """
    if ext in extension_types:
        return extension_types[ext]
    else:
        return ""

########################################################################################
def file_extension_lookup_old(ext):
    """
        Given a file extension returns its frequency and type
    """
    if ext in extension_types:
       typer = extension_types[ext]
       if typer == "static":
           type=1
       elif typer == "dynamic":
           type=2
       elif typer == "media":
           type=3
       else:
           type=4
    else:
       type = -1

    return type
