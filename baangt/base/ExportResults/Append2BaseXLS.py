from logging import getLogger
import baangt.base.GlobalConstants as GC
from icopy2xls import

logger = getLogger("pyC")

class Append2BaseXLS:
    """
    If in the globals of the current testrun the parameter AR2BXLS (Append Results to Base XLS) is set,
    we execute baangt Move-Corresponding module accordingly.
    """
    def __init__(self, testRunInstance, resultsFileName:str=None):
        self.testRunInstance = testRunInstance
        self.resultsFileName = resultsFileName
        self._append2BaseXLS()

    def _append2BaseXLS(self):
        lGlobals = self.testRunInstance.globalSettings
        if not lGlobals.get("AR2BXLS"):
            logger.debug("No request to save to further destinations. Exiting.")
            return

        # Format: fileAndPath,Sheet;fileAndPath,sheet
        fileTuples = []
        if ";" in lGlobals.get("AR2BXLS"):
            files = lGlobals.get("AR2BXLS").split(";")
            for file in files:
                fileTuples.append(file.split(",")[0], file.split(",")[1])
        else:
            fileTuples.append([lGlobals["AR2BXLS"].split(",")[0], lGlobals["AR2BXLS"].split(",")[1]])

        for fileTuple in fileTuples:
            MC.Mover(source_file_path=self.resultsFileName,
                     source_sheet="Output",
                     destination_file_path=fileTuple[0],
                     destination_sheet=fileTuple[1])


