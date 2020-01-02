import baangt.GlobalConstants as GC
import sys


class TestStepMaster:
    def __init__(self, **kwargs):
        self.testcaseDataDict = kwargs.get(GC.KWARGS_DATA)
        self.browserSession = kwargs.get(GC.KWARGS_BROWSER)
        self.apiSession = kwargs.get(GC.KWARGS_API_SESSION)
        self.testCaseStatus = None

    def execute(self):
        """Method is overwritten in all children"""
        pass

    def teardown(self):
        if self.testCaseStatus:
            if not self.testcaseDataDict[GC.TESTCASESTATUS]:
                self.testcaseDataDict[GC.TESTCASESTATUS] = self.testCaseStatus
            elif self.testCaseStatus == GC.TESTCASESTATUS_SUCCESS:
                # We'll not overwrite a potential Error Status of the testcase
                pass
            elif self.testCaseStatus == GC.TESTCASESTATUS_ERROR:
                self.testcaseDataDict = GC.TESTCASESTATUS_ERROR
            else:
                sys.exit("No idea, what happened here. Unknown condition appeared")