#!/bin/sh
# test class creation with import. particularly concerned with comments
# output must be inspected manually until we have a canonical answer.
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf ccl3
mkdir ccl3
cd ccl3

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/ccl3/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
./configure
cat  << EOF > x.sidl
	// DO-NOT-DELETE bocca.splicer.begin(mypkg.comment)
		// user typed package comment
	// DO-NOT-DELETE bocca.splicer.end(mypkg.comment)
	package mypkg version 0.0 {
	    // DO-NOT-DELETE bocca.splicer.begin(mypkg.x.comment)
		// user typed class comment 
	    // DO-NOT-DELETE bocca.splicer.end(mypkg.x.comment)
	    class x 
	    {
		// DO-NOT-DELETE bocca.splicer.begin(mypkg.x.methods)
			// user typed method and comment
			void bar(in int q);
		// DO-NOT-DELETE bocca.splicer.end(mypkg.x.methods)
	    }
	}
EOF

# eat user sidl with different name
msg=`$1 create class mypkg.foo --import-sidl=mypkg.x@x.sidl`
if ! test -f components/sidl/mypkg.foo.sidl; then
	echo "missing components/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi

echo "imported to components/sidl/mypkg.foo.sidl"
grep DO-NOT-DELETE components/sidl/mypkg.foo.sidl

# eat user sidl with same name
msg=`$1 create class mypkg.x --import-sidl=mypkg.x@x.sidl`
if ! test -f components/sidl/mypkg.x.sidl; then
	echo "missing components/sidl/mypkg.x.sidl"
	echo "FAIL"
	exit 1
fi

echo "imported to components/sidl/mypkg.x.sidl"
grep DO-NOT-DELETE components/sidl/mypkg.x.sidl

# and finally eating exactly our own output
msg=`$1 create class mypkg.baz --import-sidl=mypkg.foo@components/sidl/mypkg.foo.sidl`
if ! test -f components/sidl/mypkg.baz.sidl; then
        echo "missing components/sidl/mypkg.baz.sidl"
        echo "FAIL"
        exit 1
fi

echo "imported to components/sidl/mypkg.baz.sidl"
grep DO-NOT-DELETE components/sidl/mypkg.baz.sidl

echo "XFAIL"

cat components/sidl/mypkg.foo.sidl
cat components/sidl/mypkg.x.sidl
cat components/sidl/mypkg.baz.sidl
exit 0
