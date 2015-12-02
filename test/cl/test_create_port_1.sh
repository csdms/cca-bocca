#!/bin/sh
# test simplest port creation
cd $2
mkdir crport1
cd crport1
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf myproj
msg=`$1 create project myproj`
if ! test -d "$2/crport1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
# currently there's some insane dependence on ccaffeine
# and configure that blocks handling port creation correctly
# and also fails to return a correct error code.
# --- this is only true if the bocca scripts attempt to run make [bn]
msg=`$1 create port myproj.foo`
if ! test -f ports/sidl/myproj.foo.sidl; then
	echo "missing myproj/ports/sidl/myproj.foo.sidl"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
