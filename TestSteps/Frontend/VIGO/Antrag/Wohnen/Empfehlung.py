from TestSteps.TestStepMaster import TestStepMaster
import TestSteps.CustGlobalConstants as GC

class Empfehlungen(TestStepMaster):
    def __init__(self, testcaseDataDict, browserSession):
        super().__init__(testcaseDataDict, browserSession)
        self.execute()
        self.teardown()

    def execute(self):
        self.empfehlungen()

    def empfehlungen(self):
        # Navigation "Empfehlungen":
        self.browserSession.takeTime("Empfehlungen")
        self.browserSession.findByAndClick(xpath='//*[@id="empfehlungen"]')
        self.browserSession.findByAndClick(xpath="//button[@id='empfehlungen_uebernehmen_action']")
        self.browserSession.findWaitNotVisible(xpath=GC.NG_SPINNER)
        self.browserSession.takeTime("Empfehlungen")