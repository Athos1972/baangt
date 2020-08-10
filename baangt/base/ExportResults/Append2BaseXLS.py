from logging import getLogger
import baangt.base.GlobalConstants as GC
from icopy2xls import Mover
from baangt.base.PathManagement import ManagedPaths

logger = getLogger("pyC")


class Append2BaseXLS:
    """
    If in the globals of the current testrun the parameter AR2BXLS (Append Results to Base XLS) is set,
    we execute baangt Move-Corresponding module accordingly.
    """
    def __init__(self, testRunInstance, resultsFileName: str=None):
        self.testRunInstance = testRunInstance
        self.resultsFileName = resultsFileName
        self.mp = ManagedPaths()

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
                fileTuples.append(self.checkAppend(file))
        else:
            fileTuples.append(self.checkAppend(lGlobals["AR2BXLS"]))

        for fileTuple in fileTuples:
            if not fileTuple:
                logger.critical("File to append results to not found (see message above")
                break
            logger.info(f"Starting to append results to: {str(fileTuple)}")
            lMover = Mover(source_file_path=self.resultsFileName,
                           source_sheet="Output",
                           destination_file_path=fileTuple[0],
                           destination_sheet=fileTuple[1].strip())
            lMover.move(filters={GC.TESTCASESTATUS:GC.TESTCASESTATUS_SUCCESS}, add_missing_columns=False)
            logger.debug(f"Appending results to {str(fileTuple)} finished")

    def checkAppend(self, file):
        lFileAndPath = self.mp.findFileInAnyPath(filename=file.split(",")[0])
        if lFileAndPath:
            return [lFileAndPath, file.split(",")[1]]
        else:
            logger.critical(f"File not found anywhere: {file.split(',')[0]}")
            return None