from baangt.CustTestRun import TestRun
from baangt import GlobalConstants as GC
from TestSteps import Exceptions
from TestSteps.DropsApp.Login_API import Login_API

if __name__ == '__main__':
    #l_testRun = TestRun("WSTV-Single")
    l_testRun = TestRun("API-DROPS")
    ApiInterface = l_testRun.getAPI()
    (l_record, l_count) = l_testRun.getNextRecord()

    while l_record:
        kwargs = {GC.KWARGS_DATA: l_record,
                  GC.KWARGS_API_SESSION: ApiInterface}
        Login_API(**kwargs)
        l_testRun.finishTestCase()
        (l_record, l_count) = l_testRun.getNextRecord()

    l_testRun.tearDown()
