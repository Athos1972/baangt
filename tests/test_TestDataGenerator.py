from baangt.TestDataGenerator.TestDataGenerator import TestDataGenerator
import xlrd
import os
import csv
from pathlib import Path
import pytest
import baangt.base.GlobalConstants as GC
from xlsxwriter.exceptions import FileCreateError

####
# DO NOT CHANGE THE PATHS below. Instead execute PYTEST from baangt root directory and not from /tests
####pi

# Test file path
rawTestFile = "tests/0TestInput/RawTestData.xlsx"

# Create an instance of TestDataGenerator object with sample input file

testDataGenerator = TestDataGenerator(rawTestFile)
Path(os.getcwd()).joinpath("Tests").joinpath("1TestResults").mkdir(parents=True, exist_ok=True)
testOutput100xls = str(Path(os.getcwd()).joinpath("Tests").joinpath("1TestResults").joinpath("output100.xlsx"))
testOutput300csv = str(Path(os.getcwd()).joinpath("Tests").joinpath("1TestResults").joinpath("output300.csv"))
testOutputFullxls = str(Path(os.getcwd()).joinpath("Tests").joinpath("1TestResults").joinpath("outputFull.xlsx"))
testOutputFullcsv = str(Path(os.getcwd()).joinpath("Tests").joinpath("1TestResults").joinpath("outputFull.csv"))


def removeFile(file):
    try:
        os.remove(file)
    except Exception as e:
        pass


def test_write_excel_100():
    # Tests write method of TestDataGenerator object with 100 random data in excel.
    removeFile(testOutput100xls)
    testDataGenerator.write(batch_size=100, outputfile=testOutput100xls)
    xl_book = xlrd.open_workbook(testOutput100xls)
    xl_sheet = xl_book.sheet_by_index(0)
    assert xl_sheet.nrows == 101
    print("Test 100 random data successful.")


def test_write_csv_300():
    # Tests write method of TestDataGenerator object with 300 random data in csv.
    removeFile(testOutput300csv)
    testDataGenerator.write(OutputFormat="csv", batch_size=250, outputfile=testOutput300csv)
    data = []
    with open(testOutput300csv, 'r', encoding='utf-8-sig') as raw_file:
        raw = csv.reader(raw_file)
        for row in raw:
            data.append(row)
    assert len(data) == 251
    print("Test 300 random data successful.")


def test_write_excel_all():
    removeFile(testOutputFullxls)
    # Takes too much time!!!!!
    # Tests write_excel method of TestDataGenerator object with all data.
    testDataGenerator.write(outputfile=testOutputFullxls)
    xl_book = xlrd.open_workbook(testOutputFullxls)
    xl_sheet = xl_book.sheet_by_index(0)
    print(f"Total data in excel file = {str(xl_sheet.nrows)}")


def test_write_csv_all():
    # Tests write_csv method of TestDataGenerator
    removeFile(testOutputFullcsv)
    testDataGenerator.write(OutputFormat="csv", outputfile=testOutputFullcsv)
    data = []
    with open(testOutputFullcsv, 'r', encoding='utf-8-sig') as raw_file:
        raw = csv.reader(raw_file)
        for row in raw:
            data.append(row)
    print(f"Total data in excel file = {str(len(data))}")


def test_write_to_wrong_Path():
    with pytest.raises(FileCreateError):
        testDataGenerator.write(outputfile="/franzi/fritzi/hansi.xlsx", batch_size=100)


def test_rrd_simple_input():
    # Checks __processRrd to get dict to target data
    rrd_output_dict = testDataGenerator._TestDataGenerator__processRrd(
        'Customers', 'Customer', {'Age group': ['30s', '40s'], 'Employment_status': ['employed']}
    )
    assert len(rrd_output_dict) > 0
    for data in rrd_output_dict:
        print(data)


def test_rrd_target_data_all():
    # Checks __processRrd to get dict to for all data of matching values
    rrd_output_dict = testDataGenerator._TestDataGenerator__processRrd(
        'Customers', '*', {'Age group': ['30s', '40s'], 'Employment_status': ['employed']}
    )
    assert len(rrd_output_dict) > 0
    for data in rrd_output_dict:
        print(data)


def test_rrd_no_data_to_match():
    # Checks __processRrd to get dict to for all data of when no value of matching is given
    rrd_output_dict = testDataGenerator._TestDataGenerator__processRrd('PaymentTerms', '*', {})
    assert len(rrd_output_dict) > 0
    for data in rrd_output_dict:
        print(data)

