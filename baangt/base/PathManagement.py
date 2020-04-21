import os
import json


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    
class ManagedPaths(metaclass=Singleton):
    def __init__(self):
        self.path = os.getcwd()
        self.LogFileName = ""
        self.LogFileName = self.get_log_filename()
        self.ScreenshotPath = ""
        self.DownloadPath = ""

    def check_paths_file(self):
        paths_file = os.path.isfile('Paths.json')
        return paths_file

    def __get_path(self, key):
        with open('Paths.json','r') as file:
            dic = json.load(file)
        if key in dic:
            if dic[key] != "":
                return dic[key]
            else:
                return os.getcwd()
        else:
            return os.getcwd()

    def get_log_filename(self):
        if self.LogFileName != "":
            return self.LogFileName
        if self.check_paths_file():
            path = self.__get_path('logFile')
        else:
            path = os.getcwd()
        return path

    def set_screenshot_path(self, path=None, change=False):
        if self.ScreenshotPath != "" and change is False:
            return self.ScreenshotPath
        if path:
            self.ScreenshotPath = path
        else:
            self.ScreenshotPath = os.getcwd()
        return self.ScreenshotPath

    def set_download_path(self, path=None, change=False):
        if self.DownloadPath != "" and change is False:
            return self.DownloadPath
        if path:
            self.DownloadPath = path
        else:
            self.DownloadPath = os.getcwd()
        return self.DownloadPath


