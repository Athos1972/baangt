from TestSteps.TestStepMaster import TestStepMaster

class ProduktauswahlURL(TestStepMaster):
    def __init__(self, testcaseDataDict, browserSession):
        super().__init__(testcaseDataDict, browserSession)
        self.go2url()
        self.teardown()

    def go2url(self):
        self.browserSession.takeTime("Testfall gesamt")
        self.browserSession.goToUrl(
            f'https://{self.testcaseDataDict["Mandant"]}-{self.testcaseDataDict["base_url"]}.corpnet.at/'
            f'vigong-produktauswahl/produktauswahl/{self.testcaseDataDict["VN"]}')