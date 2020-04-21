# import pytest


# @pytest.fixture
# def getdriver():
#     """ This will return BrowserDriver instance
#         for below test function
#     """
#     from baangt.base.BrowserHandling import BrowserDriver
#     return BrowserDriver()

# def test_slowExecutionToggle(getdriver):
#     """ Test slowExecution Function """
#     oldstate = getdriver.slowExecution
#     # toggle
#     newstate = getdriver.slowExecutionToggle()

#     assert newstate != oldstate
    


# def test_takeScreenshot_exception(getdriver):
#     """ Test takeScreenshot method """
#     if not getdriver.driver:
#         with pytest.raises(Exception) as e:
#             filename = getdriver.takeScreenshot()

    

# def test_takeScreenshot_filecheck(getdriver):
#     """ check if png file created in path """
#     #create browser
#     b = getdriver.createNewBrowser()
#     #take screenshot
#     b.goToUrl("http://www.google.com")
#     filename = b.takeScreenshot() 
#     import os
#     #the file name should  exist
#     assert os.path.isfile(filename)
    
