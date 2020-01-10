import PySimpleGUI as sg

class UI:
    def __init__(self):
        self.directory = None
        self.configFile = None
        self.configFiles = []
        self.testRunFile = None
        self.testRunFiles = []
        self.window = None

        self.startWindow()


    def startWindow(self):
        sg.theme("TanBlue")

        lLayout = [[sg.Text("Select Directory, Testrun and Global settings to use:")],
                   [sg.Text("Directory", size=(20,1)),
                    sg.In(key="-directory-", size=(20,1)), sg.FolderBrowse()],
                   [sg.Text("TestRun", size=(20,1)),
                    sg.InputCombo(("CV1", "CV2"), key="testRunFile", size=(20,1))],
                   [sg.Text("Global Settings", size=(20,1)),
                    sg.InputCombo(("GS1", "GS2"), key="configFile", size=(20,1))],
                   [sg.Submit(), sg.Button('Exit')]]

        self.window = sg.Window("Baangt interactive Starter", layout=lLayout)
        lWindow = self.window
        lWindow.finalize()
        lWindow["_franzi_"].update("jetztzeit")
        lWindow["configFile"].update(values=["susi", "strolchi"])
        lWindow["-directory-"].update(value=self.directory)

        while True:

            lEvent, lValues = lWindow.read()
            print(lValues["configFile"])
            if lEvent == "Exit":
                break
            if lValues.get('-directory-') != self.directory:
                self.directory = lValues.get("-directory-")
                self.getConfigFilesInDirectory()
                lWindow['configFile'].update(values=self.configFiles, value="")
                lWindow['testRunFile'].update(values=self.testRunFiles, value="")
            text_input = lValues.get('franzi')
            file_chosen = lValues["configFile"]
            sg.popup(f"You entered: {text_input} and chose file {file_chosen}")

        lWindow.close

    def getConfigFilesInDirectory(self):
        """Reads *.JSON-Files from directory given in self.directory and builds 2 lists (Testrunfiles and ConfiFiles"""





