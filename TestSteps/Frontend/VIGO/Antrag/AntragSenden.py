from TestSteps.CustTestStepMaster import CustTestStepMaster
from baangt import CustGlobalConstants as CGC
from baangt import GlobalConstants as GC

class AntragSenden(CustTestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()
        self.teardown()

    def execute(self):
        self.antragSenden()

    def antragSenden(self):
        # Antrag
        self.browserSession.takeTime("Antrag fertigstellen")
        self.browserSession.findByAndClick(xpath="//div[@id='fertigstellen']/div/div[2]")
        self.browserSession.takeTime("Antrag drucken")
        self.browserSession.findByAndClick(xpath="//button[@id='antrag_action']")
        self.browserSession.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]", timeout=120)
        if len(self.browserSession.errorToasts) > 0:
            self.testcaseDataDict[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_ERROR
            self.tc_finalisieren()
            return
        self.browserSession.takeTime("Antrag drucken")
        self.browserSession.findByAndClick(xpath='id("manuell_unterschreiben_action")')
        self.browserSession.sleep(0.2)
        self.browserSession.findByAndClick(xpath='//*[@id="antragsdaten-bestaetigen-select"]')
        self.browserSession.findByAndClick(xpath='//*[@id="antragsdaten-bestaetigen-uebernehmen"]')
        self.browserSession.takeTime("Warten auf Senden an Bestand Button")
        self.browserSession.findByAndClick(xpath="//button[@id='sendenAnBestand_action']")
        self.browserSession.takeTime("Warten auf Senden an Bestand Button")
        self.browserSession.takeTime("Senden an Bestand")
        self.browserSession.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]", timeout=120)
        self.testcaseDataDict[CGC.SAPPOLNR] = self.browserSession.findByAndWaitForValue(xpath='id("info-card-polizzennummer")')
        self.testcaseDataDict[CGC.VIGOGFNUMMER] = self.browserSession.findByAndWaitForValue(xpath='id("info-card-geschaeftsfallnummer")')
        self.testcaseDataDict["PRAEMIE"] = self.browserSession.findByAndWaitForValue(xpath='id("nav-component-praemie")')
        self.browserSession.takeTime("Senden an Bestand")
        self.browserSession.takeTime("Antrag fertigstellen")
        self.testcaseDataDict[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_SUCCESS
        self.tc_finalisieren()
        # Close current Application window

    def tc_finalisieren(self):
        self.testcaseDataDict[GC.TIMING_DURATION] = self.browserSession.takeTime("Testfall gesamt")
        self.browserSession.handleWindow(0, "close")