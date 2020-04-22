import pytest
from os import getcwd
from pathlib import Path
from baangt.base.PDFCompare import PDFCompare

def __getDictStructure():
    return {"Reference-ID": "",
            "BLOB": "",
            "Status": "",
            "StatusText": "",
            "BLOB_OUT": ""}


def test_PDFCompare_wrongInput():
    pdfCompare = PDFCompare()

    lDict = {"1234": __getDictStructure()}
    lDict["1234"].pop("Reference-ID")

    pdfCompare.compare_multiple(lDict)

    assert lDict["1234"].get("Status", None) == "NOK"


def test_PDFCompare_withFileLoad():
    pdfCompare = PDFCompare()

    lDict = {Path(getcwd()).joinpath("tests").joinpath("pdfs").joinpath("sample.pdf"): __getDictStructure()}

    pdfCompare.compare_multiple(lDict)

