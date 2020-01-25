Parameters in Configuration files (``globals``)
===============================================

Generally it's not needed to change parameters in the config files during manual or automated execution as the parameters
have default values or are anyway defined in the Testrun definition. Still sometimes it's very handy to change them on the fly,
for instance to slowly retest a single testrecord or to not close the browser after an error.

.. list-table:: Parameters in globals
   :widths: 25 75
   :header-rows: 1

   * - Parameter
     - Description
   * - ``TC.slowExecution``
     - When set to ``true`` the browser will stop for a short time after each command, so that you can also visually see what the browser is doing
   * - ``dontCloseBrowser``
     - When the browser or script finds an error usually it takes a screenshot and moves on to the next testcase. With this setting to ``True`` the Browsersession will stop right at the error
   * - ``TC.Lines``
     - Which lines from datafile to process.

       * ``linennumber`` e.g. ``5``. Will execute the selected testrun using line 5 from the datafile
       * ``linenumber_from - linenumber_to`` e.g. ``1530 - 1540``. Will execute the selected testrun with lines 1530 until including line 1540

       Combinations are possible and allowed, in this case separate the numbers by comma e.g. ``5, 10-20, 30-90``
   * - ``TC.Browser``
     - If the testcase is WEB-Testing, then you can overwrite the browser, which is defined inside the testrun definition. If the testcase is not a Web-Testcase this setting doesn't have any effect. Valid values are ``Chrome``, ``FF`` and ``Safari``
   * - ``TC.ParallelRuns``
     - Number of parallel sessions to be executing. Values depend largely on your hardware and internet connection. Debugging works only in a single session.

# Todo:
BrowserAttributes
