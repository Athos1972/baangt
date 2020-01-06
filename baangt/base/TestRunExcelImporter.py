from baangt.base.utils import utils
from baangt.base.TestRunUtils import TestRunUtils
import baangt.base.GlobalConstants as GC
import baangt.base.CustGlobalConstants as CGC
import xlrd
import logging

logger = logging.getLogger("pyC")


class TestRunExcelImporter:
    def __init__(self, FileNameAndPath, testRunUtils: TestRunUtils):
        # self.testRunAttributes = testRunUtils.testRunAttributes
        self.testRunUtils = testRunUtils
        try:
            self.excelFile = xlrd.open_workbook(FileNameAndPath)
        except FileNotFoundError as e:
            raise BaseException(f"File not found - exiting {e}")

        self.fileName = utils.extractFileNameFromFullPath(FileNameAndPath)

    def importConfig(self):
        self._initTestRun()
        return self.testRunUtils.getCompleteTestRunAttributes(self.fileName)

    def _initTestRun(self):
        self.testRunUtils.testRunAttributes = \
            {
                self.fileName: {
                    GC.KWARGS_TESTRUNATTRIBUTES: {
                    },
                },
            }
        testRunAttributes = self.testRunUtils.testRunAttributes[self.fileName][GC.KWARGS_TESTRUNATTRIBUTES]

        xlsTab = self._getTab("TestRun")
        testRunAttributes[GC.EXPORT_FORMAT] = {GC.EXPORT_FORMAT: self._getValueFromList(xlsTab=xlsTab,
                                                                                        searchField=GC.EXPORT_FORMAT)}
        xlsTab = self._getTab("ExportFieldList")
        testRunAttributes[GC.EXPORT_FORMAT][GC.EXP_FIELDLIST] = self._getRowAsList(xlsTab)

        testRunAttributes[GC.STRUCTURE_TESTCASESEQUENCE] = {}
        testrunSequence = testRunAttributes[GC.STRUCTURE_TESTCASESEQUENCE]
        xlsTab = self._getTab("TestCaseSequence")
        lSequenceDict = self.getRowsWithHeadersAsDict(xlsTab=xlsTab)
        for key, sequence in lSequenceDict.items():
            testrunSequence[key] = [sequence["SequenceClass"], {}]
            for field, value in sequence.items():
                testRunAttributes[GC.STRUCTURE_TESTCASESEQUENCE][key][1][field] = value

        xlsTab = self._getTab("TestCase")
        lTestCaseDict = self.getRowsWithHeadersAsDict(xlsTab=xlsTab)
        for key, testCase in lTestCaseDict.items():
            testSequenceRoot = testrunSequence[testCase["TestCaseSequenceNumber"]][1]
            testSequenceRoot[GC.STRUCTURE_TESTCASE] = {testCase["TestCaseNumber"]: []}
            testSequenceRoot[GC.STRUCTURE_TESTCASE][testCase["TestCaseNumber"]].append(testCase["TestCaseClass"])
            testSequenceRoot[GC.STRUCTURE_TESTCASE][testCase["TestCaseNumber"]].append(
                {"TestCaseType": testCase["TestCaseType"],
                 GC.KWARGS_BROWSER: testCase["Browser"],
                 GC.BROWSER_ATTRIBUTES: testCase["BrowserAttributes"]
                 })

        xlsTab = self._getTab("TestStep")
        lStepDict = self.getRowsWithHeadersAsDict(xlsTab=xlsTab)
        for key, testStep in lStepDict.items():
            testStepRoot = testrunSequence[testStep["TestCaseSequenceNumber"]][1]
            testStepRoot = testStepRoot[GC.STRUCTURE_TESTCASE][testStep["TestCaseNumber"]]
            if len(testStepRoot) == 2:
                testStepRoot.append({GC.STRUCTURE_TESTSTEP: {}})

            testStepRoot = testStepRoot[2][GC.STRUCTURE_TESTSTEP]
            testStepRoot[testStep["TestStepNumber"]] = testStep["TestStepClass"]

        xlsTab = self._getTab("TestStepExecution")
        lExecDict = self.getRowsWithHeadersAsDict(xlsTab=xlsTab)
        for key,execLine in lExecDict.items():
            lSequence = self.testRunUtils.getSequenceByNumber(testRunName=self.fileName,
                                                              sequence=execLine["TestCaseSequenceNumber"])
            lTestCase = self.testRunUtils.getTestCaseByNumber(sequence=lSequence,
                                                              testcaseNumber=execLine["TestCaseNumber"])
            lTestStep = self.testRunUtils.getTestStepByNumber(testCase=lTestCase,
                                                              testStepNumber=execLine["TestStepNumber"])
            # if this TestStep is still just a String, then it needs to be converted into a List with Dict
            # to hold the TestexecutionSteps in this Dict.
            if isinstance(lTestStep, str):
                lTestCase[2][GC.STRUCTURE_TESTSTEP][execLine["TestStepNumber"]] = \
                    [lTestStep, {GC.STRUCTURE_TESTSTEPEXECUTION: {}}]
                lTestStep = self.testRunUtils.getTestStepByNumber(testCase=lTestCase,
                                                                  testStepNumber=execLine["TestStepNumber"])

            lTestStep[1][GC.STRUCTURE_TESTSTEPEXECUTION][execLine["TestStepExecutionNumber"]] = {}
            for lkey, value in execLine.items():
                lTestStep[1][GC.STRUCTURE_TESTSTEPEXECUTION][execLine["TestStepExecutionNumber"]][lkey] = value

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
        for row in range(1, xlsTab.nrows):
            if xlsTab.cell_value(row, 1) == searchField:
                return self.replaceFieldValueWithValueOfConstant(xlsTab.cell_value(row, 2))

    def _getTab(self, tabName):
        worksheet = self.excelFile.sheet_by_name(tabName)
        return worksheet

    def replaceFieldValueWithValueOfConstant(self, value):
        if isinstance(value, float):
            if value % 1 == 0:
                return int(value)
        elif isinstance(value, int):
            return value

        value = value.strip()
        value = utils.replaceFieldValueWithValueOfConstant(value)

        if value[0:4] == "CGC.":
            value = getattr(globals()[value.split(".")[0]], value.split(".")[1])

        return value
