import sys
import pytest
import pandas as pd
import numpy as np
from url2features.process import padded
from url2features.process import extract_file_extension
from url2features.process import isNaN

from url2features.simple import simple_features

from url2features.extension import top_level_domain_lookup

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

