from TestSteps.CustTestStepMaster import CustTestStepMaster
from TestSteps import CustGlobalConstants as TSGC


class Deckungsumfang(CustTestStepMaster):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()
        self.teardown()

    def execute(self):
        self.deckungsUmfangStart()
        self.haushalt_deckungen()
        self.haustechnik_deckungen()
        self.deckungsUmfangEnd()

    def deckungsUmfangStart(self):
        # Deckungsumfang - weiter:
        self.browserSession.takeTime("Deckungen")
        self.browserSession.findByAndClick(xpath='//*[@id="deckungsumfang"]')
        self.browserSession.findWaitNotVisible(xpath=TSGC.NG_SPINNER)

    def haushalt_deckungen(self):

        if self.testcaseDataDict['zu_hh_art'] != '':
            if self.browserSession.findBy(
                    xpath='//*[@id="haushalt-BASIS-combobox"]', timeout=1):
                self.browserSession.findByAndClick(
                    xpath='//*[@id="haushalt-BASIS-combobox"]')

            if self.browserSession.findBy(
                    xpath='//*[@id="haushalt-PLUS-combobox"]', timeout=1):
                self.browserSession.findByAndClick(
                    xpath='//*[@id="haushalt-PLUS-combobox"]')

            if self.browserSession.findBy(
                    xpath='//*[@id="haushalt-EXTRA-combobox"]', timeout=1):
                self.browserSession.findByAndClick(xpath='//*[@id="haushalt-EXTRA-combobox"]')

            self.browserSession.findByAndClick(xpath=f"//span[@class='mat-option-text'][contains(.,'{self.testcaseDataDict['zu_hh_art']}')]")

        if self.testcaseDataDict['zu_hh_create'] == 'X':
            if self.testcaseDataDict['Mandant'] == 'DON':
                if self.testcaseDataDict['zu_hh_art'] == 'Basis':
                    self.browserSession.findByAndClick(
                        xpath="//div[@class='vigong-deckungs-umfang-box-checkbox-header-label'][contains(.,'Haushaltsversicherung Basis')]")
                else:
                    self.browserSession.findByAndClick(
                        xpath="//div[@class='vigong-deckungs-umfang-box-checkbox-header-label'][contains(.,'Haushaltsversicherung Plus')]")

            else:
                if self.testcaseDataDict['zu_hh_art'] == 'Basis':
                    self.browserSession.findByAndClick(
                        xpath="//div[@class='vigong-deckungs-umfang-box-checkbox-header-label'][contains(.,'Haushaltsversicherung Basis')]")
                else:
                    self.browserSession.findByAndClick(
                        xpath="//div[@class='vigong-deckungs-umfang-box-checkbox-header-label'][contains(.,'Haushaltsversicherung Extra')]")

            self.browserSession.sleep(0.2)

            # FIXME
            # if self.testcaseDataDict['zu_hh_hochwasser'] == 'X':
            #     self.browserSession.findByAndClick(
            #         xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_hochwasser_checkbox')
            #
            #     if self.testcaseDataDict['zu_hh_hochw_erhvar.toString().length() > 0:
            #         if self.testcaseDataDict['zu_hh_art'] == 'Basis':
            #             self.browserSession.findByAndClick(
            #                 xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_hochwasser_erh_dropdown_basis')
            #         else
            #             self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_hochwasser_erh_dropdown')
            #
            #     switch (self.testcaseDataDict['zu_hh_hochw_erhvar
            #         case 'Erh 1':
            #             self.browserSession.findByAndClick(
            #                 xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_hochwasser_erh_erh1')
            #         break
            #     case 'Erh 2':
            #         self.browserSession.findByAndClick(
            #             xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_hochwasser_erh_erh2')
            #         break
            #     case 'Erh 3':
            #         self.browserSession.findByAndClick(
            #             xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_hochwasser_erh_erh3')
            #         break

            #if self.testcaseDataDict['zu_hh_erdbeben'] == 'X':
            #    self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_erdbeben')

            # fixme
            # if self.testcaseDataDict['zu_hh_erdb_erhvar.toString().length() > 0:
            #     if self.testcaseDataDict['zu_hh_art'] == 'Basis':
            #         self.browserSession.findByAndClick(
            #         xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_erdbeben_erh_dropdown_basis')
            #     else
            #     self.browserSession.findByAndClick(
            #         xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_erdbeben_erh_dropdown')
            #
            #     switch(self.testcaseDataDict['zu_hh_erdb_erhvar
            #     case
            #     'Erh 1': \
            #         self.browserSession.findByAndClick(
            #             xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_erdbeben_erh_erh1')
            #     break
            #     case
            #     'Erh 2':
            #     self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_erdbeben_erh_erh2')
            #     break
            #     case
            #     'Erh 3':
            #     self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_erdbeben_erh_erh3')
            #     break

            if self.testcaseDataDict['zu_hh_geld'] == 'X' and (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='EXTRA-HAUSHALT-GELD_GELDESWERTE-deckungs-eintrag-zusatzDeckung-checkbox']")
            elif self.testcaseDataDict['zu_hh_geld'] == 'X':
                self.browserSession.findByAndClick(xpath="//mat-checkbox[contains(@id, 'BASIS-HAUSHALT-GELD_GELDESWERTE-deckungs-eintrag-zusatzDeckung-checkbox')]")

            if self.testcaseDataDict['zu_hh_schmuck'] == 'X' and (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='EXTRA-HAUSHALT-SCHMUCK_EDELSTEINE-deckungs-eintrag-zusatzDeckung-checkbox']")
            elif self.testcaseDataDict['zu_hh_schmuck'] == 'X':
                self.browserSession.findByAndClick(xpath="//*[@id='BASIS-HAUSHALT-SCHMUCK_EDELSTEINE-deckungs-eintrag-zusatzDeckung-checkbox']")

            if self.testcaseDataDict['zu_hh_wertsachen'] == 'X':
                if self.testcaseDataDict['zu_hh_art'] != 'Basis':
                    self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='EXTRA-HAUSHALT-WERTSACHEN-deckungs-eintrag-zusatzDeckung-checkbox']/label/div")
                    self.browserSession.findByAndForceText(xpath="//input[@id='EXTRA-HAUSHALT-WERTSACHEN-deckungs-eintrag-zusatzDeckung-input']",
                                  value=self.testcaseDataDict['zu_hh_wert_wert'])

                else:
                    self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='BASIS-HAUSHALT-WERTSACHEN-deckungs-eintrag-zusatzDeckung-checkbox']/label/div")
                    self.browserSession.findByAndForceText(xpath="//input[@id='BASIS-HAUSHALT-WERTSACHEN-deckungs-eintrag-zusatzDeckung-input']",
                                  value=self.testcaseDataDict['zu_hh_wert_wert'])

            if self.testcaseDataDict['zu_hh_panzerk'] == 'X' and (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='EXTRA-HAUSHALT-WERTSACHEN_IN_KASSEN_EN2-deckungs-eintrag-zusatzDeckung-checkbox']")

                self.browserSession.findByAndForceText(xpath="//input[@id='EXTRA-HAUSHALT-WERTSACHEN_IN_KASSEN_EN2-deckungs-eintrag-zusatzDeckung-input']",
                                value=self.testcaseDataDict['zu_hh_panzk_wert'])
            elif self.testcaseDataDict['zu_hh_panzerk'] == 'X':
                self.browserSession.findByAndClick(
                    xpath="//*[@id='BASIS-HAUSHALT-WERTSACHEN_IN_KASSEN_EN2-deckungs-eintrag-zusatzDeckung-checkbox']")

                self.browserSession.findByAndForceText(xpath="//*[@id='BASIS-HAUSHALT-WERTSACHEN_IN_KASSEN_EN2-deckungs-eintrag-zusatzDeckung-input']",
                    value=self.testcaseDataDict['zu_hh_panzk_wert'])

            if self.testcaseDataDict['zu_hh_elektronik'] == 'X':
                if self.testcaseDataDict['zu_hh_art'] != 'Basis':
                    self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='EXTRA-HAUSHALT-UNTERHALTUNGSELEKTRONIK-deckungs-eintrag-zusatzDeckung-checkbox']/label/div")
                else:
                    self.browserSession.findByAndClick(xpath="//*[@id='BASIS-HAUSHALT-UNTERHALTUNGSELEKTRONIK-deckungs-eintrag-zusatzDeckung-titel']")

            if self.testcaseDataDict['zu_hh_sport_jagd'] == 'X' and (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='EXTRA-HAUSHALT-SPORT_JAGD-deckungs-eintrag-zusatzDeckung-checkbox']/label/div")
            elif self.testcaseDataDict['zu_hh_sport_jagd'] == 'X':
                self.browserSession.findByAndClick(xpath="//*[@id='BASIS-HAUSHALT-SPORT_JAGD-deckungs-eintrag-zusatzDeckung-titel']")

            if self.testcaseDataDict['zu_hh_sport_wert'] != '' and (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndForceText(xpath="//input[@id='EXTRA-HAUSHALT-SPORT_JAGD-deckungs-eintrag-zusatzDeckung-input']",
                    value=self.testcaseDataDict['zu_hh_sport_wert'])
            elif self.testcaseDataDict['zu_hh_sport_wert'] != '':
                self.browserSession.findByAndForceText(xpath="//*[@id='BASIS-HAUSHALT-SPORT_JAGD-deckungs-eintrag-zusatzDeckung-input']",
                    value=self.testcaseDataDict['zu_hh_sport_wert'])

            if self.testcaseDataDict['zu_hh_unbenannte'] == 'X' and (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='EXTRA-HAUSHALT-UNBENANNTE_GEFAHREN-deckungs-eintrag-zusatzDeckung-checkbox']/label/div")
            elif self.testcaseDataDict['zu_hh_unbenannte'] == 'X':
                self.browserSession.findByAndClick(
                    xpath='//*[@id="BASIS-HAUSHALT-UNBENANNTE_GEFAHREN-deckungs-eintrag-zusatzDeckung-titel"]')

            if self.testcaseDataDict['zu_hh_sos'] == 'X' and (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='EXTRA-HAUSHALT-DONAUSOS-deckungs-eintrag-zusatzDeckung-checkbox']")
            elif self.testcaseDataDict['zu_hh_sos'] == 'X':
                self.browserSession.findByAndClick(xpath="//mat-checkbox[@id='BASIS-HAUSHALT-DONAUSOS-deckungs-eintrag-zusatzDeckung-checkbox']")

            if self.testcaseDataDict['zu_hh_privhaftpfl'] == 'X':
                self.browserSession.findByAndClick(
                    xpath="//mat-checkbox[@id='BASIS-HAUSHALT-PRIVATHAFTPFLICHT-deckungs-eintrag-zusatzDeckung-checkbox']/label/div")

                self.browserSession.findByAndSetText(xpath="//input[@id='BASIS-HAUSHALT-PRIVATHAFTPFLICHT-deckungs-eintrag-zusatzDeckung-input']",
                               value=self.testcaseDataDict['zu_hh_prihaftpf_person_count'])

                self.browserSession.findByAndSetText(xpath="//textarea[@id='BASIS-HAUSHALT-PRIVATHAFTPFLICHT-deckungs-eintrag-zusatzDeckung-textarea']",
                              value=self.testcaseDataDict['zu_hh_prihaftpf_person_name'])

            if self.testcaseDataDict['zu_hh_rasche_hilfe'] == 'X':
                self.browserSession.findByAndClick(
                    xpath="//mat-checkbox[@id='EXTRA-HAUSHALT-RASCHE_HILFE-deckungs-eintrag-zusatzDeckung-checkbox']/label/div")

            if self.testcaseDataDict['zu_hh_tiefkuehl'] == 'X':
                self.browserSession.findByAndClick(
                    xpath="//*[@id='EXTRA-HAUSHALT-TIEFKUEHLBEHAELTER-deckungs-eintrag-zusatzDeckung-checkbox']")

            if self.testcaseDataDict['zu_hh_freizeitpaket'] == 'X':
                self.browserSession.findByAndClick(
                    xpath='//*[@id="EXTRA-HAUSHALT-FREIZEITPAKET-deckungs-eintrag-zusatzDeckung-checkbox"]')

            if self.testcaseDataDict['zu_hh_freizeit_wert'] != '' and (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndForceText(xpath="//input[@id='EXTRA-HAUSHALT-FREIZEITPAKET-deckungs-eintrag-zusatzDeckung-input']",
                               value=self.testcaseDataDict['zu_hh_freizeit_wert'])
            elif self.testcaseDataDict['zu_hh_freizeit_wert'] != '':
                self.browserSession.findByAndForceText(xpath="//input[@id='BASIS-HAUSHALT-FREIZEITPAKET-deckungs-eintrag-zusatzDeckung-input']",
                              value=self.testcaseDataDict['zu_hh_freizeit_wert'])

            if self.testcaseDataDict['zu_hh_erw_premium'] == 'X':
                self.browserSession.findByAndClick(
                    xpath="//*[@id='EXTRA-HAUSHALT-ERWEITERTE_PREMIUM_GEFAHREN-deckungs-eintrag-zusatzDeckung-checkbox']")

    def haustechnik_deckungen(self):
        if self.testcaseDataDict['zu_htechn'] == 'X':
            if self.testcaseDataDict['zu_htechn_create'] == 'X':
                self.browserSession.findByAndClick(
                    xpath="//label[contains(@for,'technik-BASIS-checkbox-input')]")

            self.browserSession.findByAndClick(
                xpath="//div[@class='vigong-deckungs-umfang-box-checkbox-header-label'][contains(.,'Haustechnikversicherung')]")
            self.browserSession.sleep(0.5)

            if self.testcaseDataDict['zu_htechn_kasko'] == 'X':
                self.browserSession.findByAndClick(
                    xpath="//label[@for='BASIS-TECHNIK-HAUSTECHNIKKASKO-deckungs-eintrag-zusatzDeckung-checkbox-input']")

            if self.testcaseDataDict['zu_htechn_kasko_wert'] != '':
                self.browserSession.sleep(0.2)
                self.browserSession.findByAndForceText(
                    xpath="//input[contains(@id,'BASIS-TECHNIK-HAUSTECHNIKKASKO-deckungs-eintrag-zusatzDeckung-input')]",
                    value=self.testcaseDataDict['zu_htechn_kasko_wert'])

            if self.testcaseDataDict['zu_htechn_heizkask'] == 'X':
                self.browserSession.findByAndClick(
                    xpath="//span[contains(@id,'BASIS-TECHNIK-HEIZUNGSKASKO-deckungs-eintrag-zusatzDeckung-titel')]")

    def deckungsUmfangEnd(self):
        self.browserSession.takeTime("Deckungen")
