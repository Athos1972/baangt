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
