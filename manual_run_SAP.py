from pyFETest.TestRun import TestRun
from pyFETest import GlobalConstants as GC
from TestSteps import Exceptions
from TestSteps.SAPWebGui.Login.LoginURL import LoginURL
from TestSteps.SAPWebGui.Login.Login import Login
from TestSteps.SAPWebGui.PM0_ABC_FSPM.Auskunft import Auskunft
import logging

if __name__ == '__main__':
    l_testRun = TestRun("SAP")
    BrowserInterface = l_testRun.getBrowser()
    l_first = True
    (l_record, l_count) = l_testRun.getNextRecord()

    while l_record:
        try:
            kwargs = {GC.KWARGS_DATA: l_record,
                      GC.KWARGS_BROWSER: BrowserInterface}
            l_record[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_SUCCESS
            LoginURL(**kwargs)
            Login(**kwargs)
            Auskunft(**kwargs)

        except Exceptions.pyFETestException as e:
            BrowserInterface._BrowserDriver__log(logging.CRITICAL, "Unhandled Error happened: " + str(e))
            l_record[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
            pass
        finally:
            #BrowserInterface.handleWindow(0, "close")
            l_testRun.finishTestCase()
            BrowserInterface._BrowserDriver__log(logging.INFO, f"Setting Status {l_record[GC.TESTCASESTATUS]} on Testcase {l_count}")
            (l_record, l_count) = l_testRun.getNextRecord()

    l_testRun.tearDown()