#!/bin/sh
# test package creation
cd $2
TDIR=crpkg1
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
msg1=`$1 create package pkg2`
y=$?
out=0
if ! test "x$y" = "x0"; then
	echo "create package failed for new package definition"
	echo "FAIL"
	out=1
fi
msg2=`$1 display package pkg2`
x=$?
if ! test "x$x" = "x0"; then
	echo "display package failed for new package definition"
	echo "FAIL"
	out=1
fi
if test "x$out" = "x0"; then
	echo "PASS"
fi
exit $out
