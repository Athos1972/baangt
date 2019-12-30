import xlsxwriter
import logging
import json
import pyFETest.CustGlobalConstants as CGC
import pyFETest.GlobalConstants as GC

logger = logging.getLogger("pyC")

class ExportResults():
    def __init__(self, filenameWithPath):
        logger.info("Export-Sheet für Ergebnisse: " + filenameWithPath)
        self.filename = filenameWithPath
        self.workbook = xlsxwriter.Workbook(self.filename)
        self.worksheet = self.workbook.add_worksheet("Output")
        self.nextline = 0
        self.__setHeader()

    def __setHeader(self):
        i = 0
        columns = ["TF-Name", "Description", CGC.VIGOGFNUMMER, CGC.SAPPOLNR, CGC.VERMITTLER, "VN", "Pol#Host",
                   "BeratProt", "Warnmeldung BeratProt", "RefPrämie", "Fehler", "Screenshot", "TraceID",
                   "JSON", "Dauer", "Status", "Letzter Screnshot", "Letzte Meldung", "Zeit-Log"]
        for column in columns:
            self.worksheet.write(0, i, column)
            i += 1

    def addEntry(self, testRecordDict, sameLine=False):
        if not sameLine:
            self.nextline += 1
        logger.info(f"Schreibe Zeile {self.nextline} in's Excel")
        self.worksheet.write(self.nextline, 0, testRecordDict["TFName"])
        self.worksheet.write(self.nextline, 1, testRecordDict["TFDescription"])
        self.worksheet.write(self.nextline, 2, testRecordDict[CGC.VIGOGFNUMMER])
        self.worksheet.write(self.nextline, 3, testRecordDict[CGC.SAPPOLNR])
        self.__writeCell(4, testRecordDict, CGC.VERMITTLER)
        self.__writeCell(5, testRecordDict, "VN")
        self.__writeCell(6, testRecordDict, CGC.POLNRHOST)
        self.__writeCell(9, testRecordDict, CGC.PRAEMIE)
        self.__writeCell(10, testRecordDict, CGC.CUST_TOASTS, strip=True)
        self.worksheet.write(self.nextline, 13, json.dumps(testRecordDict))
        self.__writeCell(14, testRecordDict, CGC.DURATION)
        self.worksheet.write(self.nextline, 15, testRecordDict[GC.TESTCASESTATUS])
        self.__writeCell(17, testRecordDict, CGC.CUST_TOASTS_ERROR, strip=True)
        self.__writeCell(18, testRecordDict, GC.TIMELOG, strip=True)

    def __writeCell(self, cellNumber, testRecordDict, fieldName, strip=False):
        if fieldName in testRecordDict.keys():
            if strip:
                self.worksheet.write(self.nextline, cellNumber, testRecordDict[fieldName].strip())
            else:
                self.worksheet.write(self.nextline, cellNumber, testRecordDict[fieldName])

    def close(self):
        self.workbook.close()
