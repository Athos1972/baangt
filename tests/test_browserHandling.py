import pytest
from baangt.base import GlobalConstants as GC


@pytest.fixture
def getdriver():
    """ This will return BrowserDriver instance
        for below test function
    """
    from baangt.base.BrowserHandling.BrowserHandling import BrowserDriver
    return BrowserDriver()


def test_setZoomFactor(getdriver):
    """ check if png file created in path """
    # create browser

    from baangt.base import GlobalConstants as GC
    getdriver.createNewBrowser()
    getdriver.goToUrl("https://www.baangt.org")
    # FInd element by class
    getdriver.setZoomFactor(lZoomFactor = 200)

    # TODO add check

    getdriver.closeBrowser()
    assert not getdriver.browserData.driver


@pytest.mark.parametrize(("driverName", "browserName"), [("geckodriver", GC.BROWSER_FIREFOX), ("chromedriver", GC.BROWSER_CHROME)])
def test_downloadDriver(getdriver, driverName, browserName):
    """ check if png file created in path """
    from pathlib import Path
    import os
    from baangt.base.PathManagement import ManagedPaths

    # Get Remove Driver File
    path = ManagedPaths().getOrSetDriverPath()
    fileName = path.joinpath(driverName)
    try: 
        os.remove(fileName)
    except:
        pass
    assert False == os.path.isfile(fileName) 

    # create browser
    getdriver.downloadDriver(browserName)
    assert True == os.path.isfile(fileName) 


def test_findBy_class(getdriver):
    """ check if png file created in path """
    # create browser

    from baangt.base import GlobalConstants as GC
    getdriver.createNewBrowser()#(mobileType = 'True', desired_app = desired_app)
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
    assert not os.path.isfile(filename)


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
