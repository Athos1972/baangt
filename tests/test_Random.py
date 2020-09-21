from baangt.TestSteps.TestStepMaster import TestStepMaster
from baangt.TestSteps.RandomValues import RandomValues
import datetime

TestStepMaster.testcaseDataDict = {}
TestStepMaster.randomValues = RandomValues()


def test_name():
    name = TestStepMaster.replaceVariables(TestStepMaster, '$(random{"type":"name"})')
    assert len(name) > 0 and len(name.split()) > 1


def test_string():
    string1 = TestStepMaster.replaceVariables(TestStepMaster, '$(random{"type":"string"})')
    assert len(string1) > 0
    string2 = TestStepMaster.replaceVariables(TestStepMaster, '$(random{"type":"string", "min":10, "max":100})')
    assert len(string2) > 0 and len(string2) < 101


def test_int():
    integer = TestStepMaster.replaceVariables(TestStepMaster, '$(random{"type":"int", "min":100, "max":1000})')
    assert int(integer) > 99 and int(integer) < 1001


def test_float():
    flt = TestStepMaster.replaceVariables(TestStepMaster, '$(random{"type":"float", "min":100, "max":1000})')
    assert float(flt) > 99 and float(flt) < 1001


def test_date():
    date = TestStepMaster.replaceVariables(
        TestStepMaster, '$(random{"type":"date", "min":"20/1/2020", "max":"30/6/2020", "format":"%d/%m/%Y"})')
    date_obj = datetime.datetime.strptime(date, "%d/%m/%Y")
    assert type(date_obj) is datetime.datetime and date_obj.year == 2020


def test_time():
    time = TestStepMaster.replaceVariables(
        TestStepMaster, '$(random{"type":"time", "min":"10.30.00", "max":"15.00.00", "format": "%H.%M.%S"}')
    time_obj = datetime.datetime.strptime(time, "%H.%M.%S")
    assert type(time_obj) is datetime.datetime and 9 < time_obj.hour < 15
