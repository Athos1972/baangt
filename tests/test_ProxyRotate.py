from baangt.base.ProxyRotate import  ProxyRotate

proxyRotate = ProxyRotate()

def test_gather_links():
    ## Will if links are gathering from website
    proxies = proxyRotate.testGatherProxy()
    assert type(proxies)==list and len(proxies)>0

def test_verify_proxy():
    ## Verifies single proxy and will give the result
    result = proxyRotate.testVerifyProxy()
    print(result)
    assert type(result) == str

