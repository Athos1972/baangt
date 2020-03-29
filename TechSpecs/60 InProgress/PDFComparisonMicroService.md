# Overview

In test cases we may have test steps, that download a PDF from a source. So far, we can only download the PDF, but not 
do anything with it.

# Aim
Aim of this TechSpec is to provide further support for working with PDFs. In a Twitter Poll 40% said, that they need
PDF-comparison for their automation tasks.

# Functional description
We want to be able to:
* Save a reference PDF for a test step
    * The test step versioning must still work (e.g. we must be able to create one reference PDF for each stage (Dev, Pre-Quality, Final-Quality, Migration, etc.)). This can be done by uploading different reference PDFs, receive different UUIDs and maintain multiple lines of test steps for each version/stage.
* Compare a newly created/downloaded PDF to the reference PDF
* Define default deviations (for instance Dates, Times, Documentnumbers), that should not count as difference
* Receive status info, whether the document matches the reference document
* If it doesn't match get a visual representation of the difference
* If it doesn't macht get a list of differences as delimited text

## Out of scope:
* No comparison of images between PDF-Files

# Technical overview
## UI
There needs to be a Flask-UI to add, change and delete reference PDFs for Test steps. PDFs shall be stored as BLOB in 
the database together with an UUID. The UUID is the reference parameter that will be used from test step to call into
comparison service.

The UI needs to provide a simple method to define exclusions of document contents from the comparison. The backend
needs to provide a plugin/extension option for developers to develop more sophisticated comparison logic.

## Backend
The comparison functionality should be implemented as a separate microservice to be called by test execution. Results of the 
microservice will be added to testDataDict in the test run. If there's a difference between the test runs, the two
PDFs (reference and current PDF) shall be returned to the caller.

Also creation and deletion of reference PDFs should be implemented using APIs, so that we're not depending only on the
UI component, but can later implement further functionality.

## baangt
Service discovery and API-Call to microservice for PDF-comparison need to be implemented in baangt using a new command in TestStepMaster.py 
"PDF-compare". Value1 will be the UUID of the reference-PDF within the micro-service. Value2 will be the downloaded PDF.
If the result is not ``OK``, we shall add the text difference to a field in the output XLSX and embed the two updated documents (original, reference).

### Deal with PDFs in Browser-Automation:
In the step before "Compare" we'll need to download the PDF(s) or know, where the PDF was stored. 
This needs to work on all platforms and drivers (FF, Chrome, Safari), also when using remote driver like in Selenium Grid V4 
(integration currently under development) or Appium (branch "Appium" in GIT - should be finished by next week).

# DoD:
* Microservice created and pushed to new repository (not part of baangt repository) (sum: 9,5 hours)
    * Creation of new items with upload of PDF, return of UUID, insert criteria to ignore differences, 
    description text (unlimited length). --> 6 hours
    * Viewing of created items (show UUID and provide PDF for download) --> 0,5 hour
    * Update of reference PDFs (replace existing PDF with a new upload) --> 1 hour
    * Update of criteria to ignore differences and description text --> 1 hour
    * Search for UUID and fulltext in description text --> 1 hour
* baangt changes (deal with PDF-Downloads, new method "PDF-compare") committed to a new branch and tested (2 hours)
    * test examples documented in /examples (1 hour)
* Technical documentation up2date (classes have Docstrings, Methods where needed) (no additional effort)
* Documentation of Microservice and updated documentation of baangt parameters in /docs-Folder (2 hours)
* Unit-Tests with at least 80% code coverage written and successful (3 hours)
* no critical linter errors or warnings (PEP-8 conformity of the code) (no additional effort)