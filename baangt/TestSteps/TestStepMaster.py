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
import random
import itertools

logger = logging.getLogger("pyC")


class TestStepMaster:
    def __init__(self, executeDirect=True, **kwargs):
        self.anchor = None
        self.anchorLocator = None
        self.anchorLocatorType = None
        self.testCaseStatus = None
        self.ifIsTrue = True  # used to know if command is inside if condition and run command as per it
        self.elseIsTrue = False  # used to know if command is inside else condition
        self.ifLis = [self.ifIsTrue]  # useful in storing state of nested if conditions
        self.elseLis = [self.elseIsTrue]  # useful in storing state of nested else conditions
        self.ifConditions = 0  # use to verify endif
        self.repeatIsTrue = False  # use to know if commands are running inside repeat loop
        self.repeatCommands = []  # used to store steps command of repeat data
        self.repeatReplaceDataDictionary = []  # used to store RLP_ data to be looped in repeat
        self.repeatCount = []  # Used to store count of randomdata in loop
        self.repeatActive = 0  # to sync active repeat counts with repeat done and will be execute when both are equal
        self.repeatDone = 0
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

        try:
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
        except Exception as e:
            logger.warning(f"Uncought exception {e}")
            utils.traceback(exception_in=e)

        self.statistics.update_teststep_sequence()

    def executeDirect(self, executionCommands):
        """
        Executes a sequence of Commands. Will be subclassed in other modules.
        :param executionCommands:
        :return:
        """
        for index, (key, command) in enumerate(executionCommands.items()):
            try:
                self.executeDirectSingle(index, command)
            except Exception as ex:
                # 2020-07-16: This Exception is cought, printed and then nothing. That's not good. The test run
                # continues forever, despite this exception. Correct way would be to set test case to error and stop
                # this test case
                # Before we change something here we should check, why the calling function raises an error.
                logger.critical(ex)
                self.testcaseDataDict[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
                return

    def manageNestedCondition(self, condition="", ifis=False):
        """
        Manages if and else condition. Specially made to deal with nested conditions
        :param condition:
        :param ifis:
        :return:
        """
        if condition.upper() == "IF" or condition.upper() == "IF_":
            self.ifConditions += 1
            self.ifLis.append(ifis)
            self.elseLis.append(False)
        elif condition.upper() == "ELSE" or condition.upper() == "ELSE_":
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

    def manageNestedLoops(self, command, commandNumber):
        """
        This method is used to deal with Repeat statements and nested repeat statements.
        It is called on when a repeat statement comes then this method will take and store all the commands come after
        it until it reaches repeat-done statement of same level i.e. when a repeat statement is present inside this
        repeat statement then the first repeat-done came will be considered as repeat-done of the nested repeat and the
        next one will be considered as the main.
        :param command:
        :param commandNumber:
        :return:
        """
        if command["Activity"].upper() == "REPEAT":  # To sync active repeat with repeat done
            self.repeatCommands[-1][commandNumber] = command  # storing nested repeat command
            self.repeatActive += 1  # used to know the level of repeat and repeat done
            return
        if command["Activity"].upper() != "REPEAT-DONE":  # store command in repeatDict
            self.repeatCommands[-1][commandNumber] = command
            return
        else:
            self.repeatDone += 1  # to sync repeat done with active repeat
            if self.repeatDone < self.repeatActive:  # if all repeat-done are not synced with repeat, store the data
                self.repeatCommands[-1][commandNumber] = command
                logger.info(command)
                return
            self.repeatIsTrue = False
            if self.repeatReplaceDataDictionary[-1]:
                data_list = []
                if type(self.repeatReplaceDataDictionary[-1]) is list:
                    for data_dic in self.repeatReplaceDataDictionary[-1]:
                        keys, values = zip(*data_dic.items())
                        final_values = []
                        for value in values:  # coverting none list values to list. Useful in make all possible data using itertools
                            if type(value) is not list:
                                final_values.append([value])
                            else:
                                final_values.append(value)
                        data_l = [dict(zip(keys, v)) for v in
                                  itertools.product(*final_values)]  # itertools to make all possible combinations
                        data_list.extend(data_l)
                else:
                    data_list = [self.repeatReplaceDataDictionary[-1]]
                if len(self.repeatCount) > 0 and self.repeatCount[-1]:  # get random data from list of data
                    try:
                        data_list = random.sample(data_list, int(self.repeatCount[-1]))
                    except:
                        pass
                for data in data_list:
                    temp_dic = dict(self.repeatCommands[-1])
                    processed_data = {}
                    for key in temp_dic:
                        try:
                            processed_data = dict(temp_dic[key])
                        except Exception as ex:
                            logger.debug(ex)
                        try:
                            self.executeDirectSingle(key, processed_data, replaceFromDict=data)
                        except Exception as ex:
                            logger.info(ex)
            del self.repeatCommands[-1]
            del self.repeatReplaceDataDictionary[-1]
            del self.repeatCount[-1]
            self.repeatDone = 0
            self.repeatActive = 0
            return

    def executeDirectSingle(self, commandNumber, command, replaceFromDict=None):
        """
        This will execute a single instruction
        """

        # when we have an IF-condition and it's condition was not TRUE, then skip whatever comes here until we
        # reach Endif
        if not self.ifIsTrue and not self.elseIsTrue:
            if command["Activity"].upper() == "IF":
                self.manageNestedCondition(condition=command["Activity"].upper(), ifis=self.ifIsTrue)
                return True
            if command["Activity"].upper() != "ELSE" and command["Activity"].upper() != "ENDIF":
                return True
        if self.repeatIsTrue:  # If repeat statement is active then execute this
            self.manageNestedLoops(command, commandNumber)
            return

        css, id, lActivity, lLocator, lLocatorType, xpath = self._extractAllSingleValues(command)

        if lActivity == "COMMENT":
            return  # Comment's are ignored

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
        lTimeout = TestStepMaster._setTimeout(command["Timeout"])

        lTimingString = f"TS {commandNumber} {lActivity.lower()}"
        self.timing.takeTime(lTimingString)
        logger.info(
            f"Executing TestStepDetail {commandNumber} with parameters: act={lActivity}, lType={lLocatorType}, loc={lLocator}, "
            f"Val1={lValue}, comp={lComparison}, Val2={lValue2}, Optional={lOptional}, timeout={lTimeout}")
        original_value = lValue # used as key to make rlp json dict and will be used further to make sheet name
        lValue, lValue2 = self.replaceAllVariables(lValue, lValue2, replaceFromDict=replaceFromDict)

        if not TestStepMaster.ifQualifyForExecution(self.globalRelease, lRelease):
            logger.debug(f"we skipped this line due to {lRelease} disqualifies according to {self.globalRelease} ")
            return
        
        if lActivity[0:3] == "ZZ_":
            # custom command. Do nothing and return
            return
        elif lActivity.lower() == "if":
            lActivity = "if_"
        elif lActivity.lower() == "else":
            lActivity = "else_"
        elif lActivity.lower() == "assert":
            lActivity = "assert_"
        try:
            kwargs = locals()
            del kwargs["self"]
            getattr(self, lActivity.lower())(**kwargs)
        except AttributeError:
            raise BaseException(f"Unknown command in TestStep {lActivity}")
        self.timing.takeTime(lTimingString)

    def gotourl(self, **kwargs):
        if kwargs["lValue"]:
            self.browserSession.goToUrl(kwargs["lValue"])
        elif kwargs["lLocator"]:
            self.browserSession.goToUrl(kwargs["lLocator"])
        else:
            logger.critical("GotoURL without URL called. Aborting. "
                            "Please provide URL either in Value or Locator columns")


    def settext(self, **kwargs):
            self.browserSession.findByAndSetText(xpath=kwargs["xpath"], css=kwargs["css"], id=kwargs["id"], value=kwargs["lValue"],
                                                 timeout=kwargs["lTimeout"], optional=kwargs["lOptional"])

    def settextif(self, **kwargs):
            self.browserSession.findByAndSetTextIf(xpath=kwargs["xpath"], css=kwargs["css"], id=kwargs["id"], value=kwargs["lValue"],
                                                   timeout=kwargs["lTimeout"], optional=kwargs["lOptional"])

    def forcetext(self, **kwargs):
            self.browserSession.findByAndForceText(xpath=kwargs["xpath"], css=kwargs["css"], id=kwargs["id"], value=kwargs["lValue"],
                                                   timeout=kwargs["lTimeout"], optional=kwargs["lOptional"])

    def forcetextif(self, **kwargs):
            if kwargs["lValue"]:
                self.browserSession.findByAndForceText(xpath=kwargs["xpath"], css=kwargs["css"], id=kwargs["id"], value=kwargs["lValue"],
                                                       timeout=kwargs["lTimeout"], optional=kwargs["lOptional"])

    def forcetextjs(self, **kwargs):
            if kwargs["lValue"]:
                self.browserSession.findByAndForceViaJS(xpath=kwargs["xpath"], css=kwargs["css"], id=kwargs["id"], value=kwargs["lValue"],
                                                        timeout=kwargs["lTimeout"], optional=kwargs["lOptional"])

    def setanchor(self, **kwargs):
            if not kwargs["lLocator"]:
                self.anchor = None
                self.anchorLocator = None
                self.anchorLocatorType = None
            else:
                found = self.browserSession.findBy(xpath=kwargs["xpath"], css=kwargs["css"], id=kwargs["id"], timeout=kwargs["lTimeout"])
                if found:
                    self.anchor = self.browserSession.element
                    self.anchorLocator = kwargs["lLocator"]
                    self.anchorLocatorType = kwargs["lLocatorType"]
                    logger.debug(f'Anchor set: {kwargs["lLocatorType"]} {kwargs["lLocator"]}')
                else:
                    logger.error(f'Anchor should be set, but can\'t be found in the current page: {kwargs["lLocatorType"]}, {kwargs["lLocator"]}')
                    raise ValueError(f'Anchor should be set, but can\'t be found in the current page: {kwargs["lLocatorType"]}, {kwargs["lLocator"]}')

    def handleiframe(self, **kwargs):
            self.browserSession.handleIframe(kwargs["lLocator"])

    def switchwindow(self, **kwargs):
            lWindow = kwargs["lValue"]
            if lWindow.isnumeric():
                lWindow = int(lWindow)
            self.browserSession.handleWindow(windowNumber=lWindow, timeout=kwargs["lTimeout"])

    def click(self, **kwargs):
            self.browserSession.findByAndClick(xpath=kwargs["xpath"], css=kwargs["css"], id=kwargs["id"], 
                                               timeout=kwargs["lTimeout"], optional=kwargs["lOptional"])

    def clickif(self, **kwargs):
            self.browserSession.findByAndClickIf(xpath=kwargs["xpath"], css=kwargs["css"], id=kwargs["id"], 
                                    timeout=kwargs["lTimeout"], value=kwargs["lValue"], optional=kwargs["lOptional"])

    def pause(self, **kwargs):
            self.browserSession.sleep(seconds=float(kwargs["lValue"]))

    def if_(self, **kwargs):
            # Originally we had only Comparisons. Now we also want to check for existance of Field
            if not kwargs["lValue"] and kwargs["lLocatorType"] and kwargs["lLocator"]:
                kwargs["lValue"] = self.browserSession.findBy(xpath=kwargs["xpath"], css=kwargs["css"], id=kwargs["id"], optional=kwargs["lOptional"],
                                                    timeout=kwargs["lTimeout"])

            self.__doComparisons(kwargs["lComparison"], value1=kwargs["lValue"], value2=kwargs["lValue"])
            logger.debug(f'IF-condition original Value: {kwargs["original_value"]} (transformed: {kwargs["lValue"]}) '
                         f'{kwargs["lComparison"]} {kwargs["lValue"]} evaluated to: {self.ifIsTrue} ')

    def else_(self, **kwargs):
            if not self.ifIsTrue:  # don't run else statement if "if" statement is true
                self.manageNestedCondition(condition=kwargs["lActivity"])
                logger.debug("Executing ELSE-condition")
            else:
                self.ifIsTrue = False

    def endif(self, **kwargs):
            self.manageNestedCondition(condition=kwargs["lActivity"])

    def repeat(self, **kwargs):
            self.repeatActive += 1
            self.repeatIsTrue = True
            self.repeatCommands.append({})
            if kwargs["original_value"] not in self.testRunInstance.json_dict:
                self.testRunInstance.json_dict[kwargs["original_value"]] = []
            self.testRunInstance.json_dict[kwargs["original_value"]].append(kwargs["lValue"])
            self.repeatReplaceDataDictionary.append(kwargs["lValue"])
            self.repeatCount.append(kwargs["lValue"])

    def goback(self, **kwargs):
            self.browserSession.goBack()

    def apiurl(self, **kwargs):
            self.apiSession.setBaseURL(kwargs["lValue"])

    def endpoint(self, **kwargs):
            self.apiSession.setEndPoint(kwargs["lValue"])

    def post(self, **kwargs):
            self.apiSession.postURL(content=kwargs["lValue"])

    def get(self, **kwargs):
            self.apiSession.getURL()

    def header(self, **kwargs):
            self.apiSession.setHeaders(setHeaderData=kwargs["lValue"])

    def save(self, **kwargs):
            self.doSaveData(kwargs["lValue"], kwargs["lValue"], kwargs["lLocatorType"], kwargs["lLocator"])

    def clear(self, **kwargs):
            # Clear a variable:
            if self.testcaseDataDict.get(kwargs["lValue"]):
                del self.testcaseDataDict[kwargs["lValue"]]

    def saveto(self, **kwargs):
            # In this case, we need to parse the real field, not the representation of the replaced field value
            self.doSaveData(kwargs["command"]['Value'], kwargs["lValue"], kwargs["lLocatorType"], kwargs["lLocator"])

    def submit(self, **kwargs):
            self.browserSession.submit()

    def address_create(self, **kwargs):
            # Create Address with option kwargs["lValue"] and kwargs["lValue"]
            AddressCreate(kwargs["lValue"], kwargs["lValue"])
            # Update testcaseDataDict with addressDict returned from
            AddressCreate.returnAddress()
            self.testcaseDataDict.update(AddressCreate.returnAddress())

    def assert_(self, **kwargs):
            value_found = self.browserSession.findByAndWaitForValue(xpath=kwargs["xpath"], css=kwargs["css"], id=kwargs["id"],
                                                            optional=kwargs["lOptional"], timeout=kwargs["lTimeout"])
            if not self.__doComparisons(kwargs["lComparison"], value1=value_found, value2=kwargs["lValue"]):
                logger.error(f'Condition {value_found} {kwargs["lComparison"]} {kwargs["lValue"]} was not met during assert.')
                raise baangtTestStepException(f'Expected Value: {kwargs["lValue"]}, Value found :{value_found} ')

    def iban(self, **kwargs):
            # Create Random IBAN. Value1 = Input-Parameter for IBAN-Function. Value2=Fieldname
            self.__getIBAN(kwargs["lValue"], kwargs["lValue2"])

    def pdfcompare(self, **kwargs):
            self.doPDFComparison(kwargs["lValue"])

    def checklinks(self, **kwargs):
            self.checkLinks()

    def alertif(self, **kwargs):
            self.browserSession.confirmAlertIfAny()

    def tcstoptestcase(self, **kwargs):
            self.testcaseDataDict[GC.TESTCASESTATUS_STOP] = "X"              # will stop the test case

    def tcstoptestcaseerror(self, **kwargs):
            self.testcaseDataDict[GC.TESTCASESTATUS_STOPERROR] = "X"         # will stop the test case and set error


    def _extractAllSingleValues(self, command):
        lActivity = command["Activity"].upper()
        lLocatorType = command["LocatorType"].upper()
        try:
            lLocator = self.replaceVariables(command["Locator"])
        except Exception as ex:
            logger.info(ex)
        if lLocator and not lLocatorType:  # If locatorType is empty, default it to XPATH
            lLocatorType = 'XPATH'
        xpath, css, id = self.__setLocator(lLocatorType, lLocator)
        return css, id, lActivity, lLocator, lLocatorType, xpath

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

    def replaceAllVariables(self, lValue, lValue2, replaceFromDict=None):
        # Replace variables from data file
        try:
            if len(lValue) > 0:
                lValue = self.replaceVariables(lValue, replaceFromDict=replaceFromDict)
            if len(lValue2) > 0:
                lValue2 = self.replaceVariables(lValue2, replaceFromDict=replaceFromDict)
        except Exception as ex:
            logger.warning(f"During replacement of variables an error happened: {ex}")
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
    def _setTimeout(lTimeout):
        return 20 if not lTimeout else float(lTimeout)

    def __doComparisons(self, lComparison, value1, value2):
        if isinstance(value1, bool) or isinstance(value2, bool):
            value1 = utils.anything2Boolean(value1)
            value2 = utils.anything2Boolean(value2)

        if value2 == 'None':
            value2 = None

        logger.debug(f"Evaluating IF-Condition: Value1 = {value1}, comparison={lComparison}, value2={value2}")

        if lComparison == "=":
            if value1 == value2:
                self.manageNestedCondition(condition="IF", ifis=True)
            else:
                self.manageNestedCondition(condition="IF", ifis=False)
        elif lComparison == "!=":
            if value1 != value2:
                self.manageNestedCondition(condition="IF", ifis=True)
            else:
                self.manageNestedCondition(condition="IF", ifis=False)
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
        elif lComparison == ">=":
            if value1 >= value2:
                self.manageNestedCondition(condition="IF", ifis=True)
            else:
                self.manageNestedCondition(condition="IF", ifis=False)
        elif lComparison == "<=":
            if value1 <= value2:
                self.manageNestedCondition(condition="IF", ifis=True)
            else:
                self.manageNestedCondition(condition="IF", ifis=False)
        elif lComparison.upper() == "IP":     # Is Part of (Value 1 is part of Value 2)
            if value1 in value2:
                self.manageNestedCondition(condition="IF", ifis=True)
            else:
                self.manageNestedCondition(condition="IF", ifis=False)
        elif lComparison.upper() == 'CO':      # COntains (Value 1 contains Value 2)
            if value2 in value1:
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

    def replaceVariables(self, expression, replaceFromDict=None):
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
            centerValue = ""

            if replaceFromDict:  # json is supplied with repeat tag, that json is used here to get main data
                    dic = replaceFromDict
                    for key in center.split('.')[-1:]:
                        dic = self.iterate_json(dic, key)
                    centerValue = dic

            if centerValue: # if we got value from the passed json then bypass this if else conditions
                pass
            elif "." not in center:
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
                    centerValue = self._getFakerData(dictValue)
                elif self.testcaseDataDict.get(dictVariable):
                    dic = self.testcaseDataDict.get(dictVariable)
                    for key in center.split('.')[1:]:
                        dic = self.iterate_json(dic, key)
                    centerValue = dic
                else:
                    raise BaseException(f"Missing code to replace value for: {center}")

            if not centerValue:
                if center in self.testcaseDataDict.keys():
                    # The variable exists, but has no value.
                    centerValue = ""
                else:
                    raise BaseException(f"Variable not found: {center}, input parameter was: {expression}")
            if not isinstance(centerValue, list) and not isinstance(centerValue, dict):
                expression = "".join([left_part, str(centerValue), right_part])
            else:
                expression = centerValue
        return expression

    def iterate_json(self, data, key):
        # itereate through list of json and create list of data from dictionary inside those list
        if type(data) is list:
            lis = []
            for dt in data:
                dt = self.iterate_json(dt, key)
                lis.append(dt)
            return lis
        elif type(data) is dict:
            return data.get(key)


    def _getFakerData(self, fakerMethod):
        if not self.baangtFaker:
            self.baangtFaker = baangtFaker()

        logger.debug(f"Calling faker with method: {fakerMethod}")

        return self.baangtFaker.fakerProxy(fakerMethod=fakerMethod)
