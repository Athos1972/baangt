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

Plugins
-------

Please make yourself familiar with https://pluggy.readthedocs.io/en/latest/ in order to implement Plugins. If you're stuck let me know.