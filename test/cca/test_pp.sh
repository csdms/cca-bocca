#!/bin/sh
proj=pp
top=`pwd`
/bin/rm -rf $proj
$1 create project $proj
if ! test "$?" = "0"; then
	echo "FAIL: $proj create"
	exit 1
fi
cd $proj
mkdir itest
# make the c++ version
$1 config project --set-var=Project:exclude_from_import --value=None
./configure --prefix=$top/$proj/itest
if ! test "$?" = "0"; then
	echo "FAIL: $proj config"
	exit 1
fi
$1 create component \
--provides=gov.cca.ports.GoPort:go \
--import-sidl=$proj.testX:../$proj.src/${proj}.testX.sidl \
--implements=gov.cca.ports.ParameterGetListener \
--implements=gov.cca.ports.ParameterSetListener \
--import-impl=pp.testX:$top/$proj.src \
testX
if ! test "$?" = "0"; then
	echo "FAIL: $proj create testX"
	exit 1
fi
make
if ! test "$?" = "0"; then
	echo "FAIL: $proj make"
	exit 1
fi
make check
if ! test "$?" = "0"; then
	echo "FAIL: $proj make check"
	exit 1
fi
cp ../$proj.src/${proj}_testX.rc ../$proj/components/tests/instantiation.gen.rc
make check
if ! test "$?" = "0"; then
	echo "FAIL: $proj make check again"
	exit 1
fi
make install
if ! test "$?" = "0"; then
	echo "FAIL: $proj make install"
	exit 1
fi
echo PASS
exit 0
