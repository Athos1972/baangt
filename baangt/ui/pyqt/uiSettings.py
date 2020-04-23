# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'globalSettings.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(QtCore.QObject):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(900, 480)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../baangt/baangt/ui/pyqt/baangtIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: rgb(229, 222, 206);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 856, 377))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setSpacing(12)
        self.formLayout.setObjectName("formLayout")
        self.lineEdit1Label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lineEdit1Label.setToolTip("")
        self.lineEdit1Label.setObjectName("lineEdit1Label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lineEdit1Label)
        self.lineEdit1LineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit1LineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(46, 52, 54);")
        self.lineEdit1LineEdit.setObjectName("lineEdit1LineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit1LineEdit)
        self.checkBox1Label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.checkBox1Label.setObjectName("checkBox1Label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.checkBox1Label)
        self.checkBox1CheckBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox1CheckBox.setStyleSheet("color: rgb(46, 52, 54);")
        self.checkBox1CheckBox.setObjectName("checkBox1CheckBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.checkBox1CheckBox)
        self.comboBox1Label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.comboBox1Label.setObjectName("comboBox1Label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.comboBox1Label)
        self.comboBox1ComboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox1ComboBox.setStyleSheet("color: rgb(46, 52, 54);\n"
"background-color: rgb(255, 255, 255);")
        self.comboBox1ComboBox.setObjectName("comboBox1ComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox1ComboBox)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.okPushButton = QtWidgets.QPushButton(self.groupBox)
        self.okPushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(52, 101, 164);")
        self.okPushButton.setObjectName("okPushButton")
        self.horizontalLayout.addWidget(self.okPushButton)
        self.savePushButton = QtWidgets.QPushButton(self.groupBox)
        self.savePushButton.setStyleSheet("background-color: rgb(52, 101, 164);\n"
"color: rgb(255, 255, 255);")
        self.savePushButton.setObjectName("savePushButton")
        self.horizontalLayout.addWidget(self.savePushButton)
        self.saveAspushButton = QtWidgets.QPushButton(self.groupBox)
        self.saveAspushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(52, 101, 164);")
        self.saveAspushButton.setObjectName("saveAspushButton")
        self.horizontalLayout.addWidget(self.saveAspushButton)
        self.AddMorePushButton = QtWidgets.QPushButton(self.groupBox)
        self.AddMorePushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(115, 210, 22);")
        self.AddMorePushButton.setObjectName("AddMorePushButton")
        self.horizontalLayout.addWidget(self.AddMorePushButton)
        self.deleteLastPushButton = QtWidgets.QPushButton(self.groupBox)
        self.deleteLastPushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(204, 0, 0);")
        self.deleteLastPushButton.setObjectName("deleteLastPushButton")
        self.horizontalLayout.addWidget(self.deleteLastPushButton)
        self.exitPushButton = QtWidgets.QPushButton(self.groupBox)
        self.exitPushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(204, 0, 0);")
        self.exitPushButton.setObjectName("exitPushButton")
        self.horizontalLayout.addWidget(self.exitPushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Settings in globals.json"))
        self.lineEdit1Label.setText(_translate("Form", "lineEdit1"))
        self.checkBox1Label.setText(_translate("Form", "checkBox1"))
        self.comboBox1Label.setText(_translate("Form", "comboBox1"))
        self.okPushButton.setToolTip(_translate("Form", "Save to Current File and Close Window"))
        self.okPushButton.setText(_translate("Form", "Ok"))
        self.savePushButton.setToolTip(_translate("Form", "Save to Current File"))
        self.savePushButton.setText(_translate("Form", "Save"))
        self.saveAspushButton.setToolTip(_translate("Form", "Save to New File Name"))
        self.saveAspushButton.setText(_translate("Form", "Save As"))
        self.AddMorePushButton.setToolTip(_translate("Form", "Add Entry To Bottom"))
        self.AddMorePushButton.setText(_translate("Form", "Add More"))
        self.deleteLastPushButton.setToolTip(_translate("Form", "Delete Last Entry"))
        self.deleteLastPushButton.setText(_translate("Form", "Delete Last"))
        self.exitPushButton.setToolTip(_translate("Form", "Discard Unsaved Changes and Close"))
        self.exitPushButton.setText(_translate("Form", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

