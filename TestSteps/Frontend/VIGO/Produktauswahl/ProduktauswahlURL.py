from TestSteps.CustTestStepMaster import TestStepMaster
from pyFETest import GlobalConstants as GC


class ProduktauswahlURL(TestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.go2url()
        self.teardown()

    def go2url(self):
        self.browserSession.takeTime("Testfall gesamt")
        self.browserSession.goToUrl(
            f'https://{self.testcaseDataDict["Mandant"]}-{self.testcaseDataDict["base_url"]}.corpnet.at/'
            f'vigong-produktauswahl/produktauswahl/{self.testcaseDataDict["VN"]}')