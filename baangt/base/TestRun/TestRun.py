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
from baangt.base.FilesOpen import FilesOpen
import xlsxwriter
import os
import json
import logging
from pathlib import Path
import sys
from baangt.base.Timing.Timing import Timing
from baangt.base.TestRunUtils import TestRunUtils
from baangt.base.TestRun.ClassesForObjects import ClassesForObjects
import time
from baangt.base.PathManagement import ManagedPaths
from uuid import uuid4
from baangt.base.RuntimeStatistics import Statistic
from baangt.base.SendReports import Sender
import signal

logger = logging.getLogger("pyC")


class TestRun:
    """
    This is the main Class of Testexecution in the baangt Framework. It is usually started
    from baangtIA.py
    """

    def __init__(self, testRunName, globalSettingsFileNameAndPath=None,
                 testRunDict=None, uuid=uuid4(), executeDirect=True):  # -- API support: testRunDict --
        """
        @param testRunName: The name of the TestRun to be executed.
        @param globalSettingsFileNameAndPath: from where to read the <globals>.json
        """

        # Take over importing parameters:
        self.uuid = uuid
        logger.info(f'Init Testrun, uuid is {self.uuid}')
        self.testRunDict = testRunDict
        self.globalSettingsFileNameAndPath = globalSettingsFileNameAndPath
        self.testRunName, self.testRunFileName = \
            self._sanitizeTestRunNameAndFileName(testRunName)

        # Initialize everything else
        self.apiInstance = None
        self.testType = None
        self.networkInfo = None
        self.results = None
        self.browserFactory = None
        self.kwargs = {}
        self.dataRecords = {}
        self.globalSettings = {}
        self.managedPaths = ManagedPaths()
        self.classesForObjects = ClassesForObjects()         # Dynamically loaded classes
        self.timing = Timing()
        self.testRunUtils = TestRunUtils()
        self.testCasesEndDateTimes_1D = []                   # refer to single execution
        self.testCasesEndDateTimes_2D = [[]]                 # refer to parallel execution
        # New way to export additional Tabs to Excel
        # If you want to export additional data, place a Dict with Tabname + Datafields in additionalExportTabs
        # from anywhere within your custom code base.
        self.additionalExportTabs = {}
        self.statistics = Statistic()
        signal.signal(signal.SIGINT, self.exit_signal_handler)
        signal.signal(signal.SIGTERM, self.exit_signal_handler)

        # Initialize other values
        self.timing.takeTime(GC.TIMING_TESTRUN)               # Initialize Testrun Duration

        # Usually the Testrun is called without the parameter executeDirect, meaning it default to "Execute"
        # during Unit-Tests we don't want this behaviour:
        if executeDirect:
            self.executeTestRun()

    def exit_signal_handler(self, signal, frame):
        self.browserFactory.teardown()

    def executeTestRun(self):
        self._initTestRunSettingsFromFile()  # Loads the globals*.json file

        self._loadJSONTestRunDefinitions()
        self._loadExcelTestRunDefinitions()

        self.browserFactory = BrowserFactory(self)
        self.executeTestSequence()
        self.tearDown()

        try:
            Sender.send_all(self.results, self.globalSettings)
        except Exception as ex:
            logger.debug(ex)

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
        waiting = self.getWaiting()
        self.statistics.update_all(successful, error, waiting)
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

    def getWaiting(self):
        lWaiting =0
        for value in self.dataRecords.values():
            if value[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_WAITING:
                lWaiting += 1
        return lWaiting

    def getAllTestRunAttributes(self):
        return self.testRunUtils.getCompleteTestRunAttributes(self.testRunName)

    def getBrowser(self, browserInstance=0, browserName=None, browserAttributes=None, mobileType=None, mobileApp=None,
                   desired_app=None, mobile_app_setting=None, browserWindowSize=None):

        return self.browserFactory.getBrowser(browserInstance=browserInstance,
                                              browserName=browserName,
                                              browserAttributes=browserAttributes,
                                              mobileType=mobileType,
                                              mobileApp=mobileApp,
                                              desired_app=desired_app,
                                              mobile_app_setting=mobile_app_setting,
                                              browserWindowSize=browserWindowSize)

    def getAPI(self):
        if not self.apiInstance:
            self.apiInstance = ApiHandling()
        return self.apiInstance

    def setResult(self, recordNumber, dataRecordResult):
        logger.debug(f"Received new result for Testrecord {recordNumber}")
        self.dataRecords[recordNumber] = dataRecordResult

    def executeTestSequence(self):
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
        self.testRunUtils.replaceClasses(self.testRunName, self.classesForObjects)

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
                if kwargs[GC.KWARGS_DATA].get(GC.TESTCASESTATUS_STOP):
                    logger.info(f"TC wanted to stop. Not processing steps {counterName}: {key}, {value}"
                                f"and everything behind this step. TC-Status is "
                                f"{kwargs[GC.KWARGS_DATA][GC.TESTCASESTATUS]}")
                    return
                if kwargs[GC.KWARGS_DATA].get(GC.TESTCASESTATUS_STOPERROR):
                    kwargs[GC.KWARGS_DATA][GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
                    if not kwargs[GC.KWARGS_DATA].get(GC.TESTCASEERRORLOG):
                        kwargs[GC.KWARGS_DATA][GC.TESTCASEERRORLOG] = "Aborted by command 'TCStopTestCaseError'"
                    else:
                        kwargs[GC.KWARGS_DATA][GC.TESTCASEERRORLOG] = kwargs[GC.KWARGS_DATA][GC.TESTCASEERRORLOG] \
                                                                      + "\nAborted by command 'TCStopTestCaseError'"
                    return

            logger.info(f"Starting {counterName}: {key}")
            kwargs[counterName] = key

            # Get the class reference:
            if isinstance(value, list):
                lFullQualified = value[0]  # First List-Entry must hold the ClassName
            else:
                lFullQualified = value

            l_class = TestRun.__dynamicImportClasses(lFullQualified)

            try:
                l_class(**kwargs)  # Executes the class´es  __init__ method
            except TypeError as e:
                # Damn! The class is wrong.
                l_class = TestRun.__dynamicImportClasses(lFullQualified)
                l_class(**kwargs)

        self.kwargs = kwargs

    def _initTestRunSettingsFromFile(self):
        self.__loadJSONGlobals()
        self.__setPathsIfNotPredefined()
        self.__sanitizeGlobalsValues()

    def __setPathsIfNotPredefined(self):
        if not self.globalSettings.get(GC.PATH_SCREENSHOTS, None):
            self.globalSettings[GC.PATH_SCREENSHOTS] = str(
                Path(self.managedPaths.getOrSetScreenshotsPath()).expanduser())
        else:
            self.managedPaths.getOrSetScreenshotsPath(path=self.globalSettings.get(GC.PATH_SCREENSHOTS))
        if not self.globalSettings.get(GC.PATH_EXPORT, None):
            self.globalSettings[GC.PATH_EXPORT] = str(Path(self.managedPaths.getOrSetExportPath()).expanduser())
        else:
            self.managedPaths.getOrSetExportPath(path=self.globalSettings.get(GC.PATH_EXPORT))
        if not self.globalSettings.get(GC.PATH_IMPORT, None):
            self.globalSettings[GC.PATH_IMPORT] = str(Path(self.managedPaths.getOrSetImportPath()).expanduser())
        else:
            self.managedPaths.getOrSetImportPath(path=self.globalSettings.get(GC.PATH_IMPORT))
        if not self.globalSettings.get(GC.PATH_ROOT, None):
            self.globalSettings[GC.PATH_ROOT] = str(Path(self.managedPaths.getOrSetRootPath()).parent.expanduser())
        else:
            self.managedPaths.getOrSetRootPath(path=self.globalSettings.get(GC.PATH_ROOT))

    def __loadJSONGlobals(self):
        if self.globalSettingsFileNameAndPath:
            self.globalSettings = utils.openJson(self.globalSettingsFileNameAndPath)

        # Set default execution STAGE
        if not self.globalSettings.get(GC.EXECUTION_STAGE, None):
            logger.debug(f"Execution Stage was not set. Setting to default value {GC.EXECUTION_STAGE_TEST}")
            self.globalSettings[GC.EXECUTION_STAGE] = GC.EXECUTION_STAGE_TEST

    def __sanitizeGlobalsValues(self):
        # Support for new dataClass to load different Classes
        for key, value in self.globalSettings.items():
            if "CL." in key:
                self.classesForObjects.__setattr__(key.strip("CL."), value)

            # Change boolean strings into boolean values.
            if isinstance(value, str):
                if value.lower() in ("false", "true", "no", "x"):
                    self.globalSettings[key] = utils.anything2Boolean(value)

            if isinstance(value, dict):
                if "default" in value:
                    # This happens in the new UI, if a value was added manually,
                    # but is not part of the globalSetting.json. In this case there's the whole shebang in a dict. We
                    # are only interested in the actual value, which is stored in "default":
                    self.globalSettings[key] = value["default"]
                    continue
                else:
                    # This could be the "old" way of the globals-file (with {"HEADLESS":"True"})
                    self.globalSettings[key] = value
                    continue

            if isinstance(value, str) and len(value) > 0:
                if value[0] == "{" and value[-1] == "}":
                    # Dict, that is not seen as dict
                    value = value.replace("\'", '"')
                    self.globalSettings[key] = json.loads(value)

        if self.globalSettings.get("TC." + GC.EXECUTION_LOGLEVEL):
            utils.setLogLevel(self.globalSettings.get("TC." + GC.EXECUTION_LOGLEVEL))

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
        return utils.dynamicImportOfClasses(fullQualifiedImportName=fullQualifiedImportName)

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

