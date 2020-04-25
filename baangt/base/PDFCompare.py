import baangt.base.GlobalConstants as GC
import requests
from requests.exceptions import ConnectionError
from logging import getLogger
from base64 import b64encode
from dataclasses import dataclass, asdict, field

logger = getLogger("pyC")


@dataclass
class PDFCompareDetails:
    fileName: str = field(default="")
    referenceID: str = field(default="")
    BLOB: str = field(default="")
    Status: str = field(default="")
    StatusText: str = field(default="")
    BLOB_OUT: str = field(default="")
    ResultText: str =field(default="")
    newUUID: str = field(default="")


class PDFCompare:
    def __init__(self, baseURL="http://localhost:5000/"):
        self.callParam = None
        self.baseURL = baseURL

    def compare_multiple(self, files: dict):
        """

        :param files: a Dict:
                KEY = PDF-Filename and path
                "referenceID" of the original file to compare to
                "BLOB": The file as base64-encoded. Provide that in case it's not reachable from this class. If BLOB is
                       given, the file will not be read.
                "Status": OK, NOK
                "StatusText": Explanation in case of NOK
                "BLOB_OUT": If Status was NOK, this is the base64-encoded result PDF with marked differences.
                "ResultText": If Status = NOK, the text differences between the two PDFs
        :return:
        """
        results = {}

        for file, details in files.items():
            if isinstance(details, PDFCompareDetails):
                lDetails = details
            else:
                try:
                    details["newUUID"] = ""                                   # NewUUID shouldn't be set
                    lDetails = PDFCompareDetails(str(file), **details)        # Unpack DICT into the Dataclass
                except TypeError as e:
                    details["Status"] = "NOK"
                    details["StatusText"] = f"Wrong call to function. Technical error. One or more elements missing: {e}"
                    files[file] = details
                    continue

            lDetails = self.__callService(file, lDetails)

            if isinstance(details, PDFCompareDetails):
                files[file] = lDetails
            else:
                files[file] = asdict(lDetails)

        return files

    def __callService(self, file : str, details: PDFCompareDetails):
        blobToCompare = self.__getBlobFromInput(file, details.BLOB)

        if not blobToCompare:
            details.Status = "NOK"
            details.StatusText = f"No input BLOB given and file {file} not there or can't be read."
            return details
        else:
            details.BLOB = blobToCompare

        details = self.__callComparisonService(details=details)

        return details

    def __callComparisonService(self, details: PDFCompareDetails):
        """
            Step 1: Call Upload of new BLOB
            Step 2: Call Comparison service after having received the new BLOB
        :param details:
        :return:
        """

        details = self.__callUploadService(details)

        if details.newUUID:
            self.__callComparisonServiceExecution(details, details.newUUID)

        return details

    def __callUploadService(self, details: PDFCompareDetails, endpoint="/upload_original"):
        params = {
            "description": "no idea",
            "reference_uuid": details.referenceID
        }
        files = {
            "original": details.BLOB
        }
        lResponse = self.__executeRequest(params=params, methodGetOrPost="post", endpoint=endpoint, files=files)

        if not isinstance(lResponse, requests.Response):
            details.Status = "NOK"
            details.StatusText = f"Error when calling remote service. Config wrong? Server down? Error was: {lResponse}"
            return details

        if lResponse.status_code == 200:
            details.Status = "OK"
            pass
        else:
            details.Status = "NOK"
            details.StatusText = f"Error {lResponse.status_code} from Request to Service. " \
                                 f"Error from service was {lResponse.text}"

        return details

    def __callComparisonServiceExecution(self, details: PDFCompareDetails, compareFromUUID, compareToUUID):
        pass

    def __executeRequest(self, endpoint, params, methodGetOrPost="get", files=None):
        if methodGetOrPost.lower() == "post":
            try:
                lResponse = requests.post(url=f"{self.baseURL}/{endpoint}", params=params, files=files)
            except ConnectionError as e:
                return e
            except Exception as e:
                logger.critical(f"New uncought exception. Should be looked into! Exception was: {e}")

        elif methodGetOrPost.lower() == "get":
            pass
        else:
            logger.critical(f"called with wrong method: {methodGetOrPost}")

        return lResponse

    def __getBlobFromInput(self, file, blob):
        if blob:
            return blob

        lReadBinary = None

        try:
            blob = open(file, "rb").read()
            blob = b64encode(blob)
        except FileNotFoundError as e:
            logger.critical(f"File {file} not found to read current PDF for comparison")
            return None
        except Exception as e:
            logger.critical(f"File {file} could not be decoded properly. Weird stuff though.")

        return blob
