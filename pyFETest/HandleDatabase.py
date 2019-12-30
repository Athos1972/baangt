import logging
import pandas as pd
import json
import pyFETest.CustGlobalConstants as CDC
import pyFETest.GlobalConstants as GC

logger = logging.getLogger("pyC")

class HandleDatabase():
    def __init__(self):
        self.lineNumber = 3
        self.globals = {
            'base_url':'portal-fqa',
            'user': '502266',
            'password': 'R(r6ayhr7EP3',
            'file_praemienauskunft': '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/Test_unterschrift_Beratungsprotokoll.pdf',
            CDC.CUST_TOASTS: "",
            CDC.CUST_TOASTS_ERROR: "",
            CDC.VIGOGFNUMMER: "",
            CDC.SAPPOLNR: "",
            CDC.PRAEMIE: "",
            CDC.POLNRHOST: ""
        }
        self.df_json = None

    def read_excel(self, fileName, sheetName):
        df = pd.read_excel(fileName,sheet_name=sheetName)
        self.df_json = df[["JSON"]].copy()

    def readTestRecord(self, lineNumber=None):
        if lineNumber:
            self.lineNumber = lineNumber
        else:
            self.lineNumber += 1

        self.record = json.loads(self.df_json["JSON"][self.lineNumber][1:-1])

        # Dirty hack, um bei Zahlen ein Komma und zwei Nachkommastellen einzugeben:
        for key, value in self.record.items():
            if value[:].isdigit() and key not in ["vermittler", "VN", "TFZeile", "dokumente", "geb_baujahr"]\
                    and "m2" not in key:
                logger.debug(f"Changed value - added ',00' to {key}, now value is: {value + ',00'} ")
                self.record[key] = value + ",00"

        self.globals[CDC.CUST_TOASTS] = ""
        self.globals[CDC.CUST_TOASTS_ERROR] = ""
        self.globals[CDC.DURATION] = ""
        self.globals[GC.TIMELOG] = ""

        self.record.update(self.globals)

        return self.record