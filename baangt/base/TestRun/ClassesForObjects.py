from dataclasses import dataclass

@dataclass
class ClassesForObjects:
    browserFactory: str = "baangt.base.BrowserFactory.BrowserFactory"
    browserHandling: str = "baangt.base.BrowserHandling.BrowserHandling.BrowserDriver"
    testCaseSequenceMaster: str = "baangt.TestCaseSequenceMaster.TestCaseSequenceMaster"
    testStepMaster: str = "baangt.TestSteps.TestStepMaster"

