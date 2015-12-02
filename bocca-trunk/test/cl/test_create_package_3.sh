#!/bin/sh
echo "ARGS: $*"
# test subpackage creation
cd $2
TDIR=crpkg3
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

msg1=`$1 create package --version 0.0 gov`
y=$?
out=0
if ! test "x$y" = "x0"; then
	echo "create package failed for new package definition gov"
	echo "FAIL"
	out=1
fi
msg2=`$1 display package gov`
x=$?
if ! test "x$x" = "x0"; then
	echo "display package failed for gov"
	echo "FAIL"
	out=1
fi
g=`echo $msg2 | grep 'version 0.0'`
z=$?
if ! test "x$z" = "x0"; then
	echo "version failed for gov"
	echo "FAIL"
	out=1
fi

msg1=`$1 create package --version 0.8.5 gov.cca`
y=$?
out=0
if ! test "x$y" = "x0"; then
	echo "create package failed for new package definition gov.cca"
	echo "FAIL"
	out=1
fi
msg2=`$1 display package gov.cca`
x=$?
if ! test "x$x" = "x0"; then
	echo "display package failed for gov.cca"
	echo "FAIL"
	out=1
fi
g=`echo $msg2 | grep 'version 0.8.5'`
z=$?
if ! test "x$z" = "x0"; then
	echo "version failed for gov.cca"
	echo "FAIL"
	out=1
fi

msg1=`$1 create package --version 0.0.0 gov.cca.ports`
y=$?
out=0
if ! test "x$y" = "x0"; then
	echo "create package failed for new package definition gov.cca.ports"
	echo "FAIL"
	out=1
fi
msg2=`$1 display package gov.cca.ports`
x=$?
if ! test "x$x" = "x0"; then
	echo "display package failed for gov.cca.ports"
	echo "FAIL"
	out=1
fi
g=`echo $msg2 | grep 'version 0.0.0'`
z=$?
if ! test "x$z" = "x0"; then
	echo "version failed for gov.cca.ports"
	echo "FAIL"
	out=1
fi

# no output due to special casing in bocca that needs long-term fix.

if test "x$out" = "x0"; then
	echo "XFAIL"
fi
exit $out
