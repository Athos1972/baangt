import baangt.base.GlobalConstants as GC
from baangt.base.Timing.Timing import Timing
from baangt.base.BrowserHandling.BrowserHandling import BrowserDriver
from baangt.base.ApiHandling import ApiHandling
import sys
from pkg_resources import parse_version
import logging
from baangt.TestSteps.Exceptions import baangtTestStepException
from baangt.TestSteps.AddressCreation import AddressCreate

logger = logging.getLogger("pyC")


class TestStepMaster:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.testcaseDataDict = kwargs.get(GC.KWARGS_DATA)
        self.timing: Timing = kwargs.get(GC.KWARGS_TIMING)
        self.timingName = self.timing.takeTime(self.__class__.__name__, forceNew=True)
        self.browserSession: BrowserDriver = kwargs.get(GC.KWARGS_BROWSER)
        self.apiSession: ApiHandling = kwargs.get(GC.KWARGS_API_SESSION)
        self.testCaseStatus = None
        self.testStepNumber = kwargs.get(GC.STRUCTURE_TESTSTEP)    # Set in TestRun by TestCaseMaster
        self.testRunUtil = self.testRunInstance.testRunUtils
        # check, if this TestStep has additional Parameters and if so, execute
        lSequence = self.testRunUtil.getSequenceByNumber(testRunName=self.testRunInstance.testRunName,
                                                         sequence=kwargs.get(GC.STRUCTURE_TESTCASESEQUENCE))
        lTestCase = self.testRunUtil.getTestCaseByNumber(lSequence, kwargs.get(GC.STRUCTURE_TESTCASE))
        lTestStep = self.testRunUtil.getTestStepByNumber(lTestCase, kwargs.get(GC.STRUCTURE_TESTSTEP))
        self.globalRelease = self.testRunInstance.globalSettings.get("Release", "")
        self.ifActive = False
        self.ifIsTrue = True

        if not isinstance(lTestStep, str):
            # This TestStepMaster-Instance should actually do something - activitites are described
            # in the TestExecutionSteps
            self.executeDirect(lTestStep[1][GC.STRUCTURE_TESTSTEPEXECUTION])

        self.teardown()

    def executeDirect(self, executionCommands):
        """
        This will execute single Operations directly
        """
        for key, command in executionCommands.items():
            # when we have an IF-condition and it's condition was not TRUE, then skip whatever comes here until we
            # reach Endif
            if not self.ifIsTrue and command["Activity"] != "ENDIF":
                continue
            lActivity = command["Activity"].upper()
            if lActivity == "COMMENT":
                continue     # Comment's are ignored

            lLocatorType = command["LocatorType"].upper()
            lLocator = self.replaceVariables(command["Locator"])

            if lLocator and not lLocatorType:   # If locatorType is empty, default it to XPATH
                lLocatorType = 'XPATH'

            xpath, css, id = self.__setLocator(lLocatorType, lLocator)

            lValue = str(command["Value"])
            lValue2 = str(command["Value2"])
            lComparison = command["Comparison"]
            lOptional = TestStepMaster._sanitizeXField(command["Optional"])

            # check release line
            lRelease = command["Release"]

            lTimeout = TestStepMaster.__setTimeout(command["Timeout"])

            # Replace variables from data file
            if len(lValue) > 0:
                lValue = self.replaceVariables(lValue)
            if len(lValue2) > 0:
                lValue2 = self.replaceVariables(lValue2)

            if not TestStepMaster.ifQualifyForExecution(self.globalRelease, lRelease):
                logger.debug(f"we skipped this line due to {lRelease} disqualifies according to {self.globalRelease} ")
                continue  # We ignored the steps as it doesn't qualify
            if lActivity == "GOTOURL":
                self.browserSession.goToUrl(lValue)
            elif lActivity == "SETTEXT":
                self.browserSession.findByAndSetText(xpath=xpath, css=css, id=id, value=lValue, timeout=lTimeout)
            elif lActivity == 'HANDLEIFRAME':
                self.browserSession.handleIframe(lLocator)
            elif lActivity == "CLICK":
                self.browserSession.findByAndClick(xpath=xpath, css=css, id=id, timeout=lTimeout)
            elif lActivity == "PAUSE":
                self.browserSession.sleep(sleepTimeinSeconds=lValue)
            elif lActivity == "IF":
                if self.ifActive:
                    raise BaseException("No nested IFs at this point, sorry...")
                self.ifActive = True
                # Originally we had only Comparisons. Now we also want to check for existance of Field
                if not lValue and lLocatorType and lLocator:
                    lValue = self.browserSession.findBy(xpath=xpath, css=css, id=id, optional=lOptional,
                                                        timeout=lTimeout)

                self.__doComparisons(lComparison=lComparison, value1=lValue, value2=lValue2)
            elif lActivity == "ENDIF":
                if not self.ifActive:
                    raise BaseException("ENDIF without IF")
                self.ifActive = False
                self.ifIsTrue = True
            elif lActivity == 'GOBACK':
                self.browserSession.goBack()
            elif lActivity == 'APIURL':
                self.apiSession.setBaseURL(lValue)
            elif lActivity == 'ENDPOINT':
                self.apiSession.setEndPoint(lValue)
            elif lActivity == 'POST':
                self.apiSession.postURL(content=lValue)
            elif lActivity == 'GET':
                self.apiSession.getURL()
            elif lActivity == 'HEADER':
                self.apiSession.setHeaders(setHeaderData=lValue)
            elif lActivity == 'SAVE':
                self.doSaveData(lValue, lValue2)
            elif lActivity == "ADDRESS_CREATE":
                # Create Address with option lValue and lValue2
                AddressCreate(lValue,lValue2)
                # Update testcaseDataDict with addressDict returned from
                AddressCreate.returnAddress()
                self.testcaseDataDict.update(AddressCreate.returnAddress())
            elif lActivity == 'ASSERT':
                value_found = self.browserSession.findByAndWaitForValue(xpath=xpath, css=css, id=id, optional=lOptional,
                                                        timeout=lTimeout)
                value_expected = lValue
                if value_expected != value_found:
                    raise baangtTestStepException(f"Expected Value: {value_expected}, Value found :{value_found} ")
            elif lActivity == 'IBAN':
                # Create Random IBAN. Value1 = Input-Parameter for IBAN-Function. Value2=Fieldname
                self.__getIBAN(lValue, lValue2)
            elif lActivity == 'PDFCOMPARE':
                lFiles = self.browserSession.findNewFiles()
                # fixme: Implement the API-Call here
            elif lActivity == 'CHECKLINKS':
                self.checkLinks()
            else:
                raise BaseException(f"Unknown command in TestStep {lActivity}")

    def __getIBAN(self, lValue, lValue2):
        from baangt.base.IBAN import IBAN
        if not lValue2:
            logger.critical("IBAN-Method called without destination field name in column 'Value 2'")
            return

        lIBAN = IBAN()
        self.testcaseDataDict[lValue2] = lIBAN.getRandomIBAN()
        pass

    def checkLinks(self):
        """
        Will check all links on the current webpage

        Result will be written into "CheckedLinks" in TestDataDict
        """
        if self.testcaseDataDict.get("CheckedLinks"):
            self.testcaseDataDict["CheckedLinks"] += self.browserSession.checkLinks()
        else:
            self.testcaseDataDict["CheckedLinks"] = self.browserSession.checkLinks()

    @staticmethod
    def _sanitizeXField(inField):
        """
        When "X" or "True" is sent, then use this
        @param inField:
        @return:
        """
        lXField = True

        if not inField:
            lXField = False

        if inField.upper() == 'FALSE':
            lXField = False

        return lXField

    @staticmethod
    def ifQualifyForExecution(version_global, version_line):
        """ This function will test version_global and version_line
            @return True or False
        """
        if not version_global.strip():
            # No value is defined in Release, return True
            return True
        if not version_line.strip():
            # we skipped this line
            return True

        # split the version line
        if not len(version_line.strip().split(" ")) == 2:
            logger.debug(f"Invalid release format {version_line} ")
            return True
        comp_operator, version = version_line.strip().split(" ")
        if comp_operator == "<":
            return parse_version(version_global) < parse_version(version)
        elif comp_operator == ">":
            return parse_version(version_global) > parse_version(version)
        elif comp_operator == ">=":
            return parse_version(version_global) >= parse_version(version)
        elif comp_operator == "<=":
            return parse_version(version_global) <= parse_version(version)
        elif comp_operator == "=" or comp_operator == "==":
            return parse_version(version_global) == parse_version(version)
        else:
            logger.debug(f"Global version {version_global}, line version {version_line} ")
            return False

    def doSaveData(self, toField, valueForField):
        self.testcaseDataDict[toField] = valueForField

    @staticmethod
    def __setLocator(lLocatorType, lLocator):
        """

        @param lLocatorType: XPATH, CSS, ID, etc.
        @param lLocator: Value of the locator
        @return:
        """
        xpath = None
        css = None
        lId = None

        if lLocatorType:
            if lLocatorType == 'XPATH':
                xpath = lLocator
            elif lLocatorType == 'CSS':
                css = lLocator
            elif lLocatorType == 'ID':
                lId = lLocator

        return xpath, css, lId

    @staticmethod
    def __setTimeout(lTimeout):
        if lTimeout:
            lTimeout = float(lTimeout)
        else:
            lTimeout = 20
        return lTimeout

    @staticmethod
    def anyting2Boolean(valueIn):
        if isinstance(valueIn, bool):
            return valueIn

        if isinstance(valueIn, int):
            return bool(valueIn)

        if isinstance(valueIn, str):
            if valueIn.lower() in ("yes", "true", "1", "ok"):
                return True
            else:
                return False

        raise TypeError(f"Anything2Boolean had a wrong value: {valueIn}. Don't know how to convert that to boolean")

    def __doComparisons(self, lComparison, value1, value2):
        if isinstance(value1, bool) or isinstance(value2, bool):
            value1 = TestStepMaster.anyting2Boolean(value1)
            value2 = TestStepMaster.anyting2Boolean(value2)

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
        """Method is overwritten in all children/subclasses"""
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
        """
        The syntax for variables is currently $(<column_name_from_data_file>). Multiple variables can be assigned
        in one cell, for instance perfectly fine: "http://$(BASEURL)/$(ENDPOINT)"

        @param expression: the current cell, either as fixed value, e.g. "Franzi" or with a varible $(DATE)
        @return: the replaced value, e.g. if expression was $(DATE) and the value in column "DATE" of data-file was
            "01.01.2020" then return will be "01.01.2020"
        """
        if "$(" not in expression:
            return expression

        while "$(" in expression:
            if expression[0:2] == "$(":
                left_part = ""
            else:
                left_part = expression.split("$(")[0]

            center = expression[len(left_part)+2:]
            center = center.split(")")[0]

            right_part = expression[len(left_part)+len(center)+3:]

            if "." not in center:
                # Replace the variable with the value from data structure
                center = self.testcaseDataDict.get(center)
            else:
                # This is a reference to a DICT with ".": for instance APIHandling.AnswerContent("<bla>")
                dictVariable = center.split(".")[0]
                dictValue = center.split(".")[1]

                if dictVariable == 'ANSWER_CONTENT':
                    center = self.apiSession.session[1].answerJSON.get(dictValue, "Empty")
                else:
                    raise BaseException(f"Missing code to replace value for: {center}")

            if not center:
                raise BaseException(f"Variable not found: {center}")

            expression = "".join([left_part, center, right_part])
        return expression
