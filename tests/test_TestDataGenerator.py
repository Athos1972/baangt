from baangt.TestDataGenerator.TestDataGenerator import TestDataGenerator
import xlrd
import os
import csv
from pathlib import Path
import pytest
import baangt.base.GlobalConstants as GC
from xlsxwriter.exceptions import FileCreateError

# Create an instance of TestDataGenerator object with sample input file
testDataGenerator = TestDataGenerator("0TestInput/RawTestData.xlsx")
testOutput100xls = str(Path(os.getcwd()).joinpath("1TestResults").joinpath("output100.xlsx"))
testOutput300csv = str(Path(os.getcwd()).joinpath("1TestResults").joinpath("output300.csv"))
testOutputFullxls = str(Path(os.getcwd()).joinpath("1TestResults").joinpath("outputFull.xlsx"))
testOutputFullcsv = str(Path(os.getcwd()).joinpath("1TestResults").joinpath("outputFull.csv"))


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
    testDataGenerator.write(OutputFormat="csv", batch_size=300, outputfile=testOutput300csv)
    data = []
    with open(testOutput300csv, 'r') as raw_file:
        raw = csv.reader(raw_file)
        for row in raw:
            data.append(row)
    assert len(data) == 301
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
    with open(testOutputFullcsv, 'r') as raw_file:
        raw = csv.reader(raw_file)
        for row in raw:
            data.append(row)
    print(f"Total data in excel file = {str(len(data))}")


def test_write_to_wrong_Path():
    with pytest.raises(FileCreateError):
        testDataGenerator.write(outputfile="/franzi/fritzi/hansi.xlsx", batch_size=100)
