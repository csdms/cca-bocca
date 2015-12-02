#!/bin/sh
# just summarize previous test results.
name="test_~.sh"
echo "Summary ------------------- "
result=0
x=`grep FAIL *.out`
case "$?" in
0)
	echo "Failures found:"
	echo "$x"
	result=1
;;
1)
	echo "No Failures found"
;;
2)
	echo "Unexpected failure to read output files"
	result=2
;;
*)
	echo "Unexpected return code ($?) from grep."
	result=2
esac

x=`grep BROKEN *.out`
case "$?" in
0)
	echo "Broken tests found:"
	echo "$x"
	result=1
;;
1)
	echo "No broken tests found"
;;
2)
	echo "Unexpected failure to read output files"
	result=2
;;
*)
	echo "Unexpected return code ($?) from grep."
	result=2
esac

x=`grep PENDING *.out`
case "$?" in
0)
	echo "pending tests found:"
	echo "$x"
	result=1
;;
1)
	echo "No pending tests found"
;;
2)
	echo "Unexpected failure to read output files"
	result=2
;;
*)
	echo "Unexpected return code ($?) from grep."
	result=2
esac

x=`grep PASS *.out`
case "$?" in
0)
	echo "Passed tests found:"
	echo "$x"
;;
1)
	echo "No passed tests found"
	result=1
;;
2)
	echo "Unexpected failure to read output files"
	result=2
;;
*)
	echo "Unexpected return code ($?) from grep."
	result=2
esac

echo "--------------------------- "
if test "$result" = "0"; then
	echo "$name: PASS"
else
	echo "$name: FAIL"
fi
exit $result
