import requests
import time 
from random import randint
from threading import Thread
from bs4 import BeautifulSoup as bs
from dataclasses import dataclass
import logging
import csv
import sys
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
    type: str = "http"
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
    """
    In ProxyRotate class we combine all functionalities related to proxy server handling.

    If the class is called with "reReadProxies"=True, we'll scrape and test new proxy servers
    If the class is called without reReadProxies we'll read existing proxies from the list.

    There are 3 states, that a proxy can have:
    * New (we just gathered this proxy from a page. We don't know whether it works or not.
    * Failed (we tried this proxy before. It didn't work)
    * Working (Fail-Count < GlobalConstants.Proxy_failcount)

    External interface are methods:
      random_proxy to retrieve a proxy
      remove_proxy to report an error
      recheckProxies to scrape for new proxies

    """

    def __init__(self, reReadProxies=True):
        self.reReadProxies = reReadProxies
        self.proxy_gather_link = "https://www.sslproxies.org/"
        self.proxies = {}                     # Currently usable proxies
        self.all_proxies = {}                 # List of all Proxies ever discovered, including failed ones
        self.__temp_proxies = []              # List of newly gathered Proxies, that still need to be checked
        self.__read_proxies()
        self.firstRun = True
        self.MIN_PROXIES_FOR_FIRST_RUN = 3

    def recheckProxies(self, forever=False):
        # Save firstRun locally because it will be changed in __verify_proxies:
        lFirst = self.firstRun
        self.__verify_proxies(self.__temp_proxies)
        if not self.reReadProxies:
            logger.info("recheckProxies was called, but reReadProxies is not set. " + \
                        "A bit of a strange combination of parameters.")
            return

        # If we're in first run and we found already the minimum amount of working proxies, return to calling
        # program
        if lFirst and len(self.proxies) >= self.MIN_PROXIES_FOR_FIRST_RUN:
            return

        self.__gather_proxies(self.__temp_proxies)
        if forever:
            t = Thread(target=self.__threaded_proxy)
            t.daemon = True
            logger.debug("Starting daemon process for threaded Proxy rechecks")
            t.start()
            logger.debug("Daemon process started")

    def __threaded_proxy(self):
        while True:
            if self.reReadProxies:
                self.__gather_proxies()
            else:
                msg = "This thread quits now, as reReadProxies is set to false - nothing to do. Most probably " + \
                      "shouldn't  have been a thread in the first place."
                logger.critical(msg)
                sys.exit(msg)

    def __gather_proxies(self, proxy=None, test=False):
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

        try:
            if response.status_code < 400:
                soup = bs(response.content, 'html.parser')
                table = soup.find('tbody')
                tr_list = table.find_all('tr')
                for tr in tr_list:
                    ip = tr.find_all('td')[0].text
                    port = tr.find_all('td')[1].text
                    proxy = proxy_data().from_dict({"ip": ip, "port": port})
                    # Take over only new proxies.
                    if proxy not in self.__temp_proxies:
                        logger.debug(f"Added {proxy} to be checked ")
                        self.__temp_proxies.append(proxy)
                    else:
                        logger.debug(f"{proxy} gathered was already known")
            else:
                logger.debug("Error code 400 or greater in proxy link request")

        except Exception as ex:
            logger.error(f"Unable to parse html response. Error was {ex}")
        if test:
            return self.__temp_proxies

        self.__verify_proxies(self.__temp_proxies)

    def __verify_proxies(self, proxy_lis, test=False):
        removable = []
        goodProxies = 0
        links = ["https://www.youtube.com/watch?v=FghBQsZJg4U", "https://gogs.earthsquad.global"]
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        for lineCount, proxi in enumerate(proxy_lis):
            responses = []
            if not self.firstRun:
                # When the firstRun is over and we're continuously re-reading and checking proxies we don't want to
                # consume too much bandwidth. The execution will run in a separate thread, but still 5 Seconds brea
                # sounds good.
                time.sleep(5)
            logger.debug(f"{(str(proxy_lis.index(proxi) + 1))}/ {str(len(proxy_lis))}: {proxi}")
            proxy = self.__set_proxy(proxi)
            for link in links:
                res = self.__get_response(link, proxy, headers)
                responses.append(res)
            if False in responses:
                logger.debug(f"Error code 400 or greater in {proxi}")
                if test:
                    return f"Error code 400 or greater in {proxi}"
                if proxi.ip in self.all_proxies:
                    self.remove_proxy(proxi.ip)
                if proxi in self.__temp_proxies:
                    self.__temp_proxies.remove(proxi)
                continue

            try:
                soup1 = bs(responses[0].content, 'html.parser')
                soup2 = bs(responses[1].content, 'html.parser')
                name = soup1.find('meta', {'property': 'og:title'}).get('content')
                logo = soup2.find('div', class_='logo')
                if name == None or logo == None:
                    raise ValueError('Unable to parse html response.')

                logger.debug(f"Proxy can be used for Youtube: {proxi}")
                if test:
                    return f"Proxy can be used for Youtube: {proxi}"
                if proxi.ip not in self.proxies:
                    self.proxies[proxi.ip] = proxi
                    if proxi.ip not in self.all_proxies:
                        self.all_proxies[proxi.ip] = proxi
                elif proxi.failed <= GC.PROXY_FAILCOUNTER:
                    self.proxies[proxi.ip] = proxi
                # Check, if we have at least 4 proxies in the first run of the function.
                # If yes, exit, as the function will re-run soon.
                goodProxies += 1
                if goodProxies >= self.MIN_PROXIES_FOR_FIRST_RUN and self.firstRun:
                    self.firstRun = False
                    break
            except Exception as ex:
                logger.debug(f"Proxy not usable for Youtube: {proxi}, Exception: {ex}")
                if test:
                    return f"Proxy not usable for Youtube: {proxi}, Exception: {ex}"
                if proxi.ip in self.all_proxies:
                    self.remove_proxy(proxi.ip)
                if proxi in self.__temp_proxies:
                    self.__temp_proxies.remove(proxi)
            self.__write_proxies()
        logger.info(f"Total proxies in list currently = {str(len(self.all_proxies))}")
        logger.info(f"Identified {len(self.proxies)} working proxies")
        self.__write_proxies()

    def __get_response(self, link, proxy, headers):
        try:
            response = requests.get(link, proxies=proxy, headers=headers, timeout=20)
        except Exception as ex:
            logger.debug(f"Proxy not reacting: {proxy}")
            return False
        try:
            if response.status_code >= 400:
                return False
        except:
            return False
        return response

    def __set_proxy(self, proxi):
        if proxi.type == "socks5":
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
                    # Take over all proxies from the file:
                    proxy = proxy_data().from_dict(dict(data))
                    # Take over only proxies, that used to work into __temp_proxies:
                    if int(data['failed']) < GC.PROXY_FAILCOUNTER:
                        self.__temp_proxies.append(proxy)
                    self.all_proxies[data["ip"]] = proxy
        except Exception as ex:
            logger.debug(str(ex))

    def __write_proxies(self):
        if len(self.all_proxies) > 0:
            with open("proxies.csv", 'w', newline='\n')as file:
                fl = csv.DictWriter(file, self.all_proxies[list(self.all_proxies.keys())[0]].to_dict().keys())
                fl.writeheader()
                for proxy in self.all_proxies:
                    fl.writerow(self.all_proxies[proxy].to_dict())
            logger.debug(f"Wrote list of {len(self.proxies)} proxies to CSV-File")

    def __getProxy(self):
        lMaxCount = 600
        lCount = 0
        if len(self.proxies) == 0:
            logger.info("Waiting for a working proxy.")
        while len(self.proxies) == 0 and lCount <= lMaxCount:
            lCount += 1
            time.sleep(1)
        logger.critical(f"Proxies count: {len(self.proxies)}")
        if len(self.proxies) == 0:
            logger.critical("No proxy was found. Maybe internet down?")
            raise BaseException("No proxy was found. Maybe internet down?")
        proxy = self.proxies[list(self.proxies.keys())[randint(0, len(self.proxies) - 1)]]
        proxy.Called()
        if proxy.username == "" and proxy.password == "":
            return {"ip": proxy.ip, "port": proxy.port, "type": proxy.type}
        else:
            return {
                "ip": proxy.ip, "port": proxy.port,
                "username": proxy.username, "password": proxy.password, "type": proxy.type
            }

    def random_proxy(self):
        return self.__getProxy()

    def remove_proxy(self, ip, port=None, type=None):
        try:
            logger.debug(f"Increase fail count on Proxy with type {type}: {ip}:{port}")
            self.all_proxies[ip].Failed()
            if self.all_proxies[ip].failed >= GC.PROXY_FAILCOUNTER:
                del self.proxies[ip]
                logger.debug(f"Ip {ip} removed successfully.")
        except Exception as ex:
            logger.error(str(ex))


    def testProxy(self,type, ip, port, user, password):
        return "Method not yet implemented"

    """
    # TODO Functions needed for integration test?
    def testGatherProxy(self):
        proxies = self.__gather_proxies(test=True)
        print(f"Total gathered untested proxies = {str(len(proxies))}")
        return proxies

    def testVerifyProxy(self):
        proxies_lis = []
        if len(self.__temp_proxies) > 0:
            proxies_lis = [x for x in self.__temp_proxies if not x.failed > GC.PROXY_FAILCOUNTER]
        if len(proxies_lis) < 1:
            proxies_lis = [self.testGatherProxy()]
        proxies_lis = [proxies_lis[randint(0, len(proxies_lis)-1)]]
        result = self.__verify_proxies(proxies_lis, test=True)
        return result
    """

