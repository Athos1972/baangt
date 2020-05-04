# Current situation

The output files and input files used in baangt have to be opened by explorer/finder. They are not available directly
from within the app. 

We have 4 types of files:
* Simple Format XLSX: Testrun-definition and data in one file.
* Full Format 
    * XLSX: Testrun-definition with multiple tabs. Data-sheet is a separate XLSX, that can be 
      found via sheet "TestCaseSequence" in column "TestDataFileName". There can be multiple rows.
    * JSON: Testrun-definition in JSON-Format.
* Result-File of a test run
* Log-File of a test run

# Aim

Enable the user to open those files directly, not need Explorer/Finder or Python IDE to open the files.

## TestRun Definition and Data files:

* After the TestRun was selected, provide a button with icon https://material.io/resources/icons/?icon=open_in_new&style=baseline
  (or similar) in the line of TestRun-Dropdown.
* When the user clicks on it, open the file in the default application for the file type.
* If the file has a worksheet "TestCaseSequence", read through all the lines in column "TestDataFileName" and open those
  too. If one/more of the file(s) can't be found, log the problem and continue.
  
## Result file:

* After the testrun was finished, provide a button with icon https://material.io/resources/icons/?icon=open_in_new&style=baseline
  (or similar) in the statistics area of the UI main window next to the output filename.
* When the user clicks on it, open the file in the default application for the file type.

## Log file:

Same as result file (show Logfile-Name, show Icon, enable click).

# Implementation 
## UI:
* Implement as described above

## baangt.base:
* Have a new class "FilesOpen" with methods:
    * openTestRunDefinition(filenameAndPath: str)
    * openResultFile(filenameAndPath: str)
    * openLogFile(filenameAndPath: str)

Inside this class handle finding the files and OS-specific opening of the files.

# DoD

## UI:
* Button appears/is active when TestRun is selected, can be clicked and calls the method "openTestRunDefinition" 
  of the class FileOpen with str(filenameAndPath)
* Buttons appear/are active when TestRun was finished, can be clicked and call the method "openResultFile" or 
  "openLogFile" of the class FileOpen with str(filenameAndPath)
* Button for TestRun-File display disappears/is inactive when no TestRun was selected
* Button for Result and Log-File disappears/is inactive when no TestRun was executed yet or when a TestRun is currently 
  active
  
## baangt.base:
* Implemented and unit-tested on at least 2 OS (MacOS/Linux or Windows/Linux)
* Unit-Tests written. Coverage at least 80%. Example for test data in /tests/*-Folder
