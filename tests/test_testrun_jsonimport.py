# import pytest
# import os
# from pathlib import Path
# from baangt.base.TestRun.TestRun import TestRun
#
#
# def test_with_globalsHeadless():
#     lTestRun = TestRun(str(Path(os.getcwd()).parent.joinpath("examples").joinpath("SimpleTheInternet.xlsx")),
#                        globalSettingsFileNameAndPath=str(Path(os.getcwd()).joinpath("jsons").joinpath("globals_headless.json")))
#
#     assert lTestRun.globalSettings["TC.BrowserAttributes"]
#     assert isinstance(lTestRun.globalSettings["TC.BrowserAttributes"], dict)