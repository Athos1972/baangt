import os
from selenium import webdriver
#from appium import webdriver as Appiumwebdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as ffOptions
from selenium.common.exceptions import *
from selenium.webdriver.common import keys
from baangt.base import GlobalConstants as GC
#from baangt.base.Timing.Timing import Timing
from baangt.TestSteps import Exceptions
#from baangt.base.DownloadFolderMonitoring import DownloadFolderMonitoring
from baangt.base.Utils import utils
#from baangt.base.ProxyRotate import ProxyRotate
#import uuid
import time
import logging
from pathlib import Path
import json
import sys
#import platform
#import ctypes
#from urllib.request import urlretrieve
#import tarfile
#import zipfile
#import requests


from baangt.base.BrowserHandling.BrowserHelperFunction import BrowserDriverOptions
from baangt.base.BrowserHandling.BrowserHelperFunction import BrowserHelperFunction as helper




logger = logging.getLogger("pyC")



class WebdriverFunctions:

    @staticmethod
    def webdriver_setFirefoxProfile(browserProxy, profile, randomProxy=None):
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
        if browserName == GC.BROWSER_CHROME:
            lOptions = ChromeOptions()
        elif browserName == GC.BROWSER_FIREFOX:
            lOptions = ffOptions()
        else:
            return None

        # Default Download Directory for Attachment downloads
        if browserName == GC.BROWSER_CHROME:
            prefs = {"plugins.plugins_disabled" : ["Chrome PDF Viewer"],
                     "plugins.always_open_pdf_externally": True,
                     "profile.default_content_settings.popups": 0,
                     "download.default_directory":
                         helper.browserHelper_setBrowserDownloadDirRandom(),  # IMPORTANT - ENDING SLASH V IMPORTANT
                     "directory_upgrade": True}
            lOptions.add_experimental_option("prefs", prefs)
            # Set Proxy for Chrome. First RandomProxy (External), if set. If not, then internal Browsermob
            if randomProxy:
                lOptions.add_argument(f"--proxy-server={randomProxy['ip']}:{randomProxy['port']}")
            elif browserMobProxy:
                lOptions.add_argument('--proxy-server={0}'.format(browserMobProxy.proxy))

        if not desiredCapabilities and not browserMobProxy:
            return None

        # sometimes instead of DICT comes a string with DICT-Format
        if isinstance(desiredCapabilities, str) and "{" in desiredCapabilities and "}" in desiredCapabilities:
            desiredCapabilities = json.loads(desiredCapabilities.replace("'", '"'))

        if not isinstance(desiredCapabilities, dict) and not browserMobProxy:
            return None

        if isinstance(desiredCapabilities, dict) and desiredCapabilities.get(GC.BROWSER_MODE_HEADLESS):
            logger.debug("Starting in Headless mode")
            lOptions.headless = True

        return lOptions


    @staticmethod
    def webdriver_getCurrentHTMLReference(driver):
        """
        Get a reference of the current HTML-Tag into self.html. We need that for stale check
        "waitForPageLoadAfterButtonClick"
        :return:
        """
        e = None
        retryCount = 0
        wasSuccessful = False
        while retryCount < 5 and not wasSuccessful:
            try:
                html = driver.find_element_by_tag_name('html')  # This is for waitForPageLoadAfterButton
                wasSuccessful = True
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

        if retryCount == 5:
            raise Exceptions.baangtTestStepException(f"Couldn't locate HTML element in Page. "
                                                     f"No idea what's going on. This was the last error"
                                                     f" (check logs for more): {e}")

        return html


    @staticmethod
    def webdriver_tryAndRetry(browserOptions, id=None, css=None, xpath=None, class_name=None, timeout=20, optional=False):
        """
        In: Locator
        Out: Boolean whether the element was found or not.

        Also sets the self.element for further use by other Methods (for instance to setText or read existing value)

        The method is resistant to common timing problems (can't work 100% of the time but will remove at least 80%
        of your pain compared to directly calling Selenium Methods).
        """

        element = None
        begin = time.time()
        elapsed = 0
        if timeout < 1.5:
            pollFrequency = timeout / 3
        else:
            pollFrequency = 0.5

        internalTimeout = timeout / 5

        lLoopCount = 0

        try:
            html = WebdriverFunctions.webdriver_getCurrentHTMLReference(browserOptions.driver)
        except BaseException as e:
            raise Exceptions.baangtTestStepException(f"__getCurrentHTMLReference was not successful: {e}")

        while element is None and elapsed < timeout:
            lLoopCount += 1
            try:
                driverWait = WebDriverWait(browserOptions.driver, timeout=internalTimeout, poll_frequency=pollFrequency)

                if id:
                    element = driverWait.until(ec.visibility_of_element_located((By.ID, id)))
                elif css:
                    element = driverWait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, css)))
                elif class_name:
                    element = browserOptions.driver.find_element_by_class_name(class_name)
                elif xpath:
                    # visibility of element sometimes not true, but still clickable. If we tried already
                    # 2 times with visibility, let's give it one more try with Presence of element
                    if lLoopCount > 1:
                        logger.debug(f"Tried 2 times to find visible element, now trying presence "
                                     f"of element instead, XPATH = {xpath}")
                        element = driverWait.until(ec.presence_of_element_located((By.XPATH, xpath)))
                    else:
                        element = driverWait.until(ec.visibility_of_element_located((By.XPATH, xpath)))
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
                helper.browserHelper_log(logging.CRITICAL, "WebDriver Exception - terminating testrun: " + str(e), browserOptions)
                raise Exceptions.baangtTestStepException
            except ElementNotInteractableException as e:
                logger.debug("Most probably timeout exception - retrying: " + str(e))
                time.sleep(pollFrequency)
            except WebDriverException as e:
                helper.browserHelper_log(logging.ERROR, "Retrying WebDriver Exception: " + str(e), browserOptions)
                time.sleep(2)

            elapsed = time.time() - begin

        return element, html


    @staticmethod
    def webdriver_doSomething(command, element, value=None, timeout=20, xpath=None, optional=False, browserOptions=None):
        """
        Will interact in an element (that was found before by findBy-Method and stored in self.element) as defined by
        ``command``.

        Command can be "SETTEXT" (GC.CMD_SETTEXT), "CLICK" (GC.CMD_CLICK), "FORCETEXT" (GC.CMD_FORCETEXT).

        Similarly to __try_and_retry the method is pretty robust when it comes to error handling of timing issues.

        """
        didWork = False
        elapsed = 0
        begin = time.time()
        counter = 0

        locatorType = browserOptions.locatorType
        locator = browserOptions.locator

        while not didWork and elapsed < timeout:
            counter += 1
            logger.debug(f"__doSomething {command} with {value}")
            try:
                if command.upper() == GC.CMD_SETTEXT:
                    element.send_keys(value)
                elif command.upper() == GC.CMD_CLICK:
                    element.click()
                elif command.upper() == GC.CMD_FORCETEXT:
                    element.clear()
                    for i in range(0, 10):
                        element.send_keys(keys.Keys.BACKSPACE)
                    time.sleep(0.1)
                    element.send_keys(value)
                didWork = True
                return
            except ElementClickInterceptedException as e:
                logger.debug("doSomething: Element intercepted - retry")
                time.sleep(0.2)
            except StaleElementReferenceException as e:
                logger.debug(f"doSomething: Element stale - retry {locatorType} {locator}")
                # If the element is stale after 2 times, try to re-locate the element
                if counter < 2:
                    time.sleep(0.2)
                elif counter < 4:
                    begin = WebdriverFunctions.webdriver_refindElementAfterError(browserOptions, timeout)
                else:
                    raise Exceptions.baangtTestStepException(e)
            except NoSuchElementException as e:
                logger.debug("doSomething: Element not there yet - retry")
                time.sleep(0.5)
            except InvalidSessionIdException as e:
                helper.browserHelper_log(logging.ERROR, f"Invalid Session ID Exception caught - aborting... {e} ", browserOptions)
                raise Exceptions.baangtTestStepException(e)
            except ElementNotInteractableException as e:
                if counter < 2:
                    logger.debug(f"Element not interactable {locatorType} {locator}, retrying")
                    time.sleep(0.2)
                elif counter < 5:
                    logger.debug(f"Element not interactable {locatorType} {locator}, re-finding element")
                    begin = WebdriverFunctions.webdriver_refindElementAfterError(browserOptions, timeout)
                else:
                    helper.browserHelper_log(logging.ERROR, f"Element not interactable {e}", browserOptions)
                    raise Exceptions.baangtTestStepException(e)
            except NoSuchWindowException as e:
                raise Exceptions.baangtTestStepException(e)
            elapsed = time.time() - begin

        if optional:
            logger.debug(
                f"Action not possible after {timeout} s, Locator: {locatorType}: {locator}, but flag 'optional' is set")
        else:
            raise Exceptions.baangtTestStepException(
                f"Action not possible after {timeout} s, Locator: {locatorType}: {locator}")

    @staticmethod
    def webdriver_refindElementAfterError(browserOptions, timeout):
        xpath, css, id = utils.setLocatorFromLocatorType(browserOptions.locatorType, browserOptions.locator)
        element = WebdriverFunctions.webdriver_tryAndRetry(browserOptions, xpath=xpath, css=css, id=id, timeout=timeout / 2, optional=True)
        if element is not None:
            logger.debug(f"Re-Found element {browserOptions.locatorType}: {browserOptions.locator}, will retry ")
            begin = time.time()
        else:
            raise Exceptions.baangtTestStepException(
                f"Element {browserOptions.locatorType} {browserOptions.locator} couldn't be found. "
                f"Tried to re-find it, but not element was not found")
        return begin