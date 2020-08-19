from studentpathway.adjacency.sequence_matrix import sequence_matrix
import pandas as pd
import numpy as np
import pytest

PATH = "studentpathway/adjacency/tests/test_data_files/"

def test_data1():
	data = pd.read_csv(PATH + "test_data1.csv")
	data.outcome_date = pd.to_datetime(data.outcome_date)
	assert all(data.columns == ["student_id","unit_code", "unit_name", "outcome_date", "teaching_calendar", "grade", "mark"])
	assert (data.shape == (9,7))

def test_sequence_matrix_test1():
	data = pd.read_csv(PATH + "test_data1.csv")
	data.outcome_date = pd.to_datetime(data.outcome_date)
	M, students, units = sequence_matrix(data)
	assert (M == [[1,1,1,2,2,2,3,3,3]]).all()
	assert (len(students) == 1)
	assert (len(units) == 9)
	assert (students == [12345])
	assert (units == ["Physics", "Chemistry", "Maths", "English", "Biology", "Mechanics", "Philosophy", "History", "Geography"])

def test_data2():
	data = pd.read_csv(PATH + "test_data2.csv")
	data.outcome_date = pd.to_datetime(data.outcome_date)
	assert all(data.columns == ["student_id","unit_code", "unit_name", "outcome_date", "teaching_calendar", "grade", "mark"])
	assert (data.shape == (18,7))

def test_sequence_matrix_test2():
	data = pd.read_csv(PATH + "test_data2.csv")
	data.outcome_date = pd.to_datetime(data.outcome_date)
	M, students, units = sequence_matrix(data)
	assert (M == [[1,1,1,2,2,2,3,3,3],[1,1,1,2,2,2,3,3,3]]).all()
	assert (len(students) == 2)
	assert (len(units) == 9)
	assert (students == [12345, 12222])
	assert (units == ["Physics", "Chemistry", "Maths", "English", "Biology", "Mechanics", "Philosophy", "History", "Geography"])

def test_data3():
	data = pd.read_csv(PATH + "test_data3.csv")
	data.outcome_date = pd.to_datetime(data.outcome_date)
	assert all(data.columns == ["student_id","unit_code", "unit_name", "outcome_date", "teaching_calendar", "grade", "mark"])
	assert (data.shape == (16,7))

def test_sequence_matrix_test3():
	data = pd.read_csv(PATH + "test_data3.csv")
	data.outcome_date = pd.to_datetime(data.outcome_date)
	M, students, units = sequence_matrix(data)
	assert (M == [[1,1,2,2,2,3,3,3,0],[1,1,2,2,2,3,3,0,1]]).all()
	assert (len(students) == 2)
	assert (len(units) == 9)
	assert (students == [12345, 12222])
	assert (units == ["Chemistry", "Maths", "English", "Biology", "Mechanics", "Philosophy", "History", "Geography", "Physics"])


def test_data4():
	data = pd.read_csv(PATH + "test_data4.csv")
	data.outcome_date = pd.to_datetime(data.outcome_date)
	assert all(data.columns == ["student_id","unit_code", "unit_name", "outcome_date", "teaching_calendar", "grade", "mark"])
	assert (data.shape == (13,7))

def test_sequence_matrix_test4():
	data = pd.read_csv(PATH + "test_data4.csv")
	data.outcome_date = pd.to_datetime(data.outcome_date)
	M, students, units = sequence_matrix(data)
	print(M)
	assert (M == [[1,2,0,0],[2,2,1,0],[2,2,1,2],[1,0,0,0],[0,1,1,2]]).all()
	assert (len(students) == 5)
	assert (len(units) == 4)
	assert (students == [111, 222, 333, 444, 555])
	assert (units == ["Physics","Chemistry", "Maths", "Biology"])

# Test to check without datetime object in outcome_date
def test_sequence_matrix_test5():
	data = pd.read_csv(PATH + "test_data1.csv")
	M, students, units = sequence_matrix(data)
	assert (M == [[1,1,1,2,2,2,3,3,3]]).all()
	assert (len(students) == 1)
	assert (len(units) == 9)
	assert (students == [12345])
	assert (units == ["Physics", "Chemistry", "Maths", "English", "Biology", "Mechanics", "Philosophy", "History", "Geography"])


def test_sequence_matrix_test6():
	with pytest.raises(TypeError):
		M, students, units = sequence_matrix()

def test_sequence_matrix_test7():
	data = pd.read_csv(PATH + "test_data1.csv")
	data.outcome_date = pd.to_datetime(data.outcome_date)
	M, students, units = sequence_matrix(data, sem_separator_month=9)
	assert (M == [[1,1,1,2,2,2,3,3,3]]).all()
	assert (len(students) == 1)
	assert (len(units) == 9)
	assert (students == [12345])
	assert (units == ["Physics", "Chemistry", "Maths", "English", "Biology", "Mechanics", "Philosophy", "History", "Geography"])
