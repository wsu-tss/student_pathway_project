import pandas as pd
import numpy as np
import copy
import numbers


def get_data(data):
    """Reads the data as a csv or a pandas DataFrame and returns the DataFrame

    Keyword arguments:
    data -- path to the csv file or pandas DataFrame

    Returns:
    final_data -- pandas DataFrame
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
    """Returns pandas dataframe with rows that are present in unit_list

    Keyword arguments:
    data -- csv datafile of the cohort-wise data (example: data='students_data/combined_data/final_data.csv')
    student_cohort -- student cohort to filter (example: student_cohort='Bachelor of Engineering (Honours)')
    unit_list -- csv datafile of the unit list as per cohort (example: unit_list='units_data/engineering_data/engineering_units.csv') (Default=None)
    exclusive_search -- Boolean that determines to search the student_cohort exclusively or partially (Default=True)

    Returns:
    filtered_data -- Pandas dataframe with filtered data
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
    """Returns pandas dataframe with grades categorised

    Keyword arguments:
    data -- csv datafile of the cohort-wise data (example: data='students_data/combined_data/final_data.csv')
    grades -- dict of grades and lower threshold to the grades. (Default={85:"H", 75: "D", 65:"C", 50: "P", np.NaN: "S", 0: "F"})
    avoid -- set of grades to be avoided while filtering. (Default={'S'})
    remove_missing -- boolean to remove the rows whose marks and grades are missing. (Default=False)

    Returns:
    filtered_data -- Pandas dataframe with filtered data
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
    """Returns pandas dataframe with categorical variables from the columns

    Keyword arguments:
    data -- csv file of the data (example: data='students_data/combined_data/final_data.csv') or pandas DataFrame
    categorical_columns -- list of columns in the data that requires categorical filtering
    set_codes -- Boolean to set the categorical column with numerical value (Default=True)

    Returns:
    filtered_data -- filtered data with the columns as categorical variables
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
