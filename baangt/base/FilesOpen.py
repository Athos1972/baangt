import platform
import os
import subprocess

def open(filenameAndPath: str):
    """Will open the given file with the Operating system default program.

    param

    filenameAndPath : Complete absolute path to file.
    return : True if sucessfully open. False if file doesn't exists or operating system doesn't have default program.
    """

    if not isinstance(filenameAndPath, str):
        filenameAndPath = str(filenameAndPath)

    if not os.path.exists(filenameAndPath):
        return False
    elif platform.system() == "Windows":
        try:
            os.startfile(filenameAndPath)
            return True
        except:
            return False
    elif platform.system() == "Linux":
        status = subprocess.call(["xdg-open", str(filenameAndPath)])
        if status == 0:
            return True
        else:
            return False
    elif platform.system() == "Darwin":
        status = os.system("open " + str(filenameAndPath))
        if status == 0:
            return True
        else:
            return False


class FilesOpen:
    """
    Class is called from UI and will open the corresponding file-type in the os-specific application.
    """
    def __init__(self):
        pass

    @staticmethod
    def openTestRunDefinition(filenameAndPath):
        return open(filenameAndPath=filenameAndPath)

    @staticmethod
    def openResultFile(filenameAndPath):
        return open(filenameAndPath=filenameAndPath)

    @staticmethod
    def openLogFile(filenameAndPath):
        return open(filenameAndPath=filenameAndPath)






