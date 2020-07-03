# Student Pathway Project

Project to predict the enrolment pathway of students. This project is a work in progress.

## Python package requirements

* [Python 3](https://www.python.org/downloads/)
* [Anaconda](https://www.anaconda.com/)
* [Networkx](https://networkx.github.io/documentation/stable/install.html)
    * To download Networkx library use `pip install networkx`

# Dataset

The data used in the `data_processing.ipynb` file is taken from the directory `students_data`.

The folder `students_data` must remain inside this repository.

The dataset consists of the following file structure:

```
+---2015
¦       enrolments2015.csv
¦       offers2015.csv
¦       results2015.csv
¦
+---2016
¦       enrolments2016.csv
¦       results2016.csv
¦
+---2017
¦       enrolments2017.csv
¦       offers2017.csv
¦       preferences2017.csv
¦       results2017.csv
¦
+---2018
¦       enrolments2018.csv
¦       offers2018.csv
¦       preferences2018.csv
¦       results2018.csv
¦
+---2019
        enrolments2019.csv
        offers2019.csv
        preferences2019.csv
        results2019.csv
```

The key data of interest is **Enrolments** and **Results**.

**EXAMPLE**:

* Enrolments data in 2015 => `students_data/2015/enrolments2015.csv`
* Results data in 2015 => `students_data/2015/results2015.csv`

## Data Processing

All the operation related to data processing must be performed in `data_processing.ipynb`.

**DO NOT LEAVE ANY DATA VISIBLE ON JUPYTER NOTEBOOK BEFORE COMMITING**.

The code is developed to automatically collect data from a `.csv` to **Pandas** dataframe.

The data from each year is stored in an array of dataframe and then merged together as a single dataframe.

The primary key in `results` and `enrolments` data is the `student_id`.

The `student_id` is used to merge the demographic data from `enrolments` and the unit outcome from `results`.

The `final_data` is generated which is a combination of all the years of data.

## Network Diagram

Use **Networkx** library to generate the network diagram.


## Adjacency Method

`adjacency_method` is a Python module developed to use the functions declared in this module.

The functions can be directly imported into Jupyter notebook.

**EXAMPLE**:

`from adjacency_method.adjacency_method import sequence_matrix`
