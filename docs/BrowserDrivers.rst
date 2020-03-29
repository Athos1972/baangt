Handling of Browser Drivers
===========================

When you install ``baangt`` the latest version of Chromedriver and Geckodriver (for Firefox) are included. Depending on your
situation you might need different drivers.

New release of browser drivers
------------------------------

As you work with ``baangt`` for a longer time your browsers might be updated. If you receive an error telling about wrong
version of browser driver, you can simply delete the existing driver in ``baangt/BrowserDrivers/`` and on the next start
``baangt`` will automatically download the latest version.

Alternative version:
^^^^^^^^^^^^^^^^^^^^

If you start baangt with the following syntax from the command line, it will download the latest drivers (Chrome and
Firefox) automatically:

```python3 baangt.py --reloadDrivers=True```

It will overwrite existing versions.

Older releases of browser drivers
---------------------------------

Please download the release that you need from chrome and/or Firefox and replace the existing files in ``baangt/BrowserDrivers/``
which the freshly downloaded, older version. After the next start it should work fine.
