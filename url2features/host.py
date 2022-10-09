# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import string
import numpy as np
import math
import sys
import os
import re

"""
    url2features.host: Host feature flags
    Generate features for host including domain, subdomain elements
"""

from .suffixes import split_domain_and_suffix
from .process import load_dictionary
from .registration import get_registration_year

subdomain_types = load_dictionary('subdomain_types.dat')
subdomain_freqs = load_dictionary('subdomain_freqs.dat')
 
country_codes = ['af', 'ax', 'al', 'dz', 'as', 'ad', 'ao', 'ai', 'aq', 'ag', 'ar', 'am', 'aw', 'au', 'at', 'az', 'bs', 'bh', 'bd', 'bb', 'by', 'be', 'bz', 'bj', 'bm', 'bt', 'bo', 'bq', 'ba', 'bw', 'bv', 'br', 'io', 'bn', 'bg', 'bf', 'bi', 'cv', 'kh', 'cm', 'ca', 'ky', 'cf', 'td', 'cl', 'cn', 'cx', 'cc', 'co', 'km', 'cg', 'cd', 'ck', 'cr', 'ci', 'hr', 'cu', 'cw', 'cy', 'cz', 'dk', 'dj', 'dm', 'do', 'ec', 'eg', 'sv', 'gq', 'er', 'ee', 'et', 'fk', 'fo', 'fj', 'fi', 'fr', 'gf', 'pf', 'tf', 'ga', 'gm', 'ge', 'de', 'gh', 'gi', 'gr', 'gl', 'gd', 'gp', 'gu', 'gt', 'gg', 'gn', 'gw', 'gy', 'ht', 'hm', 'va', 'hn', 'hk', 'hu', 'is', 'in', 'id', 'ir', 'iq', 'ie', 'im', 'il', 'it', 'jm', 'jp', 'je', 'jo', 'kz', 'ke', 'ki', 'kp', 'kr', 'kw', 'kg', 'la', 'lv', 'lb', 'ls', 'lr', 'ly', 'li', 'lt', 'lu', 'mo', 'mk', 'mg', 'mw', 'my', 'mv', 'ml', 'mt', 'mh', 'mq', 'mr', 'mu', 'yt', 'mx', 'fm', 'md', 'mc', 'mn', 'me', 'ms', 'ma', 'mz', 'mm', 'na', 'nr', 'np', 'nl', 'nc', 'nz', 'ni', 'ne', 'ng', 'nu', 'nf', 'mp', 'no', 'om', 'pk', 'pw', 'ps', 'pa', 'pg', 'py', 'pe', 'ph', 'pn', 'pl', 'pt', 'pr', 'qa', 're', 'ro', 'ru', 'rw', 'bl', 'sh', 'kn', 'lc', 'mf', 'pm', 'vc', 'ws', 'sm', 'st', 'sa', 'sn', 'rs', 'sc', 'sl', 'sg', 'sx', 'sk', 'si', 'sb', 'so', 'za', 'gs', 'ss', 'es', 'lk', 'sd', 'sr', 'sj', 'sz', 'se', 'ch', 'sy', 'tw', 'tj', 'tz', 'th', 'tl', 'tg', 'tk', 'to', 'tt', 'tn', 'tr', 'tm', 'tc', 'tv', 'ug', 'ua', 'ae', 'gb', 'us', 'um', 'uy', 'uz', 'vu', 've', 'vn', 'vg', 'vi', 'wf', 'eh', 'ye', 'zm', 'zw']

language_codes = ['ab', 'aa', 'af', 'ak', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'av', 'ae', 'ay', 'az', 'bm', 'ba', 'eu', 'be', 'bn', 'bh', 'bi', 'bs', 'br', 'bg', 'my', 'ca', 'ch', 'ce', 'ny', 'zh', 'cv', 'kw', 'co', 'cr', 'hr', 'cs', 'da', 'dv', 'nl', 'dz', 'en', 'eo', 'et', 'ee', 'fo', 'fj', 'fi', 'fr', 'ff', 'gl', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'he', 'hz', 'hi', 'ho', 'hu', 'ia', 'id', 'ie', 'ga', 'ig', 'ik', 'io', 'is', 'it', 'iu', 'ja', 'jv', 'kl', 'kn', 'kr', 'ks', 'kk', 'km', 'ki', 'rw', 'ky', 'kv', 'kg', 'ko', 'ku', 'kj', 'la', 'lb', 'lg', 'li', 'ln', 'lo', 'lt', 'lu', 'lv', 'gv', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mh', 'mn', 'na', 'nv', 'nb', 'nd', 'ne', 'ng', 'nn', 'no', 'ii', 'nr', 'oc', 'oj', 'cu', 'om', 'or', 'os', 'pa', 'pi', 'fa', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru', 'sa', 'sc', 'sd', 'se', 'sm', 'sg', 'sr', 'gd', 'sn', 'si', 'sk', 'sl', 'so', 'st', 'es', 'su', 'sw', 'ss', 'sv', 'ta', 'te', 'tg', 'th', 'ti', 'bo', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 'ur', 'uz', 've', 'vi', 'vo', 'wa', 'cy', 'wo', 'fy', 'xh', 'yi', 'yo', 'za', 'zu']


########################################################################################
def host_features(df, columns, add_prefix=True):
    """
        Given a pandas dataframe and a set of column names.
        calculate the host features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_host_features(rez, col, add_prefix)
    return rez

########################################################################################
def extract_full_host(url):
    url = url.strip()
    prot = re.findall("^[a-zA-Z][a-zA-Z]*://", url)
    if len(prot)>0:
        url = url[len(prot[0]):]
    parts = url.split("/")
    domain = parts[0]
    return domain

def remove_port(url):
    url = str(url)
    return re.sub(':[0-9]*', '', url)

########################################################################################
def get_subdomain_type(sub):
    if sub in subdomain_types:
        return subdomain_types[sub]
    elif sub in country_codes:
        return 7
    elif sub in language_codes:
        return 8
    else:
        return 0

########################################################################################
def get_subdomain_freq(sub):
    if sub in subdomain_freqs:
        return subdomain_freqs[sub]
    else:
        return 0.0

########################################################################################
def host_is_ip(domain):
    """
    Function to detect if a string is an IP address rather than a domain name
    Srtictly speaking this function should be more restrictive -- To test if the sequence
     of numbers is a real IP. But for our purposes even a malformed IP should be flagged
     as an IP address.
    TODO: Add IPV6 Support
    """
    domain = str(domain).strip()
    temp1 = domain.replace(".", "")
    temp2 = temp1.replace(":", "")
    if temp2.isdecimal():
        return 1
    else:
        return 0

########################################################################################
def host_has_port(domain):
    """
    Function to detect if a domain string contains a port number
    """
    if domain.count(':')==1:
        return 1
    elif domain.count(']:') == 1:
        return 1
    else:
        return 0

########################################################################################
def add_host_features(df, col, add_prefix=True):
    """
        Given a pandas dataframe and a column name.
        add features for the domain:
        -- The number of sections in the domain
        -- The type of the subdomain
        -- The frequency of the subdomain
        Note: We use the value -1 to indicate that the subdomain is missing
              Where 0 is reserved for a subdomain that is present but unknown
    """
    count = lambda l1,l2: sum([1 for x in l1 if x in l2])

    def dom_features(x, col):
        url = str(x[col]).strip()
        if (url == 'None') or (url == 'nan') or (url==""):
            is_ip = np.nan
            has_port = np.nan
            secs = np.nan
            dom_len = np.nan
            dom_alpha = np.nan
            subbie = np.nan
            sub_type = np.nan
            sub_freq = np.nan
            reg_year = np.nan
        else:
            host = extract_full_host(x[col])
            is_ip = host_is_ip(host)
            has_port = host_has_port(host)
            if has_port:
                host = remove_port(host)
            parts = host.split(".")
            secs = len(parts)
            if is_ip:
                subbie = ""
                dom_len = np.nan
                dom_alpha = np.nan
                sub_type = np.nan
                sub_freq = np.nan
                reg_dom = host
            else:
                prime, suffix = split_domain_and_suffix(host)
                parts = prime.split(".")
                if len(parts) > 1:
                    dom_len = len(parts[-1])
                    if dom_len > 0:
                        dom_alpha = count(parts[-1], string.ascii_lowercase)/dom_len
                    else:
                        dom_alpha = np.nan
                    subbie = ".".join(parts[0:-1]).lower()
                    sub_type = get_subdomain_type(subbie)
                    sub_freq = get_subdomain_freq(subbie)
                    reg_dom = prime[len(subbie)+1:] + suffix
                else:
                    subbie = ""
                    dom_len = len(prime)
                    if dom_len > 0:
                        dom_alpha = count(prime, string.ascii_lowercase)/dom_len
                    else:
                        dom_alpha = np.nan
                    sub_type = -1
                    sub_freq = -1
                    reg_dom = host
            if is_ip:
                reg_year = np.nan
            else:
                reg_year = get_registration_year(reg_dom)

        return secs, dom_len, dom_alpha, subbie, is_ip, has_port, sub_type, sub_freq, reg_year

    if add_prefix:
        col_names = [ col+'_domain_sections', col+'_domain_len', col+'_domain_alpha', col+'_subdomain', col+'_host_is_ip', col+'_host_has_port', 
                      col+'_subdomain_type', col+'_subdomain_freq', col+'_domain_reg_year'  ]
    else:
        col_names = [ 'domain_sections', 'domain_len', 'subdomain', 'host_is_ip', 'host_has_port', 'subdomain_type', 'subdomain_freq', 'domain_reg_year'  ]

    df[ col_names ] = df.apply(dom_features, col=col, axis=1, result_type="expand")

    return df
 

