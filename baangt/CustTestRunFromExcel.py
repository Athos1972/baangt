from baangt.TestRunFromExcel import TestRunFromExcel
from baangt.CustBrowserHandling import CustBrowserHandling

class CustTestRunFromExcel(TestRunFromExcel):
    def _getBrowserInstance(self, browserInstance):
        self.browser[browserInstance] = CustBrowserHandling(timing=self.timing)

if __name__ == '__main__':
    lRun = CustTestRunFromExcel(lExcelDefinitionFile="/Users/bernhardbuhl/git/baangt/HeartBeat.xlsx")