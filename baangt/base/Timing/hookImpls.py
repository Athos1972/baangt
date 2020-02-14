import baangt

from baangt.base.Timing.Timing import Timing

import logging

logger = logging.getLogger("pyC")


class TimingHookImpl:
    
    @baangt.hook_impl
    def timing_init(self):
        return Timing()

    @baangt.hook_impl
    def timing_takeTime(self, timingObject, timingName, forceNew=False):
        return timingObject.takeTime(timingName, forceNew)

    @baangt.hook_impl
    def timing_addAttribute(self, timingObject, attribute, value, timingSection=None):
        return timingObject.addAttribute(attribute, value, timingSection)

    @baangt.hook_impl
    def timing_takeTimeSumOutput(self, timingObject):
        return timingObject.takeTimeSumOutput()

    @baangt.hook_impl
    def timing_returnTime(self, timingObject):
        return timingObject.returnTime()

    @baangt.hook_impl
    def timing_returnTimeSegment(self, timingObject, segment):
        return timingObject.returnTimeSegment(segment)

    @baangt.hook_impl
    def timing_resetTime(self, timingObject):
        return timingObject.resetTime()





