============================
What is ``baangt``
============================

Testing software has always been a challenging field and it's not getting easier or simpler as overall complexity in corporate
and other applications skyrockets. Release cycles in larger corporations are often long because of inefficient regression
tests. Also costs of software updates, upgrades and forward development is heavily impacted by too little test coverage.

**To stop praying when you release to production you need to start serious testing!**

With ``baangt`` you've one *open source* solution for all your test stages and needs. Be it Frontend with Webbrowser, API,
graphQL, SOAP, oData or chromium related App-Tests. You'll use one toolset, one database per stage and one reporting to
see at any given moment, how your stages and applications are doing and if it's safe to release the current state of one
stage to the next.

    ``baangt`` is optimized to be super easy to start and flexible when your demand grows.

The fastest, simplest way to record test cases
----------------------------------------------

If your requirements are pretty basic you'd start using ``baangt`` with a simple Excel-Sheet as source of Testcase definition and
Testdata definition. This is super fast, very easy even for endusers but has limited flexibility, even though it comes packed
with all features of the higher end solutions like reporting, fault tolerance, screenshots in case of errors and much more.


Still simple and more powerful ways:
------------------------------------

As your requirements grow you'd have Testcase and testrun definition separately (e.g. you want to execute the same
test cases on different stages of your system landscape (Pre-Quality, Final-Quality, Dev) and not for every heartbeat test
you'd want to run through your 1000s of test data. Maybe you'll have a SQL-Query in your Excel based data, which changes
data records dynamically or per stage or per version, that you want to test for. Things are not so simple in this stage,
but still simple enough for technically versed business department to run high quality tests on all stages by themselves.
Even after the point, where you need technicians to integrate baangt with your CD/CI-Pipeline`s buildmanagement tools,
the maintenance of data and test sequence can be done without ANY other tools (except Excel or OpenOffice) easily by the
people who know best what to test: Your business department.

Hey, why not do everything in Excel?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is one serious drawback from this flexibilty: it's **change**. Of course you started with 1 sheet, but later had some additional
requirements and simply added a second sheet to cover those whithout changing the definitions of the first excel sheet.
You're still happy as you need both behaviours tested (imagine one test set for regional customers and another test set
for customers from other countries). Great. Everything works. After having some serious problems in production and fixing
those defects you decide to write a testcase to mimic a certain user behaviour (e.g. navigating back and forth multiple
times, deleting and re-adding objects from a shopping chart, etc.). The basic test sequence would be still the same as in
the other two cases, but for a specific card you'll need changes. Simple. You copy one of the original sheets and adjust
accordingly. You immediately sleep better because now also those cases are part of your growing regression test set. Wonderful.
You continue like this for 2 months, end up with 2 or 3 datafiles and 20 test case definitions. That's not uncommon. Also
not uncommon is "**Change**". For more direct communication with the endusers the AUT (Application under test) get's enriched
with a Sentry-Popup. Wonderful idea. But wait... It's not so great after all, because now you have to update 20 test case
definitions with a way to deal with the new popup. Imagine corporate environments where we have many 1.000 or many 10.000
tests.

Subclassing for multiply used functionality
-------------------------------------------

The existing classes ``baangt.TestCase.TestCaseMaster`` and ``baangt.TestStep.TestStepMaster`` can easily be subclassed
and enriched with static functionality - even when you use the Excel version of ``baangt.py``. Yes, you'll need to know
some basics of powerful Python Language and most probably an IDE.

An example could look as simple like this:

::

    from baangt.TestStep import TestStepMaster

    class myTestStep(TestStepMaster):
        def execute():
            self.driver.goToURL("http://www.google.com")
            self.driver.findByAndSetText(xpath='//input[@type="text"]', value='baangt')
            self.driver.findByAndClick(xpath='(//input[contains(@type,'submit')])[3]')

That's it. All the rest is taken care of by ``baangt``. You'll also receive a nice export file showing timing information
for your TestCase.

You can subclass any other functionality, that doesn't fully fit your needs (IBAN-Generation, Browser-Handling, Timing)
and also create your own Assertion-classes (for instance if you need to receive data from a Host-System or
RFC/SOAP-Connection or any other source that is not natively supported by ``baangt.py``). Of course you'd only
re-implement methods, that you need to enrich and consume everything else from the framework.

Please consider creating pull-requests if you think some of your custom implemented functionality could be useful for
others.


``BaangtDB`` for flexible, powerful enterprise grade test automation
--------------------------------------------------------------------

Enter the next stage: ``baangtDB``. ``baangtDB`` does much more than just replace Excel as input and sequence source. BaangtDB
provides modularization of your test cases. In the above example you'd maintain the Sentry-Popup exactly ONCE for all your
test cases, where it applies.

Also if you're in a really large corporate environment, you'll start facing problems with the XLS-Based solution as corporate
governance, compliance, regulations and so on will sooner or later make it difficult to use the software in this way. Also
even if you use ``git`` you experience problems with different versions of the Excel-Sheets - depending on your setup of course.

But still no need invest into expensive, licensed, closed source, proprietary solutions and depend on their good will.
Run ``baangtDB`` (for testdata and testcase sequences) in a docker container on premises or in Cloud and have the full flexibility plus
comfort for free.

To sum it up
------------

There are multiple ways to use the open source testing framework ``baangt``. Each with it's up- and downsides.

.. list-table:: Possibilities to use ``baangt``
   :widths: 100

   * - **XLSX-Simple format**
   * - to get you started the single Excel-Sheet holds test sequence and data. Fully functional, full reporting on test execution.
   * - **XLSX-full format**
   * - XLSX format: more comples test run, test sequence, test case, test steps as part of testcase definition file. Separate data file.
   * - **baangtDB**
   * - Complexity of XLSX-Format, but simpler maintenance in corporate environments. More and better ways to structure and reuse testcase sequences.
   * - **Cloud**
   * - Same as database
   * - **Hosted**
   * - Same as database
