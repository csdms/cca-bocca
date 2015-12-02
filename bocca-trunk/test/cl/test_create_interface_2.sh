#!/bin/sh
# test classdependent iface creation
cd $2
BMERGE=$1-merge
mkdir criface2
cd criface2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf myproj
msg=`$1 create project myproj`
if ! test -d "$2/criface2/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
./configure
msg=`$1 create class myproj.concrete`
if ! test -f components/sidl/myproj.concrete.sidl; then
	echo "missing myproj/components/sidl/myproj.concrete.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 create port myproj.foo`
if ! test -f ports/sidl/myproj.foo.sidl; then
	echo "missing myproj/ports/sidl/myproj.foo.sidl"
	echo "FAIL"
	exit 1
fi
msg=`$1 create component myproj.bar --provides=myproj.foo`
if ! test -f components/sidl/myproj.bar.sidl; then
	echo "missing myproj/components/sidl/myproj.bar.sidl"
	echo "FAIL"
	exit 1
fi

cat << EOF > splice
        // DO-NOT-DELETE bocca.splicer.begin(myproj.foo.methods)
        myproj.concrete getWeight();
        // DO-NOT-DELETE bocca.splicer.end(myproj.foo.methods)
EOF
$BMERGE -A 'DO-NOT-DELETE bocca.splicer' -B 'DO-NOT-DELETE bocca.splicer' --from=splice --to=ports/sidl/myproj.foo.sidl
if ! test "x$?" = "x0" ; then
  echo "merge failed"
  echo "FAIL"
  exit 1
fi
$1 change myproj.foo --requires=myproj.concrete
make  
if ! test -f install/lib/libmyproj.foo-cxx.la ; then
	echo "missing install/lib/libmyproj.foo-cxx.la"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
