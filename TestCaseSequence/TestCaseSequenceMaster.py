from baangt.HandleDatabase import HandleDatabase
import baangt.GlobalConstants as GC
import baangt.CustGlobalConstants as CGC
import logging

logger = logging.getLogger("pyC")


class TestCaseSequenceMaster:
    def __init__(self, **kwargs):
        self.name = None
        self.description = None
        self.testdataDataBase : HandleDatabase = None
        self.testrunAttributes = kwargs.get(GC.KWARGS_TESTRUNATTRIBUTES)
        self.testRunInstance = kwargs.get(GC.KWARGS_TESTRUNINSTANCE)
        self.testRunName = self.testRunInstance.testRunName
        self.dataRecords = {}
        self.recordCounter = 0
        # Extract relevant data for this TestSequence:
        self.testSequenceData = self.testrunAttributes[GC.KWARGS_TESTRUNATTRIBUTES][GC.STRUCTURE_TESTCASESEQUENCE].get(kwargs.get(GC.STRUCTURE_TESTCASESEQUENCE))[1]
        self.recordPointer = self.testSequenceData[GC.DATABASE_FROM_LINE]
        self.testCaseSequence = self.testSequenceData[GC.STRUCTURE_TESTCASE]
        self.kwargs = kwargs
        self.execute()

    def execute(self):
        self.__getDatabase()
        recordPointer = 0
        # Read all Testrecords into l_testRecords:
        while True:
            self.dataRecords[recordPointer] = self.getNextRecord()
            if not self.dataRecords[recordPointer]:
                self.dataRecords.pop(recordPointer)
                recordPointer -= 1
                break
            recordPointer += 1
        logger.info(f"{recordPointer+1} test records read for processing")

        # Execute all Testcases:
        for key, value in self.dataRecords.items():
            self.kwargs[GC.STRUCTURE_TESTCASESEQUENCE] = self.testSequenceData
            self.kwargs[GC.KWARGS_DATA] = value
            self.testRunInstance.executeDictSequenceOfClasses(self.testCaseSequence, GC.STRUCTURE_TESTCASE, **self.kwargs)
            # Write Result back to TestRun for later saving in export format
            self.testRunInstance.setResult(key, value)

    def getNextRecord(self):
        self.recordCounter += 1
        if self.testdataDataBase:
            if self.recordPointer > self.testSequenceData[GC.DATABASE_TO_LINE]:
                return None
        else:
            self.__getDatabase()

        lDataRecord = self.testdataDataBase.readTestRecord(self.recordPointer)
        self.recordPointer += 1
        return lDataRecord

    def __getDatabase(self):
        if not self.testdataDataBase:
            self.testdataDataBase = HandleDatabase()
            self.testdataDataBase.read_excel(fileName=self.testSequenceData["DATAFILE"],
                                             sheetName=self.testSequenceData["SHEET"])
        return self.testdataDataBase

    def finishTestCase(self, browserInstance=1, dataRecordNumber=None):
        if not dataRecordNumber:
            dataRecordNumber = self.recordCounter
            logger.debug(f"DataRecordNumber = {dataRecordNumber}")
        dataRecord = self.dataRecords[dataRecordNumber]
        if not self.testRunInstance.apiInstance:
            if len(dataRecord[GC.TIMING_DURATION]) == 0:
                # This was a failed testcase - didn't reach the end. Still take overall time:
                dataRecord[GC.TIMING_DURATION] = self.testRunInstance.browser[browserInstance].takeTime("Testfall gesamt")
            dataRecord[GC.TIMELOG] = self.testRunInstance.browser[browserInstance].returnTime()
            self.testRunInstance.browser[browserInstance].takeTimeSumOutput()
            self.testRunInstance.browser[browserInstance].resetTime()
        else:
            # FIXME: Auch für API-Tests brauchen wir eine Zeitaufzeichnung
            pass
        self.testRunInstance.setResult()

    def tearDown(self):
        pass