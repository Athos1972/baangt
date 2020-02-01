from baangt import spec
from baangt import pm


class TestRunHookSpec:
    @spec
    def initTestRun(self, testRunObject, testRunName, globalSettingsFileNameAndPath):
        pass

    @spec
    def tearDown(self, testRunObject):
        pass

    @spec
    def getSuccessAndError(self, testRunObject):
        pass

    @spec
    def getAllTestRunAttributes(self, testRunObject):
        pass

    @spec
    def getBrowser(self, testRunObject, browserInstance=1, browserName=None, browserAttributes=None):
        pass

    @spec
    def _getBrowserInstance(self, testRunObject, browserInstance):
        pass

    @spec
    def getAPI(self, testRunObject):
        pass

    @spec
    def setResult(self, testRunObject, recordNumber, dataRecordResult):
        pass

    @spec
    def executeTestRun(self, testRunObject):
        pass

    @spec
    def executeDictSequenceOfClasses(self, testRunObject, dictSequenceOfClasses, counterName, **kwargs):
        pass

    @spec
    def _initTestRun(self, testRunObject):
        pass

    @spec
    def loadJSONGlobals(self, testRunObject):
        pass

    @spec
    def _loadJSONTestRunDefinitions(self, testRunObject):
        pass

    @spec
    def _loadExcelTestRunDefinitions(self, testRunObject):
        pass

    @spec
    def __dynamicImportClasses(self, fullQualifiedImportName):
        pass

    @spec
    def _sanitizeTestRunNameAndFileName(self, TestRunNameInput):
        pass


pm.add_hookspecs(TestRunHookSpec)
