from TestSteps.TestStepMaster import TestStepMaster

class Beratungsprotokoll(TestStepMaster):
    def __init__(self, testcaseDataDict, browserSession):
        super().__init__(testcaseDataDict, browserSession)
        self.execute()
        self.teardown()

    def execute(self):
        self.beratungsprotokoll()

    def beratungsprotokoll(self):
        # Beratungsprotokoll - zwei Buttons klicken:
        self.browserSession.takeTime("Beratungsprotokoll")
        self.browserSession.findByAndClick(xpath='id("produktinformationsblatt-email-radio-button")')
        self.browserSession.findByAndClick(xpath="//div[@class='mat-radio-label-content'][contains(.,'nicht gewünscht')]")
        self.browserSession.findByAndClick(xpath="//button[@id='nav-component-speichern-button']")
        self.browserSession.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
        self.browserSession.findByAndClick(css="#emailOeffnen_action")
        self.browserSession.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
        self.browserSession.takeTime("Beratungsprotokoll")