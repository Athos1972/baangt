from TestSteps.CustTestStepMaster import CustTestStepMaster
import TestSteps.CustGlobalConstants as GC

class Empfehlungen(CustTestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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