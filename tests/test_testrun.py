import pytest
from unittest.mock import patch
from baangt.base.TestRun.TestRun import TestRun


class subprocess_communicate:
    def __init__(self, *stdout, **stderr):
        pass

    def communicate(self):
        return b"firefox\n", 1


@pytest.fixture
def testrun_obj():
    """ This function return instance of TestRun object
        which will be used by other test methods
    """
    return TestRun("examples/SimpleTheInternet.xlsx","globals.json", executeDirect=False)


def test_filenotfound():
    """ To check if function raises File not found Error """
    with pytest.raises(BaseException) as e:
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


@pytest.mark.parametrize("system, os_version", [
    ("Linux", ["redhat-release"]),
    ("Linux", ["debian_version"]),
    ("Darwin", ["firefox"]),
    ("Darwin", ["chrome"])
])
@patch("subprocess.Popen", subprocess_communicate)
@patch("os.listdir")
@patch("platform.system")
def test_ExcelImporter(mock_plat, mock_list, system, os_version):
    from baangt.base.TestRunExcelImporter import TestRunExcelImporter
    mock_plat.return_value = system
    mock_list.return_value = os_version
    TestRunExcelImporter.get_browser(TestRunExcelImporter)
    assert mock_plat.call_count > 0
    


