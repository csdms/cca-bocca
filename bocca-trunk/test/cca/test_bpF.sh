#!/bin/sh
proj=bpF
top=`pwd`
/bin/rm -rf $proj
$1 create project $proj
if ! test "$?" = "0"; then
	echo "FAIL: $proj create"
	exit 1
fi
cd $proj
mkdir itest
# make the F90 version
./configure --prefix=$top/$proj/itest
if ! test "$?" = "0"; then
	echo "FAIL: $proj config"
	exit 1
fi
$1 create component \
--go=go \
--provides=gov.cca.ports.BasicParameterPort:tuner \
--uses=gov.cca.ports.BasicParameterPort:tunertest \
--import-impl=${proj}.testX:$top/$proj.src \
-lf90 \
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
