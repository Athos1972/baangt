from baangt.base.Utils import utils
from baangt.base.TestRunUtils import TestRunUtils
import baangt.base.GlobalConstants as GC
import baangt.base.CustGlobalConstants as CGC
import xlrd
import logging

logger = logging.getLogger("pyC")


class TestRunExcelImporter:
    """
    The TestrunSettings are in class TestRunUtils and expected to be a deep dict. For details see documentation there.

    This class will migrate data from an excel sheet (either simple format with only 1 tab or complex format with all
    structural elements) into the deep dict.

    In case the XLSX is simple format, all missing data is "predicted"/assumed.

    """
    def __init__(self, FileNameAndPath, testRunUtils: TestRunUtils):
        self.testStepExecutionNumber = 0
        # self.testRunAttributes = testRunUtils.testRunAttributes
        self.testRunUtils = testRunUtils

        try:
            self.excelFile = xlrd.open_workbook(FileNameAndPath)
        except FileNotFoundError as e:
            raise BaseException(f"File not found - exiting {e}")
        self.fileName = utils.extractFileNameFromFullPath(FileNameAndPath)

    def importConfig(self, global_settings):
        self._initTestRun(global_settings)
        return self.testRunUtils.getCompleteTestRunAttributes(self.fileName)

    def _initTestRun(self, global_settings):
        """
        Writes a new entry to testRunUtils --> = this current TestRunDefinition (Filename)
        Then loops through the tabs "TestRun", "ExportFieldList", "TestCaseSequence" and so on,
        reads the lines/columns and writes them the the deep dict of testRunUtils accordingly (TestCaseSequence,
        TestCase, TestStepSequence, TestSteps, etc.)
        @return:
        """
        self.testRunUtils.testRunAttributes = \
            {
                self.fileName: {
                    GC.KWARGS_TESTRUNATTRIBUTES: {
                    },
                },
            }
        testRunAttributes = self.testRunUtils.testRunAttributes[self.fileName][GC.KWARGS_TESTRUNATTRIBUTES]

        xlsTab = self._getTab("TestRun")
        if xlsTab:
            testRunAttributes[GC.EXPORT_FORMAT] = \
                {GC.EXPORT_FORMAT: self._getValueFromList(xlsTab=xlsTab,
                                                          searchField=GC.EXPORT_FORMAT)}
        else:
            # Default Value
            testRunAttributes[GC.EXPORT_FORMAT] = {GC.EXPORT_FORMAT: GC.EXP_XLSX}

        xlsTab = self._getTab("ExportFieldList")
        if xlsTab:
            testRunAttributes[GC.EXPORT_FORMAT][GC.EXP_FIELDLIST] = self._getRowAsList(xlsTab)
        else:
            # Default Value as there are no explicit values from the TestRunDefinition:
            testRunAttributes[GC.EXPORT_FORMAT][GC.EXP_FIELDLIST] = [GC.TESTCASESTATUS,
                                                                     GC.TIMING_DURATION,
                                                                     GC.TIMELOG]

        testRunAttributes[GC.STRUCTURE_TESTCASESEQUENCE] = {}
        testrunSequence = testRunAttributes[GC.STRUCTURE_TESTCASESEQUENCE]

        xlsTab = self._getTab("TestCaseSequence")
        if xlsTab:
            lSequenceDict = self.getRowsWithHeadersAsDict(xlsTab=xlsTab)
        else:
            lSequenceDict = {1:
                {
                "SequenceClass": GC.CLASSES_TESTCASESEQUENCE,
                "TestDataFileName": self.fileName,
                "Sheetname": "data",
                "ParallelRuns": 1,
                "FromLine": 0,
                "ToLine": 999999
                },
            }
        for key, sequence in lSequenceDict.items():
            testrunSequence[key] = [sequence["SequenceClass"], {}]
            for field, value in sequence.items():
                testRunAttributes[GC.STRUCTURE_TESTCASESEQUENCE][key][1][field] = value


        xlsTab = self._getTab("TestCase")
        # if Tab "TestCase" exists, then take the definitions from there. Otherwise (means simpleFormat)
        # we need to create "dummy" data ourselves.
        if xlsTab:
            lTestCaseDict = self.getRowsWithHeadersAsDict(xlsTab=xlsTab)
        else:
            # Dirty, but not possible in any other way in API-Simple-Format:
            if "API" in self.fileName.upper():
                    lTestCaseDict = {1: {"TestCaseSequenceNumber": 1,
                                     "TestCaseNumber": 1,
                                     "TestCaseType": GC.KWARGS_API_SESSION,
                                     "TestCaseClass": GC.CLASSES_TESTCASE}}
            else:
                if global_settings['TC.Mobile'] == 'True':
                    lTestCaseDict = {1: {"TestCaseSequenceNumber": 1,
                                         "TestCaseNumber": 1,
                                         "TestCaseType": GC.KWARGS_BROWSER,
                                         "TestCaseClass": GC.CLASSES_TESTCASE,
                                         GC.KWARGS_BROWSER: GC.BROWSER_FIREFOX,
                                         GC.BROWSER_ATTRIBUTES: "",
                                         GC.KWARGS_MOBILE: ""}}
                else:
                    lTestCaseDict = {1: {"TestCaseSequenceNumber": 1,
                                     "TestCaseNumber": 1,
                                     "TestCaseType": GC.KWARGS_BROWSER,
                                     "TestCaseClass": GC.CLASSES_TESTCASE,
                                     GC.KWARGS_BROWSER: GC.BROWSER_FIREFOX,
                                     GC.BROWSER_ATTRIBUTES: ""}}
        for key, testCase in lTestCaseDict.items():
            testSequenceRoot = testrunSequence[testCase["TestCaseSequenceNumber"]][1]
            testSequenceRoot[GC.STRUCTURE_TESTCASE] = {testCase["TestCaseNumber"]: []}
            testSequenceRoot[GC.STRUCTURE_TESTCASE][testCase["TestCaseNumber"]].append(testCase["TestCaseClass"])
            testSequenceRoot[GC.STRUCTURE_TESTCASE][testCase["TestCaseNumber"]].append(
                {"TestCaseType": testCase["TestCaseType"],
                 GC.KWARGS_BROWSER: testCase.get("Browser"),
                 GC.BROWSER_ATTRIBUTES: testCase.get("BrowserAttributes"),
                 GC.KWARGS_MOBILE: testCase.get("Mobile")
                 })

        xlsTab = self._getTab("TestStep")
        if xlsTab:
            lStepDict = self.getRowsWithHeadersAsDict(xlsTab=xlsTab)
        else:
            lStepDict = {1: {"TestCaseSequenceNumber": 1,
                         "TestCaseNumber": 1,
                         "TestStepNumber": 1,
                         "TestStepClass": GC.CLASSES_TESTSTEPMASTER}
                         }
        for key, testStep in lStepDict.items():
            testStepRoot = testrunSequence[testStep["TestCaseSequenceNumber"]][1]
            testStepRoot = testStepRoot[GC.STRUCTURE_TESTCASE][testStep["TestCaseNumber"]]
            if len(testStepRoot) == 2:
                testStepRoot.append({GC.STRUCTURE_TESTSTEP: {}})

            testStepRoot = testStepRoot[2][GC.STRUCTURE_TESTSTEP]
            testStepRoot[testStep["TestStepNumber"]] = testStep["TestStepClass"]


        xlsTab = self._getTab("TestStepExecution")
        lExecDict = self.getRowsWithHeadersAsDict(xlsTab=xlsTab)
        for key, execLine in lExecDict.items():
            lSequence = self.testRunUtils.getSequenceByNumber(testRunName=self.fileName,
                                                              sequence=execLine.get("TestCaseSequenceNumber",1))
            lTestCase = self.testRunUtils.getTestCaseByNumber(sequence=lSequence,
                                                              testcaseNumber=execLine.get("TestCaseNumber",1))
            lTestStep = self.testRunUtils.getTestStepByNumber(testCase=lTestCase,
                                                              testStepNumber=execLine.get("TestStepNumber",1))
            # if this TestStep is still just a String, then it needs to be converted into a List with Dict
            # to hold the TestexecutionSteps in this Dict.
            if isinstance(lTestStep, str):
                lTestCase[2][GC.STRUCTURE_TESTSTEP][execLine.get("TestStepNumber",1)] = \
                    [lTestStep, {GC.STRUCTURE_TESTSTEPEXECUTION: {}}]
                lTestStep = self.testRunUtils.getTestStepByNumber(testCase=lTestCase,
                                                                  testStepNumber=execLine.get("TestStepNumber",1))

            lStepExecutionNumber = self.__iterateStepExecutionNumber(execLine.get("TestStepExecutionNumber"))
            lTestStep[1][GC.STRUCTURE_TESTSTEPEXECUTION][lStepExecutionNumber] = {}
            for lkey, value in execLine.items():
                lTestStep[1][GC.STRUCTURE_TESTSTEPEXECUTION][lStepExecutionNumber][lkey] = value

    def __iterateStepExecutionNumber(self, numberFromDefinition):
        if numberFromDefinition:
            return numberFromDefinition

        # This is a teststep in simple format, without an execution number column in the XLS
        # we need to iterate ourselves and simply add 1 to each new TestStep
        self.testStepExecutionNumber += 1
        return self.testStepExecutionNumber

    def getRowsWithHeadersAsDict(self, xlsTab):
        lRetDict = {}

        for row in range(1, xlsTab.nrows):
            lRetDict[row] = {}
            for col in range(0, xlsTab.ncols):
                lRetDict[row][xlsTab.cell_value(0, col)] = self.replaceFieldValueWithValueOfConstant(
                    xlsTab.cell_value(row, col))
        return lRetDict

    def _getRowAsList(self, xlsTab, colNumber=0):
        l_fields = []
        for row in range(1, xlsTab.nrows):
            l_fields.append(self.replaceFieldValueWithValueOfConstant(xlsTab.cell_value(row, colNumber)))
        return l_fields

    def _getValueFromList(self, xlsTab, searchField):
        # Searches for Value in Column 1 and returns Value from Column 2 if found.
        # This is used for XLSX-Tabs with this format:
        # column:value
        # TestlineStart:10
        # TestlineEnd:20
        # foo:bar
        for row in range(1, xlsTab.nrows):
            if xlsTab.cell_value(row, 1) == searchField:
                return self.replaceFieldValueWithValueOfConstant(xlsTab.cell_value(row, 2))

    def _getTab(self, tabName):
        try:
            worksheet = self.excelFile.sheet_by_name(tabName)
        except Exception as e:
            return None
        return worksheet

    def replaceFieldValueWithValueOfConstant(self, value):
        """
        baangt Global constants (baangt.base.GlobalConstants) are available everywhere as GC., e.g. the variable
        "BROWSER" defined in GlobalConstants can be accessed from everywhere within baangt by using "GC.BROWSER".

        The variables can also be used in configuration files (would be very stupid if we need to change a constant and
        then 100s of Config-Files need adjustment - worst case the testruns behave unexepected). This applies both to
        XLSX and JSON Config files.

        The CGC.-Part is still needs fixing. It shouldn't appear in Baangt base, but currently still needed.

        @param value: potentially convertable value (e.g. GC.BROWSER)
        @return: potentially converted value (e.g. "Browser")
        """
        if isinstance(value, float):
            if value % 1 == 0:
                return int(value)
        elif isinstance(value, int):
            return value

        value = value.strip()
        value = utils.replaceFieldValueWithValueOfConstant(value)

        if value[0:5] == "CGC.":
            value = getattr(globals()[value.split(".")[0]], value.split(".")[1])

        return value
