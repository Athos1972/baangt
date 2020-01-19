from datetime import datetime
import baangt.base.GlobalConstants as GC
import baangt.base.CustGlobalConstants as CGC
import ntpath
import logging
import json
import sys
from pathlib import Path

logger = logging.getLogger("pyC")


class utils:
    def __init__(self):
        self.__perf_trace = {}

    @staticmethod
    def datetime_return():
        # needed, so that the datetime-module is called newly
        t = datetime.now().strftime("%Y%m%d_%H%M%S")
        return t

    @staticmethod
    def extractFileNameFromFullPath(fileAndPathName):
        return ntpath.basename(fileAndPathName)
        pass

    @staticmethod
    def sanitizeFileName(value):
        value = value.replace("'", "")
        value = value.replace('"', "")

        return value

    @staticmethod
    def replaceFieldValueWithValueOfConstant(value):
        """
        If a String reference to global Constant (e.g. GC.BROWSER_FF) is
        given, this function will replace it with the actual value (e.g. FIREFOX)
        """
        if value[0:3] == "GC." or value[0:4] == 'CGC.':
            if value[0:3] == 'GC.':
                try:
                    value = getattr(globals()[value.split(".")[0]], value.split(".")[1])
                except Exception as e:
                    logger.warning(f"Referenced variable doesn't exist: {value}")
            elif value[0:4] == 'CGC.':
                value = getattr(globals()[value.split(".")[0]], value.split(".")[1])
        return value

    @staticmethod
    def replaceAllGlobalConstantsInDict(lDict: dict):
        lDictOut = {}
        for key, value in lDict.items():
            lKey = utils.replaceFieldValueWithValueOfConstant(key)
            if isinstance(value, str):
                lDictOut[lKey] = utils.replaceFieldValueWithValueOfConstant(value)
            elif isinstance(value, dict):
                lDictOut[lKey] = utils.replaceAllGlobalConstantsInDict(value)
            elif isinstance(value, list):
                lDictOut[lKey] = utils._loopList(value)
            else:
                lDictOut[lKey] = value

        return lDictOut

    @staticmethod
    def _loopList(listIn):
        listOut = []
        for item in listIn:
            if isinstance(item, str):
                item = utils.replaceFieldValueWithValueOfConstant(item)
            elif isinstance(item, dict):
                item = utils.replaceAllGlobalConstantsInDict(item)
            elif isinstance(item, list):
                item = utils._loopList(item)
            listOut.append(item)
        return listOut

    @staticmethod
    def openJson(fileNameAndPath):
        logger.info(f"Reading Definition from {fileNameAndPath}")
        data = None
        fileNameAndPath = utils.findFileAndPathFromPath(fileNameAndPath)

        with open(fileNameAndPath) as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def findFileAndPathFromPath(fileNameAndPath):
        """
        Tries different approaches to locate a file
        basePath = the Path where the script is run

        @param fileNameAndPath:
        @return:
        """
        lFileNameAndPath = fileNameAndPath
        basePath = Path(sys.modules['__main__'].__file__).parent
        logger.debug(f"Main Path to search for files: {basePath}")

        if not Path(lFileNameAndPath).exists():
            if "~" in lFileNameAndPath:
                lFileNameAndPath = Path(lFileNameAndPath).expanduser()
            elif Path(basePath).joinpath(fileNameAndPath).exists():
                lFileNameAndPath = Path(basePath).joinpath(lFileNameAndPath)
            elif len(Path(lFileNameAndPath).parents) == 0:
                # This is only the filename. Try with current path and a bit up
                if Path(utils.__file__).joinpath(lFileNameAndPath).exists:
                    lFileNameAndPath = Path(utils.__file__).joinpath(lFileNameAndPath)
                elif Path(utils.__file__).parent.joinpath(lFileNameAndPath).exists:
                    lFileNameAndPath = Path(utils.__file__).parent.joinpath(lFileNameAndPath)
                elif Path(utils.__file__).parent.parent.joinpath(lFileNameAndPath).exists:
                    lFileNameAndPath = Path(utils.__file__).parent.parent.joinpath(lFileNameAndPath)
                else:
                    raise Exception(f"Can't find file {fileNameAndPath}")
            else:
                raise Exception(f"Can't find file {fileNameAndPath}")
        else:
            lFileNameAndPath = Path(lFileNameAndPath)

        return str(lFileNameAndPath.absolute())