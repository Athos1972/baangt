import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.common import keys
from baangt.base import GlobalConstants as GC
from baangt.base.Timing.Timing import Timing
from baangt.TestSteps import Exceptions
from baangt.base.DownloadFolderMonitoring import DownloadFolderMonitoring
from baangt.base.BrowserHandling.WebdriverFunctions import WebdriverFunctions as webDrv
from baangt.base.BrowserHandling.BrowserHelperFunction import BrowserDriverData
from baangt.base.BrowserHandling.BrowserHelperFunction import BrowserHelperFunction as helper
from baangt.base.Utils import utils
from baangt.base.ProxyRotate import ProxyRotate
from http import HTTPStatus
import uuid
import time
import logging
from pathlib import Path
#import json
import sys
import platform
#import ctypes
import requests
from baangt.base.PathManagement import ManagedPaths
from baangt.base.RuntimeStatistics import Statistic
import psutil
import signal


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

    def __init__(self, timing=None, screenshotPath=None, statistics=None):
        self.iFrame = None
        self.element = None                 
        self.browserData = BrowserDriverData(locatorType=None, locator=None,
                                             driver=webDrv.BROWSER_DRIVERS[GC.BROWSER_FIREFOX])
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
        self.statistics = Statistic()

        if timing:
            self.timing = timing
            self.takeTime = timing.takeTime
        else:
            self.timing = Timing()
            self.takeTime = self.timing.takeTime

        if not screenshotPath or screenshotPath == "":
            self.screenshotPath = self.managedPaths.getOrSetScreenshotsPath()
        else:
            self.screenshotPath = screenshotPath

    def sleep(self, seconds):
        time.sleep(seconds)

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
        self.bpid = []
        lCurPath = Path(self.managedPaths.getOrSetDriverPath())

        if browserName in webDrv.BROWSER_DRIVERS:

            browserProxy = kwargs.get('browserProxy')
            browserInstance = kwargs.get('browserInstance', 'unknown')

            if utils.anything2Boolean(mobileType):
                self.browserData.driver = self._mobileConnectAppium(browserName, desired_app, mobileApp, mobile_app_setting)
            elif GC.BROWSER_FIREFOX == browserName:
                self.browserData.driver = self._browserFirefoxRun(browserName, lCurPath, browserProxy, randomProxy, desiredCapabilities)
                helper.browserHelper_startBrowsermobProxy(browserName=browserName, browserInstance=browserInstance, browserProxy=browserProxy)
                self.bpid.append(self.browserData.driver.capabilities.get("moz:processID"))
            elif GC.BROWSER_CHROME == browserName:
                self.browserData.driver = self._browserChromeRun(browserName, lCurPath, browserProxy, randomProxy, desiredCapabilities)
                helper.browserHelper_startBrowsermobProxy(browserName=browserName, browserInstance=browserInstance, browserProxy=browserProxy)
                try:
                    port = self.browserData.driver.capabilities['goog:chromeOptions']["debuggerAddress"].split(":")[1]
                    fp = os.popen(f"lsof -nP -iTCP:{port} | grep LISTEN")
                    self.bpid.append(int(fp.readlines()[-1].split()[1]))
                except Exception as ex:
                    logger.info(ex)
            elif GC.BROWSER_EDGE == browserName:
                self.browserData.driver = webDrv.BROWSER_DRIVERS[browserName](executable_path = helper.browserHelper_findBrowserDriverPaths(GC.EDGE_DRIVER))
            elif GC.BROWSER_SAFARI == browserName:
                # SAFARI doesn't provide any options, but desired_capabilities.
                # Executable_path = the standard safaridriver path.
                if len(desiredCapabilities) == 0:
                    desiredCapabilities = {}
                self.browserData.driver = webDrv.BROWSER_DRIVERS[browserName](desired_capabilities=desiredCapabilities)
            elif GC.BROWSER_REMOTE == browserName:
                self.browserData.driver = webDrv.BROWSER_DRIVERS[browserName](options = webDrv.webdriver_createBrowserOptions(browserName=browserName,
                                                        desiredCapabilities=desiredCapabilities),
                                                        command_executor=GC.REMOTE_EXECUTE_URL,
                                                        desired_capabilities=desiredCapabilities)
            else:
                # TODO add exception, this code should never be reached
                pass
        elif GC.BROWSER_REMOTE_V4 == browserName:
            desired_capabilities, seleniumGridIp, seleniumGridPort = helper.browserHelper_setSettingsRemoteV4(desiredCapabilities)

            if desired_capabilities['browserName'] == 'firefox':
                browserExecutable = helper.browserHelper_getBrowserExecutable(GC.BROWSER_FIREFOX)
                self._downloadDriverCheck(browserExecutable, lCurPath, GC.BROWSER_FIREFOX)
            elif desired_capabilities['browserName'] == 'chrome':
                browserExecutable = helper.browserHelper_getBrowserExecutable(GC.BROWSER_CHROME)
                self._downloadDriverCheck(browserExecutable, lCurPath, GC.BROWSER_CHROME)

            serverUrl = 'http://' + seleniumGridIp + ':' + seleniumGridPort
            self.browserData.driver = webDrv.BROWSER_DRIVERS[GC.BROWSER_REMOTE](command_executor=serverUrl, desired_capabilities=desiredCapabilities)
        else:
            raise SystemExit("Browsername unknown")

        if self.downloadFolder:
            self.downloadFolderMonitoring = DownloadFolderMonitoring(self.downloadFolder)

        self.takeTime("Browser Start")

    def _downloadDriverCheck(self, executable, lCurPath, browserName):
        lCurPath = lCurPath.joinpath(executable)

        if not (os.path.isfile(str(lCurPath))):
            self.downloadDriver(browserName)

    def _browserChromeRun(self, browserName, lCurPath, browserProxy, randomProxy, desiredCapabilities):
        executable = helper.browserHelper_getBrowserExecutable(browserName)
        self._downloadDriverCheck(executable, lCurPath, browserName)

        lOptions = webDrv.webdriver_createBrowserOptions(browserName=browserName,
                                                        desiredCapabilities=desiredCapabilities,
                                                        browserMobProxy=browserProxy,
                                                        randomProxy=randomProxy)

        self.downloadFolder=webDrv.getDownloadFolderFromChromeOptions(options=lOptions)

        return webDrv.BROWSER_DRIVERS[browserName](
            chrome_options = lOptions,
            executable_path = helper.browserHelper_findBrowserDriverPaths(executable),
            service_log_path = os.path.join(self.managedPaths.getLogfilePath(), 'chromedriver.log')
        )

    def _browserFirefoxRun(self, browserName, lCurPath, browserProxy, randomProxy, desiredCapabilities):
        executable = helper.browserHelper_getBrowserExecutable(browserName)
        self._downloadDriverCheck(executable, lCurPath, browserName)

        profile = webDrv.webdriver_setFirefoxProfile(browserProxy, randomProxy)
        self.downloadFolder = webDrv.getDownloadFolderFromProfile(profile)
        logger.debug(f"Firefox Profile as follows:{profile.userPrefs}")

        return webDrv.BROWSER_DRIVERS[browserName](
            options = webDrv.webdriver_createBrowserOptions(browserName=browserName, desiredCapabilities=desiredCapabilities),
            executable_path = helper.browserHelper_findBrowserDriverPaths(executable),
            firefox_profile = profile,
            service_log_path = os.path.join(self.managedPaths.getLogfilePath(), 'geckodriver.log')
            )


    @staticmethod
    def _mobileConnectAppium(browserName, desired_app, mobileApp, mobile_app_setting):
        validSettings = False
        desired_cap = desired_app

        if desired_app[GC.MOBILE_PLATFORM_NAME] == "Android":
            validSettings = True
            if utils.anything2Boolean(mobileApp):
                desired_cap['app'] = mobile_app_setting[GC.MOBILE_APP_URL]
                desired_cap['appPackage'] = mobile_app_setting[GC.MOBILE_APP_PACKAGE]
                desired_cap['appActivity'] = mobile_app_setting[GC.MOBILE_APP_ACTIVITY]
            else:
                desired_cap['browserName'] = browserName
                desired_cap['chromedriverExecutable'] = mobile_app_setting[GC.MOBILE_APP_BROWSER_PATH]
                desired_cap['noReset'] = False
            
        elif desired_app[GC.MOBILE_PLATFORM_NAME] == "iOS":
            validSettings = True
            if utils.anything2Boolean(mobileApp):
                desired_cap['automationName'] = 'XCUITest'
                desired_cap['app'] = mobile_app_setting[GC.MOBILE_APP_URL]
            else:
                desired_cap['browserName'] = 'safari'
            
        if validSettings:
            return webDrv.BROWSER_DRIVERS[GC.BROWSER_APPIUM](GC.REMOTE_EXECUTE_URL, desired_cap)
        else:
            return None

    def closeBrowser(self):
        self.statistics.update_teststep()
        try:
            if self.browserData.driver:
                self.browserData.driver.close()
                self.browserData.driver.quit()
                self.browserData.driver = None
                if len(self.bpid) > 0:
                    for bpid in self.bpid:
                        os.kill(bpid, signal.SIGINT)

        except Exception as ex:
            logger.info(ex)
            pass  # If the driver is already dead, it's fine.


    def refresh(self):
        self.browserData.driver.execute_script("window.location.reload()")

    def takeScreenshot(self, screenShotPath=None):
        driver = self.browserData.driver
        # Filename must have ".png" inside
        lFile = str(uuid.uuid4()) + ".png"

        if screenShotPath:
            lFile = Path(screenShotPath).joinpath(lFile)
        else:
            lFile = Path(self.screenshotPath).joinpath(lFile)

        try:
            lFile = str(lFile)
            driver.save_screenshot(lFile)
            helper.browserHelper_log(logging.DEBUG, f"Stored Screenshot: {lFile}", self.browserData)
        except Exception as e:
            helper.browserHelper_log(logging.INFO, f"Screenshot not possible. Error: {e}", self.browserData)
            lFile = None

        return lFile

    def handleIframe(self, iframe=None):
        """
        Give an IFRAME and it will try to go into.
        If you're inside an iframe it will go out of the iframe
        """
        self.statistics.update_teststep()
        if iframe:
            self.browserData.locatorType="XPATH"
            self.browserData.locator=iframe
            helper.browserHelper_log(logging.DEBUG, "Going into Iframe: ", self.browserData, **{"iframe": iframe})
            # frame_to_be_availble_and_switch_to_it doesn't work.
            mustEnd = time.time() + 30
            while time.time() < mustEnd:
                try:
                    self.browserData.driver.switch_to.default_content()
                    self.iFrame = self.browserData.driver.switch_to.frame(iframe)
                    break
                except WebDriverException as e:
                    helper.browserHelper_log(logging.DEBUG, f"IFrame {iframe} not there yet - waiting 1 second", self.browserData)
                    time.sleep(1)

            if time.time() > mustEnd:
                raise TimeoutError

        elif self.iFrame:
            helper.browserHelper_log(logging.DEBUG, f"Leaving Iframe: {self.iFrame}", self.browserData)
            self.browserData.driver.switch_to.default_content()
            self.iFrame = None
        else:
            # TODO add exception, this code should never be reached
            pass

    def handleWindow(self, windowNumber=None, function=None, timeout=20):
        """
        Interations with Windows (=BrowserTabs).

        @param windowNumber: Number of the windowHandle inside this browser session (0 = startwindow(=Tab), 1=Next window
        @param function: "CLOSE", "CLOSEALL"
        """
        self.statistics.update_teststep()
        if function:
            if "close" == function.lower():
                self.browserData.driver.close()
                self.browserData.driver.switch_to.window(self.browserData.driver.window_handles[0])
            elif "closeall" in function.lower():
                exceptHandles = function.lower().replace("closeall", "")
                exceptHandles = exceptHandles.replace("-", "")
                # WindowHandles based on 0.. Value "let 2 windows open" means to close everything except 0 and 1:
                exceptHandles = int(exceptHandles.strip()) - 1
                try:
                    len(self.browserData.driver.window_handles)
                except BaseException as e:
                    logger.error(f"Tried to get amount of windows. Threw error {e}. Most probably browser crashed")
                    raise Exceptions.baangtTestStepException(f"Tried to get amount of windows. "
                                                             f"Threw error {e}. Most probably browser crashed")
                for windowHandle in self.browserData.driver.window_handles[-1:exceptHandles:-1]:
                    try:
                        self.browserData.driver.switch_to.window(windowHandle)
                        self.browserData.driver.close()
                    except NoSuchWindowException as e:
                        # If the window is already closed, it's fine. Don't do anything
                        pass
                try:
                    self.browserData.driver.switch_to.window(self.browserData.driver.window_handles[exceptHandles])
                except IndexError as e:
                    raise Exceptions.baangtTestStepException(f"Seems like the browser crashed. Main-Window lost")
            else:
                # TODO Wrong function, add exception
                pass
        else:
            success = False
            duration = 0
            while not success and duration < timeout:
                try:
                    self.browserData.driver.switch_to.window(self.browserData.driver.window_handles[windowNumber])
                    success = True
                    continue
                except Exception as e:
                    logger.debug(f"Tried to switch to Window {windowNumber} but it's not there yet")

                time.sleep(1)
                duration += 1

            if not success:
                raise Exceptions.baangtTestStepException(f"Window {windowNumber} doesn't exist after timeout {timeout}")

    def findByAndWaitForValue(self, id=None, css=None, xpath=None, class_name=None, iframe=None, timeout=20, optional=False):
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
        self.statistics.update_teststep()
        self.element = None
        returnValue = None
        start = time.time()
        duration = 0

        while not self.element and duration < timeout:
            self.element, self.html = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout / 3,
                            optional=optional)
            time.sleep(0.5)
            duration = time.time() - start

        if self.element:
            try:
                if len(self.element.text) > 0:
                    returnValue = self.element.text
                elif self.element.tag_name == 'input':
                    #  element is of type <input />
                    returnValue = self.element.get_property('value')
                else:
                    returnValue = None
            except Exception as e:
                logger.debug(f"Exception during findByAndWaitForValue, but continuing {str(e)}, "
                             f"Locator: {self.browserData.locatorType} = {self.browserData.locator}")
        else:
            logger.info(f"Couldn't find value for element {self.browserData.locatorType}:{self.browserData.locator}")

        return returnValue

    def findByAndSetText(self, id=None, css=None, xpath=None, class_name=None, value=None, iframe=None,
                         timeout=60, optional=False):
        """
        Please see documentation in findBy and __doSomething
        """
        self.element, self.html = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)
        if not self.element:
            return False

        return webDrv.webdriver_doSomething(GC.CMD_SETTEXT, self.element, value=value, timeout=timeout, optional=optional, browserData = self.browserData)

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

        if self._isValidKeyValue(value):
            return self.findByAndSetText(id=id, css=css, xpath=xpath, class_name=class_name, value=value, iframe=iframe, timeout=timeout, optional=optional)
        else:
            return False

    def findByAndSetTextValidated(self, id=None, css=None, xpath=None, class_name=None, value=None, iframe=None, timeout=60, retries=5):
        """
        This is a method not recommended to be used regularly. Sometimes (especially with Angular Frontends) it gets
        pretty hard to set a value into a field. Chrome, but also FF will show the value, but the DOM will not have it.
        Ths Method should be your last ressort. Here we try <retries> time to set a value. Then we read the element again
        and compare value to what we'd expect. If value is different and we're less than <retries>-Times, we'll try again.
        """

        tries = 0

        self.element, self.html = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

        while self.element.text != value and self.element.get_property("value") != value and tries < retries:
            helper.browserHelper_log(logging.DEBUG, f"Verified trying of SetText - iteration {tries} of {retries}", self.browserData)

            self.findByAndForceText(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe,
                                    value=value, timeout=timeout)

            self.element, self.html = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

            tries += 1

    def submit(self):
        """
        Used for forms to call the standard submit-function (similar to pressing "Enter" in Dialogue)
        @return:
        """
        self.statistics.update_teststep()
        self.element.submit()

    def findByAndClick(self, id=None, css=None, xpath=None, class_name=None, iframe=None, timeout=20, optional=False):
        """
        Execute a Click on an element identified by it's locator.
        @return wasSuccessful says, whether the element was found.
        """

        self.element, self.html = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout,
                                    optional=optional)

        if not self.element:
            logger.debug("findBy didn't work in findByAndClick")
            return False
        else:
            return webDrv.webdriver_doSomething(GC.CMD_CLICK, self.element, timeout=timeout, optional=optional, browserData = self.browserData)

    def confirmAlertIfAny(self):
        self.statistics.update_teststep()
        try:
            self.browserData.driver.switch_to().alert().accept()
        except Exception as e:
            pass

    @staticmethod
    def _isValidKeyValue(value):
        isValid = False
        if not value:
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
        if self._isValidKeyValue(value):
            return self.findByAndClick(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout, optional=optional)
        else:
            return False

    def findByAndForceText(self, id=None, css=None, xpath=None, class_name=None, value=None,
                           iframe=None, timeout=60, optional=False):
        """
        Convenience Method. Please see documentation in findBy and __doSomething.

        """

        self.element, self.html = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

        if not self.element:
            return False

        return webDrv.webdriver_doSomething(GC.CMD_FORCETEXT, self.element, value=value, timeout=timeout, optional=optional, browserData = self.browserData)

    def setBrowserWindowSize(self, browserWindowSize: str):
        """
        Resized the browser Window to a fixed size
        :param browserWindowSize: String with Widht/Height or Width;Height or Width,height or width x height
               If you want also with leading --
        :return: False, if browser wasn't reset,
                 size-Dict when resize worked.
        """
        self.statistics.update_teststep()
        lIntBrowserWindowSize = browserWindowSize.replace("-","").strip()
        lIntBrowserWindowSize = lIntBrowserWindowSize.replace(";", "/")
        lIntBrowserWindowSize = lIntBrowserWindowSize.replace(",", "/")
        lIntBrowserWindowSize = lIntBrowserWindowSize.replace("x", "/")
        lIntBrowserWindowSize = lIntBrowserWindowSize.replace("*", "/")
        validSize = False

        try:
            width = int(lIntBrowserWindowSize.split("/")[0])
            height = int(lIntBrowserWindowSize.split("/")[1])
        except KeyError as e:
            logger.warning(f"Called with wrong setting: {browserWindowSize}. Won't resize browser "
                           f"Can't determine Width/Height.")
        except ValueError as e:
            logger.warning(f"Called with wrong setting: {browserWindowSize}. Won't resize browser "
                           f"Something seems not numeric before conversion: {lIntBrowserWindowSize}")

        try:
            if width == 0 or height == 0:
                logger.warning(f"Called with wrong setting: {browserWindowSize}. Won't resize browser. Can't be 0")
            else:
                validSize = True
        except:
            pass

        if validSize:
            self.browserData.driver.set_window_size(width, height)
            size = self.browserData.driver.get_window_size()
            logger.debug(f"Resized browser window to width want/is: {width}/{size['width']}, "
                        f"height want/is: {height}/{size['height']}")
        else:
            size = False

        return size

    def findNewFiles(self):
        """
        Returns a list of new files from downloadFolderMonitoring since the last call

        :return: List of Files since last call
        """
        self.statistics.update_teststep()
        l_list = self.downloadFolderMonitoring.getNewFiles()
        return l_list

    @staticmethod
    def _setLocator(id, css, xpath, class_name, browserData):
        browserData.locatorType = None
        browserData.locator = None
        if xpath:
            browserData.locatorType = By.XPATH 
            browserData.locator = xpath
        elif css:
            browserData.locatorType = By.CSS_SELECTOR
            browserData.locator = css
        elif class_name:
            browserData.locatorType = By.CLASS_NAME 
            browserData.locator = class_name
        elif id:
            browserData.locatorType = By.ID 
            browserData.locator = id
        return browserData

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
        self.statistics.update_teststep()

        if self.slowExecution:
            time.sleep(self.slowExecutionTimeoutInSeconds)

        if iframe:
            self.handleIframe(iframe)

        # Set class variables for potential logging of problems.
        self.browserData = self._setLocator(id, css, xpath, class_name, self.browserData)

        if loggingOn:
            logger.debug(f"Locating Element {self.browserData.locatorType} = {self.browserData.locator}")

        self.element, self.html = webDrv.webdriver_tryAndRetry(self.browserData, timeout=timeout, optional=optional)

        if not self.element and not optional:
            raise Exceptions.baangtTestStepException(f"Element {self.browserData.locatorType} = {self.browserData.locator} could not be found "
                                                     f"within timeout of {timeout}")
        return self.element, self.html

    def getURL(self):
        """

        @return: the current URL/URI of the current Tab of the current Browser
        """
        self.statistics.update_teststep()
        return self.browserData.driver.current_url


    def findWaitNotVisible(self, css=None, xpath=None, id=None, timeout=90, optional=False):
        """
        You'd use this method when you wait for an element to disappear, for instance Angular Spinner or a popup
        to disapear before you continue with your script in the main screen.

        """
        self.statistics.update_teststep()
        logger.debug(f"Waiting for Element to disappear: XPATH:{xpath}, timeout: {timeout}")
        time.sleep(0.5)

        stillHere = True
        elapsed = 0
        begin = time.time()

        while stillHere and elapsed < timeout:
            try:
                if xpath:
                    self.element = self.browserData.driver.find_element_by_xpath(xpath)
                elif id:
                    self.element = self.browserData.driver.find_element_by_id(id)
                elif css:
                    self.element = self.browserData.driver.find_element_by_css_selector(css)
                time.sleep(0.2)
                elapsed = time.time() - begin
            except Exception as e:
                # Element gone - exit
                stillHere = False
                helper.browserHelper_log(logging.DEBUG, f"Element was gone after {format(elapsed, '.2f')} seconds", self.browserData)

        if not stillHere:
            raise Exceptions.baangtTestStepException(
                f"Element still here after {timeout} seconds. Locator: xpath={xpath}, id={id}")
        
        return stillHere

    def checkLinks(self):
        """
        For the current page we'll check all links and return result in format
        <status_code> <link_that_was_checked>

        :return: List of checked links
        """
        self.statistics.update_teststep()
        lResult = []
        links = self.browserData.driver.find_elements_by_css_selector("a")
        logger.debug(f"Checking links on page {self.browserData.driver.current_url}")
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
                    lResult.append([HTTPStatus.INTERNAL_SERVER_ERROR, f"Invalid URL: {lHref}"])  
                except requests.exceptions.ConnectionError as e:
                    lResult.append([HTTPStatus.INTERNAL_SERVER_ERROR, f"HTTP connection error: {lHref}"])
                except requests.exceptions.MissingSchema as e:
                    lResult.append([HTTPStatus.INTERNAL_SERVER_ERROR, f"Missing Schema - invalid URL: {lHref}"])

        return lResult

    def waitForElementChangeAfterButtonClick(self, timeout=5):
        """
        Wait for a stale element (in a good way). Stale means, that the object has changed.

        old element is in self.element
        old locator is in self.browserData.locatorType and self.browserData.locator

        :param timeout:
        :return:
        """

        self.statistics.update_teststep()

        lOldElement = self.element.id
        isValid = False
        lStartOfWaiting = time.time()
        elapsed = 0
        logger.debug("Starting")

        xpath, css, id = utils.setLocatorFromLocatorType(self.browserData.locatorType, self.browserData.locator)

        while not isValid and elapsed < timeout:
            self.element, self.html = self.findBy(xpath=xpath, css=css, id=id, timeout=0.5, optional=True)
            if not self.element:
                # Wonderful. Element is gone
                logger.debug("Old object is not in the page any longer, save to continue")
                isValid = True
            if self.element.id != lOldElement:
                logger.debug("Old element is stale, save to continue")
                isValid = True

            time.sleep(0.2)
            elapsed = time.time() - lStartOfWaiting

        if not isValid:
            # TimeOut Return false
            logger.debug("Old element equal to new element after timeout. Staleness not detected using this method")

        return isValid

    def waitForPageLoadAfterButtonClick(self, timeout=5):
        """
        Problem: If the same XPATH/CSS/ID exists on both pages (the current one, where a button is clicked
                 and the next one, where we now want to interact, then it happens very often, that the element
                 is stale (because it was bound to the current page BEFORE the page-load happened.
        Solution: Wait deliberately until current self.element is stale.
        :param timout: Yeah, you guessed it. The timeout
        :return: True = New page loaded, False = The element didn't get stale within timeout
        """

        # Performance in 5 parallel Runs dropped from 06:50 to 07:51. That's 1 Minute slower
        # 60 Seconds or 10% time lost.
        # For now let it as it is. If users report that as a problem, revisit the subject and
        # e.g. find another way to understand, whether we're still on the same page or not.

        self.statistics.update_teststep()

        if not self.html:
            sys.exit("Something is very wrong! self.html didn't exist when waitForPageLoadAfterButtonClick was called")

        lStartOfWaiting = time.time()
        elapsed = 0
        logger.debug("Starting")

        while elapsed < timeout:
            lHTML = self.browserData.driver.find_element_by_tag_name("html")
            if lHTML != self.html:
                logger.debug("Page was reloaded")
                return True

            time.sleep(0.2)

            elapsed = time.time() - lStartOfWaiting

        logger.debug("No Page reload detected by this method")
        return False    # There was no changed HTML

    def goToUrl(self, url):
        self.statistics.update_teststep()
        helper.browserHelper_log(logging.INFO, f'GoToUrl:{url}', self.browserData)
        try:
            if self.browserName==GC.BROWSER_FIREFOX:
                self.browserData.driver.set_context("content")
            self.browserData.driver.get(url)
            self.setZoomFactor()
        except WebDriverException as e:
            # Use noScreenshot-Parameter as otherwise we'll try on a dead browser to create a screenshot
            helper.browserHelper_log(logging.ERROR, f"Webpage {url} not reached. Error was: {e}", self.browserData, cbTakeScreenshot=self.takeScreenshot)
            helper.browserHelper_setProxyError(self.randomProxy)
            raise Exceptions.baangtTestStepException
        except Exception as e:
            # Use noScreenshot-Parameter as otherwise we'll try on a dead browser to create a screenshot
            helper.browserHelper_log(logging.ERROR, f"Webpage {url} throws error {e}", self.browserData, cbTakeScreenshot=self.takeScreenshot)
            helper.browserHelper_setProxyError(self.randomProxy)
            raise Exceptions.baangtTestStepException(url, e)


    def goBack(self):
        """
        Method to go 1 step back in current tab's browse history
        @return:
        """
        self.statistics.update_teststep()
        try:
            self.javaScript("window.history.go(-1)")
        except Exception as e:
            helper.browserHelper_log(logging.WARNING, f"Tried to go back in history, didn't work with error {e}", self.browserData)

    def javaScript(self, jsText, *args):
        """Execute a given JavaScript in the current Session"""
        self.statistics.update_teststep()
        self.browserData.driver.execute_script(jsText, *args)
        
    def _zoomFirefox(self, lZoomKey, lHitKeyTimes):
        try:
            lWindow = self.browserData.driver.find_element_by_tag_name("html")
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
            self.browserData.driver.set_context("content")


    def setZoomFactor(self, lZoomFactor=None):
        """
        Will try to set the browser's zoom factor.

        :param lZoomFactor: set with a value. Otherwise existing value will be used (if previously set)
        :return:
        """

        isZoomed = False
        if self.zoomFactorDesired and lZoomFactor:
            self.zoomFactorDesired = int(lZoomFactor)
            if self.browserName == GC.BROWSER_CHROME:
                logger.critical(f"Zoom in Chrome doesn't work. Continuing without zoom")
                return False
                x = self.getURL()
                if x[0:5] == "http:":       # He loaded already something. Too late for us
                    logger.debug("CHROME: Got called to change Zoom level - but already URL loaded. Too late.")
                else:
                    self.browserData.driver.get("chrome://settings/")
                    self.browserData.driver.execute_script(f"chrome.settingsPrivate.setDefaultZoom({self.zoomFactorDesired/100});")
                    logger.debug(f"CHROME: Set default zoom using JS-Method to {self.zoomFactorDesired/100}")
                    isZoomed = True
            elif self.browserName == GC.BROWSER_FIREFOX:
                self.browserData.driver.set_context("chrome")   

                lZoomKey = "+" if self.zoomFactorDesired > 100 else "-"
                # E.g. current = 100. Desired = 67%: 100-67 = 33. 33/10 = 3.3  int(3.3) = 3 --> he'll hit 3 times CTRL+"-"
                lDifference = abs(100 - self.zoomFactorDesired)
                lHitKeyTimes = int(lDifference/10)
                self._zoomFirefox(lZoomKey, lHitKeyTimes)
                isZoomed = True
            else:
                # statement not matched
                pass
        else:
            # statement not matched
            pass

        return isZoomed

    @staticmethod
    def downloadDriver(browserName):
        managedPaths = ManagedPaths()
        path = Path(managedPaths.getOrSetDriverPath())
        logger.debug(f"Trying to download browserDriver for {browserName} into {path}")
        path.mkdir(parents=True, exist_ok=True)
        if browserName == GC.BROWSER_FIREFOX:
            url, isTarFile = helper.browserHelper_getFirefoxFileUrl()
            if isTarFile:
                helper.browserHelper_extractTarDriverFile(url, path, GC.GECKO_DRIVER)
            else:
                helper.browserHelper_unzipDriverFile(url, path, GC.GECKO_DRIVER)
        elif browserName == GC.BROWSER_CHROME:
            url = helper.browserHelper_getChromeFileUrl()
            helper.browserHelper_unzipDriverFile(url, path, GC.CHROME_DRIVER)
        else:
            logger.critical(f"Please download driver for {browserName} manually into folder /browserDrivers")