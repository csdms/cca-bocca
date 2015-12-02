#!/bin/sh
# test class creation w/inherits oddities
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf ccl2
mkdir ccl2
cd ccl2

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/ccl2/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
$1 create port mypkg.test.BPort 
$1 create port mypkg.test.APort -e BPort
$1 create class -lcxx --implements=mypkg.test.APort  mypkg.test.C2
$1 create class -lcxx -e mypkg.test.C2 mypkg.test.C3

if ! test -f components/sidl/mypkg.test.C3.sidl; then
	echo "missing components/sidl/mypkg.test.C3.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING Class ======================"
./configure; make
if ! test "x$?" = "x0"; then
	echo "problem compiling components/"
	echo "FAIL"
	exit 1
fi

if ! test -f install/lib/libmypkg.test.C3.la; then
	echo "problem finding install/lib/libmypkg.test.C3.la"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
