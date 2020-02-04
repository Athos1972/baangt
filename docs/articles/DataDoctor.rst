Beware of data generators
=========================

In time of big data and machine learning when we see the difficulties to find proper data for test automation we're tempted
to turn to the silver bullet "RPA" (Robotic Process Automation). Solutions grow like mushrooms, all with the intention to
reduce effort for test data creation and test case maintenance.

We also use test data generators in ``baangt``, very well dosed, very carefully and **never** to assess, whether the AUT
(Application Under Test) is suitable for production. We use test data generators based on users data recordings to harden
the application in early stages. We'll "play" around (automatically), perform random clicks in random orders on buttons,
extend each field to it's maximum length, fill traditional chinese characters into arabic text fields and similar tests.

That's a valuable excercise. It helps to harden the application before the masses of end-users will try
to beat it down. But we use those tests not in daily or weekly regression tests or when we assess the latest build or
increment.

What do we use **instead** of random generated data?
----------------------------------------------------

Beautifully, precious, manually designed and recorded test data from the business department (preferably key-users or even
power end-users). We extend the dataset whenever a new issue arises in the production if in the post-mortem phase of
the issue it turns out, that regression testing could have identified the issue with proper data.

As this test set grows in lines, it grows in value. After a few weeks you've covered tests for all your major business logic
within the test set. Depending on your product cycles it might mean a hell of maintenance effort (e.g. if your pricing changes
every hour or day, you'll either subclass the assertion methods with your own logic or you'll be miserable updating 1000s
of comparison values in the test data), but this effort might very well lead to keeping customers (as opposed to losing them
to competition, if your software is unstable), supporting your whole organization to deliver the highest possible performance
(by having reliable software and processes in place).

That's all nice, but it won't work for us because ...
-----------------------------------------------------

The more you depend on software and the more complex your software and processes are, the less I believe, that it is
not possible in your case to run your regression tests with meaningful and reliable test data. Here's a list of rather
lame excuses. If you use any of them, please think again.


.. list-table:: Anti-reasons for bad test data
   :widths: 10 40 50
   :header-rows: 1

   * - Excuse
     - Rant
     - Grip
   * - ``too complex``
     - The software and processes are too complex. We've trillions of combinations. It would take months to test all that
       and in the end we anyway wouldn't know, whether the results are right or wrong.
     - System landscapes - especially grown ones - can be really complex. But at least try to find a good starting point
       by combining a few, beautifully crafted test cases and validation rules with ML Data expanders. It's better than
       nothing and as your system stability improves and you need less time to fight fires in production, you'll gain time
       to invest in improving your test data. You can start an uplifting spiral!
   * - ``no real data``
     - We don't have good quality data in our stages.
     - Often you'll need basic or master data before you can test variations of transactional data. In a production company
       you'll need material master data of raw materials, customer master data, vendor master data and much more before
       you can test your shiny new plant optimization system. But there are more benefits in investing time to create all those
       prerequisit master data automated.

       * You can use this high quality data also for many other processes (billing, dunning, campaigning, MRP)
       * After the next system copy, the same quality data is just one click away
       * You can produce the same quality data for test clients, migration machines or wherever else you need them

       If the mountain of work is too big to tackle it all at once, slice it down to reasonable chunks. Identify, which
       data set has the highest value in terms of data quality/reliability of test case output and start with these.
       A classical example are customer master data. All your test cases are with "John Doe". First real customer record
       without a ZIP-Code or strange address format for a certain country, phone number format, etc. breaks your tests.
       Don't be like that. Or at least don't be surprised, if it happens to you. Having a few hundred different customer
       master records, that you use in your test data base and recreate every now and then doesn't take much of your time
       but provides a great deal of increased reliability of your test activities.
   * - ``changes too fast``
     - Our internal and external customers are in need for speed. We can hardly finish the features we need to provide on time,
       let alone test them in E2E-Scenarios. No need for additional overhead. Our developers know, what they do!
     - Good example of "famous last words"? Regression tests don't need to run forever. Usually one would have approx.
       10-15% in pure (and slow) UI-Tests, 40% of (faster) API-Tests and rely for the rest on earlier test stages (like unit tests).
       The less tests you execute, the higher the need for spotless and realistic test data! Yes, of course you can (and should)
       combine various test parameters into one E2E-Testcase (e.g. a specific/problematic country code with uncommon
       payment terms and a reopened order (instead of a freshly created one)). Better define a reasonable time frame for
       regression tests (given the fact, that they should run automatically, maybe a nightly build gives you 2-3 hours?).
       Then see, which systems take how long for each test case combination. Based on the time frame, the approximate number
       of testcases and the throughput you'll understand, if and how much you need to run in parallel. With ``baangt`` you've
       the ability to run multiple TestCases in parallel and still receive exactly one result set.
   * - ``Maintenance efforts too high``
     - Our changes are frequent and fast. We tried to use test automation, but we ended up spending more time with the automation
       then in development and in the end the reliability of the results was not worth the effort we invested.
     - Understood. It is in fact true, that UI-Tests tend to need higher maintenance efforts than API-Tests. In ``baangt``
       we addressed the problem of maintaining test case version with a simple and pretty versataile solution. If you need a
       test case to run on different software versions, which behave differently, you can simply adjust the "Release"-field
       in each Teststep (those, which are new from a certain release and those which are obsolete from a certain release, all
       others remain unchanged). Instead of having to have many different versions of testcases in parallel (and potentially
       the need to maintain all of them!) with ``baangt`` you'd have only one - unless you completely replace something
       (e.g. you replace credit card payment screen **completely** with payment by PayPal - then you'd most probably create
       a new testcase called "PayPal").
   * - 'Difficult to obtain data'
     - We need real data, but it's hard to come by. We've validation on Phone-Numbers, IBAN, BIC and many other fields,
       so we need to enter real data in test cases. But we don't have it and we don't want to use data from production!
     - At least you're not using your customers data for test - that's great! Indeed for some data it's pretty difficult
       to obtain valid test data - most of the time based on the reasoning, that if the mechanism to create valid data
       was made public it would support criminal activities.

       If you encounter such a need you're in bad luck and your rant is granted. I assume, that your developer and API-Tests
       mock this interface/data anyway, so you did the maximum possible.

       In other cases you can use existing functionality and libraries (e.g. ``baangt`` support valid IBAN/BIC creation
       dynamically out-of-the-box) to create valid test data and find errors long before your customers do. If you come
       across the need for data, that is difficult to obtain (but legal!), contact us with a feature request on the public
       issue tracker. Maybe somebody will pick it up and provide a solution in ``baangt`` base functionality.


tl;dr
-----

Build realistic synthetic data for your regression tests and take good care of it. Also, for every bug found in production
enhance your test set!