from datetime import datetime
import baangt.base.GlobalConstants as GC
import baangt.base.CustGlobalConstants as CGC
import inspect
import ntpath
import logging
import json
import sys
from pathlib import Path
from baangt.base.PathManagement import ManagedPaths

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
    def setLogLevel(level):
        logger.info(f"Changing Loglevel from {logger.level} to {level}")

        for logHandler in logger.handlers:
            logHandler.setLevel(level=level.upper())

        logger.setLevel(level=level.upper())

    @staticmethod
    def listToString(completeList):
        """
        Returns a concatenated string from a list-object
        :param completeList: any List
        :return: String
        """
        if len(completeList) > 0:
            returnString = utils.__listChildToString(completeList)

        returnString = returnString.lstrip("\n")
        return returnString

    @staticmethod
    def __listChildToString(listEntry):
        """
        Recursively going through a dict and transforming each layer into a string.
        :param listEntry:
        :return:
        """
        returnString = ""
        for entry in listEntry:
            if isinstance(entry, list):
                returnString = f"{returnString}\n{utils.__listChildToString(entry)}"
            else:
                returnString = f"{returnString}, {entry}"

        returnString = returnString.lstrip(", ")
        return returnString

    @staticmethod
    def setLocatorFromLocatorType(lLocatorType, lLocator):
        """

        @param lLocatorType: XPATH, CSS, ID, etc.
        @param lLocator: Value of the locator
        @return:
        """

        xpath = None
        css = None
        lId = None

        if lLocatorType:
            if lLocatorType == 'XPATH':
                xpath = lLocator
            elif lLocatorType == 'CSS':
                css = lLocator
            elif lLocatorType == 'ID':
                lId = lLocator

        return xpath, css, lId

    @staticmethod
    def dynamicImportOfClasses(modulePath=None, className=None, fullQualifiedImportName=None):
        """
        Will import a class from a module and return the class reference

        @param fullQualifiedImportName: Full name of Module and Class. Alternatively:
        @param modulePath: Path to module and:
        @param className: Name of the class inside the module
        @return: The class instance. If no class instance can be found the TestRun aborts hard with sys.exit
        """

        if fullQualifiedImportName:
            moduleToImport = ".".join(fullQualifiedImportName.split(".")[0:-1])
            importClass = fullQualifiedImportName.split(".")[-1]
        else:
            importClass = className
            moduleToImport = modulePath

        # The above works well for classes "franzi" and "baangt.base.franzi". Not for ".franzi"
        if not moduleToImport:
            moduleToImport = importClass

        if globals().get(importClass):
            # FIXME: Here he seems to return the module instead of the class.
            x = 1 # This never happened ever. The breakpoint didn't ever halt.
            return getattr(globals()[importClass], importClass)  # Class already imported

        try:
            mod = __import__(moduleToImport, fromlist=importClass)
            logger.debug(f"Imported class {moduleToImport}.{importClass}, result was {str(mod)}")
            retClass = getattr(mod, importClass)
        except AttributeError as e:
            logger.debug("Import didn't work. Trying something else:")
            # This was not successful. Try again with adding the class-name to the Module
            mod = __import__(moduleToImport + "." + importClass, fromlist=importClass)
            logger.debug(f"Imported class {moduleToImport}.{importClass}.{importClass}, result was {str(mod)}")
            retClass = getattr(mod, importClass)

        # If this is a class, all is good.
        if inspect.isclass(retClass):
            pass
        else:
            # Try to find the class within the module:
            for name, obj in inspect.getmembers(retClass):
                if name == importClass:
                    retClass = getattr(retClass, importClass)
                    return retClass

        if not retClass:
            logger.critical(f"Can't import module: {modulePath}.{moduleToImport}")
            sys.exit("Critical Error in Class import - can't continue. "
                     "Please maintain proper classnames in Testrundefinition.")

        return retClass

    @staticmethod
    def findFileAndPathFromPath(fileNameAndPath, basePath=None):
        """
        Tries different approaches to locate a file
        lBasePath = the Path where the script is run

        @param fileNameAndPath: Filename and potentially relative path
        @param basePath (optional): Optional basePath to look at
        @return:
        """
        lFileNameAndPath = fileNameAndPath
        if basePath:
            lBasePath = Path(basePath)
            if "~" in str(lBasePath):
                lBasePath = lBasePath.expanduser()
        else:
            lBasePath = Path(sys.argv[0]).parent    # Works in Windows
            logger.debug(f"Main Path to search for files: {lBasePath}")
            if len(str(lBasePath)) < 3:
                # Most probaby we're in pyinstaller. Let's try to find executable path
                lBasePath = Path(sys.executable).parent
                logger.debug(f"New Main Path to search for files: {lBasePath}")

        if not Path(lFileNameAndPath).exists():
            managedPaths = ManagedPaths()
            root_dir = managedPaths.getOrSetRootPath()
            if "~" in str(lFileNameAndPath):
                lFileNameAndPath = Path(lFileNameAndPath).expanduser()
                if not lFileNameAndPath.exists():
                    raise Exception(f"Can't find file {fileNameAndPath}")
            elif Path(lBasePath).joinpath(fileNameAndPath).exists():
                lFileNameAndPath = Path(lBasePath).joinpath(lFileNameAndPath)
                logger.debug(f"Found file via BasePath {str(lFileNameAndPath)}")
            elif len(Path(lFileNameAndPath).parents) == 0:
                # This is only the filename. Try with current path and a bit up
                if Path(utils.__file__).joinpath(lFileNameAndPath).exists():
                    lFileNameAndPath = Path(utils.__file__).joinpath(lFileNameAndPath)
                elif Path(utils.__file__).parent.joinpath(lFileNameAndPath).exists():
                    lFileNameAndPath = Path(utils.__file__).parent.joinpath(lFileNameAndPath)
                elif Path(utils.__file__).parent.parent.joinpath(lFileNameAndPath).exists():
                    lFileNameAndPath = Path(utils.__file__).parent.parent.joinpath(lFileNameAndPath)
                elif Path(root_dir).joinpath(lFileNameAndPath).exists():
                    lFileNameAndPath = Path(root_dir).joinpath(lFileNameAndPath)
                elif Path(root_dir).joinpath("baangt").joinpath(lFileNameAndPath).exists():
                    lFileNameAndPath = Path(root_dir).joinpath("baangt").joinpath(lFileNameAndPath)
                elif Path(root_dir).joinpath("baangt").joinpath("base").joinpath(lFileNameAndPath).exists():
                    lFileNameAndPath = Path(root_dir).joinpath("baangt").joinpath("base").joinpath(lFileNameAndPath)
                else:
                    raise Exception(f"Can't find file {fileNameAndPath}")
            else:
                raise Exception(f"Can't find file {fileNameAndPath}")
        else:
            lFileNameAndPath = Path(lFileNameAndPath)

        return str(lFileNameAndPath.absolute())

    @staticmethod
    def anything2Boolean(valueIn):
        if isinstance(valueIn, bool):
            return valueIn

        if isinstance(valueIn, int):
            return bool(valueIn)

        if isinstance(valueIn, str):
            if valueIn.lower() in ("yes", "true", "1", "ok", "x"):
                return True
            else:
                return False

        if not valueIn:
            return False

        raise TypeError(f"Anything2Boolean had a wrong value: {valueIn}. Don't know how to convert that to boolean")