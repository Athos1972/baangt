from baangt.base import GlobalConstants as GC
from datetime import timedelta
from time import time
import logging

logger = logging.getLogger("pyC")

class Timing:
    def __init__(self):
        self.timing = {}
        self.currentTimingSection = None

    def takeTime(self, timingName, forceNew=False):
        if forceNew and timingName in self.timing.keys():
            for x in range(0,1000000):
                if not timingName + "_" + str(x) in self.timing.keys():
                    timingName = timingName + "_" + str(x)
                    break
        if timingName in self.timing:
            self.timing[timingName][GC.TIMING_END] = time()
            return str(timedelta(seconds=self.timing[timingName][GC.TIMING_END] - self.timing[timingName][GC.TIMING_START]))
        else:
            self.timing[timingName] = {}
            self.timing[timingName][GC.TIMING_START] = time()
            self.currentTimingSection = timingName
        return timingName

    def addAttribute(self, attribute, value, timingSection=None):
        if not timingSection:
            lSection = self.currentTimingSection
        else:
            lSection = timingSection

        self.timing[lSection][attribute]=value

    def takeTimeSumOutput(self):
        for key, value in self.timing.items():
            logger.info("Timing follows:")
            if "end" in value.keys():
                logger.info(f'{key} : {Timing.__format_time(value)}')

    def returnTime(self):
        timingString = ""
        for key,value in self.timing.items():
            if GC.TIMING_END in value.keys():
                timingString = timingString + "\n" + f'{key}: , since last call: ' \
                                                     f'{Timing.__format_time(value)}'
                if "timestamp" in value.keys():
                    timingString = timingString + ", TS:" + str(value[GC.TIMESTAMP])
        return timingString

    def resetTime(self):
        if GC.TIMING_TESTRUN in self.timing:
            buffer = self.timing.get(GC.TIMING_TESTRUN)
            self.timing = {GC.TIMING_TESTRUN: buffer}
        else:
            self.timing = {}

    @staticmethod
    def __format_time(startAndEndTimeAsDict):
        return format(startAndEndTimeAsDict[GC.TIMING_END] - startAndEndTimeAsDict[GC.TIMING_START], ".2f") + " s"