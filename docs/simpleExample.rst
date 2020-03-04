Jump-start into worry free production deployments
=================================================

You can try baangt right away and see how it works. It'll take less than 5 minutes.

Prerequisits
^^^^^^^^^^^^^

* Firefox installed
* Python3 installed
* ``baangt`` installed (either via PIP or from the GIT-Repository at https://gogs.earthsquad.global/athos/baangt)

If you prefer running ``baangt`` inside Docker, use the Dockerfile from https://gogs.earthsquad.global/athos/baangt-Docker.
After downloading the repository, enter ``make build`` and then ``make run`` in the command line.
Once Docker is up, use SVN://localhost:5902 to connect. All features are exactly like you'd install everything on your local machine.

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

    If you want to be able to watch your browser executing each step, we recommend you set the parameter ``slowExecution`` with value ``True`` in Globals and re-run the test

.. hint ::
    If you want the browser window to stay open on errors and/or after execution, you can use parameter ``dontCloseBrowser`` with value ``True``
    in global settings and run the test again. The browser will stop on errors or when the test run execution stopped.

A bit further
-------------

Go ahead and try it out with your personal real-world example of a web-page, web-app or SPA, which you would like to have
reproducable regression tests for.

Of course you could basically follow the steps above, but depending on the length and complexity of the execution, you'll
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

     You might want to execute the test case from within Katalon Recorder to make sure everything was recorded properly.

* Hit the export-Button of the recorder, chose format ``other``
* Click "Export to Clipboard"
* Switch over to ``baangt`` and press the button "Import KatalonRecorder"
    * The contents from the clipboard should be imported already and translation to ``baangt`` should be completed. If the clipboard was not inserted automatically, click on the button "Import Clipboard" and please drop a ticket stating your operating system incl. version and which browser you used for recording in Katalon recorder.
* Press "Save" and choose where you want to store the resulting XLSX-File

**That's it. You just created you first regression test case including all parameters for it.**

If you're wondering which parameters these are, and how you can influence them, fear not! Open the Testcase-XLSX from
the last step above, click on the "data"-Tab and start to enter values and lines as you please.

You can always re-run Baangt after saving your Testrun-XLSX and see your progress.

.. hint::

    If you want to be able to watch your browser executing each step, set the parameter ``slowExecution`` with value ``True`` in Globals and re-run the test

Tweaking the result
^^^^^^^^^^^^^^^^^^^

You managed to have a working recording. Congratulations! Let's learn a bit more about the structure of the created XLSX

.. list-table:: Fields in Tab ``TestStepExecution``
   :widths: 25 75
   :header-rows: 1

   * - Column Name
     - Description
   * - ``Activtity``
     - Sets the activity of this TestStep. Activities are described in more details in next chapter
   * - ``LocatorType``
     - Most of the activities need a locator. We are big fans of XPATH as locatorType, due to speed and ease of use. Sooner
       or later you'll anyway end up needing XPATH, so why not use it always when there's no downside? If you prefer
       writing CSS-Paths then use value ``CSS`` for the locator. And if you are lucky enough to have unique IDs in your
       page simply use ``ID``.
   * - ``Locator``
     - The locator is the specification on which element ``Activity`` should happen. As in the value fields, you may
       use variable replacement here too, in order to replace Locators with values from the data file. For instance the
       following would work fine:
       ``//*[@id($(CUSTOMERNUMBER))]`` - this would create an XPATH-Statement where $(CUSTOMERNUMBER) is replaced by the
       actual value of the current test record.
   * - ``Value``
     - For instance activity ``SetText`` requires a value (The text to send to a Web-element). You may use fixed values
       (which will rarely happen) or values from your test data source, in the simple cases the sheet ``Data`` .
       The column names in the sheet ``data`` can be used as variable names (e.g. if you created a column "Quantity" in
       your data tab, you can use ``$(Quantity)`` in the field value.
   * - ``Comparison`` and ``Value2``
     - For some activities (e.g. IF) you not only need the Value-Field but also a comparison operator and a
       second field or value to compare to. Values for ``comparison`` are ``eq`` and ``=``. The field ``value2``
       follows the same logic as ``value``.
   * - ``Timeout``
     - Sometimes you might to overwrite the default timeout settings of ``baangt``. Here's your chance. Values in seconds,
       decimals are OK (``0.5`` is a valid value, so is ``90``).
   * - ``Optional``
     - Usually when ``baangt`` tries to execute an activity and can't (after timeout), it will throw an exception,
       report in the Logs and stop the current test case. If you set ``optional`` to ``True`` or ``X``, ``baangt``
       will continue execution of the test case, even if the activity wasn't possible.
   * - ``Release``
     - Often you'll face situations, where you want to run a test case in several stages (e.g. DEV, Pre-Quality, Quality,
       Migration, Pre-Production, etc.) and the software version on each stage is different. A test case, that works on
       Pre-Production will not pass on Dev-System as Dev is already further developed. If you change the test case to work
       on Dev-System and you need to test a Hotfix deployment on Pre-Production, what will you do? In other test solutions
       you would "simply" copy your test case, have one version for DEV, one for Pre-Production. Do that with hundreds of
       different test cases and watch yourself drown in chaos. OR you could use ``baangt`` where this problem is solved.
       Software moves through the stages of your system landscape as it evolves. Use this field to conditionally execute
       different "branches" of your test cases, depending on the version on the current stage. ``Release`` can be any
       string value. You can add "> " "< " and "= " as the first 2 characters to signal to ``baangt`` to only execute
       the step when current release is greater than, lower than or exactly equal to the value afterwards, for instance

       ::

         > 2019.05

       will run the line only, if the Version is ``2019.05a`` or ``2019.06``. We are aware, that your version numbers might
       follow different nomenclature, so we made it very easy to subclass the corresponding logic.

More details on Activities
--------------------------

       * GoToURL
       * click
       * setText
       * SetTextIF
       * clickIF
       * goBack
       * If
       * EndIf

.. list-table:: Details of activities
   :widths: 25 75
   :header-rows: 1

   * - Activity
     - Description
   * - GoToURL
     - Navigate to the given URL. Column ``Value`` must provide the URL. You might want to use variables in your URL-String,
       for instance your URL might look like this ``https://$(STAGE).earthsquad.global/``. It will be replaced
       during runtime of the test data with the value of ``STAGE`` from either Global settings or settings in the
       ``testCaseSequence``.
   * - click
     - Will click on the object specified by the ``locator``.
   * - clickIF
     - Will click on the object specified by the locator IF the field in testDataDict, that you enter in Column ``value``
       has a value. This small and simple extension can save you hours and hours of work in maintenance of testcases.
       Imagine you have 10 checkboxes, that in various combinations provide different test results, and you have to test
       all possible combinations. Using one column in your datafile for each checkbox and the ``clickif``, you can create
       your testCases in minutes instead of hours or days. Imagine 50 checkboxes - with ``baangt`` your effort is still
       just minutes.
   * - setText
     - Write the text given in column ``value`` to the element specified by ``locator``. Only rarely will you have fixed
       values. Usually you'll assign columns of the test data using variable replacement (e.g. ``$(POSTCODE)`` to set the
       text from column ``POSTCODE`` from the datafile into the destination element.
   * - setTextIF
     - Same as SetText, but will only do something in cases where there is a value in the datafile. Similarly to clickIF
       this little helper functionality can help you save hours and hours in creation and maintenance of rocksolid and
       bulletproof test cases.
   * - goBack
     - Trigger the "back"-Button of the browser.
   * - If/Endif
     - The block between IF and ENDIF is only executed when the condition evaluated by ``value|comparator|value2`` is
       true, for instance:

            $(POSTCODE) = 7040

            $(YEAR2DATE) > $(YEARTOMONTH)

       Another use of the If-Statement is with ``LocatorType`` and ``Locator`` and comparison. This can be used when you
       want conditional execution of a larger block of statements depending on an element present or not present.
