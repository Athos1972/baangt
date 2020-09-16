import pytest
from unittest.mock import patch
from baangt.TestSteps.Exceptions import baangtTestStepException
from baangt.base.ApiHandling import ApiHandling


class fake_response:
    def __init__(self, **kwargs):
        self.status_code = 200
        self.headers = ""
        self.process()

    def get(self, **kwargs):
        return self

    def post(self, **kwargs):
        return self

    def process(self):
        return {"success": 200, "headers": ""}

    def json(self):
        return '{"success": 200, "headers": ""}'

    def close(self):
        pass


@pytest.fixture(scope="module")
def apiHandling():
    return ApiHandling()


@patch("requests.Session", fake_response)
def test_getSession(apiHandling):
    apiHandling.getSession()
    assert 1 == 1


@pytest.mark.parametrize("sessionNumber", [(None), (1)])
def test_getNewSession(sessionNumber, apiHandling):
    if sessionNumber:
        apiHandling.getNewSession(sessionNumber=sessionNumber)
    else:
        with pytest.raises(baangtTestStepException):
            apiHandling.getNewSession()
    assert 1 in apiHandling.session


@patch.object(ApiHandling, "getSession", fake_response)
def test_getURL(apiHandling):
    apiHandling.setBaseURL("")
    apiHandling.setEndPoint("")
    apiHandling.getURL()
    assert 1 == 1


@pytest.mark.parametrize("status", [(200), (300)])
def test_returnTestCaseStatus(status, apiHandling):
    result = apiHandling.returnTestCaseStatus(status)
    assert result == "OK" or result == "Failed"


@patch.object(ApiHandling, "getSession", fake_response)
def test_postURL(apiHandling):
    apiHandling.setBaseURL("")
    apiHandling.setEndPoint("")
    apiHandling.postURL(content="{}", url="url")
    assert 1 == 1


def test_setLoginData(apiHandling):
    apiHandling.setLoginData("user", "pass")
    assert apiHandling.session[1].auth == ("user", "pass")
    apiHandling.tearDown()