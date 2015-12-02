#!/bin/sh
# top level help test; should work without project present.
echo $1 help
$1 help
if test "x$?" = "x0" ; then
	echo PASS
	exit 0
else
	echo "help reported error???"
	echo "FAIL"
	exit 1
fi
