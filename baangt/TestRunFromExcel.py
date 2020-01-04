from baangt.TestRun import TestRun
from baangt.utils import utils
import baangt.GlobalConstants as GC
import baangt.CustGlobalConstants as CGC
import xlrd
import logging

logger = logging.getLogger("pyC")

class TestRunFromExcel(TestRun):
    def __init__(self, lExcelDefinitionFile:str):
        self.excelFile = xlrd.open_workbook(lExcelDefinitionFile)
        self.fileAndPathName = lExcelDefinitionFile
        self.fileName = utils.extractFileNameFromFullPath(self.fileAndPathName)
        if not self.excelFile:
            raise(f"ConfigFile not found {lExcelDefinitionFile}")
        super().__init__(testRunName=self.fileName)

    def _initTestRun(self):
        self.testrunAttributes = {
            self.fileName: {
                GC.KWARGS_TESTRUNATTRIBUTES: {
            },},}
        testrunAttributes = self.testrunAttributes[self.fileName][GC.KWARGS_TESTRUNATTRIBUTES]

        xlsTab = self._getTab("TestRun")
        testrunAttributes[GC.EXPORT_FORMAT] = {GC.EXPORT_FORMAT: self._getValueFromList(xlsTab=xlsTab,
                                                                                        searchField=GC.EXPORT_FORMAT)}
        xlsTab = self._getTab("ExportFieldList")
        testrunAttributes[GC.EXPORT_FORMAT][GC.EXP_FIELDLIST] = self._getRowAsList(xlsTab)

        testrunAttributes[GC.STRUCTURE_TESTCASESEQUENCE] = {}
        testrunSequence = testrunAttributes[GC.STRUCTURE_TESTCASESEQUENCE]
        xlsTab = self._getTab("TestCaseSequence")
        lSequenceDict = self.getRowsWithHeadersAsDict(xlsTab=xlsTab)
        for key, sequence in lSequenceDict.items():
            testrunSequence[key] = [sequence["SequenceClass"], {}]
            for field, value in sequence.items():
                testrunAttributes[GC.STRUCTURE_TESTCASESEQUENCE][key][1][field] = value

        xlsTab = self._getTab("TestCase")
        lTestCaseDict = self.getRowsWithHeadersAsDict(xlsTab=xlsTab)
        for key, testCase in lTestCaseDict.items():
            testSequenceRoot = testrunSequence[testCase["TestCaseSequenceNumber"]][1]
            testSequenceRoot[GC.STRUCTURE_TESTCASE] = {testCase["TestCaseNumber"]:[]}
            testSequenceRoot[GC.STRUCTURE_TESTCASE][testCase["TestCaseNumber"]].append(testCase["TestCaseClass"])
            testSequenceRoot[GC.STRUCTURE_TESTCASE][testCase["TestCaseNumber"]].append(
                {"TestCaseType": testCase["TestCaseType"],
                 GC.KWARGS_BROWSER: testCase["Browser"],
                 GC.BROWSER_ATTRIBUTES: testCase["BrowserAttributes"]
                 })
            for field, value in testCase.items():
                pass

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
        for key, execLine in lExecDict.items():
            lSequence = self.getSequenceByNumber(execLine["TestCaseSequenceNumber"])
            lTestCase = self.getTestCaseByNumber(sequence = lSequence,
                                                 testcaseNumber=execLine["TestCaseNumber"])
            lTestStep = self.getTestStepByNumber(testCase=lTestCase,
                                                 testStepNumber=execLine["TestStepNumber"])
            # if this TestStep is still just a String, then it needs to be converted into a List with Dict
            # to hold the TestexecutionSteps in this Dict.
            if isinstance(lTestStep, str):
                lTestCase[2][GC.STRUCTURE_TESTSTEP][execLine["TestStepNumber"]] = \
                    [lTestStep, {GC.STRUCTURE_TESTSTEPEXECUTION: {}}]
                lTestStep = self.getTestStepByNumber(testCase=lTestCase,
                                                     testStepNumber=execLine["TestStepNumber"])

            lTestStep[1][GC.STRUCTURE_TESTSTEPEXECUTION][execLine["TestStepExecutionNumber"]] = {}
            for key, value in execLine.items():
                lTestStep[1][GC.STRUCTURE_TESTSTEPEXECUTION][execLine["TestStepExecutionNumber"]][key] = value
                pass

    def getRowsWithHeadersAsDict(self, xlsTab):
        lRetDict = {}

        for row in range(1, xlsTab.nrows):
            lRetDict[row] = {}
            for col in range(0, xlsTab.ncols):
                lRetDict[row][xlsTab.cell_value(0,col)] = self.sanitizeFieldValue(xlsTab.cell_value(row,col))
        return lRetDict

    def _getRowAsList(self, xlsTab, colNumber=0):
        l_fields = []
        for row in range(1, xlsTab.nrows):
            l_fields.append(self.sanitizeFieldValue(xlsTab.cell_value(row, colNumber)))
        return l_fields

    def _getValueFromList(self, xlsTab, searchField):
        # Searches for Value in Column 1 and returns Value from Column 2 if found.
        for row in range(1, xlsTab.nrows):
            if xlsTab.cell_value(row,1) == searchField:
                return self.sanitizeFieldValue(xlsTab.cell_value(row,2))

    def _getTab(self, tabName):
        worksheet = self.excelFile.sheet_by_name(tabName)
        return worksheet

    def sanitizeFieldValue(self, value):
        if isinstance(value, float):
            if value % 1 == 0:
                return int(value)
        elif isinstance(value, int):
            return value

        #value = value.replace("'", "") # not possible due to XPATH-Notation in some fields
        #value = value.replace('"', "") # not possible due to XPATH-Notation in some fields.
        value = value.strip()
        if value[0:3] == "GC." or value[0:4] == "CGC.":
            # value = globals()[value] --> Doesn't work
            # value = getattr(value.split(".")[0], value.split(".")[1]) --> Doesn't work
            value = getattr(globals()[value.split(".")[0]], value.split(".")[1])
        return value


