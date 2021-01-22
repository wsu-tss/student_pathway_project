import pandas as pd
import numpy as np
import copy

def sort_units_program(data, unit_type="unit_code"):
    """Reads the data as a csv file and returns a dictionary of
    unit_code sorted by program.

    :param data: path to the csv file or pandas DataFrame.
    :unit_type: Type of unit information to store in a list. (Default="unit_code")

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
        units = list(np.where(units_data["program"] == program,
                     units_data[unit_type], False))

        program_units[program] = [unit for unit in units if unit != 0]

    return program_units
