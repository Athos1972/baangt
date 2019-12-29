from TestSteps.TestStepMaster import TestStepMaster
from TestSteps import CustGlobalConstants as CGC

class Praemienauskunft(TestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()
        self.teardown()

    def execute(self):
        self.praemienAuskunft()

    def praemienAuskunft(self):
        # Prämienauskunft - button clicken und dann weiter
        self.browserSession.takeTime("Prämienauskunft")
        self.browserSession.findByAndClick(xpath="//div[@id='berechnen']")
        self.browserSession.findWaitNotVisible(xpath=CGC.NG_SPINNER)
        self.browserSession.findByAndClick(xpath="//button[@id='praemienauskunft']")
        self.browserSession.findWaitNotVisible(xpath=CGC.NG_SPINNER)
        self.browserSession.findByAndClick(xpath="//mat-icon[contains(.,'keyboard_arrow_right')]")
        self.browserSession.takeTime("Prämienauskunft")