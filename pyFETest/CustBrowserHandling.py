from .BrowserHandling import BrowserDriver
from selenium.common.exceptions import *
import time
from datetime import datetime
import logging
import TestSteps.Exceptions
from . import GlobalConstants as GC
from . import CustGlobalConstants as CGC
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
        self._BrowserDriver__log(logging.INFO, f"{len(toasts)} Toasts handled")
        for element in toasts:
            if "red" in self.__getAttributesOfElement(element):
                self.errorToasts = self.errorToasts + '\n' + element.text
            else:
                self.toasts = self.toasts + '\n' + element.text
            self._BrowserDriver__log(logging.DEBUG, "Toast handled: " + element.text)
            self.findByAndClick(xpath="(//mat-icon[contains(.,'close')])[1]")

    def __getAttributesOfElement(self, element):
        html_attribs = element.get_property("outerHTML")
        style = self.__getAttributesViaOuterHTML(html_attribs)
        return style

    def __getAttributesViaOuterHTML(self, html_attribs: str):
        bs = BeautifulSoup(html_attribs, 'html.parser')
        l_attr = bs.contents[0].contents[0].attrs["style"]
        return l_attr

    def getToastsAsString(self):
        l_return = (CustBrowserHandling.__formatToasts(self.toasts),
                    CustBrowserHandling.__formatToasts(self.errorToasts))
        self.toasts = ""
        self.errorToasts = ""
        return l_return

    @staticmethod
    def __formatToasts(toast_in):
        toast_in = toast_in.replace("\ninfo\nInformation\n", "")
        toast_in = toast_in.replace("\ninfo\nEs ist ein Fehler passiert!\n", "\nFehler:")
        toast_in = toast_in.replace("\nclose", "\n")
        return toast_in

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

    def findBy(self, id = None,
               css = None,
               xpath = None,
               class_name = None,
               iframe = None,
               timeout = 60,
               loggingOn=True):

        isSuccessful = super().findBy(id = id,
               css = css,
               xpath = xpath,
               class_name = class_name,
               iframe = iframe,
               timeout = 60,
               loggingOn=loggingOn)

        if not isSuccessful:
            self.CustomHandleToasts()

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

