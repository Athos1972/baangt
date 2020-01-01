from baangt.HandleDatabase import HandleDatabase
from baangt.CustBrowserHandling import CustBrowserHandling
from baangt.utils import utils
from baangt.ExportResults import ExportResults
from baangt import GlobalConstants as GC
from baangt import CustGlobalConstants as CGC
import logging

logger = logging.getLogger("pyC")

class TestRun:
    def __init__(self, testRunName, browserName = None):
        self.testRunName = testRunName
        self.testdataDataBase : HandleDatabase = None
        self.testrunAttributes = None
        self.browser = {}
        self.dataRecord = {}
        self.outputDocument = None
        self.recordCounter = 0
        self.outputRecords = {}
        if browserName:
            self.testrunAttributes[self.testRunName]["BROWSER"] = browserName
        self.__initTestRun()
        self.recordPointer = self.testrunAttributes[self.testRunName]["FROM_LINE"]

    def tearDown(self, browserInstance=1):
        self.browser[browserInstance].closeBrowser()
        self.browser[browserInstance].takeTime(GC.TIMING_TESTRUN)
        self.browser[browserInstance].takeTimeSumOutput()
        try:
            self.__writeOutputRecords()
            self.outputDocument.close()
            logger.info("Wrote output document")
            self.outputDocument = None
        except Exception as e:
            logger.debug("Output Document already closed")

    def __writeOutputRecords(self):
        for key, value in self.outputRecords.items():
            logger.debug(f"Writing output to XLS, line: {key}")
            self.outputDocument.addEntry(testRecordDict=value, sameLine=False, lineNumber=key)

    def __getDatabase(self):
        if not self.testdataDataBase:
            self.testdataDataBase = HandleDatabase()
            self.testdataDataBase.read_excel(fileName=self.testrunAttributes[self.testRunName]["DATAFILE"],
                                             sheetName=self.testrunAttributes[self.testRunName]["SHEET"])
        return self.testdataDataBase

    def getNextRecord(self):
        self.recordCounter += 1
        if self.testdataDataBase:
            if self.recordPointer > self.testrunAttributes[self.testRunName]["TO_LINE"]:
                return (None, None)
        else:
            self.__getDatabase()

        self.dataRecord[self.recordCounter] = self.testdataDataBase.readTestRecord(self.recordPointer)
        self.recordPointer += 1
        return self.dataRecord[self.recordCounter], self.recordCounter

    def getTestcaseSequence(self):
        return self.testrunAttributes[self.testRunName]["TESTCASE-SEQUENCE"]

    def getParallelizationCount(self):
        if self.testrunAttributes[self.testRunName].get("PARALLEL_RUNS"):
            return self.testrunAttributes[self.testRunName].get("PARALLEL_RUNS")
        else:
            return 1

    def __getRecord(self, recordNumber):
        self.dataRecord[self.recordCounter] = self.testdataDataBase.readTestRecord(recordNumber)

    def getBrowser(self, browserInstance=1):
        if browserInstance not in self.browser.keys():
            logger.info(f"opening new instance of browser {browserInstance}")
            self.browser[browserInstance] = CustBrowserHandling()
            self.browser[browserInstance].createNewBrowser(
                browserName=self.testrunAttributes[self.testRunName]["BROWSER"],
                desiredCapabilities=self.testrunAttributes[self.testRunName]["BROWSER_ATTRIBUTES"])
            self.browser[browserInstance].takeTime(GC.TIMING_TESTRUN)
        else:
            logger.warning(f"Using existing instance of browser {browserInstance}")
        return self.browser[browserInstance]

    def __handleExcel(self):
        self.outputDocument = ExportResults(self.__getOutputFileName())

    def setResult(self, recordNumber, dataRecordResult, browserInstance=1):
        logger.debug(f"Received new result for Testrecord {recordNumber}")
        self.dataRecord[recordNumber] = dataRecordResult
        self.finishTestCase(browserInstance=browserInstance, dataRecordNumber=recordNumber)

    def finishTestCase(self, browserInstance=1, dataRecordNumber=None):
        if not dataRecordNumber:
            dataRecordNumber = self.recordCounter
            logger.debug(f"DataRecordNumber = {dataRecordNumber}")
        dataRecord = self.dataRecord[dataRecordNumber]
        dataRecord[GC.TIMELOG] = self.browser[browserInstance].returnTime()
        if len(dataRecord[CGC.DURATION]) == 0:
            # This was a failed testcase - didn't reach the end. Still take overall time:
            dataRecord[CGC.DURATION] = self.browser[browserInstance].takeTime("Testfall gesamt")
        self.browser[browserInstance].takeTimeSumOutput()
        self.outputRecords[dataRecordNumber] = dataRecord
        self.browser[browserInstance].resetTime()

    def __getOutputFileName(self):
        self.__getRecord(self.testrunAttributes[self.testRunName]["FROM_LINE"])
        l_file = "/Users/bernhardbuhl/git/KatalonVIG/1testoutput/" + \
                 "pyTest_" + \
                 self.testrunAttributes[self.testRunName]["BROWSER"] + "_" + \
                 utils.datetime_return() + "_" + self.dataRecord[self.recordCounter]["base_url"] \
                 + ".xlsx"
        return l_file

    def __initTestRun(self):
        self.testrunAttributes= {
            "Heartbeat": {
                "DATAFILE": '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/testdata_wstv_fqa.xlsx',
                "SHEET": 'Testcases',
                "BROWSER": GC.BROWSER_CHROME,
                "BROWSER_ATTRIBUTES": "",
                "TESTCASE-SEQUENCE": {
                    1: "ProduktauswahlURL",
                    2: "Login",
                    3: "ProduktAuswahl",
                    4: "ObjektSeite",
                    5: "Empfehlungen",
                    6: "Deckungsumfang",
                    7: "Praemienauskunft",
                    8: "Beratungsprotokoll",
                    9: "VertragDaten",
                    10: "AntragsFragen",
                    11: "Vermittler",
                    12: "Dokumente",
                    13: "AntragSenden"
                },
                "PARALLEL_RUNS": 5,
                "FROM_LINE": 488,
                "TO_LINE": 499
            },
            "HB-Dark": {
                "DATAFILE": '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/testdata_wstv_fqa.xlsx',
                "SHEET": 'Testcases',
                "BROWSER": GC.BROWSER_FIREFOX,
                "BROWSER_ATTRIBUTES": {GC.BROWSER_MODE_HEADLESS: True},
                "FROM_LINE": 488,
                "TO_LINE": 494,
                "TESTCASE-SEQUENCE": {
                    1: "ProduktauswahlURL",
                    2: "Login",
                    3: "ProduktAuswahl",
                    4: "ObjektSeite",
                    5: "Empfehlungen",
                    6: "Deckungsumfang",
                    7: "Praemienauskunft",
                    8: "Beratungsprotokoll",
                    9: "VertragDaten",
                    10: "AntragsFragen",
                    11: "Vermittler",
                    12: "Dokumente",
                    13: "AntragSenden"
                },
                "PARALLEL_RUNS": 3
            },
            "WSTV-Single": {
                "DATAFILE": '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/testdata_wstv_fqa.xlsx',
                "SHEET": 'Testcases',
                "BROWSER": GC.BROWSER_FIREFOX,
                "BROWSER_ATTRIBUTES": "",
                "FROM_LINE": 488,
                "TO_LINE": 488
            },
            "Partner": {
                "DATAFILE": '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/testdata_wstv_fqa.xlsx',
                "SHEET": 'TC_Partner',
                "BROWSER": GC.BROWSER_FIREFOX,
                "BROWSER_ATTRIBUTES": "",
                "FROM_LINE": 2,
                "TO_LINE": 4
            },
            "SAP": {
                "DATAFILE": '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/testdata_wstv_fqa.xlsx',
                "SHEET": 'TC_Partner',
                "BROWSER": GC.BROWSER_FIREFOX,
                "BROWSER_ATTRIBUTES": "",
                "FROM_LINE": 2,
                "TO_LINE": 2
            }
        }
        self.__getDatabase()
        self.__handleExcel()