import logging
import pandas as pd
import json

logger = logging.getLogger("pyC")


class HandleDatabase():
    def __init__(self):
        self.lineNumber = 3
        self.globals = {
            'base_url':'portal-fqa',
            'user': '502266',
            'password': 'R(r6ayhr7EP3',
            'file_praemienauskunft': '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/Test_unterschrift_Beratungsprotokoll.pdf'
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

        self.record.update(self.globals)

        return self.record