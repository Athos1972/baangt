import os
import json
from pathlib import Path
from baangt.base import GlobalConstants as GC

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
    - getOrSetDriverPath: Will return a path were webdriver is located. You can also set path.
    """
    def __init__(self):
        self.LogFilePath = None
        self.LogFilePath = self.getLogfilePath()
        self.ScreenshotPath = ""
        self.DownloadPath = ""
        self.AttachmentDownloadPath = ""
        self.DriverPath = ""
        self.RootPath = ""
        self.ExportPath = ""
        self.ImportPath = ""

    def getLogfilePath(self):
        """
        Will return path where Log files will be saved.

        This Path will be taken from Paths.json

        :return: Logfile path
        """
        if self.LogFilePath:
            return self.LogFilePath

        self.LogFilePath = self.__combineBasePathWithObjectPath("Logs")

        return self.LogFilePath

    def getOrSetScreenshotsPath(self, path=None, change=False):
        """
        Will return path where Screenshots taken by the browser will be saved.

        Default path will be Screenshots folder in current working directory.

        :param path: Path to be set for browser screenshots if Screenshots path didn't exists.
        :param change: True if you want to change the existing Screenshots path with the one passed in path parameter.
        :return: Screenshot path
        """
        if self.ScreenshotPath != "" and change is False:
            return self.ScreenshotPath
        if path:
            if os.path.basename(path) != GC.PATH_SCREENSHOTS:
                path = os.path.join(path, GC.PATH_SCREENSHOTS)
            self.ScreenshotPath = path
        else:
            self.ScreenshotPath = self.__combineBasePathWithObjectPath(GC.PATH_SCREENSHOTS)

        return self.ScreenshotPath

    def getOrSetDownloadsPath(self, path=None, change=False):
        """

        Will return path where downloaded file will be saved.

        Default path will be 1Testresults folder in current working directory.

        :param path: Path to be set for browser downloads if download path didn't exists.
        :param change: True if you want to change the existing download path with the one passed in path parameter.
        :return: Download path
        """
        if self.DownloadPath != "" and change is False:
            return self.DownloadPath
        if path:
            self.DownloadPath = path
        else:
            self.DownloadPath = self.__combineBasePathWithObjectPath("1Testresults")

        return self.DownloadPath

    def getOrSetAttachmentDownloadPath(self, path=None, change=False):
        """
        Will return path where downloaded file will be saved.

        Default path will be TestDownloads folder in current working directory.

        :param path: Path to be set for browser Attachment Downloads if AttachmentDownloadPath path didn't exists.
        :param change: True if you want to change the existing AttachmentDownloadPath with the one passed in path parameter.
        :return: Attachment Download path
        """
        if self.AttachmentDownloadPath != "" and change is False:
            return self.AttachmentDownloadPath
        if path:
            self.AttachmentDownloadPath = path
        else:
            self.AttachmentDownloadPath = os.path.join(self.getOrSetDownloadsPath(), "TestDownloads")

        return self.AttachmentDownloadPath

    def getOrSetDriverPath(self, path=None, change=False):
        """
        Will return path where webdrivers are located.

        Default path will be browserDriver folder in current working directory.

        :param path: Path to be set for location where webdrivers are located or to be downloaded.
        :param change: True if you want to change the existing DriverPath with the one passed in path parameter.
        :return: Webdriver path
        """
        if self.DriverPath != "" and change is False:
            return self.DriverPath
        if path:
            self.DriverPath = path
        else:
            self.DriverPath = self.__combineBasePathWithObjectPath("browserDriver")

        return self.DriverPath

    def getOrSetRootPath(self, path=None, change=False):
        """

        Will return path for root directory.

        Default path will be current working directory.

        :param path: Path to be set as root directory.
        :param change: True if you want to change root path with the one passed in path parameter.
        :return: Root path
        """
        if self.RootPath != "" and change is False:
            return self.RootPath
        if path:
            self.RootPath = path
        else:
            self.RootPath = os.getcwd()

        return self.RootPath

    def getOrSetExportPath(self, path=None, change=False):
        """
        Will return path where output files should be save.

        :param path: Path to be set for Export Path.
        :param change: True if you want to change the existing Export Path with the one passed in path parameter.
        :return: Export path
        """
        if self.ExportPath != "" and change is False:
            return self.ExportPath
        if path:
            if os.path.basename(path) != GC.PATH_EXPORT:
                path = os.path.join(path, GC.PATH_EXPORT)
            self.ExportPath = path
        else:
            self.ExportPath = self.__combineBasePathWithObjectPath(GC.PATH_EXPORT)

        return self.ExportPath

    def getOrSetImportPath(self, path=None, change=False):
        """
        Will return path where program will search for input files.

        :param path: Path to be set for location where input files are located.
        :param change: True if you want to change the existing import path with the one passed in path parameter.
        :return: Import path
        """
        if self.ImportPath != "" and change is False:
            return self.ImportPath
        if path:
            if os.path.basename(path) != GC.PATH_IMPORT:
                path = os.path.join(path, GC.PATH_IMPORT)
            self.ImportPath = path
        else:
            self.ImportPath = self.__combineBasePathWithObjectPath(GC.PATH_IMPORT)

        return self.ImportPath

    def __combineBasePathWithObjectPath(self, objectPath : str):
        """

        :param objectPath:
        :return:
        """
        newPath = self.__derivePathForOSAndInstallationOption()
        newPath = newPath.joinpath(objectPath)

        return newPath

    def __derivePathForOSAndInstallationOption(self):
        """
        Will provide different **base paths** depending on each OS and install-version (e.g. Windows Repository, Windows
        ZIP-file with Executable, Windows Installer vs. MacOS-Installer vs. MacOS Repository.

        Each Method/File-Type might have additional rules, like e.g. .joinpath("directory_for_this_filetype")

        :return: base Path
        """
        return Path(os.getcwd())
