Special functions in datafiles
==============================

Datafiles (or in Excel Simple format simply a tab "data") generally hold the data for one or more testcases.

The first line of the datafile holds the header line. Each cell in the header must have a unique value and acts as variablename,
which you can use for checking, for IF-Statements or as values to write into fields or compare with assertions.

Additionally there are some reserved names that deliver the following functionality:

.. list-table:: Field names in Datafiles and their function
   :widths: 25 75
   :header-rows: 1

   * - Field name
     - Description
   * - ``TC Expected Error`` (!sic)
     - When set to value ``X``, the Test case is supposed to fail. If it fails (as expected) the status of the testcase is set to OK.
   * - ``JSON``
     - Please don't use this fieldname, as we're using it internally to store data.
   * - ``Timelog``
     - Please don't use this fieldname, as we're using it internally to store the timelog during execution of the test case.