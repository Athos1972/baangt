import sys, getopt
from baangt.base.utils import utils
from baangt.ui.ui import UI
from baangt import plugin_manager

def print_args():
    print("""
Call: python baangt.py --parameters 
       --run=<Existing, predefined Name of a TestRun (XLSX or .JSON-File incl. Path)>
       --globals=<path to JSON-File containing global Settings. If omitted, will look for globals.json in the current directory>

 Suggested for standard use:
   python baangt.py --run="Franzi4711.xlsx": Will run a Testrun Franzi4711.xlsx
   python baangt.py --run="runProducts.json": Will execute a Testrun as specified in runProducts.json and use default globals.json, if exists
   python baangt.py --run="runProducts.json" --globals="production.json" will use settings in production.json
   python baangt.py --run="runProducts.json" --globals="qa.json" will use settings in qa.json
   
   If run without parameters you'll find a simple interactive Window
   """)

def args_read(l_search_parameter):
    l_args = sys.argv[1:]

    try:
        opts, args = getopt.getopt(l_args, "", ["run=",
                                                "globals="
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
        callTestrun(testRunFile)
    else:
        UI()




