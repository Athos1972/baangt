#TechSpec TestRun-Database
The database is a an alternative to creating testrun settings for baangt in XLSX. 
Working with the database provides - other than XLSX - also the option to reuse elements (TestCaseSequence, TestCase, TestStepSequence) inbetween testruns, while in XLSX-Format there is no referencing, only Copy+Past (and resulting maintenance issues)

##Create Database and UI for Testrun Definitions
Database and UI should be implemented using FLASK and ORM. Database SQLite is enough for now.
###Main entities
* Testrun
* TestCaseSequence (n:m to TestRun)
* DataFiles (n:m) to TestCaseSequence 
(For now baangt.py supports only 1 dataFile. Later this will be refactored to support multiple files. Also there will be an option to connect to a database and use Query as input)
* TestCase (n:m) to TestCaseSequence
* TestStepSequence (n:m) to TestCase
* TestStepExecution (1:n) to TestStepSequence

###Supporting entities
When a new database is created all entries in supporting entities shall be created (by ORM - not any db-specific command)
* GlobalTestStepExecution (identical to TestStepExecution table but for reusable TestSteps)
* ClassNames (Value table for Classnames in TestCaseSequence, TestCase, TestStepSequence)
* BrowserTypes (Value table for TestCase->BrowserType).
  * Values: FF, Chrome, IE, Safari, Edge
* TestCaseType (Value table for Testcase->TestCaseType)
  * Values: Browser, API-Rest, API-SOAP, API-oDataV2, API-oDataV4
* ActivityType (Value table for TestStepExecution->Activity)
  * Values: lots - see Note in Tab `TestStepExecution` in column `Activity`
* LocatorType (Value table for TestStepExecution->LocatorType)
  * Values: xpath, css, id

Supporting entities shall have language/locale depending descriptions, that will be used in the UI to display tooltips and/or explanations in Dropdown-Fields.
  
##Create the UI
Hierarchical display of testruns and all their subsequent entities. Most probably something like a Tree would be good with +/- Buttons to add/remove elements.

###Special treatment of Global Variables
GlobalVariables are stored in baangt.base.GlobalConstants.py - these variables shall be available at several places, additionally to manually entered values (see excel-sheet `DropsTestRunDefinition`)

###Testdatafiles:
Headers of testdatafiles must be read, so that the column names are available for selection in TestStepExecution-Steps for use in Column `Value` or `Value2` 

###Execution
There should be a "Run"-Button, which can be pressed whenever the user is inside a testrun (or any level below). When the button is clicke, all changes shall be saved to the database. `baangt.py` shall be called with the testrun-name of the currently active testrun in the UI. Further parameters need to be discussed.