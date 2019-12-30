from TestSteps.CustTestStepMaster import CustTestStepMaster

class PartnerCreate(CustTestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()

    def execute(self):
        self.browserSession.findByAndClick(xpath="//i[contains(.,'search')]")
        self.browserSession.findByAndClick(xpath="//span[@class='mat-button-text'][contains(.,'Partner anlegen')]")

        self.browserSession.findByAndSetText(xpath="//input[@placeholder='Name']",
                                             value=self.testcaseDataDict['Nachname'])
        self.browserSession.sleep(0.2)
        self.browserSession.findByAndSetText(xpath="(//input[@id='searchFieldFirstName'])[3]",
                                             value=self.testcaseDataDict['Vorname'])
        self.browserSession.findByAndClick(id='searchFieldGender')
        self.browserSession.findByAndClick(xpath="//span[contains(.,'" + self.testcaseDataDict['Geschlecht'] + "')]")

        self.browserSession.findByAndSetText(xpath="//input[contains(@formcontrolname,'birthDate')]",
                                             value=self.testcaseDataDict['Geburtsdatum'])
        self.browserSession.findByAndClick(xpath="(//button[@class='action-button search-button mat-raised-button mat-accent'])[3]")
        self.browserSession.findByAndClick(xpath="(//button[@color='vig-accent-inverse'][contains(.,'Neuen Partner anlegen')])[2]")

        # FIXME: Replace XPATHs
        self.browserSession.findByAndClick(xpath='Partner_anlegen/Page_Partnerdaten/Main_screen/slider_adressen')
        self.browserSession.findByAndClick(xpath='Partner_anlegen/Page_Partnerdaten/Main_screen/btn_AdresseHinzufuegen')
        self.browserSession.findByAndSetText(xpath='Partner_anlegen/Page_Partnerdaten/Main_screen/input_Postleitzahl',
                                             value=self.testcaseDataDict['Postleitzahl'])
        self.browserSession.findByAndSetText(xpath='Partner_anlegen/Page_Partnerdaten/Main_screen/input_Ort',
                                             value=self.testcaseDataDict['Ort'])
        self.browserSession.findByAndSetText(xpath='Partner_anlegen/Page_Partnerdaten/Main_screen/input_Strasse',
                                             value=self.testcaseDataDict['Strasse'])
        self.browserSession.findByAndSetText(xpath='Partner_anlegen/Page_Partnerdaten/Main_screen/input_Hausnummer',
                                             value=self.testcaseDataDict['Hausnummer'])
        self.browserSession.findByAndSetText(
            xpath='Partner_anlegen/Page_Partnerdaten/Main_screen/input_Stiege_stock_tuer',
            value=self.testcaseDataDict['Stiege_Stock_Tuer'])
        self.browserSession.sleep(1.0)
        self.browserSession.findByAndClick(xpath='Partner_anlegen/Page_Partnerdaten/Main_screen/btn_adresse_done')
        self.browserSession.sleep(1.0)

        self.browserSession.findByAndClick(xpath='Partner_anlegen/Page_Partnerdaten/Main_screen/btn_adresse_done')

        self.browserSession.sleep(0.5)

        self.browserSession.findByAndClick(xpath='Partner_anlegen/Page_Partnerdaten/box_weiterePartnerdaten')
        if self.testcaseDataDict['Beruf'] != '':
            self.browserSession.findByAndClick(xpath='Partner_anlegen/Page_Partnerdaten/Beruf_dropdown')
        if self.testcaseDataDict['Beruf'] == 'Student':
            self.browserSession.findByAndClick(xpath='Partner_anlegen/Page_Partnerdaten/Beruf_SchuelerStudent')

        if self.testcaseDataDict['Beruf'] == 'Karenz':
            self.browserSession.findByAndClick(xpath='Partner_anlegen/Page_Partnerdaten/Beruf_Karenz')

        if self.testcaseDataDict['Beruf'] == 'Selbständig':
            self.browserSession.findByAndClick(xpath='Partner_anlegen/Page_Partnerdaten/Beruf_selbstaendig')

        if self.testcaseDataDict['Beruf'] == 'Arbeiterin':
            self.browserSession.findByAndClick(xpath='Partner_anlegen/Page_Partnerdaten/Beruf_Arbeiterin')

        self.browserSession.findByAndClick(xpath='Partner_anlegen/Page_Partnerdaten/Main_screen/button_Anlegen')

        self.browserSession.findBy(
        xpath = 'Object Repository/Partner_anlegen/Page_Partnerdaten/Main_screen/toast_partner_angelegt', timeout=60)

        if self.browserSession.findBy(
            xpath='Object Repository/Partner_anlegen/Page_Partnerdaten/Vorlaeufige_adresse_checkbox', timeout=5):
            self.browserSession.findByAndClick(
                xpath='Object Repository/Partner_anlegen/Page_Partnerdaten/Vorlaeufige_adresse_checkbox')
        pass