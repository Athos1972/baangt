from baangt.base.BrowserHandling.BrowserHandling import BrowserDriver
from baangt.base.ProxyRotate import ProxyRotate
from baangt.base.Utils import utils
import baangt.base.GlobalConstants as GC

import logging
from os import getcwd
from time import sleep

logger = logging.getLogger("pyC")


class BrowserFactory:
    """
    This is a class, that holds the interface to browser-sessions.

    """
    def __init__(self, testrun):
        self.testrun = testrun

        self.rotatingProxiesService = None
        self.browser = {}
        self.browserInstances = {}

        self.timing = self.testrun.timing
        self.globalSettings = testrun.globalSettings
        self.browserServer = BrowserFactory.__getBrowserServer() \
            if self.globalSettings.get('TC.' + GC.EXECUTION_NETWORK_INFO) == True else None
        self.browsersMobProxies = {}

        self.__startRotatingProxies()

    def __startRotatingProxies(self):
        if self.globalSettings.get("TC.UseRotatingProxies"):
            reReadProxies = False
            if self.globalSettings.get("TC.ReReadProxies"):
                reReadProxies = True
            self.rotatingProxiesService = ProxyRotate(reReadProxies=reReadProxies)
            if self.globalSettings.get("TC.ReReadProxies"):
                self.rotatingProxiesService.recheckProxies(forever=True)

    def getBrowser(self, browserInstance=0, browserName=None, browserAttributes=None,
                         mobileType=None, mobileApp=None, desired_app=None,
                         mobile_app_setting=None, browserWindowSize = None):
        """
                This method is called whenever a browser instance (existing or new) is needed. If called without
                parameters it will create one instance of Firefox (geckodriver).

                if global setting TC.EXECUTION_SLOW is set, inform the browser instance about it.

                @param browserInstance: Number of the requested browser instance. If none is provided, always the
                                        default browser instance 0 will be returned
                @param browserName: one of the browser names (e.g. FF, Chrome) from GC.BROWSER*
                @param browserAttributes: optional Browser Attributes
                @return: the browser instance of base class BrowserDriver

                """
        if mobileType == 'True':
            logger.info(f"opening new Appium instance {browserInstance} of Appium browser {browserName}")
            self._getBrowserInstance(browserInstance=browserInstance)
            self.setBrowserProxy(browserInstance=browserInstance)
            if self.browsersMobProxies:
                browserMobProxy = self.browsersMobProxies[browserInstance]
            else:
                browserMobProxy = None
            self.browser[browserInstance].createNewBrowser(mobileType=mobileType,
                                                           mobileApp=mobileApp,
                                                           desired_app=desired_app,
                                                           mobile_app_setting=mobile_app_setting,
                                                           browserName=browserName,
                                                           desiredCapabilities=browserAttributes,
                                                           browserProxy=browserMobProxy,
                                                           browserInstance=browserInstance)
            if self.globalSettings.get("TC." + GC.EXECUTION_SLOW):
                self.browser[browserInstance].slowExecutionToggle()
            return self.browser[browserInstance]
        else:
            if self.globalSettings.get("TC.RestartBrowser"):
                if browserInstance in self.browser.keys():
                    logger.debug(f"Instance {browserInstance}: TC.RestartBrowser was set. Quitting old browser.")
                    lBrowser = self.browser[browserInstance]
                    lBrowser.closeBrowser()
                    del self.browser[browserInstance]

            if browserInstance not in self.browser.keys():
                logger.info(f"opening new instance {browserInstance} of browser {browserName}")
                self._getBrowserInstance(browserInstance=browserInstance)
                self.setBrowserProxy(browserInstance=browserInstance)
                if self.browsersMobProxies:  # Locale call of browserMob-Proxy
                    browserMobProxy = self.browsersMobProxies[browserInstance]
                else:
                    browserMobProxy = None

                randomProxy = None
                if self.globalSettings.get("TC.UseRotatingProxies"):
                    # returns a Dict of ip and port
                    randomProxy = self.rotatingProxiesService.random_proxy()

                self.browser[browserInstance].createNewBrowser(mobileType=mobileType,
                                                               mobileApp=mobileApp,
                                                               desired_app=desired_app,
                                                               mobile_app_setting=mobile_app_setting,
                                                               browserName=browserName,
                                                               desiredCapabilities=browserAttributes,
                                                               browserProxy=browserMobProxy,
                                                               browserInstance=browserInstance,
                                                               randomProxy=randomProxy)

                if self.globalSettings.get("TC." + GC.EXECUTION_SLOW):
                    self.browser[browserInstance].slowExecutionToggle()
                if browserWindowSize:
                    self.setBrowserWindowSize(self.browser[browserInstance], browserWindowSize)
                if self.globalSettings.get("TC." + GC.BROWSER_ZOOM_FACTOR):
                    self.browser[browserInstance].setZoomFactor(self.globalSettings["TC." + GC.BROWSER_ZOOM_FACTOR])
            else:
                logger.debug(f"Using existing instance of browser {browserInstance}")
            return self.browser[browserInstance]

    @staticmethod
    def setBrowserWindowSize(lBrowserInstance: BrowserDriver, browserWindowSize):
        lBrowserInstance.setBrowserWindowSize(browserWindowSize)

    def _getBrowserInstance(self, browserInstance):
        if self.testrun.classesForObjects.browserHandling:
            lClass = utils.dynamicImportOfClasses(fullQualifiedImportName=self.testrun.classesForObjects.browserHandling)

            self.browser[browserInstance] = lClass(timing=self.timing)
        else:
            # !Sic: code duplication for convenince reasons. Pure Duck-Typing would prevent where-used-list to work.
            self.browser[browserInstance] = BrowserDriver(timing=self.timing)

    @staticmethod
    def __getBrowserServer():
        from browsermobproxy import Server
        server = Server(getcwd() + GC.BROWSER_PROXY_PATH)
        logger.info("Starting browsermob proxy")
        server.start()
        return server

    def setBrowserProxy(self, browserInstance):

        sleep(1)

        proxy = self.browserServer.create_proxy() if self.browserServer else None

        if not proxy:
            return

        sleep(1)

        self.browsersMobProxies[browserInstance] = proxy

    def teardown(self):
        network_info = {}
        if not self.globalSettings.get("TC." + GC.EXECUTION_DONTCLOSEBROWSER):
            for browserInstance in self.browser.keys():
                self.browser[browserInstance].closeBrowser()

        elif self.globalSettings.get("TC." + GC.EXECUTION_DONTCLOSEBROWSER) == "False":
            for browserInstance in self.browser.keys():
                self.browser[browserInstance].closeBrowser()

        if self.browserServer:
            network_info = [info.har if info else {} for info in self.browsersMobProxies.values()]
            self.browserServer.stop()

        return network_info
