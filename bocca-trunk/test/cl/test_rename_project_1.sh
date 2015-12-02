#!/bin/sh
# test project renaming
name=test_rename_project_1.sh
cwd=`pwd`
cd $2
scrdir=`pwd`
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf myproj1
msg=`$1 create project myproj1`
if ! test -d "myproj1/BOCCA"; then
	echo "missing myproj1/BOCCA"
	echo "FAIL"
	exit 1
fi
rm -rf renamedProj
cd myproj1
echo 'y' > input
msg=`$1 rename project renamedProj < input`
retcode="$?"
if ! test "$retcode" = "0"; then
	echo "rename project failed [$retcode]"
fi
rm -rf input
cd $scrdir
if ! test -e "renamedProj/BOCCA/Dir-renamedProj"; then
	echo "missing renamedProj/BOCCA/Dir-renamedProj"
	echo "FAIL"
	exit 1
fi
if test -d "renamedProj/BOCCA/Dir-myproj1"; then
        echo "rename did not succeed, original directory still here: myproj1"
	echo "FAIL"
	exit 1
fi
if test -e "renamedProj/BOCCA/Dir-myproj1"; then
        echo "found leftovers from myproj1: renamedProj/BOCCA/Dir-myproj1"
        echo "FAIL"
        exit 1
fi
echo "PASS"
exit 0
