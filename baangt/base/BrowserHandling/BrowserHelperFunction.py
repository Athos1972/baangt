import os
#from selenium import webdriver
#from appium import webdriver as Appiumwebdriver
#from selenium.webdriver.support import expected_conditions as ec
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.chrome.options import Options as ChromeOptions
#from selenium.webdriver.firefox.options import Options as ffOptions
#from selenium.common.exceptions import *
#from selenium.webdriver.common import keys
#from baangt.base import GlobalConstants as GC
#from baangt.base.Timing.Timing import Timing#
#from baangt.TestSteps import Exceptions
#from baangt.base.DownloadFolderMonitoring import DownloadFolderMonitoring
#from baangt.base.Utils import utils
from baangt.base.ProxyRotate import ProxyRotate
import uuid
import time
import logging
from pathlib import Path
from baangt.base import GlobalConstants as GC
#import json
#import sys
#import platform
#import ctypes
#from urllib.request import urlretrieve
#import tarfile
#import zipfile
#import requests
from baangt.base.PathManagement import ManagedPaths
from dataclasses import dataclass



logger = logging.getLogger("pyC")

@dataclass
class BrowserDriverOptions:
    locatorType : str
    locator : str
    driver : None
    '''
    def __init__(self, locatorType=None, locator=None):
        self.locatorType = locatorType
        self.locator = locator
    '''


class BrowserHelperFunction:

    @staticmethod
    def browserHelper_setBrowserDownloadDirRandom():
        """
        Generate a new Directory for downloads. This needs to be specific for each browser session,
        so that we can know, which documents were created during this test case.
        :return:
        """
        randomValue = str(uuid.uuid4())
        downloadFolder = str(Path(ManagedPaths().getOrSetAttachmentDownloadPath()).joinpath(randomValue))
        Path(downloadFolder).mkdir(parents=True, exist_ok=True)

        logger.debug(f"Directory for download {downloadFolder}")
        return downloadFolder

    @staticmethod
    def browserHelper_startBrowsermobProxy(browserName, browserInstance, browserProxy):
        browserProxy.new_har(f"baangt-{browserName}-{browserInstance}",
                             options={'captureHeaders': True, 'captureContent': True}) if browserProxy else None



    @staticmethod
    def browserHelper_setSettingsRemoteV4(desiredCapabilities):
        seleniumGridIp = ""
        seleniumGridPort = ""
        desired_capabilities = {}
        if len(desiredCapabilities) > 0:
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

        return desired_capabilities, seleniumGridIp, seleniumGridPort

    @staticmethod
    def browserHelper_getBrowserExecutable(browserName):
        # Get executable
        executable = GC.GECKO_DRIVER
        if GC.BROWSER_FIREFOX == browserName:
            executable = GC.GECKO_DRIVER
        elif GC.BROWSER_CHROME == browserName:
            executable = GC.CHROME_DRIVER

        if 'NT' not in os.name.upper():
            executable = executable.split('.')[0]
        return executable

    @staticmethod
    def browserHelper_findBrowserDriverPaths(filename):

        lCurPath = Path(ManagedPaths().getOrSetDriverPath())
        lCurPath = lCurPath.joinpath(filename)

        logger.debug(f"Path for BrowserDrivers: {lCurPath}")
        return str(lCurPath)


    @staticmethod
    def browserHelper_log(logType, logText, browserOptions, cbTakeScreenshot = None, **kwargs):
        """
        Interal wrapper of Browser-Class for Logging. Takes a screenshot on Error and Warning.

        @param logType: any of logging.ERROR, logging.WARN, INFO, etc.
        @param logText: Text to log
        @param kwargs: Additional Arguments to be logged
        """
        argsString = ""
        xshot = "Couldn't take Screenshot"

        locatorType = browserOptions.locatorType
        locator = browserOptions.locator

        for key, value in kwargs.items():
            if value:
                argsString = argsString + f" {key}: {value}"

        if locator:
            argsString = argsString + f" Locator: {locatorType} = {locator}"

        if logType == logging.DEBUG:
            logger.debug(logText + argsString)
        elif logType == logging.ERROR:
            if cbTakeScreenshot is not None:
                xshot = cbTakeScreenshot()
            logger.error(logText + argsString + f" Screenshot: {xshot}")

        elif logType == logging.WARN:
            logger.warning(logText + argsString)
        elif logType == logging.INFO:
            logger.info(logText + argsString)
        elif logType == logging.CRITICAL:

            if cbTakeScreenshot is not None:
                xshot = cbTakeScreenshot()
            logger.critical(logText + argsString + f" Screenshot: {xshot}")
        else:
            print(f"Unknown call to Logger: {logType}")
            BrowserHelperFunction.browserHelper_log(logging.CRITICAL, f"Unknown type in call to logger: {logType}", browserOptions, cbTakeScreenshot = cbTakeScreenshot)


    @staticmethod
    def browserHelper_setProxyError(randomProxy):
        """
        Inform the central proxy service, that there was an error. OK, it might have been the page itself, that has
        an error and we'll never know. But more likely it's from the Proxy.
        :return:
        """
        if randomProxy:
            lProxyService = ProxyRotate()
            lProxyService.remove_proxy(ip=randomProxy["ip"], port=randomProxy["port"], type=randomProxy.get("type"))
