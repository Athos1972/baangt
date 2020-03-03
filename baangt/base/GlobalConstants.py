KWARGS_DATA = "data"
KWARGS_BROWSER = "Browser"
KWARGS_API_SESSION = "api"
KWARGS_TESTCASETYPE = "TestCaseType"
KWARGS_TESTRUNATTRIBUTES = "TESTRUNEXECUTIONPARAMETERS"
KWARGS_TESTRUNINSTANCE = "TESTRUNINSTANCE"
KWARGS_TIMING = "TimingClassInstance"

CLASSES_TESTCASESEQUENCE_OLD = "baangt.TestCaseSequence.TestCaseSequenceMaster.TestCaseSequenceMaster"
CLASSES_TESTCASESEQUENCE = "TestCaseSequenceMaster"
CLASSES_TESTCASE_OLD = "baangt.TestCase.TestCaseMaster.TestCaseMaster"
CLASSES_TESTCASE = 'TestCaseMaster'
CLASSES_TESTSTEPMASTER_OLD = 'baangt.TestSteps.TestStepMaster'
CLASSES_TESTSTEPMASTER = 'TestStepMaster'

TIMING_END = "end"
TIMING_START = "start"
TIMING_TESTRUN = "Complete Testrun"
TIMING_DURATION = "Duration"
TIMESTAMP = "timestamp"
TIMELOG = "timelog"

GECKO_DRIVER = "geckodriver.exe"
CHROME_DRIVER = "chromedriver.exe"

BROWSER_FIREFOX = "FF"
BROWSER_CHROME = "CHROME"
BROWSER_SAFARI = "SAFARI"
BROWSER_EDGE = "EDGE"
BROWSER_REMOTE = 'REMOTE'
BROWSER_MODE_HEADLESS = "HEADLESS"
BROWSER_ATTRIBUTES = "BrowserAttributes"

CMD_CLICK = "CLICK"
CMD_SETTEXT = "SETTEXT"
CMD_FORCETEXT = "FORCETEXT"

TESTCASESTATUS = "TestCaseStatus"
TESTCASESTATUS_SUCCESS = "OK"
TESTCASESTATUS_ERROR = "Failed"
TESTCASESTATUS_WAITING = "Paused"
TESTCASEERRORLOG = "TCErrorLog"
TESTCASE_EXPECTED_ERROR_FIELD = "TC Expected Error"

DATABASE_FROM_LINE = "FromLine"
DATABASE_TO_LINE = "ToLine"
DATABASE_LINES = "Lines"
DATABASE_FILENAME = "TestDataFileName"
DATABASE_SHEETNAME = "Sheetname"
DATABASE_EXPORTFILENAMEANDPATH = "exportFilesBasePath"

STRUCTURE_TESTCASESEQUENCE = "TESTSEQUENCE"
STRUCTURE_TESTCASE = "TESTCASE"
STRUCTURE_TESTSTEP = "TestStep"
STRUCTURE_TESTSTEPEXECUTION = "TestStepExecutionParameters"

EXECUTION_PARALLEL = "ParallelRuns"
SCREENSHOTS = "Screenshots"
EXECUTION_DONTCLOSEBROWSER = "dontCloseBrowser"
EXECUTION_SLOW = "slowExecution"

EXPORT_FORMAT = "Export Format"
EXP_FIELDLIST = "Fieldlist"
EXP_XLSX = "XLSX"
EXP_CSV = "CSV"

PATH_EXPORT = 'ExportPath'
PATH_IMPORT = 'ImportPath'
PATH_SCREENSHOTS = 'ScreenshotPath'
PATH_ROOT = 'RootPath'

ADDRESS_COUNTRYCODE = "CountryCode"
ADDRESS_POSTLCODE = "PostlCode"
ADDRESS_CITYNAME = "CityName"
ADDRESS_STREETNAME = "StreetName"
ADDRESS_HOUSENUMBER = "HouseNumber"
ADDRESS_ADDITION1 = "Addition1"
ADDRESS_ADDITION2 = "Addition2"

WIN_PLATFORM = 'windows'
LINUX_PLATFORM = 'linux'

BIT_64 = 8
BIT_32 = 4

OS_list = ["Linux-32", "Linux-64", "MacOS", "Windows-32", "Windows-64"]
OS_list_chrome = ['linux32', 'linux64', 'mac64', 'win32']

GECKO_URL = 'https://api.github.com/repos/mozilla/geckodriver/releases/latest'


CHROME_URL = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
NETWORK_INFO = 'NetworkInfo'
PATH_BROWSER_PROXY = '../../browsermob-proxy-2.1.4/bin/browsermob-proxy'
BROWSER_PROXY_URL = 'https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy/browsermob-proxy-bin.zip'
