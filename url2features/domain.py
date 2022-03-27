# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os
import re

"""
    url2features.domain: Domain domain feature flags
    Generate features for domains
"""

from .suffixes import split_domain_and_suffix
from .process import load_dictionary

subdomain_types = load_dictionary('subdomain_types.dat')
subdomain_freqs = load_dictionary('subdomain_freqs.dat')
 
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
def extract_full_domain(url):
    url = url.strip()
    prot = re.findall("https?://", url)
    if len(prot)>0:
        url = url[len(prot[0]):]
    parts = url.split("/")
    url = parts[0]
    return url

########################################################################################
def get_subdomain_type(sub):
    if sub in subdomain_types:
        return subdomain_types[sub]
    else:
        return 0

########################################################################################
def get_subdomain_freq(sub):
    if sub in subdomain_freqs:
        return subdomain_freqs[sub]
    else:
        return 0.0
    
########################################################################################
def add_domain_features(df, col):
    """
        Given a pandas dataframe and a column name.
        add features for the domain:
        -- The number of sections in the domain
        -- The type of the subdomain
        -- The frequency of the subdomain
        Note: We use the value -1 to indicate that the subdomain is missing
              Where 0 is reserved for a subdomain that is present but unknown
    """

    def dom_features(x, col):
        if x[col]!=x[col]:
            secs = 0
            sub_type = -1
            sub_freq = -1
        else:
            domain = extract_full_domain(x[col])
            parts = domain.split(".")
            secs = len(parts)
            prime, suffix = split_domain_and_suffix(domain)
            parts = prime.split(".")
            if len(parts) > 1:
                sub_type = get_subdomain_type(parts[0])
                sub_freq = get_subdomain_freq(parts[0])
            else:
                sub_type = -1
                sub_freq = -1

        return secs, sub_type, sub_freq

    df[[ col+'_domain_sections', col+'_subdomain_type', col+'_subdomain_freq'  ]] = df.apply(dom_features, col=col, axis=1, result_type="expand")

    return df
 

