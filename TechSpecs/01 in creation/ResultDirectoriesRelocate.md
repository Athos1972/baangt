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

# DoD
* Script for creation of Windows Executable updated to create folders also in Users Home-Directory
* Script for creation of Windows Executable updated to change log folder for browsermob-proxy
* All file system access on Mac, Ubuntu and Windows work like now when installed from GIT-Repository or unzipped ZIP-File
* All file system access on Windows work in Users-Directory if installed via the installer.

 