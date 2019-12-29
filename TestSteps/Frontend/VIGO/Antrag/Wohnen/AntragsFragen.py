from TestSteps.TestStepMaster import TestStepMaster

class AntragsFragen(TestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()
        self.teardown()

    def execute(self):
        self.antragsFragen()

    def antragsFragen(self):
        # Antragsfragen:
        self.browserSession.takeTime("Antragsfragen")
        self.browserSession.findByAndClick(xpath="id('vorversicherung')")
        self.browserSession.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
        self.browserSession.findByAndClick(
            xpath="//mat-radio-button[@id='vorversicherungenversicherungAbgelehnt-nein-radio-button']/label/div/div")
        self.browserSession.findByAndClick(
            xpath="//mat-radio-button[@id='vorversicherungenvertragsAnpassung-nein-radio-button']/label/div/div")
        self.browserSession.findByAndClick(
            xpath="//mat-radio-button[@id='bestehende-versicherungenweitereVertraege-nein-radio-button']/label/div/div")
        self.browserSession.findByAndClick(
            xpath="//mat-radio-button[@id='schaeden-elementarschaeden-nein-radio-button']/label/div/div")
        self.browserSession.findByAndClick(
            xpath="//mat-radio-button[@id='schaeden-weitereSchaeden-nein-radio-button']/label/div/div")
        self.browserSession.takeTime("Antragsfragen")