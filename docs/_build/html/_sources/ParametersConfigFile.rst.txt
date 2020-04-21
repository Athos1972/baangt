Parameters in Configuration files (``globals``)
===============================================

Generally it's not needed to change parameters in the config files during manual or automated execution, as the parameters
have default values or are anyway defined in the Testrun definition. Still sometimes it's very handy to change them on the fly,
for instance to slowly retest a single testrecord or to not close the browser after an error.

.. list-table:: Parameters in globals
   :widths: 25 75
   :header-rows: 1

   * - Parameter
     - Description
   * - ``Release``
     - As you move your maturing software through the system landscape, you might still need regression test results based
       on "old" release functionality, while on lower stages you might want to (regression)-test already newer versions
       or newer functionality. In ``baangt`` there is no need to copy test cases in those situations. You simply update
       your test case definition with the appropriate version number (e.g. >= 2020-10) and set the proper ``Release`` in
       the config file. For instance "2020-09" when you want to run on final quality and the changes from version "2020-10"
       are not there yet.

            Note for developers:

            It's a static method - if you need to apply different versioning schema for your system landscape,
            simply subclass TestStepMaster and overwrite only the method ``ifQualifyForExecution``.
   * - ``TC.slowExecution``
     - When set to ``true``, the browser will stop for a short time after each command, so that you can also visually see
       what the browser is doing
   * - ``dontCloseBrowser``
     - When the browser or script finds an error, it usually takes a screenshot and moves on to the next testcase.
       With this setting to ``True`` the browser session will stop right at the error.
   * - ``TC.BrowserAttributes``
     - Set the value to ``{'HEADLESS': 'True'}`` to run Chrome/Firefox in headless mode.
   * - ``TC.Lines``
     - Which lines from datafile to process.

       * ``linennumber`` e.g. ``5``. Will execute the selected testrun using line 5 from the datafile
       * ``linenumber_from - linenumber_to`` e.g. ``1530 - 1540``. Will execute the selected testrun with lines 1530
         until including line 1540

       Combinations are possible and allowed, in this case separate the numbers by comma e.g. ``5, 10-20, 30-90``
   * - ``TC.Browser``
     - If the testcase is WEB-Testing, then you can overwrite the browser, which is defined inside the testrun definition.
       If the testcase is not a Web-Testcase this setting doesn't have any effect.
       Valid values are ``Chrome``, ``FF`` and ``Safari``
   * - ``TC.ParallelRuns``
     - Number of parallel sessions to be executed. Values depend largely on your hardware and internet connection.
       Debugging works only in a single session.
   * - ``TC.NetworkInfo``
     - Creates a very detailed trace of network activity of the browser(s). In the output file you'll find another Tab
       "Network", that holds all API-Calls from the frontend (including header, payload and answer).
   * - ``TC.ExportAllFields``
     - When set to "True", instead of specifying certain fields from the input data, that will be exported to the result
       field, take ALL fields for export.
   * - ``TC.RestartBrowser``
     - When set to "True", will always start a new browser after the previous test case was done.
   * - ``TC.UseRotatingProxies``
     - When set to "True", will not use your own IP-Address but will use random rotating proxy servers from a list of proxies.
   * - ``TC.ReReadProxies``
     - When set to "True", the proxy-servers will be re-evaluated. Otherwise existing list of Proxy-Servers will be used
       for proxy rotation. List must be named ``proxies.json`` and contain a list of proxies.
       Each entry in the json file must contain ``ip`` and ``port``.

