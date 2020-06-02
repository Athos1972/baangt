from baangt.base import GlobalConstants as GC
from baangt.base.Timing.Timing import Timing
from baangt.TestSteps.Exceptions import *
from baangt.base.RuntimeStatistics import Statistic


class TestCaseMaster:
    def __init__(self, executeDirect=True, **kwargs):
        self.name = None
        self.description = None
        self.testSteps = {}
        self.apiInstance = None
        self.numberOfParallelRuns = None
        self.statistic = Statistic()
        self.kwargs = kwargs

        self.timing = Timing()  # Use own instance of the timing class, so that we can record timing also in
        # parallel runs.

        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.testRunUtils = self.testRunInstance.testRunUtils
        self.testSequence = self.testRunUtils.getSequenceByNumber(testRunName=self.testRunInstance.testRunName,
                                                                  sequence=kwargs.get(GC.STRUCTURE_TESTCASESEQUENCE))
        self.testCaseSettings = self.testRunUtils.getTestCaseByNumber(self.testSequence,
                                                                      kwargs.get(GC.STRUCTURE_TESTCASE))
        self.testSteps = self.testCaseSettings[2][GC.STRUCTURE_TESTSTEP]
        self.testCaseType = self.testCaseSettings[1][GC.KWARGS_TESTCASETYPE]

        self.sequenceNumber = self.kwargs.get(GC.KWARGS_SEQUENCENUMBER)

        # In Unit-Tests this is a problem. When we run within the main loop of TestRun we are expected to directly
        # execute on __init__.
        if executeDirect:
            self.executeTestCase()

    def executeTestCase(self):
        self.timingName = self.timing.takeTime(self.__class__.__name__, forceNew=True)
        if self.testCaseType == GC.KWARGS_BROWSER:
            self.kwargs[GC.KWARGS_DATA][GC.TESTCASESTATUS] = GC.TESTCASESTATUS_SUCCESS  # We believe in a good outcome
            self.__getBrowserForTestCase()

        elif self.testCaseType == GC.KWARGS_API_SESSION:
            # FIXME: For now we're using session_number always = 1. We need to be able to run e.g. 10 sessions with
            # FIXME: Parallel API-Test.
            self.apiInstance = self.testRunInstance.getAPI()
            self.kwargs[GC.KWARGS_API_SESSION] = self.apiInstance

            # For API-Tests we assume status = Passed and actively set it to error if not.
            self.kwargs[GC.KWARGS_DATA][GC.TESTCASESTATUS] = GC.TESTCASESTATUS_SUCCESS
        self.execute()
        self.tearDown()

    def __getBrowserForTestCase(self):
        logger.info(f"Settings for this TestCase: {str(self.testCaseSettings)[0:100]}")
        self.browserType = self.testCaseSettings[1][GC.KWARGS_BROWSER].upper()
        self.browserSettings = self.testCaseSettings[1][GC.BROWSER_ATTRIBUTES]
        self.mobileType = self.testCaseSettings[1].get(GC.KWARGS_MOBILE)
        self.mobileApp = self.testCaseSettings[1].get(GC.KWARGS_MOBILE_APP)
        browserWindowSize = self.testCaseSettings[1].get(GC.BROWSER_WINDOW_SIZE)
        self.mobile_desired_app = {}
        self.mobile_app_setting = {}
        if self.mobileType:
            self.mobile_desired_app[GC.MOBILE_PLATFORM_NAME] = self.testCaseSettings[1][GC.MOBILE_PLATFORM_NAME]
            self.mobile_desired_app[GC.MOBILE_DEVICE_NAME] = self.testCaseSettings[1][GC.MOBILE_DEVICE_NAME]
            self.mobile_desired_app[GC.MOBILE_PLATFORM_VERSION] = self.testCaseSettings[1][GC.MOBILE_PLATFORM_VERSION]
            self.mobile_app_setting[GC.MOBILE_APP_URL] = self.testCaseSettings[1][GC.MOBILE_APP_URL]
            self.mobile_app_setting[GC.MOBILE_APP_PACKAGE] = self.testCaseSettings[1][GC.MOBILE_APP_PACKAGE]
            self.mobile_app_setting[GC.MOBILE_APP_ACTIVITY] = self.testCaseSettings[1][GC.MOBILE_APP_ACTIVITY]
        self.browser = self.testRunInstance.getBrowser(browserInstance=self.sequenceNumber,
                                                       browserName=self.browserType,
                                                       browserAttributes=self.browserSettings,
                                                       mobileType=self.mobileType,
                                                       mobileApp=self.mobileApp,
                                                       desired_app=self.mobile_desired_app,
                                                       mobile_app_setting=self.mobile_app_setting,
                                                       browserWindowSize=browserWindowSize)
        self.kwargs[GC.KWARGS_BROWSER] = self.browser

    def execute(self):
        # Save timing Class from Testrun for later:
        lTestRunTiming = self.kwargs[GC.KWARGS_TIMING]
        # Replace Timing class with current, local timing class:
        self.kwargs[GC.KWARGS_TIMING] = self.timing

        # Get all the TestSteps for the global loop, that are kept within this TestCase:
        lTestStepClasses = {}
        for testStepSequenceNumer, testStep in enumerate(self.testSteps.keys(), start=1):
            if self.testSteps[testStep][0]["TestStepClass"]:
                lTestStepClasses[testStepSequenceNumer] = self.testSteps[testStep][0]["TestStepClass"]

        try:
            self.testRunInstance.executeDictSequenceOfClasses(lTestStepClasses, GC.STRUCTURE_TESTSTEP, **self.kwargs)
        except baangtTestStepException as e:
            self.kwargs[GC.KWARGS_DATA][GC.TESTCASEERRORLOG] += '\n' + "Exception-Text: " + str(e)
            self.kwargs[GC.KWARGS_DATA][GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
        finally:
            self._finalizeTestCase()
            # Switch back to global Timing class:
            self.kwargs[GC.KWARGS_TIMING] = lTestRunTiming

    def _finalizeTestCase(self):
        tcData = self.kwargs[GC.KWARGS_DATA]
        tcData[GC.TIMING_DURATION] = self.timing.takeTime(self.timingName)  # Write the End-Record for this Testcase

        tcData[GC.TIMELOG] = self.timing.returnTime()
        self.timing.resetTime(self.timingName)

    def _checkAndSetTestcaseStatusIfFailExpected(self):
        """
        If this Testcase is supposed to fail and failed, he's actually successful.
        If this Testcase is supposed to fail and doesn't, he's actually failed.
        @return: Directly sets the Testcasestatus accordingly.
        """
        tcData = self.kwargs[GC.KWARGS_DATA]

        if tcData.get(GC.TESTCASE_EXPECTED_ERROR_FIELD) == 'X':
            if tcData[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_ERROR:
                tcData[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_SUCCESS
            elif tcData[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_SUCCESS:
                tcData[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR

    def tearDown(self):

        data = self.kwargs[GC.KWARGS_DATA]

        # If TestcaseErrorlog is not empty, the testcase status should be error.
        if data[GC.TESTCASEERRORLOG]:
            data[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR

        if self.kwargs[GC.KWARGS_DATA][GC.TESTCASESTATUS] == GC.TESTCASESTATUS_ERROR:
            # Try taking a Screenshot
            if self.testCaseType == GC.KWARGS_BROWSER:
                lShot = self.browser.takeScreenshot()
                if lShot:    # Otherwise browser was already closed. Nothing we can do...
                    lShot = lShot.strip()
                    if data[GC.SCREENSHOTS]:
                        if isinstance(data[GC.SCREENSHOTS], str):
                            # From where does this come, damn it?!
                            data[GC.SCREENSHOTS] = [lShot, data[GC.SCREENSHOTS]]
                            pass
                        else:
                            data[GC.SCREENSHOTS].extend([lShot])
                    else:
                        data[GC.SCREENSHOTS] = [lShot]

        # If Testcase-Status was not set, we'll set error. Shouldn't happen anyways.
        if not self.kwargs[GC.KWARGS_DATA][GC.TESTCASESTATUS]:
            data[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
            data[GC.TESTCASEERRORLOG] += "\nTestcase had not status - setting error"
            logger.critical("Testcase had no status - setting error")

        self._checkAndSetTestcaseStatusIfFailExpected()

        if data[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_SUCCESS:
            self.statistic.update_success()
        elif data[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_ERROR:
            self.statistic.update_error()
        elif data[GC.TESTCASESTATUS] == GC.TESTCASESTATUS_WAITING:
            self.statistic.update_waiting()

        logger.info(
            f"Testcase {self.kwargs.get(GC.STRUCTURE_TESTSTEP, '')} finished with status: {data[GC.TESTCASESTATUS]}")
