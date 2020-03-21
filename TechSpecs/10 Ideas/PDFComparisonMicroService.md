# Overview

In test cases we may have test steps, that download a PDF from a source. So far, we can only download the PDF, but not 
do anything with it.

# Aim
Aim of this TechSpec is to provide further support for working with PDFs. In a Twitter Poll 40% said, that they need
PDF-comparison for their automation tasks.

# Functional description
We want to be able to:
* Save a reference PDF
* Compare a newly created PDF to the reference PDF
* Define default deviations (for instance Dates, Times, Documentnumbers), that should not count as difference
* Get a status, whether the document matches the reference document
* If it doesn't match get a visual representation of the difference and get a list of differences at text

## Out of scope:
* No comparison of images between PDF-Files

# Technical overview
## UI
There needs to be a Flask-UI to add, change and delete reference PDFs for Test steps. PDFs shall be stored as BLOB in 
the database together with an UUID. The UUID is the reference parameter that will be used from test step to call into
comparison service.

The UI needs to provide a simple method to define exclusions of document contents from the comparison as well as a 
plugin/extension option for developers to develop higher sophisticated comparison logics.

## Backend
The comparison functionality should be implemented as a separate microservice to be called by test execution. Results of the 
microservice will be added to testDataDict in the test run. If there's a difference between the test runs, the two
PDFs (reference and current PDF) shall be added as OLE-Objects into Excel output.

Also creation and deletion of reference PDFs should be implemented using APIs, so that we're not depending only on the
UI component, but can later implement further functionality.

## baangt
Service discovery and API-Call to microservice for PDF-comparison need to be implemented in baangt using a new command in TestStepMaster.py 
"Compare". Value1 will be the UUID of the reference-PDF within the micro-service. 

In the step before "Compare" we'll need to download the PDF(s) or know, where the PDF was stored. 
This needs to work on all platforms and drivers (FF, Chrome, Safari), also when using remote driver like in Selenium Grid V4 
(integration currently under development) or Appium (branch "Appium" in GIT - should be finished by next week).

# DoD:
* Microservice created and pushed to new repository
    * Creation of new items with upload of PDF and return of UUID possible.
    * Viewing of created items (show UUID and provide PDF for download)
    * Update of reference PDFs (replace existing PDF with a new upload)
    * Update of ignored criteria
* baangt changes committed to a new branch and tested
    * test examples documented in /examples
* Technical documentation up2date (classes have Docstrings, Methods where needed)
* no critical linter errors or warnings (PEP-8 conformity of the code)