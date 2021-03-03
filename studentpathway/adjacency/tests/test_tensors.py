from studentpathway.adjacency.tensors import *
import pandas as pd
import numpy as np
import pytest
import os

PATH = "studentpathway/adjacency/tests/test_data_files"

def test_sequence_tensor0():
    test_data_file = "test_data5.csv"
    test_unit_file = "test_unit_data.csv"

    test_data = pd.read_csv(os.path.join(PATH, test_data_file))
    test_unit_data = pd.read_csv(os.path.join(PATH, test_unit_file))

    T, students, units = sequence_tensor(test_data, test_unit_data)
    assert (len(T) == 2)
    assert (T[0].shape == (5,4))
    assert (len(students) == 5)
    assert (len(units) == 4)

def test_adjacency_tensor1():
    test_data_file = "test_data6.csv"
    test_unit_file = "test_unit_data.csv"

    test_data = pd.read_csv(os.path.join(PATH, test_data_file))
    test_unit_data = pd.read_csv(os.path.join(PATH, test_unit_file))

    T, students, units = sequence_tensor(test_data)
    assert (len(T) == 3)
    assert (T[0].shape == (5,4))

def test_adjacency_tensor2():
    test_data_file = "test_data6.csv"
    test_unit_file = "test_unit_data.csv"

    test_data = pd.read_csv(os.path.join(PATH, test_data_file))
    test_unit_data = pd.read_csv(os.path.join(PATH, test_unit_file))

    T, students, units = sequence_tensor(test_data, test_unit_data, units_from_students_data=False)
    assert (len(T) == 3)
    assert (T[0].shape == (5,4))


def test_adjacency_tensor():
    test_data_file = "test_data6.csv"
    test_unit_file = "test_unit_data.csv"

    test_data = pd.read_csv(os.path.join(PATH, test_data_file))
    test_unit_data = pd.read_csv(os.path.join(PATH, test_unit_file))

    T, students, units = sequence_tensor(test_data, test_unit_data)
    _P, P = adjacency_tensor(T)

    assert(P.shape == (4, 4))

def test_projections():
    students = {"P": {111, 222, 333, 444}, "C": set(), "M": {111,222,333,444}, "B": set()}

    P = np.array([[0, 0.25, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0.5, 0, 0.5],
                  [0, 0, 0, 0]])

    projection, projection_count = projections(students, P)

    assert (len(projection.keys()) == 4)
    assert (projection_count['P'] == 0)
    assert (projection_count['C'] == 3)

def test_sort_students_by_units():
    foo0 = np.array([[1,2,0,0],[0,0,1,2],[0,0,1,0],[1,0,0,0],[1,1,0,0]])
    foo1 = np.array([[2,0,0,0],[0,0,2,0],[0,0,1,0],[1,0,0,0],[1,1,0,0]])
    foo = [foo0, foo1]
    units = ["P", "C", "M", "B"]
    students = ["111", "222", "333", "444", "555"]
    student_dict = sort_students_by_units(foo, students, units, sem=2)

    assert(len(list(student_dict.keys())) == 4)
