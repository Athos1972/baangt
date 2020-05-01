#!/bin/sh

rm -r dist
rm -r build

pyinstaller --clean --onedir \
	--distpath exec_mac/ \
	--workpath exec_mac/build \
	--specpath exec_mac \
	--windowed \
	--name baangt \
	--add-data '../baangt/ressources/baangtLogo2020Small.png:ressources' \
	--add-data '../examples/:examples/.' \
	--add-data '../browsermob-proxy:browsermob-proxy/.' \
	--noconfirm \
	baangtIA.py

# Remove Screenshots and Logs
rm -r exec_mac/baangt/examples/Screenshots
rm -r exec_mac/baangt/examples/Logs
rm -r exec_mac/baangt/examples/1testoutput

# Create ZIP-file
mkdir executables
rm executables/baangt_mac_executable.zip
zip -r -X executables/baangt_mac_executable.zip exec_mac/baangt/

# Remove Build-Folder
rm -r exec_mac
