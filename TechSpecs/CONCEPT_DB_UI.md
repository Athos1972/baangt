# Database and UI for Testrun Definitions
### TECHNICAL CONCEPT

## General
UI will be implemented as a Flask application. The source of the application will be located within a separated directory. The connection to the database will be implemented through environment variable `DATABASE_URL` for both applications. 

## Database
The database will be created using SQLAlcheny ORM. All the ORM classes will be defined in `CreateDatabaseORP.py` script within the `base` directory. There following database entities will be addressed:

#### _Main Entities_

#### Testrun
* ID (integer, primary key)
* name (string)
* logFileName (string)
* startTime (timestamp)
* endTime (timestamp)
* globalVars (string)

#### TestCaseSequence
* ID (integer, primary key)
* name (string)
* className (integer, foreign key ClassNames)
* startTime (timestamp)
* endTime (timestamp)

#### DataFile
* ID (integer, primary key)
* fileName (string)
* created (timestamp)

#### TestCase
* ID (integer, primary key)
* name (string)
* className (integer, foreign key ClassNames)
* browserType (integer, foreign key BrowserTypes)
* testCaseType (integer, foreign key TestCaseTypes)
* startTime (timestamp)
* endTime (timestamp)

#### TestStepSequence
* ID (integer, primary key)
* name (string)
* className (integer, foreign key ClassNames)
* startTime (timestamp)
* endTime (timestamp)

#### TestStepExecution
* ID (integer, primary key)
* name (string)
* activityType (integer, foreign key ActivityTypes)
* locatorType (integer, foreign key LocatorTypes)
* startTime (timestamp)
* endTime (timestamp)
* testStepSequence (integer, foreign key TestStepSequence)

#### _Relation Entities_

#### TestrunCaseSequence
* ID (integer, primary key)
* testrun (integer, foreign key Testrun)
* testCaseSequence (integer, foreign key TestCaseSequence)

#### TestCaseSequenceDataFile
* ID (integer, primary key)
* testCaseSequence (integer, foreign key TestCaseSequence)
* dataFile (integer, foreign key DataFile)

#### TestCaseSequenceCase
* ID (integer, primary key)
* testCaseSequence (integer, foreign key TestCaseSequence)
* testCase (integer, foreign key TestCase)

#### TestCaseStepSequence
* ID (integer, primary key)
* testCase (integer, foreign key TestCase)
* testStepSequence (integer, foreign key TestStepSequence)

#### _Supporting Entities_

#### GlobalTestStepExecution
* ID (integer, primary key)
* name (string)
* activityType (integer, foreign key ActivityTypes)
* locatorType (integer, foreign key LocatorTypes)
* startTime (timestamp)
* endTime (timestamp)
* testStepSequence (integer, foreign key TestStepSequence)

#### ClassNames
* ID (integer, primary key)
* name (string)
* description (string)

#### BrowserTypes
* ID (integer, primary key)
* name (string)
* description (string)

#### TestCaseTypes
* ID (integer, primary key)
* name (string)
* description (string)

#### ActivityTypes
* ID (integer, primary key)
* name (string)
* description (string)

#### LocatorTypes
* ID (integer, primary key)
* name (string)
* description (string)

Script _CreateDatabaseORP.py_ will address creating of the following initial values within the supporting entities:
* BrowserType values: FF, Chrome, IE, Safari, Edge
* TestCaseTypes values: Browser, API-Rest, API-SOAP, API-oDataV2, API-oDataV4
* ActivityTypes values: GOTOURL, SETTEXT, SETTEXT, CLICK
* LocatorTypes values: xpath, css, id

## UI
UI will be developed as a Flask single-page web-application with JavaScript snippets referenced by HTML templates. The access to the application web-page will require user authentication.

The back-end part will contain a set of models (similar to ones described in _Database_ section) to interact with the database. The connection will be implemented via _scoped session_ to ensure different users' interaction with the database are kept alive. The application will provide a set of _routes_ that deliver requested content to the user (namely the details on _Testrun_ elements and _add/remove/execute_ options). The options _add/remove_ will allow the user to change the database content. The option _execute_ will allow the user to run _baangt_ application.   

The front-end will provide dynamic appearance of the application web-page. The left part (1/3 of page width for large screen, 100% &ndash; for medium screen) will visualize the tree structure of the _Testrun_ elements with ability of expanding and collapsing of the elements. The right part will display the details on the _Testrun_ element including add/remove/execute options. The content update will be implemented via AJAX.