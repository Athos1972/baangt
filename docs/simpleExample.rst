Jump-start into worry free production deployments
=================================================

You can try baangt right away and see, how it works. It'll take less then 5 minutes.

Prerequisits
^^^^^^^^^^^^^

* Firefox installed
* Python3 installed
* ``baangt`` installed (either via PIP or from the GIT-Repository at https://gogs.earthsquad.global/athos/baangt)

If you prefer running ``baangt`` inside Docker use the Dockerfile from https://gogs.earthsquad.global/athos/baangt-Docker.
After downloading the repository enter ``make build`` and then ``make run`` in the command line. Once Docker is up, use SVN://localhost:5902 to connect. All features are exactly as you'd install everything on your local machine.

Let's dive right into it
^^^^^^^^^^^^^^^^^^^^^^^^^

* Start baangt interactive UI by typing `python baangtIA.py`
* In the dropdown "Testrun" chose "SimpleTheInternet.xlsx" and click on "Execute TestRun"
* What's happening here is pretty similar to a real world test case:
    * Browser (in this case Firefox) starts up
    * Navigate to a certain web page
    * click on a link
    * navigate back
    * click on other link
    * click on several elements of the page (e.g. buttons)
    * write a report with summary and details about the test case. You'll find the report in the root directory of baangt, unless you stated otherwise.


Extend the Script:
------------------

For this to work we recommend an XPATH or CSS-plugin for your browser.

Follow these steps to modify the behaviour of the test script:

* Open "SimpleTheInternet.xlsx" from the baangt root directory in Excel or OpenOffice
* In your browser with activated XPATH or CSS-Plugin head over to http://the-internet.com
* Choose one of the links, that you want to play around with and find the XPATH or CSS from your tool.
* Copy and paste this ID in the last line of the XLSX in column C ("Locator").
    * Column A ("Activity") should be "CLICK"
    * Column B ("LocatorType") will be either XPATH or CSS depending on your tool
* Save the XLSX
* Execute the testrun "SimpleTheInternet.xlsx" in ``baangt`` again.
* Sit back and enjoy your victory!

.. hint::

    If you want to be able to watch your browser executing each step we recommend you set the parameter ``slowExecution`` with value ``True`` in Globals and re-run the test

.. hint ::
    If you want the browser window to stay open on errors and/or after execution you can use parameter ``dontCloseBrowser`` with value ``True``
    in global settings and run the test again. The browser will stop on errors or when the test run execution stopped.

A bit further
-------------

Go ahead and try it out with your personal real-world example of a webpage, web-app or SPA, which you would like to have
reproducable regression tests for.

Of course you could basically follow the steps above, but depending on the length and complexity of the execution you'll
definitely enjoy having more tools in your toolbox:

Recording a test case with Katalon Recorder
-------------------------------------------

Katalon Recorder is a free browser Add-on for Chrome and Firefox. Installation is simple, just google
``Katalon plugin <your-browser>`` and install the plugin. After installation of the Katalon recorder follow these steps:

* Start the plugin
* Hit the "record"-Button
* Execute the activities you want it to record. Usually following these steps:
    * Open a Webpage
    * Login (optional)
    * Navigate to some sub-page
    * Click buttons
    * Enter values
    * Download documents (optional)

* Stop recording

  .. hint::

     You might want to execute the test case from within Katalon Recorder so make sure everything was recorded proplery.

* Hit the export-Button of the recorder, chose format "other"
* Click "Export to Clipboard"
* Switch over to ``baangt`` and press the button "Import KatalonRecorder"
    * The contents from the clipboard should be imported already and translation to ``baangt`` should be completed. If not click on the button "Import Clipboard" and please drop a ticket stating your Operating System incl. Version and which Browser you used for Recording.
* Press "Save" and choose where you want to store the resulting XLSX-File to

**That's it. You just created you first regression test case including all parameters for it.**

If you're wondering, which parameters these are and how you can influence them, fear not! Open the Testcase-XLSX from
the last step above, click on the "data"-Tab and start to enter values and lines as you please.

You can always re-run Baangt after saving your Testrun-XLSX and see your progress.

.. hint::

    If you want to be able to watch your browser executing each step we recommend you set the parameter ``slowExecution`` with value ``True`` in Globals and re-run the test

