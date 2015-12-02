#!/bin/sh
# test simple install.
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf i1
mkdir i1
cd i1

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/i1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

./configure --prefix=`pwd`/installroot
if ! test "x$?" = "x0"; then
	echo "problem with configure for myproj/components/mypkg.mycomp"
	echo "FAIL"
	exit 1
fi

msg=`$1 create port mypkg.foo`
if ! test -f ports/sidl/mypkg.foo.sidl; then
	echo "missing myproj/ports/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING port clients"
make
echo "TRYING"
echo "$1 create component mypkg.mycomp --provides=mypkg.foo:myfoo --uses=mypkg.foo:yourfoo"
$1 create component  mypkg.mycomp
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
cd ..
make clean
if ! test "x$?" = "x0"; then
	echo "problem with make clean for myproj/components/mypkg.mycomp"
	echo "FAIL"
	exit 1
fi
mkdir installroot
if ! test "x$?" = "x0"; then
	echo "problem with mkdir for installroot"
	echo "FAIL"
	exit 1
fi
make
if ! test "x$?" = "x0"; then
	echo "problem with make for installation build"
	echo "FAIL"
	exit 1
fi
make install
if ! test "x$?" = "x0"; then
	echo "problem with make install build"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
