import pandas as pd
import numpy as np
import copy


def sort_units_program(data, unit_type="unit_code", header="program"):
    """Reads the data as a csv file and returns a dictionary of
    unit_code sorted by program.

    :param data: path to the csv file or pandas DataFrame.
    :param unit_type: Type of unit information to store in a list. (Default=``"unit_code"``)
    :param header: header to sort the column. (Default=``"program"``)

    :return: Dictionary mapping program as keys to the units list as values.

    :Examples:

    >>> import studentpathway as sp
    >>> program = sp.sort_units_program("units_data/engineering_data/engineering_units.csv")
    """

    # Checks if the data is not a Pandas Dataframe
    if not isinstance(data, pd.DataFrame):
        units_data = pd.read_csv(data)
    else:
        units_data = copy.deepcopy(data)

    programs = list(units_data.program.unique())

    program_units = dict()

    for program in programs:
        units = list(np.where(units_data[header] == program,
                     units_data[unit_type], False))

        program_units[program] = [unit for unit in units if unit != 0]

    return program_units

def get_student_program(student_units, program_units, skip_program=["Common"]):
    """Takes a dictionary of program units with keys are program and
    the list of units in the program as the key.

    :param student_units: List of all the units taken by a student.
    :param program_units: dictionary of program mapped with list of units in the program.
    :param skip_program: List of program to be skipped. (Default=``["Common"]``)

    :return: The program of in which the student is enrolled.

    >>> import studentpathway as sp
    >>> program_units = sp.sort_units_program("units_data/engineering_data/engineering_units.csv")
    >>> student_units = [300480, 300035, 300487, 200238, 300021, 300761, 300762, 300763, 300764]
    >>> student_program = sp.get_student_program(student_units, program_units)
    """
    program_rank = dict()

    # converts the list of units into set
    student_units = set(student_units)

    # Identifying the non common units i.e. the commmon units in the first year
    maintain_units = set()

    # Assigning the units to maintain
    maintain_units = set(student_units)

    # Checks if the skip program is an empty list
    if skip_program:
        # updating the set of units that are not in skip program
        for program in skip_program:
            maintain_units.difference_update(
                list(student_units.intersection(set(program_units[program])))
            )

    # Ranking the program based upon the occurence of the units in the student data
    for program in program_units:
        program_rank[program] = len(
            list(set(program_units[program]).intersection(maintain_units))
        )

    # Finding the maximum number of units taken by the student from a program
    student_program = max(program_rank, key=program_rank.get)

    return student_program

def add_student_program(data, student_program, header="program"):
    """Adds a new column to the pandas dataframe that outlines the program
    that student is enrolled in.

    :param data: Pandas dataframe.
    :param student_program: A string of student program.
    :param header: A string to indicate the name of the new column. (Default=``"program"``)

    :return: A dataframe with an additional student program column.
    """

    student_data = data.copy()

    student_data[header] = student_program

    return student_data

def get_features(data, feature_columns):
    """Returns a pandas dataframe with feature columns.

    :param data: Pandas dataframe.
    :param feature_columns: List of all the features to be maintained.

    :return: Pandas dataframe with the extracted features.
    """
    try:
        feature_data = data[feature_columns]
    except KeyError as e:
        print("KeyError: " + str(e))
        print("One or more features in feature_columns is not in the dataframe.")
        raise

    return feature_data

def add_age(data, dob="date_of_birth", outcome_date="outcome_date", header="age"):
    """Adds the student age column to the dataframe.

    :param data: Pandas dataframe.
    :param dob: A string of date of birth as given in the dataset. (Default=``"date_of_birth"``)
    :param outcome_date: A string of outcome date as given in the dataset. (Default=``"outcome_date"``)
    :param header: A string of column header. (Default=``"age"``)

    :return: Pandas dataframe with ``header`` column.
    """
    # Create a copy of dataframe
    df = data.copy()

    # Converting to datetime objects
    df[outcome_date] = pd.to_datetime(data[outcome_date])
    df[dob] = pd.to_datetime(data[dob])

    df[header] = pd.DatetimeIndex(df[outcome_date]).year - pd.DatetimeIndex(df[dob]).year

    return df

def sort_by_age(data, header="age"):
    """Sorts the data based on age column.

    :param data: Pandas dataframe.
    :param header: Heading of the column to sort. (Default=``"age"``)

    :return: Pandas dataframe with sorted column by age.
    """

    df = data.copy()

    df = data.sort_values(by=[header], ignore_index=True)

    return df

def special_units_year(data, year_map={"AU": '4', "OE": '4'}, header="year"):
    """Returns a pandas dataframe by changing the special category
    to the year of study.

    Eg. Students take Alternate Units ``AU`` and Other Elective ``OE`` in year 4.

    :param data: Pandas dataframe of units.
    :param year_map: A dict of mapping special category of units to year.
    :param header: Column header to perform operation.

    :return: Pandas dataframe with year mapped.
    """

    df = data.copy()

    df.replace({header: year_map}, inplace=True)

    return df

def study_score(data, mark_header="mark", unit_header="unit_code", round_upto=None):
    """Returns the score of the student depending upon the units passed
    and the number of attempts.

    score = passed units / attempted units

    :param data: pandas data frame of a single student.
    :param mark_header: Column head to look for the marks to sort. (Default=``"mark"``)
    :param unit_header: Column head to find the unit numbers.
    :param round_upto: Rounds the score upto the decimals mentioned.

    :return: study score of the students.

    :Example:

    >>> import studentpathway as sp
    >>> score = sp.study_score(student_data)
    """

    attempts = len(list(data[unit_header]))

    passed_units = data[data[mark_header] >= 50].count()[mark_header]

    score = passed_units / attempts

    if round_upto:
        return round(score, round_upto)

    return score
