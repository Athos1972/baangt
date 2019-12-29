from pyFETest.HandleDatabase import HandleDatabase
from pyFETest.CustBrowserHandling import CustBrowserHandling
from pyFETest.utils import utils
from pyFETest.ExportResults import ExportResults
from pyFETest import GlobalConstants as GC

class TestRun:
    def __init__(self, testRunName, browserName = None):
        self.testRunName = testRunName
        self.testdataDataBase : HandleDatabase = None
        self.testrunAttributes = None
        self.browser = None
        self.dataRecord = None
        self.outputDocument = None
        if browserName:
            self.testrunAttributes[self.testRunName]["BROWSER"] = browserName
        self.__initTestRun()
        self.recordPointer = self.testrunAttributes[self.testRunName]["FROM_LINE"]
        self.recordCounter = 0

    def tearDown(self):
        self.browser.closeBrowser()
        self.browser.takeTime("complete Testrun")
        self.browser.takeTimeSumOutput()
        self.outputDocument.close()

    def __getDatabase(self):
        if not self.testdataDataBase:
            self.testdataDataBase = HandleDatabase()
            self.testdataDataBase.read_excel(fileName=self.testrunAttributes[self.testRunName]["DATAFILE"],
                                             sheetName=self.testrunAttributes[self.testRunName]["SHEET"])
        return self.testdataDataBase

    def getNextRecord(self):
        if self.testdataDataBase:
            if self.recordPointer > self.testrunAttributes[self.testRunName]["TO_LINE"]:
                return (None, None)
        else:
            self.__getDatabase()

        self.dataRecord = self.testdataDataBase.readTestRecord(self.recordPointer)
        self.recordPointer += 1
        self.recordCounter += 1
        return self.dataRecord, self.recordCounter

    def __getRecord(self, recordNumber):
        self.dataRecord = self.testdataDataBase.readTestRecord(recordNumber)

    def getBrowser(self):
        if not self.browser:
            self.browser = CustBrowserHandling()
            self.browser.createNewBrowser(self.testrunAttributes[self.testRunName]["BROWSER"])
            self.browser.takeTime("Complete TestRun")
        return self.browser

    def __handleExcel(self):
        self.outputDocument = ExportResults(self.__getOutputFileName())

    def finishTestCase(self):
        self.dataRecord[GC.TIMELOG] = self.browser.returnTime()
        self.browser.takeTimeSumOutput()
        self.outputDocument.addEntry(self.dataRecord)
        self.browser.resetTime()

    def __getOutputFileName(self):
        self.__getRecord(self.testrunAttributes[self.testRunName]["FROM_LINE"])
        l_file = "/Users/bernhardbuhl/git/KatalonVIG/1testoutput/" + \
                 "pyTest_" + \
                 self.testrunAttributes[self.testRunName]["BROWSER"] + "_" + \
                 utils.datetime_return() + "_" + self.dataRecord["base_url"] \
                 + ".xlsx"
        return l_file

    def __initTestRun(self):
        self.testrunAttributes= {
            "WSTV-Heartbeat": {
                "DATAFILE": '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/testdata_wstv_fqa.xlsx',
                "SHEET": 'Testcases',
                "BROWSER": 'FF',
                "FROM_LINE": 489,
                "TO_LINE": 491
            }
        }
        self.__getDatabase()
        self.__handleExcel()