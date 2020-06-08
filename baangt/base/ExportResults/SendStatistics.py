import json
import logging
import requests
from dataclasses import dataclass, asdict


logger = logging.getLogger("pyC")


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class Statistics(metaclass=Singleton):
    # TestCaseType
    Browser: int = 0
    api: int = 0
    soap: int = 0
    web: int = 0

    SequenceClass: str = ""
    TestCaseExecuted: int = 0
    TestCasePassed: int = 0
    TestCaseFailed: int = 0
    TestCasePaused: int = 0
    TestCaseClass: str = ""
    # Activity
    Activity_GOTOURL: int = 0
    Activity_SETTEXT: int = 0
    Activity_SETTEXTIF: int = 0
    Activity_FORCETEXT: int = 0
    Activity_SETANCHOR: int = 0
    Activity_HANDLEIFRAME: int = 0
    Activity_SWITCHWINDOW: int = 0
    Activity_CLICK: int = 0
    Activity_CLICKIF: int = 0
    Activity_PAUSE: int = 0
    Activity_IF: int = 0
    Activity_ENDIF: int = 0
    Activity_GOBACK: int = 0
    Activity_APIURL: int = 0
    Activity_ENDPOINT: int = 0
    Activity_POST: int = 0
    Activity_GET: int = 0
    Activity_HEADER: int = 0
    Activity_SAVE: int = 0
    Activity_CLEAR: int = 0
    Activity_SAVETO: int = 0
    Activity_SUBMIT: int = 0
    Activity_ADDRESS_CREATE: int = 0
    Activity_ASSERT: int = 0
    Activity_IBAN: int = 0
    Activity_PDFCOMPARE: int = 0
    Activity_CHECKLINKS: int = 0
    Activity_ALERTIF: int = 0
    # LocatorType
    XPATH: int = 0
    CSS: int = 0
    ID: int = 0
    # Comparision
    equalTo: int = 0
    notEqualTo: int = 0
    greaterThan: int = 0
    smallerThan: int = 0
    # Non-empty Values count
    timeout: int = 0
    optional: int = 0
    release: int = 0
    Duration: str = ""
    TestRunUUID: str = ""
    comparision_dict = {"=": "equalTo", "!=": "notEqualTo", ">": "greaterThan", "<": "smallerThan"}

    def update_data(self, dic):
        self.SequenceClass = Statistics.get_value(dic, "SequenceClass")
        self.TestCaseClass = Statistics.get_value(dic, "TestCaseClass")
        TestCaseType = Statistics.get_value(dic, "TestCaseType")
        TestStep = Statistics.get_value(dic, "TestStepExecutionParameters")

        if len(TestCaseType) > 0:
            self.update_attribute(TestCaseType)

        if len(self.SequenceClass) == 0:
            try:
                self.SequenceClass = Statistics.get_value(dic, "TESTSEQUENCE")[1][0]
            except KeyError:
                try:
                    self.SequenceClass = Statistics.get_value(dic, "TESTSEQUENCE")['1'][0]
                except KeyError:
                    pass

        if len(self.TestCaseClass) == 0:
            try:
                self.TestCaseClass = Statistics.get_value(dic, "TESTCASE")[1][0]
            except KeyError:
                try:
                    self.TestCaseClass = Statistics.get_value(dic, "TESTCASE")['1'][0]
                except KeyError:
                    pass

        for key in TestStep:
            self.update_attribute(TestStep[key]["Activity"].upper(), prefix="Activity_")
            if len(TestStep[key]["LocatorType"]) > 0:
                self.update_attribute(TestStep[key]["LocatorType"].upper())
            if len(TestStep[key]["Comparison"]) > 0:
                self.update_attribute(self.comparision_dict[TestStep[key]["Comparison"]])
            if len(str(TestStep[key]["Timeout"])) > 0:
                self.update_attribute("timeout")
            if len(TestStep[key]["Optional"]) > 0:
                self.update_attribute("optional")
            if len(TestStep[key]["Release"]) > 0:
                self.update_attribute("release")


    def update_attribute(self, string, prefix=""):
        string = prefix+string
        var = getattr(self, string)
        var += 1
        setattr(self, string, var)

    def update_attribute_with_value(self, string, value):
        setattr(self, string, value)

    def to_dict(self):
        removeable = []
        dic = asdict(self)
        for key in dic:
            if key[0] == "-":
                continue
            if dic[key] == 0 or dic[key] == "":
                removeable.append(key)
        for key in removeable:
            del dic[key]
        return dic

    def send_statistics(self, test=False):
        payload = self.to_dict()
        res = requests.post("https://stats.baangt.org", json=payload)
        if test:
            return res
        logger.debug(f"Statistics sent to server = {json.dumps(payload)}")

    @staticmethod
    def recursive_items(dictionary):
        for key, value in dictionary.items():
            if type(value) is dict:
                yield key, value
                yield from Statistics.recursive_items(value)
            if type(value) is list:
                yield key, value
                for val in value:
                    if type(val) is dict:
                        yield from Statistics.recursive_items(val)
            else:
                yield key, value

    @staticmethod
    def get_value(dictionary, get_key):
        for key, value in Statistics.recursive_items(dictionary):
            if key == get_key:
                return value
        return ""
