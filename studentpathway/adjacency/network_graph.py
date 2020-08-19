import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import os

def network_graph(matrix,
                  units,
                  figure_size=(50,50),
                  color_node="red",
                  color_edges="blue",
                  resolution=500,
                  file_location="images/network_results/",
                  label_position=0.3,
                  edge_width=2,
                  layout_type="circular",
                  save_figure=True,
                  show_weights=True,
                  edge_radius=0.1,
                  size_node=300,
                  edge_threshold=0.5,
                  esmall_transparency=0.5,
                  esmall_thickness=1):
    """Saves and displays the network Diagram

    Keyword arguments:
    matrix -- adjacency matrix of type np.ndarray
    units -- list of units present in the dataset
    figure_size -- a tuple that determines the size of matplotlib diagram (Default=(50,50))
    color_node -- color of nodes (Default="red")
    color_edges -- cmap color used in matplotlib used for different shades of color (Default="blue")
    resolution -- image resolution used in saving the diagram (Default=500)
    file_location -- location to store the image (Default="images/test_dataset")
    label_position -- Adjust the position of the labels on the edges (Default=0.3)
    edge_width -- Size of the width of the edge (Default=2)
    layout_type -- type of layout for the graph (Default="circular")
    save_figure -- Boolean to save figure (Defaul=True)
    show_weights -- Boolean to show weights on the network diagram (Default=True)
    edge_radius -- Float value of the radius of the edge (Default=0.1)
    size_node -- Size of nodes (Default=300)
    edge_threshold -- Differentiates the edges in terms of thickness (Default=0.5)
    esmall_transparency -- transparency for edges beyond (Default=0.5)
    esmall_thickness -- thickness of underthreshold edges (Default=1)


    Returns:
    None
    """

    # Calculating start time
    start_time = datetime.now()

    # Check if matrix is a numpy matrix
    print("Checking for numpy array...", end="")
    if not isinstance(matrix, np.ndarray):
        raise TypeError("Input matrix is not of type numpy.ndarray")

    print(u'\N{check mark}')

    # Checking for units to be a List
    print("Checking for units list...", end="")
    if not isinstance(units, list):
        raise TypeError("units variable is not of type list")

    print(u'\N{check mark}')

    # Creating graph
    G = nx.from_numpy_matrix(matrix, create_using=nx.MultiDiGraph)

    # list of edges and weights for color coding the graph
    edges, weights = zip(*nx.get_edge_attributes(G,'weight').items())

    # Creating a window of figure_size to show the graph
    plt.figure(figsize=figure_size)

    # Using list of units to rename nodes in the graph
    mapping  = {}

    for i in range(len(units)):
        mapping[i] = str(units[i])

    # Relabelling the nodes with the unit names
    G = nx.relabel_nodes(G, mapping, copy=False)

    # Checking the layout of the Graph
    if layout_type == "circular":
        position = nx.circular_layout(G)
    else:
        position = nx.spring_layout(G)

    # Generating edge thickness
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] >= edge_threshold]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] < edge_threshold]

    try:
        # nodes
        nx.draw_networkx_nodes(G,
                               pos=position,
                               node_size=size_node,
                               node_color=color_node,
                               label=mapping)

        nx.draw_networkx_labels(G, pos=position)

        # edges
        nx.draw_networkx_edges(G,
                               pos=position,
                               connectionstyle='arc3, rad={}'.format(edge_radius),
                               edgelist=elarge,
                               edge_color=color_edges,
                               alpha=None,
                               width=edge_width)

        # edges
        nx.draw_networkx_edges(G,
                               pos=position,
                               connectionstyle='arc3, rad={}'.format(edge_radius),
                               edgelist=esmall,
                               edge_color=color_edges,
                               alpha=esmall_transparency,
                               width=esmall_thickness)

        # Checks if the user requested the weigts on graph
        if show_weights:
            try:
                # Draw the graph with edge labels
                weight_labels = {(u, v): round(d['weight'], 2) for u, v, d in G.edges(data=True) if d['weight'] >= edge_threshold}
                nx.draw_networkx_edge_labels(G, pos=position, label_pos=label_position, connectionstyle='arc3, rad={}'.format(edge_radius), edge_labels=weight_labels)
            except ValueError as e:
                print(e)
                # Uses default values to display graph
                nx.draw_networkx_edge_labels(G, pos=position, label_pos=label_position, connectionstyle='arc3, rad=0.1')

    except ValueError as e:
        print("ValueError: ")
        print(e)
        print("Creating default network graph...")
        # Uses default values to display Graph
        nx.draw(G, pos=position, with_labels=node_labels, connectionstyle='arc3, rad=0.1', edge_list=edges, width=2)



    # Saves the network diagram in a file file location
    if save_figure == True:
        # File location using timestamp
        file_name = file_location + str(int(datetime.timestamp(datetime.now()))) + ".png"

        # Checking if the folder does not exist
        if not os.path.exists(file_location):
            os.makedirs(file_location)

        # Saves the file with the filename as timestamp
        plt.savefig(file_name, format="PNG", dpi=resolution)

    plt.show()

    # Calculating elapsed time
    elapsed_time = datetime.now() - start_time
    print(f"Time elapsed (hh:mm:ss.ms) {elapsed_time}")

    return None
