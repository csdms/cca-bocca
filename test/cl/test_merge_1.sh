#!/bin/sh
# test standard merge: --no-preserve

BMERGE=$1-merge

cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf m1
mkdir m1
cd m1

cat <<EOF > source
//  DO-NOT-DELETE splicer.begin(mypkg.foo._includes)
  // bocca.protected.begin(mypkg.foo._includes)
  #define invalid junk
  // bocca.protected.end(mypkg.foo._includes)
  #include <falseheader>  
//  DO-NOT-DELETE splicer.end(mypkg.foo._includes) 
EOF

MERGESRC=$PWD/source

echo "==== Creating project"
msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/m1/myproj/BOCCA"; then
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
$BMERGE --verbose -A 'DO-NOT-DELETE splicer' -B 'DO-NOT-DELETE splicer' --to=components/mypkg.foo/mypkg_foo_Impl.cxx --from=$MERGESRC --no-preserve
if ! test "x$?" = "x0"; then
    echo "merge did not succeed"
    echo "FAIL"
    exit 1
fi

grep -e "invalid junk" components/mypkg.foo/mypkg_foo_Impl.cxx > /dev/null
if ! test "x$?" = "x0"; then
    echo "did not find protected source 'invalid junk' in target"
    echo "FAIL"
    exit 1
fi

grep -e "include <falseheader>" components/mypkg.foo/mypkg_foo_Impl.cxx > /dev/null
if ! test "x$?" = "x0"; then
    echo "did not find unprotected source 'include <falseheader>' in target"
    echo "FAIL"
    exit 1
fi
echo "PASS"
exit 0
 