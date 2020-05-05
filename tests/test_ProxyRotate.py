from baangt.base.ProxyRotate import  ProxyRotate
import os

def test_gather_links():
    ## Will if links are gathering from website
    proxyRotate = ProxyRotate()
    proxies = proxyRotate.testGatherProxy()
    assert type(proxies)==list and len(proxies)>0


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
    assert 1 == 1

def test_proxy_remove_invalidIP():
    proxyRotate = ProxyRotate(reReadProxies=False)
    proxyRotate.remove_proxy("Franzi")   # Invalid Proxy call shall not cause any troubles.
    assert 1 == 1


