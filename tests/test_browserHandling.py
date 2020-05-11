import pytest


@pytest.fixture
def getdriver():
    """ This will return BrowserDriver instance
        for below test function
    """
    from baangt.base.BrowserHandling.BrowserHandling import BrowserDriver
    return BrowserDriver()


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
    assert not getdriver.browserDriveroptions.driver


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
