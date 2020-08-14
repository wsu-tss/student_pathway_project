import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

def get_year_list(root_folder):
    """Returns list of years from the subfolder named as years

    Keyword arguments:
    root_folder -- path of the root folder to get the years from (example: root_folder="students_data")

    Returns:
    years -- list of years
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
