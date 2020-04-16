import json
import requests
from random import randint
from threading import Thread
from bs4 import BeautifulSoup as bs
from baangt.base.TestRun import TestRun
import logging
import sys

logger = logging.getLogger("pyC")


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ProxyRotate(metaclass=Singleton):
    def __init__(self):
        self.proxy_file = "proxies.json"
        self.proxy_gather_link = "https://www.sslproxies.org/"
        self.proxies = self.__read_proxies()
        self.__temp_proxies = []

    def recheckProxies(self, forever=False):
        if forever:
            t = Thread(target=self.__threaded_proxy)
            t.daemon = True
            t.start()
        else:
            t = Thread(target=self.__gather_proxy)
            t.daemon = True
            t.start()

    def __threaded_proxy(self):
        while True:
            self.__gather_proxy()

    def __gather_proxy(self):
        self.__temp_proxies = [p for p in self.proxies]
        logger.debug("Checking for new proxies...")
        try:
            response = requests.get(self.proxy_gather_link, timeout=15)
        except Exception as ex:
            print(ex)
            logger.error("No proxies read. Maybe Internet-connection is down. Please check and retry...")
            return None
        soup = bs(response.content, 'html.parser')
        table = soup.find('tbody')
        tr_list = table.find_all('tr')
        for tr in tr_list:
            ip = tr.find_all('td')[0].text
            port = tr.find_all('td')[1].text
            proxy = {"ip": ip, "port": port}
            if proxy not in self.__temp_proxies:
                logger.debug(f"Added {proxy} to be checked ")
                self.__temp_proxies.append(proxy)
        self.__verify_proxies()
        self.__write_proxies()

    def __verify_proxies(self):
        removable = []
        link1 = "https://www.youtube.com/watch?v=FghBQsZJg4U"
        link2 = "https://gogs.earthsquad.global"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        for proxi in self.__temp_proxies:
            logger.debug(f"{(str(self.temp_proxies.index(proxi) + 1))}/ {str(len(self.temp_proxies))}: {proxi}")
            proxy = {
                "http": "http://" + proxi["ip"] + ":" + proxi["port"],
                "https": "http://" + proxi["ip"] + ":" + proxi["port"],
            }
            try:
                response1 = requests.get(link1, proxies=proxy, headers=headers, timeout=20)
                response2 = requests.get(link2, proxies=proxy, headers=headers, timeout=20)
            except Exception as ex:
                logger.debug(f"Proxy not reacting: {proxi}")
                removable.append(proxi)
                continue

            soup1 = bs(response1.content, 'html.parser')
            soup2 = bs(response2.content, 'html.parser')
            try:
                name = soup1.find('meta', {'property': 'og:title'}).get('content')
                logo = soup2.find('div', class_='logo')
                logger.debug(f"Proxy can be used for Youtube: {proxi}")
            except Exception as ex:
                logger.debug(f"Proxy not usable for Youtube: {proxi}, Exception: {ex}")
                removable.append(proxi)
        for rm in removable:
            self.__temp_proxies.remove(rm)
        self.proxies = [p for p in self.__temp_proxies]
        logger.info(f"Identified {len(self.proxies)} working proxies")

    def __read_proxies(self):
        try:
            json_file = open(self.proxy_file, 'r')
            file = json_file.read()
            proxies = json.loads(file)
            json_file.close()
            logger.debug(f"Read {len(proxies['list'])} proxies from file")
        except Exception as e:
            proxies = {"list": []}
        return proxies["list"]

    def __write_proxies(self):
        json_file = open(self.proxy_file, 'w')
        json.dump({"list": self.proxies}, json_file)
        json_file.close()
        logger.debug(f"Wrote list of {len(self.proxies)} proxies to JSON-File")

    def __getProxy(self):
        if len(self.proxies) > 0:
            return self.proxies[randint(0, len(self.proxies) - 1)]
        else:
            logger.critical("Sorry there is no working proxy!")
            sys.exit("No working proxy identified - can't continue")

    def random_proxy(self):
        return self.__getProxy()

    def remove_proxy(self, ip, port):
        self.proxies.remove({"ip": ip, "port": str(port)})
        logger.debug(f"Ip removed successfully.")


if __name__ == '__main__':
    lProxyRotate = ProxyRotate()
    if TestRun.globalSettings["TC.ReReadProxies"] == True:
        lProxyRotate.recheckProxies(forever=True)
    else:
        lProxyRotate.recheckProxies()

    print(lProxyRotate.__getProxy())
