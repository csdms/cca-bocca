#!/bin/sh
echo "ARGS: $*"
# test subpackage creation
cd $2
TDIR=crpkg2
rm -rf $TDIR
mkdir $TDIR
cd $TDIR
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
msg=`$1 create project myproj`
if ! test -d "myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
./configure

msg1=`$1 create package --version 0.0 gob`
y=$?
out=0
if ! test "x$y" = "x0"; then
	echo "create package failed for new package definition gob"
	echo "FAIL"
	out=1
fi
msg2=`$1 display package gob`
x=$?
if ! test "x$x" = "x0"; then
	echo "display package failed for gob"
	echo "FAIL"
	out=1
fi
g=`echo $msg2 | grep 'version 0.0'`
z=$?
if ! test "x$z" = "x0"; then
	echo "version failed for gob"
	echo "FAIL"
	out=1
fi

msg1=`$1 create package --version 0.8.5 gob.cca`
y=$?
out=0
if ! test "x$y" = "x0"; then
	echo "create package failed for new package definition gob.cca"
	echo "FAIL"
	out=1
fi
msg2=`$1 display package gob.cca`
x=$?
if ! test "x$x" = "x0"; then
	echo "display package failed for gob.cca"
	echo "FAIL"
	out=1
fi
g=`echo $msg2 | grep 'version 0.8.5'`
z=$?
if ! test "x$z" = "x0"; then
	echo "version failed for gob.cca"
	echo "FAIL"
	out=1
fi

msg1=`$1 create package --version 0.0.0 gob.cca.ports`
y=$?
out=0
if ! test "x$y" = "x0"; then
	echo "create package failed for new package definition gob.cca.ports"
	echo "FAIL"
	out=1
fi
msg2=`$1 display package gob.cca.ports`
x=$?
if ! test "x$x" = "x0"; then
	echo "display package failed for gob.cca.ports"
	echo "FAIL"
	out=1
fi
g=`echo $msg2 | grep 'version 0.0.0'`
z=$?
if ! test "x$z" = "x0"; then
	echo "version failed for gob.cca.ports"
	echo "FAIL"
	out=1
fi


if test "x$out" = "x0"; then
	echo "PASS"
fi
exit $out
