How to create a simple API Test
===============================

Now API-Tests are usually something, that the classic business people wouldn't know about. But with ``baangt`` and a bit
of effort it should be possible even for business people to do some simple API-Tests.

As with all tests in ``baangt`` also API-Tests are defined in a simple format in MS Excel. See ``EarthSquadSimpleAPI.xlsx``
as working example.

    Prerequisit for simple API definition format:

    * Filename must contain the word "api", otherwise simple format will try to create a browser test run

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
   * - ``HEADER``
     - Set additional parameters for the next API-Calls into the Header. In combination with the special fields (see below)
       it's easy to take a result from one API-Request and use it (or parts of it) as input for the next call.

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
