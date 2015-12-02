#!/bin/sh
# in-project help test
cd $2
mkdir help2
cd help2
if ! test "x$?" = "x0" ; then
        echo "changing to scratch directory $2 failed"
        echo "BROKEN"
        exit 1
fi
rm -rf myproj
msg=`$1 create project myproj`
if ! test -d "$2/help2/myproj/BOCCA"; then
        echo "missing myproj/BOCCA"
        echo "FAIL"
        exit 1
fi
cd myproj
$1 help
if test "x$?" = "x0" ; then
	echo PASS
	exit 0
else
	echo "help in project reported error???"
	echo "FAIL"
	exit 1
fi
