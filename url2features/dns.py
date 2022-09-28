# -*- coding: utf-8 -*-
from dns import resolver, reversename
from urllib import parse
import pandas as pd 
import numpy as np
import ipaddress
import geocoder
import math
import os
import re

"""
    url2features.dns: Features based on the DNS records

    This module borrows heavily from URL Feature Extractor 
    by Lucas Ayres : https://www.lucasayres.com.br
    Code taken and modified from
    https://github.com/lucasayres/url-feature-extractor
"""

########################################################################################
def dns_features(df, columns, add_prefix=True):
    """
        Given a pandas dataframe and a set of column names.
        calculate the DNS summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_dns_features(rez, col, add_prefix)
    return rez


########################################################################################
def add_dns_features(df, col, add_prefix=True):
    """
        Given a pandas dataframe and a column name containing a URL
        calculate the DNS features 
    """
    def dns_feature_gen(x, col):
        if x[col]!=x[col]:
            ns = 0
            mx = 0
            spf = 0
            ptr = 0
            country = ""
        else:
            url = (x[col])
            url_parts = split_url_into_parts(url)
            ns = count_name_servers(url_parts)
            mx = count_mx_servers(url_parts)
            spf = 0
            ptr = get_ptr(url_parts)
            country = get_country(url_parts)
        return ns, mx, ptr, country

    if add_prefix:
        col_names = [ col+'_dns_ns', col+'_dns_mx', col+'_dns_ptr', col+'_dns_country' ]
    else:
        col_names = [ 'dns_ns', 'dns_mx', 'dns_ptr', 'dns_country' ]

    df[ col_names ] = df.apply(dns_feature_gen, col=col, axis=1, result_type="expand")

    return df


########################################################################################
def valid_ip(host):
    """Return if the domain has a valid IP format (IPv4 or IPv6)."""
    try:
        ipaddress.ip_address(host)
        return True
    except Exception:
        return False

########################################################################################
def count_ips(url_parts):
    """Return the number of resolved IPs (IPv4)."""
    if valid_ip(url_parts['host']):
        return 1
    try:
        answers = resolver.query(url_parts['host'], 'A')
        return len(answers)
    except Exception:
        return '?'

########################################################################################
def count_name_servers(url_parts):
    """Return number of NameServers (NS) resolved."""
    count = 0
    if count_ips(url_parts):
        try:
            answers = resolver.query(url_parts['host'], 'NS')
            return len(answers)
        except (resolver.NoAnswer, resolver.NXDOMAIN):
            split_host = url_parts['host'].split('.')
            while len(split_host) > 0:
                split_host.pop(0)
                supposed_domain = '.'.join(split_host)
                try:
                    answers = resolver.query(supposed_domain, 'NS')
                    count = len(answers)
                    break
                except Exception:
                    count = 0
        except Exception:
            count = 0
    return count

########################################################################################
def count_mx_servers(url_parts):
    """Return Number of Resolved MX Servers."""
    count = 0
    if count_ips(url_parts):
        try:
            answers = resolver.query(url_parts['host'], 'MX')
            return len(answers)
        except (resolver.NoAnswer, resolver.NXDOMAIN):
            split_host = url_parts['host'].split('.')
            while len(split_host) > 0:
                split_host.pop(0)
                supposed_domain = '.'.join(split_host)
                try:
                    answers = resolver.query(supposed_domain, 'MX')
                    count = len(answers)
                    break
                except Exception:
                    count = 0
        except Exception:
            count = 0
    return count

########################################################################################
def get_ptr(url_parts):
    """Return PTR associated with IP."""
    try:
        if valid_ip(url_parts['host']):
            ip = url_parts['host']
        else:
            ip = resolver.query(url_parts['host'], 'A')
            ip = ip[0].to_text()

        if ip:
            r = reversename.from_address(ip)
            result = resolver.query(r, 'PTR')[0].to_text()
            return result
        else:
            return '?'
    except Exception:
        return '?'

########################################################################################
def get_country(url_parts):
    """Return the country associated with IP."""
    try:
        if valid_ip(url_parts['host']):
            ip = url_parts['host']
        else:
            ip = resolver.query(url_parts['host'], 'A')
            ip = ip[0].to_text()

        if ip:
            coded = geocoder.ip(ip)
            return coded.country
        else:
            return '?'

    except Exception:
        return '?'


########################################################################################
def split_url_into_parts(url):
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

