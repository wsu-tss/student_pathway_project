from studentpathway.adjacency.tensors import sequence_tensor
import pandas as pd
import numpy as np
import pytest
import os

PATH = "studentpathway/adjacency/tests/test_data_files"

def test_sequence_tensor():
    test_data_file = "test_data5.csv"
    test_unit_file = "test_unit_data.csv"

    test_data = pd.read_csv(os.path.join(PATH, test_data_file))
    test_unit_data = pd.read_csv(os.path.join(PATH, test_unit_file))

    T, students, units = sequence_tensor(test_data, test_unit_data)
    assert (len(T) == 2)
    assert (T[0].shape == (5,4))
    assert (len(students) == 5)
    assert (len(units) == 4)
