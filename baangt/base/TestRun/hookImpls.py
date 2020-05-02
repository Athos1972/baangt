import baangt

from baangt.base.TestRun.TestRun import TestRun


class TestRunHookImpl(object):

    @baangt.hook_impl
    def testRun_init(self, testRunName, globalSettingsFileNameAndPath):
        return TestRun(testRunName=testRunName, globalSettingsFileNameAndPath=globalSettingsFileNameAndPath)

    @baangt.hook_impl
    def testRun_tearDown(self, testRunObject):
        return testRunObject.tearDown()

    @baangt.hook_impl
    def testRun_getSuccessAndError(self, testRunObject):
        return testRunObject.testRun_getSuccessAndError()

    @baangt.hook_impl
    def testRun_getAllTestRunAttributes(self, testRunObject):
        return testRunObject.getAllTestRunAttributes()

    @baangt.hook_impl
    def testRun_getBrowser(self, testRunObject, browserInstance=1, browserName=None, browserAttributes=None):
        return testRunObject.getBrowser(browserInstance, browserName, browserAttributes)

    @baangt.hook_impl
    def testRun_getAPI(self, testRunObject):
        return testRunObject._getAPI()

    @baangt.hook_impl
    def testRun_setResult(self, testRunObject, recordNumber, dataRecordResult):
        return testRunObject.setResult(recordNumber, dataRecordResult)

    @baangt.hook_impl
    def testRun_executeTestRun(self, testRunObject):
        return testRunObject.executeTestSequence()

    @baangt.hook_impl
    def testRun_executeDictSequenceOfClasses(self, testRunObject, dictSequenceOfClasses, counterName, **kwargs):
        return testRunObject.executeDictSequenceOfClasses(dictSequenceOfClasses, counterName, **kwargs)

    @baangt.hook_impl
    def testRun_loadJSONGlobals(self, testRunObject):
        return testRunObject._loadJSONGlobals()




