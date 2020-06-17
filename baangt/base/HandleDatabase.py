import logging
from xlrd import open_workbook
import itertools
import json
import baangt.base.CustGlobalConstants as CGC
import baangt.base.GlobalConstants as GC
from baangt.base.Utils import utils
import baangt.TestSteps.Exceptions
from pathlib import Path
import xl2dict
import re
from random import randint

logger = logging.getLogger("pyC")


class HandleDatabase:
    def __init__(self, linesToRead, globalSettings=None):
        self.lineNumber = 3
        # FIXME: This is still not clean. GlobalSettings shouldn't be predefined in CustomConstants-Class
        self.globals = {
            CGC.CUST_TOASTS: "",
            GC.EXECUTION_STAGE: "",
            GC.TESTCASEERRORLOG: "",
            CGC.VIGOGFNUMMER: "",
            CGC.SAPPOLNR: "",
            CGC.PRAEMIE: "",
            CGC.POLNRHOST: "",
            GC.TESTCASESTATUS: "",
            GC.TIMING_DURATION: "",
            GC.SCREENSHOTS: "",
            GC.TIMELOG: "",
        }
        if globalSettings:
            for setting, value in globalSettings.items():
                self.globals[setting] = value
        self.range = self.__buildRangeOfRecords(linesToRead)
        self.rangeDict = {}
        self.__buildRangeDict()
        self.df_json = None
        self.dataDict = []
        self.recordPointer = 0
        self.sheet_dict = {}

    def __buildRangeDict(self):
        """
        Interprets the Range and creates a DICT of values, that we can loop over later

        @return: Creates empty self.rangeDict
        """
        for lRangeLine in self.range:
            for x in range(lRangeLine[0], lRangeLine[1]+1):
                self.rangeDict[x] = ""

    def __buildRangeOfRecords(self, rangeFromConfigFile):
        lRange = []
        if not rangeFromConfigFile:
            # No selection - means all records
            return [[0,99999]]
        else:
            # Format: 4;6-99;17-200;203 or
            # Format: 4,6-100,800-1000
            if ";" in rangeFromConfigFile:
                for kombination in rangeFromConfigFile.split(";"):
                    lRange.append(HandleDatabase.__buildRangeOfRecordsOneEntry(kombination))
            elif "," in rangeFromConfigFile:
                for kombination in rangeFromConfigFile.split(","):
                    lRange.append(HandleDatabase.__buildRangeOfRecordsOneEntry(kombination))
            else:
                lRange.append(HandleDatabase.__buildRangeOfRecordsOneEntry(rangeFromConfigFile))

        # Make sure these are numbers:
        for lRangeLine in lRange:
            lRangeLine[0] = HandleDatabase.__sanitizeNumbers(lRangeLine[0])
            lRangeLine[1] = HandleDatabase.__sanitizeNumbers(lRangeLine[1])

        return lRange

    @staticmethod
    def __sanitizeNumbers(numberIn):
        if isinstance(numberIn, dict):
            numberIn = numberIn['default']
            try:
                  return int(numberIn.strip())
            except:
                  return 0
        numberIn = numberIn.strip()
        return int(numberIn)

    @staticmethod
    def __buildRangeOfRecordsOneEntry(rangeIn):
        if "-" in rangeIn:
            # This is a range (17-22)
            return HandleDatabase.__buildRangeOfRecordsSingleRange(rangeIn)
        else:
            # This is a single entry:
            return [rangeIn, rangeIn]

    @staticmethod
    def __buildRangeOfRecordsSingleRange(rangeIn):
        lSplit = rangeIn.split("-")
        return [lSplit[0], lSplit[1]]

    def read_excel(self, fileName, sheetName):
        fileName = utils.findFileAndPathFromPath(fileName)
        if not fileName:
            logger.critical(f"Can't open file: {fileName}")
            return

        book = open_workbook(fileName)
        sheet = book.sheet_by_name(sheetName)

        # read header values into the list
        keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

        for row_index in range(1, sheet.nrows):
            temp_dic = {}
            for col_index in range(sheet.ncols):
                temp_dic[keys[col_index]] = sheet.cell(row_index, col_index).value
                if type(temp_dic[keys[col_index]])==float:
                    temp_dic[keys[col_index]] = repr(temp_dic[keys[col_index]])
                    if temp_dic[keys[col_index]][-2:]==".0":
                        temp_dic[keys[col_index]] = temp_dic[keys[col_index]][:-2]

            self.dataDict.append(temp_dic)

        for temp_dic in self.dataDict:
            new_data_dic ={}
            for keys in temp_dic:
                if '$(' in str(temp_dic[keys]):
                    while '$(' in str(temp_dic[keys]):
                        start_index = temp_dic[keys].index('$(')
                        end_index = temp_dic[keys][start_index:].index(')')+start_index
                        data_to_replace_with = temp_dic[temp_dic[keys][start_index+2:end_index]]
                        temp_dic[keys] = temp_dic[keys].replace(
                            temp_dic[keys][start_index:end_index+1], data_to_replace_with
                        )
                    if temp_dic[keys][:4] == "RRD_":
                        rrd_string = self.__process_rrd_string(temp_dic[keys])
                        rrd_data = self.__rrd_string_to_python(rrd_string[4:], fileName)
                        for data in rrd_data:
                            new_data_dic[data] = rrd_data[data]
                    if temp_dic[keys][:4] == "RRE_":
                        rrd_string = self.__process_rre_string(temp_dic[keys])
                        rrd_data = self.__rre_string_to_python(rrd_string[4:])
                        for data in rrd_data:
                            new_data_dic[data] = rrd_data[data]
            for key in new_data_dic:
                temp_dic[key] = new_data_dic[key]

    def __compareEqualStageInGlobalsAndDataRecord(self, currentNewRecordDict:dict) -> bool:
        """
        As method name says, compares, whether Stage in Global-settings is equal to stage in Data Record,
        so that this record might be excluded, if it's for the wrong Stage.

        :param currentNewRecordDict: The current Record
        :return: Boolean
        """
        lAppend = True
        if self.globals.get(GC.EXECUTION_STAGE):
            if currentNewRecordDict.get(GC.EXECUTION_STAGE):
                if currentNewRecordDict[GC.EXECUTION_STAGE] != self.globals[GC.EXECUTION_STAGE]:
                    lAppend = False
        return lAppend

    def __processRrd(self, sheet_name, data_looking_for, data_to_match: dict, sheet_dict=None, caller="RRD_"):
        """
        For more detail please refer to TestDataGenerator.py
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

    def __rrd_string_to_python(self, raw_data, fileName):
        """
        Convert string to python data types
        :param raw_data:
        :return:
        """
        first_value = raw_data[1:-1].split(',')[0].strip()
        second_value = raw_data[1:-1].split(',')[1].strip()
        if second_value[0] == "[":
            second_value = ','.join(raw_data[1:-1].split(',')[1:]).strip()
            second_value = second_value[:second_value.index(']') + 1]
            third_value = [x.strip() for x in ']'.join(raw_data[1:-1].split(']')[1:]).split(',')[1:]]
        else:
            third_value = [x.strip() for x in raw_data[1:-1].split(',')[2:]]
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
        if first_value not in self.sheet_dict:
            self.sheet_dict, _ = self.__read_excel(path=fileName)
        processed_datas = self.__processRrd(first_value, second_value, evaluated_dict)
        assert len(processed_datas)>0, f"No matching data for RRD_. Please check the input file. Was searching for " \
                                       f"{first_value}, {second_value} and {str(evaluated_dict)} " \
                                       f"but didn't find anything"
        return processed_datas[randint(0, len(processed_datas)-1)]

    def __rre_string_to_python(self, raw_data):
        """
        Convert string to python data types
        :param raw_data:
        :return:
        """
        file_name = raw_data[1:-1].split(',')[0].strip()
        sheet_dict, _ = self.__read_excel(file_name)
        first_value = raw_data[1:-1].split(',')[1].strip()
        second_value = raw_data[1:-1].split(',')[2].strip()
        if second_value[0] == "[":
            second_value = ','.join(raw_data[1:-1].split(',')[2:]).strip()
            second_value = second_value[:second_value.index(']') + 1]
            third_value = [x.strip() for x in ']'.join(raw_data[1:-1].split(']')[1:]).split(',')[1:]]
        else:
            third_value = [x.strip() for x in raw_data[1:-1].split(',')[3:]]
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
        processed_datas = self.__processRrd(first_value, second_value, evaluated_dict, sheet_dict, caller="RRE_")
        assert len(processed_datas)>0, f"No matching data for RRD_. Please check the input file. Was searching for " \
                                       f"{first_value}, {second_value} and {str(evaluated_dict)} " \
                                       f"but didn't find anything"
        return processed_datas[randint(0, len(processed_datas)-1)]

    def __process_rre_string(self, rre_string):
        """
        For more detail please refer to TestDataGenerator.py
        :param rre_string:
        :return:
        """
        processed_string = ','.join([word.strip() for word in rre_string.split(', ')])
        match = re.match(
            r"(RRE_(\(|\[))[\w\d\s\-./\\]+\.(xlsx|xls),[a-zA-z0-9\s]+,(\[?[a-zA-z\s,]+\]?|)|\*,\[([a-zA-z0-9\s]+:\[[a-zA-z0-9,\s]+\](,?))*\]",
            processed_string)
        err_string = f"{rre_string} not matching pattern RRE_(fileName, sheetName, TargetData," \
                     f"[Header1:[Value1],Header2:[Value1,Value2]])"
        assert match, err_string
        return processed_string

    def __process_rrd_string(self, rrd_string):
        """
        For more detail please refer to TestDataGenerator.py
        :param rrd_string:
        :return:
        """
        processed_string = ','.join([word.strip() for word in rrd_string.split(', ')])
        match = re.match(
            r"(RRD_(\(|\[))[a-zA-z0-9\s]+,(\[?[a-zA-z\s,]+\]?|)|\*,\[([a-zA-z0-9\s]+:\[[a-zA-z0-9,\s]+\](,?))*\]",
            processed_string
        )
        err_string = f"{rrd_string} not matching pattern RRD_(sheetName,TargetData," \
                     f"[Header1:[Value1],Header2:[Value1,Value2]])"
        assert match, err_string
        return processed_string

    def __splitList(self, raw_data):
        """
        Will convert string list to python list.
        i.e. "[value1,value2,value3]" ==> ["value1","value2","value3"]
        :param raw_data: string of list
        :return: Python list
        """
        proccesed_datas = [data.strip() for data in raw_data[1:-1].split(",")]
        return proccesed_datas

    def __read_excel(self, path, sheet_name=""):
        """
        For more detail please refer to TestDataGenerator.py
        :param path: Path to raw data xlsx file.
        :param sheet_name: Name of base sheet sheet where main input data is located. Default will be the first sheet.
        :return: Dictionary of all sheets and data, Dictionary of base sheet.
        """
        wb = open_workbook(path)
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

    def readNextRecord(self):
        """
        We built self.range during init. Now we need to iterate over the range(s) in range,
        find appropriate record and return that - one at a time

        @return:
        """
        if len(self.rangeDict) == 0:
            # All records were processed
            return None
        try:
            # the topmost record of the RangeDict (RangeDict was built by the range(s) from the TestRun
            # - 1 because there's a header line in the Excel-Sheet.
            lRecord = self.dataDict[(list(self.rangeDict.keys())[0])]
            while not self.__compareEqualStageInGlobalsAndDataRecord(lRecord):
                logger.debug(f"Skipped record {str(lRecord)[:30]} due to wrong stage: {lRecord[GC.EXECUTION_STAGE]} vs. "
                             f"{self.globals[GC.EXECUTION_STAGE]}")
                self.rangeDict.pop(list(self.rangeDict.keys())[0])
                lRecord = self.dataDict[(list(self.rangeDict.keys())[0])]
        except Exception as e:
            logger.debug(f"Couldn't read record from database: {list(self.rangeDict.keys())[0]}")
            self.rangeDict.pop(list(self.rangeDict.keys())[0])
            return None

        # Remove the topmost entry from the rangeDict, so that next time we read the next entry in the lines above
        self.rangeDict.pop(list(self.rangeDict.keys())[0])
        return self.updateGlobals(lRecord)

    def readTestRecord(self, lineNumber=None):
        if lineNumber:
            self.lineNumber = lineNumber -1  # Base 0 vs. Base 1
        else:
            self.lineNumber += 1 # add 1 to read next line number

        try:
            record = self.dataDict[self.lineNumber]
            logger.info(f"Starting with Testrecord {self.lineNumber}, Details: " +
                        str({k: record[k] for k in list(record)[0:5]}))
            return self.updateGlobals(record)
        except Exception as e:
            logger.critical(f"Couldn't read record# {self.lineNumber}")

    def updateGlobals(self, record):

        self.globals[CGC.CUST_TOASTS] = ""
        self.globals[GC.TESTCASEERRORLOG] = ""
        self.globals[GC.TIMING_DURATION] = ""
        self.globals[GC.TIMELOG] = ""
        self.globals[GC.TESTCASESTATUS] = ""
        self.globals[GC.SCREENSHOTS] = ""

        record.update(self.globals)
        return record
