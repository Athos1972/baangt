import os
import pytest
import logging
from pathlib import Path
from datetime import datetime
from baangt.base.BrowserHandling.BrowserHandling import BrowserDriver
from baangt.base.Utils import utils

logger = logging.getLogger("pyC")


def test_utils_instance():
    instance = utils()
    assert instance._utils__perf_trace == {}


def test_datetime_return():
    datetime_now = datetime.now().strftime("%Y%m%d_%H%M%S")
    assert utils.datetime_return() == datetime_now


def test_sanitizeFileName():
    file_name = "'test.py'"
    sanitize_file_name = "test.py"

    assert utils.sanitizeFileName(file_name) == sanitize_file_name


def test_replaceFieldValueWithValueOfConstant_GC_GCG():
    assert utils.replaceFieldValueWithValueOfConstant(
        "GC.BROWSER_CHROME") == "CHROME"
    assert utils.replaceFieldValueWithValueOfConstant(
        "CGC.VERMITTLER") == "vermittler"
    assert utils.replaceFieldValueWithValueOfConstant(
        "GC.NOT_EXISTENT") == "GC.NOT_EXISTENT"


def test_replaceAllGlobalConstantsInDict_str():
    obj_constants = {
        "GC.BROWSER_CHROME": "GC.BROWSER_CHROME",
        "CGC.VERMITTLER": "vermittler",
        "GC.NOT_EXISTENT": "GC.NOT_EXISTENT"
    }

    obj_result = utils.replaceAllGlobalConstantsInDict(obj_constants)

    assert obj_result["CHROME"] == "CHROME"
    assert obj_result["vermittler"] == "vermittler"
    assert obj_result["GC.NOT_EXISTENT"] == "GC.NOT_EXISTENT"


def test_replaceAllGlobalConstantsInDict_dict():
    obj = {
        "constants": {
            "GC.BROWSER_CHROME": "GC.BROWSER_CHROME",
            "CGC.VERMITTLER": "vermittler",
            "GC.NOT_EXISTENT": "GC.NOT_EXISTENT"
        }
    }

    obj_result = utils.replaceAllGlobalConstantsInDict(obj)

    assert obj_result["constants"]["CHROME"] == "CHROME"
    assert obj_result["constants"]["vermittler"] == "vermittler"
    assert obj_result["constants"]["GC.NOT_EXISTENT"] == "GC.NOT_EXISTENT"


def test_replaceAllGlobalConstantsInDict_list():
    obj = {
        "constants": ["GC.BROWSER_CHROME", "CGC.VERMITTLER", "GC.NOT_EXISTENT"]
    }

    obj_result = utils.replaceAllGlobalConstantsInDict(obj)

    assert obj_result["constants"][0] == "CHROME"
    assert obj_result["constants"][1] == "vermittler"
    assert obj_result["constants"][2] == "GC.NOT_EXISTENT"


def test_replaceAllGlobalConstantsInDict_other():
    obj = {
        "total": 15.5,
        "age": 21
    }

    obj_result = utils.replaceAllGlobalConstantsInDict(obj)

    assert obj_result["total"] == 15.5
    assert obj_result["age"] == 21


def test_replaceAllGlobalConstantsInDict_loopList_dict():
    obj = {
        "constants": [
            {"GC.BROWSER_CHROME": "GC.BROWSER_CHROME"},
            {"CGC.VERMITTLER": "vermittler"},
            {"GC.NOT_EXISTENT": "GC.NOT_EXISTENT"}
        ]
    }

    result = utils.replaceAllGlobalConstantsInDict(obj)
    constants = result["constants"]

    assert constants[0]["CHROME"] == "CHROME"
    assert constants[1]["vermittler"] == "vermittler"
    assert constants[2]["GC.NOT_EXISTENT"] == "GC.NOT_EXISTENT"


def test_replaceAllGlobalConstantsInDict_loopList_list():
    obj = {
        "constants": [
            ["GC.BROWSER_CHROME", "CGC.VERMITTLER", "GC.NOT_EXISTENT"]
        ]
    }

    result = utils.replaceAllGlobalConstantsInDict(obj)
    result_list = result["constants"][0]

    assert result_list[0] == "CHROME"
    assert result_list[1] == "vermittler"
    assert result_list[2] == "GC.NOT_EXISTENT"


def test_openJson():
    directory = Path(os.getcwd()).joinpath("tests").joinpath("jsons")
    json_globals = utils.openJson(Path(directory).joinpath('globals.json'))
    assert json_globals["TC.Lines"] == ""
    assert not json_globals["TC.dontCloseBrowser"]
    assert json_globals["TC.slowExecution"] == "True"
    assert not json_globals.get("TX.DEBUG")


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
    
    xpath, css, lid = utils.setLocatorFromLocatorType(locatorType, locator)
    assert xpath == locator
    assert not css
    assert not lid


def test_setLocatorFromLocatorType_css():
    locatorType = 'CSS'
    locator = 'fa-trash'
    
    xpath, css, lid = utils.setLocatorFromLocatorType(locatorType, locator)
    assert not xpath
    assert css == locator
    assert not lid


def test_setLocatorFromLocatorType_id():
    locatorType = 'ID'
    locator = 'library'
    
    xpath, css, lid = utils.setLocatorFromLocatorType(locatorType, locator)
    assert not xpath
    assert not css
    assert lid == locator


def test_dynamicImportOfClasses_fullQualifiedImportName():
    fullQualifiedImportName = "baangt.base.BrowserHandling.BrowserHandling.BrowserDriver"
    
    assert utils.dynamicImportOfClasses(fullQualifiedImportName=fullQualifiedImportName) == BrowserDriver().__class__


def test_dynamicImportOfClasses_className():
    className = "BrowserDriver"
    with pytest.raises(Exception):
        assert utils.dynamicImportOfClasses(className=className) == BrowserDriver().__class__


def test_dynamicImportOfClasses_path_className():
    path = "baangt.base.BrowserHandling.BrowserHandling"
    className = "BrowserDriver"

    assert utils.dynamicImportOfClasses(modulePath=path, className=className) == BrowserDriver().__class__


def test_dynamicImportOfClasses_path_className_not_found_class_in_module():
    path = "baangt.base.BrowserHandling.BrowserHandling"
    className = "BrowserDriverHookImpl"
    with pytest.raises(Exception):
        assert utils.dynamicImportOfClasses(modulePath=path, className=className) == BrowserDriver().__class__


def test_findFileAndPathFromPath_directory():
    directory = "~/baangt/examples"
    fileNameAndPath = Path(directory).joinpath('global_not_exist.json')
    with pytest.raises(Exception):
        utils.findFileAndPathFromPath(fileNameAndPath, directory)


def test_findFileAndPathFromPath_only_fileNamePath():
    fileNameAndPath = 'globals.json'
    with pytest.raises(Exception):
        utils.findFileAndPathFromPath(str(fileNameAndPath))


def test_findFileAndPathFromPath_except_canot_find_file():
    directory = Path(os.getcwd()).parent.joinpath("examples")
    fileNameAndPath = Path(directory).joinpath('globals2.json')
    with pytest.raises(Exception):
        utils.findFileAndPathFromPath(str(fileNameAndPath))


def test_findFileAndPathFromPath_exists_by_directory_and_only_fileName():
    directory = Path(os.getcwd()).joinpath("examples")
    fileNameAndPath = 'globals.json'
    result = utils.findFileAndPathFromPath(fileNameAndPath, str(directory))

    assert Path(result).exists()


def test_anything2Boolean_raise():
    lResult = utils.anything2Boolean({})
    assert lResult == False


def test_anything2Boolean_booleans():
    assert utils.anything2Boolean(True) is True
    assert utils.anything2Boolean(False) is False


def test_anything2Boolean_numbers():
    assert utils.anything2Boolean(0) is False
    assert utils.anything2Boolean(1) is True
    assert utils.anything2Boolean(51) is True


def test_anything2Boolean_strings():
    assert utils.anything2Boolean("true") is True
    assert utils.anything2Boolean("something else") is False
