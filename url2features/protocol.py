# -*- coding: utf-8 -*-
import pandas as pd 
import numpy as np
import math
import os
import re

from .process import load_word_list

"""
    url2features.protocol: Feature from URL protocol
"""

########################################################################################
def protocol_features(df, columns, add_prefix=True):
    """
        Given a pandas dataframe and a set of column names.
        calculate the simple text summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_protocol_features(rez, col, add_prefix)
    return rez

########################################################################################
def add_protocol_features(df, col, add_prefix):
    """
        Given a pandas dataframe and a column name.
        calculate the protocol features 
    """
    def extract_protocol(x):
       x = str(x)
       parts = x.split("://")
       if len(parts)>1:
          return parts[0]
       else:
          return "None"

    prots = df[col].apply(extract_protocol)
    if add_prefix:
        col_name = col + "_protocol"
    else:
        col_name = "protocol"
    df[col_name] = prots

    if add_prefix:
        col_name = col + "_protocol_exists"
    else:
        col_name = "protocol_exists"
    existance = [int(p!="None") for p in prots]
    df[col_name] = existance

    def get_protocol_type(prot):
       if prot in ['http','https','shttp']:
          return "web"
       elif  prot in ['file','ftp','smb','sftp','s3']:
          return "file"
       elif prot in ['pop', 'smtp', 'imap']:
          return "mail"
       elif prot in ['nntp',]:
          return "discussion"
       elif prot in ['mms','lastfm','udp','rtsp','rtmfp']:
          return "media"
       elif prot in ['ldap','snmp','rsync']:
          return "util"
       elif prot in ['telnet','ssh']:
          return "terminal"
       elif prot in ['irc', 'irc6','ircs', 'rtmp']:
          return "chat"
       elif prot in ['ipps','ipp']:
          return "print"
       elif prot in ['steam','teamspeak']:
          return "gaming"
       elif prot in ['git','cvs','svn']:
          return "src"
       else:
           return "unkown"

    if add_prefix:
        col_name = col + "_protocol_type"
    else:
        col_name = "protocol_type"
    types = [get_protocol_type(p) for p in prots]
    df[col_name] = types

    def secure_protocol(prot):
       if prot in ['sftp','https','shttp','ssh', 'ircs','ipps']:
          return 1
       else:
          return 0

    if add_prefix:
        col_name = col + "_protocol_secure"
    else:
        col_name = "protocol_secure"
    secure = [secure_protocol(p) for p in prots]
    df[col_name] = secure
    return df

########################################################################################


