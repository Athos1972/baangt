from baangt.CustTestRun import CustTestRun as TestRun
from baangt import GlobalConstants as GC
from TestSteps import Exceptions
from TestSteps.Frontend.Portal.Login import Login
from TestSteps.Frontend.Partner.PartnerURL import PartnerURL
from TestSteps.Frontend.Partner.PartnerCreate import PartnerCreate

import logging

if __name__ == '__main__':
    #l_testRun = TestRun("Heartbeat")
    l_testRun = TestRun("Partner")
    BrowserInterface = l_testRun.getBrowser()
    l_first = True
    (l_record, l_count) = l_testRun.getNextRecord()

    while l_record:
        try:
            kwargs = {GC.KWARGS_DATA: l_record,
                      GC.KWARGS_BROWSER: BrowserInterface}
            PartnerURL(**kwargs)
            Login(**kwargs)
            PartnerCreate(**kwargs)
        except Exceptions.baangtTestStepException as e:
            BrowserInterface._BrowserDriver__log(logging.CRITICAL, "Unhandled Error happened: " + str(e))
            l_record[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
            pass
        finally:
            BrowserInterface.handleWindow(0, "close")
            l_testRun.finishTestCase()
            BrowserInterface._BrowserDriver__log(logging.INFO, f"Setting Status {l_record[GC.TESTCASESTATUS]} on Testcase {l_count}")
            (l_record, l_count) = l_testRun.getNextRecord()

    l_testRun.tearDown()