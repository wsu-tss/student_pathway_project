from studentpathway.dataprocessing.filters import cohort_filter, grades_filter, get_data, categorical_filter
import pandas as pd
import numpy as np
import math
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
    assert(filtered_data.shape[0] == 9)
    assert(isinstance(filtered_data.outcome_date[0], datetime.date))

def test_cohort_filter4():
    filtered_data = cohort_filter(data, "Engineering",unit_list=unit_list)
    assert(filtered_data.shape[0] == 8)

def test_cohort_filter5():
    filtered_data = cohort_filter(data, "Bachelor of Science")
    assert(filtered_data.shape[0] == 1)

def test_cohort_filter6():
    filtered_data = cohort_filter(data, "Science", exclusive_search=False)
    assert(filtered_data.shape[0] == 4)

def test_cohort_filter7():
    filtered_data = cohort_filter(data, "Science", unit_list=unit_list, exclusive_search=False)
    assert(filtered_data.shape[0] == 3)

# grade_filter tests
def test_grades_filter1():
    with pytest.raises(Exception):
        filtered_data = grades_filter()

def test_grades_filter2():
    filtered_data = grades_filter(data)
    assert(filtered_data.shape[0] == 14)

def test_grades_filter3():
    grade_list = ['P', 'H', 'D', 'H', 'H', 'H', 'P', 'F', 'P', 'S', 'H', 'D', 'H', None]
    filtered_data = grades_filter(data)
    assert(filtered_data['grade'].tolist() == grade_list)

def test_grades_filter4():
    grade_list = ['P', 'H', 'D', 'H', 'H', 'H', 'P', 'X', 'P', 'S', 'H', 'D', 'H', None]
    filtered_data = grades_filter(data, avoid={'S', 'X'})
    assert(filtered_data['grade'].tolist() == grade_list)

def test_grades_filter5():
    filtered_data = grades_filter(data, grades={50: 'P', 0: 'F'}, avoid={'S'})
    grade_list = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'F', 'P', 'S', 'P', 'P', 'P', None]
    assert(filtered_data['grade'].tolist() == grade_list)

def test_grades_filter6():
    filtered_data = grades_filter(data, grades={50: 'P', 0: 'F'}, avoid={})
    grade_list = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'F', 'P', None, 'P', 'P', 'P', None]
    assert(filtered_data['grade'].tolist() == grade_list)
    assert(np.isnan(filtered_data['mark'].tolist()[9]))
    assert(np.isnan(filtered_data['mark'].tolist()[13]))

# tests for remove missing
def test_grades_filter7():
    filtered_data = grades_filter(data, grades={50: 'P', 0: 'F'}, remove_missing=True)
    assert(filtered_data.shape[0] == 13)

def test_grades_filter8():
    filtered_data = grades_filter(data, grades={50: 'P', 0: 'F'}, avoid={}, remove_missing=True)
    assert(filtered_data.shape[0] == 12)

def test_get_data0():
    data_df = pd.read_csv(data)
    filtered_data = get_data(data_df)
    assert(isinstance(filtered_data, pd.DataFrame))

def test_get_data1():
    filtered_data = get_data(data)
    assert(isinstance(filtered_data, pd.DataFrame))

def test_categorical_filter0():
    filtered_data = categorical_filter(data)
    assert(filtered_data["course_attempt_status"].dtype == 'int8')

def test_categorical_filter1():
    filtered_data = categorical_filter(data, set_codes=False)
    assert(filtered_data["course_attempt_status"].dtype == 'category')
