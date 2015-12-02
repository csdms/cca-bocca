#!/bin/sh
# test --go on java component
LANG=java
tdir=g$LANG
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf $tdir
mkdir $tdir
cd $tdir

echo "creating project"
msg=`$1 create project myproj`
if ! test -d "$2/$tdir/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
pwd
if ! test -f BOCCA/myproj.dat; then
	echo "missing myproj/BOCCA/myproj.dat"
	echo "FAIL"
	exit 1
else
	cat BOCCA/myproj.dat
fi

echo "creating port"
msg=`$1 -d create port myproj.IntegratorPort`
if ! test -f ports/sidl/myproj.IntegratorPort.sidl; then
	echo "missing myproj/ports/sidl/myproj.IntegratorPort.sidl"
	echo "FAIL"
	exit 1
fi
./configure
make
echo "TRYING"
echo "$1 create component Driver -l $LANG --provides=myproj.IntegratorPort@myfoo --uses=myproj.IntegratorPort@integrate"
$1 create component Driver -l $LANG --provides=myproj.IntegratorPort@myfoo --uses=myproj.IntegratorPort@integrate --go=run
if ! test -f components/sidl/myproj.Driver.sidl; then
	echo "missing components/sidl/myproj.Driver.sidl"
	echo "FAIL test go $LANG create component"
	exit 1
fi
echo "COMPILING Component"
make 
x=$?
if  test "x$x" != "x0" ; then
	echo "problem compiling "
	echo "FAIL test go $LANG compile"
	exit 1
fi
echo "CHECKING Component"
make check
x=$?
if test "x$x" = "x0" ; then
	echo "PASS"
else
	echo "problem with make check"
	echo "FAIL test go $LANG make check"
	exit 1
fi
exit 0
