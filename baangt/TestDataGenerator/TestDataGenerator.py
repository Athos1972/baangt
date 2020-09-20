import itertools
import errno
import os
import logging
import faker
from random import choice
import baangt.base.GlobalConstants as GC
import re
import sys
import pandas as pd
from CloneXls import CloneXls
import json

logger = logging.getLogger("pyC")


class PrefixDataManager:
    def __init__(self, dataList: list, prefix: str, tdg_object=None):
        """
        This class manages data list as per functionality of their prefix
        :param dataList: List of data to be managed
        :param prefix: RRE, RRD, FKR, RND are the prefixs managed by this class
        :param tdg_object: TestDataGenerator object, only useful in RRE, RRD prefix to update usecount
        """
        self.dataList = dataList        # Iterable object to be managed
        self.prefix = prefix            # Prefix data
        self.tdg_object = tdg_object    # used to update usecount data, only for rre and rrd
        self.process()

    def process(self):
        """
        It processes the data list with respect to their prefix and save it in dataList attribute.
        :return: 
        """
        if self.prefix.lower() == "rrd" or self.prefix.lower() == "rre":
            self.dataList = [
                data for data in self.dataList if not self.tdg_object.usecountDataRecords[repr(data)]["limit"] or \
                self.tdg_object.usecountDataRecords[repr(data)]['use'] < self.tdg_object.usecountDataRecords[repr(data)]['limit']
               ]    # removing data with reached use limit

        elif self.prefix.lower() == "fkr":
            fake = faker.Faker(self.dataList[1])               # Creating faker class object
            fake_lis = []                                                       
            if len(self.dataList) == 3:         # Checks if their is any predefined number of fake data to be generated
                if int(self.dataList[2]) == 0:                 # if number of predefined data is 0 then we need to 
                    fake_lis.append([fake, self.dataList[0]])  # generate new data for each call so the required info
                    fake_lis = tuple(fake_lis)                 # is saved as tuple so program can distinguish
                else:
                    for x in range(int(self.dataList[2])):  # if greater than 0, list is created with defined number of data
                        fake_lis.append(getattr(fake, self.dataList[0])())  # on every call random data is sent from list
            else:
                for x in range(5):          # if their is no predefined number of data than a list of 5 fake data
                    fake_lis.append(getattr(fake, self.dataList[0])())  # is generated
            self.dataList = fake_lis

    def return_random(self):
        """
        It returns data as per their prefix
        :return: 
        """
        if self.prefix == "rre" or self.prefix == "rrd":
            if not len(self.dataList):
                raise BaseException(f"Not enough data, please verify if data is present or usecount limit" \
                                    "has reached!!")
            data = choice(self.dataList)
            self.tdg_object.usecountDataRecords[repr(data)]['use'] += 1  # updates usecount in TDG object
            if self.tdg_object.usecountDataRecords[repr(data)]['limit'] and \
                self.tdg_object.usecountDataRecords[repr(data)]['use'] >= self.tdg_object.usecountDataRecords[repr(data)]['limit']:
                self.dataList.remove(data)  # checks usecount after using a data and removes if limit is reached
            return data

        elif self.prefix.lower() == "fkr":
            if type(self.dataList) == tuple:  # if type is tuple then we need generate new data on every call
                return getattr(self.dataList[0][0], self.dataList[0][1])()
            return choice(self.dataList)  # else it is a list and we can send any random data from it

        elif self.prefix == 'rnd':
            return choice(self.dataList)


class TestDataGenerator:
    """
    TestDataGenerator Class is to used to create a TestData file from raw excel file containing all possible values.

    Formats accepted in input excel file:
    1. Value             = ``<value>``
    2. list of values    = ``[<value1>,<value2>]``
    3. range             = ``<start>-<end>,<step>``
    4. random            = ``RND_[list]``
    5. random from range = ``RND_<start>-<end>,<step>``
    6. List of header    = ``[<title1>, <title2>, <title3>]``
    7. Faker Prefix      = ``FKR_(<type>, <locale>, <number_of_data>)``
    8. RRD Prefix        = ``RRD_(<sheetName>,<TargetData>,[<Header1>:[<Value1>],<Header2>:[<Value1>,<Value2>]])``
    9. RRE Prefix        = ``RRE_(<fileName>,<sheetName>,<TargetData>,[<Header1>:[<Value1>],<Header2>:[<Value1>,<Value2>]])``
    10. Renv Prefix      = ``RENV_(<environmentVariable>,<default>)

    :param rawExcelPath: Takes input path for xlsx file containing input data.
    :param sheetName: Name of sheet where all base data is located.
    :method write: Will write the final processed data in excel/csv file.
    """
    def __init__(self, rawExcelPath=GC.TESTDATAGENERATOR_INPUTFILE, sheetName="",
                 from_handleDatabase=False, noUpdate=True):
        self.fileNameAndPath = os.path.abspath(rawExcelPath)
        self.sheet_name = sheetName
        if not os.path.isfile(self.fileNameAndPath):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.fileNameAndPath)
        self.allDataFramesDict, self.mainDataFrame = self.read_excel(self.fileNameAndPath, self.sheet_name)
        self.openedSheetsDataFrame = {}  # stores filenames which contains sheetname: sheetDataFrame
        self.usecountHeaderName = {}   # contains filenames which contains sheetname: usecountHeaderName
        self.usecountDataRecords = {}  # used to maintain usecount limit record and verify non of the data cross limit
        self.rreRrdProcessedData = {}  # stores rre processed data with its criteria as key and used when same criteria
        self.noUpdateFiles = noUpdate
        if not from_handleDatabase:
            self.processed_data = self.processDataFrame(self.mainDataFrame)
            self.finalDataFrame = self.updatePrefixData(self.processed_data)
            if self.usecountHeaderName:
                if not self.noUpdateFiles:
                    self.save_usecount()  # saving source input file once everything is done

    def write(self, OutputFormat=GC.TESTDATAGENERATOR_OUTPUT_FORMAT, batch_size=0, outputfile=None):
        """
        Will write the generated data in output file.
        :param OutputFormat: "xlsx" or "csv"
        :param batch_size: Number of data to be written in output file. Will be randomly selected.
        :param outputfile: name and path of outputfile.
        :return:
        """
        if batch_size > 0:
            if len(self.finalDataFrame) > batch_size:
                data_lis = self.finalDataFrame.sample(n=batch_size)
            else:
                data_lis = self.finalDataFrame
                logger.debug("Total final data is smaller than batch size.")
        else:
            data_lis = self.finalDataFrame

        if OutputFormat.lower() == "xlsx":
            if outputfile == None:
                outputfile = GC.TESTDATAGENERATOR_OUTPUTFILE_XLSX
            with pd.ExcelWriter(outputfile) as writer:
                data_lis.to_excel(writer, index=False)
                writer.save()

        elif OutputFormat.lower() == "csv":
            if outputfile == None:
                outputfile = GC.TESTDATAGENERATOR_OUTPUTFILE_CSV
            data_lis.to_csv(outputfile)

        else:
            logger.debug("Incorrect file format")

    def updatePrefixData(self, processed_data):
        """

        :param processed_data:
        :return: Final_data_list
        """
        for dic in processed_data:
            for key in dic.copy():
                if type(dic[key]) == PrefixDataManager:
                    data = dic[key].return_random()
                    if type(data) == dict:
                        del dic[key]
                        dic.update(data)
                    else:
                        dic[key] = data
        final_data = pd.DataFrame(processed_data)
        return final_data

    def processDataFrame(self, dataFrame):
        """
        This method is used to Process all the raw unprocessed data read from the excel file.

        It will first send the header to ``__splitList`` so that if it is a list then it will get converted in
        individual header.

        Later it will process the values using ``__data_generator``.

        It will then check returned data type, and convert it into list if it is not already. Then from every row which
        are dict contains value/values inside list it will use itertools to create all possible combination, now every
        data in the value list is converted in a new row with value as string.

        Finally it will return list of dictionary. Each dictionary contains processed data of a row of input file.
        Processed data are the raw data converted into python data type and class. Ranges are converted into list.

        :param dataFrame:
        :return:
        """
        processed_datas = []
        json_df = json.loads(dataFrame.to_json(orient="records"))
        for raw_data in json_df:
            if not list(raw_data.values())[0]:
                continue
            processed_data = {}
            for key in raw_data:
                keys = self.__splitList(key)
                for ke in keys:
                    data = self.data_generators(raw_data[key])
                    if type(data) != list:
                        processed_data[ke] = [data]
                    else:
                        processed_data[ke] = data
            product = list(self.product_dict(**processed_data))
            processed_datas += product
        return processed_datas

    def data_generators(self, raw_data_old):
        """
        This method first send the data to ``__raw_data_string_process`` method to split the data and remove the unwanted
        spaces.

        Later this method uses other methods to convert all the different data_types from string to their respective
        python data types.
        i.e. string list to python list, etc.

        Later according to the prefix of data and the data_type assigned it will convert them.
        Simple list and strings are converted in to ``list`` type.
        Data with prefix will be processed and the data list generated by them is used to create PrefixDataManager class
        so later when we need to get the final data this class is used to get the data as per prefix and requirements.

        Finally it will return the data for further process.

        :param raw_data:
        :return: List or Tuple containing necessary data
        """
        raw_data, prefix, data_type = self.__raw_data_string_process(raw_data_old)
        if len(raw_data)<=1:
            return [""]

        if prefix == "Rnd":
            if "-" in raw_data:
                raw_data = raw_data.split('-')
                start = raw_data[0].strip()
                end = raw_data[1].strip()
                step = 1
                if "," in end:
                    raw_data = end.split(",")
                    end = raw_data[0].strip()
                    step = raw_data[1].strip()
                processed_datas = [x for x in range(int(start), int(end) + 1, int(step))]
            else:
                processed_datas = self.__splitList(raw_data)
            processed_datas = PrefixDataManager(processed_datas, 'rnd')

        elif prefix == "Faker":
                dataList = [data.strip() for data in raw_data[1:-1].split(",")]
                processed_datas = PrefixDataManager(dataList, prefix="fkr")

        elif prefix == "Rrd":
            sheet_name, data_looking_for, data_to_match = self.extractDataFromRrd(raw_data)
            try:
                dataList = self.__processRrdRre(sheet_name, data_looking_for, data_to_match)
                processed_datas = PrefixDataManager(dataList, prefix='rrd', tdg_object=self)
            except KeyError:
                sys.exit(f"Please check that source files contains all the headers mentioned in : {raw_data_old}")

        elif prefix == "Rre":
            file_name = raw_data[1:-1].split(',')[0].strip()
            sheet_name, data_looking_for, data_to_match = self.extractDataFromRrd(raw_data, index=1)
            try:
                dataList = self.__processRrdRre(sheet_name, data_looking_for, data_to_match, filename=file_name)
                processed_datas = PrefixDataManager(dataList, prefix="rre", tdg_object=self)
            except KeyError:
                sys.exit(f"Please check that source files contains all the headers mentioned in : {raw_data_old}")

        elif prefix == "Renv":
            processed_datas = self.get_env_variable(raw_data)

        elif raw_data[0] == "[" and raw_data[-1] == "]":
            processed_datas = self.__splitList(raw_data)

        elif "-" in raw_data:
            raw_data_original = raw_data[:]
            raw_data = raw_data.split('-')
            start = raw_data[0].strip()
            end = raw_data[1].strip()
            step = 1
            if "," in end:
                raw_data = end.split(",")
                end = raw_data[0].strip()
                step = raw_data[1].strip()
            try:
                processed_datas = [x for x in range(int(start), int(end)+1, int(step))]
            except:
                processed_datas = [raw_data_original.strip()]

        else:
            processed_datas = raw_data.strip()
        return processed_datas

    def extractDataFromRrd(self, raw_data, index=0):
        """
        Splits rrd/rre string and used them according to their position
        :param raw_data:
        :param index:
        :return:
        """
        first_value = raw_data[1:-1].split(',')[0+index].strip()
        second_value = raw_data[1:-1].split(',')[1+index].strip()
        if second_value[0] == "[":
            second_value = ','.join(raw_data[1:-1].split(',')[1+index:]).strip()
            second_value = second_value[:second_value.index(']') + 1]
            third_value = [x.strip() for x in ']'.join(raw_data[1:-1].split(']')[1:]).split(',')[1:]]
        else:
            third_value = [x.strip() for x in raw_data[1:-1].split(',')[2+index:]]
        evaluated_list = ']],'.join(','.join(third_value)[1:-1].strip().split('],')).split('],')
        if evaluated_list[0] == "":
            evaluated_dict = {}
        else:
            evaluated_dict = {
                splited_data.split(':')[0]: self.__splitList(splited_data.split(':')[1]) for splited_data in
                evaluated_list
            }
        if second_value[0] == "[" and second_value[-1] == "]":
            second_value = self.__splitList(second_value)
        return first_value, second_value, evaluated_dict

    def __processRrdRre(self, sheet_name, data_looking_for, data_to_match: dict, filename=None):
        if filename:  # if filename than it is an rre file so we have to use filename instead of base file
            filename = os.path.join(os.path.dirname(self.fileNameAndPath), filename)
            if not self.noUpdateFiles:
                file_name = ".".join(filename.split(".")[:-1])
                file_extension = filename.split(".")[-1]
                file = file_name + "_baangt" + "." + file_extension
            else:
                file = filename
            if not file in self.openedSheetsDataFrame:
                logger.debug(f"Creating clone file of: {filename}")
                if not self.noUpdateFiles:
                    filename = CloneXls(filename).update_or_make_clone()
                self.openedSheetsDataFrame[filename] = {}
            filename = file
            if sheet_name in self.openedSheetsDataFrame[filename]:
                df = self.openedSheetsDataFrame[filename][sheet_name]
            else:
                df = pd.read_excel(filename, sheet_name, dtype=str)
                df.fillna("", inplace=True)
                self.openedSheetsDataFrame[filename][sheet_name] = df
        else:
            df = self.allDataFramesDict[sheet_name]
            if not self.fileNameAndPath in self.openedSheetsDataFrame:
                self.openedSheetsDataFrame[self.fileNameAndPath] = {}
            if not sheet_name in self.openedSheetsDataFrame[self.fileNameAndPath]:
                self.openedSheetsDataFrame[self.fileNameAndPath][sheet_name] = df
        df1 = df.copy()
        for key, value in data_to_match.items():
            if not isinstance(value, list):
                value = [value]
            df1 = df1.loc[df1[key].isin(value)]
        data_lis = []

        if type(data_looking_for) == str:
            data_looking_for = data_looking_for.split(",")
        data_new_header = {}
        for header in data_looking_for:
            if ":" in header:
                old_header = header.split(":")[0].strip()
                new_header = header.split(":")[1].strip()
            else:
                old_header = header
                new_header = header
            data_new_header[old_header] = new_header

        key_name = repr(sheet_name) + repr(data_looking_for) + repr(data_to_match) + repr(filename)
        if key_name in self.rreRrdProcessedData:
            logger.debug(f"Data Gathered from previously saved data.")
            return self.rreRrdProcessedData[key_name]

        usecount, limit, usecount_header = self.check_usecount(df.columns.values.tolist())
        if not filename:
            if self.fileNameAndPath not in self.usecountHeaderName:
                self.usecountHeaderName[self.fileNameAndPath] = {}
            if sheet_name not in self.usecountHeaderName[self.fileNameAndPath] and usecount_header:
                self.usecountHeaderName[self.fileNameAndPath][sheet_name] = usecount_header
        else:
            if filename not in self.usecountHeaderName:
                self.usecountHeaderName[filename] = {}
            if sheet_name not in self.usecountHeaderName[filename]:
                self.usecountHeaderName[filename][sheet_name] = usecount_header
        df1_dict = df1.to_dict(orient="index")
        for index in df1_dict:
            data = df1_dict[index]
            if usecount_header:
                try:
                    used_limit = int(data[usecount_header])
                except:
                    used_limit = 0
            else:
                used_limit = 0

            if data_looking_for[0] == "*":
                if usecount_header:
                    del data[usecount_header]
                data_lis.append(data)
                self.usecountDataRecords[repr(data)] = {
                    "use": used_limit, "limit": limit, "index": index,
                    "sheet_name": sheet_name, "file_name": filename
                }
            else:
                dt = {data_new_header[header]: data[header] for header in data_new_header}
                data_lis.append(dt)
                self.usecountDataRecords[repr(dt)] = {
                    "use": used_limit, "limit": limit, "index": index,
                    "sheet_name": sheet_name, "file_name": filename
                }

        if len(data_lis) == 0:
            logger.info(f"No data matching: {data_to_match}")
            sys.exit(f"No data matching: {data_to_match}")
        logger.debug(f"New Data Gathered.")
        self.rreRrdProcessedData[key_name] = data_lis
        return data_lis

    def __raw_data_string_process(self, raw_string):
        """
        Returns ``String, prefix, data_type`` which are later used to decided the process to perform on string.
        Their depth explanation are written in the function where they are used.

        It will process the value string of all cells in the input sheet.
        It will first convert all floats into string as by default xlrd ints are converted in float
        Later it will check if the string size is greater than 4 or not. If not then it will simply return the values,
        else it will process further.

        If string has more than 4 characters, this method will look if the fourth character is "_" or not. If not it will
        return the values. Else it mean there is prefix in string and it will process further.

        Later it will split the prefix from the value and define the data_type according to the string.
        If their is no matching prefix then the data type wil be list else it will be tuple.

        :param raw_string:
        :return: String of values, prefix, Data_type
        """
        if type(raw_string) == float:
            raw_string = int(raw_string)
        raw_string = str(raw_string).strip()
        prefix = ""
        if len(raw_string)>4:
            if raw_string[3] == "_":
                if raw_string[:4].lower() == "rnd_":
                    prefix = "Rnd"
                    raw_string = raw_string[4:]
                    data_type = tuple
                elif raw_string[:4].lower() == "fkr_":
                    prefix = "Faker"
                    raw_string = raw_string[4:]
                    data_type = tuple
                elif raw_string[:4].lower() == "rrd_":         # Remote Random (Remote = other sheet)
                    prefix = "Rrd"
                    raw_string = self.__process_rrd_string(raw_string)
                    raw_string = raw_string[4:]
                    data_type = tuple
                elif raw_string[:4].lower() == "rre_":         # Remote Random (Remote = other sheet)
                    prefix = "Rre"
                    raw_string = self.__process_rre_string(raw_string)
                    raw_string = raw_string[4:]
                    data_type = tuple
                else:
                    data_type = list
            else:
                if raw_string[:5].lower() == "renv_":
                    prefix = "Renv"
                    raw_string = raw_string[5:]
                data_type = list
        else:
            data_type = list
        return raw_string, prefix, data_type

    def get_str_sheet(self, excel, sheet):
        """
        Returns dataFrame with all data treated as string
        :param excel:
        :param sheet:
        :return:
        """
        columns = excel.parse(sheet).columns
        converters = {column: str for column in columns}
        data = excel.parse(sheet, converters=converters)
        data.fillna("", inplace=True)
        return data

    def read_excel(self, path, sheet_name="", return_json=False):
        """
        This method will read the input excel file.
        It will read all the sheets inside this excel file and will create a dictionary of dictionary containing all data
        of every sheet.
        i.e. {"sheetName": {headers**: data**}}

        It will also look for a base sheet whose name must be given while creating the instance. If no sheet name is
        given then first sheet of the file will be considered as base sheet.

        Finally it will return a dictionary containing sheetNames:data of all sheets & dictionary of base sheet.

        :param path: Path to raw data xlsx file.
        :param sheet_name: Name of base sheet sheet where main input data is located. Default will be the first sheet.
        :return: Dictionary of all sheets and data, Dictionary of base sheet.
        """
        wb = pd.ExcelFile(path)
        sheet_lis = wb.sheet_names
        sheet_df = {}
        for sheet in sheet_lis:
            sheet_df[sheet] = self.get_str_sheet(wb, sheet)
            sheet_df[sheet].fillna("", inplace=True)
        if return_json:
            for df in sheet_df.keys():
                sheet_df[df] = json.loads(sheet_df[df].to_json(orient="records"))
        if sheet_name == "":
            base_sheet = sheet_df[sheet_lis[0]]
        else:
            assert sheet_name in sheet_df, f"Excel file doesn't contain {sheet_name} sheet. Please recheck."
            base_sheet = sheet_df[sheet_name]
        return sheet_df, base_sheet

    @staticmethod
    def __splitList(raw_data):
        """
        Will convert string list to python list.
        i.e. "[value1,value2,value3]" ==> ["value1","value2","value3"]
        :param raw_data: string of list
        :return: Python list
        """
        if raw_data[0] == "[" and raw_data[-1] == "]":
            data = raw_data[1:-1]
        else:
            data = raw_data
        proccesed_datas = [data.strip() for data in data.split(",")]
        return proccesed_datas

    def check_usecount(self, data):
        # used to find and return if their is usecount header and limit in input file
        usecount = False
        limit = 0
        usecount_header = None
        for header in data:
            if "usecount" in header.lower():
                usecount = True
                usecount_header = header
                if "usecount_" in header.lower():
                    try:
                        limit = int(header.lower().strip().split("count_")[1])
                    except:
                        limit = 0
        return usecount, limit, usecount_header

    def save_usecount(self):
        """
        Saves the excel file in which have usecount to be updated
        :return:
        """
        if self.noUpdateFiles:
            return 
        for filename in self.usecountHeaderName:
            logger.debug(f"Updating file {filename} with usecounts.")
            sheet_dict = self.openedSheetsDataFrame[filename]
            ex = pd.ExcelFile(filename)
            for sheet in ex.sheet_names:
                if sheet in sheet_dict:
                    continue
                df = self.get_str_sheet(ex, sheet)
                sheet_dict[sheet] = df
            with pd.ExcelWriter(filename) as writer:
                for sheetname in sheet_dict:
                    sheet_dict[sheetname].to_excel(writer, sheetname, index=False)
                writer.save()
            logger.debug(f"File updated {filename}.")

    def update_usecount_in_source(self, data):
        """
        Updates usecount in the dataframe in correct position. These function only updates not save the file.
        :param data:
        :return:
        """
        if self.noUpdateFiles:
            return 
        filename = self.usecountDataRecords[repr(data)]["file_name"]
        sheetName = self.usecountDataRecords[repr(data)]["sheet_name"]
        if not filename:
            filename = self.fileNameAndPath
        if filename not in self.usecountHeaderName:
            return
        elif sheetName not in self.usecountHeaderName[filename]:
            return
        if not self.usecountHeaderName[filename][sheetName]:
            return
        self.openedSheetsDataFrame[filename][sheetName][self.usecountHeaderName[filename][sheetName]][
            self.usecountDataRecords[repr(data)]["index"]] = self.usecountDataRecords[repr(data)]["use"]

    def __process_rrd_string(self, rrd_string):
        """
        This method is used to validate rrd_strings provided by the user.
        If their will be any error in string this fuction will immediately create an error and will stop further execution.
        Also these function will remove empty spaces around the commas in string.
        Regex supporting formats in this method are:
        ``RRD_[sheetName,TargetData,[Header:[values**],Header:[values**]]]``
        ``RRD_[sheetName,[TargetData**],[Header:[values**],Header:[values**]]]``
        ``RRD_(sheetName,[TargetData**],[Header:[values**],Header:[values**]])``
        ``RRD_[sheetName,*,[Header:[values**],Header:[values**]]]``
        ``RRD_[sheetName,*,[Header:[values**],Header:[values**]]]``
        ``RRD_[sheetName,TargetData,[]]``
        ``RRD_(sheetName,TargetData,[])``
        ``RRD_(sheetName,*,[])``
        ``RRD_[sheetName,*,[]]``
        :param rrd_string:
        :return:
        """
        processed_string = ','.join([word.strip() for word in rrd_string.split(', ')])
        match = re.match(r"(RRD_(\(|\[))[a-zA-z0-9\s]+,(\[?[a-zA-z\s,]+\]?|)|\*,\[([a-zA-z0-9\s]+:\[[a-zA-z0-9,\s]+\](,?))*\]",processed_string)
        err_string = f"{rrd_string} not matching pattern RRD_(sheetName,TargetData," \
                     f"[Header1:[Value1],Header2:[Value1,Value2]])"
        assert match, err_string
        return processed_string

    def __process_rre_string(self, rrd_string):
        """
        This method is used to validate rrd_strings provided by the user.
        If their will be any error in string this fuction will immediately create an error and will stop further execution.
        Also these function will remove empty spaces around the commas in string.
        Regex supporting formats in this method are:
        ``RRE_[fileName,sheetName,TargetData,[Header:[values**],Header:[values**]]]``
        ``RRE_[fileName,sheetName,[TargetData**],[Header:[values**],Header:[values**]]]``
        ``RRE_(fileName,sheetName,[TargetData**],[Header:[values**],Header:[values**]])``
        ``RRE_[fileName,sheetName,*,[Header:[values**],Header:[values**]]]``
        ``RRE_[fileName,sheetName,*,[Header:[values**],Header:[values**]]]``
        ``RRE_[fileName,sheetName,TargetData,[]]``
        ``RRE_(fileName,sheetName,TargetData,[])``
        ``RRE_(fileName,sheetName,*,[])``
        ``RRE_[fileName,sheetName,*,[]]``
        :param rrd_string:
        :return:
        """
        processed_string = ','.join([word.strip() for word in rrd_string.split(', ')])
        match = re.match(r"(RRE_(\(|\[))[\w\d\s\-./\\]+\.(xlsx|xls),[a-zA-z0-9\s]+,(\[?[a-zA-z\s,]+\]?|)|\*,\[([a-zA-z0-9\s]+:\[[a-zA-z0-9,\s]+\](,?))*\]",processed_string)
        err_string = f"{rrd_string} not matching pattern RRE_(fileName, sheetName, TargetData," \
                     f"[Header1:[Value1],Header2:[Value1,Value2]])"
        assert match, err_string
        return processed_string

    @staticmethod
    def get_env_variable(string):
        """
        Returns environment variable or the default value predefined.
        :param string:
        :return:
        """
        variable = string[1:-1].strip().split(',')[0].strip()
        data = os.environ.get(variable)
        try:
            if not data:
                data = string[1:-1].strip().split(',')[1].strip()
                logger.info(f"{variable} not found in environment, using {data} instead")
        except:
            raise BaseException(f"Can't find {variable} in envrionment & default value is also not set")
        return data

    @staticmethod
    def product_dict(**kwargs):
        """
        :param kwargs: Dictionary containing values in a list
        :return: yield dictionaries with individual value in dictionary from value list
        """
        keys = kwargs.keys()
        vals = kwargs.values()
        for instance in itertools.product(*vals):
            yield dict(zip(keys, instance))


if __name__ == "__main__":
    lTestDataGenerator = TestDataGenerator("../../tests/0TestInput/RawTestData.xlsx")
    lTestDataGenerator.write()
