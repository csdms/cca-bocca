#!/bin/sh
# test simplest port creation
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf req1
mkdir req1
cd req1

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/req1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

msg=`$1 create port mypkg.bar`
msg=`$1 create port mypkg.foo`
if ! test -f ports/sidl/mypkg.foo.sidl; then
	echo "missing myproj/ports/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING port clients"
./configure
make
echo "TRYING"
echo "$1 create component mypkg.mycomp --provides=mypkg.foo@myfoo --requires=mypkg.bar"
$1 create component  mypkg.mycomp --provides=mypkg.foo@myfoo --requires=mypkg.bar
if ! test -f components/sidl/mypkg.mycomp.sidl; then
	echo "missing myproj/components/sidl/mypkg.mycomp.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING Component ======================"
cd components
make
if ! test "x$?" = "x0"; then
	echo "problem compiling myproj/components/mypkg.mycomp"
	echo "FAIL"
	exit 1
fi

echo "CHECKING Component ========================"
make check
if ! test "x$?" = "x0"; then
	echo "problem with make check for myproj/components/mypkg.mycomp"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
