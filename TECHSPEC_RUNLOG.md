# Testrun Log and Reporting
For easy comparison between stages, software versions and testcases we want to have a database of testruns

## Phase 1
### Create Database and entities
create (if not exisits) database and entities to save:
* Testrun-Name (from `baangt.base.TestRun.testRunName`)
* Logfile-Name (from `__init__.py->logFilename`)
* Start-Timestamp/End-Timestamp (Call to `Timing.takeTime` when TestRun starts and stops)
* values from globals.json (if used)
* *Datafile(s) used
* *Count of Testcases in each status (OK, Failed, Paused --> Values from `baangt.base.GlobalConstants.py` )

*This logic  is already implemented in ExportResults.py

### Extend TestRun.py to write into the database
* In the method `tearDown` of `baangt.base.TestRun.py` add a call to store the testrun execution data into the database.
