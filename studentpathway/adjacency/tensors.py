import pandas as pd
import numpy as np
from datetime import datetime
import sys
from tqdm import tqdm


def sequence_tensor(students_data,
                    unit_data,
                    sem_separator_month=8,
                    unit_header="unit_code",
                    id_header="student_id",
                    date_header="outcome_date"):
    """Returns a sequence tensor of the student unit selection.

    :param students_data: Pandas dataframe.
    :param unit_data: Pandas dataframe of unit data.
    :param sem_separator_month: Month  number used to separate the semesters. (Default=8)
    :param unit_header: Column heading for unit name. (Default="unit_name")
    :param id_header: Column heading for student it. (Default="student_id")

    :return T: Sequence tensors of i x j x k where i = rows, j = columns, k = channel.
    :return students: list of all the students in the data.
    :return units: list of all the units in the data.
    """

    # List of students
    students = list(data[id_header].unique())

    # List of units
    units = list(data[unit_header].unique())

    # Creating a Tensor
    T = [np.zeros((len(students), len(units)))]

    for student in students:
        # getting the data of a single student
        df0 = students_data.loc[student_data[id_header] == student]
        df1 = df0.copy()
        df1 = df0.sort_values(by=[date_header], ignore_index=True)

        years = list(df1[date_header].dt.year.unique())
        months = list(df1[date_header].dt.month.unique())

        # A list of units taken by a student
        s_units = list(df1[unit_header])

        # Initialising for allocation of matrix
        current_year = 0
        past_month = 0
        semester_preference = 0

        for i in range(len(s_units)):
            # Initialising updated to False to check if changes are made to the matrix.
            updated = False
            unit = df1.iloc[i][unit_header]

            # unit outcome year and month
            uo_year = df1.iloc[i][date_header].year
            uo_month = df1.iloc[i][date_header].month

            if uo_year > current_year or uo_month > sem_separator_month:
                if past_month is not uo_month:
                    semester_preference += 1
                    past_month = uo_month
                current_year = uo_year

            student_index = students.index(student)
            unit_index = units.index(unit)

            # every matrix in the tensor T
            for m in T:
                if not m[student_index][unit_index]:
                    m[student_index][unit_index] = semester_preference
                    updated = True
                    break

            if not updated:
                T.append(np.zeros((len(students), len(units))))
                T[-1][student_index][unit_index] = semester_preference

    return T
