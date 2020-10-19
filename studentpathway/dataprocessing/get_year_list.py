import os

def get_year_list(root_folder):
    """Returns list of years from the subfolder named as years

    :param root_folder: path of the root folder to get the years from (example: root_folder="students_data")

    :returns years: list of years
    """

    try:
        # List the subfolders
        sub_folders = os.listdir(root_folder)

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
