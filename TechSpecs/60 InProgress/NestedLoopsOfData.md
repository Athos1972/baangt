# Current situation

```baangt``` provides a simple way to run test automation with as little as one Microsoft Excel File (of course with
reduced functionality, compared to full Excel format or ``baangtDB``). This works well as long as data for one test case
can be read from one line in the data-file or data-tab (simple format).

When we have nested data, it's not easily possible to process it, for example:

* Sales order -> currently possible with baangt simple format. All good
* Line items -> currently only possible by extending the fields of sales order with e.g. ```item_01_materialnumber```, 
  ``item_01_quantity``, ``item_02_materialnumber``, ``item_02_quantity`` and so on.
* Schedule items (e.g. 10 pieces in June, 20 pieces in July, etc.) -> with the current data structure not possible.

# functional requirement

We need to provide a simple way to deal with nested data structures like in the example above, without the user having
to code. 

# Solution approach

## Provide JSON-Arrays in Excel cells.

Enable ``baangt`` to read data from cells as arrays: 
```
[{line-item-number: 1,
  material-number: 'baangtSticker'
  quantity: 10
  schedule: [{
    date: '2020-03-20',
    quantity: 5},
    {
    date: '2020-05-01',
    quantity: 5}]
 },
 {line-item-number: 2,
  material-number: 'baangtCourse'
  quantity: 5
 }]
```

## Provide possibility to write in separate tab (and interpret Tab into JSON)
As the above mentioned way is definitely convenient to work with in Python, but is not at all user friendly, we should
provide a function to read structured data from another Excel-Tab.

If the column name of the current Excel-Column is identical to a tab-name in the same XLSX, read the tab and move all
data from there, that is identical with the test case number, into the cell in the test case data as JSON (see above).

## New command in testStepMaster.py

We'll need a new command ``repeat``. Value1 is the column/field-name in testDataDict. The implementation of this command
must loop over the json-array and process each test step until it reaches (the also new command) ``repeat-done``. It 
shall automatically create a variable ``_enum`` into each loop (also nested) to know the current position.

Nested ```repeat``` are possible as a JSON-String may include further lists of Dicts. For any command executed within 
the ``repeat`` the ``Value1`` would read: ``<column_name>.<dict_Key>`` and for a nested entry: ``<column_name>.<dict_key>.<dict_key>``.

## Export data 
* Export format in XLSX shall contain the nested data as tabs with reference to test case line.
* Export format in Database shall store the data in table ``<stage>_<object>`` (in above example e.g. ``test_schedule``)

### Example:
* REPEAT items
* SETTEXT <some_xpath_to_material_field$(items._enum)> $(items.materialnumber)
* SETTEXT <some_xpath_to_quantity_field$(items._enum)> $(items.quantity)
* REPEAT items.schedule
* SETTEXT <some_xpath_to_schedule_line$(items.schedule._enum)_date> $(items.schedule.date)
* SETTEXT <some_xpath_to_schedule_line$(items.schedule._enum)_quantity> $(items.schedule.quantity)

# DoD (including effort estimation (18 hours))

* Implementation of JSON-Loops in TestStepMaster done and tested (2 hours)
* Implementation of commands ```repeat``` and ``repeat-done`` incl. ``_enum`` (2 hours)
* Implementation of Excel-Import from tabs into JSON-Field done and tested (2 hours)
* Implementation of Excel-Export and database inserts for nested data (3 hours)
* One working example file in /examples using 2 levels of nested data without other tabs (2 hours)
* One working example file in /examples using 2 levels of nested data from other tabs (2 hours)
* Updated documentation in /docs-Folder (1 hour)
* Unit-Test coverage (in folder /tests) of 80% (for all committed/changed methods) (4 hours)
* no critical linter errors or warnings (PEP-8 conformity of the code) (no additional effort)
