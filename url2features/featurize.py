# -*- coding: utf-8 -*-
import functools
import pandas as pd 
import numpy as np

from .process import start_profile
from .process import end_profile
from .simple import simple_features
from .domain import domain_features
from .extension import extension_features
from .file import file_features

"""
    url2features.featurize: Core functions to apply a set of features to a data frame.
"""
########################################################################################

def process_df(df, params):
    """ 
    process_df: Function that co-ordinates the process of generating the features
    
    """ 
    if params["simple"] :
        start_profile("simple")
        df = simple_features( df, params["columns"] )
        end_profile("simple")
    if params["file"] :
        start_profile("file")
        df = file_features( df, params["columns"] )
        end_profile("file")
    if params["domain"] :
        start_profile("domain")
        df = domain_features( df, params["columns"] )
        end_profile("domain")
    if params["extension"] :
        start_profile("extension")
        df = extension_features( df, params["columns"] )
        end_profile("extension")
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

