#!/bin/sh
# test component copying with --language

BMERGE=$1-merge
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf clcopy2
mkdir clcopy2
cd clcopy2

$1 create project -p mypkg myproj
if ! test -d "$2/clcopy2/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

$1 create class mypkg.cl
if ! test -f components/sidl/mypkg.cl.sidl; then
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

$BMERGE --to=components/mypkg.cl/mypkg_cl_Impl.cxx --from=splice
if ! test "x$?" = "x0"; then
    echo "merge into CXX impl failed"
    echo "FAIL"
    exit 1
fi

$1 copy class --language=f90 mypkg.cl mypkg.cl2
if ! test -f components/sidl/mypkg.cl2.sidl; then
	echo "missing myproj/components/sidl/mypkg.cl2.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING Project ======================"
./configure
make
if ! test "x$?" = "x0"; then
	echo "problem compiling myproj/components/mypkg.cl"
	echo "FAIL"
	exit 1
fi
echo "CHECKING Project ========================"
make check
if ! test "x$?" = "x0"; then
	echo "problem with make check for myproj/components/mypkg.cl"
	echo "FAIL"
	exit 1
fi

echo "CHECK for correct implementation file"
if ! test -f components/mypkg.cl2/mypkg_cl2_Impl.F90; then
    echo "F90 implementation not generated for mypkg.cl2"
    echo "FAIL"
    exit 1
fi

echo "CHECK that C++ implementation was not merged into F90 implementation"
# $?=1 indicates grep failed to find a match
grep -e "TEST: INCLUDED" components/mypkg.cl2/mypkg_cl2_Impl.F90 > /dev/null

if ! test "x$?" = "x1"; then
    echo "cxx implementation merged into F90 implementation"
    echo "FAIL"
    exit 1
fi

echo "PASS"
exit 0
