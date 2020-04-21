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
    def __init__(self):
        self.LogFilePath = None
        self.LogFilePath = self.get_log_path()
        self.ScreenshotPath = ""
        self.DownloadPath = ""

    def get_log_path(self):
        if self.LogFilePath:
            return self.LogFilePath

        self.LogFilePath = self.__combineBasePathWithObjectPath("Logs")

        return self.LogFilePath

    def set_screenshot_path(self, path=None, change=False):
        if self.ScreenshotPath != "" and change is False:
            return self.ScreenshotPath
        if path:
            self.ScreenshotPath = path
        else:
            self.ScreenshotPath = self.__combineBasePathWithObjectPath("Screenshots")

        return self.ScreenshotPath

    def set_download_path(self, path=None, change=False):
        if self.DownloadPath != "" and change is False:
            return self.DownloadPath
        if path:
            self.DownloadPath = path
        else:
            self.DownloadPath = self.__combineBasePathWithObjectPath("1Testresults")

        return self.DownloadPath

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
