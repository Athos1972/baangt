from baangt.base.ExportResults.Append2BaseXLS import Append2BaseXLS
import pytest
from unittest.mock import patch
import icopy2xls


class testRun:
    def __init__(self):
        self.globalSettings = {"AR2BXLS": "examples/CompleteBaangtWebdemo.xlsx,1;/fake/path/test.xlsx,1"}


@pytest.fixture(scope="module")
def testRunInstance():
    return testRun()


@patch.object(icopy2xls.Mover, "move")
def test_A2BX(mock_mover, testRunInstance):
    Append2BaseXLS(testRunInstance)
    assert 1 == 1
