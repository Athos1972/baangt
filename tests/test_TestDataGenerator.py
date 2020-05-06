from baangt.TestDataGenerator.TestDataGenerator import TestDataGenerator
import xlrd
import os
import csv
import baangt.base.GlobalConstants as GC

# Create an instance of TestDataGenerator object with sample input file
testDataGenerator = TestDataGenerator("0TestInput/RawTestData.xlsx")


def test_write_excel_1000():
    # Tests write method of TestDataGenerator object with 1000 random data in excel.
    testDataGenerator.write(batch_size=1000)
    xl_book = xlrd.open_workbook(GC.TESTDATAGENERATOR_OUTPUTFILE_XLSX)
    xl_sheet = xl_book.sheet_by_index(0)
    assert xl_sheet.nrows == 1001
    print("Test 1000 random data successful.")
    os.remove(GC.TESTDATAGENERATOR_OUTPUTFILE_XLSX)


def test_write_csv_3000():
    # Tests write method of TestDataGenerator object with 3000 random data in csv.
    testDataGenerator.write(OutputFormat="csv", batch_size=3000)
    data = []
    with open(GC.TESTDATAGENERATOR_OUTPUTFILE_CSV, 'r') as raw_file:
        raw = csv.reader(raw_file)
        for row in raw:
            data.append(row)
    assert len(data) == 3001
    print("Test 3000 random data successful.")
    os.remove(GC.TESTDATAGENERATOR_OUTPUTFILE_CSV)


def test_write_excel_all():
    # Takes too much time!!!!!
    # Tests write_excel method of TestDataGenerator object with all data.
    testDataGenerator.write()
    xl_book = xlrd.open_workbook(GC.TESTDATAGENERATOR_OUTPUTFILE_XLSX)
    xl_sheet = xl_book.sheet_by_index(0)
    print(f"Total data in excel file = {str(xl_sheet.nrows)}")
    os.remove(GC.TESTDATAGENERATOR_OUTPUTFILE_XLSX)


def test_write_csv_all():
    # Tests write_csv method of TestDataGenerator
    testDataGenerator.write(OutputFormat="csv")
    data = []
    with open(GC.TESTDATAGENERATOR_OUTPUTFILE_CSV, 'r') as raw_file:
        raw = csv.reader(raw_file)
        for row in raw:
            data.append(row)
    print(f"Total data in excel file = {str(len(data))}")
    os.remove(GC.TESTDATAGENERATOR_OUTPUTFILE_CSV)

