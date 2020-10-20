import pandas as pd
import numpy as np
import copy
import numbers


def get_data(data):
    """Reads the data as a csv or a pandas DataFrame and returns the DataFrame.
    Although this function is used in other functions to import the data from a csv file,
    this can also work as a stand-alone function for reading a csv file.

    :param data: path to the csv file or pandas DataFrame

    :return: pandas DataFrame.

    :raises ValueError: Check for the file path and make sure the file is a csv file.

    :Example:

    >>> from studentpathway.dataprocessing import filters
    >>> data = filters.get_data("students_data/combined_data/eng_data.csv")
    >>> data.shape
    (11379, 20)
    """

    try:
        # Checks if the data is not a Pandas Dataframe
        if not isinstance(data, pd.DataFrame):
            # Reads the csv file
            final_data = pd.read_csv(data)

            # Converts the outcome_date into datetime objects
            final_data['outcome_date'] = pd.to_datetime(final_data.outcome_date)
        else:
            final_data = copy.deepcopy(data)

        return final_data
    except ValueError as e:
        print("ValueError: " + str(e))
        raise

def cohort_filter(data, student_cohort, unit_list=None, exclusive_search=True):
    """Returns pandas dataframe having the ``student_cohort`` value in the column student_cohort.
    The filter also allows the process to filter the units from a list of units provided by ``unit_list``.
    ``unit_list`` is by default ``None``, but also reads a csv file which has two columns: unit_code and unit_name.
    The ``student_cohort`` can have almost similar degrees. eg: ``Bachelor of Engineering``, ``Bachelor of Engineering (Honours)``, etc.,
    ``exclusive_search=True`` (Default) allows to filter by exact string provided by ``student_cohort``.
    ``exclusive_search=False`` considers almost similar string. eg: ``Bachelor of Engineering`` and ``Bachelor of Engineering (Honours)
    will be included in the ``filtered_data``.

    :param data: csv datafile of the cohort-wise data (example: data='students_data/combined_data/final_data.csv')
    :param student_cohort: student cohort to filter (example: student_cohort='Bachelor of Engineering (Honours)')
    :param unit_list: csv datafile of the unit list as per cohort (example: unit_list='units_data/engineering_data/engineering_units.csv') (Default=None)
    :param exclusive_search: Boolean that determines to search the student_cohort exclusively or partially (Default=True)

    :return: Pandas dataframe with filtered data.

    :Example:

    >>> from studentpathway.dataprocessing import filters
    >>> data = filters.cohort_filter("students_data/combined_data/final_data.csv", student_cohort="Bachelor of Engineering", unit_list="units_data/engineering_data/engineering_units.csv" ,exclusive_search=False)
    >>> data.shape
    (11379, 20)
    """

    # Reads the data from the csv file
    try:
        final_data = pd.read_csv(data)

        # Converts the outcome_date into datetime objects
        final_data['outcome_date'] = pd.to_datetime(final_data.outcome_date)

        # Sort the data with the student_cohort
        if exclusive_search:
            filtered_data = final_data.loc[final_data["student_cohort"] == student_cohort]
        else:
            filtered_data = final_data.loc[final_data["student_cohort"].str.contains(student_cohort) == True]

    except ValueError as e:
        print("ValueError: " + str(e))
        raise

    # Checks for filtering units
    if unit_list is not None:
        try:
            units_data = pd.read_csv(unit_list)

            unit_code = units_data["unit_code"].to_list()

            filtered_data = filtered_data[filtered_data["unit_code"].isin(unit_code)]

            return filtered_data

        except ValueError as e:
            print("ValueError: " + str(e))
            raise
    else:
        return filtered_data

def grades_filter(data, grades = {85:"H", 75: "D", 65:"C", 50: "P", np.NaN: "S", 0: "F"}, avoid={'S'}, remove_missing=False):
    """Returns pandas dataframe with grades categorised.
    ``grades_filter`` maps the ``grades`` with key as the lower threshold for the value of the respective grades.
    The ``grades`` has a default input and it is optional argument.
    ``avoid`` is a set of all the grades that must be avoided during the filtering process
    and avoids mapping the respective grade column with any the mapping.
    ``remove_missing`` is a boolean, if true, allows to remove the entire row from the dataframe.

    :param data: csv datafile of the cohort-wise data (example: data='students_data/combined_data/final_data.csv')
    :param grades: dict of grades and lower threshold to the grades. (Default={85:"H", 75: "D", 65:"C", 50: "P", np.NaN: "S", 0: "F"})
    :param avoid: set of grades to be avoided while filtering. (Default={'S'})
    :param remove_missing: boolean to remove the rows whose marks and grades are missing. (Default=False)

    :return: Pandas dataframe with filtered data

    :Example:

    >>> from studentpathway.dataprocessing import filters
    >>> data = filters.grades_filter("students_data/combined_data/eng_data.csv")
    """

    final_data = get_data(data)
    # Creating a deepcopy of the data
    filtered_data = copy.deepcopy(final_data)

    # List of all the grades
    grade_list = list(grades.values())

    # List of all the marks threshold for grades
    mark_list = list(grades.keys())
    mark_list = [mark for mark in mark_list if not np.isnan(mark)]

    for index, row in filtered_data.iterrows():
        # Checks if the grade is to be avoided
        if row['grade'] in avoid:
            filtered_data.loc[index, 'mark'] = None
            continue

        # Checks if the value is not a NaN
        if not np.isnan(row['mark']):
            for mark in mark_list:
                if row['mark'] >= mark:
                    filtered_data.loc[index, 'grade'] = grades[mark]
                    break
        else:
            filtered_data.loc[index, 'mark'] = np.NaN
            filtered_data.loc[index, 'grade'] = None

    # removes the missing data rows
    if remove_missing:
            filtered_data = filtered_data.drop(filtered_data[pd.isnull(filtered_data.grade) & np.isnan(filtered_data.mark)].index).reset_index(drop=True)

    return filtered_data

def categorical_filter(data, categorical_columns=["course_attempt_status" ,"gender", "campus_code", "citizenship", "indigenous_type"], set_codes=True):
    """Returns pandas dataframe with categorical variables from the columns.
    It takes ``categorical_columns`` as an argument which is to be converted to the categorical variable.
    The categorical variable can be converted into the numerical value by ensuring ``set_codes`` is True.

    :param data: csv file of the data (example: data='students_data/combined_data/final_data.csv') or pandas DataFrame
    :param categorical_columns: list of columns in the data that requires categorical filtering
    :param set_codes: Boolean to set the categorical column with numerical value (Default=True)

    :return: filtered data with the columns as categorical variables.

    :raises ValueError: Check for the file path and make sure the file is a csv file.

    :Example:

    >>> from studentpathway.dataprocessing import filters
    >>> data = filters.categorical_filter("students_data/combined_data/eng_data.csv")
    >>> data.gender
    0        1
    1        1
    2        1
    3        1
    4        1
            ..
    11374    1
    11375    1
    11376    1
    11377    0
    11378    0
    Name: gender, Length: 11379, dtype: int8
    """

    data = get_data(data)

    filtered_data = copy.deepcopy(data)

    for column in categorical_columns:
        if column in data.columns:
            try:
                if set_codes:
                    filtered_data[column] = pd.Categorical(data[column]).codes
                else:
                    filtered_data[column] = pd.Categorical(data[column])
            except ValueError as e:
                print("ValueError: " + str(e))
                raise
        else:
            print(f"Column with name {column} does not exist in the dataset!\nSkipping {column}.")

    return filtered_data
