import requests
from . import GlobalConstants as GC
from TestSteps import Exceptions
import logging

logger = logging.getLogger("pyC")

class ApiHandling:
    def __init__(self):
        self.session = {}

    def getSession(self, sessionNumber=1):
        if not self.session.get(sessionNumber):
            self.session[sessionNumber] = requests.Session()
        return self.session[sessionNumber]

    def getNewSession(self, sessionNumber=None):
        if not sessionNumber:
            # fixme: Get highest Session Number, add 1, etc.
            logger.critical("Method not implemented - aborting")
            raise Exceptions.pyFETestException("Method not properly implemented")
        else:
            self.session[sessionNumber] = requests.session()

    def getURL(self, url, sessionNumber=1):
        answer = self.getSession(sessionNumber=sessionNumber).get(url=url)

        return (answer.status_code, answer.json(), answer.headers)

    @staticmethod
    def returnTestCaseStatus(status_code):
        if status_code < 300:
            return GC.TESTCASESTATUS_SUCCESS
        else:
            return GC.TESTCASESTATUS_ERROR

    def postURL(self, url, content, sessionNumber=1):
        answer = self.getSession(sessionNumber=sessionNumber).post(url=url, data=content )

        return (answer.status_code, answer.json(), dict(answer.headers))

    def setLoginData(self, userName, password, sessionNumber=1):
        self.session[sessionNumber].auth = (userName, password)

    def setHeaders(self, sessionNumber, setHeaderData):
        self.session[sessionNumber].headers.update(setHeaderData)

    def tearDown(self, sessionNumber=None):
        if not sessionNumber:
            for key, value in self.session.items():
                self.session[key].close()
        else:
            self.session[sessionNumber].close()