
pyinstaller --noconfirm windows/baangtWindows.spec

rem Remove Screenshots and Logs ^
rm -r dist/baangt/examples/Screenshots
rm -r dist/baangt/examples/Logs

rem Create ZIP-file
mkdir executables
rm executables/baangt_windows_executable.zip
powershell Compress-Archive dist/baangt/. executables/baangt_windows_executable.zip