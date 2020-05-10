rm -r dist
rm -r build
rm -r executables

pyinstaller --noconfirm --path venv/Lib/site-packages windows/baangtWindows.spec

rem Remove Screenshots and Logs ^
rm -r dist/baangt/examples/Screenshots
rm -r dist/baangt/examples/Logs
rm -r dist/baangt/examples/1testoutput
rm -r dist/baangt/Logs


rem Create ZIP-file
mkdir executables
rm executables/baangt_windows_executable.zip
powershell Compress-Archive dist/baangt/. executables/baangt_windows_executable.zip
