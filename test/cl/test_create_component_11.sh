#!/bin/sh
# test simplest bad port creation
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf cc11
mkdir cc11
cd cc11






msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/cc11/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
./configure --prefix=$2/cc11/install
msg=`$1 create interface fv`
if ! test -f ports/sidl/mypkg.fv.sidl; then
	echo "$msg"
	echo "missing myproj/ports/sidl/mypkg.fv.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 create interface patch`
if ! test -f ports/sidl/mypkg.patch.sidl; then
	echo "$msg"
	echo "missing myproj/ports/sidl/mypkg.patch.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 create interface mesh`
if ! test -f ports/sidl/mypkg.mesh.sidl; then
	echo "$msg"
	echo "missing myproj/ports/sidl/mypkg.mesh.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 create interface bc`
if ! test -f ports/sidl/mypkg.bc.sidl; then
	echo "$msg"
	echo "missing myproj/ports/sidl/mypkg.bc.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 create enum mc`
if ! test -f ports/sidl/mypkg.mc.sidl; then
	echo "$msg"
	echo "missing myproj/ports/sidl/mypkg.mc.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 create class fvcxx --implements=fv`
if ! test -f components/sidl/mypkg.fvcxx.sidl; then
	echo "$msg"
	echo "missing myproj/components/sidl/mypkg.fvcxx.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 create class pcxx --implements=patch`
if ! test -f components/sidl/mypkg.pcxx.sidl; then
	echo "$msg"
	echo "missing myproj/components/sidl/mypkg.pcxx.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 create class mcxx --implements=mesh --requires=fvcxx,pcxx`
if ! test -f components/sidl/mypkg.mcxx.sidl; then
	echo "$msg"
	echo "missing myproj/components/sidl/mypkg.mcxx.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 create component micxx --extends=mcxx`
if ! test -f components/sidl/mypkg.micxx.sidl; then
	echo "$msg"
	echo "missing myproj/components/sidl/mypkg.micxx.sidl"
	echo "FAIL"
	exit 1
fi
make 
x=$?
if ! test "x$x" = "x0"; then
	echo "make failed"
	echo "FAIL"
	exit 1
fi
make install
x=$?
if ! test "x$x" = "x0"; then
	echo "make install failed"
	echo "FAIL"
	exit 1
fi

if ! test -f $2/cc11/install/lib/libmypkg.micxx.la; then
	echo "make install failed in linking a library. see .out file."
	echo "FAIL"
	exit 1
fi

echo "PASS"
exit 0
