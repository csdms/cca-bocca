#!/bin/sh
# test simplest bad port creation
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf cc10
mkdir cc10
cd cc10

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/cc10/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

msg=`$1 create port mypkg.foo`
if ! test -f ports/sidl/mypkg.foo.sidl; then
	echo "missing myproj/ports/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi
echo "TRYING"
echo "$1 create component mypkg.c -l c --provides=mypkg.foo@myfoo --uses=mypkg.foo@yourfoo--uses=mypkg.foo@yourfoo2"
$1 create component mypkg.c -l c --provides=mypkg.foo@myfoo --uses=mypkg.foo@yourfoo--uses=mypkg.foo@yourfoo2
if ! test -f components/sidl/mypkg.c.sidl; then
	: ;	# echo "missing myproj/components/sidl/mypkg.c.sidl as expected"
else
	echo "should be missing myproj/components/sidl/mypkg.c.sidl"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
