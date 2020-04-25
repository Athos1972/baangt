import pytest
from os import getcwd
from pathlib import Path
from baangt.base.PDFCompare import PDFCompare, PDFCompareDetails

def __getDictStructure():
    return {"referenceID": "",
            "BLOB": "",
            "Status": "",
            "StatusText": "",
            "BLOB_OUT": "",
            "ResultText": ""}


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

def test_PDFCompare_withFileLoad():
    pdfCompare = PDFCompare()
    lFile = Path(getcwd()).joinpath("pdfs").joinpath("sample.pdf")

    lDict = {lFile: __getDictStructure()}
    lDict[lFile]["referenceID"] = "12345"

    pdfCompare.compare_multiple(lDict)

    assert len(lDict[lFile]["newUUID"]) > 0
    assert lDict[lFile]["Status"] == "OK"

def test_PDFCompare_withDataClass():
    pdfCompare = PDFCompare()
    pdfDataClass = PDFCompareDetails()
    pdfDataClass.fileName = Path(getcwd()).joinpath("pdfs").joinpath("sample.pdf")
    pdfDataClass.referenceID = "12345"

    lDict = {pdfDataClass.fileName: pdfDataClass}

    pdfCompare.compare_multiple(lDict)

    assert lDict[pdfDataClass.fileName].Status == "NOK"
    assert "Config wrong?" in lDict[pdfDataClass.fileName].StatusText

def test_PDFCompare_withWrongURL():
    pdfCompare = PDFCompare(baseURL="http://franzi.fritzi:4711")
    lFile = Path(getcwd()).joinpath("pdfs").joinpath("sample.pdf")

    lDict = {lFile: __getDictStructure()}

    pdfCompare.compare_multiple(lDict)

    assert lDict[lFile]["Status"] == "NOK"
    assert "Config wrong?" in lDict[lFile]["StatusText"]

