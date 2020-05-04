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

