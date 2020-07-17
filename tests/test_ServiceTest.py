import os
import glob
import xlrd
import subprocess
from pathlib import Path
from baangt.base.DownloadFolderMonitoring import DownloadFolderMonitoring
from baangt.base.BrowserFactory import BrowserDriver
from baangt.base import GlobalConstants as GC
from baangt.base.PathManagement import ManagedPaths
from baangt.base.TestRun.TestRun import TestRun
from uuid import uuid4
import psutil
import pytest
import platform
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
from baangt.base.DataBaseORM import TestrunLog
import json

# Will Check for the current directory and change it to baangt root dir
if not os.path.basename(os.getcwd()) == "baangt":
    if os.path.basename(os.path.dirname(os.getcwd())) == "baangt":
        os.chdir('..')
    else:
        assert 0, "Please run the test from baangt/ or baangt/tests/ directory."


# Paths
current_dir = os.getcwd()
managed_path = ManagedPaths()
output_dir = Path(managed_path.getOrSetExportPath())
input_dir = Path(current_dir).joinpath("tests/0TestInput/ServiceTestInput")
input_file = str(Path(current_dir).joinpath("tests/0TestInput/ServiceTestInput/simpleAutomationpractice_small.xlsx"))
input_file_parallel = str(Path(input_dir).joinpath("simpleAutomationpractice.xlsx"))
drivers_folder = Path(managed_path.getOrSetDriverPath())

isLinux = True if platform.system().upper() == "LINUX" else False

# Creates a copy of your environment
my_env = os.environ.copy()
# Use if you get error 'java' command not found even after it is installed in your system
# Replace the path inside "" to the bin folder of java.
my_env["PATH"] = r"C:\Program Files (x86)\Java\jre1.8.0_251\bin;" + my_env["PATH"]


# To monitor new download files
folder_monitor = DownloadFolderMonitoring(str(output_dir))


# Program execution functions
def execute_from_main(run_file, globals_file):
    # Execute the main baangt program with TestRunFile and globals file
    subprocess.call(
        "python baangt.py --run "+run_file+" --globals "+globals_file,
        shell=True, env=my_env
    )


def execute(run_file, globals_file):
    # Execute the program using TestRun
    lUUID = uuid4()
    lTestRun = TestRun(run_file, globalSettingsFileNameAndPath=globals_file, uuid=lUUID)


# Testing Output Functions
def check_output(xlsx_file):
    workbook = xlrd.open_workbook(xlsx_file)
    book = workbook.sheet_by_name("Summary")
    test_records = book.row(2)[1].value or 0
    success = book.row(3)[1].value or 0
    error = book.row(5)[1].value or 0
    test_records = int(test_records)
    success = int(success)
    error = int(error)
    assert success >= test_records/2


def check_browsermob_output(xlsx_file):
    workbook = xlrd.open_workbook(xlsx_file)
    book = workbook.sheet_by_name("Network")
    assert book.nrows > 25

# 20.5.2020: This is covered in test_browserHandling.
# def test_download_browser_drivers():
#     # Will delete the pre-existing browsers and download new.
#     file_list = glob.glob(str(drivers_folder.joinpath('*')))
#     for file in file_list:
#         print(file)
#         os.remove(file)
#     driver_folder_monitor = DownloadFolderMonitoring(str(drivers_folder))
#     BrowserDriver.downloadDriver(GC.BROWSER_FIREFOX)
#     BrowserDriver.downloadDriver(GC.BROWSER_CHROME)
#     new_drivers = driver_folder_monitor.getNewFiles()
#     assert driver_folder_monitor
#     for drivers in new_drivers:
#         print(drivers[0], "downloaded")
#     return "Downloading drivers test succeeded"
#

# Firefox testing section
def test_regular_firefox():
    # Will run the main program with normal regular globals settings
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_ff.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    output_file = output_dir.joinpath(new_file[0][0]).as_posix()
    check_output(output_file)
    os.remove(output_file)
    return "Firefox regular test succeed output file =", new_file[0][0]


def test_parellel_firefox():
    # Will run the main program with 2 browsers running parallel
    run_file = input_file_parallel
    globals_file = Path(input_dir).joinpath("globals_parellel_ff.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    output_file = output_dir.joinpath(new_file[0][0]).as_posix()
    check_output(output_file)
    os.remove(output_file)
    return "Firefox parellel test succeed output file =", new_file[0][0]


def test_browsermob_proxy_firefox():
    # Will run the main program with browsermob proxy mode
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_browsermob_proxy_ff.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    output_file = output_dir.joinpath(new_file[0][0]).as_posix()
    check_output(output_file)
    check_browsermob_output(output_file)
    os.remove(output_file)
    return "Firefox Browsermob test succeed output file =", new_file[0][0]


def test_headless_firefox():
    # Will run the main program with headless browser
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_headless_ff.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    output_file = output_dir.joinpath(new_file[0][0]).as_posix()
    check_output(output_file)
    os.remove(output_file)
    return "Firefox headless test succeed output file =", new_file[0][0]


def test_csv_firefox():
    # Will run the main program for csv output
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_csv_ff.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    assert ".csv" in new_file[0][0]
    output_file = output_dir.joinpath(new_file[0][0]).as_posix()
    os.remove(output_file)
    return "Firefox Output Format test succeed output file =", new_file[0][0]


# Chrome Testing Section
@pytest.mark.skipif(isLinux, reason="Chrome not stable on Linux in Docker")
def test_regular_chrome():
    # Will run the main program with normal regular globals settings
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_chrome.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    output_file = output_dir.joinpath(new_file[0][0]).as_posix()
    check_output(output_file)
    os.remove(output_file)
    return "Chrome regular test succeed output file =", new_file[0][0]


@pytest.mark.skipif(isLinux, reason="Chrome not stable on Linux in Docker")
def test_parellel_chrome():
    # Will run the main program with 2 browsers running parallel
    run_file = input_file_parallel
    globals_file = Path(input_dir).joinpath("globals_parellel_chrome.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    output_file = output_dir.joinpath(new_file[0][0]).as_posix()
    check_output(output_file)
    os.remove(output_file)
    return "Chrome parellel test succeed output file =", new_file[0][0]


@pytest.mark.skipif(isLinux, reason="Chrome not stable on Linux in Docker")
def test_browsermob_proxy_chrome():
    # Will run the main program with browsermob proxy mode
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_browsermob_proxy_chrome.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    output_file = output_dir.joinpath(new_file[0][0]).as_posix()
    check_output(output_file)
    check_browsermob_output(output_file)
    os.remove(output_file)
    return "Chrome Browsermob test succeed output file =", new_file[0][0]


@pytest.mark.skipif(isLinux, reason="Chrome not stable on Linux in Docker")
def test_headless_chrome():
    # Will run the main program with headless browser
    for proc in psutil.process_iter():
        if proc.name() == "browsermob-proxy":
            proc.kill()

    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_headless_chrome.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    output_file = output_dir.joinpath(new_file[0][0]).as_posix()
    check_output(output_file)
    os.remove(output_file)
    return "Chrome headless test succeed output file =", new_file[0][0]


@pytest.mark.skipif(isLinux, reason="Chrome not stable on Linux in Docker")
def test_csv_chrome():
    # Will run the main program for csv output
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_csv_chrome.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    assert ".csv" in new_file[0][0]
    return "Chrome Output Format test succeed output file =", new_file[0][0]


def test_full_BaangtWebDemo():
    run_file = str(input_dir.joinpath("CompleteBaangtWebdemo.xlsx"))
    execute(run_file, globals_file=Path(input_dir).joinpath("globals_ff.json"))
    new_file = folder_monitor.getNewFiles()
    assert new_file
    output_file = output_dir.joinpath(new_file[0][0]).as_posix()
    check_output(output_file)
    os.remove(output_file)

def test_NestedIfElse_with_NoBrowser():
    run_file = str(input_dir.joinpath("CompleteBaangtWebdemo_else.xlsx"))
    execute(run_file, globals_file=Path(input_dir).joinpath("globalsNoBrowser.json"))
    new_file = folder_monitor.getNewFiles()
    assert new_file
    output_file = output_dir.joinpath(new_file[0][0]).as_posix()
    check_output(output_file)
    os.remove(output_file)

def test_NestedIfElse_with_greater_endif():
    run_file = str(input_dir.joinpath("CompleteBaangtWebdemo_else_error.xlsx"))
    try:
        execute(run_file, globals_file=Path(input_dir).joinpath("globalsNoBrowser.json"))
        assert 1 == 0
    except BaseException:
        assert 1 == 1

def test_NestedLoops_and_repeat():
    run_file = str(input_dir.joinpath("CompleteBaangtWebdemo_nested.xlsx"))
    execute(run_file, globals_file=Path(input_dir).joinpath("globalsNoBrowser.json"))
    managedPaths = ManagedPaths()
    DATABASE_URL = os.getenv('DATABASE_URL') or 'sqlite:///' + str(
        managedPaths.derivePathForOSAndInstallationOption().joinpath('testrun.db'))
    new_file = folder_monitor.getNewFiles()
    assert new_file
    output_file = output_dir.joinpath(new_file[0][0]).as_posix()
    wb = xlrd.open_workbook(output_file)
    sheet1 = wb.sheet_by_name("Test_textarea2")
    sheet2 = wb.sheet_by_name("Test_textarea2.nested")
    assert sheet1.nrows == 3
    assert sheet2.nrows == 3
    TestRunSheet = wb.sheet_by_name("Summary")
    TestRunUUID = TestRunSheet.cell_value(8, 1)
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    s = Session()
    data = s.query(TestrunLog).get(uuid.UUID(TestRunUUID).bytes)
    assert "textarea2" in json.loads(data.RLPJson)
    os.remove(output_file)
