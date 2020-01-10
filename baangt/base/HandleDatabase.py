import logging
import pandas as pd
import itertools
import json
import baangt.base.CustGlobalConstants as CGC
import baangt.base.GlobalConstants as GC

logger = logging.getLogger("pyC")


class HandleDatabase:
    def __init__(self, globalSettings=None):
        self.lineNumber = 3
        self.globals = {
            CGC.CUST_TOASTS: "",
            GC.TESTCASEERRORLOG: "",
            # CGC.CUST_TOASTS_ERROR: "", # Replaced by GC.TESTCASEERRORLOG
            CGC.VIGOGFNUMMER: "",
            CGC.SAPPOLNR: "",
            CGC.PRAEMIE: "",
            CGC.POLNRHOST: "",
            GC.TESTCASESTATUS: "",
            GC.TIMING_DURATION: "",
            GC.SCREENSHOTS: "",
            GC.TIMELOG: ""
        }
        # FIXME: This is still not clean. GlobalSettings shouldn't be predefined in CustomConstants-Class
        if globalSettings:
            for setting, value in globalSettings.items():
                self.globals[setting] = value
        self.df_json = None

    def read_excel(self, fileName, sheetName):
        df = pd.read_excel(fileName, sheet_name=sheetName)
        self.df_json = df[["JSON"]].copy()

    def readTestRecord(self, lineNumber=None):
        if lineNumber:
            self.lineNumber = lineNumber - 1 # -1 for Header-File
        else:
            self.lineNumber += 1

        try:
            record=None
            record = json.loads(
                self.df_json["JSON"][self.lineNumber][1:-1])  # 1:-1 to remove leading and traling "]"
            logger.info(f"Starting with Testrecord {lineNumber}, Details: " +
                        str({k: record[k] for k in list(record)[0:5]}))
        except Exception as e:
            logger.critical(f"Couldn't read record# {self.lineNumber}")
            return None

        self.globals[CGC.CUST_TOASTS] = ""
        self.globals[GC.TESTCASEERRORLOG] = ""
        # self.globals[CGC.CUST_TOASTS_ERROR] = "" Replaced by GC.TESTCASEEROROG
        self.globals[GC.TIMING_DURATION] = ""
        self.globals[GC.TIMELOG] = ""
        self.globals[GC.TESTCASESTATUS] = ""
        self.globals[GC.SCREENSHOTS] = ""

        record.update(self.globals)

        return record