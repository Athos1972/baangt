from pyFETest.TestRun import TestRun
from pyFETest import GlobalConstants as GC
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
    l_testRun = TestRun("WSTV-Heartbeat")
    BrowserInterface = l_testRun.getBrowser()
    l_first = True
    (l_record, l_count) = l_testRun.getNextRecord()

    while l_record:
        try:
            kwargs = {GC.KWARGS_DATA: l_record,
                      GC.KWARGS_BROWSER: BrowserInterface}
            ProduktauswahlURL(l_record, BrowserInterface, **kwargs)
            if l_count == 1:
                Login(l_record, BrowserInterface)

            ProduktAuswahl(l_record, BrowserInterface)
            ObjektSeite(l_record, BrowserInterface)
            Empfehlungen(l_record, BrowserInterface)
            Deckungsumfang(l_record, BrowserInterface)
            Praemienauskunft(l_record, BrowserInterface)
            Beratungsprotokoll(l_record, BrowserInterface)
            VertragDaten(l_record, BrowserInterface)
            AntragsFragen(l_record, BrowserInterface)
            Vermittler(l_record, BrowserInterface)
            Dokumente(l_record, BrowserInterface)
            AntragSenden(l_record, BrowserInterface)
            l_record[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_SUCCESS
        except Exception as e:
            BrowserInterface._BrowserDriver__log(logging.CRITICAL, "Unhandled Error happened: " + str(e))
            l_record[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
            pass
        finally:
            BrowserInterface.handleWindow(0, "close")
            l_testRun.finishTestCase()
            BrowserInterface._BrowserDriver__log(logging.INFO, f"Setting Status {l_record[GC.TESTCASESTATUS]} on Testcase {l_count}")
            (l_record, l_count) = l_testRun.getNextRecord()

    l_testRun.tearDown()