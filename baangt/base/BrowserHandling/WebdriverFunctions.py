import os
from selenium import webdriver
from appium import webdriver as Appiumwebdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as ffOptions
from selenium.common.exceptions import *
from selenium.webdriver.common import keys
from baangt.base import GlobalConstants as GC
from baangt.TestSteps import Exceptions
from baangt.base.Utils import utils
from baangt.base.BrowserHandling.BrowserHelperFunction import BrowserDriverData
from baangt.base.BrowserHandling.BrowserHelperFunction import BrowserHelperFunction as helper
import time
import logging
from pathlib import Path
import json
import sys

logger = logging.getLogger("pyC")

class WebdriverFunctions:
    """
    The webdriverclass for BrowserHandling to interact with selenium webdriver.
    """

    BROWSER_DRIVERS = {
        GC.BROWSER_FIREFOX: webdriver.Firefox,
        GC.BROWSER_CHROME: webdriver.Chrome,
        GC.BROWSER_SAFARI: webdriver.Safari,
        GC.BROWSER_EDGE: webdriver.Edge,
        GC.BROWSER_REMOTE: webdriver.Remote,
        GC.BROWSER_APPIUM : Appiumwebdriver.Remote
    }

    @staticmethod
    def getDownloadFolderFromProfile(profile: webdriver.FirefoxProfile):
        return profile.__getattribute__("default_preferences")["browser.download.dir"]

    @staticmethod
    def webdriver_setFirefoxProfile(browserProxy, randomProxy=None):
        profile = webdriver.FirefoxProfile()
        if browserProxy:
            profile.set_proxy(browserProxy.selenium_proxy())

        if randomProxy:
            """
            from selenium import webdriver
            return webdriver.Proxy({
                "httpProxy": self.proxy,
                "sslProxy": self.proxy,
            })
            """
            # We shall use a random Proxy from the list:
            PROXY = f"{randomProxy['ip']}:{randomProxy['port']}"

            logger.info(f"Using Proxy-Server: {PROXY}")

            ffProxy = webdriver.Proxy( {
                        "httpProxy":PROXY,
                        "ftpProxy":PROXY,
                        "sslProxy":PROXY,
                        "noProxy":None,
                        "proxy_type":"MANUAL",
                        "proxyType":"MANUAL",
                        "class":"org.openqa.selenium.Proxy",
                        "autodetect":False
                        })

            profile.set_proxy(ffProxy)

        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.manager.showAlertOnComplete", False)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk',
                            'application/octet-stream,application/pdf,application/x-pdf,application/vnd.pdf,application/zip,application/octet-stream,application/x-zip-compressed,multipart/x-zip,application/x-rar-compressed, application/octet-stream,application/msword,application/vnd.ms-word.document.macroEnabled.12,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-excel,application/pdf,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/rtf,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel,application/vnd.ms-word.document.macroEnabled.12,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/xls,application/msword,text/csv,application/vnd.ms-excel.sheet.binary.macroEnabled.12,text/plain,text/csv/xls/xlsb,application/csv,application/download,application/vnd.openxmlformats-officedocument.presentationml.presentation,application/octet-stream')
        profile.set_preference('browser.helperApps.neverAsk.openFile',
                            'application/octet-stream,application/pdf,application/x-pdf,application/vnd.pdf,application/zip,application/octet-stream,application/x-zip-compressed,multipart/x-zip,application/x-rar-compressed, application/octet-stream,application/msword,application/vnd.ms-word.document.macroEnabled.12,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-excel,application/pdf,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/rtf,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel,application/vnd.ms-word.document.macroEnabled.12,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/xls,application/msword,text/csv,application/vnd.ms-excel.sheet.binary.macroEnabled.12,text/plain,text/csv/xls/xlsb,application/csv,application/download,application/vnd.openxmlformats-officedocument.presentationml.presentation,application/octet-stream')
        profile.set_preference("browser.download.dir", helper.browserHelper_setBrowserDownloadDirRandom())
        profile.set_preference("browser.download.manager.useWindow", False)
        profile.set_preference("browser.download.manager.focusWhenStarting", False)
        profile.set_preference("browser.download.manager.showAlertOnComplete", False)
        profile.set_preference("browser.download.manager.closeWhenDone", True)
        profile.set_preference("pdfjs.enabledCache.state", False)
        profile.set_preference("pdfjs.disabled", True) # This is nowhere on the Internet! But that did the trick!

        # Set volume to 0
        profile.set_preference("media.volume_scale", "0.0")
        return profile

    @staticmethod
    def webdriver_createBrowserOptions(browserName, desiredCapabilities, browserMobProxy=None, randomProxy=None):
        """
        Translates desired capabilities from the Testrun (or globals) into specific BrowserOptions for the
        currently active browser

        @param browserName: any of the GC.BROWSER*
        @param desiredCapabilities: Settings from TestRun or globals
        @param browserMobProxy: Proxy-Server IP+Port of internal BrowserMobProxy.
        @param randomProxy: Proxy-Server IP+Port of random external Proxy
        @return: the proper BrowserOptions for the currently active browser.
        """

        # Default Download Directory for Attachment downloads
        if browserName == GC.BROWSER_CHROME:
            lOptions = ChromeOptions()
            prefs = {"plugins.plugins_disabled" : ["Chrome PDF Viewer"],
                     "plugins.always_open_pdf_externally": True,
                     "profile.default_content_settings.popups": 0,
                     "download.default_directory": helper.browserHelper_setBrowserDownloadDirRandom(),  # IMPORTANT - ENDING SLASH V IMPORTANT
                     "directory_upgrade": True}
            lOptions.add_experimental_option("prefs", prefs)
            # Set Proxy for Chrome. First RandomProxy (External), if set. If not, then internal Browsermob
            if randomProxy:
                lOptions.add_argument(f"--proxy-server={randomProxy['ip']}:{randomProxy['port']}")
            elif browserMobProxy:
                lOptions.add_argument('--proxy-server={0}'.format(browserMobProxy.proxy))
        elif browserName == GC.BROWSER_FIREFOX:
            lOptions = ffOptions()
        else:
            lOptions = None

        if desiredCapabilities and lOptions:
            # sometimes instead of DICT comes a string with DICT-Format
            if isinstance(desiredCapabilities, str) and "{" in desiredCapabilities and "}" in desiredCapabilities:
                desiredCapabilities = json.loads(desiredCapabilities.replace("'", '"'))

            if isinstance(desiredCapabilities, dict):
                if desiredCapabilities.get(GC.BROWSER_MODE_HEADLESS):
                    logger.debug("Starting in Headless mode")
                    lOptions.headless = True
                else:
                    # statement not matched
                    pass
            else:
                # statement not matched
                pass
        else:
            # statement not matched
            pass

        return lOptions

    @staticmethod
    def getDownloadFolderFromChromeOptions(options: ChromeOptions):
        return options.__getattribute__("experimental_options")["prefs"]["download.default_directory"]

    @staticmethod
    def webdriver_getCurrentHTMLReference(driver):
        """
        Get a reference of the current HTML-Tag into self.html. We need that for stale check
        "waitForPageLoadAfterButtonClick"
        :return:
        """
        RETRY_COUNTER_LIMIT = 5
        e = None
        html = None
        retryCount = 0

        while retryCount < RETRY_COUNTER_LIMIT and not html:
            try:
                html = driver.find_element_by_tag_name('html')  # This is for waitForPageLoadAfterButton
            except NoSuchElementException as e:
                logger.debug(f"had a NoSuchElementException: {e}")
            except NoSuchWindowException as e:
                logger.debug(f"had a noSuchWindowException: {e}")
            except WebDriverException as e:
                logger.debug(f"had a WebDriverException: {e}")
            except BaseException as e:
                logger.warning(f"had an unknown exception (should be checked): {e}")

            retryCount += 1
            time.sleep(0.5)

        if retryCount >= RETRY_COUNTER_LIMIT:
            raise Exceptions.baangtTestStepException(f"Couldn't locate HTML element in Page. "
                                                     f"No idea what's going on. This was the last error"
                                                     f" (check logs for more): {e}")

        return html


    @staticmethod
    def webdriver_tryAndRetry(browserData, timeout=20, optional=False):
        """
        In: Locator
        Out: Boolean whether the element was found or not.

        Also sets the self.element for further use by other Methods (for instance to setText or read existing value)

        The method is resistant to common timing problems (can't work 100% of the time but will remove at least 80%
        of your pain compared to directly calling Selenium Methods).
        """
        REQUEST_TIMEOUT_MINIMUM = 1.5
        REQUEST_POLL_FREQUENCY = 0.5

        element = None
        html = None
        begin = time.time()
        elapsed = 0
        if timeout < REQUEST_TIMEOUT_MINIMUM:
            pollFrequency = timeout / 3
        else:
            pollFrequency = REQUEST_POLL_FREQUENCY

        internalTimeout = timeout / 5

        lLoopCount = 0

        try:
            html = WebdriverFunctions.webdriver_getCurrentHTMLReference(browserData.driver)
        except BaseException as e:
            raise Exceptions.baangtTestStepException(f"__getCurrentHTMLReference was not successful: {e}")

        while not element and elapsed < timeout:
            lLoopCount += 1
            try:
                driverWait = WebDriverWait(browserData.driver, timeout=internalTimeout, poll_frequency=pollFrequency)

                if By.ID == browserData.locatorType or By.CSS_SELECTOR == browserData.locatorType:
                    element = driverWait.until(ec.visibility_of_element_located((browserData.locatorType, browserData.locator)))
                elif By.CLASS_NAME == browserData.locatorType:
                    element = browserData.driver.find_element_by_class_name(browserData.locator)
                elif By.XPATH == browserData.locatorType:
                    # visibility of element sometimes not true, but still clickable. If we tried already
                    # 2 times with visibility, let's give it one more try with Presence of element
                    if lLoopCount > 1:
                        logger.debug(f"Tried 2 times to find visible element, now trying presence "
                                     f"of element instead, XPATH = {browserData.locator}")
                        element = driverWait.until(ec.presence_of_element_located((browserData.locatorType, browserData.locator)))
                    else:
                        element = driverWait.until(ec.visibility_of_element_located((browserData.locatorType, browserData.locator)))
            except StaleElementReferenceException as e:
                logger.debug("Stale Element Exception - retrying " + str(e))
                time.sleep(pollFrequency)
            except ElementClickInterceptedException as e:
                logger.debug("ElementClickIntercepted - retrying " + str(e))
                time.sleep(pollFrequency)
            except TimeoutException as e:
                logger.debug("TimoutException - retrying " + str(e))
                time.sleep(pollFrequency)
            except NoSuchElementException as e:
                logger.debug("Retrying Webdriver Exception: " + str(e))
                time.sleep(pollFrequency)
            except InvalidSessionIdException as e:
                logger.debug("WebDriver Exception - terminating testrun: " + str(e))
                raise Exceptions.baangtTestStepException
            except NoSuchWindowException as e:
                helper.browserHelper_log(logging.CRITICAL, "WebDriver Exception - terminating testrun: " + str(e), browserData)
                raise Exceptions.baangtTestStepException
            except ElementNotInteractableException as e:
                logger.debug("Most probably timeout exception - retrying: " + str(e))
                time.sleep(pollFrequency)
            except WebDriverException as e:
                helper.browserHelper_log(logging.ERROR, "Retrying WebDriver Exception: " + str(e), browserData)
                time.sleep(2)

            elapsed = time.time() - begin

        return element, html


    @staticmethod
    def webdriver_doSomething(command, element, value=None, timeout=20, optional=False, browserData=None):
        """
        Will interact in an element (that was found before by findBy-Method and stored in self.element) as defined by
        ``command``.

        Command can be "SETTEXT" (GC.CMD_SETTEXT), "CLICK" (GC.CMD_CLICK), "FORCETEXT" (GC.CMD_FORCETEXT).

        Similarly to __try_and_retry the method is pretty robust when it comes to error handling of timing issues.

        """
        NUMBER_OF_SEND_KEY_BACKSPACE = 10
        COUNTER_LIMIT_RETRY = 2
        COUNTER_LIMIT_ELEMENT_REF = 4
        COUNTER_LIMIT_ELEMENT_NOT_INTERACT = 5

        didWork = False
        elapsed = 0
        counter = 0
        begin = time.time()

        while not didWork and elapsed < timeout:
            counter += 1
            logger.debug(f"__doSomething {command} with {value}")
            try:
                if command.upper() == GC.CMD_SETTEXT:
                    if not value:
                        value = ""
                    element.send_keys(value)
                elif command.upper() == GC.CMD_CLICK:
                    element.click()
                elif command.upper() == GC.CMD_FORCETEXT:
                    element.clear()
                    for i in range(0, NUMBER_OF_SEND_KEY_BACKSPACE):
                        element.send_keys(keys.Keys.BACKSPACE)
                    time.sleep(0.1)
                    element.send_keys(value)
                didWork = True
            except ElementClickInterceptedException as e:
                logger.debug("doSomething: Element intercepted - retry")
                time.sleep(0.2)
            except StaleElementReferenceException as e:
                logger.debug(f"doSomething: Element stale - retry {browserData.locatorType} {browserData.locator}")
                # If the element is stale after 2 times, try to re-locate the element
                if counter < COUNTER_LIMIT_RETRY:
                    time.sleep(0.2)
                elif counter < COUNTER_LIMIT_ELEMENT_REF:
                    begin, element = WebdriverFunctions.webdriver_refindElementAfterError(browserData, timeout)
                else:
                    raise Exceptions.baangtTestStepException(e)
            except NoSuchElementException as e:
                logger.debug("doSomething: Element not there yet - retry")
                time.sleep(0.5)
            except InvalidSessionIdException as e:
                helper.browserHelper_log(logging.ERROR, f"Invalid Session ID Exception caught - aborting... {e} ", browserData)
                raise Exceptions.baangtTestStepException(e)
            except ElementNotInteractableException as e:
                if counter < COUNTER_LIMIT_RETRY:
                    logger.debug(f"Element not interactable {browserData.locatorType} {browserData.locator}, retrying")
                    time.sleep(0.2)
                elif counter < COUNTER_LIMIT_ELEMENT_NOT_INTERACT:
                    logger.debug(f"Element not interactable {browserData.locatorType} {browserData.locator}, re-finding element")
                    begin, element = WebdriverFunctions.webdriver_refindElementAfterError(browserData, timeout)
                else:
                    helper.browserHelper_log(logging.ERROR, f"Element not interactable {e}", browserData)
                    raise Exceptions.baangtTestStepException(e)
            except NoSuchWindowException as e:
                raise Exceptions.baangtTestStepException(e)
            elapsed = time.time() - begin

        if not didWork:
            if optional:
                logger.debug(
                    f"Action not possible after {timeout} s, Locator: {browserData.locatorType}: {browserData.locator}, but flag 'optional' is set")
            else:
                raise Exceptions.baangtTestStepException(f"Action not possible after {timeout} s, Locator: {browserData.locatorType}: {browserData.locator}")
        else:
            # Function successful
            pass

        return didWork

    @staticmethod
    def webdriver_refindElementAfterError(browserData, timeout):
        element, _ = WebdriverFunctions.webdriver_tryAndRetry(browserData, timeout=timeout / 2, optional=True)
        if element:
            logger.debug(f"Re-Found element {browserData.locatorType}: {browserData.locator}, will retry ")
            begin = time.time()
        else:
            raise Exceptions.baangtTestStepException(
                f"Element {browserData.locatorType} {browserData.locator} couldn't be found. "
                f"Tried to re-find it, but not element was not found")
        return begin, element