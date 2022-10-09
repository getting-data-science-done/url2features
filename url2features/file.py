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
from .process import add_protocol_if_missing

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

def remove_extension(file_name):
    file_parts = file_name.split(".")
    if len(file_parts) > 1:
        return file_name[0:-(len(file_parts[-1])+1)]
    else:
        return file_name

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
        file_len = 0
        file_wds = 0
        file_wd_len = 0
        file_1st_wd_prefix = ""
        file_1st_wd = ""
        if x[col]==x[col]:
            url = add_protocol_if_missing(x[col])
            protocol, host, path, params, query, fragment = parse.urlparse(url.strip())
            sections = path.split("/")
            final_file = sections[len(sections)-1]
            file_len = len(final_file)
            file_1st_wd_prefix, file_1st_wd, file_wds, file_wd_len = extract_word_stats( remove_extension(final_file) )
            file_parts = final_file.split(".")
            if len(file_parts) > 1:
                ext = file_parts[len(file_parts)-1].lower()
                type = file_extension_lookup(ext)
                existance = 1
        return file_len, file_1st_wd_prefix, file_1st_wd, file_wds, file_wd_len, ext, type, existance

    if add_prefix:
        col_names = [ col+'_file_len', col+"_file_1st_wd_prefix", col+"_file_1st_wd", col+'_file_wd_count', col+'_file_wd_len', 
                      col+'_file_extn', col+'_file_extn_type', col+'_file_extn_exists', ] 
    else:
        col_names = [ 'file_len', "file_1st_wd_prefix", "file_1st_wd", 'file_wd_count', 'file_wd_len', 
                      'file_extn', 'file_extn_type', 'file_extn_exists' ]

    df[ col_names ] = df.apply(get_file_features, col=col, axis=1, result_type="expand")

    return df

########################################################################################
def extract_word_stats(path):
   wds = re.split("[-_/~]+", path)
   wd_len = np.mean([len(w) for w in wds])
   my_wds = [w for w in wds if len(w)>2]
   if len(my_wds)>0:
      fst_wd = my_wds[0]
   else:
      fst_wd = ""
   if len(fst_wd)>3:
      fst_wd_pre = fst_wd[0:3]
   else:
      fst_wd_pre = fst_wd

   return fst_wd_pre.lower(), fst_wd.lower(), sum([1 for w in wds if len(w)>2]), wd_len


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
