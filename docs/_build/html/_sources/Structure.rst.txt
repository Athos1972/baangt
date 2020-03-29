Structure of baangt
===============================================

If you never used any test automation software before, these terms can be intimidating, but in reality it's all very simple.

We'll start from the bottom to the top.

TestStep
--------

A teststep is a single activity, for instance clicking on a button or sending a ``GET`` request to an API. A teststep has
a mandatory parameter ``Activity``. All other parameters depend on the chosen activity, for instance for Activitiy GOTOURL
you need only a value (the URL where the browser should go to).

For SetText you need a locatorType, the locator (which input field to send the text to) and the text itself.

A teststep may have a timeout setting. If none given, system default will be considered.

TestStepSequence
----------------
Many Teststeps together are a TestStepSequence. The Sequence just defines, in which order each individual TestStep is
executed. A TestStepSequence will provide timing information in the test report (Start- and End-Timestamps and
Duration in Seconds)

TestCase
--------
A Testcase is a Sequence of TestStepSequences. You might wonder, why this additional TestStepSequence is needed, why not
simply write the TestSteps directly into the TestCase.

First of all: you don't need the TestStepSequence. In the simple XLSX-Format this grouping area doesn't exist.
Second: Imagine you have a login-page, a product bucket, product return functionality and invoice reprint functionality in
your SPA and you want to test all of them. Obviously you'll have at least 3 Testcases, but in all of them you'll have to
do a login. You can use the TestStepSequence to extract this repeated Sequence.

In a Testcase we define not only the Sequence of TestStepSequences but also which type of Testcase (Browser, API, etc.)
this is.

TestCaseSequence
----------------

    Oh no, another level of confusion?!

One or many TestCases can be grouped into a TestcaseSequence. The TestCaseSequence holds the
connection to the datafile(s) to be used and which records to process in this TestRun. In a TestCaseSequence you could
for instance group together the execution of a WEB-Page TestCase and subsequently the execution of an API-Call to retrieve
results from another system. This scenario is of course mostly for corporate system landscapes, where the frontend (Web) communicates
more or less asynchronous with backend components like Hosts, CRM-Systems, SAP-Backends and so on.

By all means if you don't need it: don't use it. But in case you need it, it's good to know it's there.

TestRun
-------
You guessed it by now. A TestRun as the highest level is a sequence of TestCaseSequences. Why would you need another level of grouping here?

In End-2-End-Tests or Lifecycle tests you'd want to test the whole system's functionality along a value stream:

* Create Partner in CRM-System
* Use Partner for a Contract
* Deliver Contract
* Invoice Contract
* Dunn invoice
* Post Payment
* Close contract
* Flag all Documents for archiving
* Archive all documents

Each item of this list would be a TestCaseSequence with 1 to many testcases included, various systems, various Web-, API
and other Interfaces within each TestCase.

Again: If you don't need it, just don't use it. Every parameter has a default value assigned, so ``baangt`` will work
perfectly without you touching things you don't need.