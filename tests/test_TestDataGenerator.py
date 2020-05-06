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
testOutput1000xls = str(Path(os.getcwd()).joinpath("1TestResults").joinpath("output1000.xlsx"))
testOutput3000csv = str(Path(os.getcwd()).joinpath("1TestResults").joinpath("output3000.csv"))
testOutputFullxls = str(Path(os.getcwd()).joinpath("1TestResults").joinpath("outputFull.xlsx"))
testOutputFullcsv = str(Path(os.getcwd()).joinpath("1TestResults").joinpath("outputFull.csv"))


def removeFile(file):
    try:
        os.remove(file)
    except Exception as e:
        pass


def test_write_excel_1000():
    # Tests write method of TestDataGenerator object with 1000 random data in excel.
    removeFile(testOutput1000xls)
    testDataGenerator.write(batch_size=1000, outputfile=testOutput1000xls)
    xl_book = xlrd.open_workbook(testOutput1000xls)
    xl_sheet = xl_book.sheet_by_index(0)
    assert xl_sheet.nrows == 1001
    print("Test 1000 random data successful.")


def test_write_csv_3000():
    # Tests write method of TestDataGenerator object with 3000 random data in csv.
    removeFile(testOutput3000csv)
    testDataGenerator.write(OutputFormat="csv", batch_size=3000, outputfile=testOutput3000csv)
    data = []
    with open(testOutput3000csv, 'r') as raw_file:
        raw = csv.reader(raw_file)
        for row in raw:
            data.append(row)
    assert len(data) == 3001
    print("Test 3000 random data successful.")


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
