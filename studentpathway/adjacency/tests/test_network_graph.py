import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import os
import pytest
from studentpathway.adjacency.network_graph import network_graph

def test_network_graph1():
    with pytest.raises(TypeError):
        network_graph()

def test_network_graph2():
    with pytest.raises(TypeError):
        P = np.array([[1,2],[3,4]])
        network_graph(P, 1)
