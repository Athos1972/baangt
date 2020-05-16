rm -R dist/baangt-*
rm -R dist/baangt
rm -R dist/baangtIA
rm -R dist/baangt.app
rm -R dist/baangtIA.app
python3 setup.py sdist bdist_wheel
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
rm -R build/
