import pandas as pd
import numpy as np
from datetime import datetime
import sys
from tqdm import tqdm


def sequence_matrix(data, sem_separator_month=8):
    """Return the sequence matrix.

    :param data: Pandas dataframe for which the sequence matrix is to be generated.
    :param sem_separator_month: Month number used to separate the semesters. Default value is 8 for august.

    :returns M: sequence matrix of m x n where m = rows of students and n = columns of units.
    :returns students: list of all the students in the data.
    :returns units: list of all the units in the data.

    :raises TypeError: The parameter to sequence_matrix must contain pandas dataframe.

    :Example:

    >>> import studentpathway as sp
    >>> import pandas as pd
    >>> data = pd.read_csv("students_data/combined_data/eng_data.csv")
    >>> M, students, units = sp.sequence_matrix(data)
    """

    # Calculating start time
    start_time = datetime.now()

    #Checking for pandas dataframe
    print("Checking for the input parameter is pandas dataframe...", end="")
    if not isinstance(data, pd.DataFrame):
        raise TypeError("The parameter to sequence_matrix must contain pandas dataframe.")

    print(u'\N{check mark}')

    # Checking for datetime
    print("Converting to dates to datetime object...", end="")
    data.outcome_date = pd.to_datetime(data.outcome_date)

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

    # Initiating progress bar
    loop = tqdm(total=data.shape[0], position=0, leave=False)

    # Iterating through the list of students
    for student in students:
        # loop counter variable
        k = 0

        # Getting the dataframe of the student from students list
        student_data = data.loc[data["student_id"] == student]

        # Re-organising the student dataframe based upon outcome_date
        student_data = student_data.sort_values(by=["outcome_date"]).reset_index(drop=True)

        # list of units with unit_name
        student_units = student_data["unit_name"]

        # getting the outcome years of the results
        outcome_years = student_data["outcome_date"].dt.year.unique()
        outcome_months = student_data["outcome_date"].dt.month.unique()

        # Initialising
        current_year = 0
        past_month = 0
        semester_preference = 0

        # Iterating through the list of units for the student
        for i in range(len(student_units)):
            unit_name = student_data.iloc[i].unit_name
            unit_outcome_year = student_data.iloc[i].outcome_date.year
            unit_outcome_month = student_data.iloc[i].outcome_date.month


            # sorting the units as per the semesters
            if unit_outcome_year > current_year or unit_outcome_month > sem_separator_month:
                if past_month is not unit_outcome_month:
                    semester_preference += 1
                    past_month = unit_outcome_month
                current_year = unit_outcome_year

            # Getting the student row in the matrix
            student_index = students.tolist().index(student)

            # Getting the unit coloumn in the matrix
            unit_index = units.tolist().index(unit_name)

            # Updating the sequence matrix
            M[student_index][unit_index] = semester_preference

            loop.set_description("Loading...".format(k))
            k += 1
            loop.update(1)

    loop.close()

    # Calculating elapsed time
    elapsed_time = datetime.now() - start_time
    print(f"Time elapsed (hh:mm:ss.ms) {elapsed_time}")

    return M, students.tolist(), units.tolist()
