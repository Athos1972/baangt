from TestSteps.TestStepMaster import TestStepMaster

class AntragSenden(TestStepMaster):
    def __init__(self, testcaseDataDict, browserSession):
        super().__init__(testcaseDataDict, browserSession)
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
        self.testcaseDataDict["SAPPOL"] = self.browserSession.findByAndWaitForValue(xpath='id("info-card-polizzennummer")')
        self.testcaseDataDict["VIGOGF#"] = self.browserSession.findByAndWaitForValue(xpath='id("info-card-geschaeftsfallnummer")')
        self.testcaseDataDict["PRAEMIE"] = self.browserSession.findByAndWaitForValue(xpath='id("nav-component-praemie")')
        self.browserSession.takeTime("Senden an Bestand")
        self.browserSession.takeTime("Antrag fertigstellen")
        self.testcaseDataDict["Dauer"] = self.browserSession.takeTime("Testfall gesamt")
