import csv
import itertools
import xlsxwriter
import xl2dict
import errno
import os
import logging
from random import sample
import baangt.base.GlobalConstants as GC

logger = logging.getLogger("pyC")


class TestDataGenerator:
    """
    TestDataGenerator Class is to used to create a TestData file from raw excel file containing all possible values.

    :param rawExcelPath: Takes input path for raw xlsx file.

    :method write_excel: Will write the final processed data in excel file.
    :method write_csv: Will write the final processed data in csv file.
    """
    def __init__(self, rawExcelPath=GC.TESTDATAGENERATOR_INPUTFILE):
        self.path = os.path.abspath(rawExcelPath)
        if not os.path.isfile(self.path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.path)
        self.raw_data_json = self.__read_excel(self.path)
        self.processed_datas = self.__process_data(self.raw_data_json)
        self.headers = list(self.processed_datas[0].keys())
        self.final_data = self.__generateFinalData(self.processed_datas)

    def write(self, OutputFormat=GC.TESTDATAGENERATOR_OUTPUT_FORMAT, batch_size=0, outputfile=None):
        if OutputFormat.lower() == "xlsx":
            self.__write_excel(batch_size=batch_size, outputfile=outputfile)
        elif OutputFormat.lower() == "csv":
            self.__write_csv(batch_size=batch_size, outputfile=outputfile)
        else:
            logger.debug("Incorrect file format")


    def __write_excel(self, outputfile=GC.TESTDATAGENERATOR_OUTPUTFILE_XLSX, batch_size=0):
        """
        Writes TestData file with final processsed data.
        :param outputfile: Name and path for output file.
        :param batch_size: No. of random selected data
        :param random: If false all data will be written else random data of selected batch size will be written.
        :return: None
        """
        if batch_size:
            data_lis = sample(self.final_data, batch_size)
        else:
            data_lis = self.final_data
        with xlsxwriter.Workbook(outputfile) as workbook:
            worksheet = workbook.add_worksheet()
            worksheet.write_row(0, 0, self.headers)
            for row_num, data in enumerate(data_lis):
                worksheet.write_row(row_num+1, 0, data)

    def __write_csv(self, outputfile=GC.TESTDATAGENERATOR_OUTPUTFILE_CSV, batch_size=0):
        """
        Writes final data in csv
        :param outputfile: Name and path of output file
        :return:
        """
        if batch_size:
            data_lis = sample(self.final_data, batch_size)
        else:
            data_lis = self.final_data
        with open(outputfile, 'w', newline='\n')as file:
            fl = csv.writer(file)
            fl.writerow(self.headers)
            for dt in data_lis:
                fl.writerow(list(dt))

    def __generateFinalData(self, processed_data):
        """
        Creates a list of final completely processed data.
        :param processed_data:
        :return:
        """
        final_data = []
        for lis in processed_data:
            data_lis = []
            for key in lis:
                if type(lis[key]) == str:
                    data = [lis[key]]
                else:
                    data = lis[key]
                data_lis.append(data)
            datas = itertools.product(*data_lis)
            for dtt in datas:
                final_data.append(dtt)
        logger.info(f"Total generated data = {len(final_data)}")
        return final_data


    def __process_data(self, raw_json):
        """
        Processes raw json data to __data_generators and Converts raw data range and list to python list.
        :param raw_json:
        :return:
        """
        processed_datas = []
        for raw_data in raw_json:
            if not list(raw_data.values())[0]:
                continue
            processed_data = {}
            for key in raw_data:
                keys = self.__data_generators(key)
                for ke in keys:
                    processed_data[ke] = self.__data_generators(raw_data[key])
            processed_datas.append(processed_data)
        return processed_datas

    def __data_generators(self, raw_data):
        """
        Creates generator for datas
        :param raw_data:
        :return:
        """
        if type(raw_data)==float:
            raw_data = int(raw_data)
        raw_data = str(raw_data).strip()
        if raw_data[0] == "[" and raw_data[-1] == "]":
            proccesed_datas = [data.strip() for data in raw_data[1:-1].split(",")]

        elif "-" in raw_data:
            raw_data = raw_data.split('-')
            start = raw_data[0].strip()
            end = raw_data[1].strip()
            step = 1
            if "," in end:
                raw_data = end.split(",")
                end = raw_data[0].strip()
                step = raw_data[1].strip()
            proccesed_datas = [x for x in range(int(start), int(end)+1, int(step))]

        else:
            proccesed_datas = [raw_data.strip()]
        return proccesed_datas



    def __read_excel(self, path):
        """
        :param path: Path to raw data xlsx file.
        :return: json of raw data
        """
        xl_obj = xl2dict.XlToDict()
        sheet = xl_obj.fetch_data_by_column_by_sheet_index(path,sheet_index=0)
        return sheet

if __name__=="__main__":
    lTestDataGenerator = TestDataGenerator()
    lTestDataGenerator.write(batch_size=1000)
