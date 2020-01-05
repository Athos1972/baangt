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
            # 'base_url':'portal-fqa',
            # 'user': '502266',
            # 'password': 'R(r6ayhr7EP3',
            # 'file_praemienauskunft': '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/Test_unterschrift_Beratungsprotokoll.pdf',
            CGC.CUST_TOASTS: "",
            CGC.CUST_TOASTS_ERROR: "",
            CGC.VIGOGFNUMMER: "",
            CGC.SAPPOLNR: "",
            CGC.PRAEMIE: "",
            CGC.POLNRHOST: "",
            GC.TESTCASESTATUS: ""
        }
        # FIXME: This is still not clean. GlobalSettings shouldn't be predefined in standard-Class
        if globalSettings:
            for setting, value in globalSettings.items():
                self.globals[setting] = value
        self.df_json = None

    def read_excel(self, fileName, sheetName):
        df = pd.read_excel(fileName,sheet_name=sheetName)
        self.df_json = df[["JSON"]].copy()

    def readTestRecord(self, lineNumber=None):
        if lineNumber:
            self.lineNumber = lineNumber
        else:
            self.lineNumber += 1

        try:
            self.record = json.loads(self.df_json["JSON"][self.lineNumber][1:-1])  # 1:-1 to remove leading and traling "]"
        except Exception as e:
            return None

        # Dirty hack, um bei Zahlen ein Komma und zwei Nachkommastellen einzugeben:
        for key, value in self.record.items():
            if value[:].isdigit() and key not in ["vermittler", "VN", "TFZeile", "dokumente", "geb_baujahr"]\
                    and "m2" not in key:
                logger.debug(f"Changed value - added ',00' to {key}, now value is: {value + ',00'} ")
                self.record[key] = value + ",00"

        self.globals[CGC.CUST_TOASTS] = ""
        self.globals[CGC.CUST_TOASTS_ERROR] = ""
        self.globals[GC.TIMING_DURATION] = ""
        self.globals[GC.TIMELOG] = ""
        self.globals[GC.TESTCASESTATUS] = ""

        self.record.update(self.globals)

        return self.record