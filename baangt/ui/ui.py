import PySimpleGUI as sg
import glob
import os
import sys
import platform
import subprocess
import configparser
import baangt.base.GlobalConstants as GC
from baangt.base.utils import utils
from baangt.ui.ImportKatalonRecorder import ImportKatalonRecorder
import logging
import json
from pathlib import Path

logger = logging.getLogger("pyC")


class UI:
    """
    Provides a simple UI for Testrun-Execution
    """
    def __init__(self):
        self.configFile = None
        self.tempConfigFile = None
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
        lLayout= [[sg.Text("Select Directory, Testrun and Global settings to use:")]]
        lLayout.append([sg.Text("Directory", size=(15,1)),
                    sg.In(key="-directory-", size=(31,1), enable_events=True, default_text=self.directory),
                    sg.FolderBrowse(initial_folder=os.getcwd(), enable_events=True)])
        lLayout.append([sg.Text("TestRun", size=(15,1)),
                    sg.InputCombo(self.testRunFiles, key="testRunFile", default_value=self.testRunFile, size=(29,1))])
        lLayout.append([sg.Text("Global Settings", size=(15,1)),
                    sg.InputCombo(self.configFiles, key="configFile", default_value=self.configFile, enable_events=True, size=(29,1))])

        if self.configContents:
            lLayout.append([sg.Text("-"*10 + f"Settings of file {self.configFile}" + "-"*10)])
            for key, value in self.configContents.items():
                lLayout.append([sg.In(key, key="-attrib-" + key, size=(25,1)), sg.In(key="-val-"+key, size=(30,1), default_text=value)])
            for i in range(0,4):
                lLayout.append([sg.In(key=f"-newField-{i}", size=(25,1)), sg.In(key=f"-newValue-{i}", size=(30,1))])
            lLayout.append([sg.Button('Save'), sg.Button("SaveAs"), sg.Button('Exit'), sg.Button("Execute TestRun")])
        else:
            lLayout.append([sg.Button('Exit')])

        lLayout.append([sg.Button("Import Katalon", disabled=True), sg.Button("Import KatalonRecorder")])

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
                self.modifyValuesOfConfigFileInMemory(lValues=lValues)
                self.runTestRun()

            if lEvent == "Import KatalonRecorder":
                ImportKatalonRecorder(self.directory)
                self.getConfigFilesInDirectory()   # Refresh display

        self.saveInteractiveGuiConfig()
        lWindow.close()

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
        # Remove temporary Configfile, that was created only for this run:
        try:
            os.remove(Path(self.directory).joinpath(self.tempConfigFile))
        except Exception as e:
            logger.warning(f"Tried to remove temporary file but seems to be not there: "
                           f"{self.directory}/{self.tempConfigFile}")

    def _getRunCommand(self):
        """
        If bundled (e.g. in pyinstaller), then the executable is already sys.executable,
        otherwise we need to concatenate executable and Script-Name before we can start
        a subprocess.

        @return: Full path and filename to call Subprocess
        """
        lStart = sys.executable
        if "python" in sys.executable.lower():
            if len(Path(sys.argv[0]).parents) > 1:
                # This is a system where the path the the script is given in sys.argv[0]
                lStart = lStart + f" {sys.argv[0]}"
            else:
                # this is a system where we need to join os.getcwd() and sys.argv[0] because the path is not given in sys.argv[0]
                lStart = lStart + f" {Path(os.getcwd()).joinpath(sys.argv[0])}"

        self.__makeTempConfigFile()

        return f"{lStart} " \
               f"--run='{Path(self.directory).joinpath(self.testRunFile)}' " \
               f"--globals='{Path(self.directory).joinpath(self.tempConfigFile)}'"

    def __makeTempConfigFile(self):
        """
        Add parameters to the Config-File for this Testrun and save the file under a temporary name
        """
        self.configContents[GC.PATH_ROOT] = self.directory
        self.configContents[GC.PATH_SCREENSHOTS] = str(Path(self.directory).joinpath("Screenshots"))
        self.configContents[GC.PATH_EXPORT] = str(Path(self.directory).joinpath("1testoutput"))
        self.configContents[GC.PATH_IMPORT] = str(Path(self.directory).joinpath("0testdateninput"))
        self.tempConfigFile = UI.__makeRandomFileName()
        self.saveContentsOfConfigFile(self.tempConfigFile)

    @staticmethod
    def __makeRandomFileName():
        return "globals_" + utils.datetime_return() + ".json"

    def _getPythonExecutable(self):
        if hasattr(sys, '_MEIPASS'):
            # We're in an executable created by pyinstaller
            return sys.executable

        if platform.system().lower() == 'linux' or platform.system().lower() == 'darwin':
            lPython = 'python3'
        elif platform.system().lower() == 'windows':
            lPython = 'python'
        else:
            sys.exit(f"Unknown platform to run on: {platform.system().lower()}")
        return lPython

    def getConfigFilesInDirectory(self):
        """Reads *.JSON-Files from directory given in self.directory and builds 2 lists (Testrunfiles and ConfiFiles"""
        self.configFiles = []
        self.testRunFiles = []
        lcwd = os.getcwd()
        os.chdir(self.directory)
        fileList = glob.glob("*.json")
        fileList.extend(glob.glob("*.xlsx"))
        if not platform.system().lower() == 'windows':
            # On MAC and LINUX there may be also upper/lower-Case versions
            fileList.extend(glob.glob("*.JSON"))
            fileList.extend(glob.glob("*.XLSX"))
        for file in fileList:
            if file[0:4].lower() == 'glob':      # Global Settings for Testrun must start with global_*
                self.configFiles.append(file)
            else:
                self.testRunFiles.append(file)
            pass

        self.configFiles = sorted(self.configFiles)
        self.testRunFiles = sorted(self.testRunFiles)

        os.chdir(lcwd)

    def readContentsOfGlobals(self):
        self.configContents = utils.openJson(Path(self.directory).joinpath(self.configFile))
        # Prepare some default values, if not filled:
        if not self.configContents.get("TC." + GC.DATABASE_LINES):
            self.configContents["TC." + GC.DATABASE_LINES] = ""

    def saveContentsOfConfigFile(self, lFileName = None):
        if not lFileName:
            lFileName = self.configFile

        with open(str(Path(self.directory).joinpath(lFileName)), 'w') as outfile:
            json.dump(self.configContents, outfile, indent=4)

    def modifyValuesOfConfigFileInMemory(self, lValues):
        for key, value in lValues.items():
            if '-attrib-' in key:
                # Existing field - update value from value
                lSearchKey = key.replace("-attrib-","")
                if lSearchKey != value:
                    # an existing variable was changed to a new name. Delete the old one:
                    self.configContents.pop(lSearchKey)
                    lSearchKey = value
                    lSearchVal = lValues['-val-'+key.replace("-attrib-", "")]
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
        config["DEFAULT"] = {"path": self.directory,
                             "testrun": UI.__nonEmptyString(self.testRunFile),
                             "globals": UI.__nonEmptyString(self.configFile)}
        with open("baangt.ini", "w") as configFile:
            config.write(configFile)

    @staticmethod
    def __nonEmptyString(stringIn):
        if stringIn:
            return stringIn
        else:
            return ""

    def readConfig(self):
        config = configparser.ConfigParser()
        try:
            config.read("baangt.ini")
            self.directory = config["DEFAULT"]['path']
            self.testRunFile = config["DEFAULT"]['testrun']
            self.configFile = config["DEFAULT"]['globals']
            self.readContentsOfGlobals()
        except Exception as e:
            self.directory = os.getcwd()
            pass





