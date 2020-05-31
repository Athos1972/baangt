KWARGS_DATA = "data"
KWARGS_MOBILE = "Mobile"
KWARGS_MOBILE_APP = "MobileApp"
KWARGS_BROWSER = "Browser"
KWARGS_API_SESSION = "api"
KWARGS_APPIUM = 'Appium'
KWARGS_TESTCASETYPE = "TestCaseType"
KWARGS_TESTRUNATTRIBUTES = "TESTRUNEXECUTIONPARAMETERS"
KWARGS_TESTRUNINSTANCE = "TESTRUNINSTANCE"
KWARGS_TIMING = "TimingClassInstance"
KWARGS_SEQUENCENUMBER = "SequenceNumberOfThisTestCase"

CLASSES_TESTCASESEQUENCE = "baangt.TestCaseSequence.TestCaseSequenceMaster.TestCaseSequenceMaster"
# CLASSES_TESTCASESEQUENCE_new = "TestCaseSequenceMaster"
CLASSES_TESTCASE = "baangt.TestCase.TestCaseMaster.TestCaseMaster"
# CLASSES_TESTCASE_new = 'TestCaseMaster'
CLASSES_TESTSTEPMASTER = 'baangt.TestSteps.TestStepMaster.TestStepMaster'
# CLASSES_TESTSTEPMASTER_new = 'TestStepMaster'

TIMING_END = "end"
TIMING_START = "start"
TIMING_TESTRUN = "Complete Testrun"
TIMING_DURATION = "Duration"
TIMESTAMP = "timestamp"
TIMELOG = "timelog"

GECKO_DRIVER = "geckodriver.exe"
CHROME_DRIVER = "chromedriver.exe"
EDGE_DRIVER = "msedgedriver.exe"
REMOTE_EXECUTE_URL = "http://localhost:4444/wd/hub"

BROWSER_FIREFOX = "FF"
BROWSER_CHROME = "CHROME"
BROWSER_SAFARI = "SAFARI"
BROWSER_EDGE = "EDGE"
BROWSER_REMOTE = 'REMOTE'
BROWSER_REMOTE_V4 = 'REMOTE_V4'
BROWSER_APPIUM = 'APPIUM'
BROWSER_MODE_HEADLESS = "HEADLESS"
BROWSER_ATTRIBUTES = "BrowserAttributes"
BROWSER_WINDOW_SIZE = "BrowserWindowSize"
BROWSER_ZOOM_FACTOR = "BrowserZoomFactor"

CMD_CLICK = "CLICK"
CMD_SETTEXT = "SETTEXT"
CMD_FORCETEXT = "FORCETEXT"

TESTCASESTATUS = "TestCaseStatus"
TESTCASESTATUS_SUCCESS = "OK"
TESTCASESTATUS_ERROR = "Failed"
TESTCASESTATUS_WAITING = "Paused"
TESTCASEERRORLOG = "TCErrorLog"
TESTCASESTATUS_STOP = "TCStopTestCase"
TESTCASESTATUS_STOPERROR = "TCStopTestCaseError"
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
EXECUTION_NETWORK_INFO = 'NetworkInfo'
EXECUTION_LOGLEVEL = "LogLevel"

EXECUTION_STAGE = 'Stage'
EXECUTION_STAGE_TEST = 'Test'
EXECUTION_STAGE_DEVELOPMENT = 'Development'
EXECUTION_STAGE_PRODUCTION = 'Production'
EXECUTION_STAGE_QA = 'Quality Assurance'

EXPORT_FORMAT = "ExportFormat"
EXPORT_ADDITIONAL_DATA = "AdditionalExportTabs"
EXP_FIELDLIST = "Fieldlist"
EXP_XLSX = "XLSX"
EXP_CSV = "CSV"

PATH_EXPORT = '1TestResults'
PATH_IMPORT = '0TestInput'
PATH_SCREENSHOTS = 'Screenshots'
PATH_ROOT = 'RootPath'

ADDRESS_COUNTRYCODE = "CountryCode"
ADDRESS_POSTLCODE = "PostlCode"
ADDRESS_CITYNAME = "CityName"
ADDRESS_STREETNAME = "StreetName"
ADDRESS_HOUSENUMBER = "HouseNumber"
ADDRESS_ADDITION1 = "Addition1"
ADDRESS_ADDITION2 = "Addition2"

MOBILE_PLATFORM_NAME = "platformName"
MOBILE_DEVICE_NAME = "deviceName"
MOBILE_PLATFORM_VERSION = "platformVersion"
MOBILE_APP_URL = 'app'
MOBILE_APP_PACKAGE = 'appPackage'
MOBILE_APP_ACTIVITY = 'appActivity'
MOBILE_APP_BROWSER_PATH = 'mobileAppBrowserPath'   # Path to Browser on Mobile device

WIN_PLATFORM = 'windows'
LINUX_PLATFORM = 'linux'

BIT_64 = 8
BIT_32 = 4

OS_list = ["Linux-32", "Linux-64", "MacOS", "Windows-32", "Windows-64"]
OS_list_chrome = ['linux32', 'linux64', 'mac64', 'win32']

GECKO_URL = 'https://api.github.com/repos/mozilla/geckodriver/releases/latest'
CHROME_URL = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'

BROWSER_PROXY_PATH = '/browsermob-proxy/bin/browsermob-proxy'
BROWSER_PROXY_URL = 'https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy/browsermob-proxy-bin.zip'

PROXY_FAILCOUNTER = 3

TESTDATAGENERATOR_OUTPUT_FORMAT = "xlsx"
TESTDATAGENERATOR_INPUTFILE = "RawTestData.xlsx"
TESTDATAGENERATOR_OUTPUTFILE_XLSX = "output.xlsx"
TESTDATAGENERATOR_OUTPUTFILE_CSV = "output.csv"

REPORT_PATH = 'reports'
