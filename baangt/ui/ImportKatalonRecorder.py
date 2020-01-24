import PySimpleGUI as sg
import os
import xlsxwriter
from pathlib import Path
import pyperclip
import logging

logger = logging.getLogger("pyC")

class ImportKatalonRecorder:
    def __init__(self, directory):
        self.window = None
        self.directory = directory
        self.clipboardText = ""
        self.outputText = ""

        self.clipboardText = """open | https://www.orf.at/ | 
click | //main[@id='content']/div[2]/div/div[2]/a/div[2]/div | 
click | //input[@type='text'] | 
type | //input[@type='text'] | test151
click | //input[@type='password'] | 
type | //input[@type='password'] | test4711
click | xpath=(//button[@type='button'])[5] | 
click | //div[@id='main']/div[2]/div/div[2]/div/div[3]/div[2]/button/div[2]/i | 
click | //input[@type='text'] | 
type | //input[@type='text'] | franzi
type | xpath=(//input[@type='text'])[2] | franzi@fritzi.com
type | //input[@type='password'] | 1234567
type | xpath=(//input[@type='password'])[2] | 1234567
click | //div[@id='main']/div[2]/div/div[2]/div/div[5]/button/div[2] | 
click | //input[@type='password'] | 
type | //input[@type='password'] | 12345678
type | xpath=(//input[@type='password'])[2] | 12345678
click | //div[@id='main']/div[2]/div/div[2]/div/div[5]/button/div[2]/i | 
click | xpath=(//input[@type='password'])[2] | 
click | //input[@type='password'] | 
sendKeys | //input[@type='password'] | ${KEY_DOWN}
sendKeys | //input[@type='password'] | ${KEY_DOWN}
type | //input[@type='password'] | 12345678!!
click | xpath=(//input[@type='password'])[2] | 
type | xpath=(//input[@type='password'])[2] | 12345678!!
click | //div[@id='main']/div[2]/div/div[2]/div/div[5]/button/div[2] | 
"""
        self.outputFormatted = []
        self.startWindow()

    def startWindow(self):
        self.getLayout()
        sg.theme("TanBlue")

        self.window = sg.Window("Baangt interactive Starter", layout=self.getLayout())

        lWindow = self.window
        lWindow.finalize()

        while True:
            lEvent, lValues = lWindow.read()
            if lEvent == "Exit":
                break

            if lEvent == 'Save':
                self.fileNameExport = sg.popup_get_text("Name of new Testcase:")
                self.saveTestCase()

            if lEvent == "TextIn": # Textinput in TextIn
                self.__importTranslateAndUpdate(lWindow=lWindow)

            if lEvent == 'Import from Clipboard':
                self.clipboardText = pyperclip.paste()
                self.window["TextIn"].update(value=self.clipboardText)
                self.__importTranslateAndUpdate(lWindow=lWindow)

        lWindow.close()

    def __importTranslateAndUpdate(self, lWindow):
        self.importClipboard()
        lWindow['TextOut'].update(value=self.outputText)

    def saveTestCase(self):
        if not "XLSX" in self.fileNameExport.upper():
            self.fileNameExport = self.fileNameExport + ".xlsx"
        lExcel = xlsxwriter.Workbook(str(Path(self.directory).joinpath(self.fileNameExport)))
        lWorksheetDefinition = lExcel.add_worksheet("TestStepExecution")
        lWorksheetData = lExcel.add_worksheet("data")
        self.saveTestCaseHeader(worksheet=lWorksheetDefinition)
        self.saveTestCaseExecution(worksheet=lWorksheetDefinition)
        self.saveTestData(lWorksheetData)
        lExcel.close()

    def saveTestData(self, worksheet):
        # fixme: We should translate the values in Testcase with VariableNames and then write those to data.
        self.writeCell(worksheet,0,0, "Dummy")
        self.writeCell(worksheet,1,0, "Dummy")
        self.writeCell(worksheet,2,0, "Dummy")
        pass

    def saveTestCaseHeader(self, worksheet):
        self.writeCell(worksheet, 0, 0, "Activity")
        self.writeCell(worksheet, 0, 1, "LocatorType")
        self.writeCell(worksheet, 0, 2, "Locator")
        self.writeCell(worksheet, 0, 3, "Value")
        self.writeCell(worksheet, 0, 4, "Comparison")
        self.writeCell(worksheet, 0, 5, "Value2")
        self.writeCell(worksheet, 0, 6, "Timeout")
        self.writeCell(worksheet, 0, 7, "Optional")
        self.writeCell(worksheet, 0, 8, "Release")
        # fixme: Write comments in the header line

    def saveTestCaseExecution(self, worksheet):
        for row, line in enumerate(self.outputFormatted, start=1):
            for col, (key, value) in enumerate(line.items()):
                self.writeCell(worksheet, row, col, value)

    def writeCell(self, sheet, cellRow, cellCol, value, format=None):
        sheet.write(cellRow, cellCol, value)

    def getLayout(self):
        lLayout = []
        lLayout.append([sg.Multiline(default_text=self.clipboardText, size=(50,30), key='TextIn', change_submits=True),
                        sg.Multiline(default_text=self.outputText, size=(50,30), key='TextOut')])
        lLayout.append([sg.Text("Select Directory, Testrun and Global settings to use:")])
        lLayout.append([sg.Text("Directory", size=(15, 1)),
                        sg.In(key="-directory-", size=(30, 1), enable_events=True, default_text=self.directory),
                        sg.FolderBrowse(initial_folder=os.getcwd(), enable_events=True)])

        lLayout.append([sg.Button('Save'), sg.Button('Exit'), sg.Button("Import from Clipboard")])

        return lLayout

    def importClipboard(self):
        lineOut = []

        for line in self.clipboardText.split("\n"):
            if len(line.strip()) > 2:
                if not "|" in line:
                    continue

                lineOut.append(self.doTranslate(line))

        self.outputText = ""
        self.outputFormatted = lineOut
        for line in lineOut:
            if not line:
                continue
            lStr = ""
            for key, value in line.items():
                lStr = lStr + (f"{key}: {value}, ")
            lStr = lStr + "\n"
            self.outputText += lStr

    def doTranslate(self, lineIn):
        value = ""
        if "|" not in lineIn:
            return None
        lParts = lineIn.split("|")
        command = lParts[0].strip()
        locator = lParts[1].strip()
        if command=="type" or command == "sendKeys":
            value = lParts[2].strip()

        if command == 'click':
            return ImportKatalonRecorder.doTranslateClick(locator)
        elif command == 'type':
            return ImportKatalonRecorder.doTranslateType(locator, value)
        elif command == 'sendKeys':
            return ImportKatalonRecorder.doTranslateType(locator, value)
        elif command == 'open':
            return ImportKatalonRecorder.__fillDict("GOTOURL", "", locator)
        elif command == 'goBackAndWait' or command == 'goBack':
            return ImportKatalonRecorder.doTranslategoBackAndWait()
        else:
            logger.exception(f"Translation for command not implemented: {command}")
            return None

    @staticmethod
    def doTranslateType(locator, value):
        return ImportKatalonRecorder.__fillDict("SETTEXT", locator, value)

    @staticmethod
    def doTranslateClick(locator):
        return ImportKatalonRecorder.__fillDict("click", locator)

    @staticmethod
    def doTranslategoBackAndWait():
        return ImportKatalonRecorder.__fillDict("goBack", "")

    @staticmethod
    def __fillDict(activity, locator, value="", locatorType='xpath'):
        return {"Activity": activity,
                "LocatorType": locatorType,
                "Locator": ImportKatalonRecorder.doTranslateLocator(locator),
                "Value": str(value)
                }

    @staticmethod
    def doTranslateLocator(locator):
        if "xpath=" in locator:
            # he comes with xpath=(//button[@type='button'])[5]
            locator = locator.replace("xpath=", "")
        return locator

    def exportResult(self):
        pass
