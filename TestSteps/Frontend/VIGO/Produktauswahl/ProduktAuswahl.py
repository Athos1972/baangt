from TestSteps.TestStepMaster import TestStepMaster

class ProduktAuswahl(TestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()
        self.teardown()

    def execute(self):
        self.ProduktAuswahl()

    def ProduktAuswahl(self):
        self.browserSession.takeTime("Produktauswahl")
        self.browserSession.handleIframe("portal-content-iframe")
        self.browserSession.findByAndSetText(xpath="//input[contains(@placeholder,'Provisionskonto')]",
                                             value=self.testcaseDataDict['vermittler'])
        self.clickRightProduct(self.testcaseDataDict["Product"],
                               self.testcaseDataDict["Mandant"],
                               self.testcaseDataDict["vermittler"])
        self.browserSession.handleIframe()
        self.browserSession.takeTime("Produktauswahl")

    def clickRightProduct(self, productName, mandant, vermittler):
        if productName.upper() == "WOHNEN" and mandant == "WSTV" :
            self.browserSession.findByAndClick(xpath='//button[@id="productWohnen"]')
        elif productName.upper() == "WOHNEN" and mandant == "DON":
            self.browserSession.findByAndClick(xpath='//button[@id="productDonWohnen"]')
        elif productName.upper() == 'RS':
            self.browserSession.findByAndClick(xpath='//button[@id="productDonRechtsschutz"]')
