#!/bin/sh
# test basic class copying

BMERGE=$1-merge
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf clcopy1
mkdir clcopy1
cd clcopy1

$1 create project -p mypkg myproj
if ! test -d "$2/clcopy1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

$1 create class mypkg.cl
if ! test -f components/sidl/mypkg.cl.sidl; then
	echo "missing myproj/components/sidl/mypkg.cl.sidl"
	echo "FAIL"
	exit 1
fi

# This splicer includes empty protected blocks in order to handle
# issues with overwriting target blocks
cat <<EOF > splice
// DO-NOT-DELETE splicer.begin(mypkg.cl._includes)
// TEST: INCLUDED COMMENT
//bocca.protected.begin(mypkg.cl._includes)
//bocca.protected.end(mypkg.cl._includes)
// DO-NOT-DELETE splicer.end(mypkg.cl._includes)

// DO-NOT-DELETE splicer.begin(mypkg.cl.boccaSetServices)
// bocca.protected.begin(mypkg.cl.boccaSetServices)
// bocca.protected.end(mypkg.cl.boccaSetServices)
// DO-NOT-DELETE splicer.end(mypkg.cl.boccaSetServices)

// DO-NOT-DELETE splicer.begin(mypkg.cl.boccaReleaseServices)
// bocca.protected.begin(mypkg.cl.boccaReleaseServices)
// bocca.protected.end(mypkg.cl.boccaReleaseServices)
// DO-NOT-DELETE splicer.end(mypkg.cl.boccaReleaseServices)

// DO-NOT-DELETE splicer.begin(mypkg.cl.boccaForceUsePortInclude)
//bocca.protected.begin(mypkg.cl.boccaForceUsePortInclude)
//bocca.protected.end(mypkg.cl.boccaForceUsePortInclude)
// DO-NOT-DELETE splicer.end(mypkg.cl.boccaForceUsePortInclude)
EOF

$BMERGE --to=components/mypkg.cl/mypkg_cl_Impl.cxx --from=splice
if ! test "x$?" = "x0"; then
    echo "merge into CXX impl failed"
    echo "FAIL"
    exit 1
fi

$1 copy class mypkg.cl mypkg.cl2
if ! test -f components/sidl/mypkg.cl2.sidl; then
	echo "missing myproj/components/sidl/mypkg.cl2.sidl"
	echo "FAIL"
	exit 1
fi
echo "COMPILING project ======================"
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

echo "CHECK that mypkg.cl implementation was merged into mypkg.cl2 implementation"
grep -e "TEST: INCLUDED" components/mypkg.cl2/mypkg_cl2_Impl.cxx > /dev/null

if ! test "x$?" = "x0"; then
    echo "mypkg.cl implementation not merged into mypkg.cl2 implementation"
    echo "FAIL"
    exit 1
fi

echo "PASS"
exit 0
