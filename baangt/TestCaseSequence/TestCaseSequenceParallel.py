import multiprocessing
import logging
from baangt.TestSteps import Exceptions
from baangt.base import GlobalConstants as GC
from datetime import datetime
import time
logger = logging.getLogger("pyC")


class TestCaseSequenceParallel:
    def __init__(self, sequenceNumber, tcNumber, testcaseSequence=None, **kwargs):
        self.manager = multiprocessing.Manager()
        self.process_list = self.manager.list()
        self.sequenceNumber = sequenceNumber
        self.dataRecord = kwargs.get(GC.KWARGS_DATA)
        self.tcNumber = tcNumber
        self.testcaseSequence = testcaseSequence
        self.kwargs = kwargs

    def one_sequence(self, resultQueue: multiprocessing.Queue):
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
            self.kwargs[GC.KWARGS_TESTRUNINSTANCE].append2DTestCaseEndDateTimes(self.sequenceNumber,
                                                                                datetime.fromtimestamp(time.time()))

        except Exceptions.baangtTestStepException as e:
            logger.critical(f"Unhandled Error happened in parallel run {parallelizationSequenceNumber}: " + str(e))
            dataRecord[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
        finally:
            # the result must be pushed into the queue:
            logger.debug(
                f"Starting to Put value in Queue {currentRecordNumber}. Len of datarecord: {len(str(dataRecord))}")
            resultQueue.put({self.tcNumber: dataRecord})
            logger.debug(f"Finished putting Value i Queue for TC {currentRecordNumber}")