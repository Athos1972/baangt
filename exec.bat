
pyinstaller --clean --onedir --noconfirm ^
	--distpath windows/ ^
	--workpath windows/build ^
	--specpath windows ^
	--name baangt ^
	--add-data "../baangt/ressources/baangtLogo2020Small.png;ressources" ^
	--add-data "../browserDrivers/geckodriver.exe;." ^
	baangtExec.py