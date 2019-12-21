from pyFETest.HandleDatabase import HandleDatabase
from pyFETest.CustBrowserHandling import CustBrowserHandling
from pyFETest.ExportResults import ExportResults
from pyFETest.utils import utils

def openBrowser(browserName):

    l_test.takeTime("Start Browser")
    # l_test.createNewBrowser("CHROME")
    l_test.createNewBrowser(browserName)
    l_test.takeTime("Start Browser")

def loginPage(with_login=True):
    l_test.takeTime("Testfall gesamt")
    # Login to page
    l_test.takeTime("Login")
    l_test.goToUrl(
        f'https://{l_record["Mandant"]}-{l_record["base_url"]}.corpnet.at/vigong-produktauswahl/produktauswahl/{l_record["VN"]}')
    if with_login:
        l_test.findBy(css='#Ecom_User_ID', command='setText', value=l_record['user'])
        l_test.findBy(css='#Ecom_Password', command='setText', value=l_record['password'])
        l_test.findByAndClick(css='#loginButton2')
    l_test.takeTime("Login")

def produktAuswahl():

    # Produktauswahl
    l_test.takeTime("Produktauswahl")
    l_test.handleIframe("portal-content-iframe")
    l_test.findBy(xpath="//input[contains(@placeholder,'Provisionskonto')]", command='setText',
                  value=l_record['vermittler'])
    l_test.findByAndClick(xpath='//button[@id="productWohnen"]')
    l_test.handleIframe()
    l_test.takeTime("Produktauswahl")

def risikoSeite():
    # Risikoseite
    l_test.takeTime("Risiko")
    l_test.takeTime("Haushalt")
    l_test.handleWindow(1)
    l_test.handleIframe('portal-content-iframe')
    l_test.findByAndClick(css='.vigong-selection-panel-zonen-button')
    l_test.sleep(0.2)
    l_test.findByAndClick(xpath='//button[contains(.,"OK")]')

def hausHalt():
    # Haushalt anlegen
    if l_record["inh_create"] == 'X':
        l_test.findByAndClick(xpath='//button[@id="inhalt-hinzufuegen-action"]')
        l_test.findBy(xpath='//input[@id="inhalt-form-wohnnutzflaeche"]', command='setText', value=l_record['inh_m2'])
        l_test.findByAndClick(xpath='id("inhalt-form-gebeaudebezeichnung-select")')
        l_test.findByAndClick(xpath="//span[@class='mat-option-text'][contains(.,'" + l_record['inh_gebart'] + "')]")
        l_test.findByAndClick(xpath='id("inhalt-form-nutzung-select")')
        l_test.findByAndClick(xpath="//span[@class='mat-option-text'][contains(.,'" + l_record['inh_nutzung'] + "')]")
        l_test.takeTime("Haushalt")
    l_test.takeTime("Risiko")

def empfehlungen():
    # Navigation "Empfehlungen":
    l_test.takeTime("Empfehlungen")
    l_test.findByAndClick(xpath='//*[@id="empfehlungen"]')
    l_test.findByAndClick(xpath="//button[@id='empfehlungen_uebernehmen_action']")
    l_test.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
    l_test.takeTime("Empfehlungen")

def deckungsUmfang():
    # Deckungsumfang - weiter:
    l_test.takeTime("Deckungen")
    l_test.findByAndClick(xpath="//mat-icon[contains(.,'keyboard_arrow_right')]")
    l_test.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
    l_test.takeTime("Deckungen")

def praemienAuskunft():
    # Prämienauskunft - button clicken und dann weiter
    l_test.takeTime("Prämienauskunft")
    l_test.findByAndClick(xpath="//button[@id='praemienauskunft']")
    l_test.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
    l_test.findByAndClick(xpath="//mat-icon[contains(.,'keyboard_arrow_right')]")
    l_test.takeTime("Prämienauskunft")

def beratungsProtokoll():
    # Beratungsprotokoll - zwei Buttons klicken:
    l_test.takeTime("Beratungsprotokoll")
    l_test.findByAndClick(xpath='id("produktinformationsblatt-email-radio-button")')
    l_test.findByAndClick(xpath="//div[@class='mat-radio-label-content'][contains(.,'nicht gewünscht')]")
    l_test.findByAndClick(xpath="//button[@id='nav-component-speichern-button']")
    l_test.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
    # l_test.findByAndClick(css="#emailOeffnen_action")
    l_test.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
    l_test.takeTime("Beratungsprotokoll")

def vertragsDaten():
    # Vertragsdaten, VN, Zahlung
    l_test.findByAndClick(xpath="//div[@class='vigong-prozessnav-link-text'][contains(.,'Vertragsdaten, VN, Zahlung')]")
    l_test.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
    l_test.findByAndClick(xpath="//div[@class='mat-radio-label-content'][contains(.,'Zahlschein')]")

def antragsFragen():
    # Antragsfragen:
    l_test.takeTime("Antragsfragen")
    l_test.findByAndClick(xpath="id('vorversicherung')")
    l_test.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
    l_test.findByAndClick(
        xpath="//mat-radio-button[@id='vorversicherungenversicherungAbgelehnt-nein-radio-button']/label/div/div")
    l_test.findByAndClick(
        xpath="//mat-radio-button[@id='vorversicherungenvertragsAnpassung-nein-radio-button']/label/div/div")
    l_test.findByAndClick(
        xpath="//mat-radio-button[@id='bestehende-versicherungenweitereVertraege-nein-radio-button']/label/div/div")
    l_test.findByAndClick(xpath="//mat-radio-button[@id='schaeden-elementarschaeden-nein-radio-button']/label/div/div")
    l_test.findByAndClick(xpath="//mat-radio-button[@id='schaeden-weitereSchaeden-nein-radio-button']/label/div/div")
    l_test.takeTime("Antragsfragen")

def vermittler():
    # Vermittler
    l_test.takeTime("Vermittler")
    l_test.findByAndClick(
        xpath='id("rechtliches")/div[@class="vigong-prozessnav-link-div"]/div[@class="vigong-prozessnav-link-text"]')
    l_test.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")
    l_test.findByAndClick(xpath="//div[@class='mat-radio-label-content'][contains(.,'Ja, ich/wir stimme(n) zu')]")
    l_test.takeTime("Vermittler")

def dokumente():
    # Dokumente
    l_test.findByAndClick(xpath="//div[@id='dokumente']/div/div[2]")
    l_test.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]")

    # Upload Beilage
    l_test.takeTime("Upload Beratungsprotokoll")
    l_test.findByAndClick(xpath="//span[@class='mat-button-wrapper'][contains(.,'Beilage hinzufügen')]")
    l_test.sleep(0.2)
    l_test.findByAndClick(xpath="(//span[contains(.,'Beilagentyp')])[1]")
    l_test.findByAndClick(xpath="//span[contains(.,'Beratungsprotokoll (unterschrieben)')]")
    l_test.javaScript("""

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
    l_test.findBy(xpath="//input[contains(@type,'file')]", command="Settext", value=l_record["file_praemienauskunft"])
    l_test.findByAndClick(xpath='//*[@id="beilage-hinzufügen-save"]')
    l_test.takeTime("Upload Beratungsprotokoll")

def antragSenden():
    # Antrag
    l_test.takeTime("Antrag fertigstellen")
    l_test.findByAndClick(xpath="//div[@id='fertigstellen']/div/div[2]")
    l_test.takeTime("Antrag drucken")
    l_test.findByAndClick(xpath="//button[@id='antrag_action']")
    l_test.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]", timeout=120)
    l_test.takeTime("Antrag drucken")
    l_test.findByAndClick(xpath='id("manuell_unterschreiben_action")')
    l_test.sleep(0.2)
    l_test.findByAndClick(xpath='//*[@id="antragsdaten-bestaetigen-select"]')
    l_test.findByAndClick(xpath='//*[@id="antragsdaten-bestaetigen-uebernehmen"]')
    l_test.takeTime("Warten auf Senden an Bestand Button")
    l_test.findByAndClick(xpath="//button[@id='sendenAnBestand_action']")
    l_test.takeTime("Warten auf Senden an Bestand Button")
    l_test.takeTime("Senden an Bestand")
    l_test.findWaitNotVisible(xpath="//div[contains(@class,'overlay-spinner ng-star-inserted')]", timeout=120)
    l_record["SAPPOL"] = l_test.findByAndWaitForValue(xpath='id("info-card-polizzennummer")')
    l_record["VIGOGF#"] = l_test.findByAndWaitForValue(xpath='id("info-card-geschaeftsfallnummer")')
    l_record["PRAEMIE"] = l_test.findByAndWaitForValue(xpath='id("nav-component-praemie")')
    l_test.takeTime("Senden an Bestand")
    l_test.takeTime("Antrag fertigstellen")
    l_record["Dauer"] = l_test.takeTime("Testfall gesamt")

def schmuftelFilenamen():
    l_file = "/Users/bernhardbuhl/git/KatalonVIG/1testoutput/" + \
             "pyTest_" + \
             l_browser + "_" + \
             utils.datetime_return() + "_" + l_record["base_url"] \
             +".xlsx"
    return l_file


if __name__ == '__main__':

    l_database = HandleDatabase()
    l_database.read_excel("/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/testdata_wstv_fqa.xlsx", "Testcases")

    l_test = CustBrowserHandling()

    l_browser = "FF"
    # l_browser = "CHROME"

    openBrowser(l_browser)

    l_first = True
    l_test.takeTime("Testrun complete")
    for n in range(3,32,1):
        l_record = l_database.readTestRecord(n)
        loginPage(l_first)
        if l_first:
            l_first = False
            l_excel = ExportResults(schmuftelFilenamen())
        produktAuswahl()
        risikoSeite()
        hausHalt()
        empfehlungen()
        deckungsUmfang()
        praemienAuskunft()
        beratungsProtokoll()
        vertragsDaten()
        antragsFragen()
        vermittler()
        dokumente()
        antragSenden()
        l_test.handleWindow(0, "close")
        l_record["TimeLog"] = l_test.returnTime()
        l_test.takeTimeSumOutput()
        l_excel.addEntry(l_record)
        l_test.resetTime()

    l_test.closeBrowser()

    l_test.takeTime("Testrun complete")
    l_test.takeTimeSumOutput()
    l_excel.close()


