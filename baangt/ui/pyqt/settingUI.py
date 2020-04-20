# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from baangt.ui.pyqt.uiSettings import Ui_Form as SettingForm
from baangt.ui.pyqt.settingsGlobal import GlobalSettings
import sys
import os
import json
import configparser


class settingUI(SettingForm):
    def __init__(self, configFile=None, directory="./"):
        SettingForm.__init__(self)
        self.configInstance = GlobalSettings.getInstance()
        self.configFile = configFile

    def setupUi(self, Form):
        super().setupUi(Form)
        Form.resize(500, 480)
        self.readConfig()
        self.readConfigFile()
        self.drawSetting()
        self.okPushButton.clicked.connect(self.saveToFile)
        self.savePushButton.clicked.connect(self.saveToFile)
        # self.exitPushButton.clicked.connect(self.quitApplication)
        self.saveAspushButton.clicked.connect(self.saveAsNewFile)

    def readConfig(self):
        """ Read existing baangt.ini file """
        config = configparser.ConfigParser()
        try:
            config.read("baangt.ini")
            self.directory = config["Default"]['path']
            self.configFile  = config["Default"]['globals']
        except Exception as e:
            print("Exception in settingui ", e)
            self.directory = os.getcwd()
            self.configFile = None
            pass

    def readConfigFile(self):
        """ Read the configFile and update the configInstance """
        if self.configFile:
            if os.path.isfile(self.configFile):
                self.configInstance.addValue(self.configFile)

    @QtCore.pyqtSlot()
    def quitApplication(self):
        """ Exit the application """
        QtWidgets.QApplication.exit()

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
                data[key] = value['default']

            with open(newFile, 'w') as f:
                json.dump(data, f, indent=4)

    @QtCore.pyqtSlot()
    def saveToFile(self):
        """ Save the content to file"""
        # call saveFile before saving to File
        self.saveValue()
        data = {}
        for key, value in self.configInstance.config.items():
            data[key] = value['default']

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

            with open(self.configFile, 'w') as f:
                json.dump(data, f, indent=4)

    @QtCore.pyqtSlot()
    def saveValue(self):
        """ This simple function will print the value from
        formlayout widget
        """
        data = {}
        count = self.formLayout.count()
        for d in range(0, count):
            item = self.formLayout.itemAt(d)
            if isinstance(item, QtWidgets.QHBoxLayout):
                # Type got:  lable  :  fieldname
                label_item = item.itemAt(0).widget()
                input_item = item.itemAt(1).widget()
                if isinstance(input_item, QtWidgets.QLineEdit):
                    value = input_item.text()
                elif isinstance(input_item, QtWidgets.QComboBox):
                    value = input_item.currentText()
                data[label_item.objectName()] = value
            elif isinstance(item, QtWidgets.QWidgetItem):
                # we got checkbox item
                checkbox_item = item.widget()
                data[checkbox_item.objectName()] = checkbox_item.isChecked()
        # save and update the globals Setting
        self.configInstance.updateValue(data)
        # update the screen
        self.drawSetting()

        # print(data)

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

        # update the groupbox headlines
        if self.configFile:
            settingFile = self.configFile
        else:
            settingFile = "globalSetting.json"
        _translate = QtCore.QCoreApplication.translate
        self.groupBox.setTitle(
                   _translate(
                       "Form",
                       "Settings in {}".format(settingFile)
                       ))
        settings = self.configInstance.config
        count = 0
        for key, value in sorted(
                         settings.items(),
                         key=lambda x: x[1]['type']
                         ):
            if value['type'] == 'bool':
                count += 1
                # create check box
                self.checkBox = QtWidgets.QCheckBox(self.groupBox)
                self.checkBox.setObjectName(key)
                self.checkBox.setToolTip(value['hint'])
                self.checkBox.setText(_translate("Form", value['displayText']))
                if isinstance(value['default'], bool):
                    self.checkBox.setChecked(value['default'])
                elif isinstance(value['default'], str):
                    # its in form 'True', 'TRUE','true','false','False'
                    if value['default'].lower() == 'true':
                        self.checkBox.setChecked(True)
                    else:
                        self.checkBox.setChecked(False)
                self.formLayout.setWidget(
                                  count,
                                  QtWidgets.QFormLayout.SpanningRole,
                                  self.checkBox
                                  )
            elif value['type'] == 'text':
                self.lablebox1 = QtWidgets.QLabel(self.groupBox)
                self.lablebox1.setObjectName(key)
                self.lablebox1.setToolTip(value['hint'])
                self.lablebox1.setText(_translate(
                                 "Form",
                                 key
                                 ))
                self.inputBox = QtWidgets.QLineEdit(self.groupBox)
                if isinstance(value['default'], str):
                    self.inputBox.setText(_translate("Form", value['default']))
                else:
                    self.inputBox.setText(_translate("Form", str(value['default'])))
                self.horizontal1 = QtWidgets.QHBoxLayout()
                self.horizontal1.addWidget(self.lablebox1)
                self.horizontal1.addWidget(self.inputBox)
                self.formLayout.addRow(self.horizontal1)

            elif value['type'] == 'select':
                self.lablebox1 = QtWidgets.QLabel(self.groupBox)
                self.lablebox1.setText(_translate(
                                 "Form",
                                 value['displayText']
                                 ))
                self.lablebox1.setObjectName(key)
                self.lablebox1.setToolTip(value['hint'])
                self.comboBox = QtWidgets.QComboBox(self.groupBox)
                self.comboBox.addItems(value['options'])
                self.horizontal1 = QtWidgets.QHBoxLayout()
                self.horizontal1.addWidget(self.lablebox1)
                self.horizontal1.addWidget(self.comboBox)
                self.formLayout.addRow(self.horizontal1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = settingUI()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
