# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'katalonImporter.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(QtCore.QObject):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(900, 480)
        Form.setBaseSize(QtCore.QSize(900, 480))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/new/logo/baangt/baangt/ressources/baangtIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: rgb(229, 222, 206);\n"
"color: rgb(255, 255, 255);")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setHorizontalSpacing(29)
        self.gridLayout.setVerticalSpacing(30)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TextIn = QtWidgets.QPlainTextEdit(Form)
        self.TextIn.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.TextIn.setObjectName("TextIn")
        self.horizontalLayout.addWidget(self.TextIn)
        self.TextOut = QtWidgets.QPlainTextEdit(Form)
        self.TextOut.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.TextOut.setObjectName("TextOut")
        self.horizontalLayout.addWidget(self.TextOut)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.savePushButton = QtWidgets.QPushButton(Form)
        self.savePushButton.setStyleSheet("background-color: rgb(52, 101, 164);")
        self.savePushButton.setObjectName("savePushButton")
        self.horizontalLayout_2.addWidget(self.savePushButton)
        self.copyClipboard = QtWidgets.QPushButton(Form)
        self.copyClipboard.setStyleSheet("background-color: rgb(52, 101, 164);")
        self.copyClipboard.setObjectName("copyClipboard")
        self.horizontalLayout_2.addWidget(self.copyClipboard)
        self.exitPushButton = QtWidgets.QPushButton(Form)
        self.exitPushButton.setStyleSheet("background-color: rgb(204, 0, 0);")
        self.exitPushButton.setObjectName("exitPushButton")
        self.horizontalLayout_2.addWidget(self.exitPushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "KatalonImporter"))
        self.TextIn.setPlaceholderText(_translate("Form", "Input Text here ..."))
        self.TextOut.setPlaceholderText(_translate("Form", "Output Text"))
        self.savePushButton.setText(_translate("Form", "save"))
        self.copyClipboard.setText(_translate("Form", "Copy Clipboard"))
        self.exitPushButton.setText(_translate("Form", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

