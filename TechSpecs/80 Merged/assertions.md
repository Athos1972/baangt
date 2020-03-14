# Situation
Currently ``baangt`` supports on the WEB click, settext, iframes, windowhandling and so on. There's also a way to access
values from elements and write them back to ``testDataDict``. But there are no classical assertions implemented.

# Aim
Assertions should be available in all test technologies (currently API and Browser). Assertions should follow the 
existing logic by using method ```findBy``` (similar to current implementation in ``findByAndWaitForValue``). This method
retrieves the value of an element but doesn't compare to a reference value. It could be a good base though for the assert
method (just call ``findByAndWaitForValue`` and compare result to given reference parameter in ``testdataDict``)

The simplest type of assertions are to read the attribute or text of an element and compare to a variable from ``testDataDict``.
They should also be available in Excel Simple Format (implementation in ``TestStepMaster`` in method ``executeDirect``). 

A more complex situation comes up, when the assertion is checked against an API. The sequence would be
* Execute SetText or Click or any sequence of activities
* Execute an API-Call, receive result
* Compare specific part of the result with a field value from ``testDataDict``

The most complex functionality is needed in asynchronous assertions, either by callback or from batch processing. This 
needs to be implemented by customer specific routines. The main point here is to set the Testcase into condition 
```GC.TESTCASESTATUS_PENDING``` and have a unique ID of the testrun and the TestCase-ID, that can be matched/found by 
asynchronous trigger, which would later set Testcasestatus accordingly (failed, OK).

# Implementation
For now we'll only implement the simplest type of assertions for Browsers and later tend to more complex implementations.

