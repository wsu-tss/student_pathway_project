from data_processing_methods import get_year_list, get_data_frames
import pandas as pd
import pytest

PATH = "data_processing_methods/tests/test_data_files/test_year"
DATA_NAME = "test_data"
years = get_year_list(PATH)

def test_get_data_frame1():
    with pytest.raises(Exception):
        data = get_data_frames()

def test_get_data_frames2():
    data = get_data_frames(DATA_NAME, PATH, years)

    assert(isinstance(data, list))
    assert(isinstance(data[0], pd.DataFrame))
    assert(len(data) == 3)
