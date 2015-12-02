#!/bin/sh
# test port creation with import
cd $2
TDIR=crport4
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
interface Func {
   int goomba(in string s, in array<double> A);
}
interface Func2 {
   int foomba(in string s, in array<double,2> A);
}
}
}
EOF
cd myproj
msg=`$1 -d create port --import-sidl=../oldport.sidl foo`
if ! test -f ports/sidl/myproj.foo.sidl; then
	echo "missing myproj/ports/sidl/myproj.foo.sidl"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
