# Multiprocessing
In baangt.TestCaseSequenceMaster.py in method execute_parallel the class TestCaseSequenceParallel is called and executed.

This works well on Mac and Ubuntu. But doesn't work on Windows.

Also on Mac and Ubuntu the performance using this technique is not ideal, as all executations wait for the last task to 
finish before they start a new iteration.

# Goals
Change from process based multiprocessing to thread based parallel processing (using standard module Threads instead of 
Multiprocessing)

# DoD:
* Usage of `threading` and `Queue` instead of `multiprocessing` library to start parallel browsers and execute testcases
in parallel.
* After execution of Testcase latest data from Testcase (`TestdataDict`) is updated in `TestRun.py`
* Functionality was tested locally on either Linux and/or Windows and/or Mac and results documented (e.g. Log-File 
showing successful execution)
* Pull request was created