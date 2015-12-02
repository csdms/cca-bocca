#!/bin/sh
# test basic enum copying

BMERGE=$1-merge
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf emcopy1
mkdir emcopy1
cd emcopy1

$1 create project -p mypkg myproj
if ! test -d "$2/emcopy1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

$1 create enum mypkg.enm
if ! test -f ports/sidl/mypkg.enm.sidl; then
	echo "missing myproj/ports/sidl/mypkg.enm.sidl"
	echo "FAIL"
	exit 1
fi

# This splicer includes empty protected blocks in order to handle
# issues with overwriting target blocks
cat <<EOF > splice
// DO-NOT-DELETE bocca.splicer.begin(mypkg.enm.entries)
test1,
test2
// DO-NOT-DELETE bocca.splicer.end(mypkg.enm.entries)
EOF

$BMERGE --to=ports/sidl/mypkg.enm.sidl --from=splice \
    -A '// DO-NOT-DELETE bocca.splicer' -B '// DO-NOT-DELETE bocca.splicer'
if ! test "x$?" = "x0"; then
    echo "merge into SIDL failed"
    echo "FAIL"
    exit 1
fi

$1 copy enum mypkg.enm mypkg.enm2
if ! test -f ports/sidl/mypkg.enm2.sidl; then
	echo "missing myproj/ports/sidl/mypkg.enm2.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING project ======================"
./configure
make
if ! test "x$?" = "x0"; then
	echo "problem compiling myproj/ports/mypkg.enm"
	echo "FAIL"
	exit 1
fi
echo "CHECKING Project ========================"
make check
if ! test "x$?" = "x0"; then
	echo "problem with make check for myproj/ports/mypkg.enm"
	echo "FAIL"
	exit 1
fi

echo "CHECK that mypkg.enm SIDL was merged into mypkg.enm2 SIDL"
grep -e "test1" ports/sidl/mypkg.enm2.sidl > /dev/null
if ! test "x$?" = "x0"; then
    echo "mypkg.enm SIDL not merged into mypkg.enm2 SIDL"
    echo "FAIL"
    exit 1
fi

echo "CHECK that mypkg.enm2 SIDL does not contain 'dummy'"
grep -e "dummy" ports/sidl/mypkg.enm2.sidl > /dev/null
if ! test "x$?" = "x1"; then
    echo "mypkg.enm2 SIDL contains dummy enum element"
    echo "FAIL"
    exit 1
fi

echo "PASS"
exit 0
