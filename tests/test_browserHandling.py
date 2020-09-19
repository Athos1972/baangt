import pytest
import platform
from baangt.base import GlobalConstants as GC
from baangt.base.BrowserHandling.BrowserHandling import BrowserDriver
from unittest.mock import patch, MagicMock


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
    from baangt.base.BrowserHandling.WebdriverFunctions import WebdriverFunctions
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
    getdriver.browserData.driver.window_handles = ["test"]
    getdriver.handleWindow(function=function)
    assert 1 == 1

