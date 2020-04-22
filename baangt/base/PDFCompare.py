import baangt.base.GlobalConstants as GC
import requests
from logging import getLogger
from base64 import b64encode

logger = getLogger("pyC")


class PDFCompare:
    def __init__(self):
        self.callParam = None

    def compare_multiple(self, files: dict):
        """

        :param files: a Dict:
                KEY = PDF-Filename and path
                "Reference-ID" of the original file to compare to
                "BLOB": The file as base64-encoded. Provide that in case it's not reachable from this class. If BLOB is
                       given, the file will not be read.
                "Status": OK, NOK
                "StatusText": Explanation in case of NOK
                "BLOB_OUT": If Status was NOK, this is the base64-encoded result PDF with marked differences.
        :return:
        """
        results = {}

        for file, details in files.items():
            details = self.__callService(file, details)
            files[file] = details

        return files

    def __callService(self, file : str, details: dict):
        blobToCompare = self.__getBlobFromInput(file, details.get("BLOB", None))

        if not blobToCompare:
            details["Status"] = "NOK"
            details["StatusText"] = f"No input BLOB given and file {file} not there or can't be read."
            return details

        self.__callComparisonService(details=details)

    def __callComparisonService(self, details: dict):

        # FIXME: details is for sure not the right thing!
        # FIXME: GET-Call might not be right
        # FIXME:

        lResponse = requests.get(url="http://localhost:5080/", params=details)
        if lResponse.status_code == 200:
            details["Status"] = "OK"
            pass
        else:
            details["Status"] = "NOK"
            details["StatusText"] = f"Error {lResponse.status_code} from Request to Service. " \
                                    f"Error was {lResponse.headers}"

        # FIXME! --> Receive the result!

    def __getBlobFromInput(self, file, blob):
        if blob:
            return blob

        lReadBinary = None

        try:
            with open(file, "rb") as readFile:
                blob = b64encode(readFile.read())
        except FileNotFoundError as e:
            logger.critical(f"File {file} not found to read current PDF for comparison")
            return None
        except Exception as e:
            logger.critical(f"File {file} could not be decoded properly. Weird stuff though.")

        return blob
