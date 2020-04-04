# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
import os

class Ui_MainWindow(QObject):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(926, 480)
        icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("./baangt/ressources/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(os.path.join("baangt","ressources","favicon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(229, 222, 206);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(700, 0))
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.mainAndExtraSplitter = QtWidgets.QSplitter(self.centralwidget)
        self.mainAndExtraSplitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mainAndExtraSplitter.setOrientation(QtCore.Qt.Vertical)
        self.mainAndExtraSplitter.setHandleWidth(20)
        self.mainAndExtraSplitter.setObjectName("mainAndExtraSplitter")
        self.widget = QtWidgets.QWidget(self.mainAndExtraSplitter)
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.mainGroupBox = QtWidgets.QGroupBox(self.widget)
        self.mainGroupBox.setTitle("")
        self.mainGroupBox.setObjectName("mainGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.mainGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pathLabel = QtWidgets.QLabel(self.mainGroupBox)
        self.pathLabel.setMinimumSize(QtCore.QSize(70, 0))
        self.pathLabel.setMaximumSize(QtCore.QSize(70, 16777215))
        self.pathLabel.setStyleSheet("color: rgb(32, 74, 135);")
        self.pathLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pathLabel.setObjectName("pathLabel")
        self.horizontalLayout.addWidget(self.pathLabel)
        self.pathLineEdit = QtWidgets.QLineEdit(self.mainGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pathLineEdit.sizePolicy().hasHeightForWidth())
        self.pathLineEdit.setSizePolicy(sizePolicy)
        self.pathLineEdit.setMinimumSize(QtCore.QSize(100, 0))
        self.pathLineEdit.setMaximumSize(QtCore.QSize(300, 16777215))
        self.pathLineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pathLineEdit.setObjectName("pathLineEdit")
        self.horizontalLayout.addWidget(self.pathLineEdit)
        self.browsePushButton = QtWidgets.QPushButton(self.mainGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browsePushButton.sizePolicy().hasHeightForWidth())
        self.browsePushButton.setSizePolicy(sizePolicy)
        self.browsePushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(114, 159, 207);")
        self.browsePushButton.setObjectName("browsePushButton")
        self.horizontalLayout.addWidget(self.browsePushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.testRunLabel = QtWidgets.QLabel(self.mainGroupBox)
        self.testRunLabel.setMinimumSize(QtCore.QSize(70, 0))
        self.testRunLabel.setMaximumSize(QtCore.QSize(70, 16777215))
        self.testRunLabel.setStyleSheet("color: rgb(32, 74, 135);")
        self.testRunLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.testRunLabel.setObjectName("testRunLabel")
        self.horizontalLayout_2.addWidget(self.testRunLabel)
        self.testRunComboBox = QtWidgets.QComboBox(self.mainGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.testRunComboBox.sizePolicy().hasHeightForWidth())
        self.testRunComboBox.setSizePolicy(sizePolicy)
        self.testRunComboBox.setMinimumSize(QtCore.QSize(100, 0))
        self.testRunComboBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.testRunComboBox.setStyleSheet("background-color: rgb(255, 255, 255); color: black;")
        self.testRunComboBox.setObjectName("testRunComboBox")
        self.horizontalLayout_2.addWidget(self.testRunComboBox)
        self.executePushButton = QtWidgets.QPushButton(self.mainGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.executePushButton.sizePolicy().hasHeightForWidth())
        self.executePushButton.setSizePolicy(sizePolicy)
        self.executePushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(138, 226, 52);")
        self.executePushButton.setObjectName("executePushButton")
        self.horizontalLayout_2.addWidget(self.executePushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.settingLabel = QtWidgets.QLabel(self.mainGroupBox)
        self.settingLabel.setMinimumSize(QtCore.QSize(70, 0))
        self.settingLabel.setMaximumSize(QtCore.QSize(70, 16777215))
        self.settingLabel.setStyleSheet("color: rgb(32, 74, 135);")
        self.settingLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.settingLabel.setObjectName("settingLabel")
        self.horizontalLayout_3.addWidget(self.settingLabel)
        self.settingComboBox = QtWidgets.QComboBox(self.mainGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingComboBox.sizePolicy().hasHeightForWidth())
        self.settingComboBox.setSizePolicy(sizePolicy)
        self.settingComboBox.setMinimumSize(QtCore.QSize(100, 0))
        self.settingComboBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.settingComboBox.setStyleSheet("background-color: rgb(255, 255, 255); color: black;")
        self.settingComboBox.setObjectName("settingComboBox")
        self.horizontalLayout_3.addWidget(self.settingComboBox)
        self.settingsPushButton = QtWidgets.QPushButton(self.mainGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsPushButton.sizePolicy().hasHeightForWidth())
        self.settingsPushButton.setSizePolicy(sizePolicy)
        self.settingsPushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(114, 159, 207);")
        self.settingsPushButton.setObjectName("settingsPushButton")
        self.horizontalLayout_3.addWidget(self.settingsPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout_4.addWidget(self.mainGroupBox)
        self.logo = QtWidgets.QLabel(self.widget)
        self.logo.setMinimumSize(QtCore.QSize(400, 200))
        self.logo.setMaximumSize(QtCore.QSize(400, 200))
        self.logo.setText("")
        # self.logo.setPixmap(QtGui.QPixmap("./baangt/ressources/baangtLogo2020.png"))
        self.logo.setPixmap(QtGui.QPixmap(os.path.join("baangt","ressources","baangtLogo2020.png")))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.horizontalLayout_4.addWidget(self.logo)
        self.settingsAndLogSplitter = QtWidgets.QSplitter(self.mainAndExtraSplitter)
        self.settingsAndLogSplitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.settingsAndLogSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.settingsAndLogSplitter.setHandleWidth(20)
        self.settingsAndLogSplitter.setObjectName("settingsAndLogSplitter")
        self.settingsGroupBox = QtWidgets.QGroupBox(self.settingsAndLogSplitter)
        self.settingsGroupBox.setStyleSheet("color: rgb(32, 74, 135);")
        self.settingsGroupBox.setObjectName("settingsGroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.settingsGroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.settingsTableWidget = QtWidgets.QTableWidget(self.settingsGroupBox)
        self.settingsTableWidget.setBaseSize(QtCore.QSize(0, 0))
        self.settingsTableWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.settingsTableWidget.setLineWidth(200)
        self.settingsTableWidget.setRowCount(15)
        self.settingsTableWidget.setObjectName("settingsTableWidget")
        self.settingsTableWidget.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.settingsTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.settingsTableWidget.setHorizontalHeaderItem(1, item)
        self.settingsTableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.settingsTableWidget.horizontalHeader().setMinimumSectionSize(150)
        self.settingsTableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.settingsTableWidget)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.settingsSavePushButton = QtWidgets.QPushButton(self.settingsGroupBox)
        self.settingsSavePushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
" \n"
"background-color: rgb(114, 159, 207);")
        self.settingsSavePushButton.setObjectName("settingsSavePushButton")
        self.horizontalLayout_5.addWidget(self.settingsSavePushButton)
        self.settingsSaveAsPushButton = QtWidgets.QPushButton(self.settingsGroupBox)
        self.settingsSaveAsPushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
" \n"
"background-color: rgb(114, 159, 207);")
        self.settingsSaveAsPushButton.setObjectName("settingsSaveAsPushButton")
        self.horizontalLayout_5.addWidget(self.settingsSaveAsPushButton)
        self.settingsClosePushButton = QtWidgets.QPushButton(self.settingsGroupBox)
        self.settingsClosePushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(239, 41, 41);")
        self.settingsClosePushButton.setObjectName("settingsClosePushButton")
        self.horizontalLayout_5.addWidget(self.settingsClosePushButton)
        spacerItem = QtWidgets.QSpacerItem(58, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.logsGroupBox = QtWidgets.QGroupBox(self.settingsAndLogSplitter)
        self.logsGroupBox.setStyleSheet("color: rgb(32, 74, 135);")
        self.logsGroupBox.setObjectName("logsGroupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.logsGroupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.logsPlainTextEdit = QtWidgets.QPlainTextEdit(self.logsGroupBox)
        self.logsPlainTextEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.logsPlainTextEdit.setObjectName("logsPlainTextEdit")
        self.verticalLayout_3.addWidget(self.logsPlainTextEdit)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.LogsClosePushButton = QtWidgets.QPushButton(self.logsGroupBox)
        self.LogsClosePushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(239, 41, 41);")
        self.LogsClosePushButton.setObjectName("LogsClosePushButton")
        self.horizontalLayout_6.addWidget(self.LogsClosePushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.mainAndExtraSplitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 926, 25))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuPreferences = QtWidgets.QMenu(self.menuFile)
        self.menuPreferences.setObjectName("menuPreferences")
        self.menuImport = QtWidgets.QMenu(self.menubar)
        self.menuImport.setObjectName("menuImport")
        self.menuKatalon_Importer = QtWidgets.QMenu(self.menuImport)
        self.menuKatalon_Importer.setObjectName("menuKatalon_Importer")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionsettings = QtWidgets.QAction(MainWindow)
        self.actionsettings.setObjectName("actionsettings")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionCopy_Ctrl_C = QtWidgets.QAction(MainWindow)
        self.actionCopy_Ctrl_C.setObjectName("actionCopy_Ctrl_C")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuPreferences.addAction(self.actionsettings)
        self.menuFile.addAction(self.menuPreferences.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menuKatalon_Importer.addAction(self.actionCopy_Ctrl_C)
        self.menuKatalon_Importer.addAction(self.actionPaste)
        self.menuKatalon_Importer.addAction(self.actionSave)
        self.menuImport.addAction(self.menuKatalon_Importer.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuImport.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Baangt Interactive Starter"))
        self.pathLabel.setText(_translate("MainWindow", "Path"))
        self.browsePushButton.setText(_translate("MainWindow", "Browse"))
        self.testRunLabel.setText(_translate("MainWindow", "Test Run"))
        self.executePushButton.setText(_translate("MainWindow", "Execute"))
        self.settingLabel.setText(_translate("MainWindow", "Settings"))
        self.settingsPushButton.setText(_translate("MainWindow", "Details"))
        self.settingsGroupBox.setTitle(_translate("MainWindow", "Settings in Globals.json"))
        item = self.settingsTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Parameters"))
        item = self.settingsTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Values"))
        self.settingsSavePushButton.setText(_translate("MainWindow", "Save"))
        self.settingsSaveAsPushButton.setText(_translate("MainWindow", "Save As"))
        self.settingsClosePushButton.setText(_translate("MainWindow", "Close"))
        self.logsGroupBox.setTitle(_translate("MainWindow", "Execution Logs"))
        self.LogsClosePushButton.setText(_translate("MainWindow", "close"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuPreferences.setTitle(_translate("MainWindow", "Preferences"))
        self.menuImport.setTitle(_translate("MainWindow", "Import"))
        self.menuKatalon_Importer.setTitle(_translate("MainWindow", "Katalon Importer"))
        self.actionsettings.setText(_translate("MainWindow", "settings"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionCopy_Ctrl_C.setText(_translate("MainWindow", "Copy"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionSave.setText(_translate("MainWindow", "Save"))

# import baangtResource_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

