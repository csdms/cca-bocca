#!/bin/sh
# test component copying; handling of -i/-e/--requires/--import-sidl

cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf clcopy4
mkdir clcopy4
cd clcopy4

$1 create project -p mypkg myproj
if ! test -d "$2/clcopy4/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

# Class used to test -e option
$1 create class mypkg.extend
if ! test -f components/sidl/mypkg.extend.sidl; then
	echo "missing myproj/components/sidl/mypkg.extend.sidl"
	echo "FAIL"
	exit 1
fi

# This splice exists to create required SIDL symbols
cat <<EOF > splice.sidl
package demo version 0.0 {
	class foo {
		  // DO-NOT-DELETE bocca.splicer.begin(demo.foo.methods)
		  void imported();
		  // DO-NOT-DELETE bocca.splicer.end(demo.foo.metods)
	}
	interface bar {
		  // DO-NOT-DELETE bocca.splicer.begin(demo.bar.methods)
		  void implemented();
		  // DO-NOT-DELETE bocca.splicer.end(demo.bar.metods)
	}
	interface baz {
		  // DO-NOT-DELETE bocca.splicer.begin(demo.baz.methods)
		  void required();
		  // DO-NOT-DELETE bocca.splicer.end(demo.baz.metods)
	}
}
EOF

$1 create class \
    --extends=mypkg.extend \
    --implements=demo.bar@${PWD}/splice.sidl \
    --requires=demo.baz@${PWD}/splice.sidl \
    --import-sidl=demo.foo@${PWD}/splice.sidl \
    mypkg.cl
if ! test -f components/sidl/mypkg.cl.sidl; then
	echo "missing myproj/components/sidl/mypkg.cl.sidl"
	echo "FAIL"
	exit 1
fi

SIDLFILE=components/sidl/mypkg.cl2.sidl
$1 copy class mypkg.cl mypkg.cl2
if ! test -f $SIDLFILE; then
	echo "missing myproj/components/sidl/mypkg.cl2.sidl"
	echo "FAIL"
	exit 1
fi

echo "CHECK: mypkg.cl2.sidl extends mypkg.extend"
grep -e "class.*extends mypkg\.extend" $SIDLFILE > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not extend mypkg.extend"
    echo "FAIL"
    exit 1
fi

echo "CHECK: mypkg.cl2.sidl implements demo.bar"
grep -e "implements-all demo\.bar" $SIDLFILE > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not implement demo.bar"
    echo "FAIL"
    exit 1
fi

echo "CHECK: mypkg.cl2 requires demo.baz"
grep -e "class.*mypkg\.cl2.*requires.*demo\.baz.*externalSidlFiles" BOCCA/myproj.dat > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not require demo.baz"
    echo "FAIL"
    exit 1
fi

echo "CHECK: mypkg.cl2.sidl imports mypkg.cl.sidl"
grep -e "void imported()" $SIDLFILE > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not import mypkg.cl.sidl"
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

# NOTE: Avoid inclusion check, tested everywhere else and requires an extra merge!

echo "PASS"
exit 0
