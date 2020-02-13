# Creation of address data

## Prerequisits

In many cases test master data (in this case addresses) needs to be created before any transactional data (e.g. sales orders,
user accounts, shipping information) can be processed.

Depending on the industry and use-case generation of this data might be of critical importance for the subsequent processes,
e.g. to test shipping fees for an international forwarding company you'll likely need test data in different countries.

When testing e.g. for property insurance you'll even need more distinct data to test business logic, that derives premium 
discounts and surcharges based on risk attributes of a certain address.

The more complex the data requirement is, the more likely testers start to prepare "their" own syntectic test data set (e.g.
1 address per parameter to test) and re-use this data over and over again for manual and automated tests. Very often this
leads to undetected errors (this one combination obviously works, but a slight deviation with real world data brings 
errors, that linger undetected in productive system) or false errors (e.g. a customer, who has 10.000 insurance contracts 
in Test-system and brings this in turn leads to wrongfully reported performance bottlenecks (which will never happen in 
production). This happens over and over again in many organizations. Time and money spent for wrong analysis hurts double! 
Once because it's money spent on activities, that don't deliver value. Second because time spent on those activities means 
less time for important improvements.). 

## Aim

``baangt`` should provide an easy and easily extendable way to generate address data for a test case. 

## Implementation

There needs to be a new activity "ADDRESS_CREATE" in SimpleFormat (``TestStepMaster.py``). Field ``value`` = optional list of 
attributes (see below), ``value2`` = prefix for fieldnames (optional).

When this activity is called, we shall call a singleton class "AddressGenerate" using the (optional) parameters from the
Value-Field. This class is **not** in scope of the current specification. The method "returnAddress" provides a dict of 
fields and values, which shall be stored in TestDataDict (with (optional) prefix taken from value2).

After the fields were filled, they'll be used by the testcase to fill in fields of the UI or API.

### Fields
The following fields are part of the return value of method ``returnAddress``:
* CountryCode**
* PostlCode**
* CityName
* StreetName
* HouseNumber
* AdditionalData1
* AdditionalData2

**These fields can be used as filter criteria in field ``value``. JSON-Format should be supported. Example of field ``Value``: {CountryCode:CY, PostlCode: 7*}.
Values must be mapped into a ``Dict``.

If a prefix was povided in field ``Value2``, the fieldnames shall be concatenated with this prefix, e.g. if 
prefix = ``PremiumPayer_``, then the resulting fieldname for ``CountryCode`` in testDataDict would become 
``PremiumPayer_CountryCode``.