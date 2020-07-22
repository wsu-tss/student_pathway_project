from adjacency_method import sequence_matrix, adjacency_matrix
import pandas as pd
import numpy as np
import pytest

def test_adjacency_matrix1():
    with pytest.raises(TypeError):
        _P, P = adjacency_matrix()

def test_adjacency_matrix2():
    data = pd.read_csv("adjacency_method/tests/test_data_files/test_data4.csv")
    data.outcome_date = pd.to_datetime(data.outcome_date)
    M, students, units = sequence_matrix(data)
    m_dim = M.shape
    _P, P = adjacency_matrix(M)
    assert (P.shape == (m_dim[1], m_dim[1]))
    assert (_P.shape == (m_dim[1], m_dim[1]))
    assert (_P[0,:] == np.array([0,2,1,0])).all()
    np.testing.assert_almost_equal(P[0,:], np.array([0, 0.5, 0.33, 0]), 2)
