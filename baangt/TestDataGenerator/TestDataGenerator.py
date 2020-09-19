import csv
import itertools
import xlsxwriter
import errno
import os
import logging
import faker
from random import sample, choice
import baangt.base.GlobalConstants as GC
import re
import sys
import pandas as pd
from CloneXls import CloneXls
import json

logger = logging.getLogger("pyC")


class PrefixData:
    def __init__(self, dataList, prefix, tdg_object=None):
        self.dataList = dataList
        self.prefix = prefix
        self.tdg_object = tdg_object
        self.process()

    def process(self):
        if self.prefix.lower() == "rrd" or self.prefix.lower() == "rre":
            self.dataList = [
                data for data in self.dataList if not self.tdg_object.usecount_dict[repr(data)]["limit"] or \
                self.tdg_object.usecount_dict[repr(data)]['use'] < self.tdg_object.usecount_dict[repr(data)]['limit']
               ]

        elif self.prefix.lower() == "fkr":
            fake = faker.Faker(self.dataList[1])
            fake_lis = []
            if len(self.dataList) == 3:
                if int(self.dataList[2]) == 0:
                    fake_lis.append(getattr(fake, self.dataList[0])())
                else:
                    for x in range(int(self.dataList[2])):
                        fake_lis.append(getattr(fake, self.dataList[0])())
            else:
                for x in range(5):
                    fake_lis.append(getattr(fake, self.dataList[0])())
            self.dataList = fake_lis

    def return_random(self):
        if self.prefix == "rre" or self.prefix == "rrd":
            if not len(self.dataList):
                print(self.dataList)
                raise BaseException(f"Not enough data, please verify if data is present or usecount limit" \
                                    "has reached!!")
            data = choice(self.dataList)
            self.tdg_object.usecount_dict[repr(data)]['use'] += 1
            if self.tdg_object.usecount_dict[repr(data)]['limit'] and \
                self.tdg_object.usecount_dict[repr(data)]['use'] >= self.tdg_object.usecount_dict[repr(data)]['limit']:
                self.dataList.remove(data)
            return data

        elif self.prefix.lower() == "fkr":
            return choice(self.dataList)

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

    :param rawExcelPath: Takes input path for xlsx file containing input data.
    :param sheetName: Name of sheet where all base data is located.
    :method write: Will write the final processed data in excel/csv file.
    """
    def __init__(self, rawExcelPath=GC.TESTDATAGENERATOR_INPUTFILE, sheetName="",
                 from_handleDatabase=False, noUpdate=True):
        self.path = os.path.abspath(rawExcelPath)
        self.sheet_name = sheetName
        if not os.path.isfile(self.path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.path)
        self.sheet_dict, self.raw_data_json = self.read_excel(self.path, self.sheet_name)
        self.rre_sheets = {}
        self.isUsecount = {}
        self.remove_header = []
        self.usecount_dict = {}  # used to maintain usecount limit record and verify if that non of the data cross limit
        self.done = {}
        self.noUpdateFiles = noUpdate
        self.writers = {}
        if not from_handleDatabase:
            self.processed_datas = self.__process_data(self.raw_data_json)
            self.final_data = self.__generateFinalData(self.processed_datas)
            if self.isUsecount:
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
        if OutputFormat.lower() == "xlsx":
            if outputfile == None:
                outputfile = GC.TESTDATAGENERATOR_OUTPUTFILE_XLSX
            #self.__write_excel(batch_size=batch_size, outputfile=outputfile)
            with pd.ExcelWriter(outputfile) as writer:
                self.final_data.to_excel(writer, index=False)
            writer.save()
        elif OutputFormat.lower() == "csv":
            if outputfile == None:
                outputfile = GC.TESTDATAGENERATOR_OUTPUTFILE_CSV
            self.__write_csv(batch_size=batch_size, outputfile=outputfile)
        else:
            logger.debug("Incorrect file format")

    def __write_excel(self, outputfile=GC.TESTDATAGENERATOR_OUTPUTFILE_XLSX, batch_size=0):
        """
        Writes TestData file with final processsed data.
        :param outputfile: Name and path for output file.
        :param batch_size: No. of data to be randomly selected and written in output file.
        :return: None
        """
        if batch_size > 0:
            if len(self.final_data) > batch_size:
                data_lis = sample(self.final_data, batch_size)
            else:
                data_lis = self.final_data
                logger.debug("Total final data is smaller than batch size.")
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
        :param batch_size: No. of data to be randomly selected and written in output file.
        :return:
        """
        if batch_size > 0:
            if len(self.final_data) > batch_size:
                data_lis = sample(self.final_data, batch_size)
            else:
                data_lis = self.final_data
        else:
            data_lis = self.final_data
        with open(outputfile, 'w', newline='\n', encoding='utf-8-sig') as file:
            fl = csv.writer(file)
            fl.writerow(self.headers)
            for dt in data_lis:
                fl.writerow(list(dt))

    def __generateFinalData(self, processed_data):
        """
        This method will do the final process on the processed_data. Processed_data contains list of dictionary, each
        dictionary is the row from input file which are processed to be interact able in python as per the requirement.

        First loop is of processed_data
        Second loop is of the dictionary(row) and each key:value of that dictionary is header:processed_data

        Method will first check the data type of value.
        If it is a string than method will put it inside a list(i.e. ["string"])
        If it is a tuple than it is a data with prefix so it will be sent to ``__prefix_data_processing`` method for
        further processing.
        Else the value is of type list.

        Then we store all this lists in a list(can be treat as row). This list contains value of cells. They are evaluted
        i.e. ranges are converted to list, strings are converted to list & list are all ready list. So to generate all
        possible combinations from it we use ``iterable`` module.

        Once this list of lists which contains all possible combinations is created we will call
        ``__update_prefix_data_in_final_list`` method. This method will insert the processed prefix data along with the
        data of all combinations list in the final list with the correct position of every value.

        Finally it will return the list of lists which is completely processed and ready to be written in output file.

        :param processed_data:
        :return: Final_data_list
        """
        for dic in processed_data:
            for key in dic:
                if type(dic[key]) == PrefixData:
                    dic[key] = dic[key].return_random()
        final_data = pd.DataFrame(processed_data)
        return final_data

    def __process_data(self, raw_json):
        """
        This method is used to Process all the raw unprocessed data read from the excel file.

        It will first send the header to ``__data_generator`` so that if it is a list then it will get converted in
        individual header.

        Later it will process the values using ``__data_generator``.

        It will then check returned iterable type, if it is a tuple that mean input value was with prefix, so, it will
        further check if the tuple contains dict. If True than prefix was RRD_. In that case we will have to deal with
        the original header of the input value. Because if the original value's header is not in the TargetData then this
        header will contain no value in the output file and my cause errors too. So the header will added in
        ``self.remove_header`` list which will be further used to remove it from main header list.

        Finally it will return list of dictionarys. Each dictionary contains processed data of a row of input file.
        Processed data are the raw data converted into python data type and iterables. Ranges are converted into list.

        :param raw_json:
        :return:
        """
        processed_datas = []
        raw_json = json.loads(raw_json.to_json(orient="records"))
        for raw_data in raw_json:
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
        print(len(processed_datas))
        return processed_datas

    @staticmethod
    def product_dict(**kwargs):
        keys = kwargs.keys()
        vals = kwargs.values()
        for instance in itertools.product(*vals):
            yield dict(zip(keys, instance))

    def data_generators(self, raw_data_old):
        """
        This method first send the data to ``__raw_data_string_process`` method to split the data and remove the unwanted
        spaces.

        Later this method uses other methods to convert all the different data_types from string to their respective
        python data types.
        i.e. string list to python list, etc.

        Later according to the prefix of data and the data_type assigned it will convert them.
        Simple list and strings are converted in to ``list`` type.
        Data with prefix will converted in to ``tuple`` type so further it will be helpful in distinguishing. Also it will
        insert the prefix name in first value of tuple if the prefix is ``FKR_`` so it will be helpful in further process.

        Finally it will return the iterable for further process.

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
            processed_datas = PrefixData(processed_datas, 'rnd')

        elif prefix == "Faker":
                dataList = [data.strip() for data in raw_data[1:-1].split(",")]
                processed_datas = PrefixData(dataList, prefix="fkr")

        elif prefix == "Rrd":
            sheet_name, data_looking_for, data_to_match = self.extractDataFromRrd(raw_data)
            try:
                dataList = self.__processRrdRre(sheet_name, data_looking_for, data_to_match)
                processed_datas = PrefixData(dataList, prefix='rrd', tdg_object=self)
            except KeyError:
                sys.exit(f"Please check that source files contains all the headers mentioned in : {raw_data_old}")

        elif prefix == "Rre":
            file_name = raw_data[1:-1].split(',')[0].strip()
            sheet_name, data_looking_for, data_to_match = self.extractDataFromRrd(raw_data, index=1)
            try:
                dataList = self.__processRrdRre(sheet_name, data_looking_for, data_to_match, filename=file_name)
                processed_datas = PrefixData(dataList, prefix="rre", tdg_object=self)
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
        if filename:
            filename = os.path.join(os.path.dirname(self.path), filename)
            if not self.noUpdateFiles:
                file_name = ".".join(filename.split(".")[:-1])
                file_extension = filename.split(".")[-1]
                file = file_name + "_baangt" + "." + file_extension
            else:
                file = filename
            if not file in self.rre_sheets:
                logger.debug(f"Creating clone file of: {filename}")
                if not self.noUpdateFiles:
                    filename = CloneXls(filename).update_or_make_clone()
                self.rre_sheets[filename] = {}
            filename = file
            if sheet_name in self.rre_sheets[filename]:
                df = self.rre_sheets[filename][sheet_name]
            else:
                df = pd.read_excel(filename, sheet_name, dtype=str)
                df.fillna("", inplace=True)
                self.rre_sheets[filename][sheet_name] = df
        else:
            df = self.sheet_dict[sheet_name]
            if not self.path in self.rre_sheets:
                self.rre_sheets[self.path] = {}
            if not sheet_name in self.rre_sheets[self.path]:
                self.rre_sheets[self.path][sheet_name] = df
        df1 = df.copy()
        for key, value in data_to_match.items():
            if not isinstance(value, list):
                value = [value]
            df1 = df1.loc[df1[key].isin(value)]
        data_lis = []

        if type(data_looking_for) == str:
            data_looking_for = data_looking_for.split(",")
        data_new_header = {}
        data_looking_for_old = data_looking_for[:]
        data_looking_for = []
        for header in data_looking_for_old:
            if ":" in header:
                old_header = header.split(":")[0].strip()
                new_header = header.split(":")[1].strip()
            else:
                old_header = header
                new_header = header
            data_new_header[old_header] = new_header
            data_looking_for.append(header)

        key_name = repr(sheet_name) + repr(data_looking_for) + repr(data_to_match) + repr(filename)
        if key_name in self.done:
            logger.debug(f"Data Gathered from previously saved data.")
            return self.done[key_name]

        usecount, limit, usecount_header = self.check_usecount(df.columns.values.tolist())
        if not filename:
            if self.path not in self.isUsecount:
                self.isUsecount[self.path] = usecount_header
            if not self.isUsecount[self.path]:
                self.isUsecount[self.path] = usecount_header
        else:
            if filename not in self.isUsecount:
                self.isUsecount[filename] = usecount_header
            if not self.isUsecount[filename]:
                self.isUsecount[filename] = usecount_header
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
                data_lis.append(data)
                self.usecount_dict[repr(data)] = {
                    "use": used_limit, "limit": limit, "index": index,
                    "sheet_name": sheet_name, "file_name": filename
                }
            else:
                dt = {header: data[keys] for (keys, header) in zip(data_looking_for, data_looking_for_old)}
                data_lis.append(dt)
                self.usecount_dict[repr(dt)] = {
                    "use": used_limit, "limit": limit, "index": index,
                    "sheet_name": sheet_name, "file_name": filename
                }

        if len(data_lis) == 0:
            logger.info(f"No data matching: {data_to_match}")
            sys.exit(f"No data matching: {data_to_match}")
        logger.debug(f"New Data Gathered.")
        self.done[key_name] = data_lis
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
        if self.noUpdateFiles:
            return 
        for filename in self.isUsecount:
            logger.debug(f"Updating file {filename} with usecounts.")
            sheet_dict = self.rre_sheets[filename]
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
        if self.noUpdateFiles:
            return 
        filename = self.usecount_dict[repr(data)]["file_name"]
        if not filename:
            filename = self.path
        if filename not in self.isUsecount:
            return
        if not self.isUsecount[filename]:
            return
        self.rre_sheets[filename][self.usecount_dict[repr(data)]["sheet_name"]][
            self.isUsecount[filename]][self.usecount_dict[repr(data)]["index"]] = self.usecount_dict[repr(data)]["use"]

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
        variable = string[1:-1].strip().split(',')[0].strip()
        data = os.environ.get(variable)
        try:
            if not data:
                data = string[1:-1].strip().split(',')[1].strip()
                logger.info(f"{variable} not found in environment, using {data} instead")
        except:
            raise BaseException(f"Can't find {variable} in envrionment & default value is also not set")
        return data


if __name__ == "__main__":
    lTestDataGenerator = TestDataGenerator("../../tests/0TestInput/RawTestData.xlsx")
    lTestDataGenerator.write()
