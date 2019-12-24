from TestSteps.TestStepMaster import TestStepMaster

class Dokumente(TestStepMaster):
    def __init__(self, testcaseDataDict, browserSession):
        super().__init__(testcaseDataDict, browserSession)
        self.dokumenteOpen()
        self.beilageBeratungsProtokollHochladen()
        self.teardown()

    def dokumenteOpen(self):
        # Dokumente
        self.browserSession.findByAndClick(xpath="//div[@id='dokumente']/div/div[2]")
        self.browserSession.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")

    def beilageBeratungsProtokollHochladen(self):
        # Upload Beilage
        self.browserSession.takeTime("Upload Beratungsprotokoll")
        self.browserSession.findByAndClick(xpath="//span[@class='mat-button-wrapper'][contains(.,'Beilage hinzufügen')]")
        self.browserSession.sleep(0.2)
        self.browserSession.findByAndClick(xpath="(//span[contains(.,'Beilagentyp')])[1]")
        if self.testcaseDataDict["Mandant"] == "WSTV":
            self.browserSession.findByAndClick(xpath="//span[contains(.,'Beratungsprotokoll (unterschrieben)')]")
        else:
            self.browserSession.findByAndClick(xpath="//span[contains(.,'Beratungsdokumentation (unterschrieben)')]")
        self.browserSession.javaScript("""

            var ancestor = document.getElementById('fileupload');

            // get all Descendent items of DOM
            descendents = ancestor.getElementsByTagName('*');

            var i, e, d;
            for (i = 0; i < descendents.length; ++i) {
                e = descendents[i];
                e.removeAttribute('style');
                e.removeAttribute('width');
                e.removeAttribute('align');
                e.removeAttribute('visibility');
            }

            """)
        self.browserSession.findByAndSetText(xpath="//input[contains(@type,'file')]",
                                             value=self.testcaseDataDict["file_praemienauskunft"])
        self.browserSession.findByAndClick(xpath='//*[@id="beilage-hinzufügen-save"]')
        self.browserSession.takeTime("Upload Beratungsprotokoll")
