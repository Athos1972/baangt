import os
import json


class managedPaths:
    def __init__(self):
        self.path = os.cwd()

    @staticmethod
    def check_paths_file():
        paths_file = os.path.isfile('Paths.json')
        return paths_file

    @staticmethod
    def __get_path(key):
        with open('Paths.json','r') as file:
            dic = json.load(file)
        if key in dic:
            return dic[key]
        else:
            return os.getcwd()

    @staticmethod
    def get_log_filename():
        if managedPaths.check_paths_file():
            path = managedPaths.__get_path('logFile')
        else:
            path = os.getcwd()
        return path

    @staticmethod
    def get_screenshot_path():
        if managedPaths.check_paths_file():
            path = managedPaths.__get_path('screenshot')
        else:
            path = os.getcwd()
        return path

    @staticmethod
    def get_download_path():
        if managedPaths.check_paths_file():
            path = managedPaths.__get_path('download')
        else:
            path = os.getcwd()
        return path


