import pandas as pd
import numpy as np
from datetime import datetime
import sys
import copy

def adjacency_matrix(M):
    """Return adjacency matrix

    Keyword arguments:
    M -- sequence matrix of (m, n) dimensions matrix of type numpy.ndarray

    Returns:
    _P -- graph projection matrix of (m, m) dimensions
    P -- adjaceny matrix of (m, m) dimensions
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

    # Creating a zeros _P matrix of size of units from M
    _P = np.zeros((_P_dim, _P_dim))

    # Creating a zeros P matrix of size of units from M
    P = copy.deepcopy(_P)

    # P matrix generation
    print("Generating P matrix...", end="")

    for i in range(_P_dim):
        for j in range(_P_dim):
            delta = M[:, j] - M[:, i]
            d = np.absolute(delta)
            _P[i][j] = np.sum(np.array([int(k >= 0) for k in delta]) * np.array([int(l == 1) for l in d]) * np.array([int(n != 1) for n in M[:, j]]))
            P[i][j] = _P[i][j]/np.sum(np.array([int(m > 0) for m in M[:, j]]))

    print(u'\N{check mark}')

    # Calculating elapsed time
    elapsed_time = datetime.now() - start_time
    print(f"Time elapsed (hh:mm:ss.ms) {elapsed_time}")

    return _P, P
