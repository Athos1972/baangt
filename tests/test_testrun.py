import pytest

@pytest.fixture
def testrun_obj():
    """ This function return instance of TestRun object
        which will be used by other test methods
    """
    from baangt.base.TestRun.TestRun import TestRun
    with pytest.raises(Exception) as e:
        return TestRun("SimpleTheInternet.xlsx","globals.json")



def test_filenotfound():
    """ To check if function raises File not found Error """
    with pytest.raises(Exception) as e:
        TestRun("SimpleTheInternet.xlsx","global.json")

def test_objectreturned(testrun_obj):
    """ Returns number of successful and number of error test cases of
         the current test run
    """
    from baangt.base.TestRun.TestRun import TestRun
    assert TestRun.__instancecheck__(testrun_obj)

def test_checkattribute(testrun_obj):
    """ check if has attribute """
    assert hasattr(testrun_obj, "getSuccessAndError")
    assert hasattr(testrun_obj, "setResult")


@pytest.mark.xfail(testrun_obj, reason="TestRun didn't return object")
def test_getSuccessAndError(testrun_obj):
    """ This function test getSuccessAndError method
        working or not
    """
    assert (0,1) == testrun_obj.getSuccessAndError()


@pytest.mark.xfail(testrun_obj, reason="TestRun didn't return object")
def test_setResult(testrun_obj):
    """ check setResult Function """
    # get the previous result
    old_result = testrun_obj.getSuccessAndError()
    testrun_obj.setResult(1,0)
    # check the result
    new_result = set(old_result[0]+1, old_result[1])
    assert new_result == testrun_obj.getSuccessAndError()
    


