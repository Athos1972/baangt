Future Features
===============
We implement all features for 3 operating Systems (Mac, Windows, Debian Linux and Ubuntu on Docker).

Short/Medium term features
---------------------------
* Refactoring of parallel processing on a single computer (2020.03) --> Done
* Executables on Mac, Linux and Windows (2020.03) --> Done
* Nicer interactive UI-Starter (2020.03)
    * Phase 1 done 2020.02
    * Phase 2 (UI-elements) (2020.03) --> will move to 2020.04 RC5
    * Provide live statistics (2020.04)
* Double Opt-In Automation (2020.03) --> will move to 2020.04 RC6
* Support for Selenium Grid V4 (2020.04)
* Better support for multiple sources (e.g. multiple XLSX) of test data (2020.04)
* Better support to store test data output to database and export files (2020.04)
* Support for Appium integration (2020.04)
* Katalon Importer/Converter as Webservice (2020.04)

Features for later
------------------
* Proof of concept with PyWinAuto
* Integration with SAP Gui Scripting via VBS and PyWinAuto
* Better support for Mass testing APIs
* Integration with Atlassian Confluence (for Testcase and Testrun definitions)
* Integration with Atlassian Confluence (to publish results of testruns)
* Integration with MS Teams to publish results of Testruns
* Integration with Telegram to publish results of Testruns
* Grafana Board for baangtDB
* Better support for oData V4.0 (similar to SOAP)
* Support for GraphQL via Graphene

PRO-Features
------------
There's no time plan yet, when a pro version will be released. So far whatever we do goes into the open source version.
Future features might include:

* DB-Migration tools (to ease the pain of upgrading databases)
* Multi-User environment (who did when which activity and who changed when which test object)
* History of Testcases (what was changed when. If urgently needed we could come up with DB-Dump and GIT diff or so.)
* Test-Canons (deliberately stop test cases multiple times at certain test steps, wait for trigger, then resume. After first Testcase *finished* his first waiting period, start second round of Testcases (that's how the name "Canon" came up). So far implemented in customer project, but needs to be polished up for public version)
* XML/PDF-Compare
* Consulting
* Priority support

