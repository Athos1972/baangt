import baangt.base.GlobalConstants as GC
from baangt.base.Timing.Timing import Timing
from baangt.base.BrowserHandling.BrowserHandling import BrowserDriver
from baangt.base.ApiHandling import ApiHandling
import sys
from pkg_resources import parse_version
import logging
from baangt.TestSteps.Exceptions import baangtTestStepException
from baangt.TestSteps.AddressCreation import AddressCreate
from baangt.base.PDFCompare import PDFCompare, PDFCompareDetails
from baangt.base.Faker import Faker as baangtFaker
from baangt.base.Utils import utils
from baangt.base.RuntimeStatistics import Statistic

logger = logging.getLogger("pyC")


class TestStepMaster:
    def __init__(self, executeDirect=True, **kwargs):
        self.anchor = None
        self.anchorLocator = None
        self.anchorLocatorType = None
        self.testCaseStatus = None
        self.ifActive = False
        self.ifIsTrue = True
        self.elseIsTrue = False
        self.ifLis = [self.ifIsTrue]
        self.elseLis = [self.elseIsTrue]
        self.ifConditions = 0
        self.baangtFaker = None
        self.statistics = Statistic()
        self.kwargs = kwargs
        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.testcaseDataDict = kwargs.get(GC.KWARGS_DATA)
        self.timing: Timing = kwargs.get(GC.KWARGS_TIMING)
        self.timingName = self.timing.takeTime(self.__class__.__name__, forceNew=True)
        self.browserSession: BrowserDriver = kwargs.get(GC.KWARGS_BROWSER)
        self.apiSession: ApiHandling = kwargs.get(GC.KWARGS_API_SESSION)

        self.testStepNumber = kwargs.get(GC.STRUCTURE_TESTSTEP)  # Set in TestRunData by TestCaseMaster
        self.testRunUtil = self.testRunInstance.testRunUtils

        # Get the release from testrun-customizing if set: (will influence, whether or not elements will be executed)
        self.globalRelease = self.testRunInstance.globalSettings.get("Release", "")

        # check, if this TestStep has additional Parameters and if so, execute
        lSequence = self.testRunUtil.getSequenceByNumber(testRunName=self.testRunInstance.testRunName,
                                                         sequence=kwargs.get(GC.STRUCTURE_TESTCASESEQUENCE))
        self.testCase = self.testRunUtil.getTestCaseByNumber(lSequence, kwargs.get(GC.STRUCTURE_TESTCASE))
        self.testStep = self.testRunUtil.getTestStepByNumber(self.testCase, self.testStepNumber)

        if self.testStep and len(self.testStep) > 1:
            if not isinstance(self.testStep[1], str) and executeDirect:
                # This TestStepMaster-Instance should actually do something - activitites are described
                # in the TestExecutionSteps.
                # Otherwise there's only a classname in TestStep[0]
                self.executeDirect(self.testStep[1][GC.STRUCTURE_TESTSTEPEXECUTION])

                # Teardown makes only sense, when we actually executed something directly in here
                # Otherwise (if it was 1 or 2 Tab-stops more to the left) we'd take execution time without
                # having done anything
                self.teardown()

        self.statistics.update_teststep_sequence()

    def executeDirect(self, executionCommands):
        """
        Executes a sequence of Commands. Will be subclassed in other modules.
        :param executionCommands:
        :return:
        """
        for index, (key, command) in enumerate(executionCommands.items()):
            self.executeDirectSingle(index, command)
            # self.statistics.update_teststep()  --> Moved to BrowserHandling into the activities themselves,
            # so that we can also count for externally (subclassed) activitis

    def manageNestedCondition(self, condition="", ifis=False):
        if condition.upper() == "IF":
            self.ifConditions += 1
            self.ifLis.append(ifis)
            self.elseLis.append(False)
        elif condition.upper() == "ELSE":
            self.elseLis[-1] = True
        elif condition.upper() == "ENDIF":
            self.ifConditions -= 1
            if self.ifConditions < 0:
                raise BaseException("Numbers of ENDIF are greater than IF.")
            self.ifLis.pop()
            self.elseLis.pop()
        assert len(self.ifLis) == self.ifConditions + 1 and len(self.elseLis) == self.ifConditions + 1
        self.ifIsTrue = self.ifLis[-1]
        self.elseIsTrue = self.elseLis[-1]

    def executeDirectSingle(self, commandNumber, command):
        """
        This will execute a single instruction
        """

        # when we have an IF-condition and it's condition was not TRUE, then skip whatever comes here until we
        # reach Endif
        if not self.ifIsTrue and not self.elseIsTrue:
            if command["Activity"].upper() != "ELSE" and command["Activity"].upper() != "ENDIF":
                return
        lActivity = command["Activity"].upper()
        if lActivity == "COMMENT":
            return  # Comment's are ignored

        lLocatorType = command["LocatorType"].upper()
        lLocator = self.replaceVariables(command["Locator"])

        if lLocator and not lLocatorType:  # If locatorType is empty, default it to XPATH
            lLocatorType = 'XPATH'

        xpath, css, id = self.__setLocator(lLocatorType, lLocator)

        if self.anchor and xpath:
            if xpath[0:3] == '///':         # Xpath doesn't want to use Anchor
                xpath = xpath[1:]
                logger.debug(f"Anchor active, but escaped. Using pure xpath: {xpath}")
            else:
                logger.debug(f"Anchor active. combining {self.anchorLocator} with {xpath}")
                xpath = self.anchorLocator + xpath

        lValue = str(command["Value"])
        lValue2 = str(command["Value2"])
        lComparison = command["Comparison"]
        lOptional = utils.anything2Boolean(command["Optional"])

        # check release line
        lRelease = command["Release"]

        # Timeout defaults to 20 seconds, if not set otherwise.
        lTimeout = TestStepMaster.__setTimeout(command["Timeout"])

        lTimingString = f"TS {commandNumber} {lActivity.lower()}"
        self.timing.takeTime(lTimingString)
        logger.info(
            f"Executing TestStepDetail {commandNumber} with parameters: act={lActivity}, lType={lLocatorType}, loc={lLocator}, "
            f"Val1={lValue}, comp={lComparison}, Val2={lValue2}, Optional={lOptional}, timeout={lTimeout}")

        lValue, lValue2 = self.replaceAllVariables(lValue, lValue2)

        if not TestStepMaster.ifQualifyForExecution(self.globalRelease, lRelease):
            logger.debug(f"we skipped this line due to {lRelease} disqualifies according to {self.globalRelease} ")
            return
        if lActivity == "GOTOURL":
            self.browserSession.goToUrl(lValue)
        elif lActivity == "SETTEXT":
            self.browserSession.findByAndSetText(xpath=xpath, css=css, id=id, value=lValue, timeout=lTimeout)
        elif lActivity == "SETTEXTIF":
            self.browserSession.findByAndSetTextIf(xpath=xpath, css=css, id=id, value=lValue, timeout=lTimeout,
                                                   optional=lOptional)
        elif lActivity == "FORCETEXT":
            self.browserSession.findByAndForceText(xpath=xpath, css=css, id=id, value=lValue, timeout=lTimeout)
        elif lActivity == "SETANCHOR":
            if not lLocator:
                self.anchor = None
                self.anchorLocator = None
                self.anchorLocatorType = None
            else:
                found = self.browserSession.findBy(xpath=xpath, css=css, id=id, timeout=lTimeout)
                if found:
                    self.anchor = self.browserSession.element
                    self.anchorLocator = lLocator
                    self.anchorLocatorType = lLocatorType
                    logger.debug(f"Anchor set: {lLocatorType} {lLocator}")
                else:
                    logger.error(f"Anchor should be set, but can't be found in the current page: {lLocatorType}, {lLocator}")
                    raise ValueError(f"Anchor should be set, but can't be found in the current page: {lLocatorType}, {lLocator}")
        elif lActivity == 'HANDLEIFRAME':
            self.browserSession.handleIframe(lLocator)
        elif lActivity == 'SWITCHWINDOW':
            lWindow = lValue
            if lWindow.isnumeric():
                lWindow = int(lWindow)
            self.browserSession.handleWindow(windowNumber=lWindow, timeout=lTimeout)
        elif lActivity == "CLICK":
            self.browserSession.findByAndClick(xpath=xpath, css=css, id=id, timeout=lTimeout)
        elif lActivity == "CLICKIF":
            self.browserSession.findByAndClickIf(xpath=xpath, css=css, id=id, timeout=lTimeout, value=lValue)
        elif lActivity == "PAUSE":
            self.browserSession.sleep(seconds=float(lValue))
        elif lActivity == "IF":
            # Originally we had only Comparisons. Now we also want to check for existance of Field
            if not lValue and lLocatorType and lLocator:
                lValue = self.browserSession.findBy(xpath=xpath, css=css, id=id, optional=lOptional,
                                                    timeout=lTimeout)

            self.__doComparisons(lComparison=lComparison, value1=lValue, value2=lValue2)
            logger.debug(f"IF-condition {lValue} {lComparison} {lValue2} evaluated to: {self.ifIsTrue} ")
        elif lActivity == "ELSE":
            if not self.ifIsTrue:
                self.manageNestedCondition(condition=lActivity)
                logger.debug("Executing ELSE-condition")
        elif lActivity == "ENDIF":
            self.ifIsTrue = True
            self.elseIsTrue = False
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
            self.doSaveData(lValue, lValue2, lLocatorType, lLocator)
        elif lActivity == 'CLEAR':
            # Clear a variable:
            if self.testcaseDataDict.get(lValue):
                del self.testcaseDataDict[lValue]
        elif lActivity == 'SAVETO':
            # In this case, we need to parse the real field, not the representation of the replaced field value
            self.doSaveData(command['Value'], lValue2, lLocatorType, lLocator)
        elif lActivity == 'SUBMIT':
            self.browserSession.submit()
        elif lActivity == "ADDRESS_CREATE":
            # Create Address with option lValue and lValue2
            AddressCreate(lValue, lValue2)
            # Update testcaseDataDict with addressDict returned from
            AddressCreate.returnAddress()
            self.testcaseDataDict.update(AddressCreate.returnAddress())
        elif lActivity == 'ASSERT':
            value_found = self.browserSession.findByAndWaitForValue(xpath=xpath, css=css, id=id, optional=lOptional,
                                                                    timeout=lTimeout)
            if not self.__doComparisons(lComparison=lComparison, value1=value_found, value2=lValue):
                raise baangtTestStepException(f"Expected Value: {lValue}, Value found :{value_found} ")
        elif lActivity == 'IBAN':
            # Create Random IBAN. Value1 = Input-Parameter for IBAN-Function. Value2=Fieldname
            self.__getIBAN(lValue, lValue2)
        elif lActivity == 'PDFCOMPARE':
            self.doPDFComparison(lValue)
        elif lActivity == 'CHECKLINKS':
            self.checkLinks()
        elif lActivity == 'ALERTIF':
            self.browserSession.confirmAlertIfAny()
        elif lActivity == GC.TESTCASESTATUS_STOP.upper():
            self.testcaseDataDict[GC.TESTCASESTATUS_STOP] = "X"              # will stop the test case
        elif lActivity == GC.TESTCASESTATUS_STOPERROR.upper():
            self.testcaseDataDict[GC.TESTCASESTATUS_STOPERROR] = "X"         # will stop the test case and set error
        else:
            raise BaseException(f"Unknown command in TestStep {lActivity}")

        self.timing.takeTime(lTimingString)

    def doPDFComparison(self, lValue, lFieldnameForResults="DOC_Compare"):
        lFiles = self.browserSession.findNewFiles()
        if len(lFiles) > 1:
            # fixme: Do something! There were more than 1 files since last check. Damn
            logger.critical(f"There were {len(lFiles)} files new since last check. Can't handle that. ")
            raise Exception
        elif len(lFiles) == 1:
            # Wonderful. Let's do the PDF-Comparison
            lPDFDataClass = PDFCompareDetails()
            lPDFDataClass.fileName = lFiles[0][0]
            lPDFDataClass.referenceID = lValue
            lDict = {"": lPDFDataClass}
            lPDFCompare = PDFCompare()
            lDict = lPDFCompare.compare_multiple(lDict)
            self.testcaseDataDict[lFieldnameForResults + "_Status"] = lDict[""].Status
            self.testcaseDataDict[lFieldnameForResults + "_Results"] = lDict[""].StatusText

    def replaceAllVariables(self, lValue, lValue2):
        # Replace variables from data file
        if len(lValue) > 0:
            lValue = self.replaceVariables(lValue)
        if len(lValue2) > 0:
            lValue2 = self.replaceVariables(lValue2)
        return lValue, lValue2

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

        If theres a returncode >= 400 in the list, we'll mark the testcase as failed
        """
        if self.testcaseDataDict.get("CheckedLinks"):
            self.testcaseDataDict["Result_CheckedLinks"] += self.browserSession.checkLinks()
        else:
            self.testcaseDataDict["Result_CheckedLinks"] = self.browserSession.checkLinks()

        for entry in self.testcaseDataDict["Result_CheckedLinks"]:
            if entry[0] > 400:
                self.testcaseDataDict[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
                self.testcaseDataDict[GC.TESTCASEERRORLOG] = self.testcaseDataDict.get(GC.TESTCASEERRORLOG, "") \
                                                             + "URL-Checker error"
                break

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

    def doSaveData(self, toField, valueForField, lLocatorType, lLocator):
        """
        Save fields. Either from an existing DICT (usually in API-Mode) or from a Webelement (in Browser-Mode)

        :param toField:
        :param valueForField:
        :param lLocatorType:
        :param lLocator:
        :return: no return parameter. The implicit return is a value in a field.
        """
        if self.testCase[1][GC.KWARGS_TESTCASETYPE] == GC.KWARGS_BROWSER:
            xpath, css, id = TestStepMaster.__setLocator(lLocatorType, lLocator)
            self.testcaseDataDict[toField] = self.browserSession.findByAndWaitForValue(xpath=xpath, css=css, id=id)
            logger.debug(f"Saved {self.testcaseDataDict[toField]} to {toField}")
        elif self.testCase[1][GC.KWARGS_TESTCASETYPE] == GC.KWARGS_API_SESSION:
            self.testcaseDataDict[toField] = valueForField
        else:
            sys.exit("Testcase Type not supported")

    @staticmethod
    def __setLocator(lLocatorType, lLocator):
        return utils.setLocatorFromLocatorType(lLocatorType, lLocator)

    @staticmethod
    def __setTimeout(lTimeout):
        return 20 if not lTimeout else float(lTimeout)

    def __doComparisons(self, lComparison, value1, value2):
        if isinstance(value1, bool) or isinstance(value2, bool):
            value1 = utils.anything2Boolean(value1)
            value2 = utils.anything2Boolean(value2)

        if value2 == 'None':
            value2 = None

        if lComparison == "=":
            if value1 == value2:
                self.manageNestedCondition(condition="IF", ifis=True)
            else:
                self.manageNestedCondition(condition="IF", ifis=False)
        elif lComparison == "!=":
            self.ifIsTrue = False if value1 == value2 else True
        elif lComparison == ">":
            if value1 > value2:
                self.manageNestedCondition(condition="IF", ifis=True)
            else:
                self.manageNestedCondition(condition="IF", ifis=False)
        elif lComparison == "<":
            if value1 < value2:
                self.manageNestedCondition(condition="IF", ifis=True)
            else:
                self.manageNestedCondition(condition="IF", ifis=False)
        elif not lComparison:  # Check only, if Value1 has a value.
            val = True if value1 else False
            self.manageNestedCondition(condition="IF", ifis=val)
        else:
            raise BaseException(f"Comparison Operator not supported/unknown {lComparison}")

        return self.ifIsTrue

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

        There's a special syntax for the faker module: $(FAKER.<fakermethod>).

        Also a special syntax for API-Handling: $(APIHandling.<DictElementName>).

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

            center = expression[len(left_part) + 2:]
            center = center.split(")")[0]

            right_part = expression[len(left_part) + len(center) + 3:]

            if "." not in center:
                # Replace the variable with the value from data structure
                centerValue = self.testcaseDataDict.get(center)
            else:
                # This is a reference to a DICT with ".": for instance APIHandling.AnswerContent("<bla>")
                dictVariable = center.split(".")[0]
                dictValue = center.split(".")[1]

                if dictVariable == 'ANSWER_CONTENT':
                    centerValue = self.apiSession.session[1].answerJSON.get(dictValue, "Empty")
                elif dictVariable == 'FAKER':
                    # This is to call Faker Module with the Method, that is given after the .
                    centerValue = self.__getFakerData(dictValue)
                else:
                    raise BaseException(f"Missing code to replace value for: {center}")

            if not centerValue:
                if center in self.testcaseDataDict.keys():
                    # The variable exists, but has no value.
                    return None
                else:
                    raise BaseException(f"Variable not found: {center}, input parameter was: {expression}")

            expression = "".join([left_part, centerValue, right_part])
        return expression

    def __getFakerData(self, fakerMethod):
        if not self.baangtFaker:
            self.baangtFaker = baangtFaker()

        logger.debug(f"Calling faker with method: {fakerMethod}")

        return self.baangtFaker.fakerProxy(fakerMethod=fakerMethod)
