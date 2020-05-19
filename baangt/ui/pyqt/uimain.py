# This Python file uses the following encoding: utf-8

# if__name__ == "__main__":
#     pass
# from baangt.ui.pyqt.uidesign import Ui_MainWindow
from baangt.ui.pyqt.uiDesign import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
import os
import glob
import json
from pathlib import Path
import baangt.base.GlobalConstants as GC
from baangt.base.Utils import utils
import logging
import configparser
# import subprocess
import sys
from baangt.ui.pyqt import resources
from baangt.ui.pyqt.settingsGlobal import GlobalSettings
from baangt.ui.ImportKatalonRecorder import ImportKatalonRecorder
import pyperclip
import platform
from baangt.base.PathManagement import ManagedPaths
from uuid import uuid4
from baangt.base.FilesOpen import FilesOpen

logger = logging.getLogger("pyC")

class PyqtKatalonUI(ImportKatalonRecorder):
    """ Subclass of ImportKatalonRecorder :
        Aim : To disable GUI created by PySimpleGui
        and initialize everything
    """
    def __init__(self, directory=None):
        self.managedPaths = ManagedPaths()
        if directory == None:
            directory = self.managedPaths.derivePathForOSAndInstallationOption()
        self.directory = directory
        self.clipboardText = ""
        self.outputText = ""
        self.window = None
        self.outputData = {}
        self.outputFormatted = []
        self.fileNameExport = None


class MainWindow(Ui_MainWindow):
    """ BaangtUI : Logic implementation file for uidesign
    """

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        ''' Init the super class '''
        super().__init__()

    def setupUi(self, MainWindow, directory=None):
        ''' Setup the UI for super class and Implement the
        logic here we want to do with User Interface
        '''
        super().setupUi(MainWindow)
        self.managedPaths = ManagedPaths()
        if directory == None:
            directory = self.managedPaths.derivePathForOSAndInstallationOption()
        self.directory = directory
        self.configFile = None
        self.configFiles = []
        self.configContents = {}
        self.tempConfigFile = None
        self.testRunFile = None
        self.testRunFiles = []
        # self.refreshNew()
        # self.setupBasePath(self.directory)
        self.readConfig()

        self.katalonRecorder = PyqtKatalonUI(self.directory)
        # update logo and icon
        self.updateLogoAndIcon(MainWindow)

        # initialize Katalon Importer and Global Setting Page
        # Add Button Signals and Slot here
        self.browsePushButton_4.clicked.connect(self.browsePathSlot)
        # self.executePushButton.clicked(self.executeTest)

        # Setting Page actions and triggered
        self.settingsPushButton_4.clicked.connect(self.settingView)
        self.okPushButton.clicked.connect(self.saveToFile)
        self.settingComboBox_4.activated.connect(self.updateSettings)
        self.testRunComboBox_4.activated.connect(self.updateRunFile)
        self.exitPushButton.clicked.connect(self.mainPageView)
        self.AddMorePushButton.clicked.connect(self.addMore)
        self.deleteLastPushButton.clicked.connect(self.deleteLast)
        self.saveAspushButton.clicked.connect(self.saveAsNewFile)
        self.executePushButton_4.clicked.connect(self.runTestRun)

        # FileOpen buttons
        self.openResultFilePushButton_4.clicked.connect(self.openResultFile)
        self.openLogFilePushButton_4.clicked.connect(self.openLogFile)
        self.openTestFilePushButton_4.clicked.connect(self.openTestFile)

        # Quit Event
        self.actionExit.triggered.connect(self.quitApplication)

        # Katalon triggered
        self.actionImport_Katalon.triggered.connect(self.show_katalon)
        self.exitPushButton_3.clicked.connect(self.exitKatalon)
        self.savePushButton_2.clicked.connect(self.saveTestCase)
        self.copyClipboard_2.clicked.connect(self.copyFromClipboard)
        self.TextIn_2.textChanged.connect(self.importClipboard)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def saveInteractiveGuiConfig(self):
        """ Save Interactive Gui Config variables """
        config = configparser.ConfigParser()
        config["Default"] = {
                    "path": self.directory,
                    "testrun": self.testRunComboBox_4.currentText(),
                    "globals": self.settingComboBox_4.currentText(),
                    }
        with open(self.managedPaths.getOrSetIni().joinpath("baangt.ini"), "w" ) as configFile:
            config.write(configFile)

    def readConfig(self):
        """ Read existing baangt.ini file """
        config = configparser.ConfigParser()
        try:
            config.read(self.managedPaths.getOrSetIni().joinpath("baangt.ini"))
            self.directory = config["Default"]['path']
            self.testRunFile = config["Default"]['testrun']
            self.configFile  = config["Default"]['globals']
            self.setupBasePath(self.directory)
            self.readContentofGlobals()
        except Exception as e:
            print("Exception in Main readConfig. Starting with defaults", e)
            self.directory = self.managedPaths.derivePathForOSAndInstallationOption().joinpath("examples")
            if not self.directory.is_dir():
                self.directory = str(self.managedPaths.derivePathForOSAndInstallationOption())
            else:
                self.directory = str(self.directory)
            self.setupBasePath(self.directory)

    def readContentofGlobals(self):
        """ This will read the content of config file """
        configInstance = GlobalSettings.getInstance()
        configInstance.addValue(self.configFile)
        self.configContents = configInstance.config
        if not self.configContents.get('TC.' + GC.DATABASE_LINES):
            key = 'TC.' + GC.DATABASE_LINES
            self.configContents[key] = ""
        if not self.configContents.get('TC.' + GC.EXECUTION_DONTCLOSEBROWSER):
            key = 'TC.' + GC.EXECUTION_DONTCLOSEBROWSER
            self.configContents[key] = ""
        if not self.configContents.get('TC.' + GC.EXECUTION_SLOW):
            key = 'TC.' + GC.EXECUTION_SLOW
            self.configContents[key] = ""

    @QtCore.pyqtSlot()
    def show_katalon(self):
        """ Display katalon panel for Test case preparation """
        self.stackedWidget.setCurrentIndex(2)
        self.statusMessage("Katalon Studio is triggered", 1000)

    def updateLogoAndIcon(self, MainWindow):
        """ This function initialize logo and icon """
        logo_pixmap = QtGui.QPixmap(":/baangt/baangtlogo")
        logo_pixmap.scaled(300, 120, QtCore.Qt.KeepAspectRatio)
        self.logo_4.setPixmap(logo_pixmap)
        icon = QtGui.QIcon()
        icon.addPixmap(
                QtGui.QPixmap(":/baangt/baangticon"),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off
                )
        MainWindow.setWindowIcon(icon)

        self.mainPage.setStyleSheet(
                 "QLineEdit { background-color: white; \n"
                 "            color: rgb(46, 52, 54);  \n"
                 "}"
                 "QComboBox { background-color: white; \n"
                 "            color: rgb(46, 52, 54);  \n"
                 "}"
                 "QButton { color: white; \n"
                 "}"
                 )

        self.settingPage.setStyleSheet(
                 "QLineEdit { background-color: white; \n"
                 "            color: rgb(46, 52, 54);  \n"
                 "}"
                 "QComboBox { background-color: white; \n"
                 "            color: rgb(46, 52, 54);  \n"
                 "}"
                 "QLabel { font: 75 11pt 'Arial';\n"
                 "}"
                 "QButton { color: white; \n"
                 "}"
                 )
        self.katalonPage.setStyleSheet(
                 "QButton { color: white; \n"
                 "}"
                 )

        MainWindow.resize(980, 480)

    def statusMessage(self, str, duration=1000):
        """ Display status message passed in Status Bar
        Default duration (ms) = 1000 (1 sec)
        """
        self.statusbar.showMessage(str, duration)

    def getSettingsAndTestFilesInDirectory(self, dirName):
        """ Scan for *.xlsx files and *.json files and
        update the testRunComboBox and settingsComboBox items
        """
        if not dirName and not os.path.isdir(dirName):
            dirName = os.getcwd()
        # for getting back to original directory
        orig_path = os.getcwd()
        os.chdir(dirName)
        # self.testRunFiles = glob.glob("*.xlsx")
        # self.configFiles = glob.glob("global*.json")
        self.testRunFiles = []
        self.configFiles = []

        fileList = glob.glob("*.json")
        fileList.extend(glob.glob("*.xlsx"))
        if not platform.system().lower() == 'windows':
            # On MAC and LINUX there may be also upper/lower-Case versions
            fileList.extend(glob.glob("*.JSON"))
            fileList.extend(glob.glob("*.XLSX"))
        for file in fileList:
            if file[0:6].lower() == 'global':      # Global Settings for Testrun must start with global_*
                self.configFiles.append(file)
            else:
                self.testRunFiles.append(file)
            pass

        # get back to orig_dir
        os.chdir(orig_path)

        # update the combo box
        self.testRunComboBox_4.clear()
        self.settingComboBox_4.clear()
        # Also, disable Execute and Details Button
        self.executePushButton_4.setEnabled(False)
        self.settingsPushButton_4.setEnabled(False)
        # Add files in Combo Box
        self.testRunComboBox_4.addItems(
                        sorted(self.testRunFiles, key=lambda x: x.lower())
                               )
        self.settingComboBox_4.addItems(
                        sorted(self.configFiles, key=lambda x: x.lower())
                               )

        # set default selection to 0

        if len(self.testRunFiles) > 0:
            # if testrun file not in Combo box of TestRunFiles
            index = self.testRunComboBox_4.findText(
                                 self.testRunFile,
                                 QtCore.Qt.MatchFixedString
                                 )
            if self.testRunFile not in self.testRunFiles:
                self.testRunComboBox_4.setCurrentIndex(0)
                self.testRunFile = self.testRunComboBox_4.currentText()
            else:
                self.testRunComboBox_4.setCurrentIndex(index)
            self.statusMessage("testrun file: {}".format(self.testRunFile))
            # Activate the Execute Button
            self.executePushButton_4.setEnabled(True)

        if len(self.configFiles) > 0:
            # if config file not in list of ConfigListFiles
            index = self.settingComboBox_4.findText(
                              self.configFile,
                              QtCore.Qt.MatchFixedString
                              )
            if self.configFile not in self.configFiles:
                self.settingComboBox_4.setCurrentIndex(0)
                # Activate the Settings Detail Button
                self.configFile = self.settingComboBox_4.currentText()
            else:
                self.settingComboBox_4.setCurrentIndex(index)
            self.statusMessage("value of self.configfile {}".format(
                               self.configFile))
            self.settingsPushButton_4.setEnabled(True)
            self.updateSettings()

    def setupBasePath(self, dirPath=""):
        """ Setup Base path of Execution as per directory Path"""

        if not dirPath:
            # Set up base path to Baangt directory
            # Based on current File path ../../../
            dirPath = os.path.dirname(os.path.dirname(
                          os.path.dirname(os.path.dirname(__file__))
                          ))
            if not dirPath:
                dirPath = os.path.abspath(os.curdir)
            self.pathLineEdit_4.insert(dirPath)
        else:
            self.pathLineEdit_4.setText(dirPath)
        self.directory = dirPath
        self.getSettingsAndTestFilesInDirectory(dirPath)
        self.statusMessage("Current Path: {} ".format(dirPath), 2000)

    @pyqtSlot()
    def quitApplication(self):
        """ This function will close the UI """
        buttonReply = QtWidgets.QMessageBox.question(
                           self.centralwidget,
                           "Close Confirmation ",
                           "Are you sure to quit?",
                           QtWidgets.QMessageBox.Yes |
                           QtWidgets.QMessageBox.No,
                           QtWidgets.QMessageBox.No
                           )
        if buttonReply == QtWidgets.QMessageBox.Yes:
            QtWidgets.QApplication.exit()

    @pyqtSlot()
    def mainPageView(self):
        """ This function will redirect to main page """
        self.stackedWidget.setCurrentIndex(0)

    @pyqtSlot()
    def updateRunFile(self):
        """ this file will update the testRunFile selection
        """
        self.testRunFile = os.path.join(self.directory,
                                  self.testRunComboBox_4.currentText())
        self.statusMessage("Test Run Changed to: {}".format(self.testRunFile))
        self.saveInteractiveGuiConfig()

    @pyqtSlot()
    def updateSettings(self):
        """ Update the settings Variable with content in fileName"""
        # Try to get full path
        # write changes to ini file
        self.configFile = os.path.join(self.directory,
                                 self.settingComboBox_4.currentText())

        self.saveInteractiveGuiConfig()
        self.statusMessage("Settings changed to: {}".format(self.configFile))
        self.readContentofGlobals()

    @pyqtSlot()
    def runTestRun(self):
        if not self.configFile:
            self.statusMessage("No Config File", 2000)
            return
        if not self.testRunFile:
            self.statusMessage("No test Run File selected", 2000)

        runCmd = self._getRunCommand()

        # show status in status bar
        self.statusMessage("Executing.....", 4000)

        if self.configContents.get("TX.DEBUG"):
            from baangt.base.TestRun.TestRun import TestRun

            lUUID = uuid4()
            self.lTestRun = TestRun(f"{Path(self.directory).joinpath(self.testRunFile)}",
                 globalSettingsFileNameAndPath=f'{Path(self.directory).joinpath(self.tempConfigFile)}', uuid=lUUID)

        else:
            logger.info(f"Running command: {runCmd}")
            self.run_process = QtCore.QProcess()
            self.run_process.execute(runCmd)
            # p = subprocess.run(runCmd, shell=True, close_fds=True)
            # Set status to show Execution is complete
            buttonReply = QtWidgets.QMessageBox.question(
                                self.centralwidget,
                                "Baangt Interactive Starter ",
                                "Test Run finished !!",
                                QtWidgets.QMessageBox.Ok,
                                QtWidgets.QMessageBox.Ok
                                 )

        self.statusMessage(f"Completed ", 3000)

        # Remove temporary Configfile, that was created only for this run:
        try:
            os.remove(Path(self.directory).joinpath(self.tempConfigFile))
        except Exception as e:
            logger.warning(f"Tried to remove temporary file but seems to be not there: "
                           f"{self.directory}/{self.tempConfigFile}")


    def _getRunCommand(self):
        """
        If bundled (e.g. in pyinstaller),
        then the executable is already sys.executable,
        otherwise we need to concatenate executable and
        Script-Name before we can start
        a subprocess.

        @return: Full path and filename to call Subprocess
        """
        lStart = sys.executable
        if "python" in sys.executable.lower():
            if len(Path(sys.argv[0]).parents) > 1:
                # This is a system where the path the the script is
                # given in sys.argv[0]
                lStart = lStart + f" {sys.argv[0]}"
            else:
                # this is a system where we need to join os.getcwd()
                # and sys.argv[0] because the path is not given in sys.argv[0]
                lStart = lStart + f" {Path(os.getcwd()).joinpath(sys.argv[0])}"

        self.__makeTempConfigFile()

        return f"{lStart} " \
               f"--run='{Path(self.directory).joinpath(self.testRunFile)}' " \
               f"--globals='{Path(self.directory).joinpath(self.tempConfigFile)}'"


    def __makeTempConfigFile(self):
        """
         Add parameters to the Config-File for this Testrun and
         save the file under a temporary name
        """
        self.configContents[GC.PATH_ROOT] = self.directory
        self.configContents[GC.PATH_SCREENSHOTS] = str(Path(
                                  self.directory).joinpath("Screenshots"))
        self.configContents[GC.PATH_EXPORT] = str(Path(
                                  self.directory).joinpath("1testoutput"))
        self.configContents[GC.PATH_IMPORT] = str(Path(
                                  self.directory).joinpath("0testdateninput"))
        self.tempConfigFile = MainWindow.__makeRandomFileName()
        self.saveContentsOfConfigFile(self.tempConfigFile)

    def saveContentsOfConfigFile(self, lFileName = None):
        if not lFileName:
            lFileName = self.configFile

        with open(str(Path(self.directory).joinpath(lFileName)), 'w') as outfile:
            json.dump(self.configContents, outfile, indent=4)


    @staticmethod
    def __makeRandomFileName():
        return "globals_" + utils.datetime_return() + ".json"

    @pyqtSlot()
    def settingView(self):
        """
        View settings Below Main Windows
        """
        self.statusMessage("Settings Page Opened")
        self.stackedWidget.setCurrentIndex(1)
        self.readConfigFile()
        self.drawSetting()

    @pyqtSlot()
    def browsePathSlot(self):
        """ Browse Folder Containing *.xlsx file for execution. And
           globals.json file for Test specific settings
        """
        # get path from pathLineEdit
        basepath = self.pathLineEdit_4.text()
        if not basepath:
            basepath = "./"
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        dirName = QtWidgets.QFileDialog.getExistingDirectory(
                         None,
                         "Select Directory ",
                         basepath,
                         options=options
                         )
        if dirName:
            # self.pathLineEdit.insert(dirName)
            self.setupBasePath(dirName)

    # Settings Page
    # All action and function related to Setting page is below
    def readConfigFile(self):
        """ Read the configFile and update the configInstance """
        if self.configFile:
            # Compute full path
            fullpath = os.path.join(self.directory, self.configFile)
            if os.path.isfile(fullpath):
                self.configInstance = GlobalSettings.getInstance()
                self.configInstance.addValue(fullpath)

    @QtCore.pyqtSlot()
    def addMore(self):
        """ This function will popup a dialog box,
        User input the keword and a new row is added
        to Form Layout
        """
        # get total no of rows, it will be index for new row
        count = self.formLayout.rowCount()
        all_keys = self.configInstance.globalconfig.items()
        # get keys values from formLayout
        formlayoutItems = self.parseFormLayout()

        # convert to dict, to fix unhashable type: dict error
        all_keys = dict(all_keys)
        # unused keys : globalconfig keys - formlayout keys
        keys = [d for d in all_keys.keys() if d not in formlayoutItems]

        # Now prepare key and displayText pair
        displayTextPairs = [
                         (k, v['displayText'])
                         for k, v in all_keys.items()
                         if k in keys]

        # to store keys for displayText list
        shownkeys = [p[0] for p in displayTextPairs]
        # to store displayTextList
        shownvalues = [p[1] for p in displayTextPairs]

        item, okPressed = QtWidgets.QInputDialog.getItem(
                               None,
                               "New Parameter ",
                               "Parameter Name",
                               shownvalues,
                               0,
                               True
                               )
        if item and okPressed:
            if item in shownvalues:
                # get keys using index of item selection
                key = shownkeys[shownvalues.index(item)]
            else:
                # this is the key still not added in globalSettings
                key = item
            value = self.configInstance.globalconfig.get(
                              key,
                              GlobalSettings.transformToDict(key, ""))
            self.addNewRow(count, key, value)

    @QtCore.pyqtSlot()
    def deleteLast(self):
        """ This function when call delete last row
        from the form layout
        """
        # get the index of last row, equals totalrow minus one
        count = self.formLayout.rowCount()

        # delete the count - 1 th row
        if count > 0:
            self.formLayout.removeRow(count - 1)

    @QtCore.pyqtSlot()
    def saveAsNewFile(self):
        """ This will ask new file to save data """
        # save recent changes to config
        self.saveValue()
        # ask for fileName
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename = QtWidgets.QFileDialog.getSaveFileName(
                                None,
                                "Save Global Setting  File",
                                self.directory,
                                "JsonFile (*.json)",
                                "",
                                options=options
                                )
        newFile = filename[0]
        if newFile:
            if not os.path.basename(newFile).endswith(".json"):
                newFile = os.path.join(
                             os.path.dirname(newFile),
                             os.path.basename(newFile) + ".json"
                             )

            data = {}
            for key, value in self.configInstance.config.items():
                data[key] = value

            with open(newFile, 'w') as f:
                json.dump(data, f, indent=4)

    @QtCore.pyqtSlot()
    def saveToFile(self):
        """ Save the content to file"""
        # call saveFile before saving to File
        self.saveValue()
        data = {}
        for key, value in self.configInstance.config.items():
            data[key] = value

        if not self.configFile:
            # Open Dialog box to save file
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            filename = QtWidgets.QFileDialog.getSaveFileName(
                                    None,
                                    "Save Global Setting  File",
                                    self.directory,
                                    "JsonFile (*.json)",
                                    "",
                                    options=options
                                    )
            self.configFile = filename[0]
        if self.configFile:
            if not os.path.basename(self.configFile).endswith(".json"):
                self.configFile = os.path.join(
                             os.path.dirname(self.configFile),
                             os.path.basename(self.configFile) + ".json"
                             )

            fullpath = self.configFile
            if not os.path.isabs(self.configFile):
                if self.directory:
                    fullpath = os.path.join(self.directory, self.configFile)
                else:
                    self.directory = os.getcwd()#.managedPaths.derivePathForOSAndInstallationOption()
                    fullpath = os.path.join(self.directory, self.configFile)

            with open(fullpath, 'w') as f:
                json.dump(data, f, indent=4)

        self.drawSetting()
        self.readContentofGlobals()
        self.mainPageView()

    def parseFormLayout(self):
        """ This function will parse form layout
        and return dictionary items
        """
        data = {}
        count = self.formLayout.rowCount()
        for d in range(count):

            # item = self.formLayout.takeRow(0)
            labelItem = self.formLayout.itemAt(
                                   d,
                                   QtWidgets.QFormLayout.LabelRole
                                   )

            fieldItem = self.formLayout.itemAt(
                                   d,
                                   QtWidgets.QFormLayout.FieldRole
                                   )
            # print(labelItem)
            # print(fieldItem)
            key = ""
            value = ""
            if isinstance(labelItem, QtWidgets.QWidgetItem):
                lablename = labelItem.widget()
                key = lablename.objectName()
            if isinstance(fieldItem, QtWidgets.QWidgetItem):
                fieldname = fieldItem.widget()
                if isinstance(fieldname, QtWidgets.QCheckBox):
                    # get checked status
                    value = str(fieldname.isChecked())
                elif isinstance(fieldname, QtWidgets.QComboBox):
                    # get current Text
                    value = fieldname.currentText()
                elif isinstance(fieldname, QtWidgets.QLineEdit):
                    value = fieldname.text()
            if key:
                data[key] = value

        return data

    @QtCore.pyqtSlot()
    def saveValue(self):
        """ This simple function call parseFormlayout to get
        dictionary data and update the config value
        """
        # update the data to config instance
        data = self.parseFormLayout()

        if self.configInstance:
            self.configInstance.updateValue(data)
            # print(self.configInstance.config)
        else:
            print("No config instance ")
            self.configInstance = GlobalSettings.getInstance()
            self.configInstance.updateValue(data)

    def drawSetting(self):
        """ This will draw Setting based on data in configInstance
        """
        # We will use filtered dict key only
        # settings = self.configInstance.filterIniKey()
        # Remove all existing data to print
        n_rows = self.formLayout.rowCount()

        if n_rows > 0:
            # Delete all existing rows
            # print("Number of rows", n_rows)
            for d in range(n_rows):
                self.formLayout.removeRow(0)
        self.formLayout.update()

        # update the groupbox headlines
        if self.configFile:
            settingFile = self.configFile
            # compute full path
            fullpath = os.path.join(self.directory, self.configFile)
            if os.path.isfile(fullpath):
                settingFile = fullpath
        else:
            settingFile = "globalSetting.json"
        _translate = QtCore.QCoreApplication.translate
        self.groupBox.setTitle(
                   _translate(
                       "Form",
                       "Settings in {}".format(
                          os.path.basename(settingFile)
                       )))
        # prepare settings here
        settings = {}
        for key, value in self.configInstance.config.items():
            if key in self.configInstance.globalconfig:
                settings[key] = self.configInstance.globalconfig[key]
                settings[key]['default'] = value
            else:
                settings[key] = GlobalSettings.transformToDict(key, value)

        # settings = self.configInstance.config
        count = 0
        for key, value in sorted(
                         settings.items(),
                         key=lambda x: x[1]['type']
                         ):
            self.addNewRow(count, key, value)
            count += 1

    def addNewRow(self, count, key, value):
        """ This function will add new row at
        count number with given key value pair
        in formlayout
        """
        _translate = QtCore.QCoreApplication.translate
        if value['type'] == 'bool':
            # create check box
            self.checkBox1Label = QtWidgets.QLabel(
                                 self.scrollAreaWidgetContents
                                  )
            self.checkBox1Label.setObjectName(key)
            self.checkBox1Label.setToolTip(value['hint'])
            self.checkBox1Label.setText(
                           _translate("Form", value['displayText']))
            self.checkBox1CheckBox = QtWidgets.QCheckBox(
                            self.scrollAreaWidgetContents)
            # self.checkBox1CheckBox.setStyleSheet(
            #                "color: rgb(46, 52, 54);")
            if isinstance(value['default'], bool):
                # its bool type
                self.checkBox1CheckBox.setChecked(value['default'])

            elif isinstance(value['default'], str):
                # its string type
                if value['default'].lower() == "true":
                    self.checkBox1CheckBox.setChecked(True)
                else:
                    self.checkBox1CheckBox.setChecked(False)
            else:
                # default
                self.checkBox1CheckBox.setChecked(False)
            self.formLayout.setWidget(
                              count,
                              QtWidgets.QFormLayout.LabelRole,
                              self.checkBox1Label)
            self.formLayout.setWidget(
                              count,
                              QtWidgets.QFormLayout.FieldRole,
                              self.checkBox1CheckBox)

        elif value['type'] == 'text':
            self.lineEdit1Label = QtWidgets.QLabel(
                              self.scrollAreaWidgetContents)
            self.lineEdit1Label.setToolTip(
                               _translate("Form", value['hint']))
            self.lineEdit1Label.setObjectName(key)
            self.lineEdit1Label.setText(
                               _translate("Form", value['displayText'])
                               )
            self.lineEdit1LineEdit = QtWidgets.QLineEdit(
                              self.scrollAreaWidgetContents)
            sizePolicy = QtWidgets.QSizePolicy(
                        QtWidgets.QSizePolicy.MinimumExpanding,
                        QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                    self.lineEdit1LineEdit.sizePolicy().hasHeightForWidth())
            self.lineEdit1LineEdit.setSizePolicy(sizePolicy)
            self.lineEdit1LineEdit.setMinimumSize(QtCore.QSize(250, 0))

            # self.lineEdit1LineEdit.setStyleSheet(
            #                 "background-color: rgb(255, 255, 255);\n"
            #                 "color: rgb(46, 52, 54);")
            self.lineEdit1LineEdit.setText(
                             _translate("Form", value['default']))
            self.formLayout.setWidget(
                             count,
                             QtWidgets.QFormLayout.LabelRole,
                             self.lineEdit1Label)
            self.formLayout.setWidget(
                             count,
                             QtWidgets.QFormLayout.FieldRole,
                             self.lineEdit1LineEdit)

        elif value['type'] == 'select':
            self.comboBox1Label = QtWidgets.QLabel(
                             self.scrollAreaWidgetContents)
            self.comboBox1Label.setObjectName(key)
            self.comboBox1Label.setToolTip(value['hint'])
            self.comboBox1Label.setText(
                             _translate("Form", value['displayText']))
            self.formLayout.setWidget(
                              count,
                              QtWidgets.QFormLayout.LabelRole,
                              self.comboBox1Label)
            self.comboBox1ComboBox = QtWidgets.QComboBox(
                              self.scrollAreaWidgetContents)
            # self.comboBox1ComboBox.setStyleSheet(
            #                  "color: rgb(46, 52, 54):\n"
            #                  "background-color: rgb(255, 255, 255);")
            self.comboBox1ComboBox.addItems(value['options'])
            # set the Value
            self.comboBox1ComboBox.setCurrentIndex(
                            self.comboBox1ComboBox.findText(
                                value['default'],
                                QtCore.Qt.MatchFixedString
                                ))
            self.formLayout.setWidget(
                              count,
                              QtWidgets.QFormLayout.FieldRole,
                              self.comboBox1ComboBox)

    # Katalon Recorder Page
    #  All setting and Action for Katalon Page is Below
    @QtCore.pyqtSlot()
    def exitKatalon(self):
        """ this function will clear text from textIn and
        TextOut and exit
        """
        self.TextIn_2.clear()
        self.TextOut_2.clear()
        self.stackedWidget.setCurrentIndex(0)

    @QtCore.pyqtSlot()
    def saveTestCase(self):
        """ Use Existing ImportKatalonRecorder.saveTestCase internally to
        save test cast to XLSX
        """
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog

        filename = QtWidgets.QFileDialog.getSaveFileName(
                                None,
                                "Save Test Case File",
                                self.katalonRecorder.directory,
                                "",
                                "",
                                options=options
                                )
        # resulted filename is in tuple, (fullpath, All Files(*))
        if filename[0]:
            self.katalonRecorder.directory = os.path.dirname(filename[0])
            self.katalonRecorder.fileNameExport = os.path.basename(filename[0])
            # save File
            self.katalonRecorder.saveTestCase()

            # Change the testrun file to newone and change directory
            self.testRunFile = self.katalonRecorder.fileNameExport
            self.setupBasePath(self.katalonRecorder.directory)
            self.exitKatalon()


    @QtCore.pyqtSlot()
    def importClipboard(self):
        """Extend: katalonRecorder.importClipboard internally """
        # ignore last line as this will result unexpected
        # Index out of range error
        self.clipboardText = self.TextIn_2.toPlainText()
        self.katalonRecorder.clipboardText = "\n".join([
                              text for text in self.clipboardText.split("\n")
                              if len(text.split("|")) > 2
                              ])
        self.katalonRecorder.importClipboard()
        self.TextOut_2.setPlainText(self.katalonRecorder.outputText)

    @QtCore.pyqtSlot()
    def copyFromClipboard(self):
        """ Call ImportKatalonRecorder.importClipboard internally """
        self.TextIn_2.setPlainText(pyperclip.paste())
        self.importClipboard()

    @QtCore.pyqtSlot()
    def openResultFile(self):
        """ Uses Files Open class to open Result file """
        try:
            filePathName = self.lTestRun.results.fileName
            fileName = os.path.basename(filePathName)
            self.statusbar.showMessage(f"Opening file {fileName}")
            FilesOpen.openResultFile(filePathName)
        except:
            self.statusbar.showMessage("No file found!")

    @QtCore.pyqtSlot()
    def openLogFile(self):
        """ Uses Files Open class to open Log file """
        try:
            filePathName = [
                handler.baseFilename for handler in logger.handlers if isinstance(handler, logging.FileHandler)
            ][0]
            fileName = os.path.basename(filePathName)
            self.statusbar.showMessage(f"Opening file {fileName}")
            FilesOpen.openResultFile(filePathName)
        except:
            self.statusbar.showMessage("No file found!")

    @QtCore.pyqtSlot()
    def openTestFile(self):
        """ Uses Files Open class to open Log file """
        try:
            filePathName = f"{Path(self.directory).joinpath(self.testRunFile)}"
            fileName = os.path.basename(filePathName)
            self.statusbar.showMessage(f"Opening file {fileName}")
            FilesOpen.openResultFile(filePathName)
        except:
            self.statusbar.showMessage("No file found!")


# Controller
class MainController:
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.window = QtWidgets.QMainWindow()
        self.main = MainWindow()

    def show_main(self):
        self.main = MainWindow()
        self.main.setupUi(self.window)
        self.window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    controller = MainController()
    controller.show_main()

    sys.exit(app.exec_())
