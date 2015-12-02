#!/bin/sh
# test port creation with implicit package
cd $2
TDIR=crport3
mkdir $TDIR
cd $TDIR
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf myproj
msg=`$1 create project myproj`
if ! test -d "$2/$TDIR/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
msg=`$1 create port foo`
if ! test -f ports/sidl/myproj.foo.sidl; then
	echo "missing myproj/ports/sidl/myproj.foo.sidl"
	echo "FAIL"
	exit 1
fi
$1 create port foo
x=$?
if test "x$x" = "x0"; then
	echo "repeated create port did not report an error"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
