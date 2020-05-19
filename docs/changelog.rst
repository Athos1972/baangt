Change log
==========

2020.05
^^^^^^^

Summary:
++++++++

While baangtDB is making great progress, we're in the final touches to release Version 1.0 of baangt base.

New features:
+++++++++++++

* Added more parameters for testruns in the new UI (e.g. BrowserZoomFactor)
* test data generator for complex random and/or multiplying test conditions created
* All test data from all test runs is now logged in a database. Additionally to results per test run you can compare
  results over time. Especially usefull when you have the local proxy server activated!

Bugfixes:
+++++++++


2020.04
^^^^^^^

Summary:
++++++++

A huge step closer to release 1. Some minor functionalities still need fixing. May May be the release month!

New features
++++++++++++

* Brandnew UI! The pySimpleGui was great during the beginning of the project. As we mature, we switched to QT5, which
  looks really great.

    * No need to remember technical field names! Yeah!
    * All settings to customize a test run execution are now nicely arranged in the details screen
    * Katalon-Importer added a few usability changes (e.g. when you save, you'll see this TestRun selected as default).
    * Browsers, Selenium Grid, etc. can be selected via Dropdown-Menu
    * Common BrowserAttributes (e.g. Headless) can be selected via Droddown-Menu
* SimpleFormat: New command ``iban`` will create a random IBAN. Powered by Schwifty library.
* SimpleFormat: New command ``pdfcompare`` compares a downloaded PDF-File with a reference PDF-File and
  reports differences. Works also well with parallel sessions.
* All: Variable replacement using Faker module. For instance ``$(FAKER.email)`` will generate a random E-Mail address
* All: New flag to export all fields of TestDataDict to result file: ``TC.ExportAllFields`` = ``True``
* All: Web-Testcases: Screenshots automatically embedded to result file, not only as a link. Makes it easier to share results
  on a communication channel.
* All: Support of Proxies and rotating Proxies (``TC.UseRotatingProxies`` and ``TC.ReReadProxies``)
* All: Support of restarting browser-sessions after each TestCase execution (``TC.RestartBrowser`` = ``True``)
* All: CL.* in Globals-File to overwrite standard classes (e.g. BrowserDriver) to custom classes.
* Appium integration for Android and iOS App tests using Appium Webdriver (see in /examples/App* and globalsApp.json)
* Subclassing: New commands to identify stale objects on page (HTML-Reload and SPA-Support)
* Additional way to export data to Excel-Result (can be used for results of scraping) GC.EXPORT_ADDITIONAL_DATA in
  TestRun.additionalExportTabs. For each Tab you want created set up one dict with {<tabname>:<ExportDictContent>}.
  Headers = Fieldnames.
* New flag to export all fields of TestDataDict to result file: ``TC.ExportAllFields`` = ``True``
* Web-Testcases: Screenshots automatically embedded to result file, not only as a link. Makes it easier to share results
  on a communication channel.
* Windows Installer: baangt now works without admin rights on Windows10
* Support of Proxies and rotating Proxies (``TC.UseRotatingProxies`` and ``TC.ReReadProxies``)
* Support of restarting browser-sessions after each TestCase execution (``TC.RestartBrowser`` = ``True``)
* Subclassing: Additional way to export data to Excel-Result (can be used for results of scraping) GC.EXPORT_ADDITIONAL_DATA in
  TestRun.additionalExportTabs create one dict with <tabname>:<ExportDictContent>. Headers = Fieldnames.


Changes
+++++++

* Improved browserDriver Download for executables (didn't work in some cases)
* Improved database logging of testrun results
* Dramatically improved speed for reading larger Input files (got rid of Pandas for XLSX-Import)
* Improved ease of subclassing for TestStepMaster.
* Improved reaction to common errors on Webpages (Stale element, not accessable, etc.)
* Improved handling of closed windows and tabs (when e.g. PDF-Download was activated)
* Support to supply webelement in driver.javaScript() as ``*args``
* Added many unit tests, but still not full coverage

2020.03
^^^^^^^

Summary: Release Candiate 3 is on the road!

New features
++++++++++++

* Executable files and ZIP-Archives for Mac, Windows and Ubuntu - no more GIT CLONE needed! Simply download, unzip and run.
* Network logging during WEB-Sessions and export to Excel-Result in separate tab. Use ``TC.NetworkInfo`` with value ``True`` (tested on Mac and Windows, most probably works on Linux too).
* baangtDB: Import and Export functionality for simpleFormat and complex XLSX-Testrun definitions.
* baangtDB: Export also to JSON-Format
* baangtDB: cascaded delete: Delete a test run and all it's objects (unless used in other test runs)
* baangtDB: Update testrun from XLSX (closed circuit between IT-Department and business department)
* Docs updated with latest parameters
* SimpleFormat: ``pause`` command added
* SimpleFormat: ``address_creation`` command added to create a random address. Customizable.
  Multiple calls will create multiple random addresses.
* CLI: New parameter ``--reloadDrivers=True`` downloads latest version of webdrivers for Chrome and Firefox.
* Integration with Selenium Grid V4.0 and baangt. See docs for further details. Separate Repository for the Dockerfile

Bugfixes
++++++++

* Reporting: Duration sometimes off by Timezone shift hours
* Minor fixes for increased stability with Chrome-based browsers
* Parallel executions on Windows work now, rewrote parallelism (local, without Selenium/Zalenium) completely to run with
  less resources. 10 parallel Firefox sessions on a single MacBook with 16 GB RAM works.

2020.02
^^^^^^^

Summary: Web- and API-Tests XLSX-SimpleFormat are almost completed. Shouldn't take much longer to have a production ready version.

* Pypi-Version 2020.02.* deployed
* First version of baangtDB with Flask (including Docker Container). No DOCS yet, as it's still under heavy development. For an early preview you can navigate to ``/flask`` directory and execute ``./start_docker.sh``
* Support of Edge on Microsoft Platform and Safari on Apple/Mac
* Completed support for Versions in SimpleFormat and SimpleAPIFormat (can also be used for ``baangtDB``, subclassed methods and complex Excel TestRun Defintions)
* SimpleFormat now with default ``locatorType`` = ``xpath``. No breaking change. Just a tiny little convenience when filling in long Excel Testcase definitions.
* Katalon Importer now creates proper data fields in data tab for simple format XLSX and refers proper variable (column) names in Teststep-Definition
* Improved support for API-Calls and data extraction from API response to result sheet
* Added logical comparison for IF-conditions, whether a field exists or not (using LocatorType and Locator). You can see an example in file ``BaangtDBFill.xlsx``
* Plugin structure for TestRun, ExportResults and BrowserHandling implemented. Example in separate repository https://gogs.earthsquad.global/athos/baangt-Plugin. If you subclassed those classes, you need to adjust the import statements (e.g. ``from baangt.base.TestRun`` to ``baangt.base.TestRun.TestRun``)
* Apart from exporting to XLSX it's now also possible to export testrun results to CSV. In simpleFormat you can set parameter ``TC.Export Format`` to the value ``CSV``. In baangtDB and full Excel format you can use Testrun property ``Export format``

2020.01
^^^^^^^

Very first public beta version. Not at all ready for production.

* First version on Pypi (https://pypi.org/project/baangt/), Docker (https://gogs.earthsquad.global/athos/baangt-Docker) and GIT Repository (https://gogs.earthsquad.global/athos/baangt)
* Support for SimpleExcel and Excel format including some examples
* Basic UI (interactive mode) and CLI (Command Line Interface with 2 parameters)
* Methods for Web testing implemented:
    * SetText(If)
    * Click(If)
    * GotoUrl
    * HandleIframe and Windows (Tabs)
    * If/Endif
    * GoBack
    * simple comparisons (=, >, <)
* Full support for Excel Data files
* Experimental support for Katalon Recorder Import to SimpleExcel format
* Very basic support to Export from Katalon Studio Projects (as subclassed modules)
* Logs
* Export result of TestRun to XLS including statistics, Timing information and analysis
* Docs created, styled, revisited and stored on https://baangt.jointhedocs.io
* Runlog: Additionally to saving execution information in a single Excel sheet for each testrun, also store information in a database for simple comparison of testruns between stages, days, endpoints or whatever else you want to compare. In this version only data storage was implemented. No reporting yet.