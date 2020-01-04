from baangt.base.HandleDatabase import HandleDatabase
from baangt.TestCaseSequence.TestCaseSequenceParallel import TestCaseSequenceParallel
from baangt.base.Timing import Timing
import baangt.base.GlobalConstants as GC
import multiprocessing
import logging

logger = logging.getLogger("pyC")


class TestCaseSequenceMaster:
    def __init__(self, **kwargs):
        self.name = None
        self.description = None
        self.timing : Timing = kwargs.get(GC.KWARGS_TIMING)
        self.testdataDataBase: HandleDatabase = None
        self.testrunAttributes = kwargs.get(GC.KWARGS_TESTRUNATTRIBUTES)
        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.testRunName = self.testRunInstance.testRunName
        self.dataRecords = {}
        self.recordCounter = 0
        # Extract relevant data for this TestSequence:
        self.testSequenceData = self.testrunAttributes[GC.STRUCTURE_TESTCASESEQUENCE].get(
            kwargs.get(GC.STRUCTURE_TESTCASESEQUENCE))[1]
        self.recordPointer = self.testSequenceData[GC.DATABASE_FROM_LINE]
        self.testCases = self.testSequenceData[GC.STRUCTURE_TESTCASE]
        self.kwargs = kwargs
        self.timingName = self.timing.takeTime(self.__class__.__name__,forceNew=True)
        self.prepareExecution()
        if self.testSequenceData.get(GC.EXECUTION_PARALLEL, 0) > 1:
            self.execute_parallel(self.testSequenceData.get(GC.EXECUTION_PARALLEL, 0))
        else:
            self.execute()

    def prepareExecution(self):
        self.__getDatabase()
        recordPointer = 0
        # Read all Testrecords into l_testRecords:
        while True:
            self.dataRecords[recordPointer] = self.getNextRecord()
            if not self.dataRecords[recordPointer]:
                self.dataRecords.pop(recordPointer)
                recordPointer -= 1
                break
            recordPointer += 1
        logger.info(f"{recordPointer + 1} test records read for processing")

    def execute_parallel(self, parallelInstances):
        # Usually the Testcases themselves would request Browser from Testrun
        # In this case we need to request them, because the Testcases will run in their own
        # Processes
        browserInstances = {}
        for n in range(0, parallelInstances):
            # fixme: Browser should come from Testcase - not hardcoded
            browserInstances[n] = self.testRunInstance.getBrowser(browserInstance=n, browserName=GC.BROWSER_FIREFOX)

        processes = {}
        processExecutions = {}
        resultQueue = multiprocessing.Queue()

        numberOfRecords = len(self.dataRecords)
        for n in range(0, numberOfRecords, parallelInstances):
            for x in range(0, parallelInstances):
                if self.dataRecords.get(n + x):
                    logger.debug(f"starting Process and Executions {x}. Value of n+x is {n + x}, "
                                 f"Record = {str(self.dataRecords[n + x])[0:50]}")
                    self.kwargs[GC.STRUCTURE_TESTCASESEQUENCE] = self.testSequenceData
                    self.kwargs[GC.KWARGS_DATA] = self.dataRecords[n+x]
                    self.kwargs[GC.KWARGS_BROWSER] = browserInstances[x]
                    processes[x] = TestCaseSequenceParallel(sequenceNumber=x,
                                                            tcNumber=n + x,
                                                            testcaseSequence=self.testCases,
                                                            **self.kwargs)
                    processExecutions[x] = multiprocessing.Process(target=processes[x].one_sequence,
                                                                   args=(resultQueue,))
                else:
                    # This is the case when we have e.g. 4 parallel runs and 5 testcases,
                    # First iteration: all 4 are used. Second iteration: only 1 used, 3 are empty.
                    if processExecutions.get(x):
                        processExecutions.pop(x)

            for x in range(0, parallelInstances):
                logger.info(f"starting execution of parallel instance {x}")
                if processExecutions.get(x):
                    processExecutions[x].start()

            for x in range(0, parallelInstances):
                if processExecutions.get(x):
                    # Queue should be filled by now - take entries into Testrun-instance:
                    while not resultQueue.empty():
                        resultDict = resultQueue.get()
                        for recordNumber, dataRecordAfterExecution in resultDict.items():
                            self.testRunInstance.setResult(recordNumber, dataRecordAfterExecution)
                    # Quit the running parallel process:
                    logger.info(f"Stopping parallel instance {x}")
                    processExecutions[x].join()

    def execute(self):
        # Execute all Testcases:
        for key, value in self.dataRecords.items():
            # self.kwargs[GC.STRUCTURE_TESTCASESEQUENCE] = self.testSequenceData
            self.kwargs[GC.KWARGS_DATA] = value
            self.testRunInstance.executeDictSequenceOfClasses(self.testCases, GC.STRUCTURE_TESTCASE,
                                                              **self.kwargs)
            # Write Result back to TestRun for later saving in export format
            self.testRunInstance.setResult(key, value)

    def getNextRecord(self):
        self.recordCounter += 1
        if self.testdataDataBase:
            if self.recordPointer > self.testSequenceData[GC.DATABASE_TO_LINE]:
                return None
        else:
            self.__getDatabase()

        lDataRecord = self.testdataDataBase.readTestRecord(self.recordPointer)
        self.recordPointer += 1
        return lDataRecord

    def __getDatabase(self):
        if not self.testdataDataBase:
            self.testdataDataBase = HandleDatabase()
            self.testdataDataBase.read_excel(fileName=self.testSequenceData[GC.DATABASE_FILENAME],
                                             sheetName=self.testSequenceData[GC.DATABASE_SHEETNAME])
        return self.testdataDataBase

    def finishTestCase(self, browserInstance=1, dataRecordNumber=None):
        if not dataRecordNumber:
            dataRecordNumber = self.recordCounter
            logger.debug(f"DataRecordNumber = {dataRecordNumber}")
        dataRecord = self.dataRecords[dataRecordNumber]
        if not self.testRunInstance.apiInstance:
            if len(dataRecord[GC.TIMING_DURATION]) == 0:
                # This was a failed testcase - didn't reach the end. Still take overall time:
                dataRecord[GC.TIMING_DURATION] = self.testRunInstance.browser[browserInstance].takeTime(
                    "Testfall gesamt")
            dataRecord[GC.TIMELOG] = self.testRunInstance.browser[browserInstance].returnTime()
            self.testRunInstance.browser[browserInstance].takeTimeSumOutput()
            self.testRunInstance.browser[browserInstance].resetTime()
        else:
            # FIXME: Auch für API-Tests brauchen wir eine Zeitaufzeichnung
            pass
        self.testRunInstance.setResult()

    def tearDown(self):
        self.timing.takeTime(self.timingName)
        pass