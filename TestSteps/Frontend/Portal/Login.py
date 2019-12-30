from TestSteps.CustTestStepMaster import CustTestStepMaster

class Login(CustTestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()

    def execute(self):
        self.login()

    def login(self):
        # Login to page
        self.browserSession.takeTime("Login")
        if "login" in self.browserSession.getURL():
            self.browserSession.findByAndSetText(css='#Ecom_User_ID', value=self.testcaseDataDict['user'])
            self.browserSession.findByAndSetText(css='#Ecom_Password', value=self.testcaseDataDict['password'])
            self.browserSession.findByAndClick(css='#loginButton2')
        self.browserSession.takeTime("Login")