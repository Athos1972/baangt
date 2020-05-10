from baangt.base.DownloadFolderMonitoring import DownloadFolderMonitoring
from datetime import datetime
import os

directoryToMonitor = "0TestInput"
newFileName = "DownloadFolderMonitoring_test.txt"
newFile = os.path.join(directoryToMonitor, newFileName)

if os.path.exists(newFile):
    os.remove(newFile)


def removeFile(file):
    try:
        os.remove(file)
    except Exception as e:
        pass


def createFile(file):
    with open(file, 'w')as file_object:
        file_object.write(str(datetime.now()))


def test_getNewFiles():
    lDownloadFolderMonitoring = DownloadFolderMonitoring(directoryToMonitor)
    createFile(newFile)
    newFiles = lDownloadFolderMonitoring.getNewFiles()
    assert newFile == newFiles[0][0]
    print("Success. New File detected.")
    removeFile(newFile)


def test_creation_date():
    test_file_creation = int(datetime.now().timestamp())
    file = os.path.join(directoryToMonitor, str(test_file_creation)+".txt")
    createFile(file)
    creation_date = DownloadFolderMonitoring.creation_date(file)
    assert test_file_creation-int(creation_date) < 1
    print("Creation time is correct. Test Successful!")
    removeFile(file)
