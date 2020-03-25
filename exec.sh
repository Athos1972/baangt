#!/bin/sh

pyinstaller --clean --onedir --noconfirm \
	--distpath ubuntu/ \
	--workpath ubuntu/build \
	--specpath ubuntu \
	--name baangt \
	--add-data '../baangt/ressources/baangtLogo2020Small.png:ressources' \
	--add-data '../browserDrivers/geckodriver:geckodriver' \
	baangtExec.py