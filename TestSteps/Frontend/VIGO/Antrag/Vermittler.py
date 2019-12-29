from TestSteps.TestStepMaster import TestStepMaster

class Vermittler(TestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()
        self.teardown()

    def execute(self):
        self.vermittler()

    def vermittler(self):
        # Vermittler
        self.browserSession.takeTime("Vermittler")
        self.browserSession.findByAndClick(
            xpath='id("rechtliches")/div[@class="vigong-prozessnav-link-div"]/div[@class="vigong-prozessnav-link-text"]')
        self.browserSession.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
        self.browserSession.findByAndClick(
            xpath="//div[@class='mat-radio-label-content'][contains(.,'Ja, ich/wir stimme(n) zu')]")
        self.browserSession.takeTime("Vermittler")