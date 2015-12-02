#!/bin/sh
# test co-installation of dependent project
tdir=coinst1
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf $tdir
mkdir $tdir
cd $tdir
top=`pwd`

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/$tdir/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

./configure --prefix=$top/install
if ! test "x$?" = "x0"; then
	echo "problem configuring myproj"
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
if ! test "x$?" = "x0"; then
	echo "problem building myproj"
	echo "FAIL"
	exit 1
fi

echo "INSTALLING port clients"
make install
if ! test "x$?" = "x0"; then
	echo "problem installing myproj"
	echo "FAIL"
	exit 1
fi

foosidl=`$1 whereis port mypkg.foo`
cd ..


msg=`$1 create project -p mypkg depproj`
if ! test -d "$2/$tdir/depproj/BOCCA"; then
	echo "missing depproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd depproj

./configure --prefix=$top/install "--with-languages=c cxx"
if ! test "x$?" = "x0"; then
	echo "problem configuring depproj"
	echo "FAIL"
	exit 1
fi

$1 create component  mypkg.mycomp --provides=mypkg.foo@foo@$foosidl 
if ! test -f components/sidl/mypkg.mycomp.sidl; then
	echo "missing depproj/components/sidl/mypkg.mycomp.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING Component ======================"
make
if ! test "x$?" = "x0"; then
	echo "problem compiling depproj/components/mypkg.mycomp"
	echo "FAIL"
	exit 1
fi

echo "CHECKING Component ========================"
make check
if ! test "x$?" = "x0"; then
	echo "problem with make check for depproj/components/mypkg.mycomp"
	echo "FAIL"
	exit 1
fi

echo "INSTALLING Component ========================"
make install
if ! test "x$?" = "x0"; then
	echo "problem with make check for depproj/components/mypkg.mycomp"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
