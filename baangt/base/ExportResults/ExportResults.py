import xlsxwriter
import logging
import json
import baangt.base.GlobalConstants as GC
from baangt.base.Timing.Timing import Timing
import sys
from baangt.base.Utils import utils
from pathlib import Path
from typing import Optional
from xlsxwriter.worksheet import (
    Worksheet, cell_number_tuple, cell_string_tuple)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from baangt.base.DataBaseORM import DATABASE_URL, TestrunLog
from datetime import datetime
import time
from baangt import plugin_manager
import re
import csv
from dateutil.parser import parse

logger = logging.getLogger("pyC")


class ExportResults:
    def __init__(self, **kwargs):
        self.testList = []
        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.networkInfo = kwargs.get('networkInfo')
        self.testCasesEndDateTimes_1D = kwargs.get('testCasesEndDateTimes_1D')

        logger.info('init ExportResults, testCasesEndDateTimes_2D: {}'.format(kwargs.get('testCasesEndDateTimes_2D')))
        self.testCasesEndDateTimes_2D = kwargs.get('testCasesEndDateTimes_2D')
        self.testRunName = self.testRunInstance.testRunName
        self.dataRecords = self.testRunInstance.dataRecords

        try:
            self.exportFormat = kwargs.get(GC.KWARGS_TESTRUNATTRIBUTES).get(GC.EXPORT_FORMAT)[GC.EXPORT_FORMAT]
        except KeyError:
            self.exportFormat = GC.EXP_XLSX

        self.fileName = self.__getOutputFileName()
        logger.info("Export-Sheet for results: " + self.fileName)

        if self.exportFormat == GC.EXP_XLSX:
            self.fieldListExport = kwargs.get(GC.KWARGS_TESTRUNATTRIBUTES).get(GC.EXPORT_FORMAT)["Fieldlist"]
            self.workbook = xlsxwriter.Workbook(self.fileName)
            self.summarySheet = self.workbook.add_worksheet("Summary")
            self.worksheet = self.workbook.add_worksheet("Output")
            self.timingSheet = self.workbook.add_worksheet("Timing")
            self.networkSheet = self.workbook.add_worksheet("Network")
            self.cellFormatGreen = self.workbook.add_format()
            self.cellFormatGreen.set_bg_color('green')
            self.cellFormatRed = self.workbook.add_format()
            self.cellFormatRed.set_bg_color('red')
            self.cellFormatBold = self.workbook.add_format()
            self.cellFormatBold.set_bold(bold=True)
            self.summaryRow = 0
            self.__setHeaderDetailSheetExcel()
            self.makeSummaryExcel()
            self.exportResultExcel()
            self.exportTiming = ExportTiming(self.dataRecords,
                                            self.timingSheet)
            self.exportNetWork = ExportNetWork(self.networkInfo,
                                               self.testCasesEndDateTimes_1D,
                                               self.testCasesEndDateTimes_2D,
                                               self.workbook,
                                               self.networkSheet)
            self.closeExcel()
        elif self.exportFormat == GC.EXP_CSV:
            self.export2CSV()
        self.exportToDataBase()

    def export2CSV(self):
        """
        Writes CSV-File of datarecords

        """
        f = open(self.fileName, 'w')
        writer = csv.DictWriter(f, self.dataRecords[0].keys())
        writer.writeheader()
        for i in range(0, len(self.dataRecords)-1):
            writer.writerow(self.dataRecords[i])
        f.close()

    def exportToDataBase(self):
        engine = create_engine(f'sqlite:///{DATABASE_URL}')

        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        # get timings
        timing: Timing = self.testRunInstance.timing
        start, end, duration = timing.returnTimeSegment(GC.TIMING_TESTRUN)

        # get status
        success = 0
        error = 0
        waiting = 0
        for value in self.dataRecords.values():
            if value[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_SUCCESS:
                success += 1
            elif value[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_ERROR:
                error += 1
            if value[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_WAITING:
                waiting += 1

        # get globals
        globalString = '{'
        for key, value in self.testRunInstance.globalSettings.items():
            if len(globalString) > 1:
                globalString += ', '
            globalString += f'{key}: {value}'
        globalString += '}'

        # get documents
        datafiles = self.fileName

        # create object
        log = TestrunLog(
            testrunName = self.testRunName,
            logfileName = logger.handlers[1].baseFilename,
            startTime = datetime.strptime(start, "%H:%M:%S"),
            endTime = datetime.strptime(end, "%H:%M:%S"),
            statusOk = success,
            statusFailed = error,
            statusPaused = waiting,
            globalVars = globalString,
            dataFile = datafiles,
        )
        # write to DataBase
        session.add(log)
        session.commit()

    def exportResultExcel(self, **kwargs):
        self._exportData()

    def makeSummaryExcel(self):

        self.summarySheet.write(0,0, f"Testreport for {self.testRunName}", self.cellFormatBold)
        self.summarySheet.set_column(0, last_col=0, width=15)
        # get testrunname my
        self.testList.append(self.testRunName)
        # Testrecords
        self.__writeSummaryCell("Testrecords", len(self.dataRecords), row=2, format=self.cellFormatBold)
        value = len([x for x in self.dataRecords.values()
                                                   if x[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_SUCCESS])
        self.testList.append(value) # Ok my
        if not value:
            value = ""
        self.__writeSummaryCell("Successful", value, format=self.cellFormatGreen)
        self.testList.append(value)  # paused my
        self.__writeSummaryCell("Paused", len([x for x in self.dataRecords.values()
                                                   if x[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_WAITING]))
        value = len([x for x in self.dataRecords.values()
                                               if x[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_ERROR])
        self.testList.append(value)  # error my
        if not value:
            value = ""
        self.__writeSummaryCell("Error", value, format=self.cellFormatRed)

        # Logfile
        self.__writeSummaryCell("Logfile", logger.handlers[1].baseFilename, row=7)
        # get logfilename for database my
        self.testList.append(logger.handlers[1].baseFilename)
        # Timing
        timing:Timing = self.testRunInstance.timing
        start, end, duration = timing.returnTimeSegment(GC.TIMING_TESTRUN)
        self.__writeSummaryCell("Starttime", start, row=9)
        # get start end during time my
        self.testList.append(start)
        self.testList.append(end)

        self.__writeSummaryCell("Endtime", end)
        self.__writeSummaryCell("Duration", duration, format=self.cellFormatBold )
        self.__writeSummaryCell("Avg. Dur", "")
        # Globals:
        self.__writeSummaryCell("Global settings for this testrun", "", format=self.cellFormatBold, row=14)
        for key, value in self.testRunInstance.globalSettings.items():
            self.__writeSummaryCell(key, str(value))
            # get global data my
            self.testList.append(str(value))
        # Testcase and Testsequence setting
        self.__writeSummaryCell("TestSequence settings follow:", "", row=16+len(self.testRunInstance.globalSettings),
                                format=self.cellFormatBold)
        lSequence = self.testRunInstance.testRunUtils.getSequenceByNumber(testRunName=self.testRunName, sequence="1")
        if lSequence:
            for key, value in lSequence[1].items():
                if isinstance(value, list) or isinstance(value, dict):
                    continue
                self.__writeSummaryCell(key, str(value))

    def __writeSummaryCell(self, lineHeader, lineText, row=None, format=None):
        if not row:
            self.summaryRow += 1
        else:
            self.summaryRow = row

        if not lineText:
            # If we have no lineText we want to apply format to the Header
            self.summarySheet.write(self.summaryRow, 0, lineHeader, format)
        else:
            self.summarySheet.write(self.summaryRow, 0, lineHeader)
            self.summarySheet.write(self.summaryRow, 1, lineText, format)

    def __getOutputFileName(self):
        if self.testRunInstance.globalSettings[GC.PATH_ROOT]:
            basePath = Path(self.testRunInstance.globalSettings[GC.PATH_ROOT])
        elif "/" not in self.testRunInstance.globalSettings[GC.DATABASE_EXPORTFILENAMEANDPATH][0:1]:
            basePath = Path(sys.modules['__main__'].__file__).parent
        else:
            basePath = ""
        l_file: Path = Path(basePath).joinpath(self.testRunInstance.globalSettings[GC.DATABASE_EXPORTFILENAMEANDPATH])
        if "~" in str(l_file.absolute()):
            l_file = l_file.expanduser()
        if not Path(l_file).is_dir():
            logger.info(f"Create directory {l_file}")
            Path(l_file).mkdir(parents=True, exist_ok=True)

        if self.exportFormat == GC.EXP_XLSX:
            lExtension = '.xlsx'
        elif self.exportFormat == GC.EXP_CSV:
            lExtension = '.csv'
        else:
            logger.critical(f"wrong export file format: {self.exportFormat}, using 'xlsx' instead")
            lExtension = '.xlsx'

        l_file = l_file.joinpath("baangt_" + self.testRunName + "_" + utils.datetime_return() + lExtension)
        logger.debug(f"Filename for export: {str(l_file)}")
        return str(l_file)

    def __setHeaderDetailSheetExcel(self):
        i = 0
        self.__extendFieldList()  # Add fields with name "RESULT_*" to output fields.
        for column in self.fieldListExport:
            self.worksheet.write(0, i, column)
            i += 1
        self.worksheet.write(0, len(self.fieldListExport), "JSON")

    def __extendFieldList(self):
        """
        Fields, that start with "RESULT_" shall always be exported.

        @return:
        """
        for key in self.dataRecords[0].keys():
            if "RESULT_" in key:
                if not key in self.fieldListExport:
                    self.fieldListExport.append(key)

    def _exportData(self):
        for key, value in self.dataRecords.items():
            for (n, column) in enumerate(self.fieldListExport):
                self.__writeCell(key+1, n, value, column)
            # Also write everything as JSON-String into the last column
            self.worksheet.write(key+1, len(self.fieldListExport), json.dumps(value))

        # Create autofilter
        self.worksheet.autofilter(0,0,len(self.dataRecords.items()),len(self.fieldListExport)-1)

        # Make cells wide enough
        for n in range(0,len(self.fieldListExport)):
            ExcelSheetHelperFunctions.set_column_autowidth(self.worksheet, n)

    def __writeCell(self, line, cellNumber, testRecordDict, fieldName, strip=False):
        if fieldName in testRecordDict.keys() and testRecordDict[fieldName]:
            if '\n' in testRecordDict[fieldName][0:5] or strip:
                testRecordDict[fieldName] = testRecordDict[fieldName].strip()
            if isinstance(testRecordDict[fieldName], dict) or isinstance(testRecordDict[fieldName], list):
                self.worksheet.write(line, cellNumber, testRecordDict[fieldName].strip())
            else:
                if fieldName == GC.TESTCASESTATUS:
                    if testRecordDict[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_SUCCESS:
                        self.worksheet.write(line, cellNumber, testRecordDict[fieldName], self.cellFormatGreen)
                    elif testRecordDict[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_ERROR:
                        self.worksheet.write(line, cellNumber, testRecordDict[fieldName], self.cellFormatRed)
                else:
                    self.worksheet.write(line, cellNumber, testRecordDict[fieldName])

    def closeExcel(self):
        self.workbook.close()
        # Next line doesn't work on MAC. Returns "not authorized"
        # subprocess.Popen([self.filename], shell=True)


class ExcelSheetHelperFunctions:
    def __init__(self):
        pass

    @staticmethod
    def set_column_autowidth(worksheet: Worksheet, column: int):
        """
        Set the width automatically on a column in the `Worksheet`.
        !!! Make sure you run this function AFTER having all cells filled in
        the worksheet!
        """
        maxwidth = ExcelSheetHelperFunctions.get_column_width(worksheet=worksheet, column=column)
        if maxwidth is None:
            return
        elif maxwidth > 45:
            maxwidth = 45
        worksheet.set_column(first_col=column, last_col=column, width=maxwidth)

    @staticmethod
    def get_column_width(worksheet: Worksheet, column: int) -> Optional[int]:
        """Get the max column width in a `Worksheet` column."""
        strings = getattr(worksheet, '_ts_all_strings', None)
        if strings is None:
            strings = worksheet._ts_all_strings = sorted(
                worksheet.str_table.string_table,
                key=worksheet.str_table.string_table.__getitem__)
        lengths = set()
        for row_id, colums_dict in worksheet.table.items():  # type: int, dict
            data = colums_dict.get(column)
            if not data:
                continue
            if type(data) is cell_string_tuple:
                iter_length = len(strings[data.string])
                if not iter_length:
                    continue
                lengths.add(iter_length)
                continue
            if type(data) is cell_number_tuple:
                iter_length = len(str(data.number))
                if not iter_length:
                    continue
                lengths.add(iter_length)
        if not lengths:
            return None
        return max(lengths)


class ExportNetWork:

    headers = ['BrowserName', 'TestCaseNum', 'Status', 'Method', 'URL', 'ContentType', 'ContentSize', 'Headers',
               'Params', 'Response', 'startDateTime', 'Duration/ms']

    def __init__(self, networkInfo: dict, testCasesEndDateTimes_1D: list,
                 testCasesEndDateTimes_2D: list, workbook: xlsxwriter.Workbook, sheet: xlsxwriter.worksheet):

        self.networkInfo = networkInfo
        self.testCasesEndDateTimes_1D = testCasesEndDateTimes_1D
        logger.info('init ExportNetWork, testCasesEndDateTimes_2D: {}'.format(testCasesEndDateTimes_2D))
        self.testCasesEndDateTimes_2D = testCasesEndDateTimes_2D
        self.workbook = workbook
        self.sheet = sheet
        header_style = self.get_header_style()
        self.write_header(style=header_style)
        self.set_column_align()
        self.write_content()
        self.set_column_width()

    def set_column_align(self):
        right_align_indexes = list()
        right_align_indexes.append(ExportNetWork.headers.index('ContentSize'))
        right_align_indexes.append(ExportNetWork.headers.index('Duration/ms'))
        right_align_style = self.get_column_style(alignment='right')
        left_align_style = self.get_column_style(alignment='left')
        [self.sheet.set_column(i, i, cell_format=right_align_style) if i in right_align_indexes else
         self.sheet.set_column(i, i, cell_format=left_align_style) for i in range(len(ExportNetWork.headers))]

    def set_column_width(self):
        [ExcelSheetHelperFunctions.set_column_autowidth(self.sheet, i) for i in range(len(ExportNetWork.headers))]

    def get_header_style(self):
        header_style = self.workbook.add_format()
        header_style.set_bg_color("#00CCFF")
        header_style.set_color("#FFFFFF")
        header_style.set_bold()
        header_style.set_border()
        return header_style

    def get_column_style(self, alignment=None):
        column_style = self.workbook.add_format()
        column_style.set_color("black")
        column_style.set_align('right') if alignment == 'right'\
            else column_style.set_align('left') if alignment == 'left' else None
        column_style.set_border()
        return column_style

    def write_header(self, style=None):
        for index, value in enumerate(ExportNetWork.headers):
            self.sheet.write(0, index, value, style)

    def _get_test_case_num(self, start_date_time, browser_name):
        d_t = parse(start_date_time)
        d_t = d_t.replace(tzinfo=None)
        logger.info('get in to _get_test_case_num, testCasesEndDateTimes_1D: {}, testCasesEndDateTimes_2D: {}'
              .format(self.testCasesEndDateTimes_1D, self.testCasesEndDateTimes_2D))
        if self.testCasesEndDateTimes_1D:
            for index, dt_end in enumerate(self.testCasesEndDateTimes_1D):
                if d_t < dt_end:
                    return index
        elif self.testCasesEndDateTimes_2D:
            browser_num = re.findall(r"\d+\.?\d*", str(browser_name))[-1] \
                if re.findall(r"\d+\.?\d*", str(browser_name)) else 0
            logger.info('get browser_num: {}'.format(browser_num))
            dt_list_index = int(browser_num) if int(browser_num) > 0 else 0
            logger.info('get dt_list_index: {}'.format(dt_list_index))
            for i, tcAndDtEnd in enumerate(self.testCasesEndDateTimes_2D[dt_list_index]):
                logger.info('i: {}, tc: {}, dt_end: {}'.format(i, tcAndDtEnd[0], tcAndDtEnd[1]))
                if d_t < tcAndDtEnd[1]:
                    logger.info('get into d_t < dt_end')
                    return tcAndDtEnd[0]
        return 'unknown'

    def write_content(self):
        if not self.networkInfo:
            return

        logger.info(f'networkInfo length: {len(self.networkInfo)}')

        partition_index = 0

        for info in self.networkInfo:
            for index, entry in enumerate(info['log']['entries']):
                browser_name = entry['pageref']
                status = entry['response']['status']
                method = entry['request']['method']
                url = entry['request']['url']
                content_type = entry['response']['content']['mimeType']
                content_size = entry['response']['content']['size']
                headers = entry['response']['headers']
                params = entry['request']['queryString']
                response = entry['response']['content']['text'] if 'text' in entry['response']['content'] else ''
                start_date_time = entry['startedDateTime']
                duration = entry['time']
                test_case_num = self._get_test_case_num(start_date_time, browser_name)

                data_list = [browser_name, test_case_num, status, method, url, content_type, content_size,
                             headers, params, response, start_date_time, duration]

                [self.sheet.write(index + partition_index + 1, i, str(data_list[i]) or 'null')
                 for i in range(len(data_list))]

            partition_index += len(info['log']['entries'])



class ExportTiming:
    def __init__(self, testdataRecords:dict, sheet:xlsxwriter.worksheet):
        self.testdataRecords = testdataRecords
        self.sheet:xlsxwriter.worksheet = sheet

        self.sections = {}

        self.findAllTimingSections()
        self.writeHeader()
        self.writeLines()

        # Autowidth
        for n in range(0,len(self.sections)+1):
            ExcelSheetHelperFunctions.set_column_autowidth(self.sheet, n)

    def writeHeader(self):
        self.wc(0,0,"Testcase#")
        for index, key in enumerate(self.sections.keys(), start=1):
            self.wc(0, index, key)

    def writeLines(self):
        for tcNumber, (key, line) in enumerate(self.testdataRecords.items(),start=1):
            self.wc(tcNumber, 0, tcNumber)
            lSections = self.interpretTimeLog(line[GC.TIMELOG])
            for section, timingValue in lSections.items():
                # find, in which column this section should be written:
                for column, key in enumerate(self.sections.keys(),1):
                    if key == section:
                        self.wc(tcNumber, column,
                                ExportTiming.shortenTimingValue(timingValue[GC.TIMING_DURATION]))
                        continue

    @staticmethod
    def shortenTimingValue(timingValue):
        # TimingValue is seconds in Float. 2 decimals is enough:
        timingValue = int(float(timingValue) * 100)
        return timingValue/100

    def writeCell(self, row, col, content, format=None):
        self.sheet.write(row, col, content, format)

    wc = writeCell

    def findAllTimingSections(self):
        """
        We try to have an ordered list of Timing Sequences. As each Testcase might have different sections we'll have
        to make guesses

        @return:
        """
        lSections = {}
        for key, line in self.testdataRecords.items():
            lTiming:dict = ExportTiming.interpretTimeLog(line[GC.TIMELOG])
            for key in lTiming.keys():
                if lSections.get(key):
                    continue
                else:
                    lSections[key] = None

        self.sections = lSections

    @staticmethod
    def interpretTimeLog(lTimeLog):
        """Example Time Log:
        Complete Testrun: Start: 1579553837.241974 - no end recorded
        TestCaseSequenceMaster: Start: 1579553837.243414 - no end recorded
        CustTestCaseMaster: Start: 1579553838.97329 - no end recorded
        Browser Start: , since last call: 2.3161418437957764
        Empfehlungen: , since last call: 6.440968036651611, ZIDs:[175aeac023237a73], TS:2020-01-20 21:57:46.525577
        Annahme_RABAZ: , since last call: 2.002716064453125e-05, ZIDs:[6be7d0a44e59acf6], TS:2020-01-20 21:58:37.203583
        Antrag drucken: , since last call: 9.075241088867188, ZIDs:[6be7d0a44e59acf6, b27c3875ddcbb4fa], TS:2020-01-20 21:58:38.040137
        Warten auf Senden an Bestand Button: , since last call: 1.3927149772644043
        Senden an Bestand: , since last call: 9.60469913482666, ZIDs:[66b12fa4869cf8a0, ad1f3d47c4694e26], TS:2020-01-20 21:58:49.472288

        where the first part before ":" is the section, "since last call:" is the duration, TS: is the timestamp"""
        lExport = {}
        lLines = lTimeLog.split("\n")
        for line in lLines:
            parts = line.split(",")
            if len(parts) < 2:
                continue
            if "Start:" in line:
                # Format <sequence>: <Start>: <time.loctime>
                continue
            else:
                lSection = parts[0].replace(":","").strip()
                lDuration = parts[1].split(":")[1]
                lExport[lSection] = {GC.TIMING_DURATION: lDuration}
        return lExport

