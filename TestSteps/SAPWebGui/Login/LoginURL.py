from TestSteps.CustTestStepMaster import CustTestStepMaster

class LoginURL(CustTestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()

    def execute(self):
        self.browserSession.takeTime("OpenSapGUI")
        self.browserSession.goToUrl(
            'https://sap-pcq.viennainsurancegroup.com/sap/bc/gui/sap/its/webgui')
        self.browserSession.takeTime("OpenSapGUI")
        pass