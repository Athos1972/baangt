# import PySimpleGUI as sg
import glob
import os
import sys
import platform
import subprocess
import configparser
import baangt.base.GlobalConstants as GC
from baangt.base.Utils import utils
from baangt.ui.ImportKatalonRecorder import ImportKatalonRecorder
import logging
import json
from pathlib import Path
from baangt.base.PathManagement import ManagedPaths

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
        self.toggleAdditionalFieldsVisible = False

        self.iconFileWindow = b"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"
        self.directory = None
        self.mainWindowPosition = (None, None)
        self.managedPaths = ManagedPaths()

        self.readConfig()

        if not self.directory:
            self.directory = self.managedPaths.derivePathForOSAndInstallationOption()#.getcwd()

        self.getConfigFilesInDirectory()

        self.startWindow()

    # def getLayout(self):
    #
    #     lMenu = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
    #              ['&Katalon Studio', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
    #              ['&Help', '&About...'], ]
    #     # lMenu doesnt' work. It shows up in the Mac-Menu, but none of the buttons work. Even the
    #     # Mac-Button stops working until the window is closed
    #
    #     lColumnLeft = [[sg.Text("")],
    #                    [sg.Text("Path", size=(10,1), font="Helvetica 10 bold"),
    #                     sg.In(key="-directory-", size=(31,1), enable_events=True, default_text=self.directory, font="Helvetica 12"),
    #                     sg.FolderBrowse(initial_folder=os.getcwd(), font="Helvetica 10", enable_events=True, size=(10,1))]]
    #
    #     lColumnLeft.append([sg.Text("TestRun", size=(10, 1), font="Helvetica 10 bold"),
    #                     sg.InputCombo(self.testRunFiles, key="testRunFile", default_value=self.testRunFile,
    #                                   size=(29, 1), font="Helvetica 12"),
    #                     sg.Button("Execute", size=(10, 1), font="Helvetica 10", button_color=('white', 'darkgreen'))])
    #
    #     lColumnLeft.append([sg.Text("Settings", size=(10, 1), font="Helvetica 10 bold"),
    #                         sg.InputCombo(self.configFiles, key="configFile", default_value=self.configFile,
    #                                       enable_events=True, size=(29, 1), font="Helvetica 12"),
    #                         sg.Button("Details", size=(10, 1), font="Helvetica 10", key="ToggleFields")])
    #
    #     # Baangt Logo
    #     lPathLogo = Path(__file__).parent.parent.parent.joinpath("ressources").joinpath("baangtLogo2020Small.png")
    #     # when in pip-Package, this doesn't work.
    #     if not lPathLogo.exists():
    #         lPathLogo = Path(__file__).parent.parent.joinpath("ressources").joinpath("baangtLogo2020Small.png")
    #
    #     lColumnRight = [[sg.Image(filename=lPathLogo)]]
    #
    #     lLayout = [[sg.Menu(lMenu)],
    #                [sg.Col(lColumnLeft, pad=(0,0)),
    #                 sg.Col(lColumnRight, pad=(0,0), justification="right")]]
    #
    #     # Show the button to provide more details
    #     ttip_Recorder = 'Will start the Katalon Recorder Importer'
    #
    #     if self.configContents:
    #         lLayout.append([sg.Text(f"SETTINGS IN {self.configFile}", font="Helvetica 8 bold",
    #                                 visible=self.toggleAdditionalFieldsVisible)])
    #         for key, value in self.configContents.items():
    #             lLayout.append([sg.In(key, key="-attrib-" + key, size=(28,1), visible=self.toggleAdditionalFieldsVisible),
    #                             sg.In(key="-val-"+key, size=(34,1), default_text=value, visible=self.toggleAdditionalFieldsVisible)])
    #         for i in range(0,4):
    #             lLayout.append([sg.In(key=f"-newField-{i}", size=(28,1), visible=self.toggleAdditionalFieldsVisible),
    #                             sg.In(key=f"-newValue-{i}", size=(34,1), visible=self.toggleAdditionalFieldsVisible)])
    #
    #         lLayout.append([sg.Button('Save', size=(13,1)),
    #                         sg.Button("SaveAs", size=(13,1)),
    #                         sg.Button("Import Recorder", size=(13,1), tooltip=ttip_Recorder),
    #                         sg.Button("Import Katalon", size=(13,1), disabled=True),])
    #         lLayout.append([sg.T()])
    #
    #     return lLayout
    #
    # def startWindow(self):
    #     sg.theme("LightBrown1")
    #
    #     self.window = sg.Window("baangt Interactive Starter", layout=self.getLayout(), location=self.mainWindowPosition,
    #                             icon=self.iconFileWindow)  # size=(750,400)
    #     lWindow = self.window
    #     lWindow.finalize()
    #
    #     while True:
    #         lEvent, lValues = lWindow.read(timeout=200)
    #         if lEvent == "Exit":
    #             break
    #
    #         if not lEvent:       # Window was closed by "X"-Button
    #             break
    #
    #         self.mainWindowPosition = lWindow.CurrentLocation()
    #
    #         if lValues.get('-directory-') != self.directory:
    #             self.directory = lValues.get("-directory-")
    #             self.getConfigFilesInDirectory()
    #
    #         if lValues["testRunFile"]:
    #             self.testRunFile = lValues["testRunFile"]
    #
    #         if lValues["configFile"]:
    #             if lValues["configFile"] != self.configFile:
    #                 self.configFile = lValues['configFile']
    #                 self.readContentsOfGlobals()
    #                 lWindow = self.reopenWindow(lWindow)
    #
    #         if lEvent == 'Save':
    #             lWindow = self.saveConfigFileProcedure(lWindow, lValues)
    #
    #         if lEvent == 'SaveAs':
    #             self.configFile = sg.popup_get_text("New Name of Configfile:")
    #             if len(self.configFile) > 0:
    #                 lWindow = self.saveConfigFileProcedure(lWindow, lValues)
    #
    #         if lEvent == "Execute":
    #             self.modifyValuesOfConfigFileInMemory(lValues=lValues)
    #             self.runTestRun()
    #
    #         if lEvent == "Import Recorder":
    #             lRecorder = ImportKatalonRecorder(self.directory)
    #             self.getConfigFilesInDirectory()   # Refresh display
    #             lWindow['testRunFile'].update(values=self.testRunFiles,
    #                                           value=lRecorder.fileNameExport)
    #
    #         if lEvent == 'ToggleFields':
    #             lWindow = self.toggleAdditionalFieldsExecute(lWindow=lWindow)
    #
    #     self.saveInteractiveGuiConfig()
    #     lWindow.close()

    def saveConfigFileProcedure(self, lWindow, lValues):
        # receive updated fields and values to store in JSON-File
        self.modifyValuesOfConfigFileInMemory(lValues)
        self.saveContentsOfConfigFile()
        lWindow = self.reopenWindow(lWindow)
        return lWindow

    # def reopenWindow(self, lWindow):
    #     lSize = lWindow.Size
    #     lPosition = lWindow.CurrentLocation()
    #     lWindow.close()
    #     self.window = sg.Window("baangt Interactive Starter", layout=self.getLayout(),
    #                             location=lPosition, icon=self.iconFileWindow)
    #     lWindow = self.window
    #     lWindow.finalize()
    #     return lWindow
    #
    # def toggleAdditionalFieldsExecute(self, lWindow):
    #     if self.toggleAdditionalFieldsVisible:
    #         self.toggleAdditionalFieldsVisible = False
    #     else:
    #         self.toggleAdditionalFieldsVisible = True
    #
    #     lWindow = self.reopenWindow(lWindow=lWindow)
    #     return lWindow
    #
    # def runTestRun(self):
    #     if not self.configFile:
    #         sg.popup_cancel("No Config File selected - can't run")
    #         return
    #     if not self.testRunFile:
    #         sg.popup_cancel("No Testrun File selected - can't run")
    #         return
    #     runCmd = self._getRunCommand()
    #     if self.configContents.get("TX.DEBUG"):
    #         from baangt.base.TestRun.TestRun import TestRun
    #
    #         lTestRun = TestRun(f"{Path(self.directory).joinpath(self.testRunFile)}",
    #                            globalSettingsFileNameAndPath=f'{Path(self.directory).joinpath(self.tempConfigFile)}')
    #
    #     else:
    #         logger.info(f"Running command: {runCmd}")
    #         p = subprocess.run(runCmd, shell=True, close_fds=True)
    #
    #
    #     sg.popup_ok("Testrun finished")
    #     # Remove temporary Configfile, that was created only for this run:
    #     try:
    #         os.remove(Path(self.directory).joinpath(self.tempConfigFile))
    #     except Exception as e:
    #         logger.warning(f"Tried to remove temporary file but seems to be not there: "
    #                        f"{self.directory}/{self.tempConfigFile}")

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

        # self.configContents[GC.PATH_SCREENSHOTS] = str(Path(self.directory).joinpath(GC.PATH_SCREENSHOTS))
        # self.configContents[GC.PATH_EXPORT] = str(Path(self.directory).joinpath(GC.PATH_EXPORT))
        # self.configContents[GC.PATH_IMPORT] = str(Path(self.directory).joinpath(GC.PATH_IMPORT))
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
        """
        Reads JSON-Files from directory given in self.directory and builds 2 lists (Testrunfiles and ConfiFiles)
        """
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

        lWindow = self.window
        if lWindow:
            lWindow['configFile'].update(values=self.configFiles, value=self.configFile if self.configFile else "")
            lWindow['testRunFile'].update(values=self.testRunFiles, value=self.testRunFile if self.testRunFile else "")

        os.chdir(lcwd)

    def readContentsOfGlobals(self):
        self.configContents = utils.openJson(Path(self.directory).joinpath(self.configFile))
        # Prepare some default values, if not filled:
        if not self.configContents.get("TC." + GC.DATABASE_LINES):
            self.configContents["TC." + GC.DATABASE_LINES] = ""
        if not self.configContents.get("TC." + GC.EXECUTION_DONTCLOSEBROWSER):
            self.configContents["TC." + GC.EXECUTION_DONTCLOSEBROWSER] = ""
        if not self.configContents.get("TC." + GC.EXECUTION_SLOW):
            self.configContents["TC." + GC.EXECUTION_SLOW] = ""

    def saveContentsOfConfigFile(self, lFileName = None):
        if not lFileName:
            lFileName = self.configFile

        with open(str(Path(self.directory).joinpath(lFileName)), 'w') as outfile:
            json.dump(self.configContents, outfile, indent=4)

    def modifyValuesOfConfigFileInMemory(self, lValues):
        for key, value in lValues.items():
            if not isinstance(key, str):
                continue

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
                             "globals": UI.__nonEmptyString(self.configFile),
                             "position": self.mainWindowPosition}
        with open(self.managedPaths.getOrSetIni().joinpath("baangt.ini"), "w") as configFile:
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
            config.read(self.managedPaths.getOrSetIni().joinpath("baangt.ini"))
            self.directory = config["DEFAULT"]['path']
            self.testRunFile = config["DEFAULT"]['testrun']
            self.configFile = config["DEFAULT"]['globals']
            self.mainWindowPosition = UI.__convert_configPosition2Tuple(config["DEFAULT"]['position'])
            # Value in there is now a string of "(x-coordinates, y-coordinates)". We need a tuple (int:x, int:y)

            self.readContentsOfGlobals()
        except Exception as e:
            # if baangt.ini is not there. Default the directory to /examples.
            if Path(os.getcwd()).joinpath("examples").exists():
                self.directory = Path(os.getcwd()).joinpath("examples")
                self.testRunFile = 'simpleAutomationpractice.xlsx'
                self.configFile = 'globals.json'
                self.mainWindowPosition = (20,30)
                self.readContentsOfGlobals()

    @staticmethod
    def __convert_configPosition2Tuple(inString):
        x = int(inString.split(",")[0].lstrip("("))
        y = int(inString.split(",")[1].rstrip(")"))

        return (x,y)




