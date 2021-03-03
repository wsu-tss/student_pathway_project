import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append('../')
import studentpathway as sp

# constants
unit_header = "unit_code"
id_header = "student_id"
date_header = "outcome_date"
sem_separator_month=8

# data
data = sp.get_data("../students_data/combined_data/eng_data.csv")

students_data = data.copy()

# units data
units_data = pd.read_csv("../units_data/engineering_data/engineering_units.csv")

# removing the zero scores students
df = sp.remove_score(students_data, units_data)

# separating the data for the processing operation.
# Note:
# -----
# This is not required, but to complete this task where the data needed to be
# separated, we did this.

mask0 = (df["outcome_date"].dt.year >= 2015) & (df["outcome_date"].dt.year <= 2017)

df0 = df.loc[mask0].reset_index(drop=True)

mask1 = (df["outcome_date"].dt.year >= 2018)

df1 = df.loc[mask1].reset_index(drop=True)

# Running the sequence tensor
T0, students0, units0 = sp.sequence_tensor(df1, units_data,units_from_students_data=False)

T1, students1, units1 = sp.sequence_tensor(df1, units_data,units_from_students_data=False)

_P0, P0 = sp.adjacency_tensor(T0)

students_dict1 = sp.sort_students_by_units(T1, students1, units1)

proj, proj_count = sp.projections(students_dict1, P0)

students_dict1_count = dict()
for k, v in students_dict1.items():
    students_dict1_count[k] = len(v)

projection = pd.DataFrame({"units": proj_count.keys(), "future_count": proj_count.values()})

past_data = pd.DataFrame({"units": students_dict1_count.keys(), "past_count": students_dict1_count.values()})

unit_map = pd.Series(units_data.unit_name.values, index=units_data.unit_code).to_dict()

past_data1 = past_data.replace({"units": unit_map})

future_data1 = projection.replace({"units": unit_map})

merged_df = future_data1.join(past_data1.set_index("units"), on="units")

# Plotting the bar graph
merged_df.set_index("units").plot(kind="bar", grid=True, figsize=(20,5))
plt.title("Number of students predicting 2018 from the data of 2016-2017")
plt.ylabel("Number of students")

# Use the following line to save the bar graph image
# Note:
# -----
# The code is commented out so that the image does not get saved accidentally.
# plt.savefig("merged0.jpg", dpi=200, bbox_inches="tight")
