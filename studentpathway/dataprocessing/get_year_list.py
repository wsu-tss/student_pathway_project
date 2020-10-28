import os

def get_year_list(root_directory):
    """Returns list of ``years`` by browsing the root directory of the dataset.
    The dataset is categorised in different subdirectories named after the year of the data.
    The function looks at the name of the subdirectories and if it happens to be a year, it updates the ``years`` list.

    :param root_directory: path of the root folder to get the years from.

    :return: list of years.

    :Example:

    >>> import studentpathway as sp
    >>> years = sp.get_year_list("students_data")
    >>> print(years)
    [2015, 2016, 2017, 2018, 2019]
    """

    try:
        # List the subfolders
        sub_folders = os.listdir(root_directory)

        years = []

        for year in sub_folders:
            try:
                years.append(int(year))
            except ValueError:
                continue

        # Sorting the year
        years.sort()

        return years

    except Exception as e:
        raise
