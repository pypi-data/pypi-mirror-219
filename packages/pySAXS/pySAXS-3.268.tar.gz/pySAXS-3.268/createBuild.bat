python createChanges.py
cd build
del /q *.*
cd..
cd dist
del /q *.*
cd..
rem python setup.py bdist --format=wininst
python setup.py bdist_wheel --universal
rem distribution tar
python setup.py  bdist --format=gztar
rem twine upload dist/*
