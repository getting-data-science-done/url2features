# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import whois

"""
    url2features.registration: Domain registration features
"""
from .process import load_dictionary

dom_reg = load_dictionary('dom_reg.dat')
 
#########################################################################
def get_registration_year(domain):
    #print("FUNCTION CALL: get_registration_year(", domain, ")")
    reg = get_domain_registration_date(domain)
    if reg:
      try:
        return int(reg[0:4])
      except:
        return np.nan
    else:
        return np.nan

#########################################################################
def get_domain_registration_date(domain):
    if domain in dom_reg:
      return dom_reg[domain]
    else:
      try:
        w2 = whois.whois(domain)
        if isinstance(w2.creation_date, list):
            created = w2.creation_date[0]
        else:
            created = w2.creation_date
        return str(created)
      except:
            return ""


