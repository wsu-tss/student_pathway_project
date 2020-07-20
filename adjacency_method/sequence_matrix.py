import pandas as pd
import numpy as np
from datetime import datetime
import sys

def sequence_matrix(data, sem_separator_month=8):
    """Return the sequence matrix.

    Keyword arguments:
    data -- Pandas dataframe for which the sequence matrix is to be generated.
    sem_separator_month -- Month number used to separate the semesters. Default value is 8 for august.

    Returns:
    M -- sequence matrix of m x n where m = rows of students and n = columns of units.
    students -- list of all the students in the data.
    units -- list of all the units in the data.
    """

    # Calculating start time
    start_time = datetime.now()

    #Checking for pandas dataframe
    print("Checking for the input parameter is pandas dataframe...", end="")
    if not isinstance(data, pd.DataFrame):
        raise TypeError("The parameter to sequence_matrix must contain pandas dataframe.")

    print(u'\N{check mark}')

    # Checking for datetime
    print("Checking for the outcome_date to be a datetime object...", end="")
    dates = data["outcome_date"].to_list()
    for date in dates:
        if not isinstance(date, datetime):
            raise ValueError("outcome_date is not a datetime object.")

    print(u'\N{check mark}')

    # Number of units
    unit_number = data["unit_name"].nunique()

    # Number of students
    student_number = data["student_id"].nunique()

    # Generates a matrix of size m x n where m = student_number and n = unit_number
    M = np.zeros((student_number, unit_number))

    # List of students with student_id
    students = data["student_id"].unique()

    # list of units with unit_name
    units = data["unit_name"].unique()

    print("Initiating sequence matrix generation...", end="")

    # Iterating through the list of students
    for student in students:

        # Getting the dataframe of the student from students list
        student_data = data.loc[data["student_id"] == student]

        # Re-organising the student dataframe based upon outcome_date
        student_data = student_data.sort_values(by=["outcome_date"]).reset_index(drop=True)

        # list of units with unit_name
        student_units = student_data["unit_name"].unique()

        # getting the outcome years of the results
        outcome_years = student_data["outcome_date"].dt.year.unique()
        outcome_months = student_data["outcome_date"].dt.month.unique()

        # alocating semester value
        semester_preference = 1

        # Iterating through the list of units for the student
        for i in range(len(student_units)):
            unit_name = student_data.iloc[i].unit_name
            unit_outcome_year = student_data.iloc[i].outcome_date.year
            unit_outcome_month = student_data.iloc[i].outcome_date.month

            # Checking semester preference
            if (unit_outcome_month > sem_separator_month and spring == False):
                semester_preference += 1
                spring = True
            elif (unit_outcome_month < sem_separator_month):
                spring = False

            # Gets the preference of the unit as per the year
            preference = outcome_years.tolist().index(unit_outcome_year) + semester_preference

            # Getting the student row in the matrix
            student_index = students.tolist().index(student)

            # Getting the unit coloumn in the matrix
            unit_index = units.tolist().index(unit_name)

            # Updating the sequence matrix
            M[student_index][unit_index] = preference

    print(u'\N{check mark}')

    # Calculating elapsed time
    elapsed_time = datetime.now() - start_time
    print(f"Time elapsed (hh:mm:ss.ms) {elapsed_time}")

    return M, students.tolist(), units.tolist()
