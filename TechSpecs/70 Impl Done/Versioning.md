# Aim

In ``baangt`` simple XLSX and in complete XLSX-Formats there's a field ``Release`` for each TestStep. Right now this field
is not interpreted in the program.

The intended use of the field is described in the Docs in "SimpleExample" toward the end. Basically we should have an option
to conditionally (per stage) activate/deactivate testSteps (Example: In DEV-Stage you need to fill a field, which doesn't
(yet) exist in Quality-Stage. Instead of copying the test case and adding one statement in the Dev-Copy you'd add one TestStep
in the Testcase and put ">= " + the proper version of the Dev-Stage in the field "Release").

# Prerequisits

PyPi already supports several different approaches to software version numbering. We should implement the same logic in 
``baangt`` standard. If the user needs something else, they'll need to subclass the method. It's a prerequisit for this task
to understand the existing version logic used by PyPi.

# Field characteristics
* The field may be empty. In this case the TestStep will run no matter which version was set in Globals
* The field may have a condition in the first two characters ("<", ">", "=", "<>", "<=", ">=") followed by blank and 
the version number (e.g. ``>= 2019.05b``)

# Implementation

* First we need to extend BrowserDriver-Methods (``findBy`` and all callers) with a new optional variable ``release``. 
* A new parameter ``Release`` needs to be added to UI.py with a default value of None and stored in all globals.json. (Same logic
as was already added for "TC." + GC.DATABASELINES). 
    * If this parameter is set in Globals and a TestStep's line has the
field ``release`` filled, we shall use the PyPi-Logic to see, if the current version qualifies to run this line (this method
should be encapsulated, so that it can be easily subclassed by users).
    * If the line doesn't quality for execution, we shall document in the logs (Level=Debug), that we skipped this line due to 
{version_line} disqualifies according to {version_globals} and return to the caller.
* Additionally check, if the field is included in flask implementation. If not, add it to the model and prepare migration.
* Also make sure the field "Release" is correctly mapped in TestStepMaster.py, so that the value reaches the ``findBy`` methods.

# Test

* Write unit tests to show behaviour of comparison of version between globals and TestSteps.
* Write unit tests to show behaviour if no value was set in globals, but value in TestStep.
* Write unit zest to show behaviour if value is set in globals, but no value in TestStep.