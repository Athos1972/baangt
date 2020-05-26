from baangt.base import GlobalConstants as GC
from datetime import timedelta
import time
import logging
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional, Tuple

logger = logging.getLogger("pyC")


@dataclass
class Duration:
    start: float = None
    end: float = None
    timestamp: float = None
    other: dict = field(default_factory=dict)


    def clear(self):
        self.start = None
        self.end = None
        self.timestamp = None

class Timing:
    def __init__(self):
        self.timing = defaultdict(Duration)
        self.counter = Counter()
        self.current = None

    def takeTime(self, name: str, forceNew: bool = False) -> str:
        if forceNew:
            self.counter[name] += 1
            name = f'{name}_{self.counter[name] - 1}'
            
            
        duration = self.timing[name]

        if not duration.start:
            self.timing[name].start = time.time()
            self.current = name
            return name
        
        duration.end = time.time()
        elapsed = duration.end - duration.start
        return str(timedelta(seconds=elapsed))
    
    def addAttribute(self, attribute: str, value: str, 
                    section: Optional[str] = None) -> None:
        section = section or self.current
        
        if section not in self.timing:
            raise ValueError('Section not found')

        # If this is not a standard attribute of the timing class, then add it to section "other"
        if attribute not in Duration.__annotations__:
            if not self.timing[section].other.get(attribute,"nix") == "nix":
                self.timing[section].other[attribute] = \
                     self.timing[section].other[attribute] + value
            else:
                self.timing[section].other[attribute] = value
        else:
            self.timing[section].__setattr__(attribute, value)

    def takeTimeSumOutput(self) -> None:
        logger.info("Timing follows:")
        for key, value in self.timing.items():
            if not value.end:
                continue
            elapsed = value.end - value.start
            logger.info(f'{key} : {Timing.__format_time(elapsed)}')

    def returnTime(self) -> str:
        ret = ""
        for key, value in self.timing.items():
            if not value.end:
                continue

            elapsed = value.end - value.start
            ret = f'{ret}\n{key}: , since last call: ' \
                    f'{Timing.__format_time(elapsed)}'
            
            if value.timestamp:
                ret = f'{ret}, TS: {str(value.timestamp)}'

            if value.other:
                for key, object in value.other.items():
                    ret = f'{ret}, {key}:{object}'

        return ret

    def returnTimeSegment(self, section: str) -> Tuple[str, str, str]:
        duration = self.timing[section]
        if duration.end:
            start, end = map(Timing.__format_date_time, \
                (duration.start, duration.end))
            duration = Timing.__format_time(duration.end - duration.start)

            return start, end, duration

        raise ValueError('Section not found')

    def resetTime(self, name):
        testrun = self.timing.get(GC.TIMING_TESTRUN)
        for key in self.timing.keys():
            if key == testrun:
                continue
            if "TestCaseMaster" in key and key != name:
                continue
            self.timing[key].clear()
        self.counter.clear()
        if testrun:
            self.timing[GC.TIMING_TESTRUN] = testrun
        
    @staticmethod
    def __format_time(elapsed_seconds: float):
        return time.strftime("%H:%M:%S", time.gmtime(elapsed_seconds))

    @staticmethod
    def __format_date_time(elapsed_seconds: float):
        return time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(elapsed_seconds))

if __name__ == '__main__':
    test = Timing()
