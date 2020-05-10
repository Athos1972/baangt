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
        self.driver : webdriver.firefox
        self.iFrame = None
        self.element = None
        self.locatorType = None
        self.locator = None
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

        ChromeExecutable, GeckoExecutable = BrowserDriver.__getBrowserExecutableNames()

        lCurPath = Path(self.managedPaths.getOrSetDriverPath())

        if browserName in browserNames:

            browserProxy = kwargs.get('browserProxy')
            browserInstance = kwargs.get('browserInstance', 'unknown')

            if browserName == GC.BROWSER_FIREFOX:
                lCurPath = lCurPath.joinpath(GeckoExecutable)

                if mobileType == 'True':
                    self.mobileConnectAppium(GeckoExecutable, browserName, desired_app, lCurPath, mobileApp,
                                             mobile_app_setting)
                else:
                    if not (os.path.isfile(str(lCurPath))):
                        self.downloadDriver(browserName)

                    profile = webdriver.FirefoxProfile()
                    profile = self.__setFirefoxProfile(browserProxy, profile, self.randomProxy)
                    logger.debug(f"Firefox Profile as follows:{profile.userPrefs}")

                    self.driver = browserNames[browserName](
                        options=self.__createBrowserOptions(browserName=browserName,
                                                            desiredCapabilities=desiredCapabilities),
                        executable_path=self.__findBrowserDriverPaths(GeckoExecutable),
                        firefox_profile=profile,
                        service_log_path=os.path.join(self.managedPaths.getLogfilePath(), 'geckodriver.log')
                        # ,
                        # log_path=os.path.join(self.managedPaths.getLogfilePath(),'firefox.log')
                    )
                    self.__startBrowsermobProxy(browserName=browserName, browserInstance=browserInstance,
                                                browserProxy=browserProxy)

            elif browserName == GC.BROWSER_CHROME:
                lCurPath = lCurPath.joinpath(ChromeExecutable)

                if mobileType == 'True':
                    self.mobileConnectAppium(ChromeExecutable, browserName, desired_app, mobileApp,
                                             mobile_app_setting)
                else:

                    if not (os.path.isfile(str(lCurPath))):
                        self.downloadDriver(browserName)

                    self.driver = browserNames[browserName](
                        chrome_options=self.__createBrowserOptions(browserName=browserName,
                                                                   desiredCapabilities=desiredCapabilities,
                                                                   browserMobProxy=browserProxy,
                                                                   randomProxy=self.randomProxy),
                        executable_path=self.__findBrowserDriverPaths(ChromeExecutable),
                        service_log_path=os.path.join(self.managedPaths.getLogfilePath(), 'chromedriver.log')
                    )
                    self.__startBrowsermobProxy(browserName=browserName, browserInstance=browserInstance,
                                                browserProxy=browserProxy)

            elif browserName == GC.BROWSER_EDGE:
                self.driver = browserNames[browserName](
                    executable_path=self.__findBrowserDriverPaths("msedgedriver.exe"))
            elif browserName == GC.BROWSER_SAFARI:
                # SAFARI doesn't provide any options, but desired_capabilities.
                # Executable_path = the standard safaridriver path.
                if len(desiredCapabilities) == 0:
                    desiredCapabilities = {}
                self.driver = browserNames[browserName](desired_capabilities=desiredCapabilities)

            elif browserName == GC.BROWSER_REMOTE:
                self.driver = browserNames[browserName](options=self.__createBrowserOptions(browserName=browserName,
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

            self.driver = webdriver.Remote(command_executor=serverUrl,
                                           desired_capabilities=desiredCapabilities)
        else:
            raise SystemExit("Browsername unknown")

        if self.downloadFolder:
            self.downloadFolderMonitoring = DownloadFolderMonitoring(self.downloadFolder)

        self.takeTime("Browser Start")

    def __setFirefoxProfile(self, browserProxy, profile, randomProxy=None):
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
        profile.set_preference("browser.download.dir", self.__setBrowserDownloadDirRandom())
        profile.set_preference("browser.download.manager.useWindow", False)
        profile.set_preference("browser.download.manager.focusWhenStarting", False)
        profile.set_preference("browser.download.manager.showAlertOnComplete", False)
        profile.set_preference("browser.download.manager.closeWhenDone", True)
        profile.set_preference("pdfjs.enabledCache.state", False)
        profile.set_preference("pdfjs.disabled", True) # This is nowhere on the Internet! But that did the trick!

        # Set volume to 0
        profile.set_preference("media.volume_scale", "0.0")
        return profile

    def __setBrowserDownloadDirRandom(self):
        """
        Generate a new Directory for downloads. This needs to be specific for each browser session,
        so that we can know, which documents were created during this test case.
        :return:
        """
        randomValue = str(uuid.uuid4())
        self.downloadFolder = str(Path(self.managedPaths.getOrSetAttachmentDownloadPath()).joinpath(randomValue))
        Path(self.downloadFolder).mkdir(parents=True, exist_ok=True)

        logger.debug(f"Directory for download {self.downloadFolder}")
        return self.downloadFolder


    def __startBrowsermobProxy(self, browserName, browserInstance, browserProxy):
        browserProxy.new_har(f"baangt-{browserName}-{browserInstance}",
                             options={'captureHeaders': True, 'captureContent': True}) if browserProxy else None

    @staticmethod
    def __getBrowserExecutableNames():
        GeckoExecutable = "geckodriver"
        ChromeExecutable = "chromedriver"
        if 'NT' in os.name.upper():
            GeckoExecutable = GeckoExecutable + ".exe"
            ChromeExecutable = ChromeExecutable + ".exe"
        return ChromeExecutable, GeckoExecutable

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
            self.driver = Appiumwebdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
        elif desired_app[GC.MOBILE_PLATFORM_NAME] == "iOS":
            desired_cap = desired_app
            if mobileApp == 'True':
                desired_cap['automationName'] = 'XCUITest'
                desired_cap['app'] = mobile_app_setting[GC.MOBILE_APP_URL]
            else:
                desired_cap['browserName'] = 'safari'
            self.driver = Appiumwebdriver.Remote("http://localhost:4723/wd/hub", desired_cap)

    def __findBrowserDriverPaths(self, filename):

        lCurPath = Path(self.managedPaths.getOrSetDriverPath())
        lCurPath = lCurPath.joinpath(filename)

        logger.debug(f"Path for BrowserDrivers: {lCurPath}")
        return str(lCurPath)

    def slowExecutionToggle(self, newSlowExecutionWaitTimeInSeconds=None):
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

    def __createBrowserOptions(self, browserName, desiredCapabilities, browserMobProxy=None, randomProxy=None):
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
                         self.__setBrowserDownloadDirRandom(),  # IMPORTANT - ENDING SLASH V IMPORTANT
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

    def closeBrowser(self):
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
        except Exception as ex:
            pass  # If the driver is already dead, it's fine.

    def _log(self, logType, logText, noScreenShot=False, **kwargs):
        """
        Interal wrapper of Browser-Class for Logging. Takes a screenshot on Error and Warning.

        @param logType: any of logging.ERROR, logging.WARN, INFO, etc.
        @param logText: Text to log
        @param kwargs: Additional Arguments to be logged
        """
        argsString = ""
        xshot = "Couldn't take Screenshot"

        for key, value in kwargs.items():
            if value:
                argsString = argsString + f" {key}: {value}"

        if self.locator:
            argsString = argsString + f" Locator: {self.locatorType} = {self.locator}"

        if logType == logging.DEBUG:
            logger.debug(logText + argsString)
        elif logType == logging.ERROR:
            if not noScreenShot:
                xshot = self.takeScreenshot()
            logger.error(logText + argsString + f" Screenshot: {xshot}")

        elif logType == logging.WARN:
            logger.warning(logText + argsString)
        elif logType == logging.INFO:
            logger.info(logText + argsString)
        elif logType == logging.CRITICAL:

            if not noScreenShot:
                xshot = self.takeScreenshot()
            logger.critical(logText + argsString + f" Screenshot: {xshot}")
        else:
            print(f"Unknown call to Logger: {logType}")
            self._log(logging.CRITICAL, f"Unknown type in call to logger: {logType}")

    def refresh(self):
        self.driver.execute_script("window.location.reload()")

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

    def handleWindow(self, windowNumber=None, function=None, timeout=20):
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
                try:
                    totalWindows = len(self.driver.window_handles)
                except BaseException as e:
                    logger.error(f"Tried to get amount of windows. Threw error {e}. Most probably browser crashed")
                    raise Exceptions.baangtTestStepException(f"Tried to get amount of windows. "
                                                             f"Threw error {e}. Most probably browser crashed")
                for windowHandle in self.driver.window_handles[-1:exceptHandles:-1]:
                    try:
                        self.driver.switch_to.window(windowHandle)
                        self.driver.close()
                    except NoSuchWindowException as e:
                        # If the window is already closed, it's fine. Don't do anything
                        pass
                try:
                    self.driver.switch_to.window(self.driver.window_handles[exceptHandles])
                except IndexError as e:
                    raise Exceptions.baangtTestStepException(f"Seems like the browser crashed. Main-Window lost")
        else:
            success = False
            duration = 0
            while not success and duration < timeout:
                try:
                    self.driver.switch_to.window(self.driver.window_handles[windowNumber])
                    success = True
                    continue
                except Exception as e:
                    logger.debug(f"Tried to switch to Window {windowNumber} but it's not there yet")

                self.sleep(1)
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
                elif self.element.tag_name == 'input':
                    #  element is of type <input />
                    return self.element.get_property('value')

            except Exception as e:
                logger.debug(f"Exception during findByAndWaitForValue, but continuing {str(e)}, "
                             f"Locator: {self.locatorType} = {self.locator}")
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

    def findByAndClick(self, id=None, css=None, xpath=None, class_name=None, iframe=None, timeout=20, optional=False):
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
            return False

        if len(value) == 0:
            return False

        if str(value) == "0":
            return False

        return self.findByAndClick(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout,
                                   optional=optional)

    def findByAndForceText(self, id=None, css=None, xpath=None, class_name=None, value=None,
                           iframe=None, timeout=60, optional=False):
        """
        Convenience Method. Please see documentation in findBy and __doSomething.

        """

        self.findBy(id=id, css=css, xpath=xpath, class_name=class_name, iframe=iframe, timeout=timeout)

        self.__doSomething(GC.CMD_FORCETEXT, value=value, timeout=timeout, xpath=xpath, optional=optional)

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

        self.driver.set_window_size(width, height)
        size = self.driver.get_window_size()
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
            logger.debug(f"Locating Element {self.locatorType} = {self.locator}")

        successful = self.__tryAndRetry(id, css, xpath, class_name, timeout=timeout, optional=optional)

        if not successful and not optional:
            raise Exceptions.baangtTestStepException(f"Element {self.locatorType} = {self.locator} could not be found "
                                                     f"within timeout of {timeout}")
        return successful

    def getURL(self):
        """

        @return: the current URL/URI of the current Tab of the current Browser
        """
        return self.driver.current_url

    def __tryAndRetry(self, id=None, css=None, xpath=None, class_name=None, timeout=20, optional=False):
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

        internalTimeout = timeout / 5

        lLoopCount = 0

        try:
            self.__getCurrentHTMLReference()
        except BaseException as e:
            raise Exceptions.baangtTestStepException(f"__getCurrentHTMLReference was not successful: {e}")

        while not wasSuccessful and elapsed < timeout:
            lLoopCount += 1
            try:
                driverWait = WebDriverWait(self.driver, timeout=internalTimeout, poll_frequency=pollFrequency)

                if id:
                    self.element = driverWait.until(ec.visibility_of_element_located((By.ID, id)))
                elif css:
                    self.element = driverWait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, css)))
                elif class_name:
                    self.element = self.driver.find_element_by_class_name(class_name)
                elif xpath:
                    # visibility of element sometimes not true, but still clickable. If we tried already
                    # 2 times with visibility, let's give it one more try with Presence of element
                    if lLoopCount > 1:
                        logger.debug(f"Tried 2 times to find visible element, now trying presence "
                                     f"of element instead, XPATH = {xpath}")
                        self.element = driverWait.until(ec.presence_of_element_located((By.XPATH, xpath)))
                    else:
                        self.element = driverWait.until(ec.visibility_of_element_located((By.XPATH, xpath)))

                wasSuccessful = True
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
                self._log(logging.CRITICAL, "WebDriver Exception - terminating testrun: " + str(e))
                raise Exceptions.baangtTestStepException
            except ElementNotInteractableException as e:
                logger.debug("Most probably timeout exception - retrying: " + str(e))
                time.sleep(pollFrequency)
            except WebDriverException as e:
                self._log(logging.ERROR, "Retrying WebDriver Exception: " + str(e))
                time.sleep(2)

            elapsed = time.time() - begin

        return wasSuccessful

    def __getCurrentHTMLReference(self):
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
                self.html = self.driver.find_element_by_tag_name('html')  # This is for waitForPageLoadAfterButton
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
            self.sleep(0.5)

        if retryCount == 5:
            raise Exceptions.baangtTestStepException(f"Couldn't locate HTML element in Page. "
                                                     f"No idea what's going on. This was the last error"
                                                     f" (check logs for more): {e}")

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
                    self.element = self.driver.find_element_by_xpath(xpath)
                elif id:
                    self.element = self.driver.find_element_by_id(id)
                elif css:
                    self.element = self.driver.find_element_by_css_selector(css)
                time.sleep(0.2)
                elapsed = time.time() - begin
            except Exception as e:
                # Element gone - exit
                stillHere = False
                self._log(logging.DEBUG, f"Element was gone after {format(elapsed, '.2f')} seconds")
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
        links = self.driver.find_elements_by_css_selector("a")
        logger.debug(f"Checking links on page {self.driver.current_url}")
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
        counter = 0

        while not didWork and elapsed < timeout:
            counter += 1
            logger.debug(f"__doSomething {command} with {value}")
            try:
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
                logger.debug("doSomething: Element intercepted - retry")
                time.sleep(0.2)
            except StaleElementReferenceException as e:
                logger.debug(f"doSomething: Element stale - retry {self.locatorType} {self.locator}")
                # If the element is stale after 2 times, try to re-locate the element
                if counter < 2:
                    time.sleep(0.2)
                elif counter < 4:
                    begin = self.refindElementAfterError(timeout)
                else:
                    raise Exceptions.baangtTestStepException(e)
            except NoSuchElementException as e:
                logger.debug("doSomething: Element not there yet - retry")
                time.sleep(0.5)
            except InvalidSessionIdException as e:
                self._log(logging.ERROR, f"Invalid Session ID Exception caught - aborting... {e} ")
                raise Exceptions.baangtTestStepException(e)
            except ElementNotInteractableException as e:
                if counter < 2:
                    logger.debug(f"Element not interactable {self.locatorType} {self.locator}, retrying")
                    time.sleep(0.2)
                elif counter < 5:
                    logger.debug(f"Element not interactable {self.locatorType} {self.locator}, re-finding element")
                    begin = self.refindElementAfterError(timeout)
                else:
                    self._log(logging.ERROR, f"Element not interactable {e}")
                    raise Exceptions.baangtTestStepException(e)
            except NoSuchWindowException as e:
                raise Exceptions.baangtTestStepException(e)
            elapsed = time.time() - begin

        if optional:
            logger.debug(
                f"Action not possible after {timeout} s, Locator: {self.locatorType}: {self.locator}, but flag 'optional' is set")
        else:
            raise Exceptions.baangtTestStepException(
                f"Action not possible after {timeout} s, Locator: {self.locatorType}: {self.locator}")

    def refindElementAfterError(self, timeout):
        xpath, css, id = utils.setLocatorFromLocatorType(self.locatorType, self.locator)
        foundNow = self.findBy(xpath=xpath, css=css, id=id, optional=True, timeout=timeout / 2)
        if foundNow:
            logger.debug(f"Re-Found element {self.locatorType}: {self.locator}, will retry ")
            begin = time.time()
        else:
            raise Exceptions.baangtTestStepException(
                f"Element {self.locatorType} {self.locator} couldn't be found. "
                f"Tried to re-find it, but not element was not found")
        return begin

    def waitForElementChangeAfterButtonClick(self, timeout=5):
        """
        Wait for a stale element (in a good way). Stale means, that the object has changed.

        old element is in self.element
        old locator is in self.locatorType and self.locator

        :param timeout:
        :return:
        """

        lOldElement = self.element.id

        lStartOfWaiting = time.time()
        elapsed = 0

        logger.debug("Starting")

        xpath, css, id = utils.setLocatorFromLocatorType(self.locatorType, self.locator)

        while elapsed < timeout:
            lFound = self.findBy(xpath=xpath, css=css, id=id, timeout=0.5, optional=True)
            if not lFound:
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
            lHTML = self.driver.find_element_by_tag_name("html")
            if lHTML != self.html:
                logger.debug("Page was reloaded")
                return True

            time.sleep(0.2)

            elapsed = time.time() - lStartOfWaiting

        logger.debug("No Page reload detected by this method")
        return False    # There was no changed HTML

    def goToUrl(self, url):
        self._log(logging.INFO, f'GoToUrl:{url}')
        try:
            if self.browserName==GC.BROWSER_FIREFOX:
                self.driver.set_context("content")
            self.driver.get(url)
            self.setZoomFactor()
        except WebDriverException as e:
            # Use noScreenshot-Parameter as otherwise we'll try on a dead browser to create a screenshot
            self._log(logging.ERROR, f"Webpage {url} not reached. Error was: {e}", noScreenShot=True)
            self.__setProxyError()
            raise Exceptions.baangtTestStepException
        except Exception as e:
            # Use noScreenshot-Parameter as otherwise we'll try on a dead browser to create a screenshot
            self._log(logging.ERROR, f"Webpage {url} throws error {e}", noScreenShot=True)
            self.__setProxyError()
            raise Exceptions.baangtTestStepException(url, e)

    def __setProxyError(self):
        """
        Inform the central proxy service, that there was an error. OK, it might have been the page itself, that has
        an error and we'll never know. But more likely it's from the Proxy.
        :return:
        """
        if self.randomProxy:
            lProxyService = ProxyRotate()
            lProxyService.remove_proxy(ip=self.randomProxy["ip"], port=self.randomProxy["port"],
                                       type=self.randomProxy.get("type"))

    def goBack(self):
        """
        Method to go 1 step back in current tab's browse history
        @return:
        """
        try:
            self.javaScript("window.history.go(-1)")
        except Exception as e:
            self._log(logging.WARNING, f"Tried to go back in history, didn't work with error {e}")

    def javaScript(self, jsText, *args):
        """Execute a given JavaScript in the current Session"""
        self.driver.execute_script(jsText, *args)

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
            self.driver.get("chrome://settings/")
            self.driver.execute_script(f"chrome.settingsPrivate.setDefaultZoom({self.zoomFactorDesired/100});")
            logger.debug(f"CHROME: Set default zoom using JS-Method to {self.zoomFactorDesired/100}")
            return True

        if self.browserName == GC.BROWSER_FIREFOX:
            self.driver.set_context("chrome")                # !sic: in Firefox.. Whatever...

        if self.zoomFactorDesired > 100:
            lZoomKey = "+"
        else:
            lZoomKey = "-"

        # E.g. current = 100. Desired = 67%: 100-67 = 33. 33/10 = 3.3  int(3.3) = 3 --> he'll hit 3 times CTRL+"-"
        lDifference = abs(100 - self.zoomFactorDesired)
        lHitKeyTimes = int(lDifference/10)

        try:
            lWindow = self.driver.find_element_by_tag_name("html")
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
                self.driver.set_context("content")

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