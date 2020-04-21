# Situation

So far we're using os.getcwd() to get the current working directory. Everything works fine on direct download of the
repository or unzipped Zip-Files from https://github.com/athos1972/baangt-executables.

Even the Windows-installer works fine, but when the installed EXE is started, it needs Admin-Rights, because we're 
accessing the c:\Programs - folder. 

# Aim

If installed on Windows, behave like a normal Windows-Application. Save data in \User\baangt-Folder and use C:\Programme 
only for the sources.

# Implementation

Unfortunately there are many places in the code, where we access directories. Some of them already have parameters, 
which are derived during runtime (but so far wrongly derived).

Some logs (Browsermob-Proxy) need updates in configuration files

For Firefox, Chromedriver and Edge/Chromium the log-directory needs to be set in the code (currently not done, which
makes them also log into os.getcwd(). )

After this TechSpec was implemented, all accces to the file system should be opinionated according to the OS
and installer-option (pyInstaller (executable) vs. python script execution ``python3 baangtIA.py``).

## Separate class

It would be a good thing to have all writing file system accesses in one class and have a method for each
OS. Inside the class we could determine, on which OS we are and whether or not we're in pyInstaller-mode
or as executable in Windows.

Methods could be: 
* getScreenshotPath
* getLogPath
* getOutputDirectoryPath
* getDatabasePath
* getIniPath
etc.

This class must also respect paths, that are given by the user (like e.g. GC.PATH_SCREENSHOTS, 
GC.PATH_EXPORT) and only make assumptions when these paths are not defined by the user.

## How to find places to replace code
os.getcwd() and pathlib are used throughout the code base to determine paths. Start there and look, what happens with
the results. If write-access happens, encapsulate in the above mentioned class.

# DoD
* Script for creation of Windows Executable updated to create folders also in Users Home-Directory
* Script for creation of Windows Executable updated to change log folder for browsermob-proxy
* All file system access on Mac, Ubuntu and Windows work like now when installed from GIT-Repository or unzipped ZIP-File
* All file system access on Windows work in Users-Directory if installed via the installer.

 