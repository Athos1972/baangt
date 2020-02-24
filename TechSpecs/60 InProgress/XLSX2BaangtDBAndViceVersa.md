# Current Situation

We've currently 3 loosely connected ways how to define test runs (and testCaseSequences, testCases, TestStepSequences 
and teststeps) in baangt:

* SimpleFormat (XLSX): Has only 2 tabs ("TestStepExecution" and "data"). Very fast, very simple. No options for further
configuration except the options that come from "overriding" in globals. When interpreted by baangt interactive starter
or baangt CLI we actually create a complex XLSX with default values.
* Complex XLSX: Has a lot of tabs and all options, that we have in baangtDB. Multiple TestCases, Browsers, data files, 
and so on.
* BaangtDB: The flask app, that enables the users to have real modular test sequences and reuse sequences across all 
structural elements (e.g. Login-Page, commonly used "cards" in multiple test cases, etc.).

Directly connected to these definitions are the two following options to create customer/installation specific 
functionality:
* Subclassing: Some or all of the structural items of baangt standard are being subclassed and used instead of the standard
classes (only possible in Complex XLSX and in BaangtDB - where the executing class is a parameter).
* Plugins: Methods of the standard baangt can be redefined by using and activating plugins. These changes are also 
effective when using SimpleFormat (e.g. one could override the data source of SimpleFormat-XLSX to be something else)

# Problem

There is no support for switching between the options. Users need to be able to export and import when baangtDB is the
center of the installation.

## Processes

### Update of existing test cases:
Assume baangtDB is run by the central testmanagement department of the organization. baangt simple format is used by the business
departments all over the world. A new release of their software is about to come out and they need test cases to be 
adjusted to the local/regional specialities in pre-production stage. Central testmanagement department doesn't know, which specifics these are, 
but they know, which test cases aren't working on pre-production stage. Central testmanagement department wants to
generate SimpleFormat XLSX or Complex XLSX from a baangtDB-Testcase and send this XLSX to business departments in order to fix the 
definitions. (= Export from baangtDB to Complex XLSX).

### Adding new test cases:
Business department tests a new functionality and is happy with it. They want the testcase to be included to regression
test set. They send the SimpleFormat XLSX or Complex XLSX to central testmanagement department, who need to add those
test cases to certain test runs, defined in baangtDB. (= Import Complex XLSX to baangtDB).

# Implementation

## Flask import
* In Flask app create an import button on level Testrun. 
* When button is pressed upload XLSX, run through converter and save resulting objects in 
testrun-Database. 
* Show log of import (especially the object names, that were created)

## Flask export
* In Flask app create an export button on level Testrun.
* When button is pressed, create complex XLSX-Format. Filename = <Testrun-name><timestamp>.xlsx
* Download resulting XLSX to Frontend

# Scope / DOD
This task is considered completed after:
* Implementation provided (in line with coding standards and PEP-8 conformity)
* Functional test executed and passed
* Existing functionality not compromised - baangt Interactive Starter, baangt CLI and baangtDB work as before this change
* Enhance existing documentation in docs-Folder in RST-Format
    * For this task there will be a new page in Docs (Import/Export in baangtDB)
* Unit-Tests in tests-folder providing reasonable coverage of the newly created functionality
* git commit to feature branch and pull request on Gogs created