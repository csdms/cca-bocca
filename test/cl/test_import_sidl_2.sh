#!/bin/sh
# test sidl import
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
msg=`$1 create class foo --import-sidl=old.ports.Func@./oldport.sidl`
if ! test -f components/sidl/myproj.foo.sidl; then
	echo "missing myproj/components/sidl/myproj.foo.sidl"
	echo "FAIL"
	exit 1
fi
if grep 'function comment in' components/sidl/myproj.foo.sidl; then
	:
else
	echo "FAIL: function comment not preserved."
	exit 1
fi
if grep 'class comment in' components/sidl/myproj.foo.sidl; then
	:
else
	echo "XFAIL: class comment not preserved."
	exit 1
fi
if grep 'see package comment' components/sidl/myproj.foo.sidl; then
	echo "NOTE: package comment preserved."
else
	echo "XFAIL: package comment not preserved."
fi
if grep 'see subpackage comment' components/sidl/myproj.foo.sidl; then
	echo "NOTE: subpackage comment preserved."
else
	echo "XFAIL: subpackage comment not preserved."
fi
echo "PASS"
exit 0
