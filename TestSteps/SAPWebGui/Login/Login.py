from TestSteps.CustTestStepMaster import CustTestStepMaster

class Login(CustTestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()

    def execute(self):
        self.browserSession.findByAndSetTextValidated(xpath='//*[@id="sap-client"]', value="110")
        self.browserSession.findByAndSetTextValidated(xpath='//*[@id="sap-user"]', value="ATBUHL_B")
        self.browserSession.findByAndSetText(xpath='//*[@id="sap-password"]', value="A0RHRrKmXXJhB25QnHVI")
        self.browserSession.findByAndClick(id="sap-language-dropdown-btn")
        self.browserSession.findByAndClick(xpath="(.//*[normalize-space(text()) and normalize-space(.)='EN'])[1]/following::td[1]")
        self.browserSession.findByAndClick(xpath='//*[@id="LOGON_BUTTON"]')