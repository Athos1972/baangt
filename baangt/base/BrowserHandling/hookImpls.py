import baangt

from baangt.base.BrowserHandling.BrowserHandling import BrowserDriver
from baangt.base import GlobalConstants as GC
import logging

logger = logging.getLogger("pyC")


class BrowserDriverHookImpl:
    @baangt.hook_impl
    def browserDriver_init(self, timing=None, screenshotPath=None):
        return BrowserDriver(timing, screenshotPath)

    @baangt.hook_impl
    def browserDriver_createNewBrowser(self, browserDriverObject, browserName=GC.BROWSER_FIREFOX,
                                       desiredCapabilities=None, **kwargs):
        return browserDriverObject.createNewBrowser(browserName=browserName,
                                                    desiredCapabilities=desiredCapabilities, **kwargs)

    @baangt.hook_impl
    def browserDriver_slowExecutionToggle(self, browserDriverObject, newSlowExecutionWaitTimeInSeconds=None):
        return browserDriverObject.slowExecutionToggle(newSlowExecutionWaitTimeInSeconds)

    @baangt.hook_impl
    def browserDriver_closeBrowser(self, browserDriverObject):
        return browserDriverObject.closeBrowser()

    @baangt.hook_impl
    def browserDriver_takeScreenshot(self, browserDriverObject, screenShotPath=None):
        return browserDriverObject.takeScreenshot(screenShotPath)

    @baangt.hook_impl
    def browserDriver_handleIframe(self, browserDriverObject, iframe=None):
        return browserDriverObject.handleIframe(iframe)

    @baangt.hook_impl
    def browserDriver_handleWindow(self, browserDriverObject, windowNumber=None, function=None):
        return browserDriverObject.handleWindow(windowNumber, function)

    @baangt.hook_impl
    def browserDriver_findByAndWaitForValue(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None,
                                            iframe=None, timeout=20,
                                            optional=False):
        return browserDriverObject.findByAndWaitForValue(id, css, xpath, class_name,
                                            iframe, timeout,
                                            optional)

    @baangt.hook_impl
    def browserDriver_findByAndSetText(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None,
                                       value=None, iframe=None,
                                       timeout=60, optional=False):
        return browserDriverObject.findByAndSetText(id, css, xpath, class_name, value,
                                                    iframe, timeout,
                                                    optional)

    @baangt.hook_impl
    def browserDriver_findByAndSetTextIf(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None,
                                         value=None, iframe=None,
                                         timeout=60):
        return browserDriverObject.findByAndSetTextIf(id, css, xpath, class_name,
                                         value, iframe,
                                         timeout)

    @baangt.hook_impl
    def browserDriver_findByAndSetTextValidated(self, browserDriverObject, id=None,
                                                css=None,
                                                xpath=None,
                                                class_name=None,
                                                value=None,
                                                iframe=None,
                                                timeout=60,
                                                retries=5):
        return browserDriverObject.findByAndSetTextValidated(id,
                                                css,
                                                xpath,
                                                class_name,
                                                value,
                                                iframe,
                                                timeout,
                                                retries)

    @baangt.hook_impl
    def browserDriver_submit(self, browserDriverObject):
        return browserDriverObject.submit()

    @baangt.hook_impl
    def browserDriver_findByAndClick(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None,
                                     iframe=None, timeout=20, optional=False):
        return browserDriverObject.findByAndClick(id, css, xpath, class_name,
                                     iframe, timeout, optional)

    @baangt.hook_impl
    def browserDriver_findByAndClickIf(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None,
                                       iframe=None, timeout=60,
                                       value=None, optional=False):
        return browserDriverObject.findByAndClickIf(id, css, xpath, class_name,
                                       iframe, timeout,
                                       value, optional)

    @baangt.hook_impl
    def browserDriver_findByAndForceText(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None,
                                         value=None,
                                         iframe=None, timeout=60, optional=False):
        return browserDriverObject.findByAndForceText(id, css, xpath, class_name,
                                         value,
                                         iframe, timeout, optional)

    @baangt.hook_impl
    def browserDriver_findBy(self, browserDriverObject, id=None, css=None, xpath=None, class_name=None, iframe=None,
                             timeout=60, loggingOn=True,
                             optional=False):
        return browserDriverObject.findBy(id, css, xpath, class_name, iframe,
                             timeout, loggingOn,
                             optional)

    @baangt.hook_impl
    def browserDriver_getURL(self, browserDriverObject):
        return browserDriverObject.getURL()

    @baangt.hook_impl
    def browserDriver_findWaitNotVisible(self, browserDriverObject, xpath=None, id=None, timeout=90):
        return browserDriverObject.findWaitNotVisible(xpath, id, timeout)

    @baangt.hook_impl
    def browserDriver_sleep(self, browserDriverObject, sleepTimeinSeconds):
        return browserDriverObject.sleep(sleepTimeinSeconds)

    @baangt.hook_impl
    def browserDriver_goToUrl(self, browserDriverObject, url):
        return browserDriverObject.goToUrl(url)

    @baangt.hook_impl
    def browserDriver_goBack(self, browserDriverObject):
        return browserDriverObject.goBack()

    @baangt.hook_impl
    def browserDriver_javaScript(self, browserDriverObject, jsText):
        return browserDriverObject.javaScript(jsText)


