from baangt.TestSteps.TestStepMaster import TestStepMaster
from baangt.base.Timing.Timing import Timing
import pytest
from unittest.mock import patch, MagicMock


class FakeTestRun:
    def __init__(self):
        self.testRunName = ""
        self.testRunUtils = MagicMock()
        self.globalSettings = {}


@pytest.fixture(scope="module")
def testStepMaster():
    return TestStepMaster(TimingClassInstance=Timing(), TESTRUNINSTANCE=FakeTestRun(), data={})


@pytest.mark.parametrize("lComparison, value1, value2",[("=", True, True), ("=", "True", "None"), ("!=", True, True),
    ("!=", True, "None"), (">", 1, 2), (">", 2, 1), ("<", 1, 2), ("<", 2, 1), (">=", 1, 2), (">=", 2, 1), ("<=", 1, 2),
    ("<=", 2, 1), ("!!", True, True), (None, True, True)])
def test_doComparison(lComparison, value1, value2, testStepMaster):
    if lComparison != "!!":
        result = testStepMaster._TestStepMaster__doComparisons(lComparison, value1, value2)
        assert type(result) == bool
    else:
        with pytest.raises(BaseException):
            testStepMaster._TestStepMaster__doComparisons(lComparison, value1, value2)
        assert 1 == 1


@pytest.mark.parametrize("command, locator", [("SETTEXTIF", ""), ("FORCETEXT", ""), ("FORCETEXTIF", ""), ("FORCETEXTJS", ""),
                                     ("SETANCHOR", ""), ("HANDLEIFRAME", ""), ("APIURL", ""), ("ENDPOINT", ""),
                                     ("POST", ""), ("GET", ""), ("HEADER", ""), ("SAVE", ""), ("CLEAR", ""),
                                     ("ADDRESS_CREATE", ""), ("ASSERT", ""), ("PDFCOMPARE", ""), ("CHECKLINKS", ""),
                                     ("ZZ_", ""), ("TCStopTestCase".upper(), ""), ("TCStopTestCaseError".upper(), ""),
                                     ("SETANCHOR", "temp")])
def test_executeDirectSingle(command, locator, testStepMaster):
    if command == "SAVE":
        testStepMaster.doSaveData = MagicMock()
    testStepMaster.browserSession = MagicMock()
    testStepMaster.apiSession = MagicMock()
    testStepMaster.executeDirectSingle(0, {
        "Activity": command, "LocatorType": "", "Locator": locator, "Value": 'temp',
        "Value2": '', "Comparison": '', "Optional": '', 'Release': '', "Timeout": ''
    })
    assert 1 == 1