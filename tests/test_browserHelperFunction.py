import pytest
import logging
from unittest.mock import MagicMock, patch
from baangt.base.BrowserHandling.BrowserHelperFunction import BrowserHelperFunction


@pytest.mark.parametrize("desiredCapabilities", [({}), ({"seleniumGridIp": "0.0.0.0", "seleniumGridPort": "4444"})])
def test_browserHelper_setSettingsRemoteV4(desiredCapabilities):
    result = BrowserHelperFunction.browserHelper_setSettingsRemoteV4(desiredCapabilities)
    assert len(result) == 3


@pytest.mark.parametrize("logType", [(logging.ERROR), (logging.WARN), ("")])
def test_browserHelper_log(logType):
    BrowserHelperFunction.browserHelper_log(logType, "Log Text", MagicMock(), MagicMock, extra="test")
    assert 1 == 1


@patch("baangt.base.ProxyRotate.ProxyRotate.remove_proxy", MagicMock)
def test_browserHelper_setProxyError():
    BrowserHelperFunction.browserHelper_setProxyError({"ip": "127.0.0.1", "port": "4444"})
    assert 1 == 1
