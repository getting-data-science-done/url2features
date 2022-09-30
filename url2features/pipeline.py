from sklearn.base import TransformerMixin, BaseEstimator
import pandas as pd
import numpy as np
import re

from .featurize import generate_feature_function

class URLTransform(TransformerMixin, BaseEstimator):
    """
        This class implements a SciKit Learn compatible Transformer for
         converting a column containing a URL into a series of numeric values.
         You specify the transformations you want as an array of named
         feature groups.

        columns: Array(String) Names of the text columns to process.
        transforms: Array(String) Names of the feature sets to generate
                     Options: simple, domain, extension
    """

    def __init__(self, columns, transforms=['simple']):
        self.transforms = transforms
        self.columns = columns
        self.config = self.generate_feature_config(columns, transforms)
        self.func = generate_feature_function(self.config)
        

    def fit(self, X, y=None, **fit_params):
        return self
    
    def transform(self, X, y=None, **transform_params):
        """
            Transform the matrix of values
             -- need to deal with single or multiple columns
        """
        rez = self.func(X)        

        # Might need this later 
        #if X.__class__.__name__ == "DataFrame":
        #    X = X.values

        # REMOVE THE TEXT COLUMNS -- PARAMETERIZE THIS LATER
        for col in self.columns:
            rez.drop(col, inplace=True, axis=1)

        return rez 


    #############################################################
    def generate_feature_config(self, columns, params):
        """
        We need to process the params into a particular data structure 
        for the dataframe processing function to recognize. 
        """
        result = {
              "columns":columns,
              "simple":False,
              "protocol":False,
              "host":False,
              "tld":False,
              "path":False,
              "file":False,
              "params":False,
              "dns":False,
        }
        if "simple" in params:
           result["simple"]=True
        if "protocol":
           result["protocol"]=True
        if "host" in params:
           result["host"]=True
        if "tld" in params:
           result["tld"]=True
        if "path" in params:
           result["path"]=True
        if "file" in params:
           result["file"]=True
        if "params" in params:
           result["params"]=True
        if "dns" in params:
           result["dns"]=True

        return result

