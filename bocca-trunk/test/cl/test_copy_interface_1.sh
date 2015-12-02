#!/bin/sh
# test basic interface copying

BMERGE=$1-merge
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf ifcopy1
mkdir ifcopy1
cd ifcopy1

$1 create project -p mypkg myproj
if ! test -d "$2/ifcopy1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

$1 create interface mypkg.iface
if ! test -f ports/sidl/mypkg.iface.sidl; then
	echo "missing myproj/ports/sidl/mypkg.iface.sidl"
	echo "FAIL"
	exit 1
fi

# This splicer includes empty protected blocks in order to handle
# issues with overwriting target blocks
cat <<EOF > splice
// DO-NOT-DELETE bocca.splicer.begin(mypkg.iface.methods)
void test();
// DO-NOT-DELETE bocca.splicer.end(mypkg.iface.methods)
EOF

$BMERGE --to=ports/sidl/mypkg.iface.sidl --from=splice \
    -A '// DO-NOT-DELETE bocca.splicer' -B '// DO-NOT-DELETE bocca.splicer'
if ! test "x$?" = "x0"; then
    echo "merge into SIDL failed"
    echo "FAIL"
    exit 1
fi

$1 copy interface mypkg.iface mypkg.iface2
if ! test -f ports/sidl/mypkg.iface2.sidl; then
	echo "missing myproj/ports/sidl/mypkg.iface2.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING project ======================"
./configure
make
if ! test "x$?" = "x0"; then
	echo "problem compiling myproj/ports/mypkg.iface"
	echo "FAIL"
	exit 1
fi
echo "CHECKING Project ========================"
make check
if ! test "x$?" = "x0"; then
	echo "problem with make check for myproj/ports/mypkg.iface"
	echo "FAIL"
	exit 1
fi

echo "CHECK that mypkg.iface SIDL was merged into mypkg.iface2 SIDL"
grep -e "void test()" ports/sidl/mypkg.iface2.sidl > /dev/null

if ! test "x$?" = "x0"; then
    echo "mypkg.iface SIDL not merged into mypkg.iface2 SIDL"
    echo "FAIL"
    exit 1
fi

echo "PASS"
exit 0
