
from baangt.base.ProxyRotate import ProxyRotate
from baangt.base import GlobalConstants as GC
from baangt.base.PathManagement import ManagedPaths
import os
import uuid
import logging
from pathlib import Path
import platform
import ctypes
import zipfile
import requests
from dataclasses import dataclass
import tarfile
from urllib.request import urlretrieve

logger = logging.getLogger("pyC")

@dataclass
class BrowserDriverData:
    locatorType : str
    locator : str
    driver : None

class BrowserHelperFunction:
    """
    Helper function class for BrowserHandling. 
    """

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
        """
        Extract IP, Port and Browser from the globalSettings, if set.
        If not, use localhost:4444/firefox as default settings

        :param desiredCapabilities: (from globals)
        :return: desiredCapabiligies, IP and Port of Selenium Grid V4
        """
        seleniumGridIp = ""
        seleniumGridPort = ""
        if len(desiredCapabilities) > 0:
            if not 'seleniumGridIp' in desiredCapabilities.keys():
                seleniumGridIp = '127.0.0.1'
            else:
                seleniumGridIp = desiredCapabilities["seleniumGridIp"]
                desiredCapabilities.pop("seleniumGridIp")

            if not 'seleniumGridPort' in desiredCapabilities.keys():
                seleniumGridPort = '4444'
            else:
                seleniumGridPort = desiredCapabilities["seleniumGridPort"]
                desiredCapabilities.pop("seleniumGridPort")

            if not 'browserName' in desiredCapabilities.keys():
                desiredCapabilities['browserName'] = 'firefox'

        return desiredCapabilities, seleniumGridIp, seleniumGridPort

    @staticmethod
    def browserHelper_getBrowserExecutable(browserName):
        # Get executable
        if GC.BROWSER_FIREFOX == browserName:
            executable = GC.GECKO_DRIVER
        elif GC.BROWSER_CHROME == browserName:
            executable = GC.CHROME_DRIVER
        else:
           executable = None 

        if 'NT' not in os.name.upper() and executable:
            executable = executable.split('.')[0]
        return executable

    @staticmethod
    def browserHelper_findBrowserDriverPaths(filename):

        lCurPath = Path(ManagedPaths().getOrSetDriverPath())
        lCurPath = lCurPath.joinpath(filename)

        logger.debug(f"Path for BrowserDrivers: {lCurPath}")
        return str(lCurPath)


    @staticmethod
    def browserHelper_log(logType, logText, browserData, cbTakeScreenshot = None, **kwargs):
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

        if browserData.locator:
            argsString = argsString + f" Locator: {browserData.locatorType} = {browserData.locator}"

        if logType == logging.DEBUG:
            logger.debug(logText + argsString)
        elif logType == logging.ERROR:
            if cbTakeScreenshot:
                xshot = cbTakeScreenshot()
            logger.error(logText + argsString + f" Screenshot: {xshot}")
        elif logType == logging.WARN:
            logger.warning(logText + argsString)
        elif logType == logging.INFO:
            logger.info(logText + argsString)
        elif logType == logging.CRITICAL:
            if cbTakeScreenshot:
                xshot = cbTakeScreenshot()
            logger.critical(logText + argsString + f" Screenshot: {xshot}")
        else:
            print(f"Unknown call to Logger: {logType}")
            BrowserHelperFunction.browserHelper_log(logging.CRITICAL, f"Unknown type in call to logger: {logType}", browserData, cbTakeScreenshot = cbTakeScreenshot)


    @staticmethod
    def browserHelper_setProxyError(randomProxy):
        """
        Inform the central proxy service, that there was an error. OK, it might have been the page itself, that has
        an error and we'll never know. But more likely it's from the Proxy.
        :return:
        """
        if randomProxy:
            ProxyRotate().remove_proxy(ip=randomProxy["ip"], port=randomProxy["port"], type=randomProxy.get("type"))


    @staticmethod
    def browserHelper_getFirefoxFileUrl():
        #TODO check if this function can be combined with browserHelper_getChromeFileUrl
        # Can ctypes.c_voidp used for both browsers?
        url = None
        response = requests.get(GC.GECKO_URL)
        gecko = response.json()
        gecko = gecko['assets']
        gecko_length_results = len(gecko)
        drivers_url_dict = []

        for i in range(gecko_length_results):
            drivers_url_dict.append(gecko[i]['browser_download_url'])

        isTarFile = True
        zipbObj = zip(GC.OS_list, drivers_url_dict)
        geckoDriversDict = dict(zipbObj)
        if platform.system().lower() == GC.WIN_PLATFORM:
            isTarFile = False
            if ctypes.sizeof(ctypes.c_voidp) == GC.BIT_64:
                url = geckoDriversDict[GC.OS_list[4]]
            else:
                url = geckoDriversDict[GC.OS_list[3]]
        elif platform.system().lower() == GC.LINUX_PLATFORM:
            if ctypes.sizeof(ctypes.c_voidp) == GC.BIT_64:
                url = geckoDriversDict[GC.OS_list[1]]
            else:
                url = geckoDriversDict[GC.OS_list[0]]
        else:
            url = geckoDriversDict[GC.OS_list[2]]

        return url, isTarFile

    @staticmethod
    def browserHelper_getChromeFileUrl():
        url = None
        response = requests.get(GC.CHROME_URL)
        chromeversion = response.text
        chromedriver_url_dict = []

        for i in range(len(GC.OS_list_chrome)):
            OS = GC.OS_list_chrome[i]
            chrome = f'http://chromedriver.storage.googleapis.com/{chromeversion}/chromedriver_{OS}.zip'
            chromedriver_url_dict.append(chrome)

        zipbObjChrome = zip(GC.OS_list, chromedriver_url_dict)
        chromeDriversDict = dict(zipbObjChrome)
        if platform.system().lower() == GC.WIN_PLATFORM:
            url = chromeDriversDict[GC.OS_list[3]]
        elif platform.system().lower() == GC.LINUX_PLATFORM:
            url = chromeDriversDict[GC.OS_list[1]]
        else:
            url = chromeDriversDict[GC.OS_list[2]]

        return url
  
    @staticmethod
    def browserHelper_unzipDriverFile(url, path, driverName):
        file = requests.get(url)
        path_zip = path.joinpath(driverName.replace('exe', 'zip'))
        logger.debug(f"Zipfile with browser expected here: {path_zip} ")
        open(path_zip, 'wb').write(file.content)
        with zipfile.ZipFile(path_zip, 'r') as zip_ref:
            zip_ref.extractall(path)

        if platform.system().lower() != GC.WIN_PLATFORM:
            file_path = path.joinpath(driverName.replace('.exe', ''))
            os.chmod(file_path, 0o777)
        os.remove(path_zip)

    @staticmethod
    def browserHelper_extractTarDriverFile(url, path, driverName):
        path_zip = path.joinpath(driverName.replace('exe', 'tar.gz'))
        filename, _ = urlretrieve(url, path_zip)
        logger.debug(f"Tarfile with browser expected here: {filename} ")
        tar = tarfile.open(filename, "r:gz")
        tar.extractall(path=path)
        tar.close()