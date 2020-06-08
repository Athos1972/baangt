Dealing with variables
======================

You know the basic variable format ``$(ColumnFromDataFile)`` which works in Locators and value fields.

For instance:
    * ``//@id[$(SomeColumnName)]`` will replace the locator at run time with the content of the data file of column ``SomeColumnName``
    * ``$(URL)`` in the Value 1 or Value 2 will replace the Value at run time with the content of the data file of column ``URL``

You may combine several variables into one expression
    * ``http://($(BASEURL)-$(URLPART)`` will work, if your data file has the columns ``BASEURL`` and ``URLPART``.
      Most probably you guessed it already - Column names are case sensitive. And columns may not be used twice.

Special variables for APIs
--------------------------
TODO: Write Doku.

Faker
-----

From Version 2020.04.6rc4 (April 2020) you can also use all the methods, that the famous python module ``Faker`` provides.

The syntax is:
``$(FAKER.<methodName>)``

Examples:
    * ``$(FAKER.email)`` will generate random E-Mail addresses
    * ``$(FAKER.name)`` will generate a random name

To see all the methods, head over to https://faker.readthedocs.io/en/stable/fakerclass.html. Because you use ``baangt``
you can use all Faker Methods without writing a single line of code.

Info for Developers
^^^^^^^^^^^^^^^^^^^

Source in ``baangt.base.Faker.py``. Called from ``baangt.TestSteps.TestStepMaster.py`` from ``__getFakerData``.
Currently it is not supported to hand over parameters.