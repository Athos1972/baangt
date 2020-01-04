from baangt.base.BrowserHandling import BrowserDriver
from baangt.base.ApiHandling import ApiHandling
from baangt.base.ExportResults import ExportResults
from baangt.base.Timing import Timing
from baangt.base import GlobalConstants as GC
import logging
import sys

logger = logging.getLogger("pyC")


class TestRun:
    def __init__(self, testRunName, browserName=None):
        self.testRunName = testRunName
        self.testrunAttributes = None
        self.browser = {}
        self.apiInstance = None
        self.dataRecords = {}
        self.testType = None
        self.timing = Timing()
        self.kwargs = {}
        if browserName:
            # Overwrites the Browser-definition of the testcase
            self.testrunAttributes[self.testRunName][GC.KWARGS_BROWSER] = browserName
        self._initTestRun()
        self.executeTestRun()
        self.tearDown()

    def tearDown(self):
        for browserInstance in self.browser.keys():
            self.browser[browserInstance].closeBrowser()

        self.timing.takeTime(GC.TIMING_TESTRUN)
        self.timing.takeTimeSumOutput()

        if self.apiInstance:
            self.apiInstance.tearDown()

        ExportResults(**self.kwargs)

    def getAllTestRunAttributes(self):
        return self.testrunAttributes[self.testRunName][GC.KWARGS_TESTRUNATTRIBUTES]

    def getBrowser(self, browserInstance=1, browserName=None, browserAttributes=None):
        if browserInstance not in self.browser.keys():
            logger.info(f"opening new instance {browserInstance} of browser {browserName}")
            self._getBrowserInstance(browserInstance=browserInstance)
            self.browser[browserInstance].createNewBrowser(
                browserName=browserName,
                desiredCapabilities=browserAttributes)
            self.timing.takeTime(GC.TIMING_TESTRUN)
        else:
            logger.debug(f"Using existing instance of browser {browserInstance}")
        return self.browser[browserInstance]

    def _getBrowserInstance(self, browserInstance):
        self.browser[browserInstance] = BrowserDriver(timing=self.timing)

    def getAPI(self):
        if not self.apiInstance:
            self.apiInstance = ApiHandling()
        return self.apiInstance

    def setResult(self, recordNumber, dataRecordResult, browserInstance=1):
        logger.debug(f"Received new result for Testrecord {recordNumber}")
        self.dataRecords[recordNumber] = dataRecordResult

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
        if not kwargs.get(GC.KWARGS_TIMING):
            kwargs[GC.KWARGS_TIMING] = self.timing
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
        self.kwargs = kwargs

    def _initTestRun(self):
        pass

    def getSequenceByNumber(self, sequence):
        return self.testrunAttributes[self.testRunName][GC.KWARGS_TESTRUNATTRIBUTES][GC.STRUCTURE_TESTCASESEQUENCE].get(sequence)

    def getTestCaseByNumber(self, sequence, testcaseNumber):
        return sequence[1][GC.STRUCTURE_TESTCASE][testcaseNumber]

    def getTestStepByNumber(self, testCase, testStepNumber):
        return testCase[2][GC.STRUCTURE_TESTSTEP].get(testStepNumber)

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
            logger.critical(f"Can't import module: {fullQualifiedImportName}")
            sys.exit("Critical Error in Class import - can't continue. "
                     "Please maintain proper classnames in Testrundefinition.")
        return retClass