# Mocks
from requests.models import Response
import requests
import time 
import csv

# Test Env
import pytest 
from unittest.mock import patch

# Test functions
from baangt.base.ProxyRotate import  ProxyRotate, proxy_data
import baangt.base.GlobalConstants as GC
from dataclasses import dataclass, asdict
from http import HTTPStatus
import copy

MIN_PROXIES_FOR_FIRST_RUN = 3

def create_init_proxy_list(length):
    proxyList = []
    for index in range(length):
        proxy = asdict(proxy_data(ip = (str)(index), port = (str)(0)))
        for key in proxy:
            proxy[key] = str(proxy[key])
        proxyList.append(proxy)
    return proxyList


def init_ProxyRotate(mock_csv_DictReader, proxyListLength, firstRun = True):
    proxyRotate = ProxyRotate()
    proxyRotate.proxy_gather_link = "https://www.sslproxies.org/"
    proxyRotate.proxies = {}                     
    proxyRotate.all_proxies = {}      
    proxyRotate._ProxyRotate__temp_proxies = []           
    proxyRotate.firstRun = firstRun
    proxyRotate.MIN_PROXIES_FOR_FIRST_RUN = MIN_PROXIES_FOR_FIRST_RUN
    mock_csv_DictReader.return_value = create_init_proxy_list(proxyListLength)
    proxyRotate._ProxyRotate__read_proxies()
    return proxyRotate

def create_proxy_verification_response(status_code, length, deleteString=None):
    ret = []
    for index in range(length):
        res_youtube = Response()
        res_youtube._content = "<!DOCTYPE html><html><head><meta content='Content' property='og:title'/></head><body></body></html>"
        res_youtube.status_code = status_code
        res_google = copy.copy(res_youtube)
        res_google._content = "<!DOCTYPE html><html></head><body><div class='logo'><img src='/img/favicon.png'></img></div></body></html>"
        if deleteString is not None:
            res_google._content = res_google._content.replace(deleteString, "")
            res_youtube._content = res_youtube._content.replace(deleteString, "")
        ret.append(res_youtube)
        ret.append(res_google)
    return ret


def create_request_proxy_list(status_code, length, deleteString=None):
    res_proxy = Response()
    res_proxy._content = "<!DOCTYPEhtml><html><head></head><body><tbody>"
    for index in range(length):
        res_proxy._content +=  f'<tr><td>{index}.000</td><td>40231</td><td>KE</td></tr>' 
    res_proxy._content +=  "</tbody></body></html>"
    if deleteString is not None:
        res_proxy._content = res_proxy._content.replace(deleteString, "")
    res_proxy.status_code = status_code
    return res_proxy


@patch("requests.get")
@patch('time.sleep', return_value = None) 
@patch("csv.DictReader")
@pytest.mark.parametrize("proxyLength", list(range(0,MIN_PROXIES_FOR_FIRST_RUN)))
@pytest.mark.parametrize("additionalProxyRequestLength", [1])
def test_recheckProxies_init_proxy_with_less_min_proxy(mock_csv_DictReader, mock_time_sleep, mock_get, proxyLength, additionalProxyRequestLength):
    """ 
    Initialise a valid proxy list <= MIN_PROXIES_FOR_FIRST_RUN
    Test Steps:
    - Init a valid proxy list (length 0....MIN_PROXIES_FOR_FIRST_RUN), firstRun = True
    - Verificate proxy list successful 
    - Request for more proxy items is provided 
        If proxy list size <= MIN_PROXIES_FOR_FIRST_RUN, ProxyRotate will request for more proxy servers
    """

    # Initialize proxy list 
    proxyRotate = init_ProxyRotate(mock_csv_DictReader, proxyLength)
    # Add valid response for proxy verification
    responseList = create_proxy_verification_response(HTTPStatus.OK, proxyLength)
    # Create successful requests for proxy list and proxy verification because [proxy list size > MIN_PROXIES_FOR_FIRST_RUN]
    responseList.append(create_request_proxy_list(HTTPStatus.OK, additionalProxyRequestLength))
    responseList.extend(create_proxy_verification_response(HTTPStatus.OK, additionalProxyRequestLength + proxyLength))
    mock_get.side_effect = responseList

    proxyRotate.recheckProxies(forever= False)

    assert len(responseList) == mock_get.call_count
    assert len(proxyRotate.proxies) == (additionalProxyRequestLength + proxyLength) 


@patch("requests.get")
@patch("csv.DictReader")
@pytest.mark.parametrize("proxyLength", list(range(MIN_PROXIES_FOR_FIRST_RUN,8)))
def test_recheckProxies_init_proxy_list(mock_csv_DictReader, mock_get, proxyLength):
    """ 
    Initialise a valid proxy list greater than MIN_PROXIES_FOR_FIRST_RUN
    Test Steps:
    - Init a valid proxy list (length MIN_PROXIES_FOR_FIRST_RUN...8), firstRun = True
    - Verificate proxy list successful 
    """
    # Initialize proxy list 
    proxyRotate = init_ProxyRotate(mock_csv_DictReader, proxyLength)
    # Add valid response for proxy verification (if firstRun == True only MIN_PROXIES_FOR_FIRST_RUN are validated)
    responseList = (create_proxy_verification_response(HTTPStatus.OK, MIN_PROXIES_FOR_FIRST_RUN))
    mock_get.side_effect = responseList

    proxyRotate.recheckProxies(forever= False)

    assert len(responseList) == mock_get.call_count
    assert len(proxyRotate.proxies) == proxyRotate.MIN_PROXIES_FOR_FIRST_RUN 
    assert len(proxyRotate.all_proxies) == proxyLength 



@patch("requests.get")
@patch('time.sleep', return_value = None) 
@patch("csv.DictReader")
@pytest.mark.parametrize("proxyLengthValid", [10])
@pytest.mark.parametrize("proxyLengthInvalid", [1])
@pytest.mark.parametrize("firstRun", [False])
def test_recheckProxies_proxy_verification_failed_html_status_error(mock_csv_DictReader, mock_time_sleep, mock_get, 
        proxyLengthValid, proxyLengthInvalid, firstRun):
    """ 
    Generate a html status error code in proxy verification
    Test Steps:
    - Init a valid proxy list, firstRun = False
    - One unsuccessful proxy validation response with html response status error is generated
    """    
    # Initialize proxy list 
    proxyRotate = init_ProxyRotate(mock_csv_DictReader, proxyLengthValid + proxyLengthInvalid, firstRun)
    # Add valid response for proxy verification
    responseList = create_proxy_verification_response(HTTPStatus.OK, proxyLengthValid)
    # Add invalid response for proxy verification
    responseList.extend(create_proxy_verification_response(HTTPStatus.BAD_REQUEST, proxyLengthInvalid))
    # Create response for requesting more proxies
    responseList.append(create_request_proxy_list(HTTPStatus.OK, 0))
    # Add valid response for proxy verification - proxies are validated again
    responseList.extend(create_proxy_verification_response(HTTPStatus.OK, proxyLengthValid))
    mock_get.side_effect = responseList
    
    proxyRotate.recheckProxies(forever= False)

    assert len(responseList) == mock_get.call_count
    assert len(proxyRotate.proxies) == proxyLengthValid 
    assert len(proxyRotate.all_proxies) == (proxyLengthValid  + proxyLengthInvalid)


@patch("requests.get")
@patch('time.sleep', return_value = None) 
@patch("csv.DictReader")
@pytest.mark.parametrize("proxyLengthValid", [10])
@pytest.mark.parametrize("proxyLengthInvalid", [1])
@pytest.mark.parametrize("firstRun", [False])
@pytest.mark.parametrize("htmlBodyErrors", ["property","logo", "meta", "div", "content"])
def test_recheckProxies_proxy_verification_failed_html_body(mock_csv_DictReader, mock_time_sleep, mock_get, 
        proxyLengthValid, proxyLengthInvalid, firstRun, htmlBodyErrors):
    """ 
    Generate a html body error in proxy verification
    Test Steps:
    - Init a valid proxy list, firstRun = False
    - One unsuccessful proxy validation response with html body error is generated
    """
    
    # Initialize proxy list 
    proxyRotate= init_ProxyRotate(mock_csv_DictReader, proxyLengthValid + proxyLengthInvalid, firstRun)
    # Add valid response for proxy verification
    responseList = create_proxy_verification_response(HTTPStatus.OK, proxyLengthValid)
    # Add invalid response for proxy verification
    responseList.extend(create_proxy_verification_response(HTTPStatus.OK, proxyLengthInvalid, htmlBodyErrors))
    # Create response for requesting more proxies
    responseList.append(create_request_proxy_list(HTTPStatus.OK, 0))
    # Add valid response for proxy verification - proxies are validated again
    responseList.extend(create_proxy_verification_response(HTTPStatus.OK, proxyLengthValid))
    mock_get.side_effect = responseList

    proxyRotate.recheckProxies(forever= False)

    assert len(responseList) == mock_get.call_count 
    assert len(proxyRotate.proxies) == proxyLengthValid
    assert len(proxyRotate.all_proxies) == (proxyLengthValid + proxyLengthInvalid)


@patch("requests.get")
@patch('time.sleep', return_value = None) 
@patch("csv.DictReader")
@pytest.mark.parametrize("proxyLengthValid", [10])
@pytest.mark.parametrize("proxyLengthInvalid", [1])
@pytest.mark.parametrize("firstRun", [False])
def test_recheckProxies_proxy_list_failed_html_status_error(mock_csv_DictReader, mock_time_sleep, mock_get, 
    proxyLengthValid, proxyLengthInvalid, firstRun):
    """ 
    Generate a html body error in proxy verification
    Test Steps:
    - Init a valid proxy list, firstRun = False
    - One unsuccessful proxy validation response with html response status error is generated
    """
    # Initialize proxy list 
    proxyRotate = init_ProxyRotate(mock_csv_DictReader, proxyLengthValid, firstRun)
    # Add valid response for proxy verification
    responseList = create_proxy_verification_response(HTTPStatus.OK, proxyLengthValid)
    # Create response for requesting more proxies
    responseList.append(create_request_proxy_list(HTTPStatus.BAD_REQUEST, proxyLengthInvalid))
    # Add valid response for proxy verification - proxies are validated again
    responseList.extend(create_proxy_verification_response(HTTPStatus.OK, proxyLengthValid))
    mock_get.side_effect = responseList

    proxyRotate.recheckProxies(forever= False)

    assert len(responseList) == mock_get.call_count 
    assert len(proxyRotate.proxies) == proxyLengthValid 
    assert len(proxyRotate.all_proxies) == proxyLengthValid

@patch("requests.get")
@patch('time.sleep', return_value = None) 
@patch("csv.DictReader")
@pytest.mark.parametrize("proxyLengthValid", [10])
@pytest.mark.parametrize("proxyLengthInvalid", [1])
@pytest.mark.parametrize("firstRun", [False])
@pytest.mark.parametrize("htmlBodyErrors", ["td","tr","tbody"])
def test_recheckProxies_proxy_list_failed_html_body(mock_csv_DictReader, mock_time_sleep, mock_get, 
    proxyLengthValid, proxyLengthInvalid, firstRun, htmlBodyErrors):
    """ 
    Generate a html body error in proxy list request
    Test Steps:
    - Init a valid proxy list, firstRun = False
    - Failure in proxy list html body response is generated
    """

    # Initialize proxy list 
    proxyRotate= init_ProxyRotate(mock_csv_DictReader, proxyLengthValid, firstRun)
    # Add valid response for proxy verification
    responseList = create_proxy_verification_response(HTTPStatus.OK, proxyLengthValid)
    # Create response for requesting more proxies
    responseList.append(create_request_proxy_list(HTTPStatus.OK, proxyLengthInvalid, htmlBodyErrors))
    # Add valid response for proxy verification - proxies are validated again
    responseList.extend(create_proxy_verification_response(HTTPStatus.OK, proxyLengthValid))
    mock_get.side_effect = responseList

    proxyRotate.recheckProxies(forever= False)

    assert len(responseList) == mock_get.call_count
    assert len(proxyRotate.proxies) == proxyLengthValid
    assert len(proxyRotate.all_proxies) == proxyLengthValid



@patch('time.sleep', return_value = None) 
@patch("csv.DictReader")
@pytest.mark.parametrize("proxyInitLength", [0, 10, 700])
def test_random_proxy(mock_csv_DictReader, mock_time_sleep, proxyInitLength):
    """ 
    Test random proxy return function
    """
    # Initialize proxy list 
    proxyRotate = init_ProxyRotate(mock_csv_DictReader, proxyInitLength)
    proxyRotate.proxies = proxyRotate.all_proxies

    result = proxyRotate.random_proxy()

    assert isinstance(result["ip"], str)
    assert isinstance(result["port"], str)
    assert isinstance(result["type"], str)
    assert proxyRotate.proxies[result["ip"]].called == 1

@patch("csv.DictReader")
@pytest.mark.parametrize("failedCounter", list(range(0,GC.PROXY_FAILCOUNTER)))
@pytest.mark.parametrize("proxyInitLength", [10])
def test_remove_proxy_fail_counter_in_range(mock_csv_DictReader, failedCounter, proxyInitLength):
    """ 
    Test increase the fail counter until the fail counter limit.
    Proxy should not be removed
    """    
    # Initialize proxy list 
    proxyRotate = init_ProxyRotate(mock_csv_DictReader, proxyInitLength)
    proxyRotate.proxies = proxyRotate.all_proxies

    for item in range(0, failedCounter):
        proxyRotate.remove_proxy((str)('0'))

    assert ('0' in proxyRotate.proxies)
    assert len(proxyRotate.proxies) == proxyInitLength
    

@patch("csv.DictReader")
@pytest.mark.parametrize("failedCounter", list(range(GC.PROXY_FAILCOUNTER, 5)))
#@pytest.mark.parametrize("failedCounter", list(range(5,10)))
@pytest.mark.parametrize("proxyInitLength", [10])
@pytest.mark.parametrize("testProdyId", ["0"])
def test_remove_proxy_fail_counter_out_of_range(mock_csv_DictReader, failedCounter, proxyInitLength, testProdyId):
    """ 
    Test increase the fail counter and exceed the fail counter limit.
    Proxy should be removed 
    """    
    # Initialize proxy list 
    proxyRotate = init_ProxyRotate(mock_csv_DictReader, proxyInitLength)
    proxyRotate.proxies = proxyRotate.all_proxies

    for item in range(0, failedCounter):
        proxyRotate.remove_proxy((str)(testProdyId))

    assert failedCounter >= GC.PROXY_FAILCOUNTER
    assert testProdyId not in proxyRotate.proxies
    assert len(proxyRotate.proxies) == (proxyInitLength - 1)


@patch("csv.DictReader")
@pytest.mark.parametrize("proxyInitLength", [10])
def test_remove_proxy_invalid_param(mock_csv_DictReader, proxyInitLength):
    """ 
    Test remove proxy for invalid parameter
    """    
    # Initialize proxy list 
    proxyRotate = init_ProxyRotate(mock_csv_DictReader, proxyInitLength)
    proxyRotate.proxies = proxyRotate.all_proxies

    proxyRotate.remove_proxy(ip = f'{proxyInitLength}')
    proxyRotate.remove_proxy(ip = proxyInitLength)
    proxyRotate.remove_proxy(ip = 'p')
    proxyRotate.remove_proxy(ip = 'z', port = 0)
    proxyRotate.remove_proxy(ip = 0, port = 'p')

    assert len(proxyRotate.proxies) == proxyInitLength
    


"""
# TODO This test belongs to the integration test
def test_gather_links():
    ## Will if links are gathering from website
    proxyRotate = ProxyRotate()
    proxies = proxyRotate.testGatherProxy()

    assert type(proxies)==list and len(proxies)>0
"""

"""
# TODO This test belongs to the integration test
def test_verify_proxy():
    ## Verifies single proxy and will give the result
    if os.path.isfile("../proxies.csv"):
        with open("../proxies.csv", 'r') as file:
            data = file.read()
            with open("proxies.csv", 'w') as output_file:
                output_file.write(data)
    elif os.path.isfile(os.path.join(os.path.expanduser("~"),"baangt/proxies.csv")):
        with open(os.path.join(os.path.expanduser("~"),"baangt/proxies.csv"), 'r') as file:
            data = file.read()
            with open("proxies.csv", 'w') as output_file:
                output_file.write(data)
    proxyRotate = ProxyRotate()
    result = proxyRotate.testVerifyProxy()
    print(result)
    assert type(result) == str
"""

"""
# TODO This test belongs to the integration test
def test_proxy_full_run():
    proxyRotate = ProxyRotate(reReadProxies=True)
    proxyRotate.recheckProxies(forever=False)
    assert len(proxyRotate.all_proxies) > len(proxyRotate.proxies)
    assert len(proxyRotate.proxies) == proxyRotate.MIN_PROXIES_FOR_FIRST_RUN

    result = proxyRotate.random_proxy()
    assert isinstance(result["ip"], str)
    assert isinstance(result["port"], str)
    assert isinstance(result["type"], str)

    result = proxyRotate.remove_proxy(ip=proxyRotate.random_proxy()["ip"])
    assert 1==1
"""