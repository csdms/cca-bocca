#!/bin/sh
# test component copying with --language

BMERGE=$1-merge
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf cocopy2
mkdir cocopy2
cd cocopy2

$1 create project -p mypkg myproj
if ! test -d "$2/cocopy2/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

$1 create port mypkg.foo
if ! test -f ports/sidl/mypkg.foo.sidl; then
	echo "missing myproj/ports/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi
$1 create port mypkg.bar
if ! test -f ports/sidl/mypkg.bar.sidl; then
	echo "missing myproj/ports/sidl/mypkg.bar.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING Ports ================"
./configure
make

$1 create component mypkg.comp --uses=mypkg.foo:foo --provides=mypkg.bar:bar
if ! test -f components/sidl/mypkg.comp.sidl; then
	echo "missing myproj/components/sidl/mypkg.mycomp.sidl"
	echo "FAIL"
	exit 1
fi

# This splicer includes empty protected blocks in order to handle
# issues with overwriting target blocks
cat <<EOF > splice
// DO-NOT-DELETE splicer.begin(mypkg.comp._includes)
// TEST: INCLUDED COMMENT
//bocca.protected.begin(mypkg.comp._includes)
//bocca.protected.end(mypkg.comp._includes)
// DO-NOT-DELETE splicer.end(mypkg.comp._includes)

// DO-NOT-DELETE splicer.begin(mypkg.comp.boccaSetServices)
// bocca.protected.begin(mypkg.comp.boccaSetServices)
// bocca.protected.end(mypkg.comp.boccaSetServices)
// DO-NOT-DELETE splicer.end(mypkg.comp.boccaSetServices)

// DO-NOT-DELETE splicer.begin(mypkg.comp.boccaReleaseServices)
// bocca.protected.begin(mypkg.comp.boccaReleaseServices)
// bocca.protected.end(mypkg.comp.boccaReleaseServices)
// DO-NOT-DELETE splicer.end(mypkg.comp.boccaReleaseServices)

// DO-NOT-DELETE splicer.begin(mypkg.comp.boccaForceUsePortInclude)
//bocca.protected.begin(mypkg.comp.boccaForceUsePortInclude)
//bocca.protected.end(mypkg.comp.boccaForceUsePortInclude)
// DO-NOT-DELETE splicer.end(mypkg.comp.boccaForceUsePortInclude)
EOF

$BMERGE --to=components/mypkg.comp/mypkg_comp_Impl.cxx --from=splice
if ! test "x$?" = "x0"; then
    echo "merge into CXX impl failed"
    echo "FAIL"
    exit 1
fi

$1 copy component --language=f90 mypkg.comp mypkg.comp2
if ! test -f components/sidl/mypkg.comp2.sidl; then
	echo "missing myproj/components/sidl/mypkg.comp2.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING Project ======================"
make
if ! test "x$?" = "x0"; then
	echo "problem compiling myproj/components/mypkg.comp"
	echo "FAIL"
	exit 1
fi
echo "CHECKING Project ========================"
make check
if ! test "x$?" = "x0"; then
	echo "problem with make check for myproj/components/mypkg.comp"
	echo "FAIL"
	exit 1
fi

echo "CHECK for correct implementation file"
if ! test -f components/mypkg.comp2/mypkg_comp2_Impl.F90; then
    echo "F90 implementation not generated for mypkg.comp2"
    echo "FAIL"
    exit 1
fi

echo "CHECK that C++ implementation was not merged into F90 implementation"
# $?=1 indicates grep failed to find a match
grep -e "TEST: INCLUDED" components/mypkg.comp2/mypkg_comp2_Impl.F90 > /dev/null

if ! test "x$?" = "x1"; then
    echo "cxx implementation merged into F90 implementation"
    echo "FAIL"
    exit 1
fi

echo "CHECK for correct ports"
$1 display component mypkg.comp > comp1
$1 display component mypkg.comp2 > comp2

diff comp1 comp2 | grep 'port' > /dev/null

if ! test "x$?" = "x1"; then
    echo "Ports differ for mypkg.comp and mypkg.comp2"
    echo "FAIL"
    exit 1
fi

echo "PASS"
exit 0
