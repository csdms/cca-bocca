#!/bin/sh
# test class creation
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf ccl1
mkdir ccl1
cd ccl1

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/ccl1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

msg=`$1 create class mypkg.foo`
if ! test -f components/sidl/mypkg.foo.sidl; then
	echo "missing components/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING Class ======================"
./configure; make
if ! test "x$?" = "x0"; then
	echo "problem compiling components/mypkg.foo"
	echo "FAIL"
	exit 1
fi

if ! test -f install/lib/libmypkg.foo.la; then
	echo "problem finding install/lib/libmypkg.foo.la"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
