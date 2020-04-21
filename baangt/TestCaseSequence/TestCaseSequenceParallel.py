import logging
from baangt.TestSteps import Exceptions
from baangt.base import GlobalConstants as GC
from datetime import datetime
import time
import gevent.queue

logger = logging.getLogger("pyC")


class TestCaseSequenceParallel:
    def __init__(self, sequenceNumber: int, tcNumber: int, testcaseSequence=None, **kwargs):
        self.sequenceNumber = sequenceNumber
        self.dataRecord = kwargs.get(GC.KWARGS_DATA)
        self.tcNumber = tcNumber
        self.testcaseSequence = testcaseSequence
        self.kwargs = kwargs
        # Add the sequence-Number of parallel runs, so that the Testcase will know, which sequence he is in.
        self.kwargs[GC.KWARGS_SEQUENCENUMBER] = sequenceNumber

    def one_sequence(self, results: gevent.queue.Queue):
        dataRecord = self.dataRecord
        currentRecordNumber = self.tcNumber
        testcaseSequence = self.testcaseSequence
        parallelizationSequenceNumber = self.sequenceNumber
        
        logger.info(f"Starting one_sequence with SequenceNumber = {parallelizationSequenceNumber}, "
                    f"CurrentRecordNumber is {currentRecordNumber}")

        if not dataRecord:
            logger.warning("dataRecord was empty - doing nothing")
            return

        try:
            self.kwargs[GC.KWARGS_TESTRUNINSTANCE].executeDictSequenceOfClasses(testcaseSequence,
                                                                                GC.STRUCTURE_TESTCASE,
                                                                                **self.kwargs)

        except Exceptions.baangtTestStepException as e:
            logger.critical(f"Unhandled Error happened in parallel run {parallelizationSequenceNumber}: " + str(e))
            dataRecord[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
        finally:
            d_t = datetime.fromtimestamp(time.time())
            results.put([{self.tcNumber: dataRecord}, {self.sequenceNumber:  [self.tcNumber, d_t]}])