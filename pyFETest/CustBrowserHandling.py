from .BrowserHandling import BrowserDriver
from selenium.common.exceptions import *
import time
from datetime import datetime
import logging

class CustBrowserHandling(BrowserDriver):
    def __init__(self):
        super().__init__()
        self.zipkinIDs = {}

    def CustomHandleToasts(self):
        """
        Custom module for handling NG-Toasts
        """
        toasts = self.driver.find_elements_by_css_selector("vigong-message-display")
        if toasts.len() == 0:
            return

        # FIXME: Do something with the toasts.

        # Click on each Toast:
        for element in toasts:
            self.findByAndClick(xpath="(//mat-icon[contains(.,'close')])[1]")

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

