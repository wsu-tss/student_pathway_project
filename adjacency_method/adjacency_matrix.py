import pandas as pd
import numpy as np
from datetime import datetime
import sys

def adjacency_matrix(M, students=None, units=None):
    """Return adjacency matrix

    Keyword arguments:
    sequence_matrix -- matrix of (m, n) dimensions matrix of type numpy.ndarray

    Returns:
    P -- adjaceny matrix of (m, m) dimensions
    """

    # Checking for numpy ndarray
    print("Checking for numpy array...")
    if not isinstance(M, np.ndarray):
        raise TypeError("Sequence Matrix is not of type numpy.ndarray")

    print(u'\N{check mark}')

    _P = 1

    raise NotImplementedError
