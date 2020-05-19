from baangt import hook_spec
from baangt.base import GlobalConstants as GC

# -------------------------------------------------------------------

# correspond to baangt/base/TestRun

# -------------------------------------------------------------------


class baangtHookSpec(object):

    @hook_spec
    def testRun_init(self, testRunName, globalSettingsFileNameAndPath):
        pass


    @hook_spec
    def testRun_tearDown(self, testRunObject):
        pass


    @hook_spec
    def testRun_getSuccessAndError(self, testRunObject):
        pass


    @hook_spec
    def testRun_getAllTestRunAttributes(self, testRunObject):
        pass


    @hook_spec
    def testRun_getBrowser(self, testRunObject, browserInstance=1, browserName=None, browserAttributes=None):
        pass


    @hook_spec
    def testRun__getBrowserInstance(self, testRunObject, browserInstance):
        pass


    @hook_spec
    def testRun_getAPI(self, testRunObject):
        pass


    @hook_spec
    def testRun_setResult(self, testRunObject, recordNumber, dataRecordResult):
        pass


    @hook_spec
    def testRun_executeTestRun(self, testRunObject):
        pass


    @hook_spec
    def testRun_executeDictSequenceOfClasses(self, testRunObject, dictSequenceOfClasses, counterName, **kwargs):
        pass


    @hook_spec
    def testRun__initTestRun(self, testRunObject):
        pass


    @hook_spec
    def testRun_loadJSONGlobals(self, testRunObject):
        pass


    @hook_spec
    def testRun__loadJSONTestRunDefinitions(self, testRunObject):
        pass


    @hook_spec
    def testRun__loadExcelTestRunDefinitions(self, testRunObject):
        pass


    @hook_spec
    def testRun___dynamicImportClasses(self, fullQualifiedImportName):
        pass


    @hook_spec
    def testRun__sanitizeTestRunNameAndFileName(self, TestRunNameInput):
        pass

    # -------------------------------------------------------------------

    # correspond to baangt/base/Timing

    # -------------------------------------------------------------------

    @hook_spec
    def timing_init(self):
        pass

    @hook_spec
    def timing_takeTime(self, timingObject, timingName, forceNew=False):
        pass

    @hook_spec
    def timing_addAttribute(self, timingObject, attribute, value, timingSection=None):
        pass

    @hook_spec
    def timing_takeTimeSumOutput(self, timingObject):
        pass

    @hook_spec
    def timing_returnTime(self, timingObject):
        pass

    @hook_spec
    def timing_returnTimeSegment(self, timingObject, segment):
        pass

    @hook_spec
    def timing_resetTime(self, timingObject):
        pass

    @hook_spec
    def timing___format_time(self, startAndEndTimeAsDict):
        pass

    # -------------------------------------------------------------------

    # correspond to baangt/base/ExportResults

    # -------------------------------------------------------------------

    # ExportResults

    # -------------------------------------------------------------------
    @hook_spec
    def exportResults_init(self,  **kwargs):
        pass


    @hook_spec
    def exportResults_exportToDataBase(self, exportResultsObject):
        pass


    @hook_spec
    def exportResults_exportResult(self, exportResultsObject, **kwargs):
        pass


    @hook_spec
    def exportResults_makeSummary(self, exportResultsObject):
        pass


    @hook_spec
    def exportResults___writeSummaryCell(self, exportResultsObject, lineHeader, lineText, row=None, format=None):
        pass


    @hook_spec
    def exportResults___getOutputFileName(self, exportResultsObject):
        pass


    @hook_spec
    def exportResults___setHeaderDetailSheet(self, exportResultsObject):
        pass


    @hook_spec
    def exportResults__exportData(self, exportResultsObject):
        pass


    @hook_spec
    def exportResults___writeCell(self, exportResultsObject, line, cellNumber, testRecordDict, fieldName, strip=False):
        pass


    @hook_spec
    def exportResults_closeExcel(self, exportResultsObject, line, cellNumber, testRecordDict, fieldName, strip=False):
        pass

    # -------------------------------------------------------------------

    # correspond to baangt/base/ExportResults

    # -------------------------------------------------------------------

    # ExcelSheetHelperFunctions

    # -------------------------------------------------------------------
    @hook_spec
    def excelSheetHelperFunctions_init(self):
        pass


    @hook_spec
    def excelSheetHelperFunctions_set_column_autowidth(self, excelSheetHelperFunctionsObject, worksheet, column):
        pass


    @hook_spec
    def excelSheetHelperFunctions_get_column_width(self, excelSheetHelperFunctionsObject, worksheet, column):
        pass

    # -------------------------------------------------------------------

    # correspond to baangt/base/ExportResults

    # -------------------------------------------------------------------

    # ExportTiming

    # -------------------------------------------------------------------


    @hook_spec
    def exportTiming_init(self, testdataRecords, sheet):
        pass


    @hook_spec
    def exportTiming_writeHeader(self, exportTimingObject):
        pass


    @hook_spec
    def exportTiming_writeLines(self, exportTimingObject):
        pass


    @hook_spec
    def exportTiming_shortenTimingValue(self, exportTimingObject, timingValue):
        pass


    @hook_spec
    def exportTiming_writeCell(self, exportTimingObject, row, col, content, format=None):
        pass


    @hook_spec
    def exportTiming_findAllTimingSections(self, exportTimingObject):
        pass


    @hook_spec
    def exportTiming_interpretTimeLog(self, exportTimingObject, lTimeLog):
        pass


    # -------------------------------------------------------------------

    # correspond to baangt/base/BrowserDriver

    # -------------------------------------------------------------------

    @hook_spec
    def browserDriver_init(self, timing=None, screenshotPath=None):
        pass


    @hook_spec
    def browserDriver_createNewBrowser(self, browserDriverObject, browserName=GC.BROWSER_FIREFOX, desiredCapabilities=None, **kwargs):
        pass

    @hook_spec
    def browserDriver_slowExecutionToggle(self, browserDriverObject, newSlowExecutionWaitTimeInSeconds = None):
        pass

    @hook_spec
    def browserDriver_closeBrowser(self, browserDriverObject):
        pass

    @hook_spec
    def browserDriver_takeScreenshot(self, browserDriverObject, screenShotPath=None):
        pass


    @hook_spec
    def browserDriver_handleIframe(self, browserDriverObject, iframe=None):
        pass

    @hook_spec
    def browserDriver_handleWindow(self, browserDriverObject, windowNumber=None, function=None):
        pass


    @hook_spec
    def browserDriver_findByAndWaitForValue(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None, iframe=None, timeout=20,
                                  optional=False):
        pass


    @hook_spec
    def browserDriver_findByAndSetText(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None, value=None, iframe=None,
                             timeout=60, optional=False):
        pass


    @hook_spec
    def browserDriver_findByAndSetTextIf(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None, value=None, iframe=None,
                               timeout=60):
        pass


    @hook_spec
    def browserDriver_findByAndSetTextValidated(self, browserDriverObject,id = None,
                           css = None,
                           xpath = None,
                           class_name = None,
                           value = None,
                           iframe = None,
                           timeout = 60,
                           retries = 5):
        pass


    @hook_spec
    def browserDriver_submit(self, browserDriverObject):
        pass


    @hook_spec
    def browserDriver_findByAndClick(self, browserDriverObject, id = None, css=None, xpath=None, class_name=None, iframe=None, timeout=20, optional=False):
        pass


    @hook_spec
    def browserDriver_findByAndClickIf(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None, iframe=None, timeout=60,
                             value=None, optional=False):
        pass


    @hook_spec
    def browserDriver_findByAndForceText(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None, value=None,
                               iframe=None, timeout=60, optional=False):
        pass


    @hook_spec
    def browserDriver_findBy(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None, iframe=None, timeout=60, loggingOn=True,
                   optional=False):
        pass


    @hook_spec
    def browserDriver_getURL(self, browserDriverObject):
        pass


    @hook_spec
    def browserDriver_findWaitNotVisible(self, browserDriverObject, xpath=None, id=None, timeout = 90):
        pass


    @hook_spec
    def browserDriver_sleep(self, browserDriverObject, sleepTimeinSeconds):
        pass


    @hook_spec
    def browserDriver_goToUrl(self, browserDriverObject, url):
        pass


    @hook_spec
    def browserDriver_goBack(self, browserDriverObject):
        pass


    @hook_spec
    def browserDriver_javaScript(self, browserDriverObject, jsText):
        pass


    # -------------------------------------------------------------------

    # correspond to baangt/base/WebdriverFunctions

    # -------------------------------------------------------------------

    @hook_spec
    def webdriverFunctions_webdriver_doSomething(self, webdriverobject, command, element, value=None, timeout=20, optional=False, browserData=None):
        pass


    @hook_spec
    def webdriverFunctions_webdriver_tryAndRetry(self, webdriverobject, browserData, timeout=20, optional=False):
        pass


    @hook_spec
    def webdriver_createBrowserOptions(self, webdriverobject, browserName, desiredCapabilities, browserMobProxy=None, randomProxy=None):
        pass


    # -------------------------------------------------------------------

    # correspond to baangt/base/BrowserHelperFunctions

    # -------------------------------------------------------------------

    @hook_spec
    def browserHelperFunction_browserHelper_log(self, browserHelperObject, logType, logText, browserData, cbTakeScreenshot = None, **kwargs):
        pass


    @hook_spec
    def browserHelperFunction_browserHelper_findBrowserDriverPaths(self, browserHelperObject ,filename):
        pass

