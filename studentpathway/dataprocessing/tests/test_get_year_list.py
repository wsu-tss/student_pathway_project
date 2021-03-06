from studentpathway.dataprocessing.get_year_list import get_year_list
import pytest

def test_get_year_list1():
    years = get_year_list("studentpathway/dataprocessing/tests/test_data_files/test_year")
    assert (years == [2015, 2016, 2017])

def test_get_year_list2():
    with pytest.raises(Exception):
        years = get_year_list('test')

def test_get_year_list3():
    with pytest.raises(Exception):
        years = get_year_list()
