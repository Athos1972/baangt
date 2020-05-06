import csv
import os
import itertools
import xlsxwriter
import errno
import os
from random import sample


class TestDataGenerator:
    """
    TestDataGenerator Class is to used to create a TestData file from raw csv file containing all possible values.

    :param rawCsvPath: Takes input path for raw csv file.

    :method write_excel: Will write the final processed data in excel file.
    :method write_csv: Will write the final processed data in csv file.
    """
    def __init__(self, rawCsvPath: str="RawTestdData.csv"):
        self.path = os.path.abspath(rawCsvPath)
        if not os.path.isfile(self.path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.path)
        self.raw_data_json = self.__read_csv(self.path)
        self.processed_datas = self.__process_data(self.raw_data_json)
        self.headers = list(self.processed_datas[0].keys())
        self.final_data = self.__generateFinalData(self.processed_datas)

    def write_excel(self, outputfile: str="output.xlsx", batch_size=5000, random=True):
        """
        Writes TestData file with final processsed data.
        :param outputfile: Name and path for output file.
        :param batch_size: No. of random selected data
        :param random: If false all data will be written else random data of selected batch size will be written.
        :return: None
        """
        if random:
            data_lis = sample(self.final_data, batch_size)
        else:
            data_lis = self.final_data
        with xlsxwriter.Workbook(outputfile) as workbook:
            worksheet = workbook.add_worksheet()
            worksheet.write_row(0, 0, self.headers)
            for row_num, data in enumerate(data_lis):
                worksheet.write_row(row_num+1, 0, data)

    def write_csv(self, outputfile: str="output.csv"):
        """
        Writes final data in csv
        :param outputfile: Name and path of output file
        :return:
        """

        with open(outputfile, 'w', newline='\n')as file:
            fl = csv.writer(file)
            fl.writerow(self.headers)
            for dt in self.final_data:
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
        print(f"Total generated data = {len(final_data)}")
        return final_data


    def __process_data(self, raw_json):
        """
        Processes raw json data to __data_generators and Converts raw data range and list to python list.
        :param raw_json:
        :return:
        """
        processed_datas = []
        for raw_data in raw_json:
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



    def __read_csv(self, path):
        """
        :param path: Path to raw data csv file.
        :return: json of raw data
        """
        raw_list = []
        with open(os.path.abspath(path), 'r')as csv_file:
            csv_data = csv.DictReader(csv_file)
            for data in csv_data:
                raw_list.append(data)
        return raw_list

if __name__=="__main__":
    lTestDataGenerator = TestDataGenerator()
    lTestDataGenerator.write_excel()
