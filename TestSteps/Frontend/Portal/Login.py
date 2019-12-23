from TestSteps.TestStepMaster import TestStepMaster

class Login(TestStepMaster):
    def __init__(self, testcaseDataDict, browserSession):
        super().__init__(testcaseDataDict, browserSession)
        self.execute()

    def execute(self):
        self.login()

    def login(self):
        # Login to page
        self.browserSession.takeTime("Login")
        self.browserSession.findByAndSetText(css='#Ecom_User_ID', value=self.testcaseDataDict['user'])
        self.browserSession.findByAndSetText(css='#Ecom_Password', value=self.testcaseDataDict['password'])
        self.browserSession.findByAndClick(css='#loginButton2')
        self.browserSession.takeTime("Login")