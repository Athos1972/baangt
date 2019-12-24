from TestSteps.TestStepMaster import TestStepMaster

class ObjektSeite(TestStepMaster):

    def __init__(self, testcaseDataDict, browserSession):
        super().__init__(testcaseDataDict, browserSession)
        self.execute()
        self.teardown()

    def execute(self):
        self.objektSeite()
        self.hausHalt()
        self.eigenheim()

    def objektSeite(self):
        # Risikoseite
        self.browserSession.takeTime("Risiko")
        self.browserSession.takeTime("Haushalt")
        self.browserSession.handleWindow(1)
        self.browserSession.handleIframe('portal-content-iframe')
        self.browserSession.findByAndClick(css='.vigong-selection-panel-zonen-button')
        self.browserSession.sleep(0.2)
        self.browserSession.findByAndClick(xpath='//button[contains(.,"OK")]')

    def hausHalt(self):
        # Haushalt anlegen
        if self.testcaseDataDict["inh_create"] == 'X':
            self.browserSession.findByAndClick(xpath='//button[@id="inhalt-hinzufuegen-action"]')
            self.browserSession.findByAndSetText(xpath='//input[@id="inhalt-form-wohnnutzflaeche"]',
                          value=self.testcaseDataDict['inh_m2'])
            self.browserSession.findByAndClick(xpath='id("inhalt-form-gebeaudebezeichnung-select")')
            self.browserSession.findByAndClick(
                xpath="//span[@class='mat-option-text'][contains(.,'" + self.testcaseDataDict['inh_gebart'] + "')]")
            self.browserSession.findByAndClick(xpath='id("inhalt-form-nutzung-select")')
            self.browserSession.findByAndClick(
                xpath="//span[@class='mat-option-text'][contains(.,'" + self.testcaseDataDict['inh_nutzung'] + "')]")
            self.browserSession.takeTime("Haushalt")

            if self.testcaseDataDict['inh_outdoorsport'] == 'X':
                self.browserSession.findByAndClick(xpath='id("inhalt-beratung-aussage-checkbox-FREIZEIT")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')

            if self.testcaseDataDict['inh_elektronik'] == 'X':
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='inhalt-beratung-aussage-checkbox-ELEKTRONIK']/label/div")

            if self.testcaseDataDict['inh_haustechnik'] == 'X':
                self.browserSession.findByAndClick(xpath='id("inhalt-beratung-aussage-checkbox-HAUSTECHNIK")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')

            if self.testcaseDataDict['inh_heizung'] == 'X':
                self.browserSession.findByAndClick(xpath='id("inhalt-beratung-aussage-checkbox-HEIZUNGSANLAGE")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')

            if self.testcaseDataDict['inh_kinder'] == 'X':
                self.browserSession.findByAndClick(xpath='id("inhalt-beratung-aussage-checkbox-HAUSHALT_KIND")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')

            if self.testcaseDataDict['inh_pferde'] == 'X':
                self.browserSession.findByAndClick(xpath='id("inhalt-beratung-aussage-checkbox-TIERE_PFERD")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')

            if self.testcaseDataDict['inh_hunde'] == 'X':
                self.browserSession.findByAndClick(xpath='id("inhalt-beratung-aussage-checkbox-TIERE_HUND")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')

            if self.testcaseDataDict['inh_alarmanlage'] == 'X':
                self.browserSession.findByAndClick(xpath='id("inhalt-form-alarmanlage-checkbox")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')

            if self.testcaseDataDict['inh_brandmeldeanlage'] == 'X':
                self.browserSession.findByAndClick(xpath='id("inhalt-form-alarmanlage-brandmeldeanlage")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')

            if self.testcaseDataDict['inh_pool'] == 'X':
                self.browserSession.findByAndClick(xpath='id("inhalt-beratung-aussage-checkbox-SWIMMINGPOOL")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')

            if self.testcaseDataDict['inh_sicherheitstuere'] == 'X':
                self.browserSession.findByAndClick(xpath='id("inhalt-form-alarmanlage-sicherheitstuere")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')

            if self.testcaseDataDict['inh_smartHome'] == 'X':
                self.browserSession.findByAndClick(xpath='id("inhalt-form-alarmanlage-smartHome")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')

            if self.testcaseDataDict['inh_don_elektronik'] == 'X':
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='inhalt-beratung-aussage-checkbox-ELEKTRONIK']/label/div")

            if self.testcaseDataDict['inh_don_haustechnik'] == 'X':
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='inhalt-beratung-aussage-checkbox-HAUSTECHNIK']/label/div")

            if self.testcaseDataDict['inh_don_heizung'] == 'X':
                self.browserSession.findByAndClick(xpath='id("inhalt-beratung-aussage-checkbox-HEIZUNGSANLAGE")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')

            if self.testcaseDataDict['inh_don_sportgeraete'] == 'X':
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='inhalt-beratung-aussage-checkbox-SPORT_JAGD']/label/div")

            if self.testcaseDataDict['inh_don_pool'] == 'X':
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='inhalt-beratung-aussage-checkbox-SWIMMINGPOOL']/label/div")

            if self.testcaseDataDict['inh_don_unbekannte'] == 'X':
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='inhalt-beratung-aussage-checkbox-UNBENANNTE_GEFAHREN']/label/div")

            self.browserSession.takeTime("Risiko")

    def eigenheim(self):
        if self.testcaseDataDict["geb_create"] == 'X':

            self.browserSession.findByAndClick(xpath='//*[@id="wohngebaeude-hinzufuegen-action"]')

            self.browserSession.findByAndClick(xpath="//div[@class='mat-form-field-infix'][contains(.,'Gebäudeart')]")

            self.browserSession.findByAndClick(
                xpath="//span[@class='mat-option-text'][contains(.,'" + self.testcaseDataDict['geb_gebart'] + "')]")


            self.browserSession.findByAndSetText(xpath='id("wohngebaeude-form-individuelle-objektbezeichnung")',
                                                 value=self.testcaseDataDict['geb_indiv_objektbez'])

            self.browserSession.findByAndSetText(xpath='id("wohngebaeude-form-flaeche-erdgeschoss")',
                                                 value=self.testcaseDataDict['geb_erd_m2'])

            self.browserSession.findByAndSetText(xpath='id("wohngebaeude-form-baujahr")',
                                                 value=self.testcaseDataDict['geb_baujahr'])

            if self.testcaseDataDict['geb_erster_m2'] != '':
                self.browserSession.findByAndSetText(xpath='id("wohngebaeude-form-flaeche-erster-stock")',
                                                    value=self.testcaseDataDict['geb_erster_m2'])

            if self.testcaseDataDict['geb_zweiter_m2'] != '':
                self.browserSession.findByAndSetText(xpath='id("wohngebaeude-form-flaeche-zweiter-stock")',
                                                     value=self.testcaseDataDict['geb_zweiter_m2'])

            if self.testcaseDataDict['geb_unter_m2'] != '':
                self.browserSession.findByAndSetText(xpath='id("wohngebaeude-form-flaeche-untergeschoss")',
                                                     value=self.testcaseDataDict['geb_unter_m2'])

            if self.testcaseDataDict['geb_mansarde_m2'] != '':
                self.browserSession.findByAndSetText(xpath='id("wohngebaeude-form-flaeche-mansarde")',
                                                     value=self.testcaseDataDict['geb_mansarde_m2'])

            if self.testcaseDataDict['geb_dritter_m2'] != '':
                self.browserSession.findByAndSetText(xpath='id("wohngebaeude-form-flaeche-dritter-stock")',
                                                    value=self.testcaseDataDict['geb_dritter_m2'])

            if self.testcaseDataDict['geb_glashaus'] != '':
                self.browserSession.findByAndClick(xpath='id("wohngebaeude-beratung-aussage-checkbox-GLASBRUCH")/label[@class="mat-checkbox-layout"]/div[@class="mat-checkbox-inner-container"]')
