import sys

sys.path.append('../')

import studentpathway as sp

# Data path constants
# -------------------
#
# This path will be different depending upon how the data is stored on your local directory
# If you are coding in the jupyter notebook, inside the root directory,
# then, you do not need to include `../` before the path.
# `../` is included before the path name `students_data` in this example
# because the data is one directory level above.

DATA_PATH = "../students_data/combined_data/final_data.csv"
UNITS_PATH = "../units_data/engineering_data/engineering_units.csv"

eng_data = sp.cohort_filter(data=DATA_PATH,
                            student_cohort="Bachelor of Engineering",
                            unit_list=UNITS_PATH,
                            exclusive_search=False)

# Saving the file
# ---------------
# Saves the processed data to a csv file
eng_data.to_csv(r'../students_data/combined_data/eng_data.csv', index=False)

# Adjacency methods
# -----------------

M, students, units = sp.sequence_matrix(eng_data)

_P, P = sp.adjacency_matrix(M)

# Network diagram
# ---------------

sp.network_graph(P,
                 units,
                 figure_size=(100,100),
                 resolution=100,
                 save_figure=True,
                 show_weights=False,
                 esmall_transparency=0.1,
                 edge_threshold=0.2,
                 color_edges='k',
                 file_location="../images",
                 edge_radius=0.1)
