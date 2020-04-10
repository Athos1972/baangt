# This Python file uses the following encoding: utf-8

# if__name__ == "__main__":
#     pass
from baangt.ui.pyqt.uidesign import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
import os
import glob
import json
from pathlib import Path
import baangt.base.GlobalConstants as GC
from baangt.base.Utils import utils
import json
import logging
import configparser
import subprocess
import sys


logger = logging.getLogger("pyC")




class MainWindow(Ui_MainWindow):
    """ BaangtUI : Logic implementation file for uidesign
    """

    def __init__(self):
        ''' Init the super class '''
        super().__init__()

    def setupUi(self, MainWindow):
        ''' Setup the UI for super class and Implement the
        logic here we want to do with User Interface
        '''
        super().setupUi(MainWindow)
        self.directory = ""
        self.configFile = None
        self.configFiles = []
        self.configContents = {}
        self.tempConfigFile = None
        self.testRunFile = None
        self.testRunFiles = []
        self.refreshNew()
        self.setupBasePath()

        # Add Button Signals and Slot here
        self.browsePushButton.clicked.connect(self.browsePathSlot)
        # self.executePushButton.clicked(self.executeTest)
        self.settingsPushButton.clicked.connect(self.settingView)
        self.settingComboBox.activated.connect(self.updateSettings)

        # When Test Run file changes
        self.testRunComboBox.activated.connect(self.updateRunFile)
        # settings View action
        self.settingsClosePushButton.clicked.connect(self.refreshNew)

        # Logs View Action
        self.LogsClosePushButton.clicked.connect(self.refreshNew)
        self.executePushButton.clicked.connect(self.logsView)

        # MenuBar preferences >> Settings action clicked
        self.actionsettings.triggered.connect(self.displaySettings)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Quit Event
        self.actionExit.triggered.connect(self.quitApplication)

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
        self.testRunFiles = glob.glob("*.xlsx")
        self.configFiles = glob.glob("global*.json")

        # update the combo box
        self.testRunComboBox.clear()
        self.settingComboBox.clear()
        # Also, disable Execute and Details Button
        self.executePushButton.setEnabled(False)
        self.settingsPushButton.setEnabled(False)
        # Add files in Combo Box
        self.testRunComboBox.addItems(self.testRunFiles)
        self.settingComboBox.addItems(self.configFiles)

        # set default selection to 0
        if len(self.testRunFiles) > 0:
            self.testRunComboBox.setCurrentIndex(0)
            self.testRunFile = self.testRunComboBox.currentText()
            self.statusMessage("testrun file: {}".format(self.testRunFile))
            # Activate the Execute Button
            self.executePushButton.setEnabled(True)

        if len(self.configFiles) > 0:
            self.settingComboBox.setCurrentIndex(0)
            # Activate the Settings Detail Button
            self.configFile = self.settingComboBox.currentText()
            self.statusMessage("value of self.configfile {}".format(self.configFile))
            self.settingsPushButton.setEnabled(True)
            self.updateSettings()

        # get back to orig_dir
        os.chdir(orig_path)

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
            self.pathLineEdit.insert(dirPath)
        else:
            self.pathLineEdit.insert(dirPath)
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
    def refreshNew(self):
        """
        This method will refresh ui to initial state.
        Hide Bottom Settings and Logs Viewer.
        Made for closeSettingsButton and closeLogsButton
        """
        # Bottom Left and Right splitter
        self.settingsAndLogSplitter.setSizes([300, 0])

        # Hide Log Viewer Initially
        self.mainAndExtraSplitter.setSizes([300, 0])

        # Initially Hide splitter bottom part
        # self.centralwidget.resize(912, 400)

    @pyqtSlot()
    def updateRunFile(self):
        """ this file will update the testRunFile selection
        """
        self.testRunFile = os.path.join(self.directory,
                                  self.testRunComboBox.currentText())
        self.statusMessage("Test Run Changed to: {}".format(self.testRunFile))

    @pyqtSlot()
    def updateSettings(self):
        """ Update the settings Variable with content in fileName"""
        # Try to get full path
        self.configFile = os.path.join(self.directory,
                                 self.settingComboBox.currentText())

        self.statusMessage("Settings changed to: {}".format(self.configFile))

        # complete Path
        if os.path.abspath(self.configFile):
            # File is valid , try to open
            try:
                with open(self.configFile, 'r') as f:
                    globaldata = json.loads(f.read())

            except Exception as e:
                print("Error occured ", e)
                globaldata = {}

            # clear all exiting settings
            self.settingsTableWidget.clear()
            # reprint the table data
            for i, keypair in enumerate(globaldata.items()):
                # parameter
                if not isinstance(keypair[1], str):
                    print("Invalid value pair found", keypair)
                    continue
                self.settingsTableWidget.setItem(
                                    i,
                                    0,
                                    QtWidgets.QTableWidgetItem(keypair[0])
                                    )
                # value

                self.settingsTableWidget.setItem(
                                    i,
                                    1,
                                    QtWidgets.QTableWidgetItem(keypair[1])
                                    )

    def runTestRun(self):
        if not self.configFile:
            self.statusMessage("No Config File", 2000)
            return
        if not self.testRunFile:
            self.statusMessage("No test Run File selected", 2000)

        runCmd = self._getRunCommand()


        if self.configContents.get("TX.DEBUG"):
            from baangt.base.TestRun.TestRun import TestRun

            lTestRun = TestRun(f"{Path(self.directory).joinpath(self.testRunFile)}",
                               globalSettingsFileNameAndPath=f'{Path(self.directory).joinpath(self.tempConfigFile)}')

        else:
            logger.info(f"Running command: {runCmd}")
            p = subprocess.run(runCmd, shell=True, close_fds=True)

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
        self.mainAndExtraSplitter.setSizes([0, 300])
        self.settingsAndLogSplitter.setSizes([300, 0])

    @pyqtSlot()
    def displaySettings(self):
        """
        Display and edit Current settings, via Globals.json file
        Control:
            make upper part of splitter to 0.
            and make right part of log window to 0.
        """
        # Logs View to zero
        self.settingsAndLogSplitter.setSizes([300, 0])

        # main Area to zero
        self.mainAndExtraSplitter.setSizes([0, 300])

    @pyqtSlot()
    def logsView(self):
        """
        View Logs Below the Main Window
        """
        self.mainAndExtraSplitter.setSizes([0, 300])
        self.settingsAndLogSplitter.setSizes([0, 300])
        # run the command
        self.runTestRun()


    @pyqtSlot()
    def browsePathSlot(self):
        """ Browse Folder Containing *.xlsx file for execution. And
           globals.json file for Test specific settings
        """
        # get path from pathLineEdit
        basepath = self.pathLineEdit.text()
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
