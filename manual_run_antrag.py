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

if __name__ == '__main__':
    #l_testRun = TestRun("WSTV-Single")
    l_testRun = TestRun("Heartbeat")
    browserInterface = l_testRun.getBrowser()
    (l_record, l_count) = l_testRun.getNextRecord()

    while l_record:
        try:
            kwargs = {GC.KWARGS_DATA: l_record,
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
            l_record[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
            pass
        finally:
            browserInterface.handleWindow(0, "close")
            l_testRun.finishTestCase()
            browserInterface._BrowserDriver__log(logging.INFO, f"Setting Status {l_record[GC.TESTCASESTATUS]} on Testcase {l_count}")
            (l_record, l_count) = l_testRun.getNextRecord()

    l_testRun.tearDown()