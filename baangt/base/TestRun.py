from baangt.base.BrowserHandling import BrowserDriver
from baangt.base.ApiHandling import ApiHandling
from baangt.base.ExportResults import ExportResults
from baangt.base.Timing import Timing
from baangt.base.utils import utils
from baangt.base import GlobalConstants as GC
from baangt.base.TestRunExcelImporter import TestRunExcelImporter
from baangt.base.TestRunUtils import TestRunUtils
import logging
import sys
import json

logger = logging.getLogger("pyC")


class TestRun:
    def __init__(self, testRunName, globalSettingsFileNameAndPath=None):
        self.browser = {}
        self.apiInstance = None
        self.testType = None
        self.kwargs = {}
        self.dataRecords = {}
        self.globalSettingsFileNameAndPath = globalSettingsFileNameAndPath
        self.globalSettings = None

        self.testRunName, self.testRunFileName = TestRun._sanitizeTestRunNameAndFileName(testRunName)
        self.timing = Timing()
        self.testRunUtils = TestRunUtils()
        self._initTestRun()
        self._loadJSONTestRunDefinitions()
        self._loadExcelTestRunDefinitions()
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
        return self.testRunUtils.getCompleteTestRunAttributes(self.testRunName)
        # return self.testRunAttributes[self.testRunName][GC.KWARGS_TESTRUNATTRIBUTES]

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

    def setResult(self, recordNumber, dataRecordResult):
        logger.debug(f"Received new result for Testrecord {recordNumber}")
        self.dataRecords[recordNumber] = dataRecordResult

    def executeTestRun(self):
        """
            Start TestcaseSequence
        """
        self.executeDictSequenceOfClasses(
            self.testRunUtils.getCompleteTestRunAttributes(self.testRunName)[GC.STRUCTURE_TESTCASESEQUENCE],
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
        self.loadJSONGlobals()
        pass

    def loadJSONGlobals(self):
        if self.globalSettingsFileNameAndPath:
            self.globalSettings = utils.openJson(self.globalSettingsFileNameAndPath)

    def _loadJSONTestRunDefinitions(self):
        if not self.testRunFileName:
            return

        if ".JSON" in self.testRunFileName.upper():
            data = utils.replaceAllGlobalConstantsInDict(utils.openJson(self.testRunFileName))
            self.testRunUtils.setCompleteTestRunAttributes(testRunName=self.testRunName,
                                                           testRunAttributes=data)

    def _loadExcelTestRunDefinitions(self):
        if not self.testRunFileName:
            return

        if ".XLSX" in self.testRunFileName.upper():
            logger.info(f"Reading Definition from {self.testRunFileName}")
            lExcelImport = TestRunExcelImporter(FileNameAndPath=self.testRunFileName, testRunUtils=self.testRunUtils)
            lExcelImport.importConfig()

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

    @staticmethod
    def _sanitizeTestRunNameAndFileName(TestRunNameInput):
        if ".XLSX" in TestRunNameInput.upper() or ".JSON" in TestRunNameInput.upper():
            lRunName = utils.extractFileNameFromFullPath(TestRunNameInput)
            lFileName = TestRunNameInput
        else:
            lRunName = TestRunNameInput
            lFileName = None

        return lRunName, lFileName
