import logging
import pandas as pd
import json
import baangt.base.CustGlobalConstants as CGC
import baangt.base.GlobalConstants as GC

logger = logging.getLogger("pyC")


class HandleDatabase:
    def __init__(self, globalSettings=None):
        self.lineNumber = 3
        self.globals = {
            CGC.CUST_TOASTS: "",
            CGC.CUST_TOASTS_ERROR: "",
            CGC.VIGOGFNUMMER: "",
            CGC.SAPPOLNR: "",
            CGC.PRAEMIE: "",
            CGC.POLNRHOST: "",
            GC.TESTCASESTATUS: "",
            GC.TIMING_DURATION: "",
            GC.TIMELOG: ""
        }
        # FIXME: This is still not clean. GlobalSettings shouldn't be predefined in standard-Class
        if globalSettings:
            for setting, value in globalSettings.items():
                self.globals[setting] = value
        self.df_json = None

    def read_excel(self, fileName, sheetName):
        df = pd.read_excel(fileName, sheet_name=sheetName)
        self.df_json = df[["JSON"]].copy()

    def readTestRecord(self, lineNumber=None):
        if lineNumber:
            self.lineNumber = lineNumber
        else:
            self.lineNumber += 1

        try:
            record = json.loads(
                self.df_json["JSON"][self.lineNumber][1:-1])  # 1:-1 to remove leading and traling "]"
        except Exception as e:
            return None

        self.globals[CGC.CUST_TOASTS] = ""
        self.globals[CGC.CUST_TOASTS_ERROR] = ""
        self.globals[GC.TIMING_DURATION] = ""
        self.globals[GC.TIMELOG] = ""
        self.globals[GC.TESTCASESTATUS] = ""

        record.update(self.globals)

        return record