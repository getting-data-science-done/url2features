import sys
import pytest
import pandas as pd
import numpy as np
from url2features.process import padded
from url2features.process import extract_file_extension
from url2features.process import isNaN

from url2features.simple import simple_features

from url2features.extension import top_level_domain_lookup

from url2features.domain import extract_full_domain
from url2features.domain import get_subdomain_type
from url2features.domain import get_subdomain_freq

from url2features.registration import get_registration_year

def test_padded():
    strrez = padded("sdf", 20)
    assert len(strrez) == 20
    strrez = padded("sdf", 30)
    assert len(strrez) == 30

def test_isNaN():
    assert isNaN(20) == False
    assert isNaN(20.0) == False
    assert isNaN(np.nan) == True

def test_simple():
    df = pd.DataFrame({'ID':[1,2,3], "url":["http://example.com", "http://example.com/","example.com"]})
    rez =  simple_features(df, ["url"])
    assert rez["url_length"][0] == 18
    assert rez["url_length"][1] == 19
    assert rez["url_length"][2] == 11
    assert rez["url_depth"][0] == 1
    assert rez["url_depth"][1] == 1
    assert rez["url_depth"][2] == 1

def test_domain_features():
    freq, type = top_level_domain_lookup("com")
    assert type == 4
    freq, type = top_level_domain_lookup("au")
    assert type == 3

def test_domain_extract():
    dom = extract_full_domain("https://www.smh.com.au/sydney-news")
    assert dom == "www.smh.com.au"

def test_subdomain_type():
    f = get_subdomain_type("www")
    assert f == 6

def test_subdomain_freq():
    f = get_subdomain_freq("www")
    assert f > 0

def test_get_registration_year():
    f = get_registration_year("google.com")
    assert f == 1997


