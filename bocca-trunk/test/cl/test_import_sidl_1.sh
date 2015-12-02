#!/bin/sh
# test sidl import
cd $2
TDIR=is1
rm -rf $TDIR
mkdir $TDIR
cd $TDIR
if test "$?" != "0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf myproj
msg=`$1 create project myproj`
if ! test -d "$2/$TDIR/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cat << EOF > oldport.sidl
package old version 1.0 {
package ports {
/** we should see interface comment in the output. */
interface Func {
   /** we should see function comment in the output. */
   int goomba(in string s, in array<double> A);
}
}
}
EOF
cd myproj
msg=`$1 -d create port foo --import-sidl=old.ports.Func@../oldport.sidl`
# msg=`$1 -d create package ports --import-sidl=old.ports@../oldport.sidl`
if ! test -f ports/sidl/myproj.foo.sidl; then
	echo "missing myproj/ports/sidl/myproj.foo.sidl"
	echo "FAIL"
	exit 1
fi
if grep 'function comment in' ports/sidl/myproj.foo.sidl; then
	:
else
	echo "FAIL: function comment not preserved."
	exit 1
fi
if grep 'interface comment in' ports/sidl/myproj.foo.sidl; then
	:
else
	echo "XFAIL: interface comment not preserved."
	exit 1
fi
echo "PASS"
exit 0
