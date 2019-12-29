from TestSteps.Frontend.VIGO.Antrag.Dokumente import Dokumente

class Dokumente(Dokumente):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute()
        self.teardown()

    def execute(self):
        super().beilageBeratungsProtokollHochladen()