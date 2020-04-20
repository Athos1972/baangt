# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from baangt.ui.ImportKatalonRecorder import ImportKatalonRecorder
from baangt.ui.pyqt.uiKatalonImporter import Ui_Form
import pyperclip
import os
import configparser


class PyqtKatalonUI(ImportKatalonRecorder):
    """ Subclass of ImportKatalonRecorder :
        Aim : To disable GUI created by PySimpleGui
        and initialize everything
    """
    def __init__(self, directory="./"):
        self.directory = directory
        self.clipboardText = ""
        self.outputText = ""
        self.window = None
        self.outputData = {}
        self.outputFormatted =[]
        self.fileNameExport = None



class KatalonUI(Ui_Form):
    def __init__(self, directory):
        Ui_Form.__init__(self)
        self.readConfig()
        self.katalonRecorder = PyqtKatalonUI(self.directory)

    def setupUi(self, Form):
        super().setupUi(Form)

        self.copyClipboard.clicked.connect(self.copyFromClipboard)
        self.TextIn.textChanged.connect(self.importClipboard)
        self.savePushButton.clicked.connect(self.saveTestCase)
        # self.exitPushButton.clicked.connect(self.quit)

    def readConfig(self):
        """ Read the baaangt.ini file """
        config = configparser.ConfigParser()
        try:
            config.read('baangt.ini')
            self.directory = config['Default']['path']
        except Exception as e:
            print("Exception in KatalonUI", e)
            self.directory = os.getcwd()
            pass

    @QtCore.pyqtSlot()
    def quit(self):
        """ Quit the Katalon UI"""
        QtWidgets.QApplication.exit()


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

    @QtCore.pyqtSlot()
    def importClipboard(self):
        """Extend: katalonRecorder.importClipboard internally """
        # ignore last line as this will result unexpected Index out of range error
        self.clipboardText = self.TextIn.toPlainText()
        self.katalonRecorder.clipboardText = "\n".join([
                              text for text in self.clipboardText.split("\n")
                              if len(text.split("|")) > 2
                              ])
        self.katalonRecorder.importClipboard()
        self.TextOut.setPlainText(self.katalonRecorder.outputText)

    @QtCore.pyqtSlot()
    def copyFromClipboard(self):
        """ Call ImportKatalonRecorder.importClipboard internally """
        self.TextIn.setPlainText(pyperclip.paste())
        self.importClipboard()





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = KatalonUI("./")
    ui.setupUi(Form)
    # ui.clipboardText = pyperclip.paste()
    # print(ui.importClipboard())
    # print(ui.outputText)
    Form.show()
    sys.exit(app.exec_())
    # print(ui.directory)
    # ui.clipboardText = pyperclip.paste()
    # print(ui.clipboardText)
    # ui.importClipboard()
    # print(ui.outputText)









