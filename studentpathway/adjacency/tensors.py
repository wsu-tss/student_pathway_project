import pandas as pd
import numpy as np
from datetime import datetime
import sys
from tqdm import tqdm


def sequence_tensor(students_data,
                    units_data=None,
                    sem_separator_month=8,
                    unit_header="unit_code",
                    id_header="student_id",
                    date_header="outcome_date",
                    units_from_students_data=True):
    """Returns a sequence tensor of the student unit selection.

    :param students_data: Pandas dataframe.
    :param units_data: Pandas dataframe of unit data. (Default=None)
    :param sem_separator_month: Month  number used to separate the semesters. (Default=8)
    :param unit_header: Column heading for unit name. (Default="unit_name")
    :param id_header: Column heading for student it. (Default="student_id")
    :param units_from_students_data: Bool (Default=True)

    :return T: Sequence tensors of i x j x k where i = rows, j = columns, k = dimensions.
    :return students: list of all the students in the data.
    :return units: list of all the units in the data.

    :Example:

    >>> import studentpathway as sp
    >>> students_data = pd.read_csv("students_data/combined_data/eng_data.csv")
    >>> units_data = pd.read_csv("units_data/engineering_data/engineering_units.csv")
    >>> T, students, units = sp.sequence_tensor(students_data, units_data)
    """

    students_data[date_header] = pd.to_datetime(students_data[date_header], dayfirst=True)

    # List of students
    students = list(students_data[id_header].unique())

    # List of units
    if not units_from_students_data:
        units = list(units_data[unit_header].unique())
    else:
        units = list(students_data[unit_header].unique())

    if not isinstance(units_data, pd.DataFrame):
        units = list(students_data[unit_header].unique())

    # Creating a Tensor
    T = [np.zeros((len(students), len(units)))]

    for student in students:
        # getting the data of a single student
        df0 = students_data.loc[students_data[id_header] == student]
        df1 = df0.copy()

        # Re-organising the student df by unit outcome date
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

            # import pdb; pdb.set_trace()
            if uo_year > current_year or uo_month > sem_separator_month:
                if past_month != uo_month:
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

    return T, students, units

def _compute_count(dim0, dim1, T, i, j):
    """Returns the count of students in the sequence.

    :param dim0: First dimension of tensor T.
    :param dim1: Second dimension of tensor T.
    :param T: Sequence tensor.
    :param i: iterator from the adjacency_tensor loop.
    :param j: iterator from the adjacency_tensor loop.

    :return: Count of the students in the sequence.
    """
    delta = T[dim0][:, j] - T[dim1][:, i]

    d = np.absolute(delta)

    Tdim = T[dim0][:, j]

    count = np.sum(np.where(delta >= 0, 1, 0)
                   * np.where(d == 1, 1, 0)
                   * np.where(Tdim != 1, 1, 0))
    return count

def adjacency_tensor(T):
    """Returns the adjacency matrix from the sequence tensor.

    :param T: Sequence tensor of (i, j, k) dimensions.

    :return: Adjacency matrix represting markov chain.
    """

    # Getting the dimensions for P matrix
    P_dim = T[0].shape[1]

    # Getting total number of students from a matrix from T.
    total_students = T[0].shape[0]

    # Creating a zeros P matrix of size of units from T.
    P = np.zeros((P_dim, P_dim))

    _P = P.copy()

    # Removing the top and bottom dimensions of the Tensor.
    mid_dimensions = [*range(len(T))]

    # Remove first dimension
    mid_dimensions.pop(0)

    # Remove last dimension
    mid_dimensions.pop(-1)

    Tj = np.where(T[0] > 0, 1, 0)
    Tj_total = np.sum(Tj, axis=0)

    # Summing up all the columns - indicates the number of times a unit was taken.
    for i in range(P_dim):
        for j in range(P_dim):
            count = []
            terminate = False

            # Count top dimension
            count.append(_compute_count(0, 0, T, i, j))

            for k in mid_dimensions:
                if not np.sum(T[k][:, j]):
                    terminate = True
                    break
                # Mid upwards
                count.append(_compute_count(k, k - 1, T, i, j))

                # Mid same
                count.append(_compute_count(k, k, T, i, j))

                # Mid lower
                count.append(_compute_count(k + 1, k, T, i, j))

            # Count bottom dimension
            if not terminate:
                count.append(_compute_count(-1, -1, T, i, j))

            _P[i][j] = np.sum(count)

            if not Tj_total[j] or not _P[i][j]:
                P[i][j] = 0
            else:
                P[i][j] = _P[i][j] / Tj_total[i]

    return _P, P

def projections(s, P):
    """Returns the projection of students given the current students in the sequence tensor.

    :param s: students in every unit.
    :param P: Probability of student transitions.

    :return: Projections that indicates the student movement.
    """

    pred = np.dot(s, P)

    common_students = np.where(P > 0, 1, 0)

    common_sum = np.sum(common_students, axis=0)

    den = np.where(common_sum == 0, 1, common_sum)

    projections = pred / den

    return projections
