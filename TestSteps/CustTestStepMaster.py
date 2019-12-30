import pyFETest.GlobalConstants as GC
import pyFETest.CustGlobalConstants as CGC
from TestSteps.TestStepMaster import TestStepMaster


class CustTestStepMaster(TestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def teardown(self):
        super().teardown()
        toasts, error_toasts = self.browserSession.getToastsAsString()
        if len(toasts) > 0:
            self.testcaseDataDict[CGC.CUST_TOASTS] = self.testcaseDataDict[CGC.CUST_TOASTS] + '\n' + toasts
        if len(error_toasts) > 0:
            self.testcaseDataDict[CGC.CUST_TOASTS_ERROR] = \
                self.testcaseDataDict[CGC.CUST_TOASTS_ERROR] + '\n' + error_toasts
