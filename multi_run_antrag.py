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

def one_sequence(sequenceNumber, dataRecord, currentRecordNumber, browserInterface):
    logger.info(f"Starting one_sequnce with SequenceNumber = {sequenceNumber}, "
                f"CurrentRecordNumber is {currentRecordNumber}")

    try:
        kwargs = {GC.KWARGS_DATA: dataRecord,
                  GC.KWARGS_BROWSER: browserInterface}
        ProduktauswahlURL(**kwargs)
        Login(**kwargs)
        ProduktAuswahl(**kwargs)
        ObjektSeite(**kwargs)
        Empfehlungen(**kwargs)
        Deckungsumfang(**kwargs)
        Praemienauskunft(**kwargs)
        Beratungsprotokoll(**kwargs)
        VertragDaten(**kwargs)
        AntragsFragen(**kwargs)
        Vermittler(**kwargs)
        Dokumente(**kwargs)
        AntragSenden(**kwargs)
    except Exceptions.pyFETestException as e:
        browserInterface._BrowserDriver__log(logging.CRITICAL, "Unhandled Error happened: " + str(e))
        dataRecord[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
        pass
    finally:
        browserInterface.handleWindow(0, "close")
        l_testRun.finishTestCase(browserInstance=sequenceNumber, dataRecordNumber=currentRecordNumber)
        browserInterface._BrowserDriver__log(logging.INFO,
                                             f"Setting Status {dataRecord[GC.TESTCASESTATUS]} on Testcase {currentRecordNumber}")


class ParallelExecutionOfTestcaseStarter(object):
    def __init__(self,sequenceNumber, dataRecord, tcNumber, browserInterface=None):
        self.manager = multiprocessing.Manager()
        self.process_list = self.manager.list()
        self.sequenceNumber = sequenceNumber
        self.dataRecord = dataRecord
        self.tcNumber = tcNumber
        self.browserInterface = browserInterface

    def start(self):
        one_sequence(sequenceNumber=self.sequenceNumber, dataRecord=self.dataRecord, currentRecordNumber=self.tcNumber,
                     browserInterface=self.browserInterface)

if __name__ == '__main__':
    l_testRun = TestRun("Heartbeat")
    logger = logging.getLogger('pyC')

    l_found = True
    l_numberOfRecords = 0
    l_testRecords = {}
    l_ParallelInstances = 4
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

    processes = {}
    processExecutions = {}
    # Now execute them in batches of l_ParallelInstances
    for n in range(0, l_numberOfRecords, l_ParallelInstances):
        for x in range(0, l_ParallelInstances):
            logger.debug(f"starting Process and Executions {x}. Value of n+x is {n+x}, "
                         f"RecordCounter = {l_testRecords[n+x][1]}")
            processes[x] = ParallelExecutionOfTestcaseStarter(sequenceNumber=x,
                                                              dataRecord=l_testRecords[n + x][0],
                                                              tcNumber=l_testRecords[n + x][1],
                                                              browserInterface=browserInstances[x])
            processExecutions[x] = multiprocessing.Process(target=processes[x].start)

        for x in range(0, l_ParallelInstances):
            logger.debug(f"starting Execution of Instance {x}")
            processExecutions[x].start()

        for x in range(0, l_ParallelInstances):
            logger.info(f"Starting Joining of Instance {x}")
            processExecutions[x].join()

    # Parallel geöffnete Browser killen:
    for n in range(0, l_ParallelInstances):
        logger.info(f"Closing browser instance {n}")
        l_testRun.tearDown(browserInstance=n)