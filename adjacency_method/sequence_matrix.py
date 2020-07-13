import pandas as pd
import numpy as np

def sequence_matrix(data):
    """Return the sequence matrix.

    Keyword arguments:
    data -- Pandas dataframe for which the sequence matrix is to be generated.

    Returns:
    M -- sequence matrix of m x n where m = rows of students and n = columns of units.
    students -- list of all the students in the data.
    units -- list of all the units in the data.
    """

    #Checking for pandas dataframe
    if not isinstance(data, pd.DataFrame):
        raise TypeError("The parameter to sequence_matrix must contain pandas dataframe.")


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

    # Allocating the month to differentiate between semesters; August being the 8th month.
    august = 8

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
            if (unit_outcome_month > august and spring == False):
                semester_preference += 1
                spring = True
            elif (unit_outcome_month < august):
                spring = False

            # Gets the preference of the unit as per the year
            preference = outcome_years.tolist().index(unit_outcome_year) + semester_preference

            # Getting the student row in the matrix
            student_index = students.tolist().index(student)

            # Getting the unit coloumn in the matrix
            unit_index = units.tolist().index(unit_name)

            # Updating the sequence matrix
            M[student_index][unit_index] = preference

    return M, students.tolist(), units.tolist()
