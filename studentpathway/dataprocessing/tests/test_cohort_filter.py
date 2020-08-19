from studentpathway.dataprocessing.cohort_filter import cohort_filter
import pandas as pd
import datetime
import pytest

PATH = "studentpathway/dataprocessing/tests/test_data_files/test_cohort"

data = PATH + "/test_data.csv"
unit_list = PATH + "/test_engineering_units.csv"

def test_cohort_filter1():
    with pytest.raises(Exception):
        filtered_data = cohort_filter()

def test_cohort_filter2():
    filtered_data = cohort_filter(data, "Engineering")
    assert(isinstance(filtered_data, pd.DataFrame))

def test_cohort_filter3():
    filtered_data = cohort_filter(data, "Engineering")
    assert(filtered_data.shape == (9,8))
    assert(isinstance(filtered_data.outcome_date[0], datetime.date))

def test_cohort_filter4():
    filtered_data = cohort_filter(data, "Engineering",unit_list=unit_list)
    assert(filtered_data.shape == (8,8))

def test_cohort_filter5():
    filtered_data = cohort_filter(data, "Bachelor of Science")
    assert(filtered_data.shape == (1,8))

def test_cohort_filter6():
    filtered_data = cohort_filter(data, "Science", exclusive_search=False)
    assert(filtered_data.shape == (4,8))

def test_cohort_filter7():
    filtered_data = cohort_filter(data, "Science",unit_list=unit_list, exclusive_search=False)
    assert(filtered_data.shape == (3,8))
