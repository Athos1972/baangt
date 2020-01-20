import sqlite3

class TestRunDatabaseFill:
    def __init__(self, cursor):
        self.cursor = cursor
        self.fill()


    def fill(self):
        self.cursor.execute('insert into executionMethod (name, description, created, createdBy)'
                            'values ("Browser", "Execute with a Browser", "", "Franzi")')

        self.cursor.execute("""
        INSERT INTO "main"."locatorTypes" ("ID", "name", "description", "created", "createdBy", "changed", "changedBy") 
                VALUES ('1', 'XPATH', 'Locate via XPATH-Expression', '', 'Franzi', '', '');""")
        self.cursor.execute("""
        INSERT INTO "main"."locatorTypes" ("ID", "name", "description", "created", "createdBy", "changed", "changedBy") 
                VALUES ('2', 'ID', 'Locate via ID of the Element', '', 'Franzi', '', '');""")
        self.cursor.execute("""
        INSERT INTO "main"."locatorTypes" ("ID", "name", "description", "created", "createdBy", "changed", "changedBy") 
                VALUES ('3', 'CSS', 'Locate via CSS-Path of the Element', '', 'Franzi', '', '');
        """)

        self.cursor.execute("""
        INSERT INTO "main"."activityTypes" ("ID", "name", "description", "created", "createdBy", "changed", "changedBy") 
                VALUES ('1', 'GoToURL', 'Go to an URL', '', 'Franzi', '', '');""")
        self.cursor.execute("""INSERT INTO "main"."activityTypes" ("ID", "name", "description", "created", "createdBy", "changed", "changedBy") 
                VALUES ('2', 'SetText', 'Set Text of an Element', '', 'Franzi', '', '');""")
        self.cursor.execute("""INSERT INTO "main"."activityTypes" ("ID", "name", "description", "created", "createdBy", "changed", "changedBy") 
                VALUES ('3', 'Click', 'Click on an Element', '', 'Franzi', '', '');
        """)

        self.cursor.execute('insert into testrun (name, description, created, createdBy) '
                            'values ("Test1", "Test1", "", "Franzi")')

        self.cursor.execute('insert into testCaseSequence (name, description, testrunID, created, createdBy)'
                            'values ("Dummy", "Dummy", 1, "", "Franzi")')

        self.cursor.execute('insert into testCase (name, description, executionMethodID, methodParameters, testCaseSequenceID, created, createdBy)'
                            'values ("Dummy", "Dummy", 1, "FF", 1, "", "Franzi")')

        self.cursor.execute('insert into testStepSequence (name, description, testCaseID, created, createdBy)'
                            'values ("Dummy", "Dummy", 1, "", "Franzi")')

        self.cursor.executemany("""
        INSERT INTO "main"."testStep" ("ID", "name", "sequenceNumber", "description", "locatorTypeID", "locator", "activityTypeID", "value", "testStepSequenceID", "created", "createdBy", "changed", "changedBy") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, [('1', 'OpenURL', '1', 'Open EarthSquad Drops', '', '', '1', 'https://drops.earthsquad.global', '1', '', 'Franzi', '', ''),
                ('2', 'ENTER Username', '2', 'Enter Username', '2', '(//input[@step=''any''])[1]', '2', 'test12', '1', '', 'Franzi', '', ''),
                ('3', 'Enter Password', '3', 'Enter the password', '2', '(//input[contains(@step,''any'')])[2]', '2', 'franzi12', '1', '', 'Franzi', '', ''),
                ('4', 'Submit', '4', 'Click Submit', '2', '//div[@class=''q-btn-inner row col items-center justify-center''][contains(.,''(//div[contains(@class,"q-btn-inner row col items-center justify-center")])[5]'')]', '3', '', '1', ' ', 'Franzi', '', '')
                ])

        self.cursor.execute("""INSERT INTO "main"."testDataInput" 
                            ("name", "description", "path", "pathIsRelative", "tabName", "created", "createdBy", "changed", "changedBy") 
                            VALUES ('EarthSquad Test', 'Testfile for Earthsquad', '/earthsquad.xlsx', 'True', 'testdata', '', 'Franzi', '', '');""")

        self.cursor.execute("""INSERT INTO "main"."testDataInput" ("name", "description", "path", "pathIsRelative", "tabName", "created", "createdBy", "changed", "changedBy")
                            VALUES ('EarthSquad Test', 'Testfile for Earthsquad', '/earthsquad.xlsx', 'True', 'testdata2', '', 'Franzi', '', '');
        """)

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
        self.createExectionMethods()
        self.createActivityTypes()
        self.createLocatorTypes()
        self.createTestRun()
        self.createTestCaseSequence()
        self.createTestDataDefinition()
        self.createTestCase()
        self.createTestCase2TestData()
        self.createValidator()
        self.createTestStepSequence()
        self.createTestStep()
        pass

    def createMasterClasses(self):
        self.cursor.execute("""
        CREATE TABLE if not exists masterClasses (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            description text NOT NULL,
            CustomBrowserHandling text NOT NULL,
            CustomTestStep text NOT NULL,
            CustomGlobalConstants text,
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text,
            changedBy text
        )
        """)

    def createExectionMethods(self):
        self.cursor.execute("""
        CREATE TABLE if not exists executionMethod (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            description text NOT NULL,
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text,
            changedBy text
        )""")

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
        # Method_parameters = "FF", "CHROME", etc.
        self.cursor.execute("""
        CREATE TABLE if not exists testCase (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            description text NOT NULL,
            testCaseSequenceID integer,
            executionMethodID integer NOT NULL,
            methodParameters text NOT NULL, 
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text,
            changedBy text,
            FOREIGN KEY (testCaseSequenceID) REFERENCES testCaseSequence (ID),
            FOREIGN KEY (executionMethodID) REFERENCES executionMethod (ID)
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

    def createLocatorTypes(self):
        self.cursor.execute("""
          CREATE TABLE if not exists locatorTypes (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            description text NOT NULL,
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text ,
            changedBy text
        )         
        """)

    def createActivityTypes(self):
        self.cursor.execute("""
          CREATE TABLE if not exists activityTypes (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            description text NOT NULL,
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text ,
            changedBy text
        )         
        """)

    def createTestStep(self):
        self.cursor.execute("""
          CREATE TABLE if not exists testStep (
            ID integer PRIMARY KEY,
            name text NOT NULL,
            sequenceNumber int NOT NULL,
            description text NOT NULL,
            locatorTypeID integer,
            locator text ,
            activityTypeID integer NOT NULL,
            value text,
            testStepSequenceID integer,
            created text NOT NULL,
            createdBy text NOT NULL,
            changed text ,
            changedBy text ,
            FOREIGN KEY (testStepSequenceID) REFERENCES testStepSequence (ID),
            FOREIGN KEY (locatorTypeID) REFERENCES locatorTypes (ID),
            FOREIGN KEY (activityTypeID) REFERENCES activityTypes (ID)
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