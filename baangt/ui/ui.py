import PySimpleGUI as sg
import glob
import os
import subprocess
import configparser
import baangt.base.GlobalConstants as GC
from baangt.base.utils import utils
import logging
import json

logger = logging.getLogger("pyC")


class UI:
    """
    Provides a simple UI for Testrun-Execution
    """
    def __init__(self):
        # Todo 1: Save last used directory to local config File
        # Todo 2: Use the parameters from Globals and provide an option to change them
        self.configFile = None
        self.configFiles = []
        self.testRunFile = None
        self.testRunFiles = []
        self.configContents = {}
        self.window = None

        self.directory = None
        self.readConfig()
        self.getConfigFilesInDirectory()

        self.startWindow()

    def getLayout(self):
        lLayout = [[sg.Text("Select Directory, Testrun and Global settings to use:")],
                   [sg.Text("Directory", size=(15,1)),
                    sg.In(key="-directory-", size=(30,1), enable_events=True, default_text=self.directory),
                    sg.FolderBrowse(initial_folder=os.getcwd(), enable_events=True)],
                   [sg.Text("TestRun", size=(15,1)),
                    sg.InputCombo(self.testRunFiles, key="testRunFile", default_value=self.testRunFile, size=(30,1))],
                   [sg.Text("Global Settings", size=(15,1)),
                    sg.InputCombo(self.configFiles, key="configFile", default_value=self.configFile, enable_events=True, size=(30,1))]]

        if self.configContents:
            lLayout.append([sg.Text("-"*10 + f"Settings of file {self.configFile}" + "-"*10)])
            for key, value in self.configContents.items():
                lLayout.append([sg.In(key, key="-attrib-" + key, size=(25,1)), sg.In(key="-val-"+key, size=(30,1), default_text=value)])
            for i in range(0,4):
                lLayout.append([sg.In(key=f"-newField-{i}", size=(25,1)), sg.In(key=f"-newValue-{i}", size=(30,1))])
            lLayout.append([sg.Button('Save'), sg.Button("SaveAs"), sg.Button('Exit'), sg.Button("Execute TestRun")])
        else:
            lLayout.append([sg.Button('Exit')])

        return lLayout

    def startWindow(self):
        sg.theme("TanBlue")

        self.window = sg.Window("Baangt interactive Starter", layout=self.getLayout())
        lWindow = self.window
        lWindow.finalize()

        while True:
            lEvent, lValues = lWindow.read()
            if lEvent == "Exit":
                break
            if lValues.get('-directory-') != self.directory:
                self.directory = lValues.get("-directory-")
                self.getConfigFilesInDirectory()
                lWindow['configFile'].update(values=self.configFiles, value="")
                lWindow['testRunFile'].update(values=self.testRunFiles, value="")
                lValues['configFile'] = ""

            if lValues["testRunFile"]:
                self.testRunFile = lValues["testRunFile"]

            if lValues["configFile"]:
                if lValues["configFile"] != self.configFile:
                    self.configFile = lValues['configFile']
                    self.readContentsOfGlobals()
                    lWindow = self.reopenWindow(lWindow)

            if lEvent == 'Save':
                lWindow = self.saveConfigFileProcedure(lWindow, lValues)

            if lEvent == 'SaveAs':
                self.configFile = sg.popup_get_text("New Name of Configfile:")
                if len(self.configFile) > 0:
                    lWindow = self.saveConfigFileProcedure(lWindow, lValues)

            if lEvent == "Execute TestRun":
                self.runTestRun()


        self.saveInteractiveGuiConfig()

    def saveConfigFileProcedure(self, lWindow, lValues):
        # receive updated fields and values to store in JSON-File
        self.modifyValuesOfConfigFileInMemory(lValues)
        self.saveContentsOfConfigFile()
        lWindow = self.reopenWindow(lWindow)
        return lWindow

    def reopenWindow(self, lWindow):
        lWindow.close()
        self.window = sg.Window("Baangt interactive Starter", layout=self.getLayout())
        lWindow = self.window
        lWindow.finalize()
        return lWindow

    def runTestRun(self):
        if not self.configFile:
            sg.popup_cancel("No Config File selected - can't run")
            return
        if not self.testRunFile:
            sg.popup_cancel("No Testrun File selected - can't run")
            return
        runCmd = self._getRunCommand()
        logger.info(f"Running command: {runCmd}")
        p = subprocess.run(runCmd, shell=True)
        sg.popup_ok("Testrun finished")

    def _getRunCommand(self):
        return f"python baangt.py --run='{self.directory}/{self.testRunFile}' " \
                 f"--globals='{self.directory}/{self.configFile}'"

    def getConfigFilesInDirectory(self):
        """Reads *.JSON-Files from directory given in self.directory and builds 2 lists (Testrunfiles and ConfiFiles"""
        self.configFiles = []
        self.testRunFiles = []
        lcwd = os.getcwd()
        os.chdir(self.directory)
        fileList = glob.glob("*.json")
        fileList.extend(glob.glob("*.xlsx"))
        for file in fileList:
            if file[0:4].lower() == 'glob':
                self.configFiles.append(file)
            else:
                self.testRunFiles.append(file)
            pass

        self.configFiles = sorted(self.configFiles)
        self.testRunFiles = sorted(self.testRunFiles)

        os.chdir(lcwd)

    def readContentsOfGlobals(self):
        self.configContents = utils.openJson(self.directory + "/" + self.configFile)

    def saveContentsOfConfigFile(self):

        x = sg.popup_ok_cancel(f"Would write this content: {self.configContents} \n to file: {self.configFile} in path {self.directory}")
        print(x)

        if x == 'OK':
            with open(self.directory + "/" + self.configFile, 'w') as outfile:
                json.dump(self.configContents, outfile, indent=4)
            sg.popup_ok(f"Wrote file {self.directory}/{self.configFile}")

    def modifyValuesOfConfigFileInMemory(self, lValues):
        for key, value in lValues.items():
            if '-attrib-' in key:
                # Existing field - update value from value
                lSearchKey = key.replace("-attrib-","")
                if lSearchKey != value:
                    # an existing variable was changed to a new name. Delete the old one:
                    self.configContents.pop(lSearchKey)
                    lSearchKey = value
                    lSearchVal = lValues['-val-'+key.replace("-attrib-","")]
                else:
                    lSearchVal = lValues['-val-'+lSearchKey]
                if len(lSearchKey) > 0:
                    self.configContents[lSearchKey] = lSearchVal
            elif '-newField-' in key:
                # New field needs to be added to memory:
                lSearchKey = value # the new fieldname
                if len(lSearchKey) > 0:
                    lSearchVal = lValues['-newValue-'+key[-1]]
                    self.configContents[lSearchKey] = lSearchVal
            elif '-val-' in key or '-newValue-':
                pass # Values have been used already above
            else:
                logger.critical(f"Program error. Received something with key {key}, value {value} and no "
                                f"idea what to do with it")

    def saveInteractiveGuiConfig(self):
        config = configparser.ConfigParser()
        config["DEFAULT"] = {"path": self.directory}
        with open("baangt.ini", "w") as configFile:
            config.write(configFile)

    def readConfig(self):
        config = configparser.ConfigParser()
        try:
            config.read("baangt.ini")
            self.directory = config["DEFAULT"]['path']
        except Exception as e:
            self.directory = os.getcwd()
            pass





