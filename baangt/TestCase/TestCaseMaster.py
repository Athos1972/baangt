from baangt.base import GlobalConstants as GC
from baangt.base.Timing import Timing
from baangt.TestSteps.Exceptions import *

class TestCaseMaster:
    def __init__(self, **kwargs):
        self.name = None
        self.description = None
        self.testSteps = {}
        self.apiInstance = None
        self.numberOfParallelRuns = None
        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.testRunUtils = self.testRunInstance.testRunUtils
        self.testSequence = self.testRunUtils.getSequenceByNumber(testRunName=self.testRunInstance.testRunName,
                                                                  sequence=kwargs.get(GC.STRUCTURE_TESTCASESEQUENCE))
        self.testCaseSettings = self.testRunUtils.getTestCaseByNumber(self.testSequence,
                                                                      kwargs.get(GC.STRUCTURE_TESTCASE))
        self.testSteps = self.testCaseSettings[2][GC.STRUCTURE_TESTSTEP]
        self.testCaseType = self.testCaseSettings[1][GC.KWARGS_TESTCASETYPE]
        self.kwargs = kwargs
        self.timing : Timing = self.kwargs.get(GC.KWARGS_TIMING)
        self.timingName = self.timing.takeTime(self.__class__.__name__, forceNew=True)
        if self.testCaseType == GC.KWARGS_BROWSER:
            if self.kwargs.get(GC.KWARGS_BROWSER):
                self.browser = self.kwargs[GC.KWARGS_BROWSER] # Browser already set - most probably from parallel run
            else:
                self.browserType = self.testCaseSettings[1][GC.KWARGS_BROWSER]
                self.browserSettings = self.testCaseSettings[1][GC.BROWSER_ATTRIBUTES]
                self.browser = self.testRunInstance.getBrowser(browserName=self.browserType,
                                                               browserAttributes=self.browserSettings)
                self.kwargs[GC.KWARGS_BROWSER] = self.browser
        elif self.testCaseType == GC.KWARGS_API_SESSION:
            self.apiInstance = self.testRunInstance.getAPI()
        self.execute()
        self.tearDown()

    def execute(self):
        try:
            self.testRunInstance.executeDictSequenceOfClasses(self.testSteps, GC.STRUCTURE_TESTSTEP, **self.kwargs)
        except baangtTestStepException as e:
            logger.info(f"Testcase {self.kwargs.get(GC.STRUCTURE_TESTSTEP,'')} failed")
            self.kwargs[GC.KWARGS_DATA][GC.TESTCASEERRORLOG] += '\n' + "Exception-Text: " + str(e)
            self.kwargs[GC.KWARGS_DATA][GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
        finally:
            self._finalizeTestCase()

    def _finalizeTestCase(self):
        tcData = self.kwargs[GC.KWARGS_DATA]
        tcData[GC.TIMELOG] = self.timing.returnTime()

        self.timing.resetTime()

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
        if self.kwargs[GC.KWARGS_DATA][GC.TESTCASESTATUS] == GC.TESTCASESTATUS_ERROR:
            # Try taking a Screenshot
            if self.testCaseType == GC.KWARGS_BROWSER:
                self.kwargs[GC.KWARGS_DATA][GC.SCREENSHOTS] = self.kwargs[GC.KWARGS_DATA][GC.SCREENSHOTS] + '\n' +\
                                                              self.browser.takeScreenshot()

        self._checkAndSetTestcaseStatusIfFailExpected()

        self.timing.takeTime(self.timingName)

