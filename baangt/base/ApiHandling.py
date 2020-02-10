import requests
from baangt.base import GlobalConstants as GC
from baangt.TestSteps import Exceptions
import logging
import json

logger = logging.getLogger("pyC")


class ApiHandling:
    def __init__(self):
        """
        This class handles Session Management for API-Calls
        """
        self.session = {}
        self.baseURL = None
        self.endPoint = None
        self.answerStatusCode = None
        self.answerHeaders = None
        self.answerJSON = None

    def getSession(self, sessionNumber=1):
        if not self.session.get(sessionNumber):
            self.session[sessionNumber] = requests.Session()
        return self.session[sessionNumber]

    def getNewSession(self, sessionNumber=None):
        if not sessionNumber:
            # fixme: Get highest Session Number, add 1, etc.
            logger.critical("Method not implemented - aborting")
            raise Exceptions.baangtTestStepException("Method not properly implemented")
        else:
            self.session[sessionNumber] = requests.session()

    def getURL(self, url=None, sessionNumber=1):
        url = self.__retrieveURL(url)
        answer = self.getSession(sessionNumber=sessionNumber).get(url=url)

        self.__saveAnswerLocally(answer=answer, sessionNumber=sessionNumber)

        return self.session[sessionNumber].answerStatusCode, \
               self.session[sessionNumber].answerJSON, \
               self.session[sessionNumber].answerHeaders

    @staticmethod
    def returnTestCaseStatus(status_code):
        if status_code < 300:
            return GC.TESTCASESTATUS_SUCCESS
        else:
            return GC.TESTCASESTATUS_ERROR

    def __saveAnswerLocally(self, answer, sessionNumber):
        self.session[sessionNumber].answerStatusCode = answer.status_code
        self.session[sessionNumber].answerJSON = answer.json()
        self.session[sessionNumber].answerHeaders = dict(answer.headers)

    def postURL(self, url=None, content=None, sessionNumber=1):
        url = self.__retrieveURL(url)
        logger.info(f"POST to url: {url} with content: {content}")
        content = ApiHandling.__cnvtString2Dict(content)
        if isinstance(content, str):
            # Convert content into JSON-Format, if leading and trailing {}
            if content[0] == "{" and content[-1] == "}":
                content = json.loads(content)
        answer = self.getSession(sessionNumber=sessionNumber).post(url=url, data=content)

        self.__saveAnswerLocally(answer=answer, sessionNumber=sessionNumber)

        return self.session[sessionNumber].answerStatusCode, \
               self.session[sessionNumber].answerJSON, \
               self.session[sessionNumber].answerHeaders

    @staticmethod
    def __cnvtString2Dict(content):
        if isinstance(content, str):
            # Convert content into JSON-Format, if leading and trailing {}
            if content[0] == "{" and content[-1] == "}":
                content = json.loads(content)

        return content

    def setLoginData(self, userName, password, sessionNumber=1):
        self.session[sessionNumber].auth = (userName, password)

    def setHeaders(self, sessionNumber=1, setHeaderData=None):
        setHeaderData = ApiHandling.__cnvtString2Dict(setHeaderData)
        self.session[sessionNumber].headers.update(setHeaderData)

    def tearDown(self, sessionNumber=None):
        if not sessionNumber:
            for key, value in self.session.items():
                self.session[key].close()

    def __retrieveURL(self, url):
        """

        @param url: Importing parameter - maybe an Endpoint-URL
        @return: either the passed URL or the combination of BaseURL + Endpoint.
        """
        if url:
            return url

        url = self.baseURL + self.endPoint
        return url

    def setBaseURL(self, url):
        self.baseURL = url

    def setEndPoint(self, endpoint):
        self.endPoint = endpoint
