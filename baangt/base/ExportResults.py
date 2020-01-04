import xlsxwriter
import logging
import json
import baangt.base.GlobalConstants as GC
from baangt.base.utils import utils

logger = logging.getLogger("pyC")

class ExportResults:
    def __init__(self, **kwargs):
        self.testRunName = kwargs.get(GC.KWARGS_TESTRUNINSTANCE).testRunName
        self.filename = self.__getOutputFileName()
        logger.info("Export-Sheet für Ergebnisse: " + self.filename)
        self.workbook = xlsxwriter.Workbook(self.filename)
        self.worksheet = self.workbook.add_worksheet("Output")
        self.dataRecords = kwargs.get(GC.KWARGS_TESTRUNINSTANCE).dataRecords
        self.fieldListExport = kwargs.get(GC.KWARGS_TESTRUNATTRIBUTES).get(GC.EXPORT_FORMAT)["Fieldlist"]
        self.__setHeader()
        self._exportData()
        self.closeExcel()

    def __getOutputFileName(self):
        l_file = "/Users/bernhardbuhl/git/KatalonVIG/1testoutput/" + \
                 "baangt_" + self.testRunName + "_" + \
                 utils.datetime_return() + \
                 ".xlsx"
        logger.debug(f"Filename for export: {l_file}")
        return l_file

    def __setHeader(self):
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

    def __writeCell(self, line, cellNumber, testRecordDict, fieldName, strip=False):
        if fieldName in testRecordDict.keys() and testRecordDict[fieldName]:
            if '/n' in testRecordDict[fieldName][0:5] or strip:
                testRecordDict[fieldName] = testRecordDict[fieldName].strip()
            if isinstance(testRecordDict[fieldName], dict) or isinstance(testRecordDict[fieldName], list):
                self.worksheet.write(line, cellNumber, testRecordDict[fieldName].strip())
            else:
                self.worksheet.write(line, cellNumber, testRecordDict[fieldName])

    def closeExcel(self):
        self.workbook.close()
