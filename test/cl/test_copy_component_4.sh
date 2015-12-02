#!/bin/sh
# test component copying; handling of -i/-e/--requires/--import-sidl

cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf cocopy4
mkdir cocopy4
cd cocopy4

$1 create project -p mypkg myproj
if ! test -d "$2/cocopy4/myproj/BOCCA"; then
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

$1 create component \
    --uses=mypkg.foo:foo --provides=mypkg.bar:bar \
    --extends=mypkg.extend \
    --implements=demo.bar@${PWD}/splice.sidl \
    --requires=demo.baz@${PWD}/splice.sidl \
    --import-sidl=demo.foo@${PWD}/splice.sidl \
    mypkg.comp
if ! test -f components/sidl/mypkg.comp.sidl; then
	echo "missing myproj/components/sidl/mypkg.comp.sidl"
	echo "FAIL"
	exit 1
fi

SIDLFILE=components/sidl/mypkg.comp2.sidl
$1 copy component mypkg.comp mypkg.comp2
if ! test -f $SIDLFILE; then
	echo "missing myproj/components/sidl/mypkg.comp2.sidl"
	echo "FAIL"
	exit 1
fi

echo "CHECK: mypkg.comp2.sidl extends mypkg.extend"
grep -e "class.*extends mypkg\.extend" $SIDLFILE > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not extend mypkg.extend"
    echo "FAIL"
    exit 1
fi

echo "CHECK: mypkg.comp2.sidl implements demo.bar"
grep -e "implements-all.*demo\.bar" $SIDLFILE > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not implement demo.bar"
    echo "FAIL"
    exit 1
fi

echo "CHECK: mypkg.comp2 requires demo.baz"
grep -e "component.*mypkg\.comp2.*requires.*demo\.baz.*externalSidlFiles" BOCCA/myproj.dat > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not require demo.baz"
    echo "FAIL"
    exit 1
fi

echo "CHECK: mypkg.comp2.sidl imports mypkg.comp.sidl"
grep -e "void imported()" $SIDLFILE > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not import mypkg.comp.sidl"
    echo "FAIL"
    exit 1
fi

echo "COMPILING project ======================"
./configure
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

# NOTE: Avoid inclusion check, tested everywhere else and requires an extra merge!


echo "CHECK: correct ports"
$1 display component mypkg.comp > comp1
$1 display component mypkg.comp2 > comp2

diff comp1 comp2 | grep 'port'

# $?=1 indicates grep failed to find a match
if ! test "x$?" = "x1"; then
    echo "Ports differ for mypkg.comp and mypkg.comp2"
    echo "FAIL"
    exit 1
fi

echo "PASS"
exit 0
