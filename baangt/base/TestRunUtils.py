import baangt.base.GlobalConstants as GC

class TestRunUtils():
    def __init__(self):
        self.testRunAttributes = {}

    def setCompleteTestRunAttributes(self, testRunName:str, testRunAttributes: dict):
        self.testRunAttributes[testRunName] = testRunAttributes

    def getCompleteTestRunAttributes(self, testRunName):
        return self.testRunAttributes[testRunName][GC.KWARGS_TESTRUNATTRIBUTES]

    def getSequenceByNumber(self, sequence, testRunName):
        return self.testRunAttributes[testRunName][GC.KWARGS_TESTRUNATTRIBUTES][GC.STRUCTURE_TESTCASESEQUENCE].get(sequence)

    def getTestCaseByNumber(self, sequence, testcaseNumber):
        return sequence[1][GC.STRUCTURE_TESTCASE][testcaseNumber]

    def getTestStepByNumber(self, testCase, testStepNumber):
        return testCase[2][GC.STRUCTURE_TESTSTEP].get(testStepNumber)
