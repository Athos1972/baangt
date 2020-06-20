import csv
import itertools
import xlsxwriter
import xl2dict
import xlrd
import errno
import os
import logging
import faker
from random import sample, randint
import baangt.base.GlobalConstants as GC
import re

logger = logging.getLogger("pyC")


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
    def __init__(self, rawExcelPath=GC.TESTDATAGENERATOR_INPUTFILE, sheetName=""):
        self.path = os.path.abspath(rawExcelPath)
        self.sheet_name = sheetName
        if not os.path.isfile(self.path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.path)
        self.sheet_dict, self.raw_data_json = self.__read_excel(self.path, self.sheet_name)
        self.remove_header = []
        self.processed_datas = self.__process_data(self.raw_data_json)
        self.headers = [x for x in list(self.processed_datas[0].keys()) if x not in self.remove_header]
        self.final_data = self.__generateFinalData(self.processed_datas)

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
            self.__write_excel(batch_size=batch_size, outputfile=outputfile)
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
        final_data = []
        for lis in processed_data:
            index = {}
            data_lis = []
            for key in lis:
                if type(lis[key]) == str:
                    data = [lis[key]]
                elif type(lis[key]) == tuple:
                    if len(lis[key]) > 0:
                        self.__prefix_data_processing(lis, key, index)
                        continue
                    else:
                        data = ['']
                else:
                    data = lis[key]
                data_lis.append(data)
            datas = list(itertools.product(*data_lis))
            self.__update_prefix_data_in_final_list(datas, index, final_data)
        logger.info(f"Total generated data = {len(final_data)}")
        return final_data

    def __update_prefix_data_in_final_list(self, data_list, dictionary, final_list):
        """
        This method will insert the data from the dictionary to final_list. So further it can be written in the output.

        ``data_list`` is the list where all possible combinations generated by the input lists and ranges are stored.
        ``dictionary`` is where the data with prefix are stored with their index value(which will be used to place data)
        ``final_list`` is the list where final data will be stored after merging values from data_list and dictionary

        First it will iterate through data_list which is list of lists(Also you can take it as list of rows).
        Second loop will go through dictionary and check the data type of each value. Pairings inside dictionary are of
        ``index: value`` here index is the position from where this value was picked. So it will be used in placing the
        data in their correct position.

        List:
        =====
            If value is list then it is a data with ``FKR_`` prefix with number of data 0(i.e. create new fake data for
            every output). So we will create the faker module instance as per the input and will generate fake data for
            every row. And will insert them in the position of index(key of dictionary).


        Dictionary:
        ==========
            If it is not of type list then we will check that if it is of type dict. If yes then this is a data with
            "RRD_" prefix and we have to select the random data here. So we will start looping through this dictionary.
            Remember this is the third loop. This dictionary contains header:value(TargetDatas from matched data) pair.
            On every loop it will first check that if the same header is stored in done dictionary. If yes then it will
            get value of it from done dictionary. Then it will create a list from the TargetData list. This new list
            will contain only data which has same value for same header stored in done dictionary.
            i.e. If matching Header has value x then from TargetDatas list only data where header=x will be
            considered for random pick.

            Then the random value is selected from that list.
            If none of the header is processed before(for the same row). Then it will get random data from the list and
            will store header: value pair in done dictionary so it is used in the checking process as above.

            It will also check if the ``self.header`` list contains all the header which are in the random selected data.
            If not then it will add the header there.

            At last we will index the position of header inside self.headers list and will insert the value in same
            position and append the row in final_data list.

        Tuple:
        ======
            If the type is tuple then we need to simply pick a random value from it and insert it in the same position of
            index(key of dictionary for current value).

        :param data_list:
        :param dictionary:
        :param final_list:
        :return: None
        """
        for data in data_list:
            data = list(data)
            done = {}
            for ind in dictionary:
                if type(dictionary[ind]) == list:
                    fake = faker.Faker(dictionary[ind][2])
                    data.insert(ind, getattr(fake, dictionary[ind][1])())
                else:
                    if type(dictionary[ind][0]) == dict:
                        sorted_data = False
                        for header in dictionary[ind][0]:
                            if header in done:
                                match = done[header]
                                sorted_data = [x for x in dictionary[ind] if x[header] == match]
                                break
                        if not sorted_data:
                            sorted_data = dictionary[ind]
                        data_to_insert = sorted_data[randint(0, len(sorted_data) - 1)]
                        for keys in data_to_insert:
                            if keys not in self.headers:
                                self.headers.append(keys)
                            if keys not in done:
                                data.insert(self.headers.index(keys), data_to_insert[keys])
                                done[keys] = data_to_insert[keys]
                    else:
                        data_to_insert = dictionary[ind][randint(0, len(dictionary[ind]) - 1)]
                        data.insert(ind, data_to_insert)
            final_list.append(data)

    def __prefix_data_processing(self, dic, key, dictionary: dict):
        """
        This method will process the datas with prefix.

        ``dic`` the dictionary where all data which are in final process is stored
        ``key`` the header of the current data which will be used now to call the data.
        ``dictionary`` in which the values will be inserted after performing their process.

        First it will check the first value of tuple.
        If it is ``Faker`` then in will continue the process and will check the 4th value of tuple.
        If the 4th value(which is used to determine the number of fake data to be generated and store inside a list)
        is ``0`` then the method will store the values as it is in a list, because ``0`` value means we have to generate
        new fake data for every output data, so it will be done later.
        If it is greater than ``0`` then this method will create tuple with the given number of fake data and store it.
        (If no number is given then default number is 5.)

        If first value is not ``Faker`` then no process will be done.

        Finally the data will be inserted in the dictionary.

        :param dic:
        :param key:
        :param dictionary:
        :return:
        """
        ltuple = dic[key]
        if ltuple[0] == "Faker":
            fake = faker.Faker(ltuple[2])
            fake_lis = []
            if len(ltuple) == 4:
                if int(ltuple[3]) == 0:
                    dictionary[list(dic.keys()).index(key)] = list(ltuple)
                    return True
                else:
                    for x in range(int(ltuple[3])):
                        fake_lis.append(getattr(fake, ltuple[1])())
            else:
                for x in range(5):
                    fake_lis.append(getattr(fake, ltuple[1])())
            dictionary[list(dic.keys()).index(key)] = tuple(fake_lis)
            return True
        else:
            dictionary[list(dic.keys()).index(key)] = ltuple
            return True

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
        for raw_data in raw_json:
            if not list(raw_data.values())[0]:
                continue
            processed_data = {}
            for key in raw_data:
                keys = self.__data_generators(key)
                for ke in keys:
                    processed_data[ke] = self.__data_generators(raw_data[key])
                    if type(processed_data[ke]) == tuple and len(processed_data[ke])>0:
                        if type(processed_data[ke][0]) == dict:
                            if ke not in processed_data[ke][0]:
                                self.remove_header.append(ke)
            processed_datas.append(processed_data)
        return processed_datas

    def __data_generators(self, raw_data):
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
        raw_data, prefix, data_type = self.__raw_data_string_process(raw_data)
        if len(raw_data)<=1:
            return [""]
        if raw_data[0] == "[" and raw_data[-1] == "]" and prefix == "":
            processed_datas = self.__splitList(raw_data)
            processed_datas = data_type(processed_datas)

        elif prefix == "Faker":
                processed_datas = [data.strip() for data in raw_data[1:-1].split(",")]
                processed_datas.insert(0, "Faker")
                processed_datas = data_type(processed_datas)

        elif prefix == "Rrd":
            first_value = raw_data[1:-1].split(',')[0].strip()
            second_value = raw_data[1:-1].split(',')[1].strip()
            if second_value[0] == "[":
                second_value = ','.join(raw_data[1:-1].split(',')[1:]).strip()
                second_value = second_value[:second_value.index(']')+1]
                third_value = [x.strip() for x in ']'.join(raw_data[1:-1].split(']')[1:]).split(',')[1:]]
            else:
                third_value = [x.strip() for x in raw_data[1:-1].split(',')[2:]]
            evaluated_list = ']],'.join(','.join(third_value)[1:-1].strip().split('],')).split('],')
            if evaluated_list[0] == "":
                evaluated_dict = {}
            else:
                evaluated_dict = {
                    splited_data.split(':')[0]: self.__splitList(splited_data.split(':')[1])  for splited_data in evaluated_list
                }
            if second_value[0] == "[" and second_value[-1] == "]":
                second_value = self.__splitList(second_value)
            processed_datas = self.__processRrd(first_value, second_value,evaluated_dict)
            processed_datas = data_type(processed_datas)

        elif prefix == "Rre":
            file_name = raw_data[1:-1].split(',')[0].strip()
            sheet_dict, _ = self.__read_excel(file_name)
            first_value = raw_data[1:-1].split(',')[1].strip()
            second_value = raw_data[1:-1].split(',')[2].strip()
            if second_value[0] == "[":
                second_value = ','.join(raw_data[1:-1].split(',')[2:]).strip()
                second_value = second_value[:second_value.index(']')+1]
                third_value = [x.strip() for x in ']'.join(raw_data[1:-1].split(']')[1:]).split(',')[1:]]
            else:
                third_value = [x.strip() for x in raw_data[1:-1].split(',')[3:]]
            evaluated_list = ']],'.join(','.join(third_value)[1:-1].strip().split('],')).split('],')
            if evaluated_list[0] == "":
                evaluated_dict = {}
            else:
                evaluated_dict = {
                    splited_data.split(':')[0]: self.__splitList(splited_data.split(':')[1])  for splited_data in evaluated_list
                }
            if second_value[0] == "[" and second_value[-1] == "]":
                second_value = self.__splitList(second_value)
            processed_datas = self.__processRrd(first_value, second_value, evaluated_dict, sheet_dict)
            processed_datas = data_type(processed_datas)

        elif "-" in raw_data:
            raw_data = raw_data.split('-')
            start = raw_data[0].strip()
            end = raw_data[1].strip()
            step = 1
            if "," in end:
                raw_data = end.split(",")
                end = raw_data[0].strip()
                step = raw_data[1].strip()
            processed_datas = [x for x in range(int(start), int(end)+1, int(step))]
            processed_datas = data_type(processed_datas)

        else:
            processed_datas = [raw_data.strip()]
            processed_datas = data_type(processed_datas)
        return processed_datas

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
                if raw_string[:4].lower() == "rnd_":           # Random
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
                data_type = list
        else:
            data_type = list
        return raw_string, prefix, data_type

    @staticmethod
    def __read_excel(path, sheet_name=""):
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
        wb = xlrd.open_workbook(path)
        sheet_lis = wb.sheet_names()
        sheet_dict = {}
        for sheet in sheet_lis:
            xl_obj = xl2dict.XlToDict()
            data = xl_obj.fetch_data_by_column_by_sheet_name(path,sheet_name=sheet)
            sheet_dict[sheet] = data
        if sheet_name == "":
            base_sheet = sheet_dict[sheet_lis[0]]
        else:
            assert sheet_name in sheet_dict, f"Excel file doesn't contain {sheet_name} sheet. Please recheck."
            base_sheet = sheet_dict[sheet_name]
        return sheet_dict, base_sheet

    @staticmethod
    def __splitList(raw_data):
        """
        Will convert string list to python list.
        i.e. "[value1,value2,value3]" ==> ["value1","value2","value3"]
        :param raw_data: string of list
        :return: Python list
        """
        proccesed_datas = [data.strip() for data in raw_data[1:-1].split(",")]
        return proccesed_datas

    def __processRrd(self, sheet_name, data_looking_for, data_to_match: dict, sheet_dict=None, caller="RRD_"):
        """
        This function is internal function to process the data wil RRD_ prefix.
        The General input in excel file is like ``RRD_[sheetName,TargetData,[Header:[values**],Header:[values**]]]``
        So this program will take already have processed input i.e. strings converted as python string and list to
        python list, vice versa.

        ``sheet_name`` is the python string referring to TargetData containing string.

        ``data_looking_for`` is expected to be a string or list of TargetData. When there are multiple values then the
        previous process will send list else it will send string. When a string is received it will be automatically
        converted in list so the program will alwaus have to deal with list. If input is "*" then this method will take
        all value in the matched row as TargetData.

        ``data_to_match`` is a python dictionary created by the previous process. It will contain the key value pair
        same as given in input but just converted in python dict. Then all possible combinations will be generated inside
        this method. If an empty list is given by the user in the excel file then this list will get emptu dictionary from
        the previous process. Thus then this method will pick TargetData from all rows of the target sheet.

        :param sheet_name:
        :param data_looking_for:
        :param data_to_match:
        :return: dictionary of TargetData
        """
        sheet_dict = self.sheet_dict if sheet_dict is None else sheet_dict
        matching_data = [list(x) for x in itertools.product(*[data_to_match[key] for key in data_to_match])]
        assert sheet_name in sheet_dict, \
            f"Excel file doesn't contain {sheet_name} sheet. Please recheck. Called in '{caller}'"
        base_sheet = sheet_dict[sheet_name]
        data_lis = []
        if type(data_looking_for) == str:
            data_looking_for = data_looking_for.split(",")

        for data in base_sheet:
            if len(matching_data) == 1 and len(matching_data[0]) == 0:
                if data_looking_for[0] == "*":
                    data_lis.append(data)
                else:
                    data_lis.append({keys: data[keys] for keys in data_looking_for})
            else:
                if [data[key] for key in data_to_match] in matching_data:
                    if data_looking_for[0] == "*":
                        data_lis.append(data)
                    else:
                        data_lis.append({keys: data[keys] for keys in data_looking_for})
        return data_lis

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

if __name__ == "__main__":
    lTestDataGenerator = TestDataGenerator("../../tests/0TestInput/RawTestData.xlsx")
    lTestDataGenerator.write()
