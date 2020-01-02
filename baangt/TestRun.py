from baangt.HandleDatabase import HandleDatabase
from baangt.CustBrowserHandling import CustBrowserHandling
from baangt.ApiHandling import ApiHandling
from baangt.utils import utils
from baangt.ExportResults import ExportResults
# from TestCaseSequence.TestCaseSequenceMaster import TestCaseSequenceMaster
# from TestCase.TestCaseMaster import TestCaseMaster
from baangt import GlobalConstants as GC
from baangt import CustGlobalConstants as CGC
import logging
import sys

logger = logging.getLogger("pyC")


class TestRun:
    def __init__(self, testRunName, browserName=None):
        self.testRunName = testRunName
        self.testrunAttributes = None
        self.browser = {}
        self.apiInstance = None
        self.dataRecord = {}
        self.outputDocument = None
        self.outputRecords = {}
        self.testType = None
        if browserName:
            # Overwrites the Browser-definition of the testcase
            self.testrunAttributes[self.testRunName][GC.KWARGS_BROWSER] = browserName
        self._initTestRun()

    def tearDown(self, browserInstance=1):
        if self.browser.get(browserInstance):
            self.browser[browserInstance].closeBrowser()
            self.browser[browserInstance].takeTime(GC.TIMING_TESTRUN)
            self.browser[browserInstance].takeTimeSumOutput()
        if self.apiInstance:
            self.apiInstance.tearDown()
        try:
            self.__writeOutputRecords()
            self.outputDocument.close()
            logger.info("Wrote output document")
            self.outputDocument = None
        except Exception as e:
            logger.debug("Output Document already closed")

    def __writeOutputRecords(self):
        self.__handleExcel()
        for key, value in self.outputRecords.items():
            logger.debug(f"Writing output to XLS, line: {key}")
            self.outputDocument.addEntry(testRecordDict=value, sameLine=False, lineNumber=key)

    def getAllTestRunAttributes(self):
        return self.testrunAttributes[self.testRunName]

    def getBrowser(self, browserInstance=1, browserName=None, browserAttributes=None):
        if browserInstance not in self.browser.keys():
            logger.info(f"opening new instance {1} of browser {browserName}")
            self.browser[browserInstance] = CustBrowserHandling()
            self.browser[browserInstance].createNewBrowser(
                browserName=browserName,
                desiredCapabilities=browserAttributes)
            self.browser[browserInstance].takeTime(GC.TIMING_TESTRUN)
        else:
            logger.debug(f"Using existing instance of browser {browserInstance}")
        return self.browser[browserInstance]

    def getAPI(self):
        if not self.apiInstance:
            self.apiInstance = ApiHandling()
        return self.apiInstance

    def __handleExcel(self):
        self.outputDocument = ExportResults(self.__getOutputFileName())

    def __getOutputFileName(self):
        l_file = "/Users/bernhardbuhl/git/KatalonVIG/1testoutput/" + \
                 "baangt_" + self.testRunName + "_" + \
                 utils.datetime_return() + \
                 ".xlsx"
        return l_file

    def setResult(self, recordNumber, dataRecordResult, browserInstance=1):
        logger.debug(f"Received new result for Testrecord {recordNumber}")
        self.dataRecord[recordNumber] = dataRecordResult

    def executeTestRun(self):
        """
            Start TestcaseSequence
        """
        self.executeDictSequenceOfClasses(
            self.testrunAttributes[self.testRunName][GC.KWARGS_TESTRUNATTRIBUTES][GC.STRUCTURE_TESTCASESEQUENCE],
            counterName=GC.STRUCTURE_TESTCASESEQUENCE)

    def executeDictSequenceOfClasses(self, dictSequenceOfClasses, counterName, **kwargs):
        if not kwargs.get(GC.KWARGS_TESTRUNATTRIBUTES):
            kwargs[GC.KWARGS_TESTRUNATTRIBUTES] = self.getAllTestRunAttributes()
        if not kwargs.get(GC.KWARGS_TESTRUNINSTANCE):
            kwargs[GC.KWARGS_TESTRUNINSTANCE] = self
        for key, value in dictSequenceOfClasses.items():
            logger.info(f"Starting {counterName}: {key}, {value} ")
            kwargs[counterName] = key
            if isinstance(value, list):
                lFullQualified = value[0]  # First List-Entry must hold the ClassName
            else:
                lFullQualified = value

            if "." in lFullQualified:
                l_class = TestRun.__dynamicImportClasses(lFullQualified)
            else:
                l_class = globals()[lFullQualified]
            l_class(**kwargs)  # Executes the class __init__

    def _initTestRun(self):
        pass

    @staticmethod
    def __dynamicImportClasses(fullQualifiedImportName):
        """Requires fully qualified Name of Import-Class and module,
        e.g. TestCaseSequence.TCS_VIGO.TCS_VIGO if the class TCS_VIGO
                                                is inside the Python-File TCS_VIGO
                                                which is inside the Module TestCaseSequence
        if name is not fully qualified, the ClassName must be identical with the Python-File-Name,
        e.g. TestSteps.Franzi will try to import TestSteps.Franzi.Franzi"""
        importClass = fullQualifiedImportName.split(".")[-1]
        if globals().get(importClass):
            return globals()[importClass]  # Class already imported

        if fullQualifiedImportName.split(".")[-2:-1][0] == fullQualifiedImportName.split(".")[-1]:
            moduleToImport = ".".join(fullQualifiedImportName.split(".")[0:-1])
        else:
            moduleToImport = fullQualifiedImportName

        mod = __import__(moduleToImport, fromlist=importClass)
        logger.debug(f"Imported module {fullQualifiedImportName}, result was {str(mod)}")
        retClass = getattr(mod, importClass)
        if not retClass:
            logger.critical(f"Can't import module: {fullQualifiedImportName}, error: {e}")
            sys.exit("Critical Error in Class import - can't continue. "
                     "Please maintain proper classnames in Testrundefinition.")
        return retClass
