from baangt.base.ApiHandling import ApiHandling
from baangt.TestSteps.TestStepMaster import TestStepMaster
import baangt.base.GlobalConstants as GC


class Login_API(TestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()

    def execute(self):
        lUrl = self.testcaseDataDict["baseURL"]
        session : ApiHandling = self.apiSession
        content = {"username": self.testcaseDataDict["Username"],
                   "password": self.testcaseDataDict["Password"]}
        resultStatus, resultDict, resultHeader = session.postURL(url=lUrl, content=content)

        self.testcaseDataDict["resultStatus"] = resultStatus
        self.testcaseDataDict["resultDict"] = resultDict
        self.testcaseDataDict["resultHeader"] = resultHeader

        self.testcaseDataDict[GC.TESTCASESTATUS] = session.returnTestCaseStatus(resultStatus)
