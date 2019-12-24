from TestSteps.TestStepMaster import TestStepMaster

class VertragDaten(TestStepMaster):
    def __init__(self, testcaseDataDict, browserSession):
        super().__init__(testcaseDataDict, browserSession)
        self.execute()
        self.teardown()

    def execute(self):
        self.VertragsDatenGoTo()

    def VertragsDatenGoTo(self):
        # Vertragsdaten, VN, Zahlung
        self.browserSession.findByAndClick(
            xpath="//div[@class='vigong-prozessnav-link-text'][contains(.,'Vertragsdaten, VN, Zahlung')]")
        self.browserSession.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
        self.browserSession.findByAndClick(xpath="//div[@class='mat-radio-label-content'][contains(.,'Zahlschein')]")