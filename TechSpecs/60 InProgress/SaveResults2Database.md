# Current situation

Currently all test runs are already saved in a database. This happens in baangt.base.ExportResults.ExportResults.py in
method exportToDataBase.

Saving happens for:
* Testrun name
* Logfile name
* Count of successful test cases
* Count of not successful test cases
* GlobalVars (JSON-String)
* Name of data file

This works well, but is not enough.

# Goal
We need to have more details about the test runs in the database, so that we can do more analytics, for instance:

* Comparison of durations of the same test case throughout an extended period of time
* Detect problematic services during longer running test cases

The above mentioned analytics is **not** part of this TechSpec.

# Implementation

* Extend data persistence to save all data, that is currently exported in XLSX-Format also for database
    (not as JSON into one field but as structured tables with columns).
    * For that to work (and for other purposes) each object (TestRun, TestcaseSequence, TestCase) must have a unique key, that can be saved in the database in order to have key-columns for the database tables.
        
         Each table will have the UUID as key field.
         
    * Also testDataDict for each test case needs to be stored. Info: During a test run fields can be added. So before
        saving testDataDict to an existing table of this testdata object, the structure needs to be checked and may need
        additional fields than in a previous execution.
    * Export UUID of test run (in summary tab) and test cases (in tab Output, Timing and Network) in XLSX-Export
         
* Add capability to save test case result data in additional export format.
    * When a column of testDataDict is in format ``$<objectname>-<fieldname>``:
        * For XLSX-Output:
           * Add a new tab to MS Excel and fill in the data into this tab. Tab-name is ``<stage>_<objectname>``. 
           * Create columns in the header: ``<stage>``, ``<uuid>`` of the test case, ``[<fieldname>]``
           * For each entry in testDataDict write ``stage``, ``uuid``,``<fieldname>`` into the appropriate column 
             in this Excel-Tab.
        * Into the database:
            * look for a table ``<stage>-<objectname>``.
            * If it exsits, check if ``[<fieldname>]`` are found in the structure
            * If it doesn't exist, create the table with structure ``uuid``, ``[<fieldname>]``
            * If needed, extend structure
            * Add also ``uuid`` of the test case.
            * Append entries similarly to XLSX above.
            
This will lead to double saving of the same data, once in testDataDict (e.g. in XLSX in Tab Output) and once in a separate
tab ``<stage>_<objectname>``. The reason for that is to provide a simpler way for users to extract such data from multiple
XLSX-Files into one database, in case they don't want to or can't use the built-in database storage.

# Examples for using the additionally stored data:
* Creating master data records (e.g. customers) in a certain stage (e.g. Test, Pre-Quality, Final-Quality, Migration, etc.)
  and re-using this data in other test cases (e.g. customer orders). In this case the user would first run the test cases
  that create master data, then Cross-reference the results in their customer order data records for this stage,
  and finally run those test cases (the cross-referencing happens in XLSX, for instance using VLOOKUP or VBA). 
            
# DoD (incl. rough effort estimation)

* XLSX and Database are populated with the above mentioned data (new fields, new Tables/Tabs) (6-8 hours)
* STAGE-variable existing in all TestRuns (default value = ``Test``). Hint: Can be set in HandleDatabase.py in __init__ 
  as e.g. GC.EXECUTION_STAGE = GC.EXECUTION_STAGE_TEST (0,5 hours)
* One working example file in /examples using multiple fields in format ``$<objectname>-<fieldname>`` including 
  output file committed to examples-folder. (2 hours)
* Updated documentation in /docs-Folder (1 hour)
* Unit-Test coverage (in folder /tests) of 80% (for all committed/changed methods) (4 hours)
* no critical linter errors or warnings (PEP-8 conformity of the code) (no additional effort)
