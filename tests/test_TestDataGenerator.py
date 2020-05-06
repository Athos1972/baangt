from baangt.TestDataGenerator.TestDataGenerator import TestDataGenerator
import xlrd
import os
import csv

# Create an instance of TestDataGenerator object with sample input file
testDataGenerator = TestDataGenerator("../baangt/TestDataGenerator/RawTestData.csv")


def test_write_excel_5000():
    # Tests write_excel method of TestDataGenerator object with default 5000 random data
    testDataGenerator.write_excel()
    xl_book = xlrd.open_workbook("output.xlsx")
    xl_sheet = xl_book.sheet_by_index(0)
    assert xl_sheet.nrows == 5001
    print("Test 5000 random data successful.")
    os.remove("output.xlsx")


def test_write_excel_3000():
    # Tests write_excel method of TestDataGenerator object with 3000 random data given through parameter
    testDataGenerator.write_excel(batch_size=3000)
    xl_book = xlrd.open_workbook("output.xlsx")
    xl_sheet = xl_book.sheet_by_index(0)
    assert xl_sheet.nrows == 3001
    print("Test 3000 random data successful.")
    os.remove("output.xlsx")


def test_write_excel_all():
    # Takes too much time!!!!!
    # Tests write_excel method of TestDataGenerator object with all data by turning random to False.
    testDataGenerator.write_excel(random=False)
    xl_book = xlrd.open_workbook("output.xlsx")
    xl_sheet = xl_book.sheet_by_index(0)
    print(f"Total data in excel file = {str(xl_sheet)}")
    os.remove("output.xlsx")


def test_write_csv():
    # Tests write_csv method of TestDataGenerator
    testDataGenerator.write_csv()
    data = []
    with open("output.csv", 'r') as raw_file:
        raw = csv.reader(raw_file)
        for row in raw:
            data.append(row)
    print(f"Total data in excel file = {str(len(data))}")
    os.remove("output.csv")

