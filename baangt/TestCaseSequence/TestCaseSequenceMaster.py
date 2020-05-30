from baangt.base.HandleDatabase import HandleDatabase
from baangt.TestCaseSequence.TestCaseSequenceParallel import TestCaseSequenceParallel
from baangt.base.Timing.Timing import Timing
from baangt.base.Utils import utils
import baangt.base.GlobalConstants as GC
import multiprocessing
from pathlib import Path
import time
from datetime import datetime
import sys
import logging
import gevent
import gevent.queue
import gevent.pool
from baangt.base.RuntimeStatistics import Statistic

logger = logging.getLogger("pyC")


class TestCaseSequenceMaster:
    def __init__(self, **kwargs):
        self.name = None
        self.description = None
        self.timing: Timing = kwargs.get(GC.KWARGS_TIMING)
        self.testdataDataBase = None
        self.testrunAttributes = kwargs.get(GC.KWARGS_TESTRUNATTRIBUTES)
        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.testRunName = self.testRunInstance.testRunName
        self.dataRecords = {}
        # Extract relevant data for this TestSequence:
        self.testSequenceData = self.testrunAttributes[GC.STRUCTURE_TESTCASESEQUENCE].get(
            kwargs.get(GC.STRUCTURE_TESTCASESEQUENCE))[1]
        self.testCases = self.testSequenceData[GC.STRUCTURE_TESTCASE]
        self.kwargs = kwargs
        self.timingName = self.timing.takeTime(self.__class__.__name__, forceNew=True)
        self.statistics = Statistic()
        self.prepareExecution()
        if int(self.testSequenceData.get(GC.EXECUTION_PARALLEL, 0)) > 1:
            self.execute_parallel(self.testSequenceData.get(GC.EXECUTION_PARALLEL, 0))
        else:
            self.execute()

    def prepareExecution(self):
        if self.testSequenceData.get(GC.DATABASE_FROM_LINE) and not self.testSequenceData.get(GC.DATABASE_LINES, None):
            # Change old line selection format into new format:
            self.testSequenceData[
                GC.DATABASE_LINES] = f"{self.testSequenceData.get(GC.DATABASE_FROM_LINE)}-{self.testSequenceData.get(GC.DATABASE_TO_LINE)}"
            self.testSequenceData.pop(GC.DATABASE_FROM_LINE)
            self.testSequenceData.pop(GC.DATABASE_TO_LINE)
        self.__getDatabase()
        recordPointer = 0
        # Read all Testrecords into self.dataRecords:
        while True:
            self.dataRecords[recordPointer] = self.getNextRecord()
            if not self.dataRecords[recordPointer]:
                self.dataRecords.pop(recordPointer)
                recordPointer -= 1
                break
            recordPointer += 1
        logger.info(f"{recordPointer + 1} test records read for processing")
        self.statistics.total_testcases(recordPointer + 1)

    def execute_parallel(self, parallelInstances):

        parallelInstances = int(parallelInstances)

        results = gevent.queue.Queue()
        records = gevent.queue.Queue()

        for n, record in self.dataRecords.items():
            records.put((n, record))

        def single_thread(sequenceNumber):
            # Consume records
            while not records.empty():
                n, record = records.get()
                kwargs = {
                    GC.KWARGS_DATA: record,
                }
                kwargs.update(self.kwargs)

                logger.info(f"Starting parallel execution with TestRecord {n}, Details: " +
                            str({k: kwargs[GC.KWARGS_DATA][k] for k in list(kwargs[GC.KWARGS_DATA])[0:5]}))

                process = TestCaseSequenceParallel(tcNumber=n,
                                                   sequenceNumber=sequenceNumber,
                                                   testcaseSequence=self.testCases,
                                                   **kwargs)
                process.one_sequence(results)

        # Create and runconcurrent threads
        # 28.5.2020: We temporarily had a timeout here in Joinall as a few weeks back it looked like sometimes
        #            the complete job hangs indefinitely. The timeout worked for the whole testun, not for a single
        #            test case (spawn doesn't accept a timeout). Longer running test runs died - the timeout worked :)
        threads = gevent.joinall([gevent.spawn(single_thread, num)
                                  for num in range(parallelInstances)])

        # after joining all threads
        while not results.empty():
            result = results.get()
            for recordNumber, dataRecordAfterExecution in result[0].items():
                self.testRunInstance.setResult(recordNumber, dataRecordAfterExecution)
            for sequenceNumber, tcNumberAndTestEnd in result[1].items():
                self.testRunInstance.append2DTestCaseEndDateTimes(sequenceNumber, tcNumberAndTestEnd)

    def execute(self):
        # Execute all Testcases:
        for key, value in self.dataRecords.items():
            self.kwargs[GC.KWARGS_DATA] = value
            self.kwargs[GC.KWARGS_SEQUENCENUMBER] = 0  # There are no more sequences, so is always 0.
            logger.info(f"Starting execution with TestRecord {key}, Details: " +
                        str({k: self.kwargs[GC.KWARGS_DATA][k] for k in list(self.kwargs[GC.KWARGS_DATA])[0:5]}))

            # Here the testcase is started.
            self.testRunInstance.executeDictSequenceOfClasses(self.testCases, GC.STRUCTURE_TESTCASE,
                                                              **self.kwargs)
            d_t = datetime.fromtimestamp(time.time())
            self.testRunInstance.append1DTestCaseEndDateTimes(d_t)
            logger.info("execute append1DTestCaseEndDateTimes, param is {}".format(d_t))

            # Write Result back to TestRun for later saving in export format
            self.testRunInstance.setResult(key, value)
        self.statistics.update_testcase_sequence()

    def getNextRecord(self):

        if not self.testdataDataBase:
            self.__getDatabase()

        lDataRecord = self.testdataDataBase.readNextRecord()
        return lDataRecord

    def __getDatabase(self):
        if not self.testdataDataBase:
            self.testdataDataBase = HandleDatabase(globalSettings=self.testRunInstance.globalSettings,
                                                   linesToRead=self.testSequenceData.get(GC.DATABASE_LINES))
            self.testdataDataBase.read_excel(
                fileName=utils.findFileAndPathFromPath(
                    self.testSequenceData[GC.DATABASE_FILENAME],
                    basePath=str(Path(self.testRunInstance.globalSettingsFileNameAndPath).parent)),
                sheetName=self.testSequenceData[GC.DATABASE_SHEETNAME])
        return self.testdataDataBase

    def tearDown(self):
        self.timing.takeTime(self.timingName)
