# Situation (Munish)

Right now when you start ``baangt`` interactive starter, choose a testrun and globals file and execute the testrun there's
a log either in the console or in your IDE (depending from where you start it), but directly in the UI you don't see
anything except an hourglass.

# Aim

## Statistics
In the right area of the UI (under the logo), we should have a section showing statistical information (number of testcases
to execute, count of testcases executed, count of testcases successful, count of testcases paused, count of testcases failed
and overall duration since test case start).

Under this, the count of executed TestCaseSequences, TestCases, TestStepSequences and TestSteps should be displayed.

## Logs
Additionally in the lower part of the window a section should appear (and disappear when the test run is finished), that
shows the Info/Error/Warning-Messages that are logged.

# Additional information

Apart from using these statistical information in the current UI, the flask-Implementation will also use the same information.
To be efficient, we'll need to have data gathering in one separate class, that can be used by current UI as well as flask. 
Current flask implementation is in directory flask.

# Implementation

Majority of the data points can be found/derived from ``baangt.base.TestRun.TestRun`` in the method ``executeDictSequenceOfClasses``
(see documentation there). For single runs (one browser or one API-Session), that should work fine.

Parallel runs are different/difficult (``TestCaseSequence.TestCaseSequenceParallel``) as they run in a different Python instance 
than the UI. This means, that during runtime of the parallel sequence a Queue must be written from the parallel runs
and read from within the UI.

Most probably to display the logs inside UI the logger needs to be changed. It's defined in ``baangt.__init__.py``

## Scope / DOD
This task is considered completed after:
* Implementation provided (in line with coding standards and PEP-8 conformity)
* Functional test executed and passed
* Existing functionality not compromised - baangt background mode works as before this change
* Enhance existing documentation in docs-Folder in RST-Format
* Unit-Tests in tests-folder providing reasonable coverage of the newly created functionality
* git commit to feature branch and pull request on Gogs created