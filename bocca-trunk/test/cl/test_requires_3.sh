#!/bin/sh
# test sidl import fail modes
cd $2
TDIR=is2
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
cd myproj
cat << EOF > oldport.sidl
/** should we see package comment? */
package old version 1.0 {
/** should we see subpackage comment? */
package ports {
/** we should see class comment in the output. */
class Func {
   /** we should see function comment in the output. */
   int goomba(in string s, in array<double> A);
}
}
}
EOF
./configure
if test "$?" != "0" ; then
	echo "configure failed"
	echo "BROKEN"
	exit 1
fi
msg=`$1 create class foo --requires=old.ports.Func@./ye.oldeport.sidl`
if test "x$?" = "x0" ; then
	echo "FAIL: bad requires should have croaked create."
	exit 1
fi
if test -f components/sidl/myproj.foo.sidl; then
	echo "found myproj/components/sidl/myproj.foo.sidl"
	echo "FAIL: bad import should not have created sidl."
	exit 1
fi
echo "PASS"
exit 0
