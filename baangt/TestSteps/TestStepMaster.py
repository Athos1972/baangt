import baangt.base.GlobalConstants as GC
from baangt.base.Timing import Timing
from baangt.base.BrowserHandling import BrowserDriver
import sys


class TestStepMaster:
    def __init__(self, **kwargs):
        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.testcaseDataDict = kwargs.get(GC.KWARGS_DATA)
        self.timing: Timing = kwargs.get(GC.KWARGS_TIMING)
        self.timingName = self.timing.takeTime(self.__class__.__name__, forceNew=True)
        self.browserSession : BrowserDriver = kwargs.get(GC.KWARGS_BROWSER)
        self.apiSession = kwargs.get(GC.KWARGS_API_SESSION)
        self.testCaseStatus = None
        self.testStepNumber = kwargs.get(GC.STRUCTURE_TESTSTEP) # Set in TestRun by TestCaseMaster
        self.testRunUtil = self.testRunInstance.testRunUtils
        # check, if this TestStep has additional Parameters and if so, execute
        lSequence = self.testRunUtil.getSequenceByNumber(testRunName=self.testRunInstance.testRunName,
                                                         sequence=kwargs.get(GC.STRUCTURE_TESTCASESEQUENCE))
        lTestCase = self.testRunUtil.getTestCaseByNumber(lSequence, kwargs.get(GC.STRUCTURE_TESTCASE))
        lTestStep = self.testRunUtil.getTestStepByNumber(lTestCase, kwargs.get(GC.STRUCTURE_TESTSTEP))
        self.ifActive = False
        self.ifIsTrue = True

        if not isinstance(lTestStep, str):
            # This TestStepMaster-Instance should actually do something - activitites are described
            # in the TestExecutionSteps
            self.executeDirect(lTestStep[1][GC.STRUCTURE_TESTSTEPEXECUTION])


    def executeDirect(self, executionCommands):
        """
        This will execute single Operations directly
        """
        for key, command in executionCommands.items():
            if not self.ifIsTrue and command["Activity"] != "ENDIF":
                continue

            xpath = None
            css = None
            id = None
            lActivity = command["Activity"].upper()
            lLocatorType = command["LocatorType"].upper()
            lLocator = command["Locator"]
            lValue = command["Value"]
            lValue2 = command["Value2"]
            lComparison = command["Comparison"]
            lTimeout = command["Timeout"]
            if lTimeout:
                lTimeout = float(lTimeout)
            else:
                lTimeout=20
            if lLocatorType:
                if lLocatorType == 'XPATH':
                    xpath = lLocator
                elif lLocatorType == 'CSS':
                    css = lLocator
                elif lLocatorType == 'ID':
                    id = lLocator
            if len(lValue) > 0:
                lValue = self.replaceVariables(lValue)
            if len(lValue2) > 0:
                lValue2 = self.replaceVariables(lValue2)

            if lActivity == "GOTOURL":
                self.browserSession.goToUrl(lValue)
            elif lActivity == "SETTEXT":
                self.browserSession.findByAndSetText(xpath=xpath, css=css, id=id, value = lValue, timeout=lTimeout)
            elif lActivity == 'HANDLEIFRAME':
                self.browserSession.handleIframe(lLocator)
            elif lActivity == "CLICK":
                self.browserSession.findByAndClick(xpath=xpath, css=css, id=id, timeout=lTimeout)
            elif lActivity == "IF":
                if self.ifActive:
                    raise BaseException("No nested IFs at this point, sorry...")
                self.ifActive = True
                self.__doComparisons(lComparison=lComparison, value1=lValue, value2=lValue2)
            elif lActivity == "ENDIF":
                if not self.ifActive:
                    raise BaseException("ENDIF without IF")
                self.ifActive = False
                self.ifIsTrue = True
            else:
                raise BaseException(f"Unknown command in TestStep {lActivity}")

    def __doComparisons(self, lComparison, value1, value2):
        if lComparison == "=":
            if value1 == value2:
                self.ifIsTrue = True
            else:
                self.ifIsTrue = False
        elif lComparison == ">":
            if value1 > value2:
                self.ifIsTrue = True
            else:
                self.ifIsTrue = False
        elif lComparison == "<":
            if value1 < value2:
                self.ifIsTrue = True
            else:
                self.ifIsTrue = False
        else:
            raise BaseException(f"Comparison Operator not supported/unknown {lComparison}")
    def execute(self):
        """Method is overwritten in all children"""
        pass

    def teardown(self):
        if self.testCaseStatus:
            if not self.testcaseDataDict[GC.TESTCASESTATUS]:
                self.testcaseDataDict[GC.TESTCASESTATUS] = self.testCaseStatus
            elif self.testCaseStatus == GC.TESTCASESTATUS_SUCCESS:
                # We'll not overwrite a potential Error Status of the testcase
                pass
            elif self.testCaseStatus == GC.TESTCASESTATUS_ERROR:
                self.testcaseDataDict = GC.TESTCASESTATUS_ERROR
            else:
                sys.exit("No idea, what happened here. Unknown condition appeared")
        self.timing.takeTime(self.timingName)

    def replaceVariables(self, expression):
        if not "$(" in expression:
            return expression

        while "$(" in expression:
            if expression[0:2] == "$(":
                left_part = ""
            else:
                left_part = expression.split("$(")[0]

            center = expression[len(left_part)+2:]
            center = center.split(")")[0]

            right_part = expression[len(left_part)+len(center)+3:]

            # Replace the variable with the value from data structure
            center = self.testcaseDataDict.get(center)
            if not center:
                raise BaseException(f"Variable not found: {center}")

            expression = "".join([left_part, center, right_part])
        return expression


if __name__ == '__main__':
    l_test = TestStepMaster()
    l_test.testcaseDataDict = {"MANDANT": "DON", "base_url": "portal-fqa", "VN": "12345"}
    print(l_test.replaceVariables("https://$(MANDANT)-$(base_url).corpnet.at/vigong-produktauswahl/produktauswahl/$(VN)"))