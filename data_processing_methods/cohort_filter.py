import pandas as pd

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
            filtered_data = final_data.loc[final_data["student_cohort"].str.contains(student_cohort)]

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
