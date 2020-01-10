import os
import uuid
import xlsxwriter
import glob
import logging
import sys
from bs4 import BeautifulSoup as bs4
from pathlib import Path

def setupLogger():
    import logging
    import os
    from datetime import datetime

    logPath = "/".join(os.path.dirname(os.path.realpath(__file__)).split('/')[0:-1]) + "/logs/"
    Path(logPath).mkdir(parents=True, exist_ok=True)
    logFilename = (logPath +
                   datetime.now().strftime("%Y%m%d_%H%M%S") + '.log')
    print(f"Logfile verwendet: {logFilename}")

    # Bit more advanced logging:
    logger = logging.getLogger('pyC')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fileHandler = logging.FileHandler(logFilename, encoding="UTF-8")
    fileHandler.setLevel(level=logging.DEBUG)
    # create console handler with a higher log level
    channelHandler = logging.StreamHandler()
    channelHandler.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s _ %(levelname)s _ %(module)s _ %(funcName)s : %(message)s')
    channelHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(channelHandler)
    logger.addHandler(fileHandler)
    return logger

def readXMLFile(fileNameAndPath):
    with open(fileNameAndPath, "r") as file:
        content=file.readlines()
        content = "".join(content)
        fileAsDOM = bs4(content, "lxml")
    return fileAsDOM

def readFile(fileNameAndPath):
    with open(fileNameAndPath, "r") as file:
        content=file.readlines()
    return content

class LocatorObjects:
    def __init__(self):
        self.objects = {}

    def add(self, objectDefinition, path):
        self.objects[path] = objectDefinition

    def exportXLS(self, wsheet: xlsxwriter.Workbook.worksheet_class):
        wsheet.write(0,0, "Location")
        wsheet.write(0,1, "SelectorType")
        wsheet.write(0,2, "SelectorValue")
        wsheet.write(0,3, "IFrame")
        for line, (lObjectKey, lObjectValue) in enumerate(self.objects.items()):
            wsheet.write(line+1, 0, lObjectValue.fileNameAndPathKatalonInternal)
            wsheet.write(line+1, 1, lObjectValue.selector)
            wsheet.write(line+1, 2, lObjectValue.selectorValue)
            wsheet.write(line+1, 3, lObjectValue.iframe)

class Groovy:
    def __init__(self):
        self.groovyScriptClasses = {}

    def add(self, groovyScript, path):
        self.groovyScriptClasses[path] = groovyScript

    def doReplacementOfLiterals(self, objects: LocatorObjects):
        for key, value in self.groovyScriptClasses.items():
            value.replaceLiteralsWithLocators(objects)


class TestCases:
    def __init__(self):
        self.testcases = {}

    def add(self, testCase, path):
        self.testcases[path] = testCase

    @staticmethod
    def decodeHex(string):
        myUuid = uuid.UUID(string)
        return myUuid.fields

class fileHandling:
    def __init__(self, fileNameAndPath, format='XML'):
        self.fileNameAndPath = fileNameAndPath
        if format == 'XML':
            self.fileAsDOM: bs4 = readXMLFile(fileNameAndPath)
        else:
            self.fileAsDOM = readFile(fileNameAndPath)

        self.name = None
        self.fileNameAndPathKatalonInternal = fileHandling._makeShorterPath(self.fileNameAndPath)

    def logFileContentsHeader(self):
        logger.info(f"Processing file: {self.fileNameAndPath}")

    @staticmethod
    def _makeShorterPath(longPath):
        shortPath = fileHandling.__cutBefore(longPath, "Object Repository/")
        shortPath = fileHandling.__cutBefore(shortPath, "Test Cases/")
        shortPath = fileHandling.__cutBefore(shortPath, "Scripts/")
        return shortPath

    @staticmethod
    def __cutBefore(path, cutBeforeValue):
        if cutBeforeValue in path:
            return cutBeforeValue + "".join(path.split(cutBeforeValue)[1:])
        return path

class translateTestCase(fileHandling):
    def __init__(self, fileNameAndPath):
        super().__init__(fileNameAndPath)
        self.scripts = {}
        self.outputAnalysis()

    def outputAnalysis(self):
        lAttrib = self.fileAsDOM.find("testcaseguid").get_text(strip=True)
        hexDecode = TestCases.decodeHex(lAttrib)
        super().logFileContentsHeader()
        logger.info(f"TestCaseGuid: {lAttrib}, UUID-Decoded: {hexDecode}")
        self.findGroovyScript()

    def findGroovyScript(self):
        # There should be a groovy script with a random number in a directory
        # /Scripts/<path_to_Testcase>/<testCase>/<random>.groovy
        # Current fileNameAndPath: '/Users/bernhardbuhl/git/KatalonVIG/Test Cases/000 Login/Open_VN_Auskunft.tc'
        splitList = self.fileNameAndPath.split("/Test Cases/")
        basePath = splitList[0]
        restPath = "".join(splitList[1:])
        testCaseFileName = "".join(restPath.split("/")[-1:])
        restPath = restPath.replace(testCaseFileName, "")
        testCaseFileName = testCaseFileName.replace(".tc", "")
        searchScriptPath = basePath + "/Scripts/" + restPath + testCaseFileName + "/"
        os.chdir(searchScriptPath)
        l_files = glob.glob("*.groovy")
        for file in l_files:
            self.scripts[file] = translateGoovy(searchScriptPath + file)
            self.scripts[file].savePythonFile(self.fileNameAndPath)

class translateGoovy(fileHandling):
    def __init__(self, fileNameAndPath):
        super().__init__(fileNameAndPath, format="groovy")
        self.interpretGroovy()
        # self.savePythonFile() will be executed from caller

    def interpretGroovy(self):
        lOutput = ""
        for groovyLine in self.fileAsDOM:
            groovyLine = translateGoovy.replaceGroovyLine(groovyLine)
            if len(groovyLine) > 0:
                lOutput += groovyLine
        self.fileAsDOM = lOutput
        self.replaceLiteralsWithLocators("Dummy")

    def replaceLiteralsWithLocators(self, locatorObjectClasses: LocatorObjects):
        """Replace the internal Katalon-Links with actual definitions"""
        # The internal Locator is '<ObjectFolder>/<subfolder./.n>/<name>
        # The filename is '/Object Repository/<ObjectFolder>/<subfolder./.n>/<name>.rs
        basePath = self.fileNameAndPath.split("/Scripts/")[0]
        lOutput = ""
        lInput = self.fileAsDOM.split("\n")
        for line in lInput:
            # fixme: Here's an error - removes variable names
            if "fragen" in self.fileAsDOM:
                x = 2
            if "(xpath='" in line:
                lFileAndPathLocator = line.split("xpath='")[1]
                lFileAndPathLocator = lFileAndPathLocator.split("'")[0]
                lFileAndPathLocator = basePath + "/Object Repository/" + lFileAndPathLocator + ".rs"
                # Sometimes Katalon Studio prefixes with Object Repository and sometimes it doesn't.
                lFileAndPathLocator = lFileAndPathLocator.replace("/Object Repository/Object Repository/", "/Object Repository/")
                lLocatorObject = translateObjectDefinition(lFileAndPathLocator)

                lStart = line.split("xpath='")[0]
                lEnd = line.split("xpath='")[1:]
                lEnd = "'".join(lEnd[0].split("'")[1:])

                if lLocatorObject.selectorValue:
                    lLocatorObject.selectorValue = lLocatorObject.selectorValue.replace("'", '"')
                    line = lStart + lLocatorObject.selector.lower() + "='" + lLocatorObject.selectorValue + "'" + lEnd
                else:
                    logger.warning(f"Couldn't find locator definition for Object {lLocatorObject.fileNameAndPathKatalonInternal}")
                    line = "# FIXME: " + lStart + lLocatorObject.fileNameAndPathKatalonInternal + lEnd

            lOutput = lOutput + "\n" + line
        self.fileAsDOM = lOutput

    def savePythonFile(self, saveAsClassName = None):
        if saveAsClassName:
            lFileExport = saveAsClassName
            lFileExport = lFileExport.replace(".tc", ".py")
            self._createHeaderForClass(saveAsClassName)
        else:
            lFileExport = self.fileNameAndPath.replace(".groovy", ".py")
        lFileExport = self._replacePathForExport(lFileExport)
        lPathExport = "/".join(lFileExport.split("/")[0:-1])
        Path(lPathExport).mkdir(parents=True, exist_ok=True)
        with open(lFileExport, "w") as file:
            file.writelines(self.fileAsDOM)

    @staticmethod
    def _replacePathForExport(fullPathAndFileName):
        lFileExport = fullPathAndFileName.replace("/Test Cases/", "/Python/Test Cases/")
        lFileExport = lFileExport.replace("/Scripts/", "/Python/Scripts/")
        if not "Python" in lFileExport:
            logger.critical(f"Should replace path, but can't. input: {fullPathAndFileName}. \nI better stop now.")
            sys.exit("Critical program error or so.")
        return lFileExport

    def _createHeaderForClass(self, classNameForHeader):
        header = """
import baangt.base.GlobalConstants as GC
from baangt.TestSteps.TestStepMaster import TestStepMaster


"""
        header = header + f"class {classNameForHeader.split('/')[-1].replace('.tc', '')}(TestStepMaster):"

        header = header + """
\tdef __init__(self, **kwargs):
\t\tsuper().__init__(**kwargs)
\t\tself.execute()

\tdef execute(self):"""

        self.addTabs()
        self.fileAsDOM = header + '\n' + self.fileAsDOM

    def addTabs(self):
        """
        Add Tab-Stop to each from Groovy converted Code-Line as this code runs under Method execute()
        """
        self.fileAsDOM = self.fileAsDOM.replace("\n\n", "\n")
        l_lines = self.fileAsDOM.split("\n")
        result = ""
        for line in l_lines:
            line = '\t\t' + line
            result = result + '\n' + line
        self.fileAsDOM = result

    @staticmethod
    def replaceGroovyLine(l_string):
        l_string = l_string.replace(") {", "")
        l_string = l_string.replace("WebUI.click(findTestObject(", "self.browserSession.findByAndClick(xpath=")
        l_string = l_string.replace("WebUI.verifyElementPresent(findTestObject(", "self.browserSession.findBy(xpath=")
        l_string = l_string.replace("WebUI.setText(findTestObject(", "self.browserSession.findByAndSetText(xpath=")
        l_string = l_string.replace("WebUI.waitForElementVisible(findTestObject(", "self.browserSession.findBy(xpath=")
        l_string = l_string.replace("WebUI.verifyElementNotPresent(findTestObject(",
                                    "self.browserSession.findWaitNotVisible(xpath=")
        l_string = l_string.replace("WebUI.waitForElementNotPresent(findTestObject(",
                                    "self.browserSession.findWaitNotVisible(xpath=")
        l_string = l_string.replace("WebUI.doubleClick(findTestObject(",
                                    "self.browserSession.findByAndClick(xpath=")
        l_string = l_string.replace("WebUI.waitForElementPresent(findTestObject(",
                                    "self.browserSession.findBy(xpath=")
        l_string = l_string.replace("if (", "if ")
        l_string = l_string.replace(" && ", " and ")
        l_string = l_string.replacE(" || ", " or ")
        l_string = l_string.replace("else", "else:")
        l_string = l_string.replace("{", "")
        l_string = l_string.replace("}", "")
        l_string = l_string.replace("))", ")")
        l_string = l_string.replace(".toString()","")
        l_string = l_string.replace(".trim()", ".strip()")

        if "WebUI.waitForElementClickable" in l_string:
            l_string = ""

        if "//" in l_string.strip()[0:2]:
            l_string = l_string.replace("//", "# ")

        if "'" in l_string.strip()[0:2]:
            l_string = "# " + l_string

        if "not_run" in l_string.strip()[0:7]:
            l_string = l_string.replace("not_run:", "# ")

        if "if " in l_string:
            l_string = l_string.strip() + ":\n"

        if "import " in l_string[0:10]:
            l_string = ""

        if "Thread.sleep" in l_string:
            sleep_time = l_string.split("(")[1]
            sleep_time = sleep_time.split(")")[0]
            # Sleep time in Milliseonds.
            sleep_time = float(sleep_time) / 1000
            l_string = l_string.split("Thread")[0] + "self.browserSession.sleep(" + str(sleep_time) + ")\n"

        if "WebUI.delay(" in l_string:
            sleep_time = l_string.split("(")[1]
            sleep_time = sleep_time.split(")")[0]
            # sleep time in Seconds
            l_string = l_string.split("WebUI")[0] + "self.browserSession.sleep(" + sleep_time + ")\n"

        if "scrollTo" in l_string:
            l_string = ""

        if "CustomKeyword" in l_string:
            l_string = ""

        if "self.testcaseDataDict" in l_string and "self.browserSession" in l_string and l_string[-1:] == ")":
            l_string = l_string[0:-1] + "'])"
            # schließende Klammer zu früh...
            l_line_split = l_string.split(")")
            l_string = l_line_split[0] + l_line_split[1] + ")"
            # value als named parameter übergeben
            l_string = l_string.replace("self.testcaseDataDict", "value=self.testcaseDataDict")

        l_string = translateGoovy._replaceGlobalVariable(l_string)
        l_string = translateGoovy._replaceOtherStuff(l_string)
        return l_string

    @staticmethod
    def _replaceOtherStuff(stringIn):
        if ".contains(" in stringIn:
            # Syntax: "<space><bla>.contains('blabla')<space>
            # fixme: not done yet. Implement...
            pass
        if "self.browserSession.findByAndSetText(" in stringIn:
            # in self.browserSession.findByAndSetText( after the xpath='value' there is a closing bracket before the value
            # That must got and self.testcasedataDict must be preceeded with "value="
            stringIn = stringIn.replace("self.testcaseDataDict", "value=self.testcaseDataDict")
            stringIn = stringIn.replace("'), value=", "', value=")

        if "self.browserSession.findWaitNotVisible" in stringIn:
            # there's a timeout-value, that needs to be a parameter "timeout="
            # formats:
            #    <bla>,<blank><timeout>)
            #    <bla>,<timeout>)

            lFirst = stringIn.split(",")
            lEnd = lFirst[-1]
            lEnd = ", timeout = " + lEnd
            stringIn = " ".join(lFirst[0:-1]) + lEnd
            stringIn = stringIn.replace("), timeout =", ", timeout =")

        stringIn = stringIn.replace("else: if", "elif")

        # Fix space vs. tab in the file beginning
        lengthDiffSpace = len(stringIn) - len(stringIn.lstrip(' '))
        if lengthDiffSpace > 0:
            if lengthDiffSpace >= 8:
                stringIn = '\t\t' + stringIn.lstrip(' ')
            elif lengthDiffSpace >= 4:
                stringIn = '\t' + stringIn.lstrip(' ')
        return stringIn


    @staticmethod
    def _replaceGlobalVariable(stringIn):
        """
        We have any of the following occurances:
        covered: <blank>GlobalVariable.variablename<blank>
        covered: (GlobalVariable.variablename)
        covered: (GlobalVariable.variablename<blank>
        covered: <blank>GlobalVariable.variablename<lineend>
        covered: <blank>GlobalVariable.variablename)
        covered: <blank>GlobalVariable.variablename.contains('<text>'):
        <blank>GlobalVariable.variablename.toLowerCase()<blank>
        covered: <linestart>GlobalVariable.variablename<blank>

        That was the old code:
        #l_string = l_string.replace("((GlobalVariable.", "self.testcaseDataDict['")
        #l_string = l_string.replace("GlobalVariable.", "self.testcaseDataDict['")
        #l_string = l_string.replace(" ==", "'] ==")
        #l_string = l_string.replace(" !=", "'] !=")
        """
        if not "GlobalVariable" in stringIn:
            return stringIn

        while "GlobalVariable" in stringIn:
            addCRLF = False
            replaceVariable = stringIn.split("GlobalVariable")[1]
            replaceVariable = replaceVariable.split(" ")[0]
            replaceVariable = replaceVariable.split(")")[0]
            replaceVariable = replaceVariable.split(".")[1]
            if "\n" in replaceVariable:
                replaceVariable = replaceVariable.split("\n")[0]
            destination = "self.testcaseDataDict['" + replaceVariable + "']"
            replaceVariable = "GlobalVariable." + replaceVariable
            stringIn = stringIn.replace(replaceVariable, destination)
            if addCRLF:
                stringIn = stringIn + "\n"

        if ".length()" in stringIn:
            stringIn = translateGoovy._replaceLengthMethodGroovy(stringIn)
        if ".toLowerCase()" in stringIn:
            stringIn = stringIn.replace("toLowerCase()", "lower()")
        return stringIn
        pass

    @staticmethod
    def _replaceLengthMethodGroovy(stringIn):
        """bla.length() in Groovy should become len(bla)"""
        # Find the variable, that we want to know the length of:
        stringIn = stringIn.strip()
        partsBeforeAndAfter = stringIn.split(".length()")
        variableParts = partsBeforeAndAfter[0].split(" ")
        variableParts[-1] = "len(" + variableParts[-1]
        partsBeforeAndAfter[0] = " ".join(variableParts) + ")"
        return "".join(partsBeforeAndAfter)

class translateObjectDefinition(fileHandling):
    def __init__(self, fileNameAndPath):
        super().__init__(fileNameAndPath)
        self.selector = None
        self.selectorValue = None
        self.iframe = None
        self.analyze()
        self.outputAnalysis()

    def outputAnalysis(self):
        super().logFileContentsHeader()
        logger.debug(f"Selektor: {self.selector}")
        logger.debug(f"Value: {self.selectorValue}")
        logger.debug(f"Iframe: {self.iframe}")

    def analyze(self):
        nameTag = self.fileAsDOM.find("name")
        self.name = nameTag.text
        self.selector = self.fileAsDOM.find("selectormethod").get_text(strip=True) # XPATH, CSS
        selectorDrillDown = self.fileAsDOM.findAll("selectorcollection")
        for node in selectorDrillDown:
            lEntries = node.findAll("entry")
            for entry in lEntries:
                if entry.find("key").get_text(strip=True) == self.selector:
                    self.selectorValue = entry.find("value").get_text(strip=True)

        # Find potential Iframe:
        iframeDrilldown = self.fileAsDOM.find("webelementproperties")
        if iframeDrilldown:
            if iframeDrilldown.find("name").get_text(strip=True) == "ref_element":
                self.iframe = iframeDrilldown.find("value").get_text(strip=True)


def doImport(importDir):
    excludeDirs = ["Check Points", "Test Suites", ".git", "Reports", "/bin", "/settings", "/Drivers", "/Plugins",
                   "/Data Files", "/0testdateninput", "/2shared", "/1testout", "/Keywords", "/report", "/Libs",
                   "/Checkpoints", "/Include", "/3tools", "/Scripts", "/Test Listen"]
    for (root, dirs, files) in os.walk(importDir, topdown=True):
        lContinue = True
        for excludeDir in excludeDirs:
            if excludeDir in root:
                lContinue = False
                break
        if not lContinue:
            continue
        logger.info(str(root) + str(dirs) + str(files))
        for file in files:
            fileAndPath = _getFileAndPath(file=file, path=root)
            #if file[-3:] == '.rs':
            #    lDefinition = translateObjectDefinition(fileAndPath)
            #    locatorObjects.add(lDefinition, fileAndPath)
            if file[-3:] == '.tc':
                lTestCase = translateTestCase(fileAndPath)
                testCases.add(lTestCase, fileAndPath)
            #if file[-7:] == '.groovy':
            #    lGroovy = translateGoovy(fileAndPath)
            #    groovy.add(lGroovy, fileAndPath)

def _getFileAndPath(file, path):
    return path + "/" + file

def exportResults():
    lXLS = xlsxwriter.Workbook("export.xlsx")
    lWSObjects = lXLS.add_worksheet("Locators")
    locatorObjects.exportXLS(lWSObjects)
    lXLS.close()


if __name__ == '__main__':
    logger = setupLogger()
    IMPORTDIR = '/Users/bernhardbuhl/git/KatalonVIG'
    locatorObjects = LocatorObjects()
    testCases = TestCases()
    groovy = Groovy()
    doImport(IMPORTDIR)
    groovy.doReplacementOfLiterals(objects=locatorObjects)
    exportResults()
    print("Python-Files created in Katalon-Basepath/Python")
    print("Excel Export of Locators in export.xlsx")