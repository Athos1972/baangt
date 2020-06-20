import json
import logging
import requests
from dataclasses import dataclass, asdict, field
from typing import Dict
from baangt.base.RuntimeStatistics import Statistic


logger = logging.getLogger("pyC")


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def default_field(obj):
    return field(default_factory=lambda: obj)

@dataclass
class Statistics(metaclass=Singleton):
    Activity: Dict[str, int] = default_field({})
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
    TestStepMaster: Dict[str, int] = default_field({})
    TestStepSequences: int = 0
    TestSteps: int = 0
    TestCaseSequences: int = 0
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
        TestStepMaster_lis = Statistics.get_value(dic, "TestStepClass", lis=True)
        for value in TestStepMaster_lis:
            if value not in self.TestStepMaster:
                self.TestStepMaster[value] = 1
            else:
                self.TestStepMaster[value] += 1

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
        if prefix == "Activity_":
            if string not in self.Activity:
                self.Activity[string] = 0
            self.Activity[string] += 1
        else:
            var = getattr(self, string)
            var += 1
            setattr(self, string, var)

    def update_attribute_with_value(self, string, value):
        setattr(self, string, value)
        
    def update_runtimeStatistic(self):
        runtimeStats = Statistic()
        self.TestCaseSequences = runtimeStats.testcase_sequence_executed
        self.TestSteps = runtimeStats.teststep_executed
        self.TestStepSequences = runtimeStats.teststep_sequence_executed

    def to_dict(self):
        removeable = []
        dic = asdict(self)
        new_dic = {}
        for key in dic:
            if key[0] == "-":
                removeable.append(key)
            if dic[key] == 0 or dic[key] == "":
                removeable.append(key)
            if key == "Activity":
                for ky in dic[key]:
                    new_dic[ky] = dic[key][ky]
                removeable.append(key)
        for key in dic:
            if key not in removeable:
                new_dic[key] = dic[key]
        return new_dic

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
    def get_value(dictionary, get_key, lis=False):
        if lis:
            dic_lis = []
        for key, value in Statistics.recursive_items(dictionary):
            if key == get_key:
                if lis:
                    dic_lis.append(value)
                else:
                    return value
        if lis:
            return dic_lis
        return ""
