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
    def browserHelper_getBrowserExecutableNames():
        GeckoExecutable = "geckodriver"
        ChromeExecutable = "chromedriver"
        if 'NT' in os.name.upper():
            GeckoExecutable = GeckoExecutable + ".exe"
            ChromeExecutable = ChromeExecutable + ".exe"
        return ChromeExecutable, GeckoExecutable

    @staticmethod
    def browserHelper_findBrowserDriverPaths(filename):

        lCurPath = Path(ManagedPaths().getOrSetDriverPath())
        lCurPath = lCurPath.joinpath(filename)

        logger.debug(f"Path for BrowserDrivers: {lCurPath}")
        return str(lCurPath)



    @staticmethod
    def browserHelper_log(logType, logText, browserDriveroptions, cbTakeScreenshot = None, **kwargs):
        """
        Interal wrapper of Browser-Class for Logging. Takes a screenshot on Error and Warning.

        @param logType: any of logging.ERROR, logging.WARN, INFO, etc.
        @param logText: Text to log
        @param kwargs: Additional Arguments to be logged
        """
        argsString = ""
        xshot = "Couldn't take Screenshot"

        locatorType = browserDriveroptions.locatorType
        locator = browserDriveroptions.locator

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
            #self.browserHelper_log(logging.CRITICAL, f"Unknown type in call to logger: {logType}", browserDriveroptions, cbTakeScreenshot = cbTakeScreenshot)


    @staticmethod
    def browserHelper_setProxyError(randomProxy):
        """
        Inform the central proxy service, that there was an error. OK, it might have been the page itself, that has
        an error and we'll never know. But more likely it's from the Proxy.
        :return:
        """
        if randomProxy:
            lProxyService = ProxyRotate()
            lProxyService.remove_proxy(ip=randomProxy["ip"], port=randomProxy["port"],
                                       type=randomProxy.get("type"))
