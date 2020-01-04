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
import time
import logging

logger = logging.getLogger("pyC")

class BrowserDriver:
    def __init__(self, timing=None):
        self.driver : webdriver.Firefox = None
        self.iframe = None
        self.element = None
        self.timeout = 2000   # Default Timeout in Milliseconds
        if timing:
            self.timing = timing
        else:
            self.timing = Timing()
        self.takeTime = self.timing.takeTime

    def createNewBrowser(self, browserName, desiredCapabilities=None, **kwargs):
        self.takeTime("Browser Start")
        browserNames = {
            GC.BROWSER_FIREFOX: webdriver.Firefox,
            GC.BROWSER_CHROME: webdriver.Chrome,
            GC.BROWSER_SAFARI: webdriver.Safari,
            GC.BROWSER_REMOTE: webdriver.Remote}

        if browserName in browserNames:
            if browserName == GC.BROWSER_FIREFOX :
                self.driver = browserNames[browserName](options=self.__createOptions(browserName=browserName,
                                                                                     desiredCapabilities=desiredCapabilities),
                                                        executable_path=self.__findBrowserDriverPaths()+'/geckodriver')
            elif browserName == GC.BROWSER_CHROME:
                self.driver = browserNames[browserName](options=self.__createOptions(browserName=browserName,
                                                                                     desiredCapabilities=desiredCapabilities),
                                                        executable_path=self.__findBrowserDriverPaths()+'/chromedriver')
            elif browserName == GC.BROWSER_REMOTE:
                self.driver = browserNames[browserName](options=self.__createOptions(browserName=browserName,
                                                                                     desiredCapabilities=desiredCapabilities),
                                                        command_executor='http://localhost:4444/wd/hub',
                                                        desired_capabilities = desiredCapabilities)
        else:
            raise SystemExit("Browsername unknown")

        self.takeTime("Browser Start")

    def __findBrowserDriverPaths(self):
        lCurPath = os.getcwd()
        lCurPath = lCurPath.split("/baangt")[0]+"/baangt/browserDrivers/"

        return lCurPath

    def __createOptions(self, browserName, desiredCapabilities):
        if browserName == GC.BROWSER_CHROME:
            lOptions = ChromeOptions()
        elif browserName == GC.BROWSER_FIREFOX:
            lOptions = ffOptions()
        else:
            return None

        if not desiredCapabilities:
            return None

        if not isinstance(desiredCapabilities, dict):
            return None

        if desiredCapabilities.get(GC.BROWSER_MODE_HEADLESS):
            lOptions.headless = True

        return lOptions

    def closeBrowser(self):
        self.driver.quit()

    def __log(self, logType, logText, **kwargs):
        argsString = ""
        for key,value in kwargs.items():
            if value:
                argsString = argsString + f" {key}: {value}"
        # print(datetime.now(), logText, argsString)

        if logType == logging.ERROR:
            logger.error(logText + argsString)
        elif logType == logging.WARN:
            logger.warning(logText + argsString)
        elif logType == logging.INFO:
            logger.info(logText + argsString)
        elif logType == logging.CRITICAL:
            logger.critical(logText + argsString)
        elif logType == logging.DEBUG:
            logger.debug(logText + argsString)
        else:
            print(f"Unknown call to Logger: {logType}")

    def handleIframe(self, iframe = None):
        self.__log(logging.DEBUG, "Going into Iframe: ", **{"iframe": iframe})
        """Give an IFRAME and it will try to go into.
        If you're inside an iframe it will go out of the iframe"""
        if iframe:
            # frame_to_be_availble_and_switch_to_it doesn't work.
            mustEnd = time.time() + 300
            while time.time() < mustEnd:
                try:
                    self.driver.switch_to.default_content()
                    self.iframe = self.driver.switch_to.frame(iframe)
                    break
                except WebDriverException as e:
                    self.__log(logging.DEBUG, f"IFrame {iframe} not there yet - waiting 1 second")
                    time.sleep(1)
            if time.time() > mustEnd:
                raise TimeoutError

        elif self.iframe:
            self.driver.switch_to.default_content()
            self.iframe = None
        pass

    def handleWindow(self, windowNumber, function=None):
        if function == "close":
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        else:
            try:
                self.driver.switch_to.window(self.driver.window_handles[windowNumber])
            except Exception as e:
                logger.critical(f"Tried to switch to Window {windowNumber} but it's not there")
                raise Exceptions.baangtTestStepException(f"Window {windowNumber} doesn't exist")

    def findByAndWaitForValue(self, id = None,
                       css = None,
                       xpath = None,
                       class_name = None,
                       iframe = None,
                       timeout = 20):
        start = time.time()
        found = False
        duration = 0

        self.element = None
        self.findBy(id=id, css=css, xpath=xpath, class_name=class_name,
                    iframe=iframe)

        while not found and duration < timeout:
            try:
                if len(self.element.text) > 0:
                    return self.element.text
            except Exception as e:
                logger.debug(f"Exception during findByAndWaitForValue, but continuing {str(e)}")
                pass
            time.sleep(0.5)
            duration = time.time() - start

    def findByAndSetText(self,id = None,
                       css = None,
                       xpath = None,
                       class_name = None,
                       value = None,
                       iframe = None,
                       timeout = 60):
        self.findBy(id=id,
                    css=css,
                    xpath=xpath,
                    class_name=class_name,
                    iframe=iframe,
                    timeout=timeout)

        self.__doSomething(GC.CMD_SETTEXT, value=value, timeout=timeout, xpath=xpath)

    def findByAndSetTextValidated(self,id = None,
                       css = None,
                       xpath = None,
                       class_name = None,
                       value = None,
                       iframe = None,
                       timeout = 60,
                       retries = 5):

        tries = 0

        self.findBy(id=id,
                    css=css,
                    xpath=xpath,
                    class_name=class_name,
                    iframe=iframe,
                    timeout=timeout)

        while self.element.text != value and self.element.get_property("value") != value and tries < retries:

            self.__log(logging.DEBUG, f"Verified trying of SetText - iteration {tries} of {retries}")

            self.findByAndForceText(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe,
                                    value=value, timeout=timeout)

            self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

            tries += 1

    def submit(self):
        self.element.submit()

    def findByAndClick(self, id = None,
                       css = None,
                       xpath = None,
                       class_name = None,
                       iframe = None,
                       timeout = 60):
        critical_error = self.findBy(id = id,
                    css = css,
                    xpath=xpath,
                    class_name = class_name,
                    iframe=iframe,
                    timeout=timeout)

        if critical_error:
            logger.debug("findBy didn't work in findByAndClick")
            return

        self.__doSomething(GC.CMD_CLICK, xpath=xpath, timeout=timeout)

    def findByAndForceText(self, id=None, css=None, xpath=None, class_name=None, value=None,
                           iframe=None, timeout=60):

        self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

        self.__doSomething(GC.CMD_FORCETEXT, value=value, timeout=timeout, xpath=xpath)

    def findBy(self, id=None, css=None, xpath=None, class_name=None, iframe=None, timeout=60, loggingOn=True):

        if iframe:
            self.handleIframe(iframe)

        if loggingOn:
            self.__log(logging.DEBUG, "Locating Element", **{'id':id, 'css':css, 'xpath':xpath, 'class_name':class_name, 'iframe':iframe})

        return self.__tryAndRetry(id, css, xpath, class_name, timeout=timeout)

    def getURL(self):
        return self.driver.current_url

    def __tryAndRetry(self, id = None,
                      css = None,
                      xpath = None,
                      class_name = None,
                      timeout = 20):

        wasSuccessful = False
        begin = time.time()
        elapsed = 0

        while not wasSuccessful and elapsed < timeout:
            try:
                driverWait = WebDriverWait(self.driver, 20, poll_frequency=0.5)

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
                self.__log(logging.DEBUG, "Stale Element Exception - retrying")
                time.sleep(0.5)
            except ElementClickInterceptedException as e:
                self.__log(logging.DEBUG, "ElementClickIntercepted - retrying")
                time.sleep(0.5)
            except TimeoutException as e:
                self.__log(logging.WARNING, "TimoutException - retrying")
                time.sleep(0.5)
            except NoSuchElementException as e:
                self.__log(logging.WARNING, "Retrying Webdriver Exception:" + str(e))
                time.sleep(2)
            except InvalidSessionIdException as e:
                self.__log(logging.CRITICAL, "WebDriver Exception - terminating program: " + str(e))
                raise Exceptions.baangtTestStepException
            except NoSuchWindowException as e:
                self.__log(logging.CRITICAL, "WebDriver Exception - terminating program: " + str(e))
                raise Exceptions.baangtTestStepException
            except WebDriverException as e:
                self.__log(logging.ERROR, "Retrying WebDriver Exception: " + str(e))
                time.sleep(2)

            elapsed = time.time() - begin

        return wasSuccessful

    def findWaitNotVisible(self, xpath, timeout = 90):
        self.__log(logging.DEBUG, "Waiting for Element to disappear", **{"xpath":xpath, "timeout":timeout})
        time.sleep(0.5)

        stillHere = True
        elapsed = 0
        begin = time.time()

        while stillHere and elapsed < timeout:
            # self.CustomHandleZipkin()
            try:
                self.element = self.driver.find_element_by_xpath(xpath)
                time.sleep(0.1)
                elapsed = time.time() - begin
            except Exception as e:
                # Element gone - exit
                stillHere = False
        self.__log(logging.DEBUG, f"Element was gone after {format(elapsed, '.2f')} seconds")

    @staticmethod
    def sleep(sleepTimeinSeconds):
        time.sleep(sleepTimeinSeconds)

    def __doSomething(self, command, value=None, timeout=20, xpath=None):
        didWork = False
        elapsed = 0
        begin = time.time()

        while not didWork and elapsed < timeout:
            try:
                self.__log(logging.DEBUG, f"Do_something {command} with {value}")
                if command.upper() == GC.CMD_SETTEXT:
                    self.element.send_keys(value)
                elif command.upper() == GC.CMD_CLICK:
                    self.element.click()
                elif command.upper() == GC.CMD_FORCETEXT:
                    for i in range(0, 10):
                        self.element.send_keys(keys.Keys.BACKSPACE)
                    time.sleep(0.1)
                    self.element.send_keys(value)
                didWork = True
                return
            except ElementClickInterceptedException as e:
                self.__log(logging.DEBUG, "doSomething: Element intercepted - retry")
                time.sleep(0.2)
            except StaleElementReferenceException as e:
                self.__log(logging.DEBUG, "doSomething: Element stale - retry")
                time.sleep(0.2)
            except NoSuchElementException as e:
                self.__log(logging.DEBUG, "doSomething: Element not there yet - retry")
                time.sleep(0.5)
            except InvalidSessionIdException as e:
                self.__log(logging.ERROR, f"Invalid Session ID Exception caught - aborting... {e} ")
                raise Exceptions.baangtTestStepException
            elapsed = time.time()-begin
        raise Exceptions.baangtTestStepException(f"Action not possible after {timeout} s")

    def goToUrl(self, url):
        self.__log(logging.INFO, f'GoToUrl:{url}')
        try:
            self.driver.get(url)
        except WebDriverException as e:
            self.__log(logging.ERROR, f"Webpage {url} not reached. Error was: {e}")
            raise Exceptions.baangtTestStepException
        pass

    def javaScript(self, jsText):
        # self.driver.execute_async_script(jsText)
        self.driver.execute_script(jsText)
        # self.driver.execute(jsText)

