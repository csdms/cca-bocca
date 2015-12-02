#!/bin/sh
# test merge with preservation and --output-missing-protected-conflicts

BMERGE=$1-merge

cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf m3
mkdir m3
cd m3

BASEDIR=$PWD
cat <<EOF > source
//  DO-NOT-DELETE splicer.begin(mypkg.foo._includes)
  // bocca.protected.begin(mypkg.foo._includes)
  #define invalid junk
  // bocca.protected.end(mypkg.foo._includes)
  #include <falseheader>  
//  DO-NOT-DELETE splicer.end(mypkg.foo._includes) 
// DO-NOT-DELETE splicer.begin(mypkg.foo.boccaForceUsePortInclude)
  // Protected block missing
// DO-NOT-DELETE splicer.end(mypkg.foo.boccaForceUsePortInclude)
EOF

MERGESRC=$PWD/source

echo "==== Creating project"
msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/m3/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

echo "==== Creating class"
msg=`$1 create class mypkg.foo`
if ! test -f components/sidl/mypkg.foo.sidl; then
	echo "missing components/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi

echo "==== Merging"
$BMERGE --verbose -A 'DO-NOT-DELETE splicer' -B 'DO-NOT-DELETE splicer' --to=components/mypkg.foo/mypkg_foo_Impl.cxx --from=$MERGESRC --output-missing-protected-conflicts
if ! test "x$?" = "x0"; then
    echo "merge did not succeed"
    echo "FAIL"
    exit 1
fi

FILE=components/mypkg.foo/mypkg_foo_Impl.cxx
# check _include protected block
grep -e "_BOCCA_CTOR_PRINT" $FILE > /dev/null
if ! test "x$?" = "x0"; then
    echo "did not find protected target '_BOCCA_CTOR_PRINT' in target"
    echo "FAIL"
    exit 1
fi

grep -e "include <falseheader>" $FILE > /dev/null
if ! test "x$?" = "x0"; then
    echo "did not find unprotected source 'include <falseheader>' in target"
    echo "FAIL"
    exit 1
fi

# check boccaForcePortInclude protected block; should contain diff
grep -e "\<\<[:space:]*$FILE:" -A5 $FILE | \
grep -e "^//.*protected\.begin(mypkg\.foo\.boccaForceUsePortInclude)" -A2 $FILE | \
grep -e "^//.*protected\.end(mypkg\.foo\.boccaForceUsePortInclude)" $FILE > /dev/null

if ! test "x$?" = "x0"; then
    echo "did not find protected block for 'boccaForceUsePortInclude' in target diff"
    echo "FAIL"
    exit 1
fi

# check boccaForcePortInclude protected block; should contain diff
grep -e "\<\<[:space:]*$BASEDIR/source:" -A5 $FILE | \
grep -e "^//.*Protected block missing" $FILE > /dev/null

if ! test "x$?" = "x0"; then
    echo "did not find missing protected diff block from source in target diff"
    echo "FAIL"
    exit 1
fi

echo "PASS"
exit 0
 