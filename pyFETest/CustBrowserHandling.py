from .BrowserHandling import BrowserDriver
from selenium.common.exceptions import *
import time
from datetime import datetime
import logging
import TestSteps.Exceptions
from . import GlobalConstants as GC
from bs4 import BeautifulSoup

class CustBrowserHandling(BrowserDriver):
    def __init__(self):
        super().__init__()
        self.zipkinIDs = {}
        self.toasts = ""
        self.errorToasts = ""

    def CustomHandleToasts(self):
        """
        Custom module for handling NG-Toasts
        """
        toasts = self.driver.find_elements_by_css_selector("vigong-message-display")
        if len(toasts) == 0:
            return

        # Click on each Toast:
        for element in toasts:
            if "red" in self.__getAttributesOfElement(element):
                self.errorToasts = self.errorToasts + '\n' + element.text
                raise TestSteps.Exceptions.pyFETestException
            else:
                self.toasts = self.toasts + '\n' + element.text
            self._BrowserDriver__log(logging.INFO, "Toast handled: " + element.text)
            self.findByAndClick(xpath="(//mat-icon[contains(.,'close')])[1]")

    def __getAttributesOfElement(self, element):
        #l_attrib = self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
        properties = self.driver.execute_script('return window.getComputedStyle(arguments[0], null);', element)
        for property in properties:
            print(element.value_of_css_property(property))
        html_attribs = element.get_property("outerHTML")
        print(html_attribs)
        all_attribs = self.__getAttributesViaOuterHTML(html_attribs)
        return all_attribs

    def __getAttributesViaOuterHTML(self, html_attribs: str):
        bs = BeautifulSoup(html_attribs, 'html.parser')
        return bs.attrs

    def getToastsAsString(self):
        l_return = {'Toasts': self.toasts,
                    'ErrorToasts': self.errorToasts}
        self.toasts = ""
        self.errorToasts = ""
        return l_return

    def CustomHandleZipkin(self):
        self.findBy(xpath="//span[@title='zipkinId.requestUrl']", loggingOn=False)
        try:
            zipkinID = self.element.text.split(" ")[2]
        except StaleElementReferenceException as e:
            return

        self.zipkinIDs[zipkinID] = ""

    def CustomPrintZipkins(self):
        zipkinString = "\n".join([str(elem) for elem in self.zipkinIDs.keys()])
        self._BrowserDriver__log(logging.INFO, "Found Zipkins: " + zipkinString)

    def findWaitNotVisible(self, xpath, timeout = 90):
        self.zipkinIDs = {}
        self.CustomHandleZipkin()
        self.timing[self.currentTimingSection]["timestamp"] = datetime.now()
        self._BrowserDriver__log(logging.DEBUG, "Waiting for Element to disappear", **{"xpath":xpath, "timeout":timeout})
        time.sleep(0.5)

        stillHere = True
        elapsed = 0
        begin = time.time()

        while stillHere and elapsed < timeout:
            self.CustomHandleZipkin()
            try:
                self.element = self.driver.find_element_by_xpath(xpath)
                time.sleep(0.05)
                elapsed = time.time() - begin
            except Exception as e:
                # Element gone - exit
                stillHere = False
        self._BrowserDriver__log(logging.INFO, f"Element was gone after {elapsed} seconds")
        # Schreibt die gefundenen Zipkin-IDs in das Zeitlog mit
        self.timing[self.currentTimingSection]["zipkinIDs"] = self.zipkinIDs.keys()
        self.CustomPrintZipkins()
        self.CustomHandleToasts()

    def returnTime(self):
        # timingString = super().returnTime()
        timingString = ""
        for key,value in self.timing.items():
            if "end" in value.keys():
                timingString = timingString + "\n" + f'{key}: , since last call: ' \
                                                     f'{value[GC.TIMING_END] - value[GC.TIMING_START]}'
                if "zipkinIDs" in value.keys():
                    timingString = timingString + ", ZIDs:[" + ", ".join(value["zipkinIDs"]) + "]"
                if "timestamp" in value.keys():
                    timingString = timingString + ", TS:" + str(value["timestamp"])
        return timingString

