import sys, getopt
from baangt.base.Utils import utils
# from baangt.ui.ui import UI
from baangt import plugin_manager
import baangt.base.GlobalConstants as GC
from PyQt5 import QtWidgets
# from baangt.ui.pyqt.uimain import MainWindow
from baangt.ui.pyqt.uimain import MainController
from baangt.base.RuntimeStatistics import Statistic
def print_args():
    print("""
Call: python baangtIA.py --parameters 
       --run=<Existing, predefined Name of a TestRun (XLSX or .JSON-File incl. Path)>
       --globals=<path to JSON-File containing global Settings. If omitted, will look for globals.json in the current directory>
       --reloadDrivers=<anyValue> : This command will replace existing browser drivers (Chrome/Firefox) with latest versions

 Suggested for standard use:
   python baangtIA.py --run="Franzi4711.xlsx": Will run a Testrun Franzi4711.xlsx
   python baangtIA.py --run="runProducts.json": Will execute a Testrun as specified in runProducts.json and use default globals.json, if exists
   python baangtIA.py --run="runProducts.json" --globals="production.json" will use settings in production.json
   python baangtIA.py --run="runProducts.json" --globals="qa.json" will use settings in qa.json
   
   If run without parameters you'll find a simple interactive Window
   """)

def args_read(l_search_parameter):
    l_args = sys.argv[1:]

    try:
        opts, args = getopt.getopt(l_args, "", ["run=",
                                                "globals=",
                                                "reloadDrivers=",
                                                "gui="
                                                ])
    except getopt.GetoptError as err_det:
        print("Error in reading parameters:" + str(err_det))
        print_args()
        sys.exit("Wrong parameters - exiting")
    if opts:
        for opt, arg in opts:
            if l_search_parameter == opt:  # in ("-u", "--usage"):
                return arg
            if "--" + l_search_parameter == opt:
                return arg
    return None


def getGlobalSettings():
    lGlobals = args_read("globals")
    if not lGlobals:
        lGlobals = "globals.json"
    return lGlobals


def callTestrun(testRunFile):
    if ".XLSX" in testRunFile.upper() or ".JSON" in testRunFile.upper():

        plugin_manager.hook.testRun_init(testRunName=utils.sanitizeFileName(testRunFile),
                                         globalSettingsFileNameAndPath=utils.sanitizeFileName(getGlobalSettings()))

    else:
        sys.exit(f"Unknown Filetype - should be XLSX or JSON: {testRunFile}")

def run():

    print_args()

    testRunFile = args_read("run")
    if testRunFile:
        print(f"Starting Testrun: {testRunFile}")
        if args_read("gui"):
            s = Statistic()
            s.gui = True
        callTestrun(testRunFile)
    elif args_read("reloadDrivers"):
        from baangt.base.BrowserHandling.BrowserHandling import BrowserDriver
        lDriver = BrowserDriver()
        lDriver.downloadDriver(GC.BROWSER_FIREFOX)
        lDriver.downloadDriver(GC.BROWSER_CHROME)
        print("Latest versions of drivers for Firefox and Chrome were downloaded")
    else:
        app = QtWidgets.QApplication(sys.argv)
        controller = MainController()
        controller.show_main()
        sys.exit(app.exec_())




