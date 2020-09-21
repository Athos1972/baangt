How to create a simple API Test
===============================

API-Tests are usually something, that the classic business people wouldn't know about. With ``baangt`` and a bit
of effort it should be possible even for business people to do some simple API-Tests.

As with all tests in ``baangt`` also API-Tests are defined in a simple format in MS Excel. See ``MovieSimpleAPI.xlsx``
as working example.

    Prerequisit for simple API definition format:

    * Filename must contain the word "api", otherwise simple format will try to create a browser test run.

Steps to test the simple API Format:
------------------------------------

Fire up ``baangt``, chose file ``MovieSimpleApi.XLSX`` as your run definition. Start the testrun by clicking on the
button ``Execute``.  After a few seconds you should see the popup "Testrun finished". Now open the result file
``baangt_MovieSimpleAPI_<date>.xlsx`` and see overview and details of the API Test run.

Play around
^^^^^^^^^^^

To extend this very simple example you could want to add the field "Actors" to your result sheet. To do so, add one line
in the Tab ``TestStepExecution``.

* ``Activity`` is ``SAVE``
* ``Value`` is ``RESULT_Actors``
* ``Value2`` is ``$(ANSWER_CONTENT.Actors)``

Save the Excel-Sheet. Re-run the test case and you should see the new column "Result_Actors" with the values retrieved
from the API.

Activities for API-Tests:
-------------------------

(Even though we write all activtities in UPPER CASE, you can write them in any way you like)

.. list-table:: Values for Activities for simple API format
   :widths: 25 75
   :header-rows: 1

   * - Activity
     - Description
   * - ``APIURL``
     - Set's the main URI/URL for your API-Tests. Could be omitted, if you want to always specify full path in ENDPOINT.
   * - ``ENDPOINT``
     - Set's the Endpoint-Name for the following API-Call. E.g. if your Endpoint is located at
       https://app-eu.earthsquad.global/api/rest-auth/login and during this test case execution you'd call a lot of APIs
       on this server, then you'd set ``APIURL`` to https://app-eu.earthsquad.global and set ``ENDPOINT`` to "/api/rest-auth/login"
   * - ``POST``
     - Send a "POST"-Request to the API. Place the content, that you want to send to this endpoint in the column ``value``
   * - ``GET``
     - Send a "GET"-Request to the API. URL-Parameters are taken from ``APIURL`` and ``ENDPOINT``. Result is stored for
       immediate retrieval (see below).
   * - ``HEADER``
     - Set additional parameters for the next API-Calls into the Header. In combination with the special fields (see below)
       it's easy to take a result from one API-Request and use it (or parts of it) as input for the next call.
   * - ``SAVE``
     - Save a value from the header or from result to output file (XLSX). ``value`` is the field-name. If you name it
       "RESULT_<something>" it is automatically added to the export field list. If you work in API-Simple mode, this is
       your only chance to get fields added into the result sheet.
       ``value2`` is the source (e.g. ``$(ANSWER_CONTENT.imdbRating)`` would retrieve the value "imdbRating" of the
       answer of your API-Call.

   * - ``ASSERT``
     - This  will retrieve value of element specified by `locator`
       And compare with expected_value specified in `value`
      
       if expected_value not matches with output_value it will raise TestStepExecution and result in FAILED.

   * - ``ADDRESS_CREATE``
     - Create  Address Data for various test cases  and save in testDataDict
       The following field variable can be used via $(field_name).
       
       ['HouseNumber', 'AdditionalData1', 'AdditionalData2', 'StreetName', 'CityName', 'PostalCode', 'CountryCode']
    
       Example:
        Default Data: (value=<blank> and value2=<blank>)
        'HouseNumber': '6', 'AdditionalData1': 'Near MahavirChowk', 'AdditionalData2': 'Opposite St. Marish Church', 'StreetName': 'GoreGaon', 'CityName': 'Ambala', 'PostalCode': '160055', 'CountryCode': 'India'

       `value` optional
        if provided : (value= {"CountryCode":"US","CityName":"Athens"} value2=<blank>)
         FieldValue updated to:
         {'HouseNumber': '6', 'AdditionalData1': 'Near MahavirChowk',
         'AdditionalData2': 'Opposite St. Marish Church',
         'StreetName': 'GoreGaon', 'CityName': 'Athens',
         'PostalCode': '160055', 'CountryCode': 'US'}
 

       `value2` optional

        Field will be prefixed with "office_<field_name>". Ex. "office_CountryCode"


Special data fields in API-Tests:
---------------------------------

In WEB-Testing you check results either via ``Assert``-Statement or via mapping the text or attribute of an element to a
field in the TestDataDictionary. In API-Tests you have some automatic internal variables, that you can use without
manually declaring them:

.. list-table:: Special Internal Variables in API-Testing
    :widths: 25 75
    :header-rows: 1

    * - Variable
      - Contents
    * - RESULT_CODE
      - Result code of the last call to an API. Ideally you'd be able to match result codes as described in here
        https://restfulapi.net/http-status-codes/, but in the end setting the status code is the job of the developer of
        the API you're using - they might follow a different path or simply have bugs.
    * - ANSWER_HEADER
      - Last Header. You can access a certain part of the header by using $(ANSWER_HEADER.<partName>), so if you want to
        use the part ``login_key`` of a header you'd write ``$(ANSWER_HEADER.LOGIN_KEY)``
    * - ANSWER_CONTENT
      - Last content of an API-Call (Post, Get, etc.). Again you can access/extract/replace parts of this content using
        the "." like described in the line above (e.g. ``$(ANSWER_CONTENT.FRANZI)`` to refer to a content part ``FRANZI``.

Random
------
Sometimes we need random values like string, name, integer, float, date, time now in such case we have ``random``
functionality. It is used inside value column of and its structure is
``$(random{"type":<Type>},"min":<Minimum>,"max"<Maximum>,"format":<Format>)``. Only ``type`` field is compulsory and
every other fields are optional, also each fields are not useful in every type, e.g.- ``name`` type doesn't need any
other optional fields as they are use less for it. You can see fields and types supporting them.


.. list-table:: Fields supporting types
   :widths: 25 75
   :header-rows: 1

   * - Field
     - Type

   * - type
     - This field is compulsory and base of ``random`` funtionality.
       string, name, int, float, date, time are the types currently supported

   * - min
     - string, int, float, date, time are the types supporting this field. Value of min will be with respect to its
       type like value for string will be an integer containing minimum number of characters in string and for all other
       it will be lower limit, for int it will be an integer & float for float, for date value will be a date e.g. -
       "31/01/2020" and for time it would look like "20:30:59"

   * - max
     - string, int, float, date, time are the types supporting this field. Value of max will be same like in min,
       value for string will be an integer containing maximum number of characters in string and for all other it
       will be upper limit, for int it will be an integer & float for float, for date value will be a date e.g. -
       "01/06/2020" and for time it would look like "13:10:30"

   * - format
     - date, time are the only types supporting format field. In above date examples date is in %d/%m/%Y format and
       time is in %H:%M:%S format. Here "%d" stands for the day, "%m" stands for month, "%Y" stands for year including
       century e.g.- 2020, if you want only year you can use "%y" e.g. 20. If you use min and max fields in date, time
       then you must input its written format in format field, default will be ""%d/%m/%Y" for date. Now if you want
       date with "-" as seperator you can write format as "%d-%m-%Y" so the output would be like "31-01-2020".

       `examples`
        $(random{"type":"name"})
        $(random{"type":"string", "min":10, "max":100})
        $(random{"type":"int", "min":10, "max":100})
        $(random{"type":"float"})
        $(random{"type":"date", "min":"20/1/2020", "max":"30/6/2020", "format":"%d/%m/%Y"})
        $(random{"type":"time"})
        $(random{"type":"time", "min":"10.30.00", "max":"15.00.00"}, "format": "%H.%M.%S")
