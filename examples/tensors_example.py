import pandas as pd
import numpy as np
import sys

sys.path.append('../')
import studentpathway as sp


# importing the data
data = pd.read_csv("../students_data/combined_data/eng_data.csv")

# copying to the students_data variable
students_data = data.copy()

# importing the units dataset
units_data = pd.read_csv("../units_data/engineering_data/engineering_units.csv")

# Variables
unit_header = "unit_code"
id_header = "student_id"
date_header = "outcome_date"
sem_separator_month=8

# Identify the zero score students
program = sp.sort_units_program(units_data)

# Adding age column
df = sp.add_age(data)

# Keeping only the required features
feature_col = ["student_id",
               "unit_code",
               "teaching_calendar",
               "mark",
               "gender",
               "campus_code",
               "citizenship",
               "indigenous_type",
               "age"]

feature_data = sp.get_features(df, feature_col)

# Following are the operations that a performed on a single student data.

students = list(feature_data.student_id.unique())

d_stu1 = feature_data.loc[feature_data["student_id"] == students[0]]

student_units = list(d_stu1.unit_code)

student_program = sp.get_student_program(student_units, program)

d_stu2 = sp.sort_by_age(d_stu1)

d_stu3 = sp.add_student_program(d_stu2, student_program)

# Mapping the units and categorising any special units.

units_df = sp.special_units_year(units_data, year_map={"AU": '4', "OE": '4', "Special":'2'})

d_stu_score = sp.study_score(d_stu3, round_upto=4)

student_scores = sp.student_scores(feature_data, round_upto=2)

# Getting the frequency distribution of the scores
score_freq = sp.score_frequency(student_scores)

zero_score_student_df = sp.sort_students_by_score(feature_data,
                                                  score=0,
                                                  student_score_dict=student_scores)

zero_score_students = list(zero_score_student_df[id_header].unique())

# Removing the students with zero score from the dataset
students_data = students_data[~students_data[id_header].isin(zero_score_students)]

# Generating sequence tensor
T, students, units = sp.sequence_tensor(students_data, unit_header="unit_name")

# Generating adjacency tensor
_P, P = sp.adjacency_tensor(T)
