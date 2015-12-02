#!/bin/sh
# test depl generation and use
tdir=depl
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

msg=`$1 -d create port mypkg.foo`
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

depldir=$top/install/share/cca/myproj

# next line is in-source, not the install place we really want.
foosidl=`$1 whereis port mypkg.foo`

if ! test -f $depldir/mypkg.foo_depl.xml; then
	echo "problem finding installed xml in $depldir"
	echo "FAIL"
	exit 1
fi

cd ..


msg=`$1 -d create project -p mypkg --dpath=$depldir depproj`
if ! test -d "$2/$tdir/depproj/BOCCA"; then
	echo "missing depproj/BOCCA"
	echo "FAIL"
	exit 1
fi
grep install/share/cca/myproj "$2/$tdir/depproj/BOCCA/depproj.defaults" 
if ! test "x$?" = "x0"; then
	echo "missing repository path expected in depproj/BOCCA/depproj.defaults"
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

$1 -d create component  mypkg.mycomp2  --dpath=$depldir
if ! test -f components/sidl/mypkg.mycomp2.sidl; then
	echo "missing depproj/components/sidl/mypkg.mycomp2.sidl"
	echo "FAIL"
	exit 1
fi
echo "#######################################"
echo "#######################################"
$1 -d create component  mypkg.mycomp  --provides=mypkg.foo@foo --dpath-show-aliases
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
