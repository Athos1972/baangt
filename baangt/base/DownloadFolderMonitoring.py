
import logging
from pathlib import Path
import os
import platform


logger = logging.getLogger("pyC")


class DownloadFolderMonitoring:
    """
    Browserdrivers download all attachments into specific paths
    Here we shall watch for files, that were downloaded in this browser session
    and provide a method to report the last or all files for the current
    test case.

    A browser Driver session can run more than 1 testcase

    """

    def __init__(self, directoryToMonitor):
        self.directoryToWatch = directoryToMonitor
        # Get the current list - before we're started from the directory
        # This should be 0 as we've just created this folder
        self.__files = self.__readFiles()

    def getNewFiles(self):
        """

        :return: List of changed Files in directory since last call
        """
        lFiles = self.__readFiles()

        lNewFiles = [item for item in lFiles if item not in self.__files]

        if lNewFiles:
            logger.debug(f"List of new files in Folder {self.directoryToWatch}: {lNewFiles}")
        else:
            logger.debug(f"no new files detected in Folder {self.directoryToWatch}")

        self.__files = lFiles  # to avoid giving the same new results as on last call.

        return lNewFiles

    def __readFiles(self):
        newFiles = []
        newFilesWithDate = []
        for file in os.scandir(self.directoryToWatch):
            if not file.is_dir():
                newFiles.append(file)

        for file in newFiles:
            lCreationDate = DownloadFolderMonitoring.creation_date(file.path)
            newFilesWithDate.append([file.path, lCreationDate])

        return newFilesWithDate

    @staticmethod
    def creation_date(path_to_file):
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
        if platform.system() == 'Windows':
            return os.path.getctime(path_to_file)
        else:
            stat = os.stat(path_to_file)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return stat.st_mtime

