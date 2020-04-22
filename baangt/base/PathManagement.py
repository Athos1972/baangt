import os
import json
from pathlib import Path


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
    """
    def __init__(self):
        self.LogFilePath = None
        self.LogFilePath = self.getLogfilePath()
        self.ScreenshotPath = ""
        self.DownloadPath = ""
        self.AttachmentDownloadPath = ""

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
            self.ScreenshotPath = path
        else:
            self.ScreenshotPath = self.__combineBasePathWithObjectPath("Screenshots")

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
            self.AttachmentDownloadPath = self.__combineBasePathWithObjectPath("TestDownloads")

        return self.AttachmentDownloadPath

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
