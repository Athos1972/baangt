import logging
import pandas as pd
import itertools
import json
import baangt.base.CustGlobalConstants as CGC
import baangt.base.GlobalConstants as GC
from baangt.base.Utils import utils
import baangt.TestSteps.Exceptions
from pathlib import Path

logger = logging.getLogger("pyC")


class HandleDatabase:
    def __init__(self, linesToRead, globalSettings=None):
        self.lineNumber = 3
        # FIXME: This is still not clean. GlobalSettings shouldn't be predefined in CustomConstants-Class
        self.globals = {
            CGC.CUST_TOASTS: "",
            GC.TESTCASEERRORLOG: "",
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
        self.range = self.__buildRangeOfRecords(linesToRead)
        self.rangeDict = {}
        self.__buildRangeDict()
        self.df_json = None
        self.dataDict = {}
        self.recordPointer = 0

    def __buildRangeDict(self):
        """
        Interprets the Range and creates a DICT of values, that we can loop over later

        @return: Creates empty self.rangeDict
        """
        for lRangeLine in self.range:
            for x in range(lRangeLine[0], lRangeLine[1]+1):
                self.rangeDict[x] = ""

    def __buildRangeOfRecords(self, rangeFromConfigFile):
        lRange = []
        if not rangeFromConfigFile:
            # No selection - means all records
            return [[0,9999]]
        else:
            # Format: 4;6-99;17-200;203
            if ";" in rangeFromConfigFile:
                for kombination in rangeFromConfigFile.split(";"):
                    lRange.append(HandleDatabase.__buildRangeOfRecordsOneEntry(kombination))
                    pass
            else:
                lRange.append(HandleDatabase.__buildRangeOfRecordsOneEntry(rangeFromConfigFile))

        # Make sure these are numbers:
        for lRangeLine in lRange:
            lRangeLine[0] = HandleDatabase.__sanitizeNumbers(lRangeLine[0])
            lRangeLine[1] = HandleDatabase.__sanitizeNumbers(lRangeLine[1])

        return lRange

    @staticmethod
    def __sanitizeNumbers(numberIn):
        numberIn = numberIn.strip()
        return int(numberIn)

    @staticmethod
    def __buildRangeOfRecordsOneEntry(rangeIn):
        if "-" in rangeIn:
            # This is a range (17-22)
            return HandleDatabase.__buildRangeOfRecordsSingleRange(rangeIn)
        else:
            # This is a single entry:
            return [rangeIn, rangeIn]

    @staticmethod
    def __buildRangeOfRecordsSingleRange(rangeIn):
        lSplit = rangeIn.split("-")
        return [lSplit[0], lSplit[1]]

    def read_excel(self, fileName, sheetName):
        fileName = utils.findFileAndPathFromPath(fileName)
        if not fileName:
            logger.critical(f"Can't open file: {fileName}")
            return

        # FIXME: Sooner or later replace Pandas with direct XLSX-Import
        xl = pd.ExcelFile(fileName)
        ncols = xl.book.sheet_by_name(sheet_name=sheetName).ncols
        # Read all columns as strings:
        df = xl.parse(sheet_name=sheetName, converters={i: str for i in range(ncols)})

        # Set all Nan to empty String:
        df = df.where((pd.notnull(df)), '')
        # Create Dict of Header + item:
        self.dataDict = df.to_dict(orient="records")

    def readNextRecord(self):
        """
        We built self.range during init. Now we need to iterate over the range(s) in range,
        find appropriate record and return that - one at a time

        @return:
        """
        if len(self.rangeDict) == 0:
            # All records were processed
            return None
        try:
            # the topmost record of the RangeDict (RangeDict was built by the range(s) from the TestRun
            # - 1 because there's a header line in the Excel-Sheet.
            lRecord = self.dataDict[(list(self.rangeDict.keys())[0])-1]
        except Exception as e:
            logger.debug(f"Couldn't read record from database: {list(self.rangeDict.keys())[0]}")
            self.rangeDict.pop(list(self.rangeDict.keys())[0])
            return None

        self.rangeDict.pop(list(self.rangeDict.keys())[0])
        return self.updateGlobals(lRecord)

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
