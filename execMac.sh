#!/bin/sh

pyinstaller --clean --onedir \
	--distpath exec_mac/ \
	--workpath exec_mac/build \
	--specpath exec_mac \
	--name baangt \
	--add-data '../baangt/ressources/baangtLogo2020Small.png:ressources' \
	--add-data '../browserDrivers/geckodriver:.' \
	baangtExec.py