import os
from selenium import webdriver
from appium import webdriver as Appiumwebdriver
#from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.chrome.options import Options as ChromeOptions
#from selenium.webdriver.firefox.options import Options as ffOptions
#from selenium.common.exceptions import *
#from selenium.webdriver.common import keys
from baangt.base import GlobalConstants as GC
from baangt.base.Timing.Timing import Timing
from baangt.TestSteps import Exceptions
from baangt.base.DownloadFolderMonitoring import DownloadFolderMonitoring
from baangt.base.Utils import utils
from baangt.base.ProxyRotate import ProxyRotate
import uuid
import time
import logging
from pathlib import Path
import json
import sys
import platform
import ctypes
from urllib.request import urlretrieve
import tarfile
import zipfile
import requests
from baangt.base.PathManagement import ManagedPaths


from baangt.base.BrowserHandling.WebdriverFunctions import WebdriverFunctions
from baangt.base.BrowserHandling.BrowserHelperFunction import BrowserDriverOptions
from baangt.base.BrowserHandling.BrowserHelperFunction import BrowserHelperFunction as helper


logger = logging.getLogger("pyC")



class BrowserDriver:
    """
    The main class for baangt-Elements to interact with a browser.
    Main Methods:
    - createNewBrowser: Create one instance of a Browser
    - findBy*-Methods: e.g. findByAndClick
    - URL-Methods: To navigate to an URL
    - handleIframe and handleWindow: To navigate between Windows (=tabs) and Iframes
    - javaScript: to pass JS directly to the browser
    - takeScreenshot: yes, that.
    """

    def __init__(self, timing=None, screenshotPath=None):
        self.iFrame = None
        self.element = None
        self.browserOptions = BrowserDriverOptions(locatorType=None, locator=None, driver=webdriver.firefox)
        self.slowExecution = False
        self.slowExecutionTimeoutInSeconds = 1
        self.downloadFolder = None
        self.downloadFolderMonitoring = None
        self.randomProxy = None
        self.zoomFactorDesired = None                     # Desired zoom factor for this page
        self.browserName = None
        # Reference to Selenium "HTML" in order to track page changes. It is set on every interaction with the page
        self.html = None
        self.managedPaths = ManagedPaths()

        if timing:
            self.timing = timing
        else:
            self.timing = Timing()

        self.takeTime = self.timing.takeTime

        self.screenshotPath = self.managedPaths.getOrSetScreenshotsPath()

    def createNewBrowser(self, mobileType=None, mobileApp = None, desired_app = None, mobile_app_setting = None,
                         browserName=GC.BROWSER_FIREFOX,
                         desiredCapabilities={}, randomProxy=None, **kwargs):
        """
        Will find the specified executables of the desired browser and start it with the given capabilities.

        @param browserName: one of GC_BROWSER_*-Browsernames, e.g. GC_BROWSER_FIREFOX
        @param desiredCapabilities: DICT of desiredCapabilities for this browser
        @param kwargs: Currently (Jan2020) not used
        """
        self.takeTime("Browser Start")
        self.randomProxy = randomProxy
        self.browserName = browserName
        browserNames = {
            GC.BROWSER_FIREFOX: webdriver.Firefox,
            GC.BROWSER_CHROME: webdriver.Chrome,
            GC.BROWSER_SAFARI: webdriver.Safari,
            GC.BROWSER_EDGE: webdriver.Edge,
            GC.BROWSER_REMOTE: webdriver.Remote}


        ChromeExecutable, GeckoExecutable = helper.browserHelper_getBrowserExecutableNames()



        lCurPath = Path(self.managedPaths.getOrSetDriverPath())

        if browserName in browserNames:

            browserProxy = kwargs.get('browserProxy')
            browserInstance = kwargs.get('browserInstance', 'unknown')

            if browserName == GC.BROWSER_FIREFOX:
                lCurPath = lCurPath.joinpath(GeckoExecutable)

                if mobileType == 'True':
                    self.mobileConnectAppium(GeckoExecutable, browserName, desired_app, lCurPath, mobileApp, mobile_app_setting)
                else:
                    if not (os.path.isfile(str(lCurPath))):
                        self.downloadDriver(browserName)

                    profile = webdriver.FirefoxProfile()
                    profile = WebdriverFunctions.webdriver_setFirefoxProfile(browserProxy, profile, self.randomProxy)
                    logger.debug(f"Firefox Profile as follows:{profile.userPrefs}")

                    self.browserOptions.driver = browserNames[browserName](
                        options = WebdriverFunctions.webdriver_createBrowserOptions(browserName=browserName,
                                                            desiredCapabilities=desiredCapabilities),
                        executable_path = helper.browserHelper_findBrowserDriverPaths(GeckoExecutable),
                        firefox_profile = profile,
                        service_log_path = os.path.join(self.managedPaths.getLogfilePath(), 'geckodriver.log')
                        # ,
                        # log_path=os.path.join(self.managedPaths.getLogfilePath(),'firefox.log')
                    )
                    helper.browserHelper_startBrowsermobProxy(browserName=browserName, browserInstance=browserInstance,
                                                browserProxy=browserProxy)

            elif browserName == GC.BROWSER_CHROME:
                lCurPath = lCurPath.joinpath(ChromeExecutable)

                if mobileType == 'True':
                    self.mobileConnectAppium(ChromeExecutable, browserName, desired_app, mobileApp, mobile_app_setting)
                else:

                    if not (os.path.isfile(str(lCurPath))):
                        self.downloadDriver(browserName)

                    self.browserOptions.driver = browserNames[browserName](
                        chrome_options = WebdriverFunctions.webdriver_createBrowserOptions(browserName=browserName,
                                                                   desiredCapabilities=desiredCapabilities,
                                                                   browserMobProxy=browserProxy,
                                                                   randomProxy=self.randomProxy),
                        executable_path = helper.browserHelper_findBrowserDriverPaths(ChromeExecutable),
                        service_log_path = os.path.join(self.managedPaths.getLogfilePath(), 'chromedriver.log')
                    )
                    helper.browserHelper_startBrowsermobProxy(browserName=browserName, browserInstance=browserInstance,
                                                browserProxy=browserProxy)

            elif browserName == GC.BROWSER_EDGE:
                self.browserOptions.driver = browserNames[browserName](
                    executable_path = helper.browserHelper_findBrowserDriverPaths("msedgedriver.exe"))
            elif browserName == GC.BROWSER_SAFARI:
                # SAFARI doesn't provide any options, but desired_capabilities.
                # Executable_path = the standard safaridriver path.
                if len(desiredCapabilities) == 0:
                    desiredCapabilities = {}
                self.browserOptions.driver = browserNames[browserName](desired_capabilities=desiredCapabilities)

            elif browserName == GC.BROWSER_REMOTE:
                self.browserOptions.driver = browserNames[browserName](options = WebdriverFunctions.webdriver_createBrowserOptions(browserName=browserName,
                                                                                            desiredCapabilities=desiredCapabilities),
                                                        command_executor='http://localhost:4444/wd/hub',
                                                        desired_capabilities=desiredCapabilities)
        elif browserName == GC.BROWSER_REMOTE_V4:
            desired_capabilities = eval(desiredCapabilities)
            if 'seleniumGridIp' in desired_capabilities.keys():
                seleniumGridIp = desired_capabilities['seleniumGridIp']
                del desired_capabilities['seleniumGridIp']
            else:
                seleniumGridIp = '127.0.0.1'

            if 'seleniumGridPort' in desired_capabilities.keys():
                seleniumGridPort = desired_capabilities['seleniumGridPort']
                del desired_capabilities['seleniumGridPort']
            else:
                seleniumGridPort = '4444'

            if not 'browserName' in desired_capabilities.keys():
                desired_capabilities['browserName'] = 'firefox'

            if desired_capabilities['browserName'] == 'firefox':
                lCurPath = lCurPath.joinpath(GeckoExecutable)
                if not (os.path.isfile(str(lCurPath))):
                    self.downloadDriver(GC.BROWSER_FIREFOX)
            elif desired_capabilities['browserName'] == 'chrome':
                lCurPath = lCurPath.joinpath(ChromeExecutable)
                if not (os.path.isfile(str(lCurPath))):
                    self.downloadDriver(GC.BROWSER_CHROME)

            serverUrl = 'http://' + seleniumGridIp + ':' + seleniumGridPort

            self.browserOptions.driver = webdriver.Remote(command_executor=serverUrl,
                                           desired_capabilities=desiredCapabilities)
        else:
            raise SystemExit("Browsername unknown")

        if self.downloadFolder:
            self.downloadFolderMonitoring = DownloadFolderMonitoring(self.downloadFolder)

        self.takeTime("Browser Start")



    def mobileConnectAppium(self, BrowserExecutable, browserName, desired_app, mobileApp, mobile_app_setting):
        if desired_app[GC.MOBILE_PLATFORM_NAME] == "Android":
            desired_cap = desired_app
            if mobileApp == 'True':
                desired_cap['app'] = mobile_app_setting[GC.MOBILE_APP_URL]
                desired_cap['appPackage'] = mobile_app_setting[GC.MOBILE_APP_PACKAGE]
                desired_cap['appActivity'] = mobile_app_setting[GC.MOBILE_APP_ACTIVITY]
            else:
                desired_cap['browserName'] = browserName
                desired_cap['chromedriverExecutable'] = mobile_app_setting[GC.MOBILE_APP_BROWSER_PATH]
                desired_cap['noReset'] = False
            self.browserOptions.driver = Appiumwebdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
        elif desired_app[GC.MOBILE_PLATFORM_NAME] == "iOS":
            desired_cap = desired_app
            if mobileApp == 'True':
                desired_cap['automationName'] = 'XCUITest'
                desired_cap['app'] = mobile_app_setting[GC.MOBILE_APP_URL]
            else:
                desired_cap['browserName'] = 'safari'
            self.browserOptions.driver = Appiumwebdriver.Remote("http://localhost:4723/wd/hub", desired_cap)




    def closeBrowser(self):
        try:
            if self.browserOptions.driver:
                self.browserOptions.driver.quit()
                self.browserOptions.driver = None
        except Exception as ex:
            pass  # If the driver is already dead, it's fine.


    def refresh(self):
        self.browserOptions.driver.execute_script("window.location.reload()")

    def takeScreenshot(self, screenShotPath=None):
        driver =self.browserOptions.driver
        # Filename must have ".png" inside
        lFile = str(uuid.uuid4()) + ".png"

        if screenShotPath:
            lFile = Path(screenShotPath).joinpath(lFile)
        else:
            lFile = Path(self.screenshotPath).joinpath(lFile)

        try:
            lFile = str(lFile)
            driver.save_screenshot(lFile)
            helper.browserHelper_log(logging.DEBUG, f"Stored Screenshot: {lFile}", self.browserOptions)
        except Exception as e:
            helper.browserHelper_log(logging.INFO, f"Screenshot not possible. Error: {e}", self.browserOptions)

        return lFile

    def handleIframe(self, iframe=None):
        """
        Give an IFRAME and it will try to go into.
        If you're inside an iframe it will go out of the iframe
        """
        if iframe:
            helper.browserHelper_log(logging.DEBUG, "Going into Iframe: ", self.browserOptions, **{"iframe": iframe})
            # frame_to_be_availble_and_switch_to_it doesn't work.
            mustEnd = time.time() + 30
            while time.time() < mustEnd:
                try:
                    self.browserOptions.driver.switch_to.default_content()
                    self.iFrame = self.browserOptions.driver.switch_to.frame(iframe)
                    break
                except WebDriverException as e:
                    helper.browserHelper_log(logging.DEBUG, f"IFrame {iframe} not there yet - waiting 1 second", self.browserOptions)
                    time.sleep(1)

            if time.time() > mustEnd:
                raise TimeoutError

        elif self.iFrame:
            helper.browserHelper_log(logging.DEBUG, f"Leaving Iframe: {self.iFrame}", self.browserOptions)
            self.browserOptions.driver.switch_to.default_content()
            self.iFrame = None

    def handleWindow(self, windowNumber=None, function=None, timeout=20):
        """
        Interations with Windows (=BrowserTabs).

        @param windowNumber: Number of the windowHandle inside this browser session (0 = startwindow(=Tab), 1=Next window
        @param function: "CLOSE", "CLOSEALL"
        """
        if function:
            if function.lower() == "close":
                self.browserOptions.driver.close()
                self.browserOptions.driver.switch_to.window(self.browserOptions.driver.window_handles[0])
            elif "closeall" in function.lower():
                exceptHandles = function.lower().replace("closeall", "")
                exceptHandles = exceptHandles.replace("-", "")
                # WindowHandles based on 0.. Value "let 2 windows open" means to close everything except 0 and 1:
                exceptHandles = int(exceptHandles.strip()) - 1
                try:
                    totalWindows = len(self.browserOptions.driver.window_handles)
                except BaseException as e:
                    logger.error(f"Tried to get amount of windows. Threw error {e}. Most probably browser crashed")
                    raise Exceptions.baangtTestStepException(f"Tried to get amount of windows. "
                                                             f"Threw error {e}. Most probably browser crashed")
                for windowHandle in self.browserOptions.driver.window_handles[-1:exceptHandles:-1]:
                    try:
                        self.browserOptions.driver.switch_to.window(windowHandle)
                        self.browserOptions.driver.close()
                    except NoSuchWindowException as e:
                        # If the window is already closed, it's fine. Don't do anything
                        pass
                try:
                    self.browserOptions.driver.switch_to.window(self.browserOptions.driver.window_handles[exceptHandles])
                except IndexError as e:
                    raise Exceptions.baangtTestStepException(f"Seems like the browser crashed. Main-Window lost")
        else:
            success = False
            duration = 0
            while not success and duration < timeout:
                try:
                    self.browserOptions.driver.switch_to.window(self.browserOptions.driver.window_handles[windowNumber])
                    success = True
                    continue
                except Exception as e:
                    logger.debug(f"Tried to switch to Window {windowNumber} but it's not there yet")

                time.sleep(1)
                duration += 1

            if not success:
                raise Exceptions.baangtTestStepException(f"Window {windowNumber} doesn't exist after timeout {timeout}")

    def findByAndWaitForValue(self, id=None, css=None, xpath=None, class_name=None, iframe=None, timeout=20,
                              optional=False):
        """

        @param id: ID of the element
        @param css: CSS-Locator
        @param xpath: XPATH-Locator
        @param class_name: Class-Name
        @param iframe: Iframe to use (use only if changed. If you set an iframe before, you don't need to set it again!)
        @param timeout: Timeout in Seconds before raising an error or returning back (depending on "optional")
        @param optional: If set to "True" and the operation can not be executed, just a log entry is written but no error raised
        @return: the text of the element, if element was found
        """
        self.element = None
        returnValue = None
        start = time.time()
        duration = 0

        while self.element is None and duration < timeout:
            self.element, self.html = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout / 3,
                            optional=optional)
            time.sleep(0.5)
            duration = time.time() - start

        if self.element is not None:
            try:
                if len(self.element.text) > 0:
                    returnValue = self.element.text
                elif self.element.tag_name == 'input':
                    #  element is of type <input />
                    returnValue = self.element.get_property('value')

            except Exception as e:
                logger.debug(f"Exception during findByAndWaitForValue, but continuing {str(e)}, "
                             f"Locator: {self.browserOptions.locatorType} = {self.browserOptions.locator}")
        else:
            logger.info(f"Couldn't find value for element {self.browserOptions.locatorType}:{self.browserOptions.locator}")

        return returnValue

    def findByAndSetText(self, id=None, css=None, xpath=None, class_name=None, value=None, iframe=None,
                         timeout=60, optional=False):
        """
        Please see documentation in findBy and __doSomething
        """
        self.element, self.html = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

        WebdriverFunctions.webdriver_doSomething(GC.CMD_SETTEXT, self.element, value=value, timeout=timeout, optional=optional, browserOptions = self.browserOptions)

    def slowExecutionToggle(self, newSlowExecutionWaitTimeInSeconds=None):
        """
        SlowExecution can be set in globals or by the teststep. It's intended use is debugging or showcasing a testcases
        functionality.

        @param newSlowExecutionWaitTimeInSeconds: Optional. If set, it will change the default value of WaitTime, when SlowExecution is active
        @return: Returns the state of sloeExecution toggle after toggling was done.
        """

        if newSlowExecutionWaitTimeInSeconds:
            self.slowExecutionTimeoutInSeconds = newSlowExecutionWaitTimeInSeconds

        return not self.slowExecution

    def findByAndSetTextIf(self, id=None, css=None, xpath=None, class_name=None, value=None, iframe=None,
                           timeout=60, optional=False):
        """
        Helper function to not have to write:
        If <condition>:
            findByAndSetText(locator)

        instead use:
        findByAndSetTextIf(locator, value).

        If value is evaluated into "True" the Text is set.

        """
        if not value:
            return False

        if len(value) == 0:
            return False

        if str(value) == "0":
            return False

        return self.findByAndSetText(id=id, css=css, xpath=xpath, class_name=class_name, value=value, iframe=iframe,
                                     timeout=timeout, optional=optional)

    def findByAndSetTextValidated(self, id=None,
                                  css=None,
                                  xpath=None,
                                  class_name=None,
                                  value=None,
                                  iframe=None,
                                  timeout=60,
                                  retries=5):
        """
        This is a method not recommended to be used regularly. Sometimes (especially with Angular Frontends) it gets
        pretty hard to set a value into a field. Chrome, but also FF will show the value, but the DOM will not have it.
        Ths Method should be your last ressort. Here we try <retries> time to set a value. Then we read the element again
        and compare value to what we'd expect. If value is different and we're less than <retries>-Times, we'll try again.
        """

        tries = 0

        self.element, self.html = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

        while self.element.text != value and self.element.get_property("value") != value and tries < retries:
            helper.browserHelper_log(logging.DEBUG, f"Verified trying of SetText - iteration {tries} of {retries}", self.browserOptions)

            self.findByAndForceText(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe,
                                    value=value, timeout=timeout)

            self.element, self.html = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

            tries += 1

    def submit(self):
        """
        Used for forms to call the standard submit-function (similar to pressing "Enter" in Dialogue)
        @return:
        """
        self.element.submit()

    def findByAndClick(self, id=None, css=None, xpath=None, class_name=None, iframe=None, timeout=20, optional=False):
        """
        Execute a Click on an element identified by it's locator.
        @return wasSuccessful says, whether the element was found.
        """
        wasSuccessful = False
        self.element, self.html = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout,
                                    optional=optional)

        if self.element is None:
            logger.debug("findBy didn't work in findByAndClick")
        else:
            wasSuccessful = WebdriverFunctions.webdriver_doSomething(GC.CMD_CLICK, self.element, timeout=timeout, optional=optional, browserOptions = self.browserOptions)

        return wasSuccessful

    def _isValidKeyValue(self, value):
        isValid = False
        if value is None:
            pass
        elif len(value) == 0 or str(value) == "0":
            pass
        else:
            isValid = True
        return isValid 

    def findByAndClickIf(self, id=None, css=None, xpath=None, class_name=None, iframe=None, timeout=60,
                         value=None, optional=False):
        """
        Convenience method to not have to write:
        if <condition>:
            findByAndClick(locator)

        instead write:
        findByAndClickIf(locator, value).

        If value is evaluated to "True", the click-event is executed.
        """
        returnValue = False

        if self._isValidKeyValue(value):
            returnValue = self.findByAndClick(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout, optional=optional)
        
        return returnValue

    def findByAndForceText(self, id=None, css=None, xpath=None, class_name=None, value=None,
                           iframe=None, timeout=60, optional=False):
        """
        Convenience Method. Please see documentation in findBy and __doSomething.

        """

        self.element, self.html = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

        WebdriverFunctions.webdriver_doSomething(GC.CMD_FORCETEXT, self.element, value=value, timeout=timeout, optional=optional, browserOptions = self.browserOptions)

    def setBrowserWindowSize(self, browserWindowSize: str):
        """
        Resized the browser Window to a fixed size
        :param browserWindowSize: String with Widht/Height or Width;Height or Width,height or width x height
               If you want also with leading --
        :return: False, if browser wasn't reset,
                 size-Dict when resize worked.
        """
        lIntBrowserWindowSize = browserWindowSize.replace("-","").strip()
        lIntBrowserWindowSize = lIntBrowserWindowSize.replace(";", "/")
        lIntBrowserWindowSize = lIntBrowserWindowSize.replace(",", "/")
        lIntBrowserWindowSize = lIntBrowserWindowSize.replace("x", "/")

        try:
            width = int(lIntBrowserWindowSize.split("/")[0])
            height = int(lIntBrowserWindowSize.split("/")[1])
        except KeyError as e:
            logger.warning(f"Called with wrong setting: {browserWindowSize}. Won't resize browser "
                           f"Can't determine Width/Height.")
            return False
        except ValueError as e:
            logger.warning(f"Called with wrong setting: {browserWindowSize}. Won't resize browser "
                           f"Something seems not numeric before conversion: {lIntBrowserWindowSize}")
            return False

        if width == 0 or height == 0:
            logger.warning(f"Called with wrong setting: {browserWindowSize}. Won't resize browser. Can't be 0")
            return False

        self.browserOptions.driver.set_window_size(width, height)
        size = self.browserOptions.driver.get_window_size()
        logger.debug(f"Resized browser window to width want/is: {width}/{size['width']}, "
                     f"height want/is: {height}/{size['height']}")

        return size

    def findNewFiles(self):
        """
        Returns a list of new files from downloadFolderMonitoring since the last call

        :return: List of Files since last call
        """
        l_list = self.downloadFolderMonitoring.getNewFiles()
        return l_list



    def findBy(self, id=None, css=None, xpath=None, class_name=None, iframe=None, timeout=60, loggingOn=True, optional=False):
        """
        chose any single locator (ID, CSS, XPATH, CLASS_NAME) to identify an element within the page. if slowExectuion
        is set, we'll pause for slowExecutionTimeoutInSeconds.

        @param id: ID of the element
        @param css: CSS-Locator
        @param xpath: XPATH
        @param class_name: Class-Name
        @param iframe: Name of an Iframe. Use only, if you didn't set the Iframe previously already!
        @param timeout: How many seconds shall we try/retry, default = 60 Seconds
        @param loggingOn: Shall this request be logged? Default = Yes
        @param optional: If set to true and within Timeout we can't find the element, we just return this info. If set to False (=default), an Exception is raised
        @return: True if element was located, False if element couldn't be found.
        """

        if self.slowExecution:
            time.sleep(self.slowExecutionTimeoutInSeconds)

        if iframe:
            self.handleIframe(iframe)

        # Set class variables for potential logging of problems.

        if xpath:
            self.browserOptions.locatorType = By.XPATH #'XPATH'  
            self.browserOptions.locator = xpath
        elif css:
            self.browserOptions.locatorType = By.CSS_SELECTOR# 'CSS'
            self.browserOptions.locator = css
        elif class_name:
            self.browserOptions.locatorType = By.CLASS_NAME # 'ClassName'
            self.browserOptions.locator = class_name
        elif id:
            self.browserOptions.locatorType = By.ID  # 'ID'
            self.browserOptions.locator = id

        if loggingOn:
            logger.debug(f"Locating Element {self.browserOptions.locatorType} = {self.browserOptions.locator}")

        element, html = WebdriverFunctions.webdriver_tryAndRetry(self.browserOptions, timeout=timeout, optional=optional)

        if element is None and not optional:
            raise Exceptions.baangtTestStepException(f"Element {self.browserOptions.locatorType} = {self.browserOptions.locator} could not be found "
                                                     f"within timeout of {timeout}")
        return element, html


 

    def getURL(self):
        """

        @return: the current URL/URI of the current Tab of the current Browser
        """
        return self.browserOptions.driver.current_url


    def findWaitNotVisible(self, css=None, xpath=None, id=None, timeout=90, optional=False):
        """
        You'd use this method when you wait for an element to disappear, for instance Angular Spinner or a popup
        to disapear before you continue with your script in the main screen.

        """
        logger.debug(f"Waiting for Element to disappear: XPATH:{xpath}, timeout: {timeout}")
        time.sleep(0.5)

        stillHere = True
        elapsed = 0
        begin = time.time()

        while stillHere and elapsed < timeout:
            try:
                if xpath:
                    self.element = self.browserOptions.driver.find_element_by_xpath(xpath)
                elif id:
                    self.element = self.browserOptions.driver.find_element_by_id(id)
                elif css:
                    self.element = self.browserOptions.driver.find_element_by_css_selector(css)
                time.sleep(0.2)
                elapsed = time.time() - begin
            except Exception as e:
                # Element gone - exit
                stillHere = False
                helper.browserHelper_log(logging.DEBUG, f"Element was gone after {format(elapsed, '.2f')} seconds", self.browserOptions)
                return

        raise Exceptions.baangtTestStepException(
            f"Element still here after {timeout} seconds. Locator: xpath={xpath}, id={id}")

    def checkLinks(self):
        """
        For the current page we'll check all links and return result in format
        <status_code> <link_that_was_checked>

        :return: List of checked links
        """
        lResult = []
        links = self.browserOptions.driver.find_elements_by_css_selector("a")
        logger.debug(f"Checking links on page {self.browserOptions.driver.current_url}")
        for link in links:
            lHref = link.get_attribute("href")
            if not lHref:
                continue
            if lHref.startswith("mailto"):
                pass
            else:
                try:
                    r = requests.head(lHref)
                    lResult.append([r.status_code, lHref])
                    logger.debug(f"Result was: {r.status_code}, {lHref}")
                except requests.exceptions.InvalidURL as e:
                    lResult.append([500, f"Invalid URL: {lHref}"])
                except requests.exceptions.ConnectionError as e:
                    lResult.append([500, f"HTTP connection error: {lHref}"])
                except requests.exceptions.MissingSchema as e:
                    lResult.append([500, f"Missing Schema - invalid URL: {lHref}"])

        return lResult

    @staticmethod
    def sleep(sleepTimeinSeconds):
        time.sleep(sleepTimeinSeconds)


    def waitForElementChangeAfterButtonClick(self, timeout=5):
        """
        Wait for a stale element (in a good way). Stale means, that the object has changed.

        old element is in self.element
        old locator is in self.browserOptions.locatorType and self.browserOptions.locator

        :param timeout:
        :return:
        """

        lOldElement = self.element.id

        lStartOfWaiting = time.time()
        elapsed = 0

        logger.debug("Starting")

        xpath, css, id = utils.setLocatorFromLocatorType(self.browserOptions.locatorType, self.browserOptions.locator)

        while elapsed < timeout:
            self.element, self.html = self.findBy(xpath=xpath, css=css, id=id, timeout=0.5, optional=True)
            if self.element is None:
                # Wonderful. Element is gone
                logger.debug("Old object is not in the page any longer, save to continue")
                return True
            if self.element.id != lOldElement:
                logger.debug("Old element is stale, save to continue")
                return True

            time.sleep(0.2)
            elapsed = time.time() - lStartOfWaiting

        logger.debug("Old element equal to new element after timeout. Staleness not detected using this method")

    def waitForPageLoadAfterButtonClick(self, timeout=5):
        """
        Problem: If the same XPATH/CSS/ID exists on both pages (the current one, where a button is clicked
                 and the next one, where we now want to interact, then it happens very often, that the element
                 is stale (because it was bound to the current page BEFORE the page-load happened.
        Solution: Wait deliberately until current self.element is stale.
        :param timout: Yeah, you guessed it. The timeout
        :return: True = New page loaded, False = The element didn't get stale within timeout
        """

        if not self.html:
            sys.exit("Something is very wrong! self.html didn't exist when waitForPageLoadAfterButtonClick was called")

        lStartOfWaiting = time.time()
        elapsed = 0
        logger.debug("Starting")

        while elapsed < timeout:
            lHTML = self.browserOptions.driver.find_element_by_tag_name("html")
            if lHTML != self.html:
                logger.debug("Page was reloaded")
                return True

            time.sleep(0.2)

            elapsed = time.time() - lStartOfWaiting

        logger.debug("No Page reload detected by this method")
        return False    # There was no changed HTML

    def goToUrl(self, url):
        helper.browserHelper_log(logging.INFO, f'GoToUrl:{url}', self.browserOptions)
        try:
            if self.browserName==GC.BROWSER_FIREFOX:
                self.browserOptions.driver.set_context("content")
            self.browserOptions.driver.get(url)
            self.setZoomFactor()
        except WebDriverException as e:
            # Use noScreenshot-Parameter as otherwise we'll try on a dead browser to create a screenshot
            helper.browserHelper_log(logging.ERROR, f"Webpage {url} not reached. Error was: {e}", self.browserOptions, cbTakeScreenshot=self.takeScreenshot)
            helper.browserHelper_setProxyError(self.randomProxy)
            raise Exceptions.baangtTestStepException
        except Exception as e:
            # Use noScreenshot-Parameter as otherwise we'll try on a dead browser to create a screenshot
            helper.browserHelper_log(logging.ERROR, f"Webpage {url} throws error {e}", self.browserOptions, cbTakeScreenshot=self.takeScreenshot)
            helper.browserHelper_setProxyError(self.randomProxy)
            raise Exceptions.baangtTestStepException(url, e)


    def goBack(self):
        """
        Method to go 1 step back in current tab's browse history
        @return:
        """
        try:
            self.javaScript("window.history.go(-1)")
        except Exception as e:
            helper.browserHelper_log(logging.WARNING, f"Tried to go back in history, didn't work with error {e}", self.browserOptions)

    def javaScript(self, jsText, *args):
        """Execute a given JavaScript in the current Session"""
        self.browserOptions.driver.execute_script(jsText, *args)

    def setZoomFactor(self, lZoomFactor=None):
        """
        Will try to set the browser's zoom factor.

        :param lZoomFactor: set with a value. Otherwise existing value will be used (if previously set)
        :return:
        """
        if not self.zoomFactorDesired and not lZoomFactor:
            return False

        if lZoomFactor:
            self.zoomFactorDesired = int(lZoomFactor)

        if self.browserName == GC.BROWSER_CHROME:
            x = self.getURL()
            if x[0:5] == "http:":       # He loaded already something. Too late for us
                logger.debug("CHROME: Got called to change Zoom level - but already URL loaded. Too late.")
                return False
            self.browserOptions.driver.get("chrome://settings/")
            self.browserOptions.driver.execute_script(f"chrome.settingsPrivate.setDefaultZoom({self.zoomFactorDesired/100});")
            logger.debug(f"CHROME: Set default zoom using JS-Method to {self.zoomFactorDesired/100}")
            return True

        if self.browserName == GC.BROWSER_FIREFOX:
            self.browserOptions.driver.set_context("chrome")                # !sic: in Firefox.. Whatever...

        if self.zoomFactorDesired > 100:
            lZoomKey = "+"
        else:
            lZoomKey = "-"

        # E.g. current = 100. Desired = 67%: 100-67 = 33. 33/10 = 3.3  int(3.3) = 3 --> he'll hit 3 times CTRL+"-"
        lDifference = abs(100 - self.zoomFactorDesired)
        lHitKeyTimes = int(lDifference/10)

        try:
            lWindow = self.browserOptions.driver.find_element_by_tag_name("html")
            # Reset the browser window to 100%:
            if platform.system().lower() == "darwin":
                lWindow.send_keys(keys.Keys.META + "0")
            else:
                lWindow.send_keys(keys.Keys.CONTROL + "0")

            # Now set to desired zoom factor:
            for counter in range(lHitKeyTimes):
                if platform.system().lower() == "darwin":
                    lWindow.send_keys(keys.Keys.META + lZoomKey)
                else:
                    lWindow.send_keys(keys.Keys.CONTROL + lZoomKey)

            logger.debug(f"Adjusted zoom factor of browserwindow to {self.zoomFactorDesired}")
        except Exception as e:
            logger.debug(f"Tried to adjust zoom factor and failed: {e}")
        finally:
            if self.browserName == GC.BROWSER_FIREFOX:
                self.browserOptions.driver.set_context("content")

    def downloadDriver(self, browserName):
        path = Path(self.managedPaths.getOrSetDriverPath())
        logger.debug(f"Trying to download browserDriver for {browserName} into {path}")
        path.mkdir(parents=True, exist_ok=True)
        tar_url = ''
        url = ''
        if str(browserName) == GC.BROWSER_FIREFOX:
            response = requests.get(GC.GECKO_URL)
            gecko = response.json()
            gecko = gecko['assets']
            gecko_length_results = len(gecko)
            drivers_url_dict = []

            for i in range(gecko_length_results):
                drivers_url_dict.append(gecko[i]['browser_download_url'])

            zipbObj = zip(GC.OS_list, drivers_url_dict)
            geckoDriversDict = dict(zipbObj)
            if platform.system().lower() == GC.WIN_PLATFORM:
                if ctypes.sizeof(ctypes.c_voidp) == GC.BIT_64:
                    url = geckoDriversDict[GC.OS_list[4]]
                else:
                    url = geckoDriversDict[GC.OS_list[3]]
            elif platform.system().lower() == GC.LINUX_PLATFORM:
                if ctypes.sizeof(ctypes.c_voidp) == GC.BIT_64:
                    tar_url = geckoDriversDict[GC.OS_list[1]]
                else:
                    tar_url = geckoDriversDict[GC.OS_list[0]]
            else:
                tar_url = geckoDriversDict[GC.OS_list[2]]

            if tar_url != '':
                path_zip = path.joinpath(GC.GECKO_DRIVER.replace('exe', 'tar.gz'))
                filename, headers = urlretrieve(tar_url, path_zip)
                logger.debug(f"Tarfile with browser expected here: {filename} ")
                tar = tarfile.open(filename, "r:gz")
                tar.extractall(path)
                tar.close()

            else:
                file = requests.get(url)
                path_zip = path.joinpath(GC.GECKO_DRIVER.replace('exe', 'zip'))
                logger.debug(f"Zipfile with browser expected here: {path_zip} ")
                open(path_zip, 'wb').write(file.content)
                with zipfile.ZipFile(path_zip, 'r') as zip_ref:
                    zip_ref.extractall(path)

        elif browserName == GC.BROWSER_CHROME:
            response = requests.get(GC.CHROME_URL)
            chromeversion = response.text
            chromedriver_url_dict = []

            for i in range(len(GC.OS_list_chrome)):
                OS = GC.OS_list_chrome[i]
                chrome = 'http://chromedriver.storage.googleapis.com/{ver}/chromedriver_{os}.zip'.format(
                    ver=chromeversion,
                    os=OS)

                chromedriver_url_dict.append(chrome)

            zipbObjChrome = zip(GC.OS_list, chromedriver_url_dict)
            chromeDriversDict = dict(zipbObjChrome)
            if platform.system().lower() == GC.WIN_PLATFORM:
                url = chromeDriversDict[GC.OS_list[3]]
            elif platform.system().lower() == GC.LINUX_PLATFORM:
                url = chromeDriversDict[GC.OS_list[1]]
            else:
                url = chromeDriversDict[GC.OS_list[2]]
            file = requests.get(url)
            path_zip = path.joinpath(GC.CHROME_DRIVER.replace('exe', 'zip'))
            logger.debug(f"Writing Chrome file into {path_zip}")
            open(path_zip, 'wb').write(file.content)
            with zipfile.ZipFile(path_zip, 'r') as zip_ref:
                zip_ref.extractall(path)
                logger.debug(f"Extracting Chrome driver into {path}")
                # permissions

            if platform.system().lower() != GC.WIN_PLATFORM:
                file_path = path.joinpath(GC.CHROME_DRIVER.replace('.exe', ''))
                os.chmod(file_path, 0o777)

            os.remove(path_zip)

        else:

            logger.critical(f"Please download driver for {browserName} manually into folder /browserDrivers")