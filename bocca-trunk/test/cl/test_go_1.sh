#!/bin/sh
# test --go on component creation (commandline, not compilation, test)
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf gp1
mkdir gp1
cd gp1

echo "creating project"
msg=`$1 create project myproj`
if ! test -d "$2/gp1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj

echo "creating port"
msg=`$1 create port myproj.IntegratorPort`
if ! test -f ports/sidl/myproj.IntegratorPort.sidl; then
	echo "missing myproj/ports/sidl/myproj.IntegratorPort.sidl"
	echo "FAIL"
	exit 1
fi
./configure
make
ccargs="--provides=myproj.IntegratorPort@myfoo --uses=myproj.IntegratorPort@integrate --go=run --uses=IntegratorPort@idummy"

for i in c cxx f90 python java f77 ; do
	echo "creating $i driver"
	echo "$1 create component ${i}Driver $ccargs"
	$1 create component -l$i ${i}Driver $ccargs
	if ! test -f components/sidl/myproj.${i}Driver.sidl; then
		echo "missing components/sidl/myproj.${i}Driver.sidl"
		echo "FAIL"
		exit 1
	fi
done
echo "PASS"
exit 0
