from data_processing_methods import get_year_list
import pandas as pd
import numpy as np
import pytest
import os

def test_get_year_list1():
    years = get_year_list("data_processing_methods/tests/test_data_files/test_year")
    assert (years == [2015, 2016, 2017])

def test_get_year_list2():
    with pytest.raises(Exception):
        years = get_year_list('test')

def test_get_year_list3():
    with pytest.raises(Exception):
        years = get_year_list()
