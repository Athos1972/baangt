import getopt
import sys
from baangt.base.TestRun import TestRun
from baangt.base.TestRunFromExcel import TestRunFromExcel


def args_read(l_search_parameter):
    l_args = sys.argv[1:]

    try:
        opts, args = getopt.getopt(l_args, "", ["testrun=",
                                                "testrunfile=",
                                                "configfile=",
                                                ""
                                                ])
    except getopt.GetoptError as err_det:
        print("Error in reading parameters:" + str(err_det))
        print_args()
        sys.exit("Abgebrochen wegen Fehler in Aufrufparametern")
    if opts:
        for opt, arg in opts:
            if l_search_parameter == opt:  # in ("-u", "--usage"):
                return arg
    return None


def print_args():
    print("""
Call: python baangt.py --parameters 
       --testrun=<Existing, predefined Name of a TestRun (database or name defined inside a TestRunClass>
       --testrunfile=<XLSX-File containing Testrun Definition>
       --configfile=<Filename and path to a configuration file, that holds all necessary data>

 Suggested for standard use:
   python baangt.py --testrun="Franzi4711": Will run a Testrun Franzi4711 that is known in the database
   python baangt.py --configfile="runProd.json": Will execute a Testrun as specified in runProd.json 
   """)


print_args()

