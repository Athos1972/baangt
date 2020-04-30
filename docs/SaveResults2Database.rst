Save Testrun Results to Database
================================

One of the options that ``baangt`` provides to save the results of the executed Testruns is using an SQL database.
The identification of the database is implemented via the environmental variable BAANGT_RESULTS_DATABASE_URL.
if ``baangt`` cannot retrieve BAANGT_RESULTS_DATABASE_URL it uses the default database URL:  
``sqlite:///testrun.db``

Tables
------

Table: ``testruns``
^^^^^^^^^^^^^^^^^^^
Table holds results of the executed Testruns: Testrun Logs

.. list-table:: Testrun Logs
   :widths: 25 15 60
   :header-rows: 1

   * - Column
     - Data Type
     - Description
   * - id
     - BINARY
     - Testrun Log UUID. Primary key for Testrun Log.
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

.. list-table:: TestCaseSequence Logs
   :widths: 25 15 60
   :header-rows: 1

   * - Column
     - Data Type
     - Description
   * - id
     - BINARY
     - TestCaseSequence Log UUID. Primary key for TestCaseSequence Log.
   * - testrun_id
     - INTEGER
     - Foreign key to ``testruns``
       Testrun that contains the test case sequence.


Table: ``testCases``
^^^^^^^^^^^^^^^^^^^^
Table holds data on the executed test cases: TestCase Logs

.. list-table:: TestCase Logs
   :widths: 25 15 60
   :header-rows: 1

   * - Column
     - Data Type
     - Description
   * - id
     - BINARY
     - TestCase Log UUID. Primary key for TestCase Log.
   * - testcase_sequence_id
     - INTEGER
     - Foreign key to ``testCaseSequences``
       Test case sequence that contains the test case.


Table: ``globals``
^^^^^^^^^^^^^^^^^^
Table holds global variables of the executed Testruns

.. list-table:: Globals
   :widths: 25 15 60
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

.. list-table:: Testcase Fields
   :widths: 25 15 60
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

.. list-table:: Network Info
   :widths: 25 15 60
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
     - The request URL.
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
     - A string that represents a list of the request GET parameters in format:
       ``{'name': PARAMETER_NAME, 'value': PARAMETER_VALUE}``
   * - response
     - VARCHAR
     - The content of the response.
   * - startDateTime
     - DATETIME
     - The time when the request was sent.
   * - duration
     - INTEGER
     - The time (in ``ms``) that it took to receive the response after the request was sent.
   * - testcase_id
     - INTEGER
     - Foreign key to ``testCases``
       Test case that contains the network info.


For Developers: ORM API
--------------------------

``baangt`` provides ORM models to facilatate analysis of Testruns results.
The models are located in module ``baangt.base.DataBaseORM``


TestrunLog
^^^^^^^^^^^
Provides interface with table ``testruns``

.. list-table:: baangt.base.DataBaseORM.TestrunLog
   :widths: 30 70
   :header-rows: 1

   * - Attribute
     - Description
   * - id
     - Testrun Log UUID as a bianry string.
   * - testrunName
     - Name of the associated TestRun.
   * - logfileName
     - Path to the associated log file.
   * - startTime
     - TestRun start time as a ``datetime.datetime`` object.
   * - endTime
     - TestRun start time as a ``datetime.datetime`` object.
   * - dataFile
     - Path to the associated Data File.
   * - statusOk
     - Number of the successful test cases.
   * - statusFailed
     - Number of the failed test cases.
   * - statusPaused
     - Number of the paused test cases.
   * - globalVars
     - List of the global attributes (as ``GlobalAttribute`` instances) of the associated Testrun.
   * - testcase_sequences
     - List of the test case sequences (as ``TestCaseSequenceLog`` instances) within the associated Testrun.
   * - __str__()
     - Method. Returns Testrun Log UUID as a string.
   * - to_json()
     - Method. Returns Testrun Log as a dictionary object.


TestCaseSequenceLog
^^^^^^^^^^^^^^^^^^^
Provides interface with table ``testCaseSequences``

.. list-table:: baangt.base.DataBaseORM.TestCaseSequenceLog
   :widths: 30 70
   :header-rows: 1

   * - Attribute
     - Description
   * - id
     - TestCase Sequence Log UUID as a bianry string.
   * - testrun
     - The associated Testrun (as a ``TestrunLog`` instance).
   * - testcases
     - List of the test cases (as ``TestCaseLog`` instances) within the associated Test Case Sequence.
   * - __str__()
     - Method. Returns TestCase Sequence Log UUID as a string.
   * - to_json()
     - Method. Returns TestCase Sequence Log as a dictionary object.


TestCaseLog
^^^^^^^^^^^
Provides interface with database table ``testCases``

.. list-table:: baangt.base.DataBaseORM.TestCaseLog
   :widths: 30 70
   :header-rows: 1

   * - Attribute
     - Description
   * - id
     - TestCase Log UUID as a bianry string.
   * - testcase_sequence
     - The associated Test Case Sequence (as a ``TestCaseSequenceLog`` instance).
   * - fields
     - List of the attributes (as ``TestCaseField`` instances) of the associated Test Case.
   * - networkInfo
     - List of the network requests (as ``TestCaseNetworkInfo`` instances) made while executing the associated Test Case.
   * - __str__()
     - Method. Returns TestCase Log UUID as a string.
   * - to_json()
     - Method. Returns TestCase Log as a dictionary object.


GlobalAttribute
^^^^^^^^^^^^^^^
Provides interface with table ``globals``

.. list-table:: baangt.base.DataBaseORM.GlobalAttribute
   :widths: 30 70
   :header-rows: 1

   * - Attribute
     - Description
   * - name
     - Name of the global attribute.
   * - value
     - Value of the global attribute as a string.
   * - testrun
     - The associated Testrun (as a ``TestrunLog`` instance).


TestCaseField
^^^^^^^^^^^^^
Provides interface with table ``testCaseFields``

.. list-table:: baangt.base.DataBaseORM.TestCaseField
   :widths: 30 70
   :header-rows: 1

   * - Attribute
     - Description
   * - name
     - Name of the Test Case Field.
   * - value
     - Value of the Test Case Field as a string.
   * - testcase
     - The associated test case (as a ``TestCaseLog`` instance).


TestCaseNetworkInfo
^^^^^^^^^^^^^^^^^^^
Provides interface with table ``networkInfo``

.. list-table:: baangt.base.DataBaseORM.TestCaseField
   :widths: 30 70
   :header-rows: 1

   * - Attribute
     - Description
   * - browserName
     - Browser name that mede the request.
   * - status
     - Status code of the request as an integer.
   * - method
     - The request method used.
   * - url
     - The request URL.
   * - contentType
     - Type of the response content as a string.
   * - contentSize
     - Size of the response content as an integer.
   * - headers
     - A lList of the response headers as a string.
   * - params
     - A list of the request GET parameters as a string.
   * response
     - The response content as a string.
   * - startDateTime
     - The request start time as a ``datetime.datetime`` object.
   * - duration
     - The duration of the request in ``ms``.
   * - testcase
     - The associated test case (as a ``TestCaseLog`` instance).
   * - to_json()
     - Method. Returns the network info as a dictionary object.
