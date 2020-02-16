Change log
==========

2020.02
^^^^^^^
* Pypi-Version 2020.02.* deployed
* First version of baangtDB with Flask (including Docker Container). No DOCS yet, as it's still under heavy development.
* Support of Edge on Microsoft Platform and Safari on Apple/Mac
* Completed support for Versions in SimpleFormat and SimpleAPIFormat (can also be used for ``baangtDB``, subclassed methods and complex Excel TestRun Defintions)
* Improved support for API-Calls and data extraction from API response to result sheet
* Added logical comparison for IF-conditions, whether a field exists or not (using LocatorType and Locator). You can see an example in file ``BaangtDBFill.xlsx``


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