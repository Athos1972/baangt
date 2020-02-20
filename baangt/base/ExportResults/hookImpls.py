import baangt
from baangt.base.ExportResults.ExportResults import\
    (ExportResults, ExportTiming, ExcelSheetHelperFunctions)
import logging

logger = logging.getLogger("pyC")


class ExportResultsHookImpl:
    @baangt.hook_impl
    def exportResults_init(self, **kwargs):
        return ExportResults(**kwargs)

    @baangt.hook_impl
    def exportResults_exportToDataBase(self, exportResultsObject):
        return exportResultsObject.exportToDataBase()

    @baangt.hook_impl
    def exportResults_exportResult(self, exportResultsObject, **kwargs):
        return exportResultsObject.exportResultExcel(**kwargs)

    @baangt.hook_impl
    def exportResults_makeSummary(self, exportResultsObject):
        return exportResultsObject.makeSummaryExcel()

    @baangt.hook_impl
    def exportResults_closeExcel(self, exportResultsObject, line, cellNumber, testRecordDict, fieldName, strip=False):
        return exportResultsObject.closeExcel(line, cellNumber, testRecordDict, fieldName, strip)


class ExcelSheetHelperFunctionsHookImpl:
    
    @baangt.hook_impl
    def excelSheetHelperFunctions_init(self):
        return ExcelSheetHelperFunctions()

    @baangt.hook_impl
    def excelSheetHelperFunctions_set_column_autowidth(self, excelSheetHelperFunctionsObject, worksheet, column):
        return excelSheetHelperFunctionsObject.set_column_autowidth(worksheet, column)

    @baangt.hook_impl
    def excelSheetHelperFunctions_get_column_width(self, excelSheetHelperFunctionsObject, worksheet, column):
        return excelSheetHelperFunctionsObject.get_column_width(worksheet, column)


class ExportTimingHookImpl:
    @baangt.hook_impl
    def exportTiming_init(self, testdataRecords, sheet):
        return ExportTiming(testdataRecords, sheet)

    @baangt.hook_impl
    def exportTiming_writeHeader(self, exportTimingObject):
        return exportTimingObject.writeHeader()

    @baangt.hook_impl
    def exportTiming_writeLines(self, exportTimingObject):
        return exportTimingObject.writeLines()

    @baangt.hook_impl
    def exportTiming_shortenTimingValue(self, exportTimingObject, timingValue):
        return exportTimingObject.shortenTimingValue(timingValue)

    @baangt.hook_impl
    def exportTiming_writeCell(self, exportTimingObject, row, col, content, format=None):
        return exportTimingObject.writeCell(row, col, content, format)

    @baangt.hook_impl
    def exportTiming_findAllTimingSections(self, exportTimingObject):
        return exportTimingObject.findAllTimingSections()

    @baangt.hook_impl
    def exportTiming_interpretTimeLog(self, exportTimingObject, lTimeLog):
        return exportTimingObject.interpretTimeLog(lTimeLog)
