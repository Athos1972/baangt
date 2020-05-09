# import PySimpleGUI as sg
import os
import xlsxwriter
from pathlib import Path
import pyperclip
import logging
import re
from baangt.base.ExportResults.ExportResults import ExcelSheetHelperFunctions

# re for to extract 'text' from  //input[@type='text']
extract_var = r'.*\'(.*)\''

logger = logging.getLogger("pyC")


class ImportKatalonRecorder:
    def __init__(self, directory):
        self.window = None
        self.fileNameExport = None
        self.directory = directory
        self.clipboardText = ""
        self.outputText = ""
        self.outputData = {}

        self.clipboardText = """
        
Please
        
export the recording 
        
in 
        
Katalon Recorder (Firefox or Chrome)
        
and
        
click "Import Clipboard" button below.
   
        
Alternatively copy + paste manually
into this side of the window.
"""
        self.outputFormatted = []
    #    self.startWindow()

    # def startWindow(self):
    #     self.getLayout()
    #     sg.theme("TanBlue")
    #
    #     self.window = sg.Window("Baangt interactive Starter", layout=self.getLayout())
    #
    #     lWindow = self.window
    #     lWindow.finalize()
    #
    #     while True:
    #         lEvent, lValues = lWindow.read()
    #         if lEvent == "Exit":
    #             break
    #
    #         if lEvent == 'Save':
    #             self.fileNameExport = sg.popup_get_text("Name of new Testcase:")
    #             if self.fileNameExport:
    #                 self.saveTestCase()
    #                 break
    #
    #         if lEvent == "TextIn":  # Textinput in TextIn
    #             self.__importTranslateAndUpdate(lWindow=lWindow)
    #
    #         if lEvent == 'Import from Clipboard':
    #             self.clipboardText = pyperclip.paste()
    #             self.window["TextIn"].update(value=self.clipboardText)
    #             self.__importTranslateAndUpdate(lWindow=lWindow)
    #
    #     lWindow.close()

    def __importTranslateAndUpdate(self, lWindow):
        self.importClipboard()
        lWindow['TextOut'].update(value=self.outputText)

    def saveTestCase(self):
        if "XLSX" not in self.fileNameExport.upper():
            self.fileNameExport = self.fileNameExport + ".xlsx"
        lExcel = xlsxwriter.Workbook(str(Path(self.directory).joinpath(self.fileNameExport)))
        lWorksheetDefinition = lExcel.add_worksheet("TestStepExecution")
        lWorksheetData = lExcel.add_worksheet("data")
        self.saveTestCaseHeader(worksheet=lWorksheetDefinition)
        self.saveTestCaseExecution(worksheet=lWorksheetDefinition)
        self.saveTestData(lWorksheetData)
        lExcel.close()

    def saveTestData(self, worksheet):
        # fixed: Translated the values in Testcase with VariableNames and then write those to data.
        for index, data in enumerate(sorted(self.outputData.items())):
            # remove $( and ) from header
            header = re.search(r'.*\((.*)\)', data[0]).groups()[0]
            self.writeCell(worksheet, 0, index, header)
            self.writeCell(worksheet, 1, index, data[1])

        for i in range(len(self.outputData)):
            ExcelSheetHelperFunctions.set_column_autowidth(worksheet, i)

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
            if not line:
                continue
            for col, (key, value) in enumerate(line.items()):
                self.writeCell(worksheet, row, col, value)
        for i in range(len(self.outputFormatted)):
            ExcelSheetHelperFunctions.set_column_autowidth(worksheet, i)

    def writeCell(self, sheet, cellRow, cellCol, value, format=None):
        sheet.write(cellRow, cellCol, value)

    # def getLayout(self):
    #     lLayout = []
    #     lLayout.append([sg.Multiline(default_text=self.clipboardText, size=(50, 30), key='TextIn', change_submits=True),
    #                     sg.Multiline(default_text=self.outputText, size=(50, 30), key='TextOut')])
    #     lLayout.append([sg.Text("Select Directory, Testrun and Global settings to use:")])
    #     lLayout.append([sg.Text("Directory", size=(15, 1)),
    #                     sg.In(key="-directory-", size=(30, 1), enable_events=True, default_text=self.directory),
    #                     sg.FolderBrowse(initial_folder=os.getcwd(), enable_events=True)])
    #
    #     lLayout.append([sg.Button('Save'), sg.Button('Exit'), sg.Button("Import from Clipboard")])
    #
    #     return lLayout

    def importClipboard(self):
        lineOut = []

        for line in self.clipboardText.split("\n"):
            if len(line.strip()) > 2:
                if "|" not in line:
                    continue

                lineOut.append(self.doTranslate(line))
        # Further process into $('variable') and value format
        lineOut, self.outputData = ImportKatalonRecorder.splitVariable(lineOut)

        self.outputText = ""
        self.outputFormatted = lineOut
        for line in lineOut:
            if not line:
                continue
            lStr = ""
            for key, value in line.items():
                lStr = lStr + f"{key}: {value}, "
            lStr = lStr + "\n"
            self.outputText += lStr

    def doTranslate(self, lineIn):
        value = ""
        if "|" not in lineIn:
            return None
        lParts = lineIn.split("|")
        command = lParts[0].strip().lower()
        locator = lParts[1].strip()
        if command == "type" or command == "sendKeys":
            value = lParts[2].strip()

        if command == 'click':
            return ImportKatalonRecorder.doTranslateClick(locator)
        elif command == 'type':
            return ImportKatalonRecorder.doTranslateType(locator, value)
        elif command == 'sendkeys':
            return ImportKatalonRecorder.doTranslateType(locator, value)
        elif command == 'open':
            return ImportKatalonRecorder.__fillDict("GOTOURL", "", locator)
        elif command == 'gobackandwait' or command == 'goback':
            return ImportKatalonRecorder.doTranslategoBackAndWait()
        elif command == 'select':
            return ImportKatalonRecorder.doTranslateSelect(locator)
        elif command == 'submit':
            return ImportKatalonRecorder.doTranslateSubmit(locator)
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
    def doTranslateSelect(locator):
        return ImportKatalonRecorder.__fillDict("select", locator)

    @staticmethod
    def doTranslateSubmit(locator):
        return ImportKatalonRecorder.__fillDict("submit", locator)

    @staticmethod
    def __fillDict(activity, locator, value="", locatorType='xpath'):
        if activity == 'select':
            activity = 'click'
            return {"Activity": activity,
                    "LocatorType": locatorType,
                    "Locator": ImportKatalonRecorder.doTranslateLocator(locator, "select"),
                    "Value": str(value)}

        return {"Activity": activity,
                "LocatorType": locatorType,
                "Locator": ImportKatalonRecorder.doTranslateLocator(locator),
                "Value": str(value)
                }

    @staticmethod
    def doTranslateLocator(locator, specialInstructions=None):

        if "xpath=" in locator:
            # he comes with xpath=(//button[@type='button'])[5]
            locator = locator.replace("xpath=", "")
        if locator[0:3].upper() == "ID=":
            # This is an ID. Translate the ID to proper xpath-Syntax
            if specialInstructions == "select":
                preLocator = "//select[@id='"
            else:
                preLocator = "//*[@id='"
            postLocator = "']"
            locator = locator[3:]
            locator = preLocator + locator + postLocator
        if locator[0:5].upper() == 'LINK=':
            # //a[text()='text_i_want_to_find']/@href --> Didn't work. Return Text and Selenium can't handle that
            # //a[contains(., 'Button')]
            preLocator = "//a[contains(., '"
            postLocator = "')]"
            locator = locator[5:]
            locator = preLocator + locator + postLocator
        return locator

    @staticmethod
    def splitVariable(lines):
        # make outputData empty if already there
        """ This function will process each line and format the
            'Value' column in format $(variabe).

        @output: list(lines), list(outputData)
        """

        outputData = {}
        # loop through line and process if 'Value' column there
        for line in lines:
            # Check for GOTOURL activity
            # skip if lines == NONE
            if not line:
                continue
            if line['Activity'] == "GOTOURL":
                # we should make variable for url
                line['Value'] = ImportKatalonRecorder.prepareKeyValue(outputData, 'url', line['Value'])

            elif line['Value'].strip():
                # we will make it variable
                result = re.search(extract_var, line['Locator'])
                if result:
                    # create variable format like $(value)
                    result = result.groups()[0]

                    line['Value'] = ImportKatalonRecorder.prepareKeyValue(outputData, result, line['Value'])
        return lines, outputData

    @staticmethod
    def prepareKeyValue(outputData, key, value):
        """ This function will append key and value in 
            outputData
            if variable key exist, it will rename by
                    key1, key2, ...
        """
        for i in range(1, 100):
            var = "$(" + key + str(i) + ")"
            if not outputData.get(var, None):
                outputData[var] = value
                return var
            else:
                continue

    def exportResult(self):
        pass
