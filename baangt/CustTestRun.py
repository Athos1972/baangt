from baangt.TestRun import TestRun
from baangt import GlobalConstants as GC
from baangt import CustGlobalConstants as CGC


class CustTestRun(TestRun):
    def __init__(self, testRunName):
        self._initTestRun()
        super().__init__(testRunName=testRunName)

    def _initTestRun(self):
        super()._initTestRun()
        self.testrunAttributes= {
            "Heartbeat": {
                GC.KWARGS_TESTRUNATTRIBUTES: {
                    GC.STRUCTURE_TESTCASESEQUENCE: {
                        1: [GC.CLASSES_TESTCASESEQUENCE, {
                            "DATAFILE": '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/testdata_wstv_fqa.xlsx',
                            "SHEET": 'Testcases',
                            "PARALLEL_RUNS": 5,
                            GC.DATABASE_FROM_LINE: 488,
                            GC.DATABASE_TO_LINE: 492,
                            GC.STRUCTURE_TESTCASE: {
                                1: [GC.CLASSES_TESTCASE,
                                    {GC.KWARGS_BROWSER: GC.BROWSER_FIREFOX,
                                     "BROWSER_ATTRIBUTES": "",
                                     GC.KWARGS_TESTCASETYPE: GC.KWARGS_BROWSER},
                                    { GC.STRUCTURE_TESTSTEP:
                                      {
                                        1: "TestSteps.Frontend.VIGO.Produktauswahl.ProduktauswahlURL",
                                        2: "TestSteps.Frontend.Portal.Login",
                                        3: "TestSteps.Frontend.VIGO.Produktauswahl.ProduktAuswahl",
                                        4: "TestSteps.Frontend.VIGO.Antrag.Wohnen.ObjektSeite",
                                        5: "TestSteps.Frontend.VIGO.Antrag.Wohnen.Empfehlungen",
                                        6: "TestSteps.Frontend.VIGO.Antrag.Wohnen.Deckungsumfang",
                                        7: "TestSteps.Frontend.VIGO.Antrag.Wohnen.Praemienauskunft",
                                        8: "TestSteps.Frontend.VIGO.Antrag.Wohnen.Beratungsprotokoll",
                                        9: "TestSteps.Frontend.VIGO.Antrag.Wohnen.VertragsDaten",
                                        10: "TestSteps.Frontend.VIGO.Antrag.Wohnen.AntragsFragen",
                                        11: "TestSteps.Frontend.VIGO.Antrag.Vermittler",
                                        12: "TestSteps.Frontend.VIGO.Antrag.Dokumente",
                                        13: "TestSteps.Frontend.VIGO.Antrag.AntragSenden"
                                      },
                                    },
                                ],
                            },
                        }],
                    },
                },
            },
            "HB-Dark": {
                GC.KWARGS_TESTRUNATTRIBUTES: {
                    GC.STRUCTURE_TESTCASESEQUENCE: {
                        1: [GC.CLASSES_TESTCASESEQUENCE, {
                            "DATAFILE": '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/testdata_wstv_fqa.xlsx',
                            "SHEET": 'Testcases',
                            "PARALLEL_RUNS": 3,
                            GC.DATABASE_FROM_LINE: 488,
                            GC.DATABASE_TO_LINE: 494,
                            GC.STRUCTURE_TESTCASE: {
                                1: [GC.CLASSES_TESTCASE,
                                    {GC.KWARGS_BROWSER: GC.BROWSER_FIREFOX,
                                     "BROWSER_ATTRIBUTES": {GC.BROWSER_MODE_HEADLESS: True},
                                     GC.KWARGS_TESTCASETYPE: GC.KWARGS_BROWSER},
                                    {GC.STRUCTURE_TESTSTEP:
                                        {
                                            1: "TestSteps.Frontend.VIGO.Produktauswahl.ProduktauswahlURL",
                                            2: "TestSteps.Frontend.Portal.Login",
                                            3: "TestSteps.Frontend.VIGO.Produktauswahl.ProduktAuswahl",
                                            4: "TestSteps.Frontend.VIGO.Antrag.Wohnen.ObjektSeite",
                                            5: "TestSteps.Frontend.VIGO.Antrag.Wohnen.Empfehlungen",
                                            6: "TestSteps.Frontend.VIGO.Antrag.Wohnen.Deckungsumfang",
                                            7: "TestSteps.Frontend.VIGO.Antrag.Wohnen.Praemienauskunft",
                                            8: "TestSteps.Frontend.VIGO.Antrag.Wohnen.Beratungsprotokoll",
                                            9: "TestSteps.Frontend.VIGO.Antrag.Wohnen.VertragsDaten",
                                            10: "TestSteps.Frontend.VIGO.Antrag.Wohnen.AntragsFragen",
                                            11: "TestSteps.Frontend.VIGO.Antrag.Vermittler",
                                            12: "TestSteps.Frontend.VIGO.Antrag.Dokumente",
                                            13: "TestSteps.Frontend.VIGO.Antrag.AntragSenden"
                                        },
                                    },
                                    ],
                            },
                        }],
                    },
                },
            },
            "Antrag-Single": {
                GC.KWARGS_TESTRUNATTRIBUTES: {
                    GC.STRUCTURE_TESTCASESEQUENCE: {
                        1: [GC.CLASSES_TESTCASESEQUENCE, {
                            "DATAFILE": '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/testdata_wstv_fqa.xlsx',
                            "SHEET": 'Testcases',
                            "PARALLEL_RUNS": 3,
                            GC.DATABASE_FROM_LINE: 491,
                            GC.DATABASE_TO_LINE: 491,
                            GC.STRUCTURE_TESTCASE: {
                                1: [GC.CLASSES_TESTCASE,
                                    {GC.KWARGS_BROWSER: GC.BROWSER_FIREFOX,
                                     "BROWSER_ATTRIBUTES": {GC.BROWSER_MODE_HEADLESS: True},
                                     GC.KWARGS_TESTCASETYPE: GC.KWARGS_BROWSER},
                                    {GC.STRUCTURE_TESTSTEP:
                                        {
                                            1: "TestSteps.Frontend.VIGO.Produktauswahl.ProduktauswahlURL",
                                            2: "TestSteps.Frontend.Portal.Login",
                                            3: "TestSteps.Frontend.VIGO.Produktauswahl.ProduktAuswahl",
                                            4: "TestSteps.Frontend.VIGO.Antrag.Wohnen.ObjektSeite",
                                            5: "TestSteps.Frontend.VIGO.Antrag.Wohnen.Empfehlungen",
                                            6: "TestSteps.Frontend.VIGO.Antrag.Wohnen.Deckungsumfang",
                                            7: "TestSteps.Frontend.VIGO.Antrag.Wohnen.Praemienauskunft",
                                            8: "TestSteps.Frontend.VIGO.Antrag.Wohnen.Beratungsprotokoll",
                                            9: "TestSteps.Frontend.VIGO.Antrag.Wohnen.VertragsDaten",
                                            10: "TestSteps.Frontend.VIGO.Antrag.Wohnen.AntragsFragen",
                                            11: "TestSteps.Frontend.VIGO.Antrag.Vermittler",
                                            12: "TestSteps.Frontend.VIGO.Antrag.Dokumente",
                                            13: "TestSteps.Frontend.VIGO.Antrag.AntragSenden"
                                        },
                                    },
                                    ],
                            },
                        }],
                    },
                },
            },
            "Partner": {
                "DATAFILE": '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/testdata_wstv_fqa.xlsx',
                "SHEET": 'TC_Partner',
                "BROWSER": GC.BROWSER_FIREFOX,
                "BROWSER_ATTRIBUTES": "",
                GC.DATABASE_FROM_LINE: 2,
                GC.DATABASE_TO_LINE: 4
            },
            "SAP": {
                "DATAFILE": '/Users/bernhardbuhl/git/KatalonVIG/0testdateninput/testdata_wstv_fqa.xlsx',
                "SHEET": 'TC_Partner',
                "BROWSER": GC.BROWSER_FIREFOX,
                "BROWSER_ATTRIBUTES": "",
                GC.DATABASE_FROM_LINE: 2,
                GC.DATABASE_TO_LINE: 2
            },
            "API-DROPS": {
                "DATAFILE": '/Users/bernhardbuhl/git/baangt/dropsApiTest.xlsx',
                "SHEET": 'Tabelle1',
                GC.DATABASE_FROM_LINE: 1,
                GC.DATABASE_TO_LINE: 2
            }
        }

if __name__ == '__main__':
    #l_run = CustTestRun("Heartbeat")
    l_run = CustTestRun("Antrag-Single")
    l_run.executeTestRun()