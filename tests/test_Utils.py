import os
import pytest
import logging
from pathlib import Path
from datetime import datetime
import baangt.base.GlobalConstants as GC
import baangt.base.CustGlobalConstants as CGC
from baangt.base.BrowserHandling.BrowserHandling import BrowserDriver

logger = logging.getLogger("pyC")

from baangt.base.Utils import utils

def test_datetime_return():
    datetime_now = datetime.now().strftime("%Y%m%d_%H%M%S")
    assert utils.datetime_return() == datetime_now

def test_sanitizeFileName():
    file_name = "'test.py'"
    sanitize_file_name = "test.py"

    assert utils.sanitizeFileName(file_name) == sanitize_file_name
    

def test_openJson():
    directory = Path(os.getcwd()).joinpath("examples")
    json_globals = utils.openJson(Path(directory).joinpath('globals.json'))
    assert json_globals["TC.Lines"] == ""
    assert json_globals["TC.dontCloseBrowser"] == ""
    assert json_globals["TC.slowExecution"] == ""
    assert json_globals["TC.NetworkInfo"] == ""
    assert json_globals["TX.DEBUG"] == "True"

def test_setLogLevel():
    level = "Info"
    utils.setLogLevel(level)

    assert logger.isEnabledFor(20)

def test_listToString_number_list():
    numbers = [1, 2, 3]
    assert utils.listToString(numbers) == '1, 2, 3'

def test_listToString_string_list():
    letters = ['a', 'b', 'c']
    assert utils.listToString(letters) == 'a, b, c'

def test_listToString_object_list():
    users = [{'name': 'Andrea', 'age': 18}, {'name': 'Jhon', 'age': 25}]
    assert utils.listToString(users) == "{'name': 'Andrea', 'age': 18}, {'name': 'Jhon', 'age': 25}"

def test___listChildToString_number_list():
    numbers = [1, 2, 3]
    print("***********************************")
    print(utils._utils__listChildToString(numbers))
    print("***********************************")
    assert utils.listToString(numbers) == '1, 2, 3'

def test___listChildToString_string_list():
    letters = ['a', 'b', 'c']
    assert utils.listToString(letters) == 'a, b, c'

def test___listChildToString_object_list():
    users = [{'name': 'Andrea', 'age': 18}, {'name': 'Jhon', 'age': 25}]
    assert utils.listToString(users) == "{'name': 'Andrea', 'age': 18}, {'name': 'Jhon', 'age': 25}"

def test___listChildToString_lists_list():
    lists = [[1, 2, 3], ['a', 'b', 'c']]
    assert utils.listToString(lists) == "1, 2, 3\na, b, c"

def test_setLocatorFromLocatorType_xpath():
    locatorType = 'XPATH'
    locator = '/library/book/author'
    
    xpath, css, id = utils.setLocatorFromLocatorType(locatorType, locator)
    assert xpath == locator
    assert css == None
    assert id == None

def test_setLocatorFromLocatorType_css():
    locatorType = 'CSS'
    locator = 'fa-trash'
    
    xpath, css, id = utils.setLocatorFromLocatorType(locatorType, locator)
    assert xpath == None
    assert css == locator
    assert id == None

def test_setLocatorFromLocatorType_id():
    locatorType = 'ID'
    locator = 'library'
    
    xpath, css, id = utils.setLocatorFromLocatorType(locatorType, locator)
    assert xpath == None
    assert css == None
    assert id == locator

def test_dynamicImportOfClasses_fullQualifiedImportName():
    fullQualifiedImportName = "baangt.base.BrowserHandling.BrowserHandling.BrowserDriver"
    
    assert utils.dynamicImportOfClasses(fullQualifiedImportName=fullQualifiedImportName)  == BrowserDriver().__class__


def test_dynamicImportOfClasses_className():
    className = "BrowserDriver"
    with pytest.raises(Exception) as e:
        assert utils.dynamicImportOfClasses(className=className)  == BrowserDriver().__class__

def test_dynamicImportOfClasses_path_className():
    path = "baangt.base.BrowserHandling.BrowserHandling"
    className = "BrowserDriver"

    assert utils.dynamicImportOfClasses(modulePath=path, className=className)  == BrowserDriver().__class__

def test_dynamicImportOfClasses_path_className_not_found_class_in_module():
    path = "baangt.base.BrowserHandling.BrowserHandling"
    className = "BrowserDriverHookImpl"
    with pytest.raises(Exception) as e:
        assert utils.dynamicImportOfClasses(modulePath=path, className=className)  == BrowserDriver().__class__


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