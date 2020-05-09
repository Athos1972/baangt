import pytest
from datetime import datetime
import baangt.base.GlobalConstants as GC
import baangt.base.CustGlobalConstants as CGC

from baangt.base.Utils import utils

def test_datetime_return():
    datetime_now = datetime.now().strftime("%Y%m%d_%H%M%S")
    assert utils.datetime_return() == datetime_now

def test_sanitizeFileName():
    file_name = "'text.py'"
    sanitize_file_name = "test.py"

    assert utils.sanitizeFileName(file_name) == sanitize_file_name
    

def test_anyting2Boolean_raise():
    # todo
    pass

def test_replaceFieldValueWithValueOfConstant_GC_GCG():
    assert utils.replaceFieldValueWithValueOfConstant(
        "GC.BROWSER_CHROME") == "CHROME"
    assert utils.replaceFieldValueWithValueOfConstant(
        "CGC.VERMITTLER") == "vermittler"
    assert utils.replaceFieldValueWithValueOfConstant(
        "GC.NOT_EXISTENT") == "GC.NOT_EXISTENT"

def test_anyting2Boolean_booleans():
    assert utils.anyting2Boolean(True) is True
    assert utils.anyting2Boolean(False) is False

def test_anyting2Boolean_numbers():
    assert utils.anyting2Boolean(0) is False
    assert utils.anyting2Boolean(1) is True
    assert utils.anyting2Boolean(51) is True

def test_anyting2Boolean_strings():
    assert utils.anyting2Boolean("true") is True
    assert utils.anyting2Boolean("something else") is False