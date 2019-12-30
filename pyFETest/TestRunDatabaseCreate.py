import sqlite3

class TestRunDatabaseFill:
    def __init__(self, cursor):
        self.cursor = cursor
        self.fill()

        pass

    def fill(self):
        self.cursor.execute('insert into testrun (name, description, created, createdBy) '
                            'values ("Test1", "Test1", "", "Franzi")')
        self.cursor.execute('insert into testCaseSequence (name, description, testrunID, created, createdBy)'
                            'values ("Dummy", "Dummy", 1, "", "Franzi")')
        self.cursor.execute('insert into testCase (name, description, method, method_parameters, testCaseSequenceID, created, createdBy)'
                            'values ("Dummy", "Dummy", "BROWSER", "FF", 1, "", "Franzi")')

        self.cursor.execute('insert into testStepSequence (name, description, testCaseID, created, createdBy)'
                            'values ("Dummy", "Dummy", 1, "", "Franzi")')

        self.cursor.execute('insert into testStep (name, sequenceNumber, description, locatorType, locator, activity, value, testStepSequenceID, created, createdBy)'
                            'values ("OpenURL", 1, "Open EarthSquad Drops", "URL", "", "OPEN", "https://drops.earthsquad.global", 1, "", "Franzi")')

        self.cursor.execute('insert into testStep (name, sequenceNumber, description, locatorType, locator, activity, value, testStepSequenceID, created, createdBy)'
                            'values ("ENTER Username", 2, "", "XPATH", "franzi", "SETTEXT", "test", 1, "", "Franzi")')



class TestRunDatabaseCreate:
    """
    Initializes the Database and loads some sample data
    """
    def __init__(self, dbConnection=None):
        if dbConnection:
            self.dbCon = dbConnection
        else:
            self.dbCon = sqlite3.connect("test.db")
        self.cursor = self.dbCon.cursor()
        self.createStructures()

    def getCursor(self):
        return self.cursor

    def commit(self):
        self.dbCon.commit()

    def createStructures(self):
        self.createTestRun()
        self.createTestCaseSequence()
        self.createTestDataDefinition()
        self.createTestCase()
        self.createTestCase2TestData()
        self.createValidator()
        self.createTestStepSequence()
        self.createTestStep()
        pass

    def createTestRun(self):
        self.cursor.execute("""
        CREATE TABLE if not exists testrun (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            description text NOT NULL,
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text,
            changedBy text
        )""")

    def createTestCaseSequence(self):
        self.cursor.execute("""
        CREATE TABLE if not exists testCaseSequence (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            description text NOT NULL,
            testrunID integer,
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text,
            changedBy text,
            FOREIGN KEY (testrunID) REFERENCES testrun (ID)
        )        
        """)

    def createTestCase(self):
        # Method = "BROWSER",
        # Method_parameters = "FF", "CHROME", etc.
        self.cursor.execute("""
        CREATE TABLE if not exists testCase (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            description text NOT NULL,
            testCaseSequenceID integer,
            method text NOT NULL,
            method_parameters text NOT NULL, 
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text,
            changedBy text,
            FOREIGN KEY (testCaseSequenceID) REFERENCES testCaseSequence (ID)
        )        
        """)

    def createTestDataDefinition(self):
        self.cursor.execute("""
         CREATE TABLE if not exists testDataInput (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            description text NOT NULL,
            path text,
            pathIsRelative boolean,
            tabName text,
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text,
            changedBy text
        )               
        """)

    def createTestCase2TestData(self):
        self.cursor.execute("""
          CREATE TABLE if not exists testCaseData (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            testDataInputID integer,
            testCaseID integer,
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text ,
            changedBy text ,
            FOREIGN KEY (testDataInputID) REFERENCES testDataInput (ID),
            FOREIGN KEY (testCaseID) REFERENCES testCase (ID)
        )         
        """)

    def createTestStepSequence(self):
        self.cursor.execute("""
          CREATE TABLE if not exists testStepSequence (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            description text NOT NULL,
            testCaseID integer,
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text ,
            changedBy text ,
            FOREIGN KEY (testCaseID) REFERENCES testCase (ID)
        )         
        """)

    def createTestStep(self):
        self.cursor.execute("""
          CREATE TABLE if not exists testStep (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            sequenceNumber int NOT NULL,
            description text NOT NULL,
            locatorType text NOT NULL,
            locator text ,
            activity text NOT NULL,
            value text,
            testStepSequenceID integer,
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text ,
            changedBy text ,
            FOREIGN KEY (testStepSequenceID) REFERENCES testStepSequence (ID)
        )         
        """)

    def createValidator(self):
        self.cursor.execute("""
        CREATE TABLE if not exists testValidator (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            validatorType text NOT NULL,
            locatorType text NOT NULL,
            locator text NOT NULL,
            compareValue text NOT NULL,
            compareOption text NOT NULL,
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text ,
            changedBy text 
        ) 
        """)

if __name__ == '__main__':
    lDb = TestRunDatabaseCreate()
    lCursor = lDb.getCursor()
    lInsert = TestRunDatabaseFill(lCursor)
    lDb.commit()