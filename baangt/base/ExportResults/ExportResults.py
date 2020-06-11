import xlsxwriter
import logging
import json
import baangt.base.GlobalConstants as GC
from baangt.base.Timing.Timing import Timing
from baangt.base.Utils import utils
from pathlib import Path
from typing import Optional
from xlsxwriter.worksheet import (
    Worksheet, cell_number_tuple, cell_string_tuple)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from baangt.base.DataBaseORM import DATABASE_URL, TestrunLog, TestCaseSequenceLog
from baangt.base.DataBaseORM import TestCaseLog, TestCaseField, GlobalAttribute, TestCaseNetworkInfo
from datetime import datetime
from sqlite3 import IntegrityError
from baangt import plugin_manager
import re
import csv
from dateutil.parser import parse
from uuid import uuid4
from pathlib import Path
from baangt.base.ExportResults.SendStatistics import Statistics
from baangt.base.RuntimeStatistics import Statistic

logger = logging.getLogger("pyC")


class ExportResults:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.testList = []
        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.testCasesEndDateTimes_1D = kwargs.get('testCasesEndDateTimes_1D')
        self.testCasesEndDateTimes_2D = kwargs.get('testCasesEndDateTimes_2D')
        self.networkInfo = self._get_network_info(kwargs.get('networkInfo'))
        self.testRunName = self.testRunInstance.testRunName
        self.dataRecords = self.testRunInstance.dataRecords
        self.stage = self.__getStageFromDataRecordsOrGlobalSettings()
        self.statistics = Statistics()
        self.statistics.update_data(kwargs)
        self.statistics.update_runtimeStatistic()
        self.logfile = logger.handlers[1].baseFilename

        try:
            self.exportFormat = kwargs.get(GC.KWARGS_TESTRUNATTRIBUTES).get(GC.EXPORT_FORMAT)
            if isinstance(self.exportFormat, dict):
                self.exportFormat = self.exportFormat.get(GC.EXPORT_FORMAT)

            if not self.exportFormat:
                self.exportFormat = GC.EXP_XLSX
        except KeyError:
            self.exportFormat = GC.EXP_XLSX

        self.fileName = self.__getOutputFileName()
        logger.info("Export-Sheet for results: " + self.fileName)

        # export results to DB
        self.testcase_uuids = []
        self.exportToDataBase()

        if self.exportFormat == GC.EXP_XLSX:
            self.fieldListExport = kwargs.get(GC.KWARGS_TESTRUNATTRIBUTES).get(GC.EXPORT_FORMAT)["Fieldlist"]
            self.workbook = xlsxwriter.Workbook(self.fileName)
            self.summarySheet = self.workbook.add_worksheet("Summary")
            self.worksheet = self.workbook.add_worksheet("Output")
            self.jsonSheet = self.workbook.add_worksheet(f"{self.stage}_JSON")
            self.timingSheet = self.workbook.add_worksheet("Timing")
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
            self.exportJsonExcel()
            self.exportAdditionalData()
            self.exportTiming = ExportTiming(self.dataRecords,
                                             self.timingSheet)
            if self.networkInfo:
                self.networkSheet = self.workbook.add_worksheet("Network")
                self.exportNetWork = ExportNetWork(self.networkInfo,
                                                   self.testCasesEndDateTimes_1D,
                                                   self.testCasesEndDateTimes_2D,
                                                   self.workbook,
                                                   self.networkSheet)
            self.closeExcel()
        elif self.exportFormat == GC.EXP_CSV:
            self.export2CSV()
        if self.testRunInstance.globalSettings.get("DeactivateStatistics") == "True":
            logger.debug("Send Statistics to server is deactive")
        elif self.testRunInstance.globalSettings.get("DeactivateStatistics") is True:
            logger.debug("Send Statistics to server is deactive")
        else:
            try:
                self.statistics.send_statistics()
            except Exception as ex:
                logger.debug(ex)
        #self.exportToDataBase()

    def exportAdditionalData(self):
        # Runs only, when KWARGS-Parameter is set.
        if self.kwargs.get(GC.EXPORT_ADDITIONAL_DATA):
            addExportData = self.kwargs[GC.EXPORT_ADDITIONAL_DATA]
            # Loop over the items. KEY = Tabname, Value = Data to be exported.
            # For data KEY = Fieldname, Value = Cell-Value

            for key, value in addExportData.items():
                lExport = ExportAdditionalDataIntoTab(tabname=key, valueDict=value, outputExcelSheet=self.workbook)
                lExport.export()

    def __getStageFromDataRecordsOrGlobalSettings(self):
        """
        If "STAGE" is not provided in the data fields (should actually not happen, but who knows),
        we shall take it from GlobalSettings. If also not there, take the default Value GC.EXECUTIN_STAGE_TEST
        :return:
        """
        value = None
        for key, value in self.dataRecords.items():
            break
        if not value.get(GC.EXECUTION_STAGE):
            stage = self.testRunInstance.globalSettings.get('TC.Stage', GC.EXECUTION_STAGE_TEST)
        else:
            stage = value.get(GC.EXECUTION_STAGE)

        return stage
        

    def export2CSV(self):
        """
        Writes CSV-File of datarecords

        """
        f = open(self.fileName, 'w', encoding='utf-8-sig', newline='')
        writer = csv.DictWriter(f, self.dataRecords[0].keys())
        writer.writeheader()
        for i in range(0, len(self.dataRecords) - 1):
            writer.writerow(self.dataRecords[i])
        f.close()

    def exportToDataBase(self):
        #
        # writes results to DB
        #
        logger.info(f'Export results to database at: {DATABASE_URL}')
        engine = create_engine(DATABASE_URL)

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
        self.statistics.update_attribute_with_value("TestCasePassed", success)
        self.statistics.update_attribute_with_value("TestCaseFailed", error)
        self.statistics.update_attribute_with_value("TestCasePaused", waiting)
        self.statistics.update_attribute_with_value("TestCaseExecuted", success + error + waiting)
        # get documents
        datafiles = self.fileName

        # create testrun object
        tr_log = TestrunLog(
            id=self.testRunInstance.uuid.bytes,
            testrunName=self.testRunName,
            logfileName=self.logfile,
            startTime=datetime.strptime(start, "%d-%m-%Y %H:%M:%S"),
            endTime=datetime.strptime(end, "%d-%m-%Y %H:%M:%S"),
            statusOk=success,
            statusFailed=error,
            statusPaused=waiting,
            dataFile=self.fileName,
        )
        # add to DataBase
        session.add(tr_log)

        # set globals
        for key, value in self.testRunInstance.globalSettings.items():
            globalVar = GlobalAttribute(
                name=key,
                value=str(value),
                testrun=tr_log,
            )
            session.add(globalVar)

        self.__save_commit(session)

        # create testcase sequence instance
        tcs_log = TestCaseSequenceLog(testrun=tr_log)

        # create testcases
        for tc in self.dataRecords.values():
            # get uuid
            uuid = uuid4()
            # create TestCaseLog instances
            tc_log = TestCaseLog(
                id=uuid.bytes,
                testcase_sequence=tcs_log
            )
            # store uuid
            self.testcase_uuids.append(uuid)
            session.add(tc_log)
            # add TestCase fields
            for key, value in tc.items():
                field = TestCaseField(name=key, value=str(value), testcase=tc_log)
                session.add(field)

        self.__save_commit(session)

        # network info
        if self.networkInfo:
            for entry in self.networkInfo:
                if type(entry.get('testcase')) == type(1):
                    nw_info = TestCaseNetworkInfo(
                        testcase=tcs_log.testcases[entry.get('testcase')-1],
                        browserName=entry.get('browserName'),
                        status=entry.get('status'),
                        method=entry.get('method'),
                        url=entry.get('url'),
                        contentType=entry.get('contentType'),
                        contentSize=entry.get('contentSize'),
                        headers=str(entry.get('headers')),
                        params=str(entry.get('params')),
                        response=entry.get('response'),
                        startDateTime=datetime.strptime(entry.get('startDateTime')[:19], '%Y-%m-%dT%H:%M:%S'),
                        duration=entry.get('duration'),
                    )
                    session.add(nw_info)

        self.__save_commit(session)

    def __save_commit(self, session):
        try:
            session.commit()
        except IntegrityError as e:
            logger.critical(f"Integrity Error during commit to database: {e}")
        except Exception as e:
            logger.critical(f"Unknown error during database commit: {e}")

    def _get_test_case_num(self, start_date_time, browser_name):
        d_t = parse(start_date_time)
        d_t = d_t.replace(tzinfo=None)
        if self.testCasesEndDateTimes_1D:
            for index, dt_end in enumerate(self.testCasesEndDateTimes_1D):
                if d_t < dt_end:
                    return index + 1
        elif self.testCasesEndDateTimes_2D:
            browser_num = re.findall(r"\d+\.?\d*", str(browser_name))[-1] \
                if re.findall(r"\d+\.?\d*", str(browser_name)) else 0
            dt_list_index = int(browser_num) if int(browser_num) > 0 else 0
            for i, tcAndDtEnd in enumerate(self.testCasesEndDateTimes_2D[dt_list_index]):
                if d_t < tcAndDtEnd[1]:
                    return tcAndDtEnd[0] + 1
        return 'unknown'

    def _get_network_info(self, networkInfoDict):
        #
        # extracts network info data from the given dict 
        #
        if networkInfoDict:
            extractedNetworkInfo = []
            for info in networkInfoDict:
                #extractedEntry = {}
                for entry in info['log']['entries']:
                    # extract the current entry
                    extractedNetworkInfo.append({
                        'testcase': self._get_test_case_num(entry['startedDateTime'], entry['pageref']),
                        'browserName': entry.get('pageref'),
                        'status': entry['response'].get('status'),
                        'method': entry['request'].get('method'),
                        'url': entry['request'].get('url'),
                        'contentType': entry['response']['content'].get('mimeType'),
                        'contentSize': entry['response']['content'].get('size'),
                        'headers': entry['response']['headers'],
                        'params': entry['request']['queryString'],
                        'response': entry['response']['content'].get('text'),
                        'startDateTime': entry['startedDateTime'],
                        'duration': entry.get('time'),
                    })
            return extractedNetworkInfo

        return None


    def exportResultExcel(self, **kwargs):
        self._exportData()

    def exportJsonExcel(self):
        # headers
        headers = [
            'Stage',
            'UUID',
            'Attribute',
            'Value',
        ]
        # header style
        header_style = self.workbook.add_format()
        header_style.set_bold()
        # write header
        for index in range(len(headers)):
            self.jsonSheet.write(0, index, headers[index], header_style)
        # write data
        row = 0
        for index, testcase in self.dataRecords.items():
            # add TestCase fields
            for key, value in testcase.items():
                row += 1
                self.jsonSheet.write(row, 0, self.stage)
                self.jsonSheet.write(row, 1, str(self.testcase_uuids[index]))
                self.jsonSheet.write(row, 2, key)
                self.jsonSheet.write(row, 3, str(value))
        # Autowidth
        for n in range(len(headers)):
            ExcelSheetHelperFunctions.set_column_autowidth(self.jsonSheet, n)


    def makeSummaryExcel(self):

        self.summarySheet.write(0, 0, f"Testreport for {self.testRunName}", self.cellFormatBold)
        self.summarySheet.set_column(0, last_col=0, width=15)
        # get testrunname my
        self.testList.append(self.testRunName)
        # Testrecords
        self.__writeSummaryCell("Testrecords", len(self.dataRecords), row=2, format=self.cellFormatBold)
        value = len([x for x in self.dataRecords.values()
                     if x[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_SUCCESS])
        self.testList.append(value)  # Ok my
        if not value:
            value = ""
        self.__writeSummaryCell("Successful", value, format=self.cellFormatGreen)
        self.testList.append(value)  # paused my
        self.__writeSummaryCell("Paused", len([x for x in self.dataRecords.values()
                                               if x[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_WAITING]))
        value = len([x["Screenshots"] for x in self.dataRecords.values()
                     if x[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_ERROR])
        self.testList.append(value)  # error my
        if not value:
            value = ""
        self.__writeSummaryCell("Error", value, format=self.cellFormatRed)

        # Logfile
        self.__writeSummaryCell("Logfile", logger.handlers[1].baseFilename, row=7)
        # get logfilename for database my
        self.testList.append(logger.handlers[1].baseFilename)
        # database id
        self.__writeSummaryCell("Testrun UUID", str(self.testRunInstance.uuid), row=8)
        # Timing
        timing: Timing = self.testRunInstance.timing
        start, end, duration = timing.returnTimeSegment(GC.TIMING_TESTRUN)
        self.statistics.update_attribute_with_value("Duration", duration)
        self.statistics.update_attribute_with_value("TestRunUUID", str(self.testRunInstance.uuid))
        self.__writeSummaryCell("Starttime", start, row=10)
        # get start end during time my
        self.testList.append(start)
        self.testList.append(end)

        self.__writeSummaryCell("Endtime", end)
        self.__writeSummaryCell("Duration", duration, format=self.cellFormatBold)
        self.__writeSummaryCell("Avg. Dur", "")
        # Globals:
        self.__writeSummaryCell("Global settings for this testrun", "", format=self.cellFormatBold, row=15)
        for key, value in self.testRunInstance.globalSettings.items():
            self.__writeSummaryCell(key, str(value))
            # get global data my
            self.testList.append(str(value))
        # Testcase and Testsequence setting
        self.summaryRow += 1
        self.__writeSummaryCell("TestSequence settings follow:", "", format=self.cellFormatBold)
        lSequence = self.testRunInstance.testRunUtils.getSequenceByNumber(testRunName=self.testRunName, sequence="1")
        if lSequence:
            for key, value in lSequence[1].items():
                if isinstance(value, list) or isinstance(value, dict):
                    continue
                self.__writeSummaryCell(key, str(value))

    def __writeSummaryCell(self, lineHeader, lineText, row=None, format=None, image=False):
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
        l_file = Path(self.testRunInstance.managedPaths.getOrSetExportPath())

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
        # the 1st column is DB UUID
        self.worksheet.write(0, 0, 'UUID')
        # Add fields with name "RESULT_*" to output fields.
        i = 1
        self.__extendFieldList()
        for column in self.fieldListExport:
            self.worksheet.write(0, i, column)
            i += 1
        # add JSON field
        self.worksheet.write(0, len(self.fieldListExport)+1, "JSON")

    def __extendFieldList(self):
        """
        Fields, that start with "RESULT_" shall always be exported.

        Other fields, that shall always be exported are also added (Testcaseerrorlog, etc.)

        If global Parameter "TC.ExportAllFields" is set to True ALL fields will be exported

        @return:
        """

        if self.testRunInstance.globalSettings.get("TC.ExportAllFields", False):
            self.fieldListExport = []  # Make an empty list, so that we don't have duplicates
            for key in self.dataRecords[0].keys():
                self.fieldListExport.append(key)
            return

        try:
            for key in self.dataRecords[0].keys():
                if "RESULT_" in key.upper():
                    if not key in self.fieldListExport:
                        self.fieldListExport.append(key)

        except Exception as e:
            logger.critical(
                f'looks like we have no data in records: {self.dataRecords}, len of dataRecords: {len(self.dataRecords)}')

        # They are added here, because they'll not necessarily appear in the first record of the export data:
        if not GC.TESTCASEERRORLOG in self.fieldListExport:
            self.fieldListExport.append(GC.TESTCASEERRORLOG)
        if not GC.SCREENSHOTS in self.fieldListExport:
            self.fieldListExport.append(GC.SCREENSHOTS)
        if not GC.EXECUTION_STAGE in self.fieldListExport:
            self.fieldListExport.append(GC.EXECUTION_STAGE)

    def _exportData(self):
        for key, value in self.dataRecords.items():
            # write DB UUID
            try:
                self.worksheet.write(key + 1, 0, str(self.testcase_uuids[key]))
                # write RESULT fields
                for (n, column) in enumerate(self.fieldListExport):
                    self.__writeCell(key + 1, n + 1, value, column)
                # Also write everything as JSON-String into the last column
                self.worksheet.write(key + 1, len(self.fieldListExport) + 1, json.dumps(value))
            except IndexError as e:
                logger.error(f"List of testcase_uuids didn't have a value for {key}. That shouldn't happen!")
            except BaseException as e:
                logger.error(f"Error happened where it shouldn't. Error was {e}")

        # Create autofilter
        self.worksheet.autofilter(0, 0, len(self.dataRecords.items()), len(self.fieldListExport))

        # Make cells wide enough
        for n in range(0, len(self.fieldListExport)):
            ExcelSheetHelperFunctions.set_column_autowidth(self.worksheet, n)

    def __writeCell(self, line, cellNumber, testRecordDict, fieldName, strip=False):
        if fieldName in testRecordDict.keys() and testRecordDict[fieldName]:
            # Convert boolean for Output
            if isinstance(testRecordDict[fieldName], bool):
                testRecordDict[fieldName] = "True" if testRecordDict[fieldName] else "False"

            # Remove leading New-Line:
            if '\n' in testRecordDict[fieldName][0:5] or strip:
                testRecordDict[fieldName] = testRecordDict[fieldName].strip()
            # Do different stuff for Dicts and Lists:
            if isinstance(testRecordDict[fieldName], dict):
                self.worksheet.write(line, cellNumber, testRecordDict[fieldName])
            elif isinstance(testRecordDict[fieldName], list):
                if fieldName == GC.SCREENSHOTS:
                    self.__attachScreenshotsToExcelCells(cellNumber, fieldName, line, testRecordDict)
                else:
                    self.worksheet.write(line, cellNumber,
                                         utils.listToString(testRecordDict[fieldName]))
            else:
                if fieldName == GC.TESTCASESTATUS:
                    if testRecordDict[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_SUCCESS:
                        self.worksheet.write(line, cellNumber, testRecordDict[fieldName], self.cellFormatGreen)
                    elif testRecordDict[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_ERROR:
                        self.worksheet.write(line, cellNumber, testRecordDict[fieldName], self.cellFormatRed)
                elif fieldName == GC.SCREENSHOTS:
                    self.__attachScreenshotsToExcelCells(cellNumber, fieldName, line, testRecordDict)
                else:
                    self.worksheet.write(line, cellNumber, testRecordDict[fieldName])

    def __attachScreenshotsToExcelCells(self, cellNumber, fieldName, line, testRecordDict):
        # Place the screenshot images "on" the appropriate cell
        try:
            if type(testRecordDict[fieldName]) == list:

                if Path(testRecordDict[fieldName][-1]).is_file():
                    self.worksheet.insert_image(line, cellNumber, testRecordDict[fieldName][-1], {'x_scale': 0.05,
                                                                                                  'y_scale': 0.05})
                else:
                    logger.error(f"Sceenshot file {testRecordDict[fieldName][-1]} can't be found")

                for nextScreenshotNumber in range(len(testRecordDict[fieldName]) - 1):
                    if Path(testRecordDict[fieldName][nextScreenshotNumber]).is_file():
                        self.worksheet.insert_image(line, len(self.fieldListExport) + nextScreenshotNumber + 1,
                                                    testRecordDict[fieldName][nextScreenshotNumber],
                                                    {'x_scale': 0.05, 'y_scale': 0.05})
                    else:
                        logger.error(f"Screenshot file {testRecordDict[fieldName][nextScreenshotNumber]} can't be found")
            else:
                if Path(testRecordDict[fieldName]).is_file():
                    self.worksheet.insert_image(line, cellNumber, testRecordDict[fieldName], {'x_scale': 0.05,
                                                                                              'y_scale': 0.05})
                else:
                    logger.error(f"Screenshot file {testRecordDict[fieldName]} can't be found")

        except Exception as e:
            logger.error(f"Problem with screenshots - can't attach them {e}")

        self.worksheet.set_row(line, 35)

    def closeExcel(self):
        self.workbook.close()
        # Next line doesn't work on MAC. Returns "not authorized"
        # subprocess.Popen([self.filename], shell=True)


class ExportAdditionalDataIntoTab:
    def __init__(self, tabname, valueDict, outputExcelSheet: xlsxwriter.Workbook):
        self.tab = outputExcelSheet.add_worksheet(tabname)
        self.values = valueDict

    def export(self):
        self.makeHeader()
        self.writeLines()

    def makeHeader(self):
        for cellNumber, entries in self.values.items():
            for column, (key, value) in enumerate(entries.items()):
                self.tab.write(0, column, key)
            break  # Write header only for first line.

    def writeLines(self):
        currentLine = 1
        for line, values in self.values.items():
            for column, (key, value) in enumerate(values.items()):
                self.tab.write(currentLine, column, value)
            currentLine += 1


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
        #self.testCasesEndDateTimes_1D = testCasesEndDateTimes_1D
        #self.testCasesEndDateTimes_2D = testCasesEndDateTimes_2D
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
        column_style.set_align('right') if alignment == 'right' \
            else column_style.set_align('left') if alignment == 'left' else None
        column_style.set_border()
        return column_style

    def write_header(self, style=None):
        for index, value in enumerate(ExportNetWork.headers):
            self.sheet.write(0, index, value, style)

    def _get_test_case_num(self, start_date_time, browser_name):
        d_t = parse(start_date_time)
        d_t = d_t.replace(tzinfo=None)
        if self.testCasesEndDateTimes_1D:
            for index, dt_end in enumerate(self.testCasesEndDateTimes_1D):
                if d_t < dt_end:
                    return index + 1
        elif self.testCasesEndDateTimes_2D:
            browser_num = re.findall(r"\d+\.?\d*", str(browser_name))[-1] \
                if re.findall(r"\d+\.?\d*", str(browser_name)) else 0
            dt_list_index = int(browser_num) if int(browser_num) > 0 else 0
            for i, tcAndDtEnd in enumerate(self.testCasesEndDateTimes_2D[dt_list_index]):
                if d_t < tcAndDtEnd[1]:
                    return tcAndDtEnd[0] + 1
        return 'unknown'

    def write_content(self):
        if not self.networkInfo:
            return

        #partition_index = 0

        for index in range(len(self.networkInfo)):
            data_list = [
                self.networkInfo[index]['browserName'],
                self.networkInfo[index]['testcase'],
                self.networkInfo[index]['status'],
                self.networkInfo[index]['method'],
                self.networkInfo[index]['url'],
                self.networkInfo[index]['contentType'],
                self.networkInfo[index]['contentSize'],
                self.networkInfo[index]['headers'],
                self.networkInfo[index]['params'],
                self.networkInfo[index]['response'],
                self.networkInfo[index]['startDateTime'],
                self.networkInfo[index]['duration'],
            ]

            for i in range(len(data_list)):
                self.sheet.write(index + 1, i, str(data_list[i]) or 'null')


class ExportTiming:
    def __init__(self, testdataRecords: dict, sheet: xlsxwriter.worksheet):
        self.testdataRecords = testdataRecords
        self.sheet: xlsxwriter.worksheet = sheet

        self.sections = {}

        self.findAllTimingSections()
        self.writeHeader()
        self.writeLines()

        # Autowidth
        for n in range(0, len(self.sections) + 1):
            ExcelSheetHelperFunctions.set_column_autowidth(self.sheet, n)

    def writeHeader(self):
        self.wc(0, 0, "Testcase#")
        for index, key in enumerate(self.sections.keys(), start=1):
            self.wc(0, index, key)

    def writeLines(self):
        for tcNumber, (key, line) in enumerate(self.testdataRecords.items(), start=1):
            self.wc(tcNumber, 0, tcNumber)
            lSections = self.interpretTimeLog(line[GC.TIMELOG])
            for section, timingValue in lSections.items():
                # find, in which column this section should be written:
                for column, key in enumerate(self.sections.keys(), 1):
                    if key == section:
                        self.wc(tcNumber, column,
                                timingValue[GC.TIMING_DURATION])
                        continue

    @staticmethod
    def shortenTimingValue(timingValue):
        # TimingValue is seconds in Float. 2 decimals is enough:
        timingValue = int(float(timingValue) * 100)
        return timingValue / 100

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
            lTiming: dict = ExportTiming.interpretTimeLog(line[GC.TIMELOG])
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

        where the first part before ":" is the section, "since last call:" is the duration, TS: is the timestamp

        Update 29.3.2020: Format changed to "since last call: 00:xx:xx,", rest looks identical.
        """
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
                lSection = parts[0].replace(":", "").strip()
                lDuration = parts[1].split("since last call: ")[1]
                lExport[lSection] = {GC.TIMING_DURATION: lDuration}
        return lExport

