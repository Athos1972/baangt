import json
import requests
from time import sleep
from random import randint
from threading import Thread
from bs4 import BeautifulSoup as bs
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
    def __init__(self, reReadProxies=True):
        self.reReadProxies = reReadProxies
        self.proxy_file = "proxies.json"
        self.proxy_gather_link = "https://www.sslproxies.org/"
        self.proxies = self.__read_proxies()
        self.firstRun = True
        self.__temp_proxies = []

    def recheckProxies(self, forever=False):
        self.__gather_proxy()
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
        for lineCount, proxi in enumerate(self.__temp_proxies):
            logger.debug(f"{(str(self.__temp_proxies.index(proxi) + 1))}/ {str(len(self.__temp_proxies))}: {proxi}")
            proxy = {
                "http": f"http://{proxi['ip']}:{proxi['port']}",
                "https": f"http://{proxi['ip']}:{proxi['port']}",
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

            # Check, if we have at least 4 proxies in the first run of the function.
            # If yes, exit, as the function will re-run soon.
            goodProxies = lineCount - len(removable) - 1   # Because enum starts with 0, LEN starts with 1
            if goodProxies >= 2 and self.firstRun:
                # Remove all proxies above our current lineCount
                for index, (lDictEntry) in enumerate(self.__temp_proxies):
                    if index > lineCount:
                        removable.append(lDictEntry)
                break

        self.firstRun = False

        for rm in removable:
            self.__temp_proxies.remove(rm)
        self.proxies = [p for p in self.__temp_proxies]
        logger.info(f"Total proxies in list currently = {str(len(self.proxies))}")
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
        logger.debug(f"Ip {ip} - Port {port} removed successfully.")


if __name__ == '__main__':
    lProxyRotate = ProxyRotate(reReadProxies=False)
    lProxyRotate.recheckProxies()
    print(lProxyRotate.random_proxy())
