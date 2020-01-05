from datetime import datetime
import baangt.base.GlobalConstants as GC
import ntpath

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
        if value[0:3] == "GC.":
            value = getattr(globals()[value.split(".")[0]], value.split(".")[1])
        return value

    @staticmethod
    def replaceAllGlobalConstantsInDict(lDict : dict):
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
            elif isinstance(item,dict):
                item = utils.replaceAllGlobalConstantsInDict(item)
            elif isinstance(item,list):
                item = utils._loopList(item)
            listOut.append(item)
        return listOut
