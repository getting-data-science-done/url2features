# -*- coding: utf-8 -*-
import functools
import pandas as pd 
import numpy as np

from .process import start_profile
from .process import end_profile
from .simple import simple_features
from .protocol import protocol_features
from .host import host_features
from .tld import tld_features
from .file import file_features
from .path import path_features
from .params import params_features
from .dns import dns_features

"""
    url2features.featurize: Core functions to apply a set of features to a data frame.
"""
########################################################################################

def process_df(df, params):
    """ 
    process_df: Function that co-ordinates the process of generating the features
    
    """ 
    add_prefix = params["prefix"]
    if params["simple"] :
        start_profile("simple")
        df = simple_features( df, params["columns"], add_prefix )
        end_profile("simple")
    if params["protocol"] :
        start_profile("protocol")
        df = protocol_features( df, params["columns"], add_prefix )
        end_profile("protocol")
    if params["host"] :
        start_profile("host")
        df = host_features( df, params["columns"], add_prefix )
        end_profile("host")
    if params["tld"] :
        start_profile("tld")
        df = tld_features( df, params["columns"], add_prefix )
        end_profile("tld")
    if params["path"] :
        start_profile("path")
        df = path_features( df, params["columns"], add_prefix )
        end_profile("path")
    if params["file"] :
        start_profile("file")
        df = file_features( df, params["columns"], add_prefix )
        end_profile("file")
    if params["params"] :
        start_profile("params")
        df = params_features( df, params["columns"], add_prefix )
        end_profile("params")
    if params["dns"] :
        start_profile("dns")
        df = dns_features( df, params["columns"], add_prefix )
        end_profile("dns")
    return df

########################################################################################

def generate_feature_function(parameters):
    """
        This function will take the processed command line arguments that determine
        the feature to apply and partially apply them to the process_df function.
        Returning a function that can be used to apply those parameters to multiple
        chunks of a dataframe.
    """
    return functools.partial(process_df, params = parameters)

