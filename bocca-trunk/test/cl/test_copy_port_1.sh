#!/bin/sh
# test basic port copying

BMERGE=$1-merge
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf pocopy1
mkdir pocopy1
cd pocopy1

$1 create project -p mypkg myproj
if ! test -d "$2/pocopy1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

$1 create port mypkg.port
if ! test -f ports/sidl/mypkg.port.sidl; then
	echo "missing myproj/ports/sidl/mypkg.port.sidl"
	echo "FAIL"
	exit 1
fi

# This splicer includes empty protected blocks in order to handle
# issues with overwriting target blocks
cat <<EOF > splice
// DO-NOT-DELETE bocca.splicer.begin(mypkg.port.methods)
void test();
// DO-NOT-DELETE bocca.splicer.end(mypkg.port.methods)
EOF

$BMERGE --to=ports/sidl/mypkg.port.sidl --from=splice \
    -A '// DO-NOT-DELETE bocca.splicer' -B '// DO-NOT-DELETE bocca.splicer'
if ! test "x$?" = "x0"; then
    echo "merge into SIDL failed"
    echo "FAIL"
    exit 1
fi

$1 copy port mypkg.port mypkg.port2
if ! test -f ports/sidl/mypkg.port2.sidl; then
	echo "missing myproj/ports/sidl/mypkg.port2.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING project ======================"
./configure
make
if ! test "x$?" = "x0"; then
	echo "problem compiling myproj/ports/mypkg.port"
	echo "FAIL"
	exit 1
fi
echo "CHECKING Project ========================"
make check
if ! test "x$?" = "x0"; then
	echo "problem with make check for myproj/ports/mypkg.port"
	echo "FAIL"
	exit 1
fi

echo "CHECK that mypkg.port2 extends gov.cca.Port"

echo "CHECK: mypkg.iface2.sidl extends mypkg.extend"
grep -e "interface.*extends gov\.cca\.Port" ports/sidl/mypkg.port2.sidl > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not extend gov.cca.Port"
    echo "FAIL"
    exit 1
fi

echo "CHECK that mypkg.port SIDL was merged into mypkg.port2 SIDL"
grep -e "void test()" ports/sidl/mypkg.port2.sidl > /dev/null

if ! test "x$?" = "x0"; then
    echo "mypkg.port SIDL not merged into mypkg.port2 SIDL"
    echo "FAIL"
    exit 1
fi

echo "PASS"
exit 0
