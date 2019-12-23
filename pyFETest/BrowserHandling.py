import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.common import keys
from . import GlobalConstants as GC
import time
from datetime import timedelta
import logging
import sys

logger = logging.getLogger("pyC")

class BrowserDriver:
    def __init__(self):
        self.driver : webdriver.Firefox = None
        self.iframe = None
        self.element = None
        self.timeout = 2000   # Default Timeout in Milliseconds
        self.timing = {}
        self.currentTimingSection = None

    def takeTime(self, timingName):
        if timingName in self.timing:
            self.timing[timingName][GC.TIMING_END] = time.time()
            return str(timedelta(seconds=self.timing[timingName]["end"] - self.timing[timingName][GC.TIMING_START]))
        else:
            self.timing[timingName] = {}
            self.timing[timingName][GC.TIMING_START] = time.time()
            self.currentTimingSection = timingName

    def takeTimeSumOutput(self):
        print("-------------------")
        print("Timing")
        for key, value in self.timing.items():
            if "end" in value.keys():
                print(f'{key} : {value[GC.TIMING_END] - value[GC.TIMING_START]}')
                self.__log(logging.INFO, f'{key} : {value[GC.TIMING_END] - value[GC.TIMING_START]}')

    def returnTime(self):
        timingString = ""
        for key,value in self.timing.items():
            if GC.TIMING_END in value.keys():
                timingString = timingString + "\n" + f'{key}: , since last call: ' \
                                                     f'{value[GC.TIMING_END] - value[GC.TIMING_START]}'
                if "timestamp" in value.keys():
                    timingString = timingString + ", TS:" + str(value[GC.TIMESTAMP])
        return timingString

    def resetTime(self):
        if "Testrun complete" in self.timing:
            buffer = self.timing["Testrun complete"]
            self.timing = {}
            self.timing["Testrun complete"] = buffer
        else:
            self.timing = {}

    def createNewBrowser(self, browserName):
        self.takeTime("Browser Start")
        browserNames = {
            GC.BROWSER_FIREFOX: webdriver.Firefox,
            GC.BROWSER_CHROME: webdriver.Chrome,
            GC.BROWSER_SAFARI: webdriver.Safari}

        if browserName in browserNames:
            if browserName == GC.BROWSER_FIREFOX :
                self.driver = browserNames[browserName](executable_path=os.getcwd()+'/geckodriver')
            elif browserName == GC.BROWSER_CHROME:
                self.driver = browserNames[browserName](executable_path=os.getcwd()+'/chromedriver')
        else:
            raise SystemExit("Browsername unknown")

        self.takeTime("Browser Start")

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
            self.driver.switch_to.window(self.driver.window_handles[windowNumber])

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
                pass
            time.sleep(0.5)
            duration = time.time() - start

    def findByAndSetText(self,id = None,
                       css = None,
                       xpath = None,
                       class_name = None,
                       value = None,
                       iframe = None,
                       timeout = 20):
        self.findBy(id=id,
                    css=css,
                    xpath=xpath,
                    class_name=class_name,
                    iframe=iframe)

        self.doSomething(GC.CMD_SETTEXT, value=value, timeout=timeout)

    def findByAndClick(self, id = None,
                       css = None,
                       xpath = None,
                       class_name = None,
                       iframe = None):
        critical_error = self.findBy(id = id,
                    css = css,
                    xpath=xpath,
                    class_name = class_name,
                    iframe=iframe)

        self.doSomething(GC.CMD_CLICK)

    def findBy(self, id = None,
               css = None,
               xpath = None,
               class_name = None,
               iframe = None,
               # command = None,
               # value = None,
               loggingOn=True):

        if iframe:
            self.handleIframe(iframe)

        if loggingOn:
            self.__log(logging.INFO, "Locating Element", **{'id':id, 'css':css, 'xpath':xpath, 'class_name':class_name, 'iframe':iframe})

        return self.__tryAndRetry(id, css, xpath, class_name)

    def __tryAndRetry(self, id = None,
                      css = None,
                      xpath = None,
                      class_name = None,
                      timeout = 20):

        success = False
        begin = time.time()
        elapsed = 0

        while not success and elapsed < timeout:
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
                success = True
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
                sys.exit()
            except NoSuchWindowException as e:
                self.__log(logging.CRITICAL, "WebDriver Exception - terminating program: " + str(e))
                sys.exit()
            except WebDriverException as e:
                self.__log(logging.ERROR, "Retrying WebDriver Exception: " + str(e))
                time.sleep(2)

            elapsed = time.time() - begin

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
        self.__log(logging.INFO, f"Element was gone after {elapsed} seconds")

    @staticmethod
    def sleep(sleepTimeinSeconds):
        time.sleep(sleepTimeinSeconds)

    def doSomething(self, command, value=None, timeout=20):
        didWork = False
        elapsed = 0
        begin = time.time()

        while not didWork and elapsed < timeout:
            try:
                if command.upper() == GC.CMD_SETTEXT:
                    self.element.send_keys(value)
                elif command.upper() == GC.CMD_CLICK:
                    self.element.click()
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
            elapsed = time.time()-begin

    def goToUrl(self, url):
        self.__log(logging.INFO, f'GoToUrl:{url}')
        self.driver.get(url)
        pass

    def javaScript(self, jsText):
        # self.driver.execute_async_script(jsText)
        self.driver.execute_script(jsText)
        # self.driver.execute(jsText)

