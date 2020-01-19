from baangt.base.HandleDatabase import HandleDatabase
from baangt.TestCaseSequence.TestCaseSequenceParallel import TestCaseSequenceParallel
from baangt.base.Timing import Timing
from baangt.base.utils import utils
import baangt.base.GlobalConstants as GC
import multiprocessing
from pathlib import Path
import logging

logger = logging.getLogger("pyC")


class TestCaseSequenceMaster:
    def __init__(self, **kwargs):
        self.name = None
        self.description = None
        self.timing : Timing = kwargs.get(GC.KWARGS_TIMING)
        self.testdataDataBase = None
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
        if int(self.testSequenceData.get(GC.EXECUTION_PARALLEL, 0)) > 1:
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
        parallelInstances = int(parallelInstances)
        browserInstances = {}
        for n in range(0, int(parallelInstances)):
            # fixme: Browser should come from Testcase - not hardcoded. It's not that easy, as we might have many
            # fixme: Testcases, some Browser, some API and we might even have different browsers. For now we'll only
            # fixme: take Browser from globals-file
            lBrowserName = self.testRunInstance.globalSettings.get("TC.Browser", GC.BROWSER_FIREFOX)
            lBrowserAttributes = self.testRunInstance.globalSettings.get("TC." + GC.BROWSER_ATTRIBUTES, None)
            browserInstances[n] = self.testRunInstance.getBrowser(browserInstance=n,
                                                                  browserName=lBrowserName,
                                                                  browserAttributes=lBrowserAttributes)

        processes = {}
        processExecutions = {}
        resultQueue = multiprocessing.Queue()

        numberOfRecords = len(self.dataRecords)
        for n in range(0, numberOfRecords, parallelInstances):
            for x in range(0, parallelInstances):
                if self.dataRecords.get(n + x):
                    logger.debug(f"starting Process and Executions {x}. Value of n+x is {n + x}, "
                                 f"Record = {str(self.dataRecords[n + x])[0:50]}")
                    self.kwargs[GC.KWARGS_DATA] = self.dataRecords[n+x]
                    # Prints the first 5 fields of the data record into the log:
                    logger.info(f"Starting parallel execution with TestRecord {n+x}, Details: " +
                        str({k: self.kwargs[GC.KWARGS_DATA][k] for k in list(self.kwargs[GC.KWARGS_DATA])[0:5]}))
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
            self.kwargs[GC.KWARGS_DATA] = value
            logger.info(f"Starting execution with TestRecord {key}, Details: " +
                        str({k: self.kwargs[GC.KWARGS_DATA][k] for k in list(self.kwargs[GC.KWARGS_DATA])[0:5]}))
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
            self.testdataDataBase = HandleDatabase(globalSettings=self.testRunInstance.globalSettings)
            self.testdataDataBase.read_excel(
                fileName=utils.findFileAndPathFromPath(
                    self.testSequenceData[GC.DATABASE_FILENAME],
                    basePath=str(Path(self.testRunInstance.globalSettingsFileNameAndPath).parent)),
                sheetName=self.testSequenceData[GC.DATABASE_SHEETNAME])
        return self.testdataDataBase

    def tearDown(self):
        self.timing.takeTime(self.timingName)
        pass
