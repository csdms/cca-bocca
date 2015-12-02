#!/bin/sh
# no double creation test.
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
if ! test -d myproj ; then
	echo "expected to find myproj in $2 from previous creation test"
	echo "BROKEN"
	exit 1
fi
$1 create project myproj
# this is expected to fail because it was already done. if it succeeds, we've an error.
if ! test "x$?" = "x0" ; then
	echo PASS
	exit 0
else
	echo "create project reported no error when doing duplicate call."
	echo "FAIL"
	exit 1
fi
