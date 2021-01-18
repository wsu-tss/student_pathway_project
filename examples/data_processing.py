import pandas as pd
import os
import sys
import hashlib
sys.path.append('../')

import studentpathway as sp

# Getting the results and enrolments data

# Using pandas dataframe to import the data from the .csv file.
#
# The data is stored in a root folder titled `students_data`
#
# This data is categorised into subsequent years. For example: 2015, 2016, ...
#
# The `years` array needs to be updated should the new data of the new year is added.
#
# Example of file naming convention for the data files:
# * Results from 2015: `results2015.csv`
# * Enrolments from 2015: `enrolments2015.csv`

# print(sp.get_data_frames.__doc__)


# Root directory of the data
ROOT_FOLDER = "../students_data"
RESULTS = "results"
ENROLMENTS = "enrolments"

### Year list from the sub folders of data

# The data for the enrolments and results are stored in subfolder in the years.
# Instead of hard coding the years in an array, the following section finds the years by the subfolder name which needs to be in years.
# They years are converted into `int` datatype and sorted in `years` list.

years = sp.get_year_list(ROOT_FOLDER)

# Result data

results_data = []

results_data = sp.get_data_frames(RESULTS, ROOT_FOLDER, years)

# Standardising the columns
results_column_header = ["student_id", "course_code", "unit_cohort", "unit_code", "unit_name", "outcome_date", "teaching_calendar", "grade", "mark"]

for i in range(len(results_data)):
    results_data[i].columns = results_column_header

# Combining the results data

results = pd.concat(results_data, axis=0, sort=False).reset_index(drop=True)

# Enrolment data

# Combining the enrolment data

enrolments = pd.concat(enrolment_data, axis=0, sort=False).reset_index(drop=True)

# Merging Results and Enrolments Data

# Removing the repeated columns
enrolments = enrolments.drop(["course_code", "school_name"], axis=1)

# Combining the tables

final_data = results.join(enrolments.set_index('student_id'), on="student_id")

# Sorting the dataset with student ID

final_data = final_data.sort_values(by=['student_id']).reset_index(drop=True)

# Organising date for outcome_date
final_data['outcome_date'] = pd.to_datetime(final_data.outcome_date)

# Organising date for course_start_date
final_data['course_start_date'] = pd.to_datetime(final_data.course_start_date)

# Organising date for date_of_birth
final_data['date_of_birth'] = pd.to_datetime(final_data.date_of_birth)

# ## Duplicate data removal from final data
#
# Run the following section after merging the **results** and **enrolments**.
#
# The following code gets rid of the duplicate values.

final_data = final_data.drop_duplicates().reset_index(drop=True)

# # Encrypt Student ID
#
# The following code must be run before saving the `final_data`.
#
# The code uses sha1 algorithm to encrypt student ID

students = final_data["student_id"].to_list()

encrypted_id = []

for student in students:
    encrypted_id.append(hashlib.sha1(str(student).encode('ASCII')).hexdigest())

final_data["student_id"] = encrypted_id

# # Storing the data
#
# The `final_data` is a pandas dataframe.
#
# Run the following section for storing `final_data` into a `final_data.csv` file.
#
# File path: `students_data/combined_data/final_data.csv`

final_data.to_csv(r'students_data/combined_data/final_data.csv', index=False)
