import sqlite3

class TestRunDatabase:
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

    def createStructures(self):
        self.cursor.execute("""
        CREATE TABLE if not exist testrun ()""")
