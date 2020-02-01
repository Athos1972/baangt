from baangt import impl
from baangt import pm

from baangt.base.TestRun.TestRun import TestRun
from baangt.base.Timing import Timing
from baangt.base.TestRunUtils import TestRunUtils
from baangt.base import GlobalConstants as GC


class TestRunHookImpl:
    @impl
    def initTestRun(self, testRunObject, testRunName, globalSettingsFileNameAndPath):
        testRunObject.browser = {}
        testRunObject.apiInstance = None
        testRunObject.testType = None
        testRunObject.kwargs = {}
        testRunObject.dataRecords = {}
        testRunObject.globalSettingsFileNameAndPath = globalSettingsFileNameAndPath
        testRunObject.globalSettings = {}
        testRunObject.testRunName, testRunObject.testRunFileName = \
            TestRun._sanitizeTestRunNameAndFileName(testRunName)
        testRunObject.timing = Timing()
        testRunObject.timing.takeTime(GC.TIMING_TESTRUN)  # Initialize Testrun Duration
        testRunObject.testRunUtils = TestRunUtils()
        testRunObject._initTestRun()
        testRunObject._loadJSONTestRunDefinitions()
        testRunObject._loadExcelTestRunDefinitions()
        testRunObject.executeTestRun()
        testRunObject.tearDown()


pm.register(TestRunHookImpl())
