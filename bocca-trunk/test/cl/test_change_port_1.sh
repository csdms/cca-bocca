#!/bin/sh
# test port change with import
cd $2
TDIR=chport1
mkdir $TDIR
cd $TDIR
if ! test "x$?" = "x0" ; then
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
interface Func extends gov.cca.Port {
   int goomba(in string s, inout array<double> A);
}
interface Func2 {
   int goomba(in string s, inout array<double,2> A);
}
}
}
EOF
cd myproj
msg=`$1 create port foo`
if ! test -f ports/sidl/myproj.foo.sidl; then
	echo "missing myproj/ports/sidl/myproj.foo.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 change port --import-sidl=old.ports.Func:../oldport.sidl foo`
x=`grep goomba ports/sidl/*sidl`
case "$?" in
0) echo "Moved successfully: $x"
;;
*) echo "missing goomba in myproj/ports/sidl/myproj.foo.sidl"
   echo "FAIL"
   exit 1
esac

echo "PASS"
exit 0
