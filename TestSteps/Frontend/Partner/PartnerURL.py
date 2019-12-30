from TestSteps.CustTestStepMaster import CustTestStepMaster

class PartnerURL(CustTestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()

    def execute(self):
        self.browserSession.takeTime("OpenPortal")
        self.browserSession.goToUrl(
            f'https://{self.testcaseDataDict["Mandant"]}-{self.testcaseDataDict["base_url"]}.corpnet.at/'
            'home(overlay:dashboard)')
        self.browserSession.takeTime("OpenPortal")
        pass
