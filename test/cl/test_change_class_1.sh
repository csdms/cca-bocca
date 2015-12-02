#!/bin/sh
# test class change, removing interface
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf chcl1
mkdir chcl1
cd chcl1

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/chcl1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

msg=`$1 create interface mypkg.iface1`
if ! test -f ports/sidl/mypkg.iface1.sidl; then
	echo "missing ports/sidl/mypkg.iface1.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 create interface mypkg.iface2`
if ! test -f ports/sidl/mypkg.iface2.sidl; then
	echo "missing ports/sidl/mypkg.iface2.sidl"
	echo "FAIL"
	exit 1
fi

msg=`$1 create class -imypkg.iface1 -imypkg.iface2 mypkg.foo`
if ! test -f components/sidl/mypkg.foo.sidl; then
	echo "missing components/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi

echo "CHECK implements iface1, iface2"
grep -e "implements.*iface1.*iface2" components/sidl/mypkg.foo.sidl > /dev/null

if ! test "x$?" = "x0"; then
    echo "Does not implement iface1 or iface2"
    echo "FAIL"
    exit 1
fi

msg=`$1 change class --remove-implements=mypkg.iface1 mypkg.foo`
echo "POST-CHANGE CHECK: implements iface2 only"
grep -e "implements.*iface2" components/sidl/mypkg.foo.sidl > /dev/null

if ! test "x$?" = "x0"; then
    echo "Does not implement iface2"
    echo "FAIL"
    exit 1
fi

grep -e "implements.*iface1" components/sidl/mypkg.foo.sidl > /dev/null

if ! test "x$?" = "x1"; then
    echo "Implements iface1"
    echo "FAIL"
    exit 1
fi

echo "PASS"
exit 0
