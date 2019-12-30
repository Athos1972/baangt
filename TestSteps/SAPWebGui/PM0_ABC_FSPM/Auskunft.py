from TestSteps.CustTestStepMaster import CustTestStepMaster
from selenium.webdriver.common.keys import Keys

class Auskunft(CustTestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()

    def execute(self):
        self.browserSession.handleIframe(iframe='ITSFRAME1')
        self.browserSession.sleep(3)
        self.browserSession.findByAndSetText(xpath="//*[@id='ToolbarOkCode']", value='/N/PM0/ABC_FSPM')
        self.browserSession.findByAndSetText(xpath="//*[@id='ToolbarOkCode']", value=Keys.ENTER)
        # self.browserSession.submit()
        self.browserSession.sleep(3)
        self.browserSession.findByAndSetText(xpath="//input[@title='Policennummer']", value='4711')
        self.browserSession.findByAndClick(xpath="//*[title='Stornierte Policen einschließen']")
        self.browserSession.findByAndSetText(xpath="//input[@title='Postleitzahl des Orts']", value='4712')

        pass