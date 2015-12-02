#!/bin/sh
# test simplest iface creation
cd $2
mkdir criface1
cd criface1
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf myproj
msg=`$1 create project myproj`
if ! test -d "$2/criface1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
msg=`$1 create interface myproj.foo`
if ! test -f ports/sidl/myproj.foo.sidl; then
	echo "missing myproj/ports/sidl/myproj.foo.sidl"
	echo "FAIL"
	exit 1
fi
./configure
make -C ports
if ! test -f install/lib/libmyproj.foo-cxx.la ; then
	echo "missing install/lib/libmyproj.foo-cxx.la"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
