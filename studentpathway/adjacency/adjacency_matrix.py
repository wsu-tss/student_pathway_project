import pandas as pd
import numpy as np
from datetime import datetime
import sys
import copy

def adjacency_matrix(M):
    """Return adjacency matrices

    :param M: sequence matrix of (m, n) dimensions matrix of type numpy.ndarray

    :returns _P: graph projection matrix of (n, n) dimensions
    :returns P: adjaceny matrix of (n, n) dimensions with subject-wise probability
    :returns Q: adjacency_matrix of (n, n) dimensions with total probability
    """

    # Calculating start time
    start_time = datetime.now()

    # Checking for numpy ndarray
    print("Checking for numpy array...", end="")
    if not isinstance(M, np.ndarray):
        raise TypeError("Sequence Matrix is not of type numpy.ndarray")

    print(u'\N{check mark}')

    # Getting the dimensions for _P matrix from M matrix's columns
    _P_dim = M.shape[1]

    # Getting total number of students from M matrix's rows
    total_students = M.shape[0]

    # Creating a zeros _P matrix of size of units from M
    _P = np.zeros((_P_dim, _P_dim))

    # Creating a zeros P matrix of size of units from M
    P = copy.deepcopy(_P)

    # Creating a zeros Q matrix of size unit from M
    Q = copy.deepcopy(P)

    # Summing up the columns
    Mj = np.where(M > 0, 1, 0)
    Mj_total = np.sum(Mj, axis=0)

    # P matrix generation
    print("Generating matrices...", end="")

    for i in range(_P_dim):
        for j in range(_P_dim):
            delta = M[:, j] - M[:, i]
            d = np.absolute(delta)
            _P[i][j] = np.sum(np.where(delta >= 0, 1, 0) * np.where(d == 1, 1, 0) * np.where(M[:, j] != 1, 1, 0))
            if (Mj_total[j] == 0 or _P[i][j] == 0):
                P[i][j] = 0
                Q[i][j] = 0
            else:
                P[i][j] = _P[i][j]/Mj_total[i]
                Q[i][j] = _P[i][j]/total_students

    print(u'\N{check mark}')

    # Calculating elapsed time
    elapsed_time = datetime.now() - start_time
    print(f"Time elapsed (hh:mm:ss.ms) {elapsed_time}")

    return _P, P, Q
