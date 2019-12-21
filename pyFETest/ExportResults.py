import xlsxwriter
import logging
import json

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
        columns = ["TF-Name", "Description", "VIGOGF#", "SAP-POL", "Vermittler", "VN", "Pol#Host",
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
        self.worksheet.write(self.nextline, 2, testRecordDict["VIGOGF#"])
        self.worksheet.write(self.nextline, 3, testRecordDict["SAPPOL"])
        self.worksheet.write(self.nextline, 4, testRecordDict["vermittler"])
        self.worksheet.write(self.nextline, 5, testRecordDict["VN"])
        self.worksheet.write(self.nextline, 6, testRecordDict["polnrhost"])
        self.worksheet.write(self.nextline, 13, json.dumps(testRecordDict))
        self.worksheet.write(self.nextline, 14, testRecordDict["Dauer"])
        self.worksheet.write(self.nextline, 18, testRecordDict["TimeLog"])

    def close(self):
        self.workbook.close()
