#!/bin/sh
# test simplest port creation
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf po1
mkdir po1
cd po1

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/po1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

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
echo "$1 create component mypkg.mycomp  -lcxx --provides=mypkg.foo@yourfoo"
$1 create component  mypkg.mycomp
if ! test -f components/sidl/mypkg.mycomp.sidl; then
	echo "missing myproj/components/sidl/mypkg.mycomp.sidl"
	echo "FAIL"
	exit 1
fi

for LANG in c f77 f90 ; do
echo "$1 create component mypkg.mycomp$LANG  -l$LANG --provides=mypkg.foo@yourfoo"
$1 create component -l$LANG mypkg.mycomp$LANG
if ! test -f components/sidl/mypkg.mycomp${LANG}.sidl; then
	echo "missing myproj/components/sidl/mypkg.mycomp${LANG}.sidl"
	echo "FAIL"
	exit 1
fi
done

echo "COMPILING Components ======================"
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
