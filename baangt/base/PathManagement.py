import os
import json
import platform
from pathlib import Path
from baangt.base import GlobalConstants as GC
from baangt.TestSteps import Exceptions as baangtExceptions
import logging

logger = logging.getLogger("pyC")

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ManagedPaths(metaclass=Singleton):
    """
    The class to manage paths for different task.
    Main Methods:
    - getLogfilePath: Will return a path for logfile directory.
    - getOrSetScreenshotsPath: Will return a path for Screenshots directory. You can also set path.
    - getOrSetDownloadsPath: Will return a path for Download directory. You can also set path.
    - getOrSetAttachmentDownloadPath: Will return a path for Attachment Download directory. You can also set path.
    - getOrSetDriverPath: Will return path were webdriver is located. You can also set path.
    - getOrSetImportPath: Will return path were input files are located. You can also set path.
    - getOrSetExportPath: Will return path were files will be save. You can also set path.
    - getOrSetRootPath: Will return root directory path. You can also set path.
    - getOrSetIni: Will return path of directory where ini files are managed.
    """

    def __init__(self):
        self.LogFilePath = ""
        self.LogFilePath = self.getLogfilePath()
        self.ScreenshotPath = ""
        self.DownloadPath = ""
        self.AttachmentDownloadPath = ""
        self.DriverPath = ""
        self.RootPath = ""
        self.ExportPath = ""
        self.ImportPath = ""
        self.IniPath = ""

    def getLogfilePath(self):
        """
        Will return path where Log files will be saved.

        This Path will be taken from old_Paths.json

        :return: Logfile path
        """

        if self.LogFilePath:
            return self.LogFilePath

        self.LogFilePath = self.__combineBasePathWithObjectPath("Logs")
        self.__makeAndCheckDir(self.LogFilePath)

        return self.LogFilePath

    def getOrSetScreenshotsPath(self, path=None):
        """
        Will return path where Screenshots taken by the browser will be saved.

        Default path will be Screenshots folder in current working directory.

        :param path: Path to be set for browser screenshots.
        :return: Screenshot path
        """

        if self.ScreenshotPath != "":
            return self.ScreenshotPath

        if path:
            self.ScreenshotPath = Path(path)
        else:
            self.ScreenshotPath = self.__combineBasePathWithObjectPath(GC.PATH_SCREENSHOTS)

        self.__makeAndCheckDir(self.ScreenshotPath)
        return self.ScreenshotPath

    def getOrSetDownloadsPath(self, path=None):
        """

        Will return path where downloaded file will be saved.

        Default path will be 1TestResults folder in current working directory.

        :param path: Path to be set for browser downloads if download path didn't exists.
        :return: Download path
        """

        if self.DownloadPath != "":
            return self.DownloadPath

        if path:
            self.DownloadPath = path
        else:
            self.DownloadPath = self.__combineBasePathWithObjectPath("1TestResults")

        self.__makeAndCheckDir(self.DownloadPath)
        return self.DownloadPath

    def getOrSetAttachmentDownloadPath(self, path=None):
        """
        Will return path where downloaded file will be saved.

        Default path will be TestDownloads folder in current working directory.

        :param path: Path to be set for browser Attachment Downloads if AttachmentDownloadPath path didn't exists.
        :return: Attachment Download path
        """
        if self.AttachmentDownloadPath != "":
            return self.AttachmentDownloadPath

        if path:
            self.AttachmentDownloadPath = path
        else:
            self.AttachmentDownloadPath = os.path.join(self.getOrSetDownloadsPath(), "TestDownloads")

        self.__makeAndCheckDir(self.AttachmentDownloadPath)
        return self.AttachmentDownloadPath

    def getOrSetDriverPath(self, path=None):
        """
        Will return path where webdrivers are located.

        Default path will be browserDriver folder in current working directory.

        :param path: Path to be set for location where webdrivers are located or to be downloaded.
        :return: Webdriver path
        """
        if self.DriverPath != "":
            return self.DriverPath

        if path:
            self.DriverPath = path
        else:
            self.DriverPath = self.__combineBasePathWithObjectPath("browserDrivers")

        self.__makeAndCheckDir(self.DriverPath)
        return self.DriverPath

    def getOrSetRootPath(self, path=None):
        """

        Will return path for root directory.

        Default path will be current working directory.

        :param path: Path to be set as root directory.
        :return: Root path
        """
        if self.RootPath != "":
            return self.RootPath

        if path:
            self.RootPath = path
        else:
            self.RootPath = os.getcwd()

        return self.RootPath

    def getOrSetExportPath(self, path=None):
        """
        Will return path where output files should be save.

        :param path: Path to be set for Export Path.
        :return: Export path
        """
        if self.ExportPath != "":
            return self.ExportPath

        if path:
            self.ExportPath = path
        else:
            self.ExportPath = self.__combineBasePathWithObjectPath(GC.PATH_EXPORT)

        self.__makeAndCheckDir(self.ExportPath)
        return self.ExportPath

    def getOrSetImportPath(self, path=None):
        """
        Will return path where program will search for input files.

        :param path: Path to be set for location where input files are located.
        :return: Import path
        """
        if self.ImportPath != "":
            return self.ImportPath

        if path:
            self.ImportPath = path
        else:
            self.ImportPath = self.__combineBasePathWithObjectPath(GC.PATH_IMPORT)

        self.__makeAndCheckDir(self.ImportPath)
        return self.ImportPath

    def __combineBasePathWithObjectPath(self, objectPath: str):
        """

        :param objectPath:
        :return:
        """
        newPath = Path(self.derivePathForOSAndInstallationOption())
        newPath = newPath.joinpath(objectPath)

        return newPath

    def derivePathForOSAndInstallationOption(self):
        """
        Will provide different **base paths** depending on each OS and install-version (e.g. Windows Repository, Windows
        ZIP-file with Executable, Windows Installer vs. MacOS-Installer vs. MacOS Repository.

        Each Method/File-Type might have additional rules, like e.g. .joinpath("directory_for_this_filetype")

        :return: base Path
        """
        if platform.system() == "Windows":
            path = os.path.join(os.path.expanduser("~"), "baangt")
            if os.path.exists(path):
                return Path(path)
        return Path(os.getcwd())

    def __makeAndCheckDir(self, newPath):
        """

        :param newPath: Path to be made or check existence.
        :return: None
        """
        Path(newPath).mkdir(exist_ok=True, parents=True)

        if not Path(newPath).is_dir():
            baangtExceptions.baangtTestStepException(f"Tried to create folder {newPath} and failed.")
            logger.debug(f"Tried to create folder {newPath} and failed.")

        return None

    def getOrSetIni(self, path=None):
        """
                Will return path where program will search for ini files.

                :param path: Path to be set for location where ini files are located.
                :return: Ini path
                """
        if self.IniPath != "":
            return self.IniPath

        if path:
            self.IniPath = path
        else:
            self.IniPath = self.__combineBasePathWithObjectPath('ini')

        self.__makeAndCheckDir(self.IniPath)
        return self.IniPath
