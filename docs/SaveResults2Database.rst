Save Testrun Results to Database
================================

One of the options that ``baangt`` provides to save the results of the executed Testruns is using SQL database.

Tables
------

Table: ``testruns``
^^^^^^^^^^^^^^^^^^^
Table holds results of the executed Testruns: Testrun Logs

.. list-table::Testrun Logs
   :width: 25 15 60
   :header-rows: 1

   * - Column
     - Data Type
     - Description
   * - id
     - INTEGER
     - Primary key for Testrun Log.
   * - testrunName
     - VARCHAR
     - A name associated with the Testrun.
   * - logfileName
     - VARCHAR
     - Path to the logfile of the Testrun.
   * - startTime
     - DATETIME
     - Satrt time of the Testrun execution.
   * - endTime
     - DATETIME
     - End time of the Testrun execurtion.
   * - dataFile
     - VARCHAR
     - Path to the Data File of the Testrun.
   * - statusOk
     - INTEGER
     - Number of the successful test cases within the executed Testrun.
   * - statusFailed
     - INTEGER
     - Number of the failed test cases within the executed Testrun.
   * - statusPaused
     - INTEGER
     - Number of the paused test cases within the executed Testrun.


Table: ``testCaseSequences``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Table holds data on the executed test case sequences: TestCaseSequence Logs

.. list-table::TestCaseSequence Logs
   :width: 25 15 60
   :header-rows: 1

   * - Column
     - Data Type
     - Description
   * - id
     - INTEGER
     - Primary key for TestCaseSequence Log.
   * - testrun_id
     - INTEGER
     - Foreign key to ``testruns``
       Testrun that contains the test case sequence.


Table: ``testCases``
^^^^^^^^^^^^^^^^^^^^
Table holds data on the executed test cases: TestCase Logs

.. list-table::TestCase Logs
   :width: 25 15 60
   :header-rows: 1

   * - Column
     - Data Type
     - Description
   * - id
     - INTEGER
     - Primary key for TestCase Log.
   * - testcase_sequence_id
     - INTEGER
     - Foreign key to ``testCaseSequences``
       Test case sequence that contains the test case.


Table: ``globals``
^^^^^^^^^^^^^^^^^^
Table holds global variables of the executed Testruns

.. list-table::Globals
   :width: 25 15 60
   :header-rows: 1

   * - Column
     - Data Type
     - Description
   * - id
     - INTEGER
     - Primary key for the global variable.
   * - name
     - VARCHAR
     - Name of the global variable.
   * - value
     - VARCHAR
     - Value of the global variable.
   * - testrun_id
     - INTEGER
     - Foreign key to ``testruns``
       Testrun that contains the global variable.


Table: ``testCaseFields``
^^^^^^^^^^^^^^^^^^^^^^^^^
Table holds log fields of the executed test cases

.. list-table::Testcase Fields
   :width: 25 15 60
   :header-rows: 1

   * - Column
     - Data Type
     - Description
   * - id
     - INTEGER
     - Primary key for the field.
   * - name
     - VARCHAR
     - Name of the field.
   * - value
     - VARCHAR
     - Value of the field.
   * - testcase_id
     - INTEGER
     - Foreign key to ``testCases``
       Test case that contains the field.


Table: ``networkInfo``
^^^^^^^^^^^^^^^^^^^^^^
Table holds info on requests made while execution of the test cases

.. list-table::Network Info
   :width: 25 15 60
   :header-rows: 1

   * - Column
     - Data Type
     - Description
   * - id
     - INTEGER
     - Primary key for the network info.
   * - browserName
     - VARCHAR
     - Browser name that was used to make the request.
   * - status
     - INTEGER
     - The status code of the HTTP response.
   * - method
     - VARCHAR
     - The request method.
   * - url
     - VARCHAR
     - The requets URL.
   * - contentType
     - VARCHAR
     - Content-type header of the response.
   * - contentSize
     - INTEGER
     - The size of the response content.
   * - headers
     - VARCHAR
     - A string that represents a list of the response headers in format:
       ``{'name': HEADER_NAME, 'value': HEADER_VALUE}``
   * - params
     - VARCHAR
     - A string that represents alist of the request GET parameters in format:
       ``{'name': PARAMETER_NAME, 'value': PARAMETER_VALUE}``
   * - response
     - VARCHAR
     - The content of the response.
   * - startDateTime
     - DATETIME
     - The time when the request was sent.
   * - duration
     - INTEGER
     - The time ms that it took to recieve the response after the request was sent.
   * - testcase_id
     - INTEGER
     - Foreign key to ``testCases``
       Test case that contains the network info.
