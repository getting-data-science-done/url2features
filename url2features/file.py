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
def file_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the file type summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_file_features(rez, col)
    return rez

########################################################################################
def add_file_features(df, col):
    """
        Given a pandas dataframe and a column name.
        calculate the file features 
    """
    def file_features(x, col):
        freq = 0
        type = 0
        ext = ""
        if x[col]!=x[col]:
            freq = 0
            type = 0
        else:
            url = (x[col])
            protocol, host, path, params, query, fragment = parse.urlparse(url.strip())
            sections = path.split(".")
            if len(sections) > 1:
                ext = sections[1]
                type = file_extension_lookup(ext)
        return ext, freq, type

    df[[ col+'_file_extension', col+'_file_ext_type' ]] = df.apply(file_features, col=col, axis=1, result_type="expand")

    return df

########################################################################################
def file_extension_lookup(ext):
    """
        Given a file extension returns the type
    """
    if ext in extension_types:
        return extension_types[ext]
    else:
        return "Unknown"

########################################################################################
def file_extension_lookup_old(ext):
    """
        Given a file extension returns its frequency and type
    """
    if ext in extension_types:
       typer = ext_types[ext]
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
