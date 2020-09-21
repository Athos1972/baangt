from baangt.base.ExportResults.ExportResults import ExportAdditionalDataIntoTab, ExportNetWork
from unittest.mock import MagicMock
import datetime
import pytest


def test_ExportAdditionalDataIntoTab():
    ExportAdditionalDataIntoTab("temp", {1: {"header": "value"}}, MagicMock()).export()
    assert 1 == 1


@pytest.mark.parametrize("d1, d2", [
    ([datetime.datetime.now() + datetime.timedelta(hours=1)], []),
    ([], [[[0, datetime.datetime.now() + datetime.timedelta(hours=1)]]]),
    ([], []),
])
def test_get_test_case_num(d1, d2):
    en = ExportNetWork({}, d1, d2, MagicMock(), MagicMock())
    en._get_test_case_num(str(datetime.datetime.now()), "chrome")
    assert 1 == 1