from TestSteps.TestStepMaster import TestStepMaster
from TestSteps import CustGlobalConstants as TSGC


class Deckungsumfang(TestStepMaster):
    def __init__(self, testcaseDataDict, browserSession):
        super().__init__(testcaseDataDict, browserSession)
        self.execute()

    def execute(self):
        self.deckungsUmfangStart()
        self.haushalt_deckungen()
        self.deckungsUmfangEnd()

    def deckungsUmfangStart(self):
        # Deckungsumfang - weiter:
        self.browserSession.takeTime("Deckungen")
        self.browserSession.findByAndClick(xpath="//mat-icon[contains(.,'keyboard_arrow_right')]")
        self.browserSession.findWaitNotVisible(xpath=TSGC.NG_SPINNER)

    def haushalt_deckungen(self):

        if self.testcaseDataDict['zu_hh_art'] != '':
            if self.browserSession.findBy(
                    xpath=''Page_VIGO Wohnen / Deckungen / Haushalt_zusatzdeckungen / hh_combobox_basis'), :
            1, FailureHandling.OPTIONAL)
            self.browserSession.findByAndClick(
                xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/hh_combobox_basis')

            if self.browserSession.findBy(
                    xpath=''Page_VIGO Wohnen / Deckungen / Haushalt_zusatzdeckungen / hh_combobox_plus'), :
            1, FailureHandling.OPTIONAL)
            self.browserSession.findByAndClick(
                xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/hh_combobox_plus')

            if self.browserSession.findBy(
                    xpath=''Page_VIGO Wohnen / Deckungen / Haushalt_zusatzdeckungen / hh_combobox_extra'), :
            1, FailureHandling.OPTIONAL)
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/hh_combobox_extra')

            if self.testcaseDataDict['zu_hh_art'] == 'Basis':
                self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/hh_combobox_value_basis')

            if self.testcaseDataDict['zu_hh_art'] == 'Extra':
                self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/hh_combobox_value_extra')

            if self.testcaseDataDict['zu_hh_art'] == 'Plus':
                self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/hh_combobox_value_plus')

            if self.testcaseDataDict['zu_hh_create'] == 'X':
                if self.testcaseDataDict['Mandant'] == 'DON':
                    if self.testcaseDataDict['zu_hh_art'] == 'Basis':
                        self.browserSession.findByAndClick(
                            xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_Zusatzdeckung-expansion_BASIS')
                    else
                        self.browserSession.findByAndClick(
                            xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_Zusatzdeckung-expansion_PLUS')

                else
                    if self.testcaseDataDict['zu_hh_art'] == 'Basis':
                        self.browserSession.findByAndClick(
                            xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_Zusatzdeckung-expansion_BASIS')
                    else
                        self.browserSession.findByAndClick(
                            xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/wstv_hh_Zusatzdeckung-expansion_EXTRA')

                    WebUI.delay(1) // Chrome...

            if self.testcaseDataDict['zu_hh_hochwasser'] == 'X':
                self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_hochwasser_checkbox')

                if self.testcaseDataDict['zu_hh_hochw_erhvar.toString().length() > 0:
                    if self.testcaseDataDict['zu_hh_art'] == 'Basis':
                        self.browserSession.findByAndClick(
                            xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_hochwasser_erh_dropdown_basis')
                    else
                        self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_hochwasser_erh_dropdown')

                switch (self.testcaseDataDict['zu_hh_hochw_erhvar
                    case 'Erh 1':
                        self.browserSession.findByAndClick(
                            xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_hochwasser_erh_erh1')
                    break
                case 'Erh 2':
                    self.browserSession.findByAndClick(
                        xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_hochwasser_erh_erh2')
                    break
                case 'Erh 3':
                    self.browserSession.findByAndClick(
                        xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_hochwasser_erh_erh3')
                    break

            if self.testcaseDataDict['zu_hh_erdbeben'] == 'X':
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_erdbeben')

            if self.testcaseDataDict['zu_hh_erdb_erhvar.toString().length() > 0:
                if self.testcaseDataDict['zu_hh_art'] == 'Basis':
                    self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_erdbeben_erh_dropdown_basis')
                else
                self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_erdbeben_erh_dropdown')

                switch(self.testcaseDataDict['zu_hh_erdb_erhvar
                case
                'Erh 1': \
                    self.browserSession.findByAndClick(
                        xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_erdbeben_erh_erh1')
                break
                case
                'Erh 2':
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_erdbeben_erh_erh2')
                break
                case
                'Erh 3':
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_erdbeben_erh_erh3')
                break

            if self.testcaseDataDict['zu_hh_geld'] == 'X' and (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_geld')
            elif self.testcaseDataDict['zu_hh_geld'] == 'X':
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_geld_basis')

            if self.testcaseDataDict['zu_hh_schmuck'] == 'X' and (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_schmuck')
            elif self.testcaseDataDict['zu_hh_schmuck'] == 'X':
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_schmuck_basis')

            if self.testcaseDataDict['zu_hh_wertsachen'] == 'X':
                if self.testcaseDataDict['zu_hh_art'] != 'Basis':
                    self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_wertsachen')
                    WebUI.setText(findTestObject('Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_wertsachen_wert'),
                                  self.testcaseDataDict['zu_hh_wert_wert)

                else
                    self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_wertsachen_basis')
                    WebUI.setText(findTestObject('Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_wertsachen_wert_basis'),
                                  self.testcaseDataDict['zu_hh_wert_wert)

            if self.testcaseDataDict['zu_hh_panzerk'] == 'X' and (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_panzerkassen')

                WebUI.setText(findTestObject('Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_panzerkassen_wert'),
                                self.testcaseDataDict['zu_hh_panzk_wert)
            elif self.testcaseDataDict['zu_hh_panzerk'] == 'X':
                self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_panzerkassen_basis')

                WebUI.setText(findTestObject('Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_panzerkassen_wert_basis'),
                    self.testcaseDataDict['zu_hh_panzk_wert)

            if self.testcaseDataDict['zu_hh_elektronik'] == 'X':
                if self.testcaseDataDict['zu_hh_art'] != 'Basis':
                    self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_elektronik')
                else
                    self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_elektronik_basis')

            if self.testcaseDataDict['zu_hh_sport_jagd'] == 'X') & & (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_sport_jagd')
            elif self.testcaseDataDict['zu_hh_sport_jagd'] == 'X':
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_sport_jagd_basis')

            if self.testcaseDataDict['zu_hh_sport_wert'] != '') & & (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                WebUI.setText(findTestObject('Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_sport_jagd_wert'),
                    self.testcaseDataDict['zu_hh_sport_wert)
            elif self.testcaseDataDict['zu_hh_sport_wert'] != '':
                WebUI.setText(findTestObject('Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_sport_jagd_wert_basis'),
                    self.testcaseDataDict['zu_hh_sport_wert)

            if self.testcaseDataDict['zu_hh_unbenannte'] == 'X' & & (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_unbenannte')
            elif self.testcaseDataDict['zu_hh_unbenannte'] == 'X':
                self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_unbenannte_basis')

            if self.testcaseDataDict['zu_hh_sos'] == 'X') & & (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_sos')
            elif self.testcaseDataDict['zu_hh_sos'] == 'X':
                self.browserSession.findByAndClick(xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_sos_basis')

            if self.testcaseDataDict['zu_hh_privhaftpfl'] == 'X':
                self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_privhaftpfl_zus_person')

                WebUI.setText(findTestObject('Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_privhaftpfl_zus_person_count'),
                              self.testcaseDataDict['zu_hh_prihaftpf_person_count)

                WebUI.setText(findTestObject('Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/don_hh_privhaftpfl_zus_person_names'),
                              self.testcaseDataDict['zu_hh_prihaftpf_person_name)

            if self.testcaseDataDict['zu_hh_rasche_hilfe'] == 'X':
                self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/wstv_hh_rasche_hilfe'), FailureHandling.STOP_ON_FAILURE)


            if self.testcaseDataDict['zu_hh_tiefkuehl'] == 'X':
                self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/wstv_hh_tiefkuehl'), FailureHandling.STOP_ON_FAILURE)


            if self.testcaseDataDict['zu_hh_freizeitpaket'] == 'X':
                self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/wstv_hh_freizeitpaket'), FailureHandling.STOP_ON_FAILURE)


            if self.testcaseDataDict['zu_hh_freizeit_wert'] != '' and (self.testcaseDataDict['zu_hh_art'] != 'Basis'):
                WebUI.setText(findTestObject('Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/wstv_hh_freizeit_wert'),
                              self.testcaseDataDict['zu_hh_freizeit_wert)
            elif self.testcaseDataDict['zu_hh_freizeit_wert'] != '':
                WebUI.setText(findTestObject('Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/wstv_hh_freizeit_wert_basis'),
                              self.testcaseDataDict['zu_hh_freizeit_wert)

            if self.testcaseDataDict['zu_hh_erw_premium'] == 'X':
                self.browserSession.findByAndClick(
                    xpath='Page_VIGO Wohnen/Deckungen/Haushalt_zusatzdeckungen/wstv_hh_erw_premium'), FailureHandling.STOP_ON_FAILURE)





​

def deckungsUmfangEnd(self):
    self.browserSession.takeTime("Deckungen")
