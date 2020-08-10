# Student Pathway Project

Project to predict the enrolment pathway of students. This project is a work in progress.

## Python package requirements

* [Python 3](https://www.python.org/downloads/)
* [Anaconda](https://www.anaconda.com/)
* [Networkx](https://networkx.github.io/documentation/stable/install.html)

## Creating virtual environment and installing the requirements

Create a virtual environment and install all the required packages from `requirements.txt`

### Create virtual environment

Type the following commands in your terminal/Command prompt

**Install Virtual Environment package:** `pip install virtualenv`

**Create Virtual Environment:** `python -m venv venv`

**Activate Virtual Environment**

* For Windows: `venv\Scripts\activate`

* For Linux or Mac OS: `source venv/bin/activate`

### Exporting packages

Every time a new package is installed in the environment, execute the following:

`pip freeze --local > requirements.txt`

Run the following to get the list of install packages:

`pip list`

### Install the dependencies in the virtual environment

`pip install -r requirements.txt`

This will ensure that all the required python packages are installed in the virtual environment.

### Virtual Environment in Jupyter NOTEBOOK

Open Terminal/Anaconda Powershell Prompt and execute the following:

`ipython kernel install --user --name=venv`

Launch Jupyter notebook from Anaconda Powershell Prompt by executing the following:

`jupyter notebook`

### Changing the kernel in jupyter Notebook

On the menu bar select `Kernel > Change kernel > venv`.

While creating a new notebook, select `venv` instead of `Python3`.

# Dataset

The data used in the `data_processing.ipynb` file is taken from the directory `students_data`.

The folder `students_data` is shared via One Drive to the team members working on this project.

After cloning this repository on your local machine, make sure to add the shared folder `students_data` in the following path:

`student_pathway_project/students_data/`

Any changes to the data must reflect upon the dataset in this folder which is a shared folder with team members.

The dataset consists of the following file structure:

```
├───2015
│       enrolments2015.csv
│       offers2015.csv
│       results2015.csv
│
├───2016
│       enrolments2016.csv
│       results2016.csv
│
├───2017
│       enrolments2017.csv
│       offers2017.csv
│       preferences2017.csv
│       results2017.csv
│
├───2018
│       enrolments2018.csv
│       offers2018.csv
│       preferences2018.csv
│       results2018.csv
│
├───2019
│       enrolments2019.csv
│       offers2019.csv
│       preferences2019.csv
│       results2019.csv
│
└───combined_data
        final_data.csv
```

Any cleaning operation must result in storing the `final_data` in `students_data/combined_data/final_data.csv`

After importing the `final_data.csv` file into a Jupyter notebook, make sure to convert the dates into a datetime object.

Example:

`final_data['outcome_date'] = pd.to_datetime(final_data.outcome_date)`

**DO NOT EDIT THE RAW DATA MANUALLY WITH EXCEL OR WITH TEXT EDITOR.**

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

This module consists of :

* `sequence_matrix`
* `adjacency_matrix`


The functions can be directly imported into Jupyter notebook.

**EXAMPLE**:

`from adjacency_method import sequence_matrix, adjacency_matrix`
