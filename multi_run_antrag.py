from baangt.TestRun import TestRun
from baangt import GlobalConstants as GC
from TestSteps import Exceptions
from TestSteps.Frontend.Portal.Login import Login
from TestSteps.Frontend.VIGO.Antrag.Vermittler import Vermittler
from TestSteps.Frontend.VIGO.Antrag.Wohnen.ObjektSeite import ObjektSeite
from TestSteps.Frontend.VIGO.Antrag.Wohnen.Empfehlung import Empfehlungen
from TestSteps.Frontend.VIGO.Antrag.Wohnen.Deckungsumfang import Deckungsumfang
from TestSteps.Frontend.VIGO.Antrag.Wohnen.Praemienauskunft import Praemienauskunft
from TestSteps.Frontend.VIGO.Antrag.Wohnen.Beratungsprotokoll import Beratungsprotokoll
from TestSteps.Frontend.VIGO.Antrag.Wohnen.VertragsDaten import VertragDaten
from TestSteps.Frontend.VIGO.Antrag.Wohnen.Dokumente import Dokumente
from TestSteps.Frontend.VIGO.Produktauswahl.ProduktAuswahl import ProduktAuswahl
from TestSteps.Frontend.VIGO.Produktauswahl.ProduktauswahlURL import ProduktauswahlURL
from TestSteps.Frontend.VIGO.Antrag.Wohnen.AntragsFragen import AntragsFragen
from TestSteps.Frontend.VIGO.Antrag.AntragSenden import AntragSenden
import logging
import multiprocessing

class ParallelExecutionOfTestcaseStarter(object):
    def __init__(self,sequenceNumber, dataRecord, tcNumber, browserInterface=None, testcaseSequence=None):
        self.manager = multiprocessing.Manager()
        self.process_list = self.manager.list()
        self.sequenceNumber = sequenceNumber
        self.dataRecord = dataRecord
        self.tcNumber = tcNumber
        self.browserInterface = browserInterface
        self.testcaseSequence = testcaseSequence

    def one_sequence(self, resultQueue: multiprocessing.Queue):
        dataRecord = self.dataRecord
        currentRecordNumber = self.tcNumber
        browserInterface = self.browserInterface
        testcaseSequence = self.testcaseSequence
        parallelizationSequenceNumber = self.sequenceNumber
        logger.info(f"Starting one_sequence with SequenceNumber = {parallelizationSequenceNumber}, "
                    f"CurrentRecordNumber is {currentRecordNumber}")

        if not dataRecord:
            logger.warning("dataRecord was empty - doing nothing")
            return

        try:
            kwargs = {GC.KWARGS_DATA: dataRecord,
                      GC.KWARGS_BROWSER: browserInterface}
            for key, value in testcaseSequence.items():
                logger.info(f"Starting testcaseSequence: {key}, {value} ")
                l_class = globals()[value]  # Value holds the Class name
                l_class(**kwargs)  # Executes the class init
        except Exceptions.pyFETestException as e:
            browserInterface._BrowserDriver__log(logging.CRITICAL, "Unhandled Error happened: " + str(e))
            dataRecord[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
        finally:
            # the result must be pushed into the queue:
            logger.debug(f"Starting to Put value in Queue {currentRecordNumber}. Len of datarecord: {len(str(dataRecord))}")
            resultQueue.put({self.tcNumber: dataRecord})
            logger.debug(f"Finished putting Value i Queue for TC {currentRecordNumber}")

if __name__ == '__main__':
    l_testRun = TestRun("Heartbeat")
    logger = logging.getLogger('pyC')

    l_found = True
    l_numberOfRecords = 0
    l_testRecords = {}
    l_ParallelInstances = l_testRun.getParallelizationCount()
    # Read all Testrecords into l_testRecords:
    while l_found:
        l_testRecords[l_numberOfRecords] = l_testRun.getNextRecord()
        if not l_testRecords[l_numberOfRecords][0]:
            l_found = False
            break
        l_numberOfRecords += 1
    logger.info(f"{l_numberOfRecords} test records read for processing")

    # Create Browser-Instances
    browserInstances = {}
    for n in range(0, l_ParallelInstances):
        browserInstances[n] = l_testRun.getBrowser(browserInstance=n)

    testcaseSequence = l_testRun.getTestcaseSequence()

    processes = {}
    processExecutions = {}
    resultQueue = multiprocessing.Queue()
    # Now execute them in batches of l_ParallelInstances
    for n in range(0, l_numberOfRecords, l_ParallelInstances):
        for x in range(0, l_ParallelInstances):
            if l_testRecords.get(n+x):
                logger.debug(f"starting Process and Executions {x}. Value of n+x is {n+x}, "
                             f"RecordCounter = {l_testRecords[n+x][1]}")
                processes[x] = ParallelExecutionOfTestcaseStarter(sequenceNumber=x,
                                                                  dataRecord=l_testRecords[n + x][0],
                                                                  tcNumber=l_testRecords[n + x][1],
                                                                  browserInterface=browserInstances[x],
                                                                  testcaseSequence=testcaseSequence)
                processExecutions[x] = multiprocessing.Process(target=processes[x].one_sequence, args=(resultQueue,))
            else:
                # This is the case when we have e.g. 4 parallel runs and 5 testcases,
                # First iteration: all 4 are used. Second iteration: only 1 used, 3 are empty.
                processExecutions.pop(x)

        for x in range(0, l_ParallelInstances):
            logger.info(f"starting execution of parallel instance {x}")
            if processExecutions.get(x):
                processExecutions[x].start()

        for x in range(0, l_ParallelInstances):
            if processExecutions.get(x):
                # Queue should be filled by now - take entries into Testrun-instance:
                while not resultQueue.empty():
                    resultDict = resultQueue.get()
                    for recordNumber, dataRecordAfterExecution in resultDict.items():
                        l_testRun.setResult(recordNumber, dataRecordAfterExecution)
                # Quit the running parallel process:
                logger.info(f"Stopping parallel instance {x}")
                processExecutions[x].join()

    # close all opened browsers:
    for n in range(0, l_ParallelInstances):
        logger.info(f"Closing browser instance {n}")
        l_testRun.tearDown(browserInstance=n)