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
def get_registration_year(domain)
    reg = get_domain_registration_date(domain)
    return reg.year


#########################################################################
def get_domain_registration_date(domain):
    if domain in dom_reg:
      return dom_reg[domain]
    else:
      try:
        w2 = whois.whois(dom)
        if isinstance(w2.creation_date, list):
            created = w2.creation_date[0]
        else:
            created = w2.creation_date

        if isinstance(created, datetime):
            return created
        else:
            return np.nan
      except:
            return np.nan


