import xlsxwriter
import logging
import json
import baangt.base.GlobalConstants as GC
from baangt.base.Timing import Timing
import subprocess
import sys
import os
import sqlite3
from sqlite3 import Error
from baangt.base.utils import utils
from pathlib import Path
from typing import Optional
from xlsxwriter.worksheet import (
    Worksheet, cell_number_tuple, cell_string_tuple)

logger = logging.getLogger("pyC")

class ExportResults:
    def __init__(self, **kwargs):
        self.testList = []
        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.testRunName = self.testRunInstance.testRunName
        self.filename = self.__getOutputFileName()
        logger.info("Export-Sheet for results: " + self.filename)
        self.workbook = xlsxwriter.Workbook(self.filename)
        self.summarySheet = self.workbook.add_worksheet("Summary")
        self.worksheet = self.workbook.add_worksheet("Output")
        self.timingsheet = self.workbook.add_worksheet("Timing")
        self.dataRecords = self.testRunInstance.dataRecords
        self.fieldListExport = kwargs.get(GC.KWARGS_TESTRUNATTRIBUTES).get(GC.EXPORT_FORMAT)["Fieldlist"]
        self.cellFormatGreen = self.workbook.add_format()
        self.cellFormatGreen.set_bg_color('green')
        self.cellFormatRed = self.workbook.add_format()
        self.cellFormatRed.set_bg_color('red')
        self.cellFormatBold = self.workbook.add_format()
        self.cellFormatBold.set_bold(bold=True)
        self.summaryRow = 0
        self.__setHeaderDetailSheet()
        self.makeSummary()
        self.exportResult()
        self.exportTiming = ExportTiming(self.dataRecords, self.timingsheet)
        self.closeExcel()
        self.dataExport()

    def exportResult(self, **kwargs):
        self._exportData()

    def makeSummary(self):

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
        # fixme: Here is a new bug (Earthsquad-Demo.XLS --> he doesn't find Sequence1 and then breaks. Theoretically there should always be a sequence 1 - even in simple XLS-Format.
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
        elif not "/" in self.testRunInstance.globalSettings[GC.DATABASE_EXPORTFILENAMEANDPATH][0:1]:
            basePath = Path(sys.modules['__main__'].__file__).parent
        else:
            basePath = ""
        l_file: Path = Path(basePath).joinpath(self.testRunInstance.globalSettings[GC.DATABASE_EXPORTFILENAMEANDPATH])
        if "~" in str(l_file.absolute()):
            l_file = l_file.expanduser()
        if not Path(l_file).is_dir():
            logger.info(f"Create directory {l_file}")
            Path(l_file).mkdir(parents=True, exist_ok=True)
        l_file = l_file.joinpath("baangt_" + self.testRunName + "_" + utils.datetime_return() + ".xlsx")
        logger.debug(f"Filename for export: {str(l_file)}")
        return str(l_file)

    def __setHeaderDetailSheet(self):
        i = 0
        for column in self.fieldListExport:
            self.worksheet.write(0, i, column)
            i += 1
        self.worksheet.write(0, len(self.fieldListExport), "JSON")

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


    def dataExport(self):
        # database = "g:\\work\\codebase\\baangt\\baangt\\db\\phaseSqlite.db"
        database= r"C:\sqlitedb\test.db"
        self.testList.append(database)
        sql_create_result_table = """CREATE TABLE IF NOT EXISTS result(
                    id integer PRIMARY KEY,
                    TestName text NOT NULL,
                    LogfileName text NOT NULL,
                    StartTime text NOT NULL,
                    EndTime text NOT NULL,
                    globalValue1 text NOT NULL,
                    globalValue2 text NOT NULL,
                    globalValue3 text NOT NULL,
                    globalValue4 text NOT NULL,
                    dbFile text NOT NULL,
                    numTestCaseOk integer,
                    numTestCasePaused integer,
                    numTestCaseFail integer        
                    );"""
        conn = self.createDb(database)
        content = []
        for i in range(len(self.testList)):
            content.append(self.testList[i])
        if conn is not None:
            # print(content)
            self.createTbl(conn, sql_create_result_table,content)
        else:
            print("Error! cannot create the database connection.")

    def createDb(self,db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        return conn

    def createTbl(self,conn,create_table_sql,content):
        try:
            # print(content)
            c = conn.cursor()
            c.execute(create_table_sql)
            print("=============================")
            sqlite_insert_query = """INSERT INTO result(id,TestName,LogfileName,StartTime,EndTime,globalValue1,globalValue2,globalValue3,globalValue4,dbFile,numTestCaseOk,numTestCasePaused,numTestCaseFail)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);"""
            data_tuple = (1,content[0],content[4],content[5],content[6],content[8],content[9],content[10],content[11],content[13],content[1],content[3],content[2])
            c.execute(sqlite_insert_query,data_tuple)
            conn.commit()
        except Error as e:
            print(e)

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
            if "Start:" in line:
                # Format <sequence>: <Start>: <time.loctime>
                continue
            else:
                lSection = parts[0].replace(":","").strip()
                lDuration = parts[1].split(":")[1]
                lExport[lSection] = {GC.TIMING_DURATION: lDuration}
        return lExport

