from baangt.base import GlobalConstants as GC
from datetime import timedelta
import time
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
            self.timing[timingName][GC.TIMING_END] = time.time()
            return str(timedelta(seconds=self.timing[timingName][GC.TIMING_END] - self.timing[timingName][GC.TIMING_START]))
        else:
            self.timing[timingName] = {}
            self.timing[timingName][GC.TIMING_START] = time.time()
            self.currentTimingSection = timingName
        return timingName

    def addAttribute(self, attribute, value, timingSection=None):
        if not timingSection:
            lSection = self.currentTimingSection
        else:
            lSection = timingSection

        self.timing[lSection][attribute]=value

    def takeTimeSumOutput(self):
        logger.info("Timing follows:")
        for key, value in self.timing.items():
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

    def returnTimeSegment(self, segment):
        if self.timing.get(segment):
            lStart =  time.strftime("%H:%M:%S", time.localtime(self.timing[segment][GC.TIMING_START]))
            lEnd = time.strftime("%H:%M:%S", time.localtime(self.timing[segment][GC.TIMING_END]))
            lDuration = self.__format_time(self.timing[segment])
            return lStart, lEnd, lDuration
        return None

    def resetTime(self):
        if GC.TIMING_TESTRUN in self.timing:
            buffer = self.timing.get(GC.TIMING_TESTRUN)
            self.timing = {GC.TIMING_TESTRUN: buffer}
        else:
            self.timing = {}

    @staticmethod
    def __format_time(startAndEndTimeAsDict):
        return time.strftime("%H:%M:%S", time.gmtime(startAndEndTimeAsDict[GC.TIMING_END] -
                                                        startAndEndTimeAsDict[GC.TIMING_START]))