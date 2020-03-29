#!/bin/sh

pyinstaller --clean --onedir \
	--distpath exec_mac/ \
	--workpath exec_mac/build \
	--specpath exec_mac \
	--name baangt \
	--add-data '../baangt/ressources/baangtLogo2020Small.png:ressources' \
	--add-data '../examples/:examples/.' \
	--add-data '../browsermob-proxy:browsermob-proxy/.' \
	--noconfirm \
	baangt.py

# Remove Screenshots and Logs
rm -r exec_mac/baangt/examples/Screenshots
rm -r exec_mac/baangt/examples/Logs

# Create ZIP-file
mkdir executables
rm executables/baangt_mac_executable.zip
zip -r -X executables/baangt_mac_executable.zip exec_mac/baangt/

# Remove Build-Folder
rm -r exec_mac