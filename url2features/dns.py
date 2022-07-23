# -*- coding: utf-8 -*-
import pandas as pd 
from urllib import parse
import numpy as np
import geocoder
import math
import dns 
import os
import re

"""
    url2features.dns: Features based on the DNS records
"""

########################################################################################
def dns_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the DNS summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_dns_features(rez, col)
    return rez


########################################################################################
def add_dns_features(df, col):
    """
        Given a pandas dataframe and a column name containing a URL
        calculate the DNS features 
    """
    def ip_features(x, col):
        if x[col]!=x[col]:
            val = 0
            ptr = 0
            spf = 0
            country = ""
        else:
            url = (x[col])
            _dns_response = dns.resolver.query(url, 'TXT')
            val = 0
            ptr = 0
            spf = 0
            country = get_country(url)
        return val, ptr, spf, country

    df[[ col+'_dns_valid', col+'_dns_ptr', col+'_dns_spf', col+'_dns_country' ]] = df.apply(dns_features, col=col, axis=1, result_type="expand")

    return df


########################################################################################
def get_country(url):
    """Return the country associated with IP."""
    try:
        ip = resolver.query(url, 'A')
        ip = ip[0].to_text()

        if ip:
            coded = geocoder.ip(ip)
            return coded.country
        else:
            return '?'

    except Exception:
        return '?'


def split_url(url):
    """Split URL into: protocol, host, path, params, query and fragment."""
    if not parse.urlparse(url.strip()).scheme:
        url = 'http://' + url
    protocol, host, path, params, query, fragment = parse.urlparse(url.strip())
    result = {
        'url': host + path + params + query + fragment,
        'protocol': protocol,
        'host': host,
        'path': path,
        'params': params,
        'query': query,
        'fragment': fragment
    }
    return result

