#!/bin/sh
# test simplest port rename
cd $2

if ! test "x$?" = "x0" ; then
        echo "changing to scratch directory $2 failed"
        echo "BROKEN"
        exit 1
fi
rm -rf mvport1
mkdir mvport1
cd mvport1

if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf myproj
msg=`$1 create project myproj`
if ! test -d "$2/mvport1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
msg=`$1 create port myproj.foo`
if ! test -f ports/sidl/myproj.foo.sidl; then
	echo "missing myproj/ports/sidl/myproj.foo.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 create port myproj.bar`
if ! test -f ports/sidl/myproj.bar.sidl; then
	echo "missing myproj/ports/sidl/myproj.bar.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 rename port myproj.foo myproj.baz`
if test -f ports/sidl/myproj.foo.sidl; then
	echo "myproj/ports/sidl/myproj.foo.sidl is unexpectedly still there"
	echo "FAIL"
	exit 1
fi
if ! test -f ports/sidl/myproj.baz.sidl; then
	echo "missing myproj/ports/sidl/myproj.baz.sidl"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
