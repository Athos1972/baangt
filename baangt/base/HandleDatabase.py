import logging
import pandas as pd
import itertools
import json
import baangt.base.CustGlobalConstants as CGC
import baangt.base.GlobalConstants as GC
from baangt.base.utils import utils
import baangt.TestSteps.Exceptions
from pathlib import Path

logger = logging.getLogger("pyC")


class HandleDatabase:
    def __init__(self, globalSettings=None):
        self.lineNumber = 3
        # FIXME: This is still not clean. GlobalSettings shouldn't be predefined in CustomConstants-Class
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
        if globalSettings:
            for setting, value in globalSettings.items():
                self.globals[setting] = value
        self.df_json = None
        self.dataDict = {}

    def read_excel(self, fileName, sheetName):
        fileName = utils.findFileAndPathFromPath(fileName)
        if not fileName:
            logger.critical(f"Can't open file: {fileName}")
            return

        xl = pd.ExcelFile(fileName)
        ncols = xl.book.sheet_by_name(sheet_name=sheetName).ncols
        # Read all columns as strings:
        df = xl.parse(sheet_name=sheetName, converters={i: str for i in range(ncols)})

        # Set all Nan to empty String:
        df = df.where((pd.notnull(df)), '')
        # Create Dict of Header + item:
        self.dataDict = df.to_dict(orient="records")

    def readTestRecord(self, lineNumber=None):
        if lineNumber:
            self.lineNumber = lineNumber -1  # Base 0 vs. Base 1
        else:
            self.lineNumber += 1 # add 1 to read next line number

        try:
            record = self.dataDict[self.lineNumber]
            logger.info(f"Starting with Testrecord {self.lineNumber}, Details: " +
                        str({k: record[k] for k in list(record)[0:5]}))
            return self.updateGlobals(record)
        except Exception as e:
            logger.critical(f"Couldn't read record# {self.lineNumber}")

    def updateGlobals(self, record):

        self.globals[CGC.CUST_TOASTS] = ""
        self.globals[GC.TESTCASEERRORLOG] = ""
        self.globals[GC.TIMING_DURATION] = ""
        self.globals[GC.TIMELOG] = ""
        self.globals[GC.TESTCASESTATUS] = ""
        self.globals[GC.SCREENSHOTS] = ""

        record.update(self.globals)
        return record

    def readTestRecordOld(self, lineNumber=None):
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

        return self.updateGlobals(record)