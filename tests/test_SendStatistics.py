from baangt.base.ExportResults.SendStatistics import Statistics
import json
import os


stats = Statistics()
kwargs_file = open(os.path.join(os.getcwd(), "tests/0TestInput/kwargs.json"), 'r')
kwargs = json.load(kwargs_file)
kwargs["TESTRUNEXECUTIONPARAMETERS"]["TESTSEQUENCE"][1] = kwargs["TESTRUNEXECUTIONPARAMETERS"]["TESTSEQUENCE"]["1"]
kwargs["TESTRUNEXECUTIONPARAMETERS"]["TESTSEQUENCE"][1][1]["TESTCASE"][1] = kwargs["TESTRUNEXECUTIONPARAMETERS"][
    "TESTSEQUENCE"]['1'][1]["TESTCASE"]['1']
kwargs["TESTRUNEXECUTIONPARAMETERS"]["TESTSEQUENCE"][1][1]["TESTCASE"][1][2]["TestStep"][1] = kwargs[
    "TESTRUNEXECUTIONPARAMETERS"]["TESTSEQUENCE"]['1'][1]["TESTCASE"]['1'][2]["TestStep"]['1']
kwargs_file.close()


def test_update_data():
    stats.update_data(kwargs)
    assert stats.Activity["Activity_CLICK"] == 30


def test_update_attribute():
    stats.update_attribute("CLICK", prefix="Activity_")
    stats.update_attribute("Browser")
    assert stats.Activity["Activity_CLICK"] == 31 and stats.Browser == 2


def test_to_dict():
    dic = stats.to_dict()
    assert type(dic) == dict and dic["Browser"] == 2


def test_send_statistics():
    stats.TestRunUUID = "PYTEST"
    resp = stats.send_statistics(test=True)
    response_data = json.loads(resp.content.decode('utf-8'))
    assert resp.status_code == 200 and response_data["TestRunUUID"] == "PYTEST"
