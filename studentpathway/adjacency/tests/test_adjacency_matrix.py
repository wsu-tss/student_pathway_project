from studentpathway.adjacency.adjacency_matrix import adjacency_matrix
from studentpathway.adjacency.sequence_matrix import sequence_matrix
import pandas as pd
import numpy as np
import pytest

PATH = "studentpathway/adjacency/tests/test_data_files/"

def test_adjacency_matrix1():
    with pytest.raises(TypeError):
        _P, P = adjacency_matrix()

def test_adjacency_matrix2():
    data = pd.read_csv(PATH + "test_data4.csv")
    data.outcome_date = pd.to_datetime(data.outcome_date)
    M, students, units = sequence_matrix(data)
    m_dim = M.shape
    _P, P, Q = adjacency_matrix(M)
    assert (P.shape == (m_dim[1], m_dim[1]))
    assert (_P.shape == (m_dim[1], m_dim[1]))
    assert (Q.shape == (m_dim[1], m_dim[1]))
    assert (_P[0,:] == np.array([0,1,0,0])).all()
    np.testing.assert_almost_equal(P[0,:], np.array([0, 0.25, 0, 0]), 2)
    np.testing.assert_almost_equal(Q[0,:], np.array([0, 0.2, 0, 0]), 2)
    np.testing.assert_almost_equal(Q[2,:], np.array([0.4, 0.4, 0, 0.4]), 2)

def test_adjacency_matrix3():
    M = np.array([[1,0],[1,0],[1,0],[1,0],[1,0]])
    _P, P, Q = adjacency_matrix(M)
    np.testing.assert_almost_equal(P, np.array([[0,0],[0,0]]))
    np.testing.assert_almost_equal(Q, np.array([[0,0],[0,0]]))
