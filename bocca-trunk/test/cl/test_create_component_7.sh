#!/bin/sh
# test simplest component creation.
LANG=f77

cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
ldir=cc4-$LANG
rm -rf $ldir
mkdir $ldir
cd $ldir

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/$ldir/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
./configure --with-languages="$LANG"

echo "TRYING port"
start=`date +%s`
msg=`$1 create port mypkg.foo`
stop=`date +%s`; echo "Took `expr $stop - $start`"
if ! test -f ports/sidl/mypkg.foo.sidl; then
	echo "missing myproj/ports/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi
echo "TRYING component"

echo "$1 create component mypkg.mycomp$LANG -l $LANG --provides=mypkg.foo@myfoo --uses=mypkg.foo@yourfoo"
start=`date +%s`
$1 create component  mypkg.mycomp$LANG -l $LANG --provides=mypkg.foo@myfoo --uses=mypkg.foo@yourfoo
stop=`date +%s`; echo "Took `expr $stop - $start`"
if ! test -f components/sidl/mypkg.mycomp$LANG.sidl; then
	echo "missing myproj/components/sidl/mypkg.mycomp$LANG.sidl"
	echo "FAIL"
	exit 1
fi

echo "COMPILING Components ======================"
start=`date +%s`
./configure
if ! test "x$?" = "x0"; then
	echo "problem configuring myproj"
	echo "FAIL"
	exit 1
fi
stop=`date +%s`; echo "Took configure: `expr $stop - $start`"
start=`date +%s`
make
if ! test "x$?" = "x0"; then
	echo "problem compiling myproj/components/"
	echo "FAIL"
	exit 1
fi
stop=`date +%s`; echo "Took make: `expr $stop - $start`"

echo "CHECKING Component ========================"
make check
if ! test "x$?" = "x0"; then
	echo "problem with make check for myproj/components/mypkg.mycomp$LANG"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
