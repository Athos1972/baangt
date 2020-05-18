import os
import glob
import subprocess
from pathlib import Path
from baangt.base.DownloadFolderMonitoring import DownloadFolderMonitoring
from baangt.base.BrowserFactory import BrowserDriver
from baangt.base import GlobalConstants as GC
from baangt.base.PathManagement import ManagedPaths


# Will Check for the current directory and change it to baangt root dir
if not os.path.basename(os.getcwd()) == "baangt":
    if os.path.basename(os.path.dirname(os.getcwd())) == "baangt":
        os.chdir('..')
    else:
        assert 0, "Please run the test from baangt/ or baangt/tests/ directory."


# Paths
current_dir = os.getcwd()
output_dir = Path(current_dir).joinpath( 'tests/1Testresults/ServiceTest')
input_dir = Path(current_dir).joinpath("tests/0TestInput/ServiceTestInput")
input_file = str(Path(current_dir).joinpath("tests/0TestInput/ServiceTestInput/simpleAutomationpractice_small.xlsx"))
input_file_parellel = str(Path(input_dir).joinpath("simpleAutomationpractice.xlsx"))
drivers_folder = Path(current_dir).joinpath("tests/0TestInput/Drivers")


# Make and check dir using ManagePaths method & updating ManagePaths for driver path
managed_path = ManagedPaths()
managed_path._ManagedPaths__makeAndCheckDir(output_dir)
managed_path._ManagedPaths__makeAndCheckDir(drivers_folder)
managed_path.getOrSetDriverPath(path=str(drivers_folder))


# Creates a copy of your environment
my_env = os.environ.copy()
# Use if you get error 'java' command not found even after it is installed in your system
# Replace the path inside "" to the bin folder of java.
my_env["PATH"] = r"C:\Program Files (x86)\Java\jre1.8.0_251\bin;" + my_env["PATH"]


# Will delete old result files
files = glob.glob(str(output_dir.joinpath('*')))
for f in files:
    if '.xlsx' in f:
        os.remove(f)


# To monitor new download files
folder_monitor = DownloadFolderMonitoring(str(output_dir))


def execute(run_file, globals_file):
    # Execute the main baangt program with TestRunFile and globals file
    subprocess.call(
        "python baangt.py --run "+run_file+" --globals "+globals_file,
        shell=True, env=my_env
    )


def test_download_browser_drivers():
    # Will delete the pre-existing browsers and download new.
    file_list = glob.glob(str(drivers_folder.joinpath('*')))
    for file in file_list:
        print(file)
        os.remove(file)
    driver_folder_monitor = DownloadFolderMonitoring(str(drivers_folder))
    BrowserDriver.downloadDriver(GC.BROWSER_FIREFOX)
    BrowserDriver.downloadDriver(GC.BROWSER_CHROME)
    new_drivers = driver_folder_monitor.getNewFiles()
    assert driver_folder_monitor
    for drivers in new_drivers:
        print(drivers[0], "downloaded")
    return "Downloading drivers test succeeded"


# Firefox testing section
def test_regular_firefox():
    # Will run the main program with normal regular globals settings
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_ff.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    return "Firefox regular test succeed output file =", new_file[0][0]


def test_parellel_firefox():
    # Will run the main program with 2 browsers running parallel
    run_file = input_file_parellel
    globals_file = Path(input_dir).joinpath("globals_parellel_ff.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    return "Firefox parellel test succeed output file =", new_file[0][0]


def test_browsermob_proxy_firefox():
    # Will run the main program with browsermob proxy mode
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_browsermob_proxy_ff.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    return "Firefox Browsermob test succeed output file =", new_file[0][0]


def test_headless_firefox():
    # Will run the main program with headless browser
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_headless_ff.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    return "Firefox headless test succeed output file =", new_file[0][0]


def test_csv_firefox():
    # Will run the main program for csv output
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_csv_ff.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    assert ".csv" in new_file[0][0]
    return "Firefox Output Format test succeed output file =", new_file[0][0]


def test_all_firefox():
    # Will test all firefox functionalities together
    results = [
        test_regular_firefox(),
        test_parellel_firefox(),
        test_browsermob_proxy_firefox(),
        test_headless_firefox(),
        test_csv_firefox()
    ]
    return results


# Chrome Testing Section
def test_regular_chrome():
    # Will run the main program with normal regular globals settings
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_chrome.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    return "Chrome regular test succeed output file =", new_file[0][0]


def test_parellel_chrome():
    # Will run the main program with 2 browsers running parallel
    run_file = input_file_parellel
    globals_file = Path(input_dir).joinpath("globals_parellel_chrome.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    return "Chrome parellel test succeed output file =", new_file[0][0]


def test_browsermob_proxy_chrome():
    # Will run the main program with browsermob proxy mode
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_browsermob_proxy_chrome.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    return "Chrome Browsermob test succeed output file =", new_file[0][0]


def test_headless_chrome():
    # Will run the main program with headless browser
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_headless_chrome.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    return "Chrome headless test succeed output file =", new_file[0][0]


def test_csv_chrome():
    # Will run the main program for csv output
    run_file = input_file
    globals_file = Path(input_dir).joinpath("globals_csv_chrome.json").as_posix()
    execute(run_file, globals_file)
    new_file = folder_monitor.getNewFiles()
    assert new_file
    assert ".csv" in new_file[0][0]
    return "Chrome Output Format test succeed output file =", new_file[0][0]


def test_all_chrome():
    # Will test all firefox functionalities together
    results = [
        test_regular_chrome(),
        test_parellel_chrome(),
        test_browsermob_proxy_chrome(),
        test_headless_chrome(),
        test_csv_chrome()
    ]
    return results


def test_all():
    # Will test all functions in this module
    results = [
        test_download_browser_drivers(),
        test_all_firefox(),
        test_all_chrome()
    ]
    for result in results:
        if type(result) == str:
            print(result)
        else:
            for each in result:
                print(each)
