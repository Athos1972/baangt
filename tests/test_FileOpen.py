from baangt.base import FilesOpen
from pathlib import Path
import os

lXLSXFile = Path(os.getcwd()).joinpath("tests").joinpath("1TestResults").joinpath("baangt_testfranzi.xlsx_20200501_173746.xlsx")
lLogFile = Path(os.getcwd()).joinpath("tests").joinpath("logs").joinpath("20200502_100944.log")

def test_Open_NoFile():
    lResult = FilesOpen.open("franzi")
    assert not lResult


def test_Open_XLSX():
    lResult = FilesOpen.open(lXLSXFile)
    assert lResult


def test_Open_LOGFILE():
    lResult = FilesOpen.open(lLogFile)
    assert lResult


def test_with_class_resultFile():
    lFilesOpen = FilesOpen.FilesOpen()
    lResult = lFilesOpen.openResultFile(lXLSXFile)
    assert lResult


def test_with_class_LogFile():
    lFilesOpen = FilesOpen.FilesOpen()
    lResult = lFilesOpen.openLogFile(lLogFile)
    assert lResult


def test_with_class_TestRunDefinitionFile():
    lFilesOpen = FilesOpen.FilesOpen()
    lResult = lFilesOpen.openTestRunDefinition(lXLSXFile)
    assert lResult


def test_with_class_invalidFile():
    lFilesOpen = FilesOpen.FilesOpen()
    lResult = lFilesOpen.openTestRunDefinition("franzi")
    assert not lResult