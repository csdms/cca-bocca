#!/bin/sh
# test extends args
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf extends3
mkdir extends3
cd extends3

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/extends3/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
./configure

msg=`$1 create interface mypkg.foo --extends=gov.cca.TypeMap`
if ! test -f ports/sidl/mypkg.foo.sidl; then
	echo "missing myproj/ports/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi

echo "COMPILING port clients"
make
if ! test "x$?" = "x0"; then
	echo "problem compiling myproj/ports/mypkg.foo"
	echo "FAIL"
	exit 1
fi
msg=`$1 create class mypkg.bar --implements=mypkg.foo`
if ! test -f components/sidl/mypkg.bar.sidl; then
        echo "missing myproj/components/sidl/mypkg.bar.sidl"
        echo "FAIL"
        exit 1
fi
echo "COMPILING classes"
make
if ! test "x$?" = "x0"; then
        echo "problem compiling myproj/components/"
        echo "FAIL"
        exit 1
fi


echo "PASS"
exit 0
