#!/bin/sh
# test copy w/-e/--requires/--import-sidl

cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf pocopy2
mkdir pocopy2
cd pocopy2

$1 create project -p mypkg myproj
if ! test -d "$2/pocopy2/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

# Class used to test -e option
$1 create interface mypkg.extend
if ! test -f ports/sidl/mypkg.extend.sidl; then
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


$1 create port \
    --extends=mypkg.extend \
    --requires=demo.foo@${PWD}/splice.sidl \
    --import-sidl=demo.foo@${PWD}/splice.sidl \
    mypkg.port

if ! test "x$?" = "x0"; then
    echo "Could not create mypkg.port"
    echo "FAIL"
    exit 1
fi


SIDLFILE=ports/sidl/mypkg.port2.sidl
$1 copy port mypkg.port mypkg.port2
if ! test -f $SIDLFILE; then
	echo "missing myproj/ports/sidl/mypkg.port2.sidl"
	echo "FAIL"
	exit 1
fi

echo "CHECK: mypkg.port2.sidl extends mypkg.extend"
grep -e '\(extends \)\?mypkg\.extend' $SIDLFILE > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not extend mypkg.extend"
    echo "FAIL"
    exit 1
fi

echo "CHECK: mypkg.port2.sidl extends gov.cca.Port"
# No guarantee it appears after 'extends', port_1 should check for that case
grep -e '\(extends \)\?gov\.cca\.Port' $SIDLFILE > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not extend gov.cca.Port"
    echo "FAIL"
    exit 1
fi

echo "CHECK: mypkg.port2 requires demo.foo"
grep -e "port.*mypkg\.port2.*requires.*demo\.foo.*externalSidlFiles" BOCCA/myproj.dat > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not require demo.baz"
    echo "FAIL"
    exit 1
fi

echo "CHECK: mypkg.port2.sidl imports mypkg.port.sidl"
grep -e "void imported()" $SIDLFILE > /dev/null
if ! test "x$?" = "x0"; then
    echo "class does not import mypkg.port.sidl"
    echo "FAIL"
    exit 1
fi

echo "COMPILING project ======================"
./configure
make
if ! test "x$?" = "x0"; then
	echo "problem compiling myproj/ports/mypkg.port"
	echo "FAIL"
	exit 1
fi
echo "CHECKING Project ========================"
make check
if ! test "x$?" = "x0"; then
	echo "problem with make check for myproj/ports/mypkg.port"
	echo "FAIL"
	exit 1
fi

echo "PASS"
exit 0
