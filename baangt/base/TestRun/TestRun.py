from baangt.base.BrowserHandling.BrowserHandling import BrowserDriver
from baangt.base.ApiHandling import ApiHandling
from baangt.base.ExportResults.ExportResults import ExportResults
from baangt.base.Utils import utils
from baangt.base import GlobalConstants as GC
from baangt.base.TestRunExcelImporter import TestRunExcelImporter
from baangt.base.BrowserFactory import BrowserFactory
# needed - they'll be used dynamically later
from baangt.TestSteps.TestStepMaster import TestStepMaster
from baangt.TestCase.TestCaseMaster import TestCaseMaster
from baangt.TestCaseSequence.TestCaseSequenceMaster import TestCaseSequenceMaster
from baangt.base.ProxyRotate import ProxyRotate
import logging
from pathlib import Path
import sys
import os
from baangt.base.Timing.Timing import Timing
from baangt.base.TestRunUtils import TestRunUtils
import time

logger = logging.getLogger("pyC")


class TestRun:
    """
    This is the main Class of Testexecution in the baangt Framework. It is usually started
    from baangt.py
    """

    def __init__(self, testRunName, globalSettingsFileNameAndPath=None,
                 testRunDict=None):  # -- API support: testRunDict --
        """
        @param testRunName: The name of the TestRun to be executed.
        @param globalSettingsFileNameAndPath: from where to read the <globals>.json
        """
        logger.info('init Testrun, id is {}'.format(id(self)))

        self.apiInstance = None
        self.testType = None
        self.networkInfo = None
        self.kwargs = {}
        self.dataRecords = {}
        self.globalSettingsFileNameAndPath = globalSettingsFileNameAndPath
        self.globalSettings = {}

        # -- API support --
        # results
        self.results = None
        self.testRunDict = testRunDict
        # -- END of API support

        # New way to export additional Tabs to Excel
        # If you want to export additional data, place a Dict with Tabname + Datafields in additionalExportTabs.
        self.additionalExportTabs = {}

        self.testRunName, self.testRunFileName = \
            self._sanitizeTestRunNameAndFileName(testRunName)
        self.timing = Timing()
        self.timing.takeTime(GC.TIMING_TESTRUN)  # Initialize Testrun Duration
        self.testRunUtils = TestRunUtils()
        self._initTestRun()  # Loads the globals*.json file

        self.testCasesEndDateTimes_1D = []  # refer to single execution
        self.testCasesEndDateTimes_2D = [[]]  # refer to parallel execution
        self._loadJSONTestRunDefinitions()
        self._loadExcelTestRunDefinitions()

        self.browserFactory = BrowserFactory(self)

        self.executeTestRun()
        self.tearDown()

    def append1DTestCaseEndDateTimes(self, dt):
        self.testCasesEndDateTimes_1D.append(dt)

    def append2DTestCaseEndDateTimes(self, index, tcAndDt):
        tc = tcAndDt[0]
        dt = tcAndDt[1]
        [self.testCasesEndDateTimes_2D.append([]) for i in range(
            index + 1 - len(self.testCasesEndDateTimes_2D))] if index + 1 > len(
            self.testCasesEndDateTimes_2D) else None
        self.testCasesEndDateTimes_2D[index].append([tc, dt])

    def tearDown(self):
        """
        Close browser (unless stated in the Globals to not do so) and API-Instances
        Take overall Time spent for the complete TestRun
        Write results of TestRun to output channel(s)
        """

        self.timing.takeTime(GC.TIMING_TESTRUN)
        self.timing.takeTimeSumOutput()

        if self.apiInstance:
            self.apiInstance.tearDown()

        network_info = self.browserFactory.teardown()
        self.kwargs['networkInfo'] = network_info

        if self.testCasesEndDateTimes_1D:
            self.kwargs['testCasesEndDateTimes_1D'] = self.testCasesEndDateTimes_1D

        if self.testCasesEndDateTimes_2D and self.testCasesEndDateTimes_2D[0]:
            self.kwargs['testCasesEndDateTimes_2D'] = self.testCasesEndDateTimes_2D

        if len(self.additionalExportTabs) > 0:
            self.kwargs[GC.EXPORT_ADDITIONAL_DATA] = self.additionalExportTabs

        self.results = ExportResults(**self.kwargs)  # -- API support: self.results --
        successful, error = self.getSuccessAndError()

        logger.info(f"Finished execution of Testrun {self.testRunName}. "
                    f"{successful} Testcases successfully executed, {error} errors")
        print(f"Finished execution of Testrun {self.testRunName}. "
              f"{successful} Testcases successfully executed, {error} errors")

    def getSuccessAndError(self):
        """
        Returns number of successful and number of error test cases of the current test run
        @rtype: object
        """
        lError = 0
        lSuccess = 0
        for value in self.dataRecords.values():
            if value[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_ERROR:
                lError += 1
            elif value[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_SUCCESS:
                lSuccess += 1
        return lSuccess, lError

    def getAllTestRunAttributes(self):
        return self.testRunUtils.getCompleteTestRunAttributes(self.testRunName)

    def getBrowser(self, browserInstance=0, browserName=None, browserAttributes=None, mobileType=None, mobileApp=None,
                   desired_app=None, mobile_app_setting=None):

        return self.browserFactory.getBrowser(browserInstance=browserInstance,
                                              browserName=browserName,
                                              browserAttributes=browserAttributes,
                                              mobileType=mobileType,
                                              mobileApp=mobileApp,
                                              desired_app=desired_app,
                                              mobile_app_setting=mobile_app_setting)

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

        TestCaseSequence is a sequence of Testcases. In the TestcaseSequence there's a sequential List of
        Testcases to be executed.

        Before the loop (executeDictSequenceOfClasses) variables inside the the testrun-definition are replaced
        by values from the globals-file (e.g. if you want to generally run with FF, but in a certain case you want to
        run with Chrome, you'd have FF in the Testrundefinition, but set parameter in globals_chrome.json accordingly
        (in this case {"TC.Browser": "CHROME"}. TC.-Prefix signals the logic to look for this variable ("Browser")
        inside the testcase definitions and replace it with value "CHROME".

        """
        self.testRunUtils.replaceGlobals(self.globalSettings)

        kwargs = {GC.KWARGS_TESTRUNATTRIBUTES: self.getAllTestRunAttributes(),
                  GC.KWARGS_TESTRUNINSTANCE: self,
                  GC.KWARGS_TIMING: self.timing}

        self.executeDictSequenceOfClasses(
            kwargs[GC.KWARGS_TESTRUNATTRIBUTES][GC.STRUCTURE_TESTCASESEQUENCE],
            counterName=GC.STRUCTURE_TESTCASESEQUENCE, **kwargs)

    def executeDictSequenceOfClasses(self, dictSequenceOfClasses, counterName, **kwargs):
        """
        This is the main loop of the TestCaseSequence, TestCases, TestStepSequences and TestSteps.
        The Sequence of which class instance to create is defined by the TestRunAttributes.

        Before instancgetBrowsering the class it is checked, whether the class was loaded already and if not, will be loaded
        (only if the classname is fully qualified (e.g baangt<projectname>.TestSteps.myTestStep).
        If the testcase-Status is already "error" (GC.TESTCASESTATUS_ERROR) we'll stop the loop.

        @param dictSequenceOfClasses: The list of classes to be instanced. Must be a dict of {Enum, Classname},
        can be also {enum: [classname, <whatEverElse>]}
        @param counterName: Which Structure element we're currently looping, e.g. "TestStep" (GC.STRUCTURE_TESTSTEP)
        @param kwargs: TestrunAttributes, this TestRun, the Timings-Instance, the datarecord

        """
        if not kwargs.get(GC.KWARGS_TESTRUNATTRIBUTES):
            kwargs[GC.KWARGS_TESTRUNATTRIBUTES] = self.getAllTestRunAttributes()
        if not kwargs.get(GC.KWARGS_TESTRUNINSTANCE):
            kwargs[GC.KWARGS_TESTRUNINSTANCE] = self
            logger.info('get into not kwargs.getGC.KWARGS_TESTRUNINSTANCE, id is {}'.format(id(self)))
        if not kwargs.get(GC.KWARGS_TIMING):
            kwargs[GC.KWARGS_TIMING] = self.timing
        for key, value in dictSequenceOfClasses.items():
            # If any of the previous steps set the testcase to "Error" - exit here.
            if kwargs.get(GC.KWARGS_DATA):
                if kwargs[GC.KWARGS_DATA][GC.TESTCASESTATUS] == GC.TESTCASESTATUS_ERROR:
                    logger.info(f"TC is already in status Error - not processing steps {counterName}: {key}, {value}"
                                f"and everything behind this step")
                    return
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
        if not self.globalSettings.get(GC.PATH_SCREENSHOTS, None):
            self.globalSettings[GC.PATH_SCREENSHOTS] = str(Path(self.globalSettingsFileNameAndPath
                                                                ).parent.joinpath("Screenshots").expanduser())
            self.globalSettings[GC.PATH_EXPORT] = str(Path(self.globalSettingsFileNameAndPath
                                                           ).parent.joinpath("1testoutput").expanduser())
            self.globalSettings[GC.PATH_IMPORT] = str(Path(self.globalSettingsFileNameAndPath
                                                           ).parent.joinpath("0testdateninput").expanduser())
            self.globalSettings[GC.PATH_ROOT] = str(Path(self.globalSettingsFileNameAndPath
                                                         ).parent.expanduser())

    def loadJSONGlobals(self):
        if self.globalSettingsFileNameAndPath:
            self.globalSettings = utils.openJson(self.globalSettingsFileNameAndPath)

    def _loadJSONTestRunDefinitions(self):
        if not self.testRunFileName and not self.testRunDict:  # -- API support: testRunDict --
            return

        if self.testRunFileName and ".JSON" in self.testRunFileName.upper():  # -- API support: self.testRunFileName --
            data = utils.replaceAllGlobalConstantsInDict(utils.openJson(self.testRunFileName))
            self.testRunUtils.setCompleteTestRunAttributes(testRunName=self.testRunName,
                                                           testRunAttributes=data)

        # -- API support --
        # load TestRun from dict
        if self.testRunDict:
            data = utils.replaceAllGlobalConstantsInDict(self.testRunDict)
            self.testRunUtils.setCompleteTestRunAttributes(testRunName=self.testRunName,
                                                           testRunAttributes=data)
        # -- END of API support --

    def _loadExcelTestRunDefinitions(self):
        if not self.testRunFileName:
            return

        if ".XLSX" in self.testRunFileName.upper():
            logger.info(f"Reading Definition from {self.testRunFileName}")
            lExcelImport = TestRunExcelImporter(FileNameAndPath=self.testRunFileName, testRunUtils=self.testRunUtils)
            lExcelImport.importConfig(global_settings=self.globalSettings)

    @staticmethod
    def __dynamicImportClasses(fullQualifiedImportName):
        """
        Requires fully qualified Name of Import-Class and module,
        e.g. TestCaseSequence.TCS_VIGO.TCS_VIGO if the class TCS_VIGO
                                                is inside the Python-File TCS_VIGO
                                                which is inside the Module TestCaseSequence
        if name is not fully qualified, the ClassName must be identical with the Python-File-Name,
        e.g. TestSteps.Franzi will try to import TestSteps.Franzi.Franzi
        @param fullQualifiedImportName:
        @return: The class instance. If no class instance can be found the TestRun aborts hard with sys.exit
        """
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
        """
        @param TestRunNameInput: The complete File and Path of the TestRun definition (JSON or XLSX).
        @return: TestRunName and FileName (if definition of testrun comes from a file (JSON or XLSX)
        """
        if ".XLSX" in TestRunNameInput.upper() or ".JSON" in TestRunNameInput.upper():
            lRunName = utils.extractFileNameFromFullPath(TestRunNameInput)
            lFileName = TestRunNameInput
        else:
            lRunName = TestRunNameInput
            lFileName = None

        return lRunName, lFileName


if __name__ == '__main__':
    print(1)
