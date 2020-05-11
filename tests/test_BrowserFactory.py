from baangt.base.TestRun.TestRun import TestRun
from baangt.base.BrowserFactory import BrowserFactory
from baangt.base import GlobalConstants as GC
import pytest
import pathlib


def BrowserFactoryInit(testRunFile, settingFile):
    testRun = TestRun(f"{testRunFile}",
                      globalSettingsFileNameAndPath=f"{settingFile}", executeDirect=False)
    brFactory = BrowserFactory(testRun)
    return brFactory


def test_getBrowser(mobileType, brFactory):
    browserInstance = brFactory.getBrowser(mobileType=mobileType, browserName=GC.BROWSER_FIREFOX)
    assert browserInstance is not None
    print('GetBrowser - (mobileType={0}, browserName=GC.BROWSER_FIREFOX)   OK'.format(mobileType))


def test__getBrowserInstance(browserInstance, brFactory):
    with pytest.raises(Exception) as e:
        brFactory._getBrowserInstance(browserInstance)


def test_tearDown(brFactory):
    with pytest.raises(Exception) as e:
        brFactory.teardown()


if __name__ == '__main__':
    currentPath = pathlib.Path(__file__).parent.absolute()
    parentPath = pathlib.Path(currentPath).parent
    testRunFile = parentPath.joinpath("examples/simpleAutomationpractice.xlsx")
    settingfile = parentPath.joinpath("examples/globals.json")
    browserFactory = BrowserFactoryInit(testRunFile=testRunFile, settingFile=settingfile)
    test_getBrowser(mobileType=False, brFactory=browserFactory)
    test_tearDown(browserFactory)
    test__getBrowserInstance(0, browserFactory)
