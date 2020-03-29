#!/bin/sh

pyinstaller --clean --onedir --noconfirm \
	--distpath ubuntu/ \
	--workpath ubuntu/build \
	--specpath ubuntu \
	--name baangt \
	--add-data '../baangt/ressources/baangtLogo2020Small.png:ressources' \
	--add-data '../examples/:examples/.' \
	--add-data '../browsermob-proxy:browsermob-proxy/.' \
	--noconfirm \
	baangt.py

# Remove Screenshots and Logs
rm -r ubuntu/baangt/examples/Screenshots
rm -r ubuntu/baangt/examples/Logs

# Create ZIP-file
mkdir executables
rm executables/baangt_ubuntu_executable.tar.gz
tar -zcvf executables/baangt_ubuntu_executable.tar.gz ubuntu/baangt/

# Remove build folder
rm -r ubuntu