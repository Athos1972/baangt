from TestSteps.TestStepMaster import TestStepMaster

class Praemienauskunft(TestStepMaster):
    def __init__(self, testcaseDataDict, browserSession):
        super().__init__(testcaseDataDict, browserSession)
        self.execute()

    def execute(self):
        self.praemienAuskunft()

    def praemienAuskunft(self):
        # Prämienauskunft - button clicken und dann weiter
        self.browserSession.takeTime("Prämienauskunft")
        self.browserSession.findByAndClick(xpath="//button[@id='praemienauskunft']")
        self.browserSession.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
        self.browserSession.findByAndClick(xpath="//mat-icon[contains(.,'keyboard_arrow_right')]")
        self.browserSession.takeTime("Prämienauskunft")