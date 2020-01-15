import xlsxwriter
import logging
import json
import baangt.base.GlobalConstants as GC
from baangt.base.Timing import Timing
import subprocess
from baangt.base.utils import utils
from pathlib import Path
from typing import Optional
from xlsxwriter.worksheet import (
    Worksheet, cell_number_tuple, cell_string_tuple)

logger = logging.getLogger("pyC")


class ExportResults:
    def __init__(self, **kwargs):
        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.testRunName = self.testRunInstance.testRunName
        self.filename = self.__getOutputFileName()
        logger.info("Export-Sheet for results: " + self.filename)
        self.workbook = xlsxwriter.Workbook(self.filename)
        self.summarySheet = self.workbook.add_worksheet("Summary")
        self.worksheet = self.workbook.add_worksheet("Output")
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

    def exportResult(self, **kwargs):
        self._exportData()
        self.closeExcel()

    def makeSummary(self):

        self.summarySheet.write(0,0, f"Testreport for {self.testRunName}", self.cellFormatBold)
        self.summarySheet.set_column(0, last_col=0, width=15)

        # Testrecords
        self.__writeSummaryCell("Testrecords", len(self.dataRecords), row=2, format=self.cellFormatBold)
        self.__writeSummaryCell("Successful", len([x for x in self.dataRecords.values()
                                                   if x[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_SUCCESS]),
                                format=self.cellFormatGreen)
        self.__writeSummaryCell("Paused", len([x for x in self.dataRecords.values()
                                                   if x[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_WAITING]))
        self.__writeSummaryCell("Error", len([x for x in self.dataRecords.values()
                                               if x[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_ERROR]),
                                format=self.cellFormatRed)

        # Logfile
        self.__writeSummaryCell("Logfile", logger.handlers[1].baseFilename, row=7)

        # Timing
        timing:Timing = self.testRunInstance.timing
        start, end, duration = timing.returnTimeSegment(GC.TIMING_TESTRUN)
        self.__writeSummaryCell("Starttime", start, row=9)
        self.__writeSummaryCell("Endtime", end)
        self.__writeSummaryCell("Duration", duration, format=self.cellFormatBold )

    def __writeSummaryCell(self, lineHeader, lineText, row=None, format=None):
        if not row:
            self.summaryRow += 1
        else:
            self.summaryRow = row

        self.summarySheet.write(self.summaryRow, 0, lineHeader)
        self.summarySheet.write(self.summaryRow, 1, lineText, format)

    def __getOutputFileName(self):
        l_file: Path = Path(self.testRunInstance.globalSettings[GC.DATABASE_EXPORTFILENAMEANDPATH])
        l_file = l_file.expanduser()
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
            ExportResults.set_column_autowidth(self.worksheet, n)

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

    @staticmethod
    def set_column_autowidth(worksheet: Worksheet, column: int):
        """
        Set the width automatically on a column in the `Worksheet`.
        !!! Make sure you run this function AFTER having all cells filled in
        the worksheet!
        """
        maxwidth = ExportResults.get_column_width(worksheet=worksheet, column=column)
        if maxwidth is None:
            return
        elif maxwidth > 50:
            maxwidth = 50
        worksheet.set_column(first_col=column, last_col=column, width=maxwidth)