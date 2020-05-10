from baangt.base.DownloadFolderMonitoring import DownloadFolderMonitoring
from datetime import datetime
import os

directoryToMonitor = "0TestInput"
newFileName = "DownloadFolderMonitoring_test.txt"
newFile = os.path.join(directoryToMonitor, newFileName)

if os.path.exists(newFile):
    os.remove(newFile)


def createFile(file):
    # Create file for testing
    with open(file, 'w')as file_object:
        file_object.write(str(datetime.now()))


def removeFile(file):
    # Remove file after testing
    try:
        os.remove(file)
    except Exception as e:
        pass


def test_getNewFiles():
    # Creates a file in Monitored Folder after creating DownloadFolderMonitoring instance and check getNewFiles Method.
    lDownloadFolderMonitoring = DownloadFolderMonitoring(directoryToMonitor)
    createFile(newFile)
    newFiles = lDownloadFolderMonitoring.getNewFiles()
    assert newFile == newFiles[0][0]
    print("Success. New File detected.")
    removeFile(newFile)


def test_creation_date():
    # Creates file in Monitored Folder and verify if creation_date method of DownloadFolderMonitoring return true value.
    test_file_creation = int(datetime.now().timestamp())
    file = os.path.join(directoryToMonitor, str(test_file_creation)+".txt")
    createFile(file)
    creation_date = DownloadFolderMonitoring.creation_date(file)
    assert test_file_creation-int(creation_date) < 1
    print("Creation time is correct. Test Successful!")
    removeFile(file)
