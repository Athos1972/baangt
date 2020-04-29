Developer guidelines for custom enhancements
============================================

``baangt`` is already pretty versatile but from time to time you'll face a requirement, that simply can't be done without
writing code. But that's not a bad thing - we like writing code after all, don't we?

Subclassing
---------------------

The main classes and functions should be more than OK for you. You'll just need to implement some central enhancements.
For instance there's a requirement to check after each Browser-Interaction, whether a specific popup/message appeared.
Don't be cruel and let the end-users duplicate the locator over and over again in their XLSX.

Instead create a subclass of BrowserDriver

::

    from baangt.base.BrowserDriver import BrowserHandling

    class MyCustomBrowser(BrowserHandling)
        def findByAndClick(...)

            # Search for the element
            self.customSearchAndReact()

        def customSearchAndReact():
            if self.findBy(xpath, "specialThingForThisClient"):
                self.testdataDict[GC.TESTCASESTATUS] = GC.TESTCASESTATUS_FAILED

That's it. Business people will love you and whenever "specialThingForThisClient" changes, you'll have to adjust only
in one place.

After subclassing you'll need to replace the standard ``BrowserHandling`` with ``MyCustomBrowser`` in order for baangt
to use it.

Debugging
---------

Yeah, sometimes the logs alone are not enough, even when you set loglevel to ``debug``. In such cases you'll want to set
breakpoints and expect the program to halt on the breakpoint. You've two chances to achieve that:

* Start baangtIA.py from CLI using:
    ``python3 baangtIA.py --run=<PathAndFileOfTestrunName> --globals=<PathAndFileNameForGlobals>``
* Use ``TX.DEBUG`` as flag in ``baangt`` interactive starter (=the UI, that comes when you start CLI without parameter
  ``--run``) with value ``True``

Plugins
-------

Please make yourself familiar with https://pluggy.readthedocs.io/en/latest/ in order to implement Plugins.
If you're stuck let me know.

Network trace
-------------

Sometimes it's useful (especially for frontend debugging and in performance measurments) to have more detailed log about
the calls that the browser exchanges with the backend. If you need this, use ``TC.NetworkInfo`` with value = ``True``.
In the output file you'll see a new tab "Network" that shows all calls, headers, payload and timing information for each
call.

Use with care, as the file can get pretty big.

Building baangt sources
-----------------------
Core project members can build distribution as follows:

Building pyPi
^^^^^^^^^^^^^

* Increase version in ``setup.py``
* ``MakePackage.sh`` to upload to PyPi
* Use latest version in depending project's ``requirements.txt`` (Custom projects)
* ``pip install -r requirements.txt``

Building Executables
^^^^^^^^^^^^^^^^^^^^

* Checkout ``https://github.com/Athos1972/baangt-executables``
* On a Windows computer: ``execWindow.bat``
* Move ``/executables/baangt_windows_executable.zip`` to checked out ``baangt-executables`` ideally with this line:

    ``mv executables/baangt_mac_executable.zip ../baangt-executables``
* Repeat accordingly on Mac (``execMac.sh``)
* Repeat accordingly on Ubuntu (``execUbuntu.sh``)
* ``git add .`` in the folder ``baangt-executables``
* ``git commit -m <version>``
* ``git push``

Windows bundle executables:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Install innosetup-qsp (QuickStartPack) Version 6 from https://jrsoftware.org/isdl.php
* Open Inno Setup
* Use Script ``/windows/baangtSetupWindows.iss``

If the Script doesn't work, it's mostly due to outdated dependencies. In this case it seems to be fastest to re-create
the script from scratch:
* Create new Script in Inno Setup with Wizard
* Fill in mandatory Info (Version, ProgramName, etc.) in first screen
* Find exe in Path baangt/dist/baangt/baangt.exe
* Click "Add files" and select all files in the same folder (/baangt/dist/baangt)
* Click "Add Folder" for each folder in /baangt/dist/baangt
    * When asked, whether sub-folders should be included click on "Yes"
* Save the Script in ``/windows/baangtSetupWindows.iss``
* Execute Inno Setup as described above
