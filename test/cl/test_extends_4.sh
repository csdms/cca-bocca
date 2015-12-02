#!/bin/sh
# test extends args
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf extends4
mkdir extends4
cd extends4

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/extends4/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
./configure

msg=`$1 create interface mypkg.foo --extends=sidl.BaseException`
if ! test -f ports/sidl/mypkg.foo.sidl; then
	echo "missing myproj/ports/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi

echo "COMPILING iface clients"
make
if ! test "x$?" = "x0"; then
	echo "problem compiling myproj/ports/mypkg.foo"
	echo "FAIL"
	exit 1
fi

echo "PASS"
exit 0
