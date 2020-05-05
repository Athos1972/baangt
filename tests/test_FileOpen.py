from baangt.base import FilesOpen
from pathlib import Path
import os


def test_Open_NoFile():
    lResult = FilesOpen.open("franzi")
    assert not lResult


def test_Open_XLSX():
    lResult = FilesOpen.open(str(Path(os.getcwd()).joinpath("1TestResults").joinpath("baangt_simpleAutomationpractice.xlsx_20200427_091657.xlsx")))
    assert lResult


def test_Open_LOGFILE():
    lResult = FilesOpen.open(str(Path(os.getcwd()).joinpath("logs").joinpath("20200502_100944.log")))
    assert lResult