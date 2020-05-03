import json
import requests
from time import sleep
from random import randint
from threading import Thread
from bs4 import BeautifulSoup as bs
from dataclasses import dataclass
import logging
import sys
import csv
import baangt.base.GlobalConstants as GC
from dataclasses_json import dataclass_json


logger = logging.getLogger("pyC")


@dataclass_json
@dataclass
class proxy_data:
    ip: str = ""
    port: str = ""
    username: str = ""
    password: str = ""
    typ: str = "http"
    called: int = 0
    failed: int = 0

    def __post_init__(self):
        if not isinstance(self.called, int):
            self.called = int(self.failed)
        if not isinstance(self.failed, int):
            self.failed = int(self.failed)

    def Called(self):
        self.called+=1

    def Failed(self):
        self.failed+=1

    def Reset(self):
        self.called = 0
        self.failed = 0


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ProxyRotate(metaclass=Singleton):
    def __init__(self, reReadProxies=True):
        self.reReadProxies = reReadProxies
        self.proxy_file = "proxies.json"
        self.proxy_gather_link = "https://www.sslproxies.org/"
        self.proxies = {}
        self.all_proxies = {}
        self.__temp_proxies = []
        self.__read_proxies()
        self.firstRun = True

    def recheckProxies(self, forever=False):
        self.__verify_proxies(self.__temp_proxies)
        self.__gather_proxy(self.__temp_proxies)
        if forever:
            t = Thread(target=self.__threaded_proxy)
            t.daemon = True
            logger.debug("Starting daemon process for threaded Proxy rechecks")
            t.start()
            logger.debug("Daemon process started")

    def __threaded_proxy(self):
        while True:
            if self.reReadProxies == True:
                self.__gather_proxy()
            else:
                sleep(5)

    def __gather_proxy(self, proxy=None):
        if proxy == None:
            self.__temp_proxies = [self.proxies[p] for p in self.proxies]
        else:
            self.__temp_proxies = proxy
        logger.debug("Checking for new proxies...")
        try:
            response = requests.get(self.proxy_gather_link, timeout=15)
        except Exception as ex:
            print(ex)
            logger.error(f"No proxies read. Maybe Internet-connection is down. Please check and retry. Error was {ex}")
            return None
        soup = bs(response.content, 'html.parser')
        table = soup.find('tbody')
        tr_list = table.find_all('tr')
        for tr in tr_list:
            ip = tr.find_all('td')[0].text
            port = tr.find_all('td')[1].text
            proxy = proxy_data().from_dict({"ip": ip, "port": port})
            if proxy not in self.__temp_proxies:
                logger.debug(f"Added {proxy} to be checked ")
                self.__temp_proxies.append(proxy)
        self.__verify_proxies(self.__temp_proxies)
        self.__write_proxies()

    def __verify_proxies(self, proxy_lis):
        removable = []
        links = ["https://www.youtube.com/watch?v=FghBQsZJg4U", "https://gogs.earthsquad.global"]
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        for lineCount, proxi in enumerate(proxy_lis):
            responses = []
            if not self.firstRun:
                sleep(5)
            logger.debug(f"{(str(proxy_lis.index(proxi) + 1))}/ {str(len(proxy_lis))}: {proxi}")
            proxy = self.__set_proxy(proxi)
            for link in links:
                res = self.__get_response(link, proxy, headers)
                responses.append(res)
            if False in responses:
                logger.debug(f"Error code 400 or greater in {proxi}")
                removable.append(proxi)
                continue

            soup1 = bs(responses[0].content, 'html.parser')
            soup2 = bs(responses[1].content, 'html.parser')
            try:
                name = soup1.find('meta', {'property': 'og:title'}).get('content')
                logo = soup2.find('div', class_='logo')
                logger.debug(f"Proxy can be used for Youtube: {proxi}")
            except Exception as ex:
                logger.debug(f"Proxy not usable for Youtube: {proxi}, Exception: {ex}")
                removable.append(proxi)

            # Check, if we have at least 4 proxies in the first run of the function.
            # If yes, exit, as the function will re-run soon.
            goodProxies = lineCount - len(removable) - 1   # Because enum starts with 0, LEN starts with 1
            if goodProxies >= 2 and self.firstRun:
                break

        if len(removable)<len(proxy_lis) and self.firstRun:
            self.firstRun = False
            for proxy in proxy_lis[:lineCount]:
                if proxy not in removable:
                    self.proxies[proxy.ip] = proxy
                else:
                    self.__temp_proxies.remove(proxy)
            return None

        for rm in removable:
            if rm.ip in self.proxies:
                self.remove_proxy(rm.ip)
            proxy_lis.remove(rm)
        for proxy in proxy_lis:
            if proxy.ip not in self.proxies:
                self.proxies[proxy.ip] = proxy
                if proxy.ip not in self.all_proxies:
                    self.all_proxies[proxy.ip] = proxy
            elif proxy.failed>=GC.PROXY_FAILCOUNTER:
                self.proxies[proxy.ip] = proxy

        logger.info(f"Total proxies in list currently = {str(len(self.proxies))}")
        logger.info(f"Identified {len(self.proxies)} working proxies")

    def __get_response(self, link, proxy, headers):
        try:
            response = requests.get(link, proxies=proxy, headers=headers, timeout=15)
        except Exception as ex:
            logger.debug(f"Proxy not reacting: {proxy}")
            return False
        if response.status_code >= 400:
            return False
        return response

    def __set_proxy(self, proxi):
        if proxi.typ == "socks5":
            if proxi.username != "" and proxi.password != "":
                proxy = {
                    "http": f"socks5://{proxi.username}:{proxi.password}@{proxi.ip}:{proxi.port}",
                    "https": f"socks5://{proxi.username}:{proxi.password}@{proxi.ip}:{proxi.port}",
                }
            else:
                proxy = {
                    "http": f"socks5://{proxi.ip}:{proxi.port}",
                    "https": f"socks5://{proxi.ip}:{proxi.port}",
                }
        elif proxi.username != "" and proxi.password != "":
            proxy = {
                "http": f"http://{proxi.username}:{proxi.password}@{proxi.ip}:{proxi.port}",
                "https": f"https://{proxi.username}:{proxi.password}@{proxi.ip}:{proxi.port}",
            }
        else:
            proxy = {
                "http": f"http://{proxi.ip}:{proxi.port}",
                "https": f"http://{proxi.ip}:{proxi.port}",
            }
        return proxy

    def __read_proxies(self):
        try:
            with open('proxies.csv','r') as csv_file:
                raw_data = csv.DictReader(csv_file)
                for data in raw_data:
                    if int(data['failed']) < GC.PROXY_FAILCOUNTER:
                        proxy = proxy_data().from_dict(dict(data))
                        self.__temp_proxies.append(proxy)
                    self.all_proxies[data["ip"]] = proxy
        except Exception as ex:
            logger.debug(str(ex))

    def __write_proxies(self):
        with open("proxies.csv", 'w', newline='\n')as file:
            fl = csv.DictWriter(file, self.proxies[list(self.proxies.keys())[0]].to_dict().keys())
            fl.writeheader()
            for proxy in self.all_proxies:
                fl.writerow(self.all_proxies[proxy].to_dict())
        logger.debug(f"Wrote list of {len(self.proxies)} proxies to CSV-File")

    def __getProxy(self):
        if len(self.proxies) > 0:
            logger.critical(f"Proxies count: {len(self.proxies)}")
            proxy =  self.proxies[list(self.proxies.keys())[randint(0, len(self.proxies) - 1)]]
            proxy.Called()
            if proxy.username == "" and proxy.password == "":
                return {"ip": proxy.ip, "port": proxy.port, "type": proxy.typ}
            else:
                return {
                    "ip": proxy.ip, "port": proxy.port,
                    "username": proxy.username, "password": proxy.password, "type": proxy.typ
                }
        else:
            logger.critical("Sorry there is no working proxy!")
            sys.exit("No working proxy identified - can't continue")

    def random_proxy(self):
        return self.__getProxy()

    def remove_proxy(self, ip):
        self.proxies[ip].Failed()
        if self.proxies[ip].failed >= GC.PROXY_FAILCOUNTER:
            del self.proxies[ip]
            logger.debug(f"Ip {ip} removed successfully.")

    def testProxy(self,type, ip, port, user, password):
        return "Method not yet implemented"

if __name__ == '__main__':
    lProxyRotate = ProxyRotate(reReadProxies=False)
    lProxyRotate.recheckProxies()
    print(lProxyRotate.random_proxy())
