import pandas as pd

def get_data_frames(data_name, root_directory, years):
    """Returns a list of dataframe of the requested ``data_name``.
    The argument ``data_name`` takes the type of data. eg: ``data_name="enrolments"`` or ``data_name="results"``.
    The function navigates to the ``root_directory`` and navigates every sub directory named after year of the dataset.
    The subdirectories consist of year-wise directories which consists of the data as per the year.
    The ``years`` argument is a list of all the years whose subdirectories are named after in the root directory of the dataset.

    :param data_name: The name of the data to be imported (example: data_name=enrolments).
    :param root_directory: The path to data directory where all the csv files are present (example: root_directory=students_data).
    :param years: A list of years which is the subfolder inside the root_directory.

    :return: list of all the pandas dataframe of the data_name.

    :Example:

    >>> import studentpathway as sp
    >>> years = [2015, 2016, 2017, 2018]
    >>> result_data = sp.get_data_frames("results", "students_data", years)
    """

    data = []
    try:
        for i in range(len(years)):
            file_name = str(data_name) + str(years[i]) + ".csv"
            path = root_directory + "/" + str(years[i]) + "/" + file_name
            data.append(pd.read_csv(path))
        return data
    except TypeError as e:
        print(e)
    except ValueError as e:
        print(e)
    except:
        print("Unexpected error!")
        raise
