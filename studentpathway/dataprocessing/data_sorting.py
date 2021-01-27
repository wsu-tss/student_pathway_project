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
        for program in program_units:
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

    :returns: A dataframe with an additional student program column.
    """

    student_data = data.copy()

    student_data[header] = student_program

    return student_data
