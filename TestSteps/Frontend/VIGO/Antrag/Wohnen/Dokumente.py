from TestSteps.Frontend.VIGO.Antrag.Dokumente import Dokumente

class Dokumente(Dokumente):
    def __init__(self, testcaseDataDict, browserSession):
        super().__init__(testcaseDataDict, browserSession)
        self.execute()

    def execute(self):
        super().dokumenteOpen()
        super().beilageBeratungsProtokollHochladen()