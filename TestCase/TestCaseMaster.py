from baangt import GlobalConstants as GC
from TestSteps.Exceptions import *

class TestCaseMaster:
    def __init__(self, **kwargs):
        self.name = None
        self.description = None
        self.testSteps = {}
        self.apiInstance = None
        self.numberOfParallelRuns = None
        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.testCaseSettings = kwargs.get(GC.STRUCTURE_TESTCASESEQUENCE)[GC.STRUCTURE_TESTCASE].get(kwargs.get(GC.STRUCTURE_TESTCASE))
        self.testSteps = self.testCaseSettings[2][GC.STRUCTURE_TESTSTEP]
        self.testCaseType = self.testCaseSettings[1][GC.KWARGS_TESTCASETYPE]
        self.kwargs = kwargs
        self.timing = self.kwargs.get(GC.KWARGS_TIMING)
        if self.testCaseType == GC.KWARGS_BROWSER:
            if self.kwargs.get(GC.KWARGS_BROWSER):
                self.browser = self.kwargs[GC.KWARGS_BROWSER]
                pass # Browser already set - most probably from parallel run
            else:
                self.browserType = self.testCaseSettings[1][GC.KWARGS_BROWSER]
                self.browserSettings = self.testCaseSettings[1]["BROWSER_ATTRIBUTES"]
                self.browser = self.testRunInstance.getBrowser(browserName=self.browserType,
                                                               browserAttributes=self.browserSettings)
                self.kwargs[GC.KWARGS_BROWSER] = self.browser
        elif self.testCaseType == GC.KWARGS_API_SESSION:
            self.apiInstance = self.testRunInstance.getAPI()
        self.execute()

    def execute(self):
        try:
            self.testRunInstance.executeDictSequenceOfClasses(self.testSteps, GC.STRUCTURE_TESTSTEP, **self.kwargs)
        except baangtTestStepException as e:
            logger.info(f"Testcase {self.kwargs.get(GC.STRUCTURE_TESTSTEP,'')} failed")
            self.kwargs[GC.KWARGS_DATA][GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
        finally:
            self.kwargs[GC.KWARGS_DATA][GC.TIMELOG] = self.browser.returnTime()
            self.kwargs[GC.KWARGS_TIMING].resetTime()

    def tearDown(self):
        pass