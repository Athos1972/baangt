import pytest
import os
from pathlib import Path
from baangt.base.TestRun.TestRun import TestRun


@pytest.fixture
def testrun_obj():
    """ This function return instance of TestRun object
        which will be used by other test methods
    """
    from baangt.base.TestRun.TestRun import TestRun
    return TestRun("SimpleTheInternet.xlsx", "globals.json", executeDirect=False)


def test_with_globalsHeadless(testrun_obj):
    lTestRun = TestRun("SimpleTheInternet.xlsx",
                       globalSettingsFileNameAndPath= \
                           Path(os.getcwd()).joinpath("jsons").joinpath("globals_headless.json"),
                       executeDirect=False)
    lTestRun._initTestRunSettingsFromFile()

    assert lTestRun.globalSettings["TC.BrowserAttributes"]
    assert isinstance(lTestRun.globalSettings["TC.BrowserAttributes"], dict)


def test_with_globalsHeadlessVersion2(testrun_obj):
    lTestRun = TestRun("SimpleTheInternet.xlsx",
                       globalSettingsFileNameAndPath= \
                           Path(os.getcwd()).joinpath("jsons").joinpath("globals_headless2.json"),
                       executeDirect=False)

    lTestRun._initTestRunSettingsFromFile()

    assert lTestRun.globalSettings["TC.BrowserAttributes"]
    assert isinstance(lTestRun.globalSettings["TC.BrowserAttributes"], str)

def tests_with_fullGlobalsFile(testrun_obj):
    lTestRun = TestRun("SimpleTheInternet.xlsx",
                       globalSettingsFileNameAndPath= \
                           Path(os.getcwd()).joinpath("jsons").joinpath("globalsFullExample.json"),
                       executeDirect=False)

    lTestRun._initTestRunSettingsFromFile()

    assert not lTestRun.globalSettings["TC.Lines"]
    assert lTestRun.globalSettings["TX.DEBUG"] == True            # Was converted from string "True" to boolean True
    assert lTestRun.globalSettings["TC.RestartBrowser"] == False  # Was converted from string "False" to boolean False
    assert lTestRun.globalSettings["TC.NetworkInfo"] == True      # Was converted from string "X" to boolean True
    assert lTestRun.globalSettings["CL.browserFactory"] == 'zzbaangt.base.BrowserFactory.BrowserFactory'
    assert lTestRun.classesForObjects.browserFactory == 'zzbaangt.base.BrowserFactory.BrowserFactory'

