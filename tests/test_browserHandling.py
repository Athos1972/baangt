import pytest
import platform
from baangt.base import GlobalConstants as GC
from baangt.base.BrowserHandling.BrowserHandling import BrowserDriver
from unittest.mock import patch, MagicMock
from baangt.TestSteps.Exceptions import baangtTestStepException
from baangt.base.BrowserHandling.WebdriverFunctions import WebdriverFunctions
from baangt.base.Utils import utils


browserName = "FIREFOX"
desired_app = [{GC.MOBILE_PLATFORM_NAME: "Android"}, {GC.MOBILE_PLATFORM_NAME: "iOS"}]
mobileApp = ["True", "False"]
mobile_app_setting = {
    GC.MOBILE_APP_URL: "test",
    GC.MOBILE_APP_PACKAGE: "com.baangt.pytest",
    GC.MOBILE_APP_ACTIVITY: "baangt.test",
    GC.MOBILE_APP_BROWSER_PATH: "temp"
}


@pytest.fixture
def getdriver():
    """ This will return BrowserDriver instance
        for below test function
    """
    return BrowserDriver()


def test_setZoomFactor(getdriver):
    """ check if png file created in path """
    # create browser

    from baangt.base import GlobalConstants as GC
    getdriver.createNewBrowser()
    getdriver.goToUrl("https://www.baangt.org")
    # FInd element by class
    getdriver.zoomFactorDesired = True
    getdriver.setZoomFactor(lZoomFactor=200)

    # TODO add check

    getdriver.closeBrowser()
    assert not getdriver.browserData.driver


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows Test only")
@pytest.mark.parametrize(("driverName", "browserName"),
                         [("geckodriver.exe", GC.BROWSER_FIREFOX), ("chromedriver.exe", GC.BROWSER_CHROME)])
def test_downloadDriver_windows(getdriver, driverName, browserName):
    from pathlib import Path
    import os
    from baangt.base.PathManagement import ManagedPaths

    # Get Remove Driver File
    path = ManagedPaths().getOrSetDriverPath()
    fileName = Path(path).joinpath(driverName)
    try:
        os.remove(fileName)
    except:
        pass
    assert not os.path.isfile(fileName)

    # create browser
    getdriver.downloadDriver(browserName)
    assert os.path.isfile(fileName)


@pytest.mark.skipif(platform.system() == "Windows", reason="Test for Linux and Mac")
@pytest.mark.parametrize(("driverName", "browserName"),
                         [("geckodriver", GC.BROWSER_FIREFOX), ("chromedriver", GC.BROWSER_CHROME)])
def test_downloadDriver_NonWindows(getdriver, driverName, browserName):
    from pathlib import Path
    import os
    from baangt.base.PathManagement import ManagedPaths

    # Get Remove Driver File
    path = ManagedPaths().getOrSetDriverPath()
    fileName = Path(path).joinpath(driverName)
    try:
        os.remove(fileName)
    except:
        pass
    assert not os.path.isfile(fileName)

    # create browser
    getdriver.downloadDriver(browserName)
    assert os.path.isfile(fileName)


def test_findBy_class(getdriver):
    """ check if png file created in path """
    # create browser

    from baangt.base import GlobalConstants as GC
    getdriver.createNewBrowser()  # (mobileType = 'True', desired_app = desired_app)
    getdriver.goToUrl("https://www.baangt.org")
    # FInd element by class
    element, html = getdriver.findBy(class_name="et_pb_menu__wrap", timeout=20, optional=False)

    assert element is not None
    assert html is not None

    getdriver.closeBrowser()
    assert not getdriver.browserData.driver


def test_findBy_id(getdriver):
    """ check if png file created in path """
    # create browser
    getdriver.createNewBrowser()
    getdriver.goToUrl("https://www.baangt.org/contact/")

    # FInd element by id
    element, html = getdriver.findBy(id="et_pb_contact_name_0", timeout=20, optional=False)

    assert "input" == element.tag_name
    assert "html" == html.tag_name

    getdriver.closeBrowser()
    assert not getdriver.browserData.driver


def test_findByAndClick(getdriver):
    """ check if png file created in path """
    # create browser
    getdriver.createNewBrowser()
    getdriver.goToUrl("https://www.baangt.com")
    # FInd element by xpath
    result = getdriver.findByAndClick(xpath="//a[text()='Uncategorized']", timeout=20, optional=False)

    # the file name should  exist
    assert result == True

    getdriver.closeBrowser()
    assert not getdriver.browserData.driver


def test_slowExecutionToggle(getdriver):
    """ Test slowExecution Function """
    oldstate = getdriver.slowExecution
    # toggle
    newstate = getdriver.slowExecutionToggle()

    assert newstate != oldstate


def test_takeScreenshot_exception(getdriver):
    """
    Test takeScreenshot method
    """
    filename = getdriver.takeScreenshot()
    import os
    # the file name should not exist
    assert not filename


def test_takeScreenshot_filecheck(getdriver):
    """ check if png file created in path """
    # create browser
    getdriver.createNewBrowser()
    # take screenshot
    getdriver.goToUrl("http://www.google.com")
    filename = getdriver.takeScreenshot()
    import os
    # the file name should  exist
    assert os.path.isfile(filename)

    getdriver.closeBrowser()
    assert not getdriver.browserData.driver


def test_setBrowserWindowSizeEmpty(getdriver):
    getdriver.createNewBrowser()
    result = getdriver.setBrowserWindowSize(browserWindowSize="")
    getdriver.closeBrowser()

    assert result == False


@pytest.mark.skipif(platform.system() == "Linux", reason="FF on Linux doesn't resize")
def test_setBrowserWindowSizeReal(getdriver):
    getdriver.createNewBrowser()
    result = getdriver.setBrowserWindowSize("800;600")
    getdriver.closeBrowser()

    assert result["width"] > 750
    assert result["width"] < 850
    assert result["height"] > 550
    assert result["height"] < 650


def test_setBrowserWindowSizeWrong(getdriver):
    getdriver.createNewBrowser()
    result = getdriver.setBrowserWindowSize("1234°1231")
    getdriver.closeBrowser()
    assert result == False


def test_setBrowserWindowSizeWithLeadingStuff(getdriver):
    getdriver.createNewBrowser()
    result = getdriver.setBrowserWindowSize("--800,--600")
    getdriver.closeBrowser()
    assert isinstance(result, dict)


def test_setBrowserWindowSizeWithX(getdriver):
    getdriver.createNewBrowser()
    result = getdriver.setBrowserWindowSize("--800x600")
    getdriver.closeBrowser()
    assert isinstance(result, dict)


@pytest.mark.parametrize(
    "browserName, desired_app, mobileApp, mobile_app_setting",
    [
        (browserName, desired_app[0], mobileApp[0], mobile_app_setting),
        (browserName, desired_app[0], mobileApp[1], mobile_app_setting),
        (browserName, desired_app[1], mobileApp[0], mobile_app_setting),
        (browserName, desired_app[1], mobileApp[1], mobile_app_setting)
    ]
)
def test_mobileConnectAppium(browserName, desired_app, mobileApp, mobile_app_setting):
    wdf = WebdriverFunctions
    with patch.dict(wdf.BROWSER_DRIVERS, {GC.BROWSER_APPIUM: MagicMock}):
        BrowserDriver._mobileConnectAppium(browserName, desired_app, mobileApp, mobile_app_setting)
    assert 1 == 1


def test_handleIframe(getdriver):
    getdriver.browserData = MagicMock()
    getdriver.handleIframe("test")
    assert 1 == 1
    getdriver.iFrame = "test"
    getdriver.handleIframe()
    assert 1 == 1


def test_checkLinks(getdriver):
    getdriver.browserData = MagicMock()
    getdriver.browserData.driver.find_elements_by_css_selector.return_value = [MagicMock()]
    getdriver.checkLinks()
    assert 1 == 1


def test_waitForPageLoadAfterButtonClick(getdriver):
    getdriver.browserData = MagicMock()
    getdriver.html = "test"
    getdriver.waitForPageLoadAfterButtonClick()
    assert 1 == 1


@pytest.mark.parametrize("function", [("close"), ("closeall-0"), ("")])
def test_handleWindow(function, getdriver):
    getdriver.browserData = MagicMock()
    getdriver.browserData.driver.window_handles = ["test", "test"]
    if function == "":
        with pytest.raises(baangtTestStepException):
            getdriver.handleWindow(function=function)
        getdriver.refresh()
    else:
        getdriver.handleWindow(function=function)
    assert 1 == 1


def test_findNewFiles(getdriver):
    from baangt.base.DownloadFolderMonitoring import DownloadFolderMonitoring
    getdriver.downloadFolderMonitoring = DownloadFolderMonitoring(getdriver.downloadFolder)
    result = getdriver.findNewFiles()
    assert type(result) == list


def test_getURL(getdriver):
    result = getdriver.getURL()
    assert result


@pytest.mark.parametrize("css, xpath, id", [("test", None, None), (None, "test", None), (None, None, "test")])
def test_findWaitNotVisible(css, xpath, id, getdriver):
    getdriver.browserData = MagicMock()
    result = getdriver.findWaitNotVisible(css, xpath, id)
    assert type(result) == bool


@pytest.mark.parametrize("browser", ["firefox", "chrome"])
def test_createNewBrowser(browser, getdriver):
    with patch.dict(WebdriverFunctions.BROWSER_DRIVERS, {GC.BROWSER_REMOTE: MagicMock}):
        getdriver.createNewBrowser(browserName="REMOTE_V4", desiredCapabilities={"browserName": browser})
    assert 1 == 1


@patch.object(utils, "setLocatorFromLocatorType")
def test_waitForElementChangeAfterButtonClick(mock_utils, getdriver):
    mock_utils.return_value = (1, 2, 3)
    getdriver.findBy = MagicMock()
    id = MagicMock()
    getdriver.findBy.return_value = (id, '1234')
    getdriver.element = MagicMock()
    getdriver.element.id = "xxxx"
    id.id = "1234"
    getdriver.waitForElementChangeAfterButtonClick(timeout=0.1)
    assert 1 == 1


@pytest.mark.parametrize("css, xpath, id", [("x", None, None), (None, "x", None), (None, None, "x")])
def test_findWaitNotVisible(css, xpath, id, getdriver):
    getdriver.browserData = MagicMock()
    getdriver.findWaitNotVisible(css, xpath, id, timeout=1)
    assert 1 == 1


def test_findByAndForceViaJS(getdriver):
    getdriver.browserData = MagicMock()
    getdriver.findByAndForceViaJS(xpath="Test")
    assert 1 == 1


def test_findByAndForceText(getdriver):
    getdriver.findBy = MagicMock()
    getdriver.findBy.return_value = False, True
    getdriver.findByAndForceText()
    assert 1 == 1


def test_findByAndSetTextValidated(getdriver):
    getdriver.findBy = MagicMock()
    getdriver.findByAndForceText = MagicMock()
    getdriver.findBy.return_value = MagicMock(), "def"
    getdriver.findBy.return_value[0].text = "abc"
    getdriver.findBy.return_value[0].get_property.return_value = "abc"
    getdriver.findByAndSetTextValidated(value="123")