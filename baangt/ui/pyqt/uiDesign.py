# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import logging


class Ui_MainWindow(QtCore.QObject):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(920, 480)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(
                QtGui.QPixmap(":/new/logo/baangt/baangt/ressources/baangtIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(229, 222, 206); font: 75 11pt \"Arial\";")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(700, 0))
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.mainPage = QtWidgets.QWidget()
        self.mainPage.setObjectName("mainPage")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.mainPage)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_13.setContentsMargins(5, 5, 5, 10)
        self.horizontalLayout_13.setSpacing(15)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.mainGroupBox_4 = QtWidgets.QGroupBox(self.mainPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainGroupBox_4.sizePolicy().hasHeightForWidth())
        self.mainGroupBox_4.setSizePolicy(sizePolicy)
        self.mainGroupBox_4.setMinimumSize(QtCore.QSize(450, 0))
        self.mainGroupBox_4.setTitle("")
        self.mainGroupBox_4.setAlignment(QtCore.Qt.AlignCenter)
        self.mainGroupBox_4.setFlat(False)
        self.mainGroupBox_4.setObjectName("mainGroupBox_4")

        self.gridLayout_5 = QtWidgets.QGridLayout(self.mainGroupBox_4)
        self.gridLayout_5.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.gridLayout_5.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_5.setHorizontalSpacing(5)
        self.gridLayout_5.setVerticalSpacing(10)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setSpacing(20)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setSpacing(10)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.pathLabel_4 = QtWidgets.QLabel(self.mainGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pathLabel_4.sizePolicy().hasHeightForWidth())
        self.pathLabel_4.setSizePolicy(sizePolicy)
        self.pathLabel_4.setMinimumSize(QtCore.QSize(100, 0))
        self.pathLabel_4.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        font.setKerning(False)
        self.pathLabel_4.setFont(font)
        self.pathLabel_4.setStyleSheet("color: rgb(32, 74, 135);")
        self.pathLabel_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pathLabel_4.setObjectName("pathLabel_4")
        self.horizontalLayout_14.addWidget(self.pathLabel_4)
        self.pathLineEdit_4 = QtWidgets.QLineEdit(self.mainGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pathLineEdit_4.sizePolicy().hasHeightForWidth())
        self.pathLineEdit_4.setSizePolicy(sizePolicy)
        self.pathLineEdit_4.setMinimumSize(QtCore.QSize(250, 0))
        self.pathLineEdit_4.setMaximumSize(QtCore.QSize(500, 16777215))
        self.pathLineEdit_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pathLineEdit_4.setObjectName("pathLineEdit_4")
        self.horizontalLayout_14.addWidget(self.pathLineEdit_4)
        self.browsePushButton_4 = QtWidgets.QPushButton(self.mainGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browsePushButton_4.sizePolicy().hasHeightForWidth())
        self.browsePushButton_4.setSizePolicy(sizePolicy)
        self.browsePushButton_4.setMinimumSize(QtCore.QSize(90, 0))
        self.browsePushButton_4.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(114, 159, 207);")
        self.browsePushButton_4.setObjectName("browsePushButton_4")
        self.horizontalLayout_14.addWidget(self.browsePushButton_4)
        self.verticalLayout_8.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setSpacing(10)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.testRunLabel_4 = QtWidgets.QLabel(self.mainGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.testRunLabel_4.sizePolicy().hasHeightForWidth())
        self.testRunLabel_4.setSizePolicy(sizePolicy)
        self.testRunLabel_4.setMinimumSize(QtCore.QSize(100, 0))
        self.testRunLabel_4.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        font.setKerning(False)
        self.testRunLabel_4.setFont(font)
        self.testRunLabel_4.setStyleSheet("color: rgb(32, 74, 135);")
        self.testRunLabel_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.testRunLabel_4.setObjectName("testRunLabel_4")
        self.horizontalLayout_15.addWidget(self.testRunLabel_4)
        self.testRunComboBox_4 = QtWidgets.QComboBox(self.mainGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.testRunComboBox_4.sizePolicy().hasHeightForWidth())
        self.testRunComboBox_4.setSizePolicy(sizePolicy)
        self.testRunComboBox_4.setMinimumSize(QtCore.QSize(250, 0))
        self.testRunComboBox_4.setMaximumSize(QtCore.QSize(500, 16777215))
        self.testRunComboBox_4.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(46, 52, 54);")
        self.testRunComboBox_4.setMaxVisibleItems(20)
        self.testRunComboBox_4.setModelColumn(0)
        self.testRunComboBox_4.setObjectName("testRunComboBox_4")
        self.horizontalLayout_15.addWidget(self.testRunComboBox_4)
        self.executePushButton_4 = QtWidgets.QPushButton(self.mainGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.executePushButton_4.sizePolicy().hasHeightForWidth())
        self.executePushButton_4.setSizePolicy(sizePolicy)
        self.executePushButton_4.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(138, 226, 52);")

        self.executeIcon = QtGui.QIcon(":/baangt/executeicon")
        self.executePushButton_4.setIcon(self.executeIcon)
        self.executePushButton_4.setIconSize(QtCore.QSize(28, 20))
        self.executePushButton_4.setObjectName("executePushButton_4")
        self.horizontalLayout_15.addWidget(self.executePushButton_4)

        self.openTestFilePushButton_4 = QtWidgets.QPushButton(self.mainGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openTestFilePushButton_4.sizePolicy().hasHeightForWidth())
        self.openTestFilePushButton_4.setSizePolicy(sizePolicy)
        self.openTestFilePushButton_4.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(114, 159, 207);")
        self.openTestFilePushButton_4.setObjectName("openTestFilePushButton_4")
        self.openTestFileIcon = QtGui.QIcon(":/baangt/testfileicon")
        self.openTestFilePushButton_4.setIcon(self.openTestFileIcon)
        self.openTestFilePushButton_4.setIconSize(QtCore.QSize(28, 20))
        self.horizontalLayout_15.addWidget(self.openTestFilePushButton_4)
        self.verticalLayout_8.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setSpacing(10)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.settingLabel_4 = QtWidgets.QLabel(self.mainGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingLabel_4.sizePolicy().hasHeightForWidth())
        self.settingLabel_4.setSizePolicy(sizePolicy)
        self.settingLabel_4.setMinimumSize(QtCore.QSize(100, 0))
        self.settingLabel_4.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        font.setKerning(False)
        self.settingLabel_4.setFont(font)
        self.settingLabel_4.setStyleSheet("color: rgb(32, 74, 135);")
        self.settingLabel_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.settingLabel_4.setObjectName("settingLabel_4")
        self.horizontalLayout_16.addWidget(self.settingLabel_4)
        self.settingComboBox_4 = QtWidgets.QComboBox(self.mainGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingComboBox_4.sizePolicy().hasHeightForWidth())
        self.settingComboBox_4.setSizePolicy(sizePolicy)
        self.settingComboBox_4.setMinimumSize(QtCore.QSize(250, 0))
        self.settingComboBox_4.setMaximumSize(QtCore.QSize(500, 16777215))
        self.settingComboBox_4.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(46, 52, 54);")
        self.settingComboBox_4.setMaxVisibleItems(20)
        self.settingComboBox_4.setObjectName("settingComboBox_4")
        self.horizontalLayout_16.addWidget(self.settingComboBox_4)
        self.settingsPushButton_4 = QtWidgets.QPushButton(self.mainGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsPushButton_4.sizePolicy().hasHeightForWidth())
        self.settingsPushButton_4.setSizePolicy(sizePolicy)
        self.settingsPushButton_4.setMinimumSize(QtCore.QSize(90, 0))
        self.settingsPushButton_4.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(114, 159, 207);")
        self.settingsPushButton_4.setObjectName("settingsPushButton_4")
        self.horizontalLayout_16.addWidget(self.settingsPushButton_4)
        self.verticalLayout_8.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setSpacing(10)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.openResultFilePushButton_4 = QtWidgets.QPushButton(self.mainGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openResultFilePushButton_4.sizePolicy().hasHeightForWidth())
        self.openResultFilePushButton_4.setSizePolicy(sizePolicy)
        self.openResultFilePushButton_4.setMinimumSize(QtCore.QSize(90, 0))
        self.openResultFilePushButton_4.setStyleSheet("color: rgb(255, 255, 255);background-color: rgb(114, 159, 207);")
        self.openResultFilePushButton_4.setObjectName("openResultFilePushButton_4")
        self.horizontalLayout_20.addWidget(self.openResultFilePushButton_4)
        self.openLogFilePushButton_4 = QtWidgets.QPushButton(self.mainGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openLogFilePushButton_4.sizePolicy().hasHeightForWidth())
        self.openLogFilePushButton_4.setSizePolicy(sizePolicy)
        self.openLogFilePushButton_4.setMinimumSize(QtCore.QSize(90, 0))
        self.openLogFilePushButton_4.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(114, 159, 207);")
        self.openLogFilePushButton_4.setObjectName("openLogFilePushButton_4")
        self.horizontalLayout_20.addWidget(self.openLogFilePushButton_4)
        self.verticalLayout_8.addLayout(self.horizontalLayout_20)


        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setSpacing(10)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setSpacing(10)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.statisticTable = QtWidgets.QTableWidget(self.mainGroupBox_4)
        self.statisticTable.setRowCount(1)
        self.statisticTable.setColumnCount(9)
        self.statisticTable.setShowGrid(True)
        self.statisticTable.verticalHeader().hide()
        self.statisticTable.setStyleSheet("border: 0px;")
        headerFont = QtGui.QFont()
        headerFont.setPointSize(9)
        headerFont.setBold(True)
        header = self.statisticTable.horizontalHeader()
        headers = ["TC Total", "TC DONE", "TC Pending", "TC OK", "TC Failed", "TC Paused", "TCS", "TS", "TSS"]
        headers_fullform = [
            "Total TestCases", "TestCases Done", "TestCases Pending", "TestCases Succeed", "TestCases Failed",
            "TestCases Paused", "TestCase Sequence Done", "TestStep Done", "TestStep Sequence Done"]
        self.statisticTable.setFocusPolicy(QtCore.Qt.NoFocus)
        for x in range(9):
            self.statisticTable.setItem(0, x, QtWidgets.QTableWidgetItem())
            self.statisticTable.item(0,x).setBackground(QtGui.QBrush(QtCore.Qt.white))
            self.statisticTable.item(0, x).setFlags(self.statisticTable.item(0, x).flags() ^ QtCore.Qt.ItemIsSelectable)
            self.statisticTable.item(0, x).setFlags(self.statisticTable.item(0, x).flags() ^ QtCore.Qt.ItemIsEditable)
            header.setSectionResizeMode(x, QtWidgets.QHeaderView.Stretch)
            self.statisticTable.setHorizontalHeaderItem(x, QtWidgets.QTableWidgetItem(headers[x]))
            self.statisticTable.horizontalHeaderItem(x).setFont(headerFont)
            self.statisticTable.horizontalHeaderItem(x).setToolTip(headers_fullform[x])


        self.statisticTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.statisticTable.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_21.addWidget(self.statisticTable)
        self.logTextBox = QtWidgets.QPlainTextEdit(self.mainGroupBox_4)
        self.logTextBox.setStyleSheet("background-color: rgb(255, 255, 255); border: 1px solid black;")
        self.logTextBox.setReadOnly(True)
        self.horizontalLayout_22.addWidget(self.logTextBox)


        self.gridLayout_5.addLayout(self.verticalLayout_8, 0, 0, 0, 0)
        self.horizontalLayout_13.addWidget(self.mainGroupBox_4)
        self.logo_4 = QtWidgets.QLabel(self.mainPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo_4.sizePolicy().hasHeightForWidth())
        self.logo_4.setSizePolicy(sizePolicy)
        self.logo_4.setMinimumSize(QtCore.QSize(0, 0))
        self.logo_4.setMaximumSize(QtCore.QSize(300, 120))
        self.logo_4.setBaseSize(QtCore.QSize(600, 240))
        self.logo_4.setText("")
        self.logo_4.setPixmap(QtGui.QPixmap(":/new/logo/baangtLogo"))
        self.logo_4.setScaledContents(True)
        self.logo_4.setObjectName("logo_4")
        self.horizontalLayout_13.addWidget(self.logo_4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_13)
        self.verticalLayout_7.addLayout(self.horizontalLayout_21)
        self.verticalLayout_7.addLayout(self.horizontalLayout_22)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_7.addItem(spacerItem)
        self.gridLayout_6.addLayout(self.verticalLayout_7, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.mainPage)
        self.settingPage = QtWidgets.QWidget()
        self.settingPage.setObjectName("settingPage")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.settingPage)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.groupBox = QtWidgets.QGroupBox(self.settingPage)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 282, 144))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setSpacing(12)
        self.formLayout.setObjectName("formLayout")
        self.lineEdit1Label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lineEdit1Label.setToolTip("")
        self.lineEdit1Label.setObjectName("lineEdit1Label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lineEdit1Label)
        self.lineEdit1LineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit1LineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit1LineEdit.setSizePolicy(sizePolicy)
        self.lineEdit1LineEdit.setMinimumSize(QtCore.QSize(250, 0))
        self.lineEdit1LineEdit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(46, 52, 54);")
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
        self.comboBox1ComboBox.setStyleSheet("color: rgb(46, 52, 54); background-color: rgb(255, 255, 255);")
        self.comboBox1ComboBox.setObjectName("comboBox1ComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox1ComboBox)
        self.verticalLayout_10.addLayout(self.formLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_9.addWidget(self.scrollArea)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.okPushButton = QtWidgets.QPushButton(self.groupBox)
        self.okPushButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(52, 101, 164);")
        self.okPushButton.setObjectName("okPushButton")
        self.horizontalLayout_17.addWidget(self.okPushButton)
        self.saveAspushButton = QtWidgets.QPushButton(self.groupBox)
        self.saveAspushButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(52, 101, 164);")
        self.saveAspushButton.setObjectName("saveAspushButton")
        self.horizontalLayout_17.addWidget(self.saveAspushButton)
        self.AddMorePushButton = QtWidgets.QPushButton(self.groupBox)
        self.AddMorePushButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(115, 210, 22);")
        self.AddMorePushButton.setObjectName("AddMorePushButton")
        self.horizontalLayout_17.addWidget(self.AddMorePushButton)
        self.deleteLastPushButton = QtWidgets.QPushButton(self.groupBox)
        self.deleteLastPushButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(204, 0, 0);")
        self.deleteLastPushButton.setObjectName("deleteLastPushButton")
        self.horizontalLayout_17.addWidget(self.deleteLastPushButton)
        self.exitPushButton = QtWidgets.QPushButton(self.groupBox)
        self.exitPushButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(204, 0, 0);")
        self.exitPushButton.setObjectName("exitPushButton")
        self.horizontalLayout_17.addWidget(self.exitPushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem1)
        self.verticalLayout_9.addLayout(self.horizontalLayout_17)
        self.gridLayout_7.addWidget(self.groupBox, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.settingPage)
        self.katalonPage = QtWidgets.QWidget()
        self.katalonPage.setObjectName("katalonPage")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.katalonPage)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setSpacing(20)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.TextIn_2 = QtWidgets.QPlainTextEdit(self.katalonPage)
        self.TextIn_2.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self.TextIn_2.setObjectName("TextIn_2")
        self.horizontalLayout_18.addWidget(self.TextIn_2)
        self.TextOut_2 = QtWidgets.QPlainTextEdit(self.katalonPage)
        self.TextOut_2.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self.TextOut_2.setObjectName("TextOut_2")
        self.horizontalLayout_18.addWidget(self.TextOut_2)
        self.verticalLayout_11.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setSpacing(15)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.savePushButton_2 = QtWidgets.QPushButton(self.katalonPage)
        self.savePushButton_2.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(255, 255, 255);")
        self.savePushButton_2.setObjectName("savePushButton_2")
        self.horizontalLayout_19.addWidget(self.savePushButton_2)
        self.copyClipboard_2 = QtWidgets.QPushButton(self.katalonPage)
        self.copyClipboard_2.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(255, 255, 255);")
        self.copyClipboard_2.setObjectName("copyClipboard_2")
        self.horizontalLayout_19.addWidget(self.copyClipboard_2)
        self.exitPushButton_3 = QtWidgets.QPushButton(self.katalonPage)
        self.exitPushButton_3.setStyleSheet("background-color: rgb(204, 0, 0); color: rgb(255, 255, 255);")
        self.exitPushButton_3.setObjectName("exitPushButton_3")
        self.horizontalLayout_19.addWidget(self.exitPushButton_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem2)
        self.verticalLayout_11.addLayout(self.horizontalLayout_19)
        self.gridLayout_8.addLayout(self.verticalLayout_11, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.katalonPage)
        self.gridLayout_3.addWidget(self.stackedWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        self.toolBar.setFont(font)
        self.toolBar.setStyleSheet("font: 63 11pt \"Arial\";")
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionImport_Katalon = QtWidgets.QAction(MainWindow)
        self.actionImport_Katalon.setObjectName("actionImport_Katalon")
        self.toolBar.addAction(self.actionImport_Katalon)
        self.toolBar.addAction(self.actionExit)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def close(self,event):
        self.child.terminate()
        self.child.waitForFinished()
        event.accept()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Baangt Interactive Starter"))
        self.pathLabel_4.setText(_translate("MainWindow", "Path"))
        self.browsePushButton_4.setText(_translate("MainWindow", "Browse"))
        self.testRunLabel_4.setText(_translate("MainWindow", "Test Run"))
        self.settingLabel_4.setText(_translate("MainWindow", "Settings"))
        self.settingsPushButton_4.setText(_translate("MainWindow", "Details"))
        self.groupBox.setTitle(_translate("MainWindow", "Settings in globals.json"))
        self.lineEdit1Label.setText(_translate("MainWindow", "lineEdit1"))
        self.checkBox1Label.setText(_translate("MainWindow", "checkBox1"))
        self.comboBox1Label.setText(_translate("MainWindow", "comboBox1"))
        self.okPushButton.setToolTip(_translate("MainWindow", "Save to Current File and Close Window"))
        self.okPushButton.setText(_translate("MainWindow", "Ok"))
        self.saveAspushButton.setToolTip(_translate("MainWindow", "Save to New File Name"))
        self.saveAspushButton.setText(_translate("MainWindow", "Save As"))
        self.AddMorePushButton.setToolTip(_translate("MainWindow", "Add Entry To Bottom"))
        self.AddMorePushButton.setText(_translate("MainWindow", "Add More"))
        self.deleteLastPushButton.setToolTip(_translate("MainWindow", "Delete Last Entry"))
        self.deleteLastPushButton.setText(_translate("MainWindow", "Delete Last"))
        self.exitPushButton.setToolTip(_translate("MainWindow", "Discard Unsaved Changes and Close"))
        self.exitPushButton.setText(_translate("MainWindow", "Exit"))
        self.TextIn_2.setPlaceholderText(_translate("MainWindow", "Input Text here ..."))
        self.TextOut_2.setPlaceholderText(_translate("MainWindow", "Output Text"))
        self.savePushButton_2.setText(_translate("MainWindow", "Save"))
        self.copyClipboard_2.setText(_translate("MainWindow", "Copy Clipboard"))
        self.exitPushButton_3.setText(_translate("MainWindow", "Exit"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionImport_Katalon.setText(_translate("MainWindow", "Import Katalon"))
        self.actionImport_Katalon.setToolTip(_translate("MainWindow", "Import Katalon studio"))

        self.openResultFilePushButton_4.setText(_translate("MainWindow", "Result File"))
        self.openLogFilePushButton_4.setText(_translate("MainWindow", "Log File"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

