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
        self.AddMorePushButton.clicked.connect(self.addMore)
        self.deleteLastPushButton.clicked.connect(self.deleteLast)

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

    def readConfigFile(self):
        """ Read the configFile and update the configInstance """
        if self.configFile:
            # Compute full path
            fullpath = os.path.join(self.directory, self.configFile)
            if os.path.isfile(fullpath):
                self.configInstance.addValue(fullpath)

    @QtCore.pyqtSlot()
    def quitApplication(self):
        """ Exit the application """
        QtWidgets.QApplication.exit()

    @QtCore.pyqtSlot()
    def addMore(self):
        """ This function will popup a dialog box,
        User input the keword and a new row is added
        to Form Layout
        """
        # get total no of rows, it will be index for new row
        count = self.formLayout.rowCount()

        all_keys = self.configInstance.globalconfig.keys()
        item, okPressed = QtWidgets.QInputDialog.getItem(
                               None,
                               "New Parameter ",
                               "Parameter Name",
                               all_keys,
                               0,
                               True
                               )
        if item and okPressed:
            key = item
            value = self.configInstance.globalconfig.get(
                              key,
                              GlobalSettings.transformToDict(key, ""))
            self.addNewRow(count, key, value)


        # get the key
        pass

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

            if not os.path.isabs(self.configFile):
                if self.directory:
                    fullpath = os.path.join(self.directory, self.configFile)
                else:
                    self.directory = os.getcwd()
                    fullpath = os.path.join(self.directory, self.configFile)

            with open(fullpath, 'w') as f:
                json.dump(data, f, indent=4)

        self.drawSetting()

    @QtCore.pyqtSlot()
    def saveValue(self):
        """ This simple function save the data and value from
        form layout and return dictionary data
        """
        data = {}
        count = self.formLayout.rowCount()
        for d in range(count):
            item = self.formLayout.takeRow(0)
            labelItem = item.labelItem
            fieldItem = item.fieldItem
            key = ""
            value = ""
            if isinstance(labelItem, QtWidgets.QWidgetItem):
                lablename = labelItem.widget()
                key = lablename.objectName()
            if isinstance(fieldItem, QtWidgets.QWidgetItem):
                fieldname = fieldItem.widget()
                if isinstance(fieldname, QtWidgets.QCheckBox):
                    # get checked status
                    value = fieldname.isChecked()
                elif isinstance(fieldname, QtWidgets.QComboBox):
                    # get current Text
                    value = fieldname.currentText()
                elif isinstance(fieldname, QtWidgets.QLineEdit):
                    value = fieldname.text()
            if key:
                data[key] = value

        # update the data to config instance
        if self.configInstance:
            self.configInstance.updateValue(data)
            # print(self.configInstance.config)
        else:
            print("No config instance ")

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
        settings = self.configInstance.config
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
            self.checkBox1CheckBox.setStyleSheet(
                             "color: rgb(46, 52, 54);")
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
                               _translate("Form", value['displayText']))
            self.lineEdit1LineEdit = QtWidgets.QLineEdit(
                              self.scrollAreaWidgetContents)
            self.lineEdit1LineEdit.setStyleSheet(
                             "background-color: rgb(255, 255, 255);\n"
                             "color: rgb(46, 52, 54);")
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
            self.comboBox1ComboBox.setStyleSheet(
                              "color: rgb(46, 52, 54):\n"
                              "background-color: rgb(255, 255, 255);")
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



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = settingUI("globals.json")
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
