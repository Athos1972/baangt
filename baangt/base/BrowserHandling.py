import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as ffOptions
from selenium.common.exceptions import *
from selenium.webdriver.common import keys
from baangt.base import GlobalConstants as GC
from baangt.base.Timing import Timing
from baangt.TestSteps import Exceptions
import uuid
import time
import logging
from pathlib import Path
import json
import sys
import platform

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
        self.driver = None
        self.iFrame = None
        self.element = None
        self.locatorType = None
        self.locator = None
        self.slowExecution = False
        self.slowExecutionTimeoutInSeconds = 1

        if timing:
            self.timing = timing
        else:
            self.timing = Timing()

        self.takeTime = self.timing.takeTime

        if screenshotPath:
            self.screenshotPath = screenshotPath
            Path(self.screenshotPath).mkdir(exist_ok=True)
        else:
            self.screenshotPath = os.getcwd()

    def createNewBrowser(self, browserName=GC.BROWSER_FIREFOX, desiredCapabilities=None, **kwargs):
        """
        Will find the specified executables of the desired browser and start it with the given capabilities.

        @param browserName: one of GC_BROWSER_*-Browsernames, e.g. GC_BROWSER_FIREFOX
        @param desiredCapabilities: DICT of desiredCapabilities for this browser
        @param kwargs: Currently (Jan2020) not used
        """
        self.takeTime("Browser Start")
        browserNames = {
            GC.BROWSER_FIREFOX: webdriver.Firefox,
            GC.BROWSER_CHROME: webdriver.Chrome,
            GC.BROWSER_SAFARI: webdriver.Safari,
            GC.BROWSER_REMOTE: webdriver.Remote}

        if browserName in browserNames:
            GeckoExecutable = "geckodriver"
            ChromeExecutable = "chromedriver"

            if 'NT' in os.name.upper():
                GeckoExecutable = GeckoExecutable + ".exe"
                ChromeExecutable = ChromeExecutable + ".exe"

            if browserName == GC.BROWSER_FIREFOX:
                self.driver = browserNames[browserName](options=self.__createBrowserOptions(browserName=browserName,
                                                                                            desiredCapabilities=desiredCapabilities),
                                                        executable_path=self.__findBrowserDriverPaths(GeckoExecutable))
            elif browserName == GC.BROWSER_CHROME:
                self.driver = browserNames[browserName](options=self.__createBrowserOptions(browserName=browserName,
                                                                                            desiredCapabilities=desiredCapabilities),
                                                        executable_path=self.__findBrowserDriverPaths(ChromeExecutable))
            elif browserName == GC.BROWSER_REMOTE:
                self.driver = browserNames[browserName](options=self.__createBrowserOptions(browserName=browserName,
                                                                                            desiredCapabilities=desiredCapabilities),
                                                        command_executor='http://localhost:4444/wd/hub',
                                                        desired_capabilities = desiredCapabilities)
        else:
            raise SystemExit("Browsername unknown")

        self.takeTime("Browser Start")

    def __findBrowserDriverPaths(self, filename):
        if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
            # We're in pyinstaller. Chromedriver and Geckodriver are in the executable-directory
            # in the subdirectory /chromedriver/ or /geckodriver for Linux und MAC,
            # directly in the exeuctable directory for the windows.exe
            if platform.system().lower() == 'windows':
                lCurPath = Path(sys.executable).parent.joinpath(filename)
            else:
                lCurPath = Path(sys.executable).parent.joinpath(filename).joinpath(filename)

        else:
            lCurPath = Path(os.getcwd())
            lCurPath = lCurPath.joinpath("browserDrivers")
            lCurPath = lCurPath.joinpath(filename)

        logger.debug(f"Path for BrowserDrivers: {lCurPath}")
        return str(lCurPath)

    def slowExecutionToggle(self, newSlowExecutionWaitTimeInSeconds = None):
        """
        SlowExecution can be set in globals or by the teststep. It's intended use is debugging or showcasing a testcases
        functionality.

        @param newSlowExecutionWaitTimeInSeconds: Optional. If set, it will change the default value of WaitTime, when SlowExecution is active
        @return: Returns the state of sloeExecution toggle after toggling was done.
        """

        if self.slowExecution:
            self.slowExecution = False
        else:
            self.slowExecution = True

        if newSlowExecutionWaitTimeInSeconds:
            self.slowExecutionTimeoutInSeconds = newSlowExecutionWaitTimeInSeconds

        return self.slowExecution

    def __createBrowserOptions(self, browserName, desiredCapabilities):
        """
        Translates desired capabilities from the Testrun (or globals) into specific BrowserOptions for the
        currently active browser

        @param browserName: any of the GC.BROWSER*
        @param desiredCapabilities: Settings from TestRun or globals
        @return: the proper BrowserOptions for the currently active browser.
        """
        if browserName == GC.BROWSER_CHROME:
            lOptions = ChromeOptions()
        elif browserName == GC.BROWSER_FIREFOX:
            lOptions = ffOptions()
        else:
            return None

        if not desiredCapabilities:
            return None

        # sometimes instead of DICT comes a string with DICT-Format
        if isinstance(desiredCapabilities, str) and "{" in desiredCapabilities and "}" in desiredCapabilities:
            desiredCapabilities = json.loads(desiredCapabilities.replace("'", '"'))

        if not isinstance(desiredCapabilities, dict):
            return None

        if desiredCapabilities.get(GC.BROWSER_MODE_HEADLESS):
            logger.debug("Starting in Headless mode")
            lOptions.headless = True
            lOptions.add_argument("--window-size=1920,1080")

        return lOptions

    def closeBrowser(self):
        self.driver.quit()

    def _log(self, logType, logText, **kwargs):
        """
        Interal wrapper of Browser-Class for Logging. Takes a screenshot on Error and Warning.

        @param logType: any of logging.ERROR, logging.WARN, INFO, etc.
        @param logText: Text to log
        @param kwargs: Additional Arguments to be logged
        """
        argsString = ""
        for key, value in kwargs.items():
            if value:
                argsString = argsString + f" {key}: {value}"

        if self.locator:
            argsString = argsString + f"Locator: {self.locatorType}:{self.locator}"

        if logType == logging.DEBUG:
            logger.debug(logText + argsString)
        elif logType == logging.ERROR:
            logger.error(logText + argsString)
            self.takeScreenshot()
        elif logType == logging.WARN:
            logger.warning(logText + argsString)
            self.takeScreenshot()
        elif logType == logging.INFO:
            logger.info(logText + argsString)
        elif logType == logging.CRITICAL:
            logger.critical(logText + argsString)
            self.takeScreenshot()
        else:
            print(f"Unknown call to Logger: {logType}")
            self._log(logging.CRITICAL, f"Unknown type in call to logger: {logType}")

    def takeScreenshot(self, screenShotPath=None):
        driver = self.driver
        # Filename must have ".png" inside
        lFile = str(uuid.uuid4()) + ".png"

        if screenShotPath:
            lFile = Path(screenShotPath).joinpath(lFile)
        else:
            lFile = Path(self.screenshotPath).joinpath(lFile)

        try:
            lFile = str(lFile)
            driver.save_screenshot(lFile)
            self._log(logging.DEBUG, f"Stored Screenshot: {lFile}")
        except Exception as e:
            self._log(logging.INFO, f"Screenshot not possible. Error: {e}")

        return lFile

    def handleIframe(self, iframe=None):
        """
        Give an IFRAME and it will try to go into.
        If you're inside an iframe it will go out of the iframe
        """
        if iframe:
            self._log(logging.DEBUG, "Going into Iframe: ", **{"iframe": iframe})
            # frame_to_be_availble_and_switch_to_it doesn't work.
            mustEnd = time.time() + 30
            while time.time() < mustEnd:
                try:
                    self.driver.switch_to.default_content()
                    self.iFrame = self.driver.switch_to.frame(iframe)
                    break
                except WebDriverException as e:
                    self._log(logging.DEBUG, f"IFrame {iframe} not there yet - waiting 1 second")
                    time.sleep(1)
            if time.time() > mustEnd:
                raise TimeoutError

        elif self.iFrame:
            self._log(logging.DEBUG, f"Leaving Iframe: {self.iFrame}")
            self.driver.switch_to.default_content()
            self.iFrame = None

    def handleWindow(self, windowNumber=None, function=None):
        """
        Interations with Windows (=BrowserTabs).

        @param windowNumber: Number of the windowHandle inside this browser session (0 = startwindow(=Tab), 1=Next window
        @param function: "CLOSE", "CLOSEALL"
        """
        if function:
            if function.lower() == "close":
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            elif "closeall" in function.lower():
                exceptHandles = function.lower().replace("closeall", "")
                exceptHandles = exceptHandles.replace("-", "")
                # WindowHandles based on 0.. Value "let 2 windows open" means to close everything except 0 and 1:
                exceptHandles = int(exceptHandles.strip()) - 1
                totalWindows = len(self.driver.window_handles)
                for windowHandle in self.driver.window_handles[-1:exceptHandles:-1]:
                    self.driver.switch_to.window(windowHandle)
                    self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[exceptHandles])
        else:
            try:
                self.driver.switch_to.window(self.driver.window_handles[windowNumber])
            except Exception as e:
                logger.critical(f"Tried to switch to Window {windowNumber} but it's not there")
                raise Exceptions.baangtTestStepException(f"Window {windowNumber} doesn't exist")

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
        start = time.time()
        found = False
        duration = 0

        while not found and duration < timeout:
            self.element = None
            self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout / 3,
                        optional=optional)
            try:
                if len(self.element.text) > 0:
                    return self.element.text
            except Exception as e:
                logger.debug(f"Exception during findByAndWaitForValue, but continuing {str(e)}, "
                             f"Locator: {self.locatorType}:{self.locator}")
                pass
            time.sleep(0.5)
            duration = time.time() - start

        logger.info(f"Couldn't find value for element {self.locatorType}:{self.locator}")
        return None

    def findByAndSetText(self, id=None, css=None, xpath=None, class_name=None, value=None, iframe=None,
                         timeout=60, optional=False):
        """
        Please see documentation in findBy and __doSomething
        """
        self.findBy(id=id,
                    css=css,
                    xpath=xpath,
                    class_name=class_name,
                    iframe=iframe,
                    timeout=timeout)

        self.__doSomething(GC.CMD_SETTEXT, value=value, timeout=timeout, xpath=xpath, optional=optional)

    def findByAndSetTextIf(self, id=None, css=None, xpath=None, class_name=None, value=None, iframe=None,
                           timeout=60):
        """
        Helper function to not have to write:
        If <condition>:
            findByAndSetText(locator)

        instead use:
        findByAndSetTextIf(locator, value).

        If value is evaluated into "True" the Text is set.

        """
        if not value:
            return True

        if len(value) == 0:
            return

        return self.findByAndSetText(id=id, css=css, xpath=xpath, class_name=class_name, value=value, iframe=iframe,
                                     timeout=timeout)

    def findByAndSetTextValidated(self,id = None,
                       css = None,
                       xpath = None,
                       class_name = None,
                       value = None,
                       iframe = None,
                       timeout = 60,
                       retries = 5):
        """
        This is a method not recommended to be used regularly. Sometimes (especially with Angular Frontends) it gets
        pretty hard to set a value into a field. Chrome, but also FF will show the value, but the DOM will not have it.
        Ths Method should be your last ressort. Here we try <retries> time to set a value. Then we read the element again
        and compare value to what we'd expect. If value is different and we're less than <retries>-Times, we'll try again.
        """

        tries = 0

        self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

        while self.element.text != value and self.element.get_property("value") != value and tries < retries:

            self._log(logging.DEBUG, f"Verified trying of SetText - iteration {tries} of {retries}")

            self.findByAndForceText(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe,
                                    value=value, timeout=timeout)

            self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

            tries += 1

    def submit(self):
        """
        Used for forms to call the standard submit-function (similar to pressing "Enter" in Dialogue)
        @return:
        """
        self.element.submit()

    def findByAndClick(self, id = None, css=None, xpath=None, class_name=None, iframe=None, timeout=20, optional=False):
        """
        Execute a Click on an element identified by it's locator.
        @return wasSuccessful says, whether the element was found.
        """
        wasSuccessful = self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout,
                                    optional=optional)

        if not wasSuccessful:
            logger.debug("findBy didn't work in findByAndClick")
            return wasSuccessful

        self.__doSomething(GC.CMD_CLICK, xpath=xpath, timeout=timeout, optional=optional)

        return wasSuccessful

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
        if not value:
            return True

        if len(value) == 0:
            return True

        return self.findByAndClick(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout,
                                   optional=optional)

    def findByAndForceText(self, id=None, css=None, xpath=None, class_name=None, value=None,
                           iframe=None, timeout=60, optional=False):
        """
        Convenience Method. Please see documentation in findBy and __doSomething.

        """

        self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

        self.__doSomething(GC.CMD_FORCETEXT, value=value, timeout=timeout, xpath=xpath, optional=optional)

    def findBy(self, id=None, css=None, xpath=None, class_name=None, iframe=None, timeout=60, loggingOn=True,
               optional=False):
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
            self.locatorType = 'XPATH'
            self.locator = xpath
        elif css:
            self.locatorType = 'CSS'
            self.locator = css
        elif class_name:
            self.locatorType = 'ClassName'
            self.locator = class_name
        elif id:
            self.locatorType = 'ID'
            self.locator = id

        if loggingOn:
            self._log(logging.DEBUG, f"Locating Element {self.locatorType}={self.locator}")

        successful = self.__tryAndRetry(id, css, xpath, class_name, timeout=timeout)

        if not successful and not optional:
            raise Exceptions.baangtTestStepException(f"Element {self.locatorType}={self.locator} could not be found within timeout of {timeout}")
        return successful

    def getURL(self):
        """

        @return: the current URL/URI of the current Tab of the current Browser
        """
        return self.driver.current_url

    def __tryAndRetry(self, id=None, css=None, xpath=None, class_name=None, timeout=20):
        """
        In: Locator
        Out: Boolean whether the element was found or not.

        Also sets the self.element for further use by other Methods (for instance to setText or read existing value)

        The method is resistant to common timing problems (can't work 100% of the time but will remove at least 80%
        of your pain compared to directly calling Selenium Methods).
        """

        wasSuccessful = False
        begin = time.time()
        elapsed = 0
        if timeout < 1.5:
            pollFrequency = timeout / 3
        else:
            pollFrequency = 0.5

        internalTimeout = timeout / 3

        while not wasSuccessful and elapsed < timeout:
            try:
                driverWait = WebDriverWait(self.driver, timeout=internalTimeout, poll_frequency=pollFrequency)

                if id:
                    self.element = driverWait.until(ec.visibility_of_element_located((By.ID, id)))
                elif css:
                    self.element = driverWait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, css)))
                elif class_name:
                    self.element = self.driver.find_element_by_class_name(class_name)
                elif xpath:
                    self.element = driverWait.until(ec.visibility_of_element_located((By.XPATH, xpath)))
                wasSuccessful = True
            except StaleElementReferenceException as e:
                self._log(logging.DEBUG, "Stale Element Exception - retrying " + str(e))
                time.sleep(pollFrequency)
            except ElementClickInterceptedException as e:
                self._log(logging.DEBUG, "ElementClickIntercepted - retrying " + str(e))
                time.sleep(pollFrequency)
            except TimeoutException as e:
                self._log(logging.WARNING, "TimoutException - retrying " + str(e))
                time.sleep(pollFrequency)
            except NoSuchElementException as e:
                self._log(logging.WARNING, "Retrying Webdriver Exception: " + str(e))
                time.sleep(pollFrequency)
            except InvalidSessionIdException as e:
                self._log(logging.CRITICAL, "WebDriver Exception - terminating testrun: " + str(e))
                raise Exceptions.baangtTestStepException
            except NoSuchWindowException as e:
                self._log(logging.CRITICAL, "WebDriver Exception - terminating testrun: " + str(e))
                raise Exceptions.baangtTestStepException
            except ElementNotInteractableException as e:
                self._log(logging.DEBUG, "Most probably timeout exception - retrying: " + str(e))
            except WebDriverException as e:
                self._log(logging.ERROR, "Retrying WebDriver Exception: " + str(e))
                time.sleep(2)

            elapsed = time.time() - begin

        return wasSuccessful

    def findWaitNotVisible(self, xpath=None, id=None, timeout = 90, optional = False):
        """
        You'd use this method when you wait for an element to disappear, for instance Angular Spinner or a popup
        to disapear before you continue with your script in the main screen.

        """
        self._log(logging.DEBUG, "Waiting for Element to disappear", **{"xpath":xpath, "timeout":timeout})
        time.sleep(0.5)

        stillHere = True
        elapsed = 0
        begin = time.time()

        while stillHere and elapsed < timeout:
            try:
                if xpath:
                    self.element = self.driver.find_element_by_xpath(xpath)
                elif id:
                    self.element = self.driver.find_element_by_id(id)
                time.sleep(0.1)
                elapsed = time.time() - begin
            except Exception as e:
                # Element gone - exit
                stillHere = False
                self._log(logging.DEBUG, f"Element was gone after {format(elapsed, '.2f')} seconds")
                return

        raise Exceptions.baangtTestStepException(f"Element still here after {timeout} seconds. Locator: xpath={xpath}, id={id}")

    @staticmethod
    def sleep(sleepTimeinSeconds):
        time.sleep(sleepTimeinSeconds)

    def __doSomething(self, command, value=None, timeout=20, xpath=None, optional=False):
        """
        Will interact in an element (that was found before by findBy-Method and stored in self.element) as defined by
        ``command``.

        Command can be "SETTEXT" (GC.CMD_SETTEXT), "CLICK" (GC.CMD_CLICK), "FORCETEXT" (GC.CMD_FORCETEXT).

        Similarly to __try_and_retry the method is pretty robust when it comes to error handling of timing issues.

        """
        didWork = False
        elapsed = 0
        begin = time.time()

        while not didWork and elapsed < timeout:
            try:
                self._log(logging.DEBUG, f"Do_something {command} with {value}")
                if command.upper() == GC.CMD_SETTEXT:
                    self.element.send_keys(value)
                elif command.upper() == GC.CMD_CLICK:
                    self.element.click()
                elif command.upper() == GC.CMD_FORCETEXT:
                    self.element.clear()
                    for i in range(0, 10):
                        self.element.send_keys(keys.Keys.BACKSPACE)
                    time.sleep(0.1)
                    self.element.send_keys(value)
                didWork = True
                return
            except ElementClickInterceptedException as e:
                self._log(logging.DEBUG, "doSomething: Element intercepted - retry")
                time.sleep(0.2)
            except StaleElementReferenceException as e:
                self._log(logging.DEBUG, "doSomething: Element stale - retry")
                time.sleep(0.2)
            except NoSuchElementException as e:
                self._log(logging.DEBUG, "doSomething: Element not there yet - retry")
                time.sleep(0.5)
            except InvalidSessionIdException as e:
                self._log(logging.ERROR, f"Invalid Session ID Exception caught - aborting... {e} ")
                raise Exceptions.baangtTestStepException(e)
            except ElementNotInteractableException as e:
                self._log(logging.ERROR, f"Element not interactable {e}")
                raise Exceptions.baangtTestStepException(e)
            except NoSuchWindowException as e:
                raise Exceptions.baangtTestStepException(e)
            elapsed = time.time()-begin

        if optional:
            logger.debug(f"Action not possible after {timeout} s, Locator: {self.locatorType}: {self.locator}, but flag 'optional' is set")
        else:
            raise Exceptions.baangtTestStepException(f"Action not possible after {timeout} s, Locator: {self.locatorType}: {self.locator}")

    def goToUrl(self, url):
        self._log(logging.INFO, f'GoToUrl:{url}')
        try:
            self.driver.get(url)
        except WebDriverException as e:
            self._log(logging.ERROR, f"Webpage {url} not reached. Error was: {e}")
            raise Exceptions.baangtTestStepException
        pass

    def goBack(self):
        """
        Method to go 1 step back in current tab's browse history
        @return:
        """
        try:
            self.javaScript("window.history.go(-1)")
        except Exception as e:
            self._log(logging.WARNING, f"Tried to go back in history, didn't work with error {e}")


    def javaScript(self, jsText):
        """Execute a given JavaScript in the current Session"""
        self.driver.execute_script(jsText)

