import TestSteps.Exceptions
import TestSteps.CustGlobalConstants as GC

class TestStepMaster:
    def __init__(self, testcaseDataDict, browserSession):
        self.testcaseDataDict = testcaseDataDict
        self.browserSession = browserSession
        self.testCaseStatus = "Failed"
        pass

    def execute(self):
        """Method is overwritten in all children"""
        pass

