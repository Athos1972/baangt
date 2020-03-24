# Multiprocessing
In baangt.TestCaseSequenceMaster.py in method execute_parallel the class TestCaseSequenceParallel is called and executed.

This works as designed on Mac and Ubuntu. But doesn't work on Windows.

Also on Mac and Ubuntu the performance using this technique is not ideal, as all executions wait for the last task to 
finish before they start a new iteration.

# Goals
Change from process based multiprocessing to thread based parallel processing (using standard module Threads instead of 
Multiprocessing).

Executions run in real parallel, for instance if we have 4 parallel executions, each one of them starts the next
test case as soon as it was finished with the test case before.

# Current implementation
Current implementation is in baangt.TestCaseSequence.TestCaseSequenceMaster.py and from there calls 
baangt.TestCaseSequenceParallel.py when parameter ``ParallelRuns`` has a value greater than 1.

# Further documentation:
baangt documentation is on https://baangt.readthedocs.io
Repository is on https://gogs.earthsquad.global/athos/baangt

# DoD:
* Usage of `threading` and `Queue` instead of `multiprocessing` library to start parallel browsers and execute testcases
in parallel.
* After execution of Testcase latest data from Testcase (`TestdataDict`) is updated in `TestRun.py` (=same behaviour as 
  in the current implementation)
* Functionality was tested locally on either Linux and/or Windows and/or Mac and results documented (e.g. Log-File 
showing successful execution)
* Pull request was created