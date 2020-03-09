Change log
==========

2020.03
^^^^^^^
Summary: Release Candiate 1 is on the road!

New features
++++++++++++
* Network logging during WEB-Sessions and export to Excel-Result in separate tab. Use ``TC.NetworkInfo`` with value ``True`` (Windows version works, MAC not yet)
* baangtDB: Import and Export functionality for simpleFormat and complex XLSX-Testrun definitions.
* baangtDB: cascaded delete: Delete a test run and all it's objects (unless used in other test runs)
* baangtDB: Update testrun from XLSX (closed circuit between IT-Department and business department)


Bugfixes
++++++++
* Reporting: Duration sometimes off by Timezone shift hours
* Minor fixes for increased stability with Chrome-based browsers

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