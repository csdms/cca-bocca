#!/bin/sh
# test class change, handling of removing externals
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf chcl2
mkdir chcl2
cd chcl2

cat <<EOF > test.sidl
package demo version 0.0 {
interface foo {
  // DO-NOT-DELETE bocca.splicer.begin(demo.bar.methods)
  void test();
  // DO-NOT-DELETE bocca.splicer.end(demo.bar.metods)
}
}
EOF

TESTSIDL=$PWD/test.sidl
msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/chcl2/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

msg=`$1 create class --requires=demo.foo@$TESTSIDL mypkg.cl`
if ! test -f components/sidl/mypkg.cl.sidl; then
	echo "missing components/sidl/mypkg.cl.sidl"
	echo "FAIL"
	exit 1
fi

echo "CHECK compile"
./configure
make

if ! test "x$?" = "x0"; then
    echo "initial make failed"
    echo "FAIL"
    exit 1
fi

echo "CHECK cached test.sidl"
if ! test -e external/sidl/test.sidl; then
    echo "Did not cache test.sidl"
    echo "FAIL"
    exit 1
fi

msg=`$1 change class --remove-requires=demo.foo mypkg.cl`
echo "POST-CHANGE: cached test.sidl removed"

if test -e external/sidl/test.sidl; then
    echo "Cached test.sidl not removed"
    echo "FAIL"
    exit 1
fi

echo "PASS"
exit 0
