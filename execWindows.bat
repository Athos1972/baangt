
pyinstaller --clean --onedir --noconfirm ^
	--distpath windows/ ^
	--workpath windows/build ^
	--specpath windows ^
	--name baangt ^
	--add-data "../baangt/ressources/baangtLogo2020Small.png;ressources" ^
	--add-data '../examples/:examples/.' \
	--add-data '../browsermob-proxy:browsermob-proxy/.' \
	--noconfirm \
	baangt.py

rem Remove Screenshots and Logs
rm -r exec_mac/baangt/examples/Screenshots
rm -r exec_mac/baangt/examples/Logs

rem Create ZIP-file
mkdir executables
rm executables/baangt_windows_executable.zip
powershell Compress-Archive windows/. executables/baangt_windows_executable.zip