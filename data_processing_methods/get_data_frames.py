import pandas as pd

def get_data_frames(data_name, root_folder, years):
    """Returns an array of dataframe of the requested data_name

    Keyword arguments:
    data_name -- The name of the data to be imported (example: data_name=enrolments)
    root_folder -- The path to data folder where all the csv files are present (example: root_folder=students_data)
    years -- A list of years which is the subfolder inside the root_folder

    Returns:
    data -- list of all the pandas dataframe of the data_name
    """

    data = []
    try:
        for i in range(len(years)):
            file_name = str(data_name) + str(years[i]) + ".csv"
            path = root_folder + "/" + str(years[i]) + "/" + file_name
            data.append(pd.read_csv(path))
        return data
    except TypeError as e:
        print(e)
    except ValueError as e:
        print(e)
    except:
        print("Unexpected error!")
        raise
