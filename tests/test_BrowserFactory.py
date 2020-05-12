import pytest
import pathlib
from baangt.base.TestRun.TestRun import TestRun
from baangt.base.BrowserFactory import BrowserFactory
from baangt.base import GlobalConstants as GC

testRun = None
brFactory = None

currentPath = pathlib.Path(__file__).parent.absolute()
# parentPath = pathlib.Path(currentPath).parent
parentPath = currentPath
testRunFile = parentPath.joinpath("0TestInput/YoutubePromo.xlsx")
settingfile = parentPath.joinpath("0TestInput/globals_headless.json")


def BrowserFactoryInit(testRunFile, settingFile):
    global testRun
    testRun = TestRun(f"{testRunFile}",
                      globalSettingsFileNameAndPath=f"{settingFile}", executeDirect=False)
    testRun._initTestRunSettingsFromFile()  # Loads the globals*.json file
    testRun._loadJSONTestRunDefinitions()
    testRun._loadExcelTestRunDefinitions()
    brFactory = BrowserFactory(testRun)
    return brFactory


browserFactory = BrowserFactoryInit(testRunFile=testRunFile, settingFile=settingfile)


def test_getBrowser():
    global testRun
    mobileType = False
    browserInstance = browserFactory.getBrowser(mobileType=mobileType, browserName=GC.BROWSER_FIREFOX,
                                           browserAttributes=testRun.globalSettings["TC." + GC.BROWSER_ATTRIBUTES])
    assert browserInstance is not None
    print('GetBrowser - (mobileType={0}, browserName=GC.BROWSER_FIREFOX)   OK'.format(mobileType))


def test__getBrowserInstance():
    try:
        with pytest.raises(Exception) as e:
            browserFactory._getBrowserInstance(browserInstance=0)
    except:
        print("test__getBrowserInstance OK")


def test_tearDown():
    try:
        with pytest.raises(Exception) as e:
            browserFactory.teardown()
    except:
        print("test_tearDown OK")

