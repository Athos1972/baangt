
pyinstaller windows/baangtWindows.spec

rem              datas=[('../baangt/ressources/baangtLogo2020Small.png', 'ressources'),
rem                    ('..\examples\', 'examples'),
rem                    ('..\browsermob-proxy','browsermob-proxy\')],


rem --add-data "..\examples\;examples" --add-data "..\browsermob-proxy;browsermob-proxy\"

rem Remove Screenshots and Logs ^
rm -r windows/baangt/examples/Screenshots
rm -r windows/baangt/examples/Logs

rem Create ZIP-file
mkdir executables
rm executables/baangt_windows_executable.zip
rem powershell Compress-Archive windows/. executables/baangt_windows_executable.zip