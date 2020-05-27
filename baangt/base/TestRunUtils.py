from baangt.base.TestRun.ClassesForObjects import ClassesForObjects
import baangt.base.GlobalConstants as GC
import logging

logger = logging.getLogger("pyC")

class TestRunUtils():
    def __init__(self):
        self.testRunAttributes = {}

    def setCompleteTestRunAttributes(self, testRunName:str, testRunAttributes: dict):
        self.testRunAttributes[testRunName] = testRunAttributes

    def getCompleteTestRunAttributes(self, testRunName):
        logger.info('get into getCompleteTestRunAttributes, testRunName is {}'.format(testRunName))
        return self.testRunAttributes[testRunName][GC.KWARGS_TESTRUNATTRIBUTES]

    def getSequenceByNumber(self, sequence, testRunName):
        return self.testRunAttributes[testRunName][GC.KWARGS_TESTRUNATTRIBUTES][GC.STRUCTURE_TESTCASESEQUENCE].get(sequence)

    def getTestCaseByNumber(self, sequence, testcaseNumber):
        return sequence[1][GC.STRUCTURE_TESTCASE].get(testcaseNumber) or \
               sequence[1][GC.STRUCTURE_TESTCASE].get(int(testcaseNumber)) or \
               sequence[1][GC.STRUCTURE_TESTCASE].get(str(testcaseNumber))

    def getTestStepByNumber(self, testCase, testStepNumber):
        return testCase[2][GC.STRUCTURE_TESTSTEP].get(testStepNumber) or \
               testCase[2][GC.STRUCTURE_TESTSTEP].get(int(testStepNumber)) or \
               testCase[2][GC.STRUCTURE_TESTSTEP].get(str(testStepNumber))


    def replaceClasses(self, testRunName, classes:ClassesForObjects, ):
        """
        Apart from what is defined in the TestRunDefintion (XLSX or "guessed" by TestRunExcelImporter) the user
        may give new class names in the globals file.

        We shall replace all corresponding appearances with those new class names

        :param classes:
        :return: No return parameter. Changes are kept internally
        """
        lTestRun = self.testRunAttributes[testRunName]

        try:
            for n in range(1,999):
                lSequence = self.getSequenceByNumber(n, testRunName=testRunName)
                if lSequence:
                    lSequence[0] = classes.testCaseSequenceMaster
                    lSequence[1]["SequenceClass"] = classes.testCaseSequenceMaster
                else:
                    break
        except BaseException as e:
            pass # This was the last TestCaseSequence within this test case.

    def replaceGlobals(self, globals):
        """
        Will go through all testcase-Settings and replace values with values from global settings, if matched
        """
        for key, value in globals.items():
            if not "TC." in key[0:3]:
                continue
            if not isinstance(value, bool):
                if len(value) == 0:
                    continue
            self.testRunAttributes = TestRunUtils._recursive_replace(self.testRunAttributes, key.replace("TC.",""), value)

    @staticmethod
    def _recursive_replace(dictToBeReplaced, lKey, lValue):
        if isinstance(dictToBeReplaced, list):
            for entry in dictToBeReplaced:
                TestRunUtils._recursive_replace(entry, lKey, lValue)
        elif isinstance(dictToBeReplaced, dict):
            if lKey in dictToBeReplaced:
                logger.info(f"Due to Globals replaced value {dictToBeReplaced[lKey]} of {lKey} with value {lValue}")
                dictToBeReplaced[lKey] = lValue
            for k,v in dictToBeReplaced.items():
                TestRunUtils._recursive_replace(v, lKey, lValue)
        else:
            pass
        return dictToBeReplaced
