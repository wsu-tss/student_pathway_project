import pandas as pd
import numpy as np
import sys

sys.path.append('../')
import studentpathway as sp

# Importing engineering data
data = pd.read_csv("../students_data/combined_data/eng_data.csv")

# Importing units data
units_data = pd.read_csv("../units_data/engineering_data/engineering_units.csv")

# Creating a data structure to sort the units by their program.
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

student_units = list(d_stu.unit_code)

student_program = sp.get_student_program(student_units, program)

d_stu2 = sp.sort_by_age(d_stu1)

s_stu3 = sp.add_student_program(d_stu2, student_program)

# Mapping the units and categorising any special units.

units_df = sp.special_units_year(units_data, year_map={"AU": '4', "OE": '4', "Special":'2'})

d_stu_score = sp.study_score(d_stu3, round_upto=4)


# Getting scores of all the students
# This returns a dictionary mapping the student id to their scores.
student_scores = sp.student_scores(feature_data, round_upto=2)

# Getting the frequency distribution of the scores
score_freq = sp.score_frequency(student_scores)

zero_score_student_df = sp.sort_students_by_score(feature_data,
                                                  score=0,
                                                  student_score_dict=student_scores)
