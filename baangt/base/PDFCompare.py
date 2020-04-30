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
    ResultText: str = field(default="")
    Description: str = field(default="No description available from calling functionality")
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

            logger.debug(f"Comparing PDF-Files: {lDetails.fileName} with reference {lDetails.referenceID}")
            lDetails = self.__callService(file, lDetails)

            if isinstance(details, PDFCompareDetails):
                files[file] = lDetails
            else:
                files[file] = asdict(lDetails)

        return files

    def uploadNewReferenceFile(self, details: PDFCompareDetails):
        """
        Will upload the file specified in details.Filename and receive the new UUID
        :param details: filled in dataclass PDFCompareDetails
        :return: same structure. If everything went right, with a newUUID of the uploaded file.
        """

        details = self.__callService(file=None, details=details, typeOfService="createOriginal")
        return details

    def __callService(self, file : str, details: PDFCompareDetails, typeOfService="compare"):
        if not file:
            lFile = details.fileName
        else:
            lFile = file

        blobToCompare = self.__getBlobFromInput(lFile, details.BLOB)

        if not blobToCompare:
            details.Status = "NOK"
            details.StatusText = f"No input BLOB given and file {lFile} not there or can't be read."
            return details
        else:
            details.BLOB = blobToCompare

        if typeOfService == 'compare':
            details = self.__callComparisonService(details=details)
        elif typeOfService == 'createOriginal':
            details = self.__callUploadService(details=details, endpoint="/upload_reference")
        else:
            details.Status = "NOK"
            details.StatusText = f"Unknown typeOfService specified: {typeOfService}"

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
            details = self.__callComparisonServiceExecution(details)

        return details

    def __callUploadService(self, details: PDFCompareDetails, endpoint="/upload_original"):
        if endpoint == '/upload_original':
            files = {
                "original": (details.fileName, details.BLOB),
                "reference_uuid": (None, details.referenceID),
                "description": (None, details.Description)
            }
        elif endpoint == '/upload_reference':
            files = {
                "reference": (details.fileName, details.BLOB),
                "description": (None, details.Description)
            }

        lResponse = self.__executeRequest(params=None, methodGetOrPost="post", endpoint=endpoint, files=files)

        if not isinstance(lResponse, requests.Response):
            details.Status = "NOK"
            details.StatusText = f"Error when calling remote service. Config wrong? Server down? Error was: {lResponse}"
            return details

        if lResponse.status_code == 200:
            details.Status = "OK"
            lJson = lResponse.json()
            details.newUUID = lJson[0].get("uuid")
            if not details.newUUID:
                details.Status = "NOK"
                details.StatusText = f"Response didn't have UUID. Here's the response: {lResponse.text}"
        else:
            details.Status = "NOK"
            details.StatusText = f"Error {lResponse.status_code} from Request to Service. " \
                                 f"Error from service was {lResponse.text}"

        return details

    def __callComparisonServiceExecution(self, details: PDFCompareDetails):
        # Requests Comparison of the two IDs, typically after they were uploaded
        # UUID 1 = new ID of this file
        # UUID 2 = Reference ID of old file (Uploaded as a reference and given as parameter in the Testcase!
        params = {"uuid1": details.newUUID,
                  "uuid2": details.referenceID}
        lResponse = self.__executeRequest(endpoint='/comparison', params=params, methodGetOrPost="get")

        if lResponse.status_code == 200:
            details.Status = "OK"
            lJson = lResponse.json()
            if lJson["result"] == "OK":
                details.Status = "OK"
                details.StatusText = ""
            else:
                details.Status = "NOK"
                details.StatusText = "Diff in Original: " + lJson["result"]["orig_file_diff"] + \
                                     "\nDiff in Reference:" +  lJson["result"]["orig_file_diff"]
        else:
            details.Status = "NOK"
            details.StatusText = f"Error {lResponse.status_code} from Request to Service. " \
                                 f"Error from service was {lResponse.text}"

        return details

    def __executeRequest(self, endpoint, params, methodGetOrPost="get", files=None):
        lUrl = f"{self.baseURL}/{endpoint}"
        if methodGetOrPost.lower() == "post":
            try:
                lResponse = requests.post(url=lUrl, params=params, files=files)
            except ConnectionError as e:
                return e
            except Exception as e:
                logger.critical(f"New uncought exception. Should be looked into! Exception was: {e}")
                return e

        elif methodGetOrPost.lower() == "get":
            try:
                lResponse = requests.get(url=lUrl, params=params)
            except ConnectionError as e:
                return e
            except Exception as e:
                logger.critical(f"New uncought exception. Should be looked into! Exception was: {e}")
                return e
        else:
            logger.critical(f"called with wrong method: {methodGetOrPost}")

        return lResponse

    def __getBlobFromInput(self, file, blob):
        if blob:
            return blob

        lReadBinary = None

        try:
            blob = open(file, "rb").read()
            # blob = b64encode(blob)
        except FileNotFoundError as e:
            logger.critical(f"File {file} not found to read current PDF for comparison")
            return None
        except Exception as e:
            logger.critical(f"File {file} could not be decoded properly. Weird stuff though.")

        return blob
