import pytest
from os import getcwd
from pathlib import Path
from baangt.base.PDFCompare import PDFCompare, PDFCompareDetails
import socket

"""
#####################
### Attention #######
#####################
# Before you run these tests, you'll have to run **flask run** in PDF-Comparison service on local host, or most of these
# Tests will be skipped.

# To do so (first start)
git clone https://gogs.earthsquad.global/athos/baangt-PDFComparison
cd baangt-PDFComparison
virtualenv venv
source venv/bin/activate
pip install -r pdf_comaprison_flask_api/requirements.txt

# Everytime:
cd pdf_comaprison_flask_api
export FLASK_APP=app.py 
flask run 
"""

newOriginalFile1_UUID = None     # UUID of new example file 1

def __checkSocketOpen() -> bool:
    aSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = aSocket.connect_ex(("127.0.0.1", 5000))
    aSocket.close()
    if result == 0:
        return True
    else:
        return False

lPortOpen = __checkSocketOpen()


def __getDictStructure():
    return {"referenceID": "",
            "BLOB": "",
            "Status": "",
            "StatusText": "",
            "BLOB_OUT": "",
            "ResultText": ""}

def __uploadNewFiles():
    global newOriginalFile2_UUID
    global newOriginalFile1_UUID
    newOriginalFile1_UUID = __uploadNewFile(Path(getcwd()).joinpath("tests").joinpath("pdfs").joinpath("sample.pdf"))


def __uploadNewFile(fileNameAndPath):
    lFileDetails = PDFCompareDetails()
    lFileDetails.fileName = str(fileNameAndPath)
    lPDFCompare = PDFCompare()
    lFileDetails = lPDFCompare.uploadNewReferenceFile(lFileDetails)
    assert lFileDetails.Status == "OK"
    return lFileDetails.newUUID


@pytest.mark.skipif(lPortOpen==False, reason="PDF-Comparison service not available")
def test_UploadNewFilesForTests():
    __uploadNewFiles()
    assert newOriginalFile1_UUID

def test_PDFCompare_wrongInput():
    pdfCompare = PDFCompare()

    lDict = {"1234": __getDictStructure()}
    # Remove ReferenceID - should give an error during call
    lDict["1234"].pop("referenceID")

    pdfCompare.compare_multiple(lDict)

    assert lDict["1234"].get("Status", None) == "NOK"

def test_PDFCompare_withWrongFile():
    pdfCompare = PDFCompare()
    lDict = {"pdfThatdoesntExist.pdf": __getDictStructure()}

    pdfCompare.compare_multiple(lDict)

    assert lDict["pdfThatdoesntExist.pdf"]["Status"] == 'NOK'


@pytest.mark.skipif(lPortOpen==False, reason="PDF-Comparison service not available")
def test_PDFCompare_withFileLoadOK():
    pdfCompare = PDFCompare()
    lFile = Path(getcwd()).joinpath("tests").joinpath("pdfs").joinpath("sample.pdf")

    lDict = {lFile: __getDictStructure()}
    lDict[lFile]["referenceID"] = newOriginalFile1_UUID

    pdfCompare.compare_multiple(lDict)

    assert len(lDict[lFile]["newUUID"]) > 0
    assert lDict[lFile]["Status"] == "OK"


@pytest.mark.skipif(lPortOpen==False, reason="PDF-Comparison service not available")
def test_PDFCompare_withFileLoadNOK():
    pdfCompare = PDFCompare()
    lFile = Path(getcwd()).joinpath("tests").joinpath("pdfs").joinpath("sample2.pdf")

    lDict = {lFile: __getDictStructure()}
    lDict[lFile]["referenceID"] = newOriginalFile1_UUID

    pdfCompare.compare_multiple(lDict)

    assert len(lDict[lFile]["newUUID"]) > 0
    assert lDict[lFile]["Status"] == "NOK"


def test_PDFCompare_withDataClass():
    pdfCompare = PDFCompare()
    pdfDataClass = PDFCompareDetails()
    pdfDataClass.fileName = Path(getcwd()).joinpath("tests").joinpath("pdfs").joinpath("sample.pdf")
    pdfDataClass.referenceID = "12345"

    lDict = {pdfDataClass.fileName: pdfDataClass}

    pdfCompare.compare_multiple(lDict)

    assert lDict[pdfDataClass.fileName].Status == "NOK"
    assert "Config wrong?" in lDict[pdfDataClass.fileName].StatusText


def test_PDFCompare_withWrongURL():
    pdfCompare = PDFCompare(baseURL="http://franzi.fritzi:4711")
    lFile = Path(getcwd()).joinpath("tests").joinpath("pdfs").joinpath("sample.pdf")

    lDict = {lFile: __getDictStructure()}

    pdfCompare.compare_multiple(lDict)

    assert lDict[lFile]["Status"] == "NOK"
    assert "Config wrong?" in lDict[lFile]["StatusText"]

