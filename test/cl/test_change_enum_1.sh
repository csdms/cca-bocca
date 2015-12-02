#!/bin/sh
# test enum change, importing SIDL w/build merge
topdir=`pwd`
cd $2
if ! test "x$?" = "x0" ; then
    echo "changing to scratch directory $2 failed"	
    echo "BROKEN"
    exit 1
fi
rm -rf chenum1
mkdir chenum1
cd chenum1

# Create project to import from
msg=`$1 create project -p mypkg from`
if ! test -d "$2/chenum1/from/BOCCA"; then
    echo "missing from/BOCCA"
    echo "FAIL"
    exit 1
fi
cd from

msg=`$1 create interface mypkg.iface`
if ! test -f ports/sidl/mypkg.iface.sidl; then
    echo "missing ports/sidl/mypkg.iface.sidl"
    echo "FAIL"
    exit 1
fi

# Patch source (from)
echo "Patching source project"
# Patch port makefiles
patch ports/make.rules.user $topdir/patches/makefiles/port/make.rules.user.source.patch
if ! test "x$?" = "x0"; then
    echo "Patching ports/make.rules.user from ${topdir}/patches/makefiles/port/make.rules.user.source.patch failed"
    echo "FAIL"
    exit 1
fi
patch ports/make.vars.user ${topdir}/patches/makefiles/port/make.vars.user.source.patch
if ! test "x$?" = "x0"; then
    echo "Patching ports/make.vars.user from $topdir/patches/makefiles/port/make.vars.user.source.patch failed"
    echo "FAIL"
    exit 1
fi

cd $2/chenum1

# Create project to import to
msg=`$1 create project -p mypkg to`
if ! test -d "$2/chenum1/to/BOCCA"; then
	echo "missing to/BOCCA"
	echo "FAIL"
	exit 1
fi
cd to

# Patch target (to)
echo "Patching target project"
# Patch port makefiles
patch ports/make.rules.user $topdir/patches/makefiles/port/make.rules.user.target.patch
if ! test "x$?" = "x0"; then
    echo "Patching ports/make.rules.user from ${topdir}/patches/makefiles/port/make.rules.user.target.patch failed"
    echo "FAIL"
    exit 1
fi
patch ports/make.vars.user ${topdir}/patches/makefiles/port/make.vars.user.target.patch
if ! test "x$?" = "x0"; then
    echo "Patching ports/make.vars.user from $topdir/patches/makefiles/port/make.vars.user.target.patch failed"
    echo "FAIL"
    exit 1
fi

# Patch class makefiles
patch components/make.rules.user $topdir/patches/makefiles/components/make.rules.user.target.patch
if ! test "x$?" = "x0"; then
    echo "Patching components/make.rules.user from${topdir}/patches/makefiles/components/make.rules.user.target.patch failed"
    echo "FAIL"
    exit 1
fi
patch components/make.vars.user ${topdir}/patches/makefiles/components/make.vars.user.target.patch
if ! test "x$?" = "x0"; then
    echo "Patching components/make.vars.user from ${topdir}/patches/makefiles/components/make.vars.user.target.patch failed"
    echo "FAIL"
    exit 1
fi

# TODO: Multiple --import-sidls in the same command do NOT work.  There is not a bug created for this
# since the bug tracker is down... but we should check each individual merge anyway.

# Import from/port/sidl/mypkg.iface.sidl
$1 create enum foobar --import-sidl=$2/chenum1/from/ports/sidl/mypkg.iface.sidl
if ! test "x$?" = "x0"; then
    echo "Failed to import sidl from $2/chenum1/from/ports/sidl/mypkg.iface.sidl"
    echo "FAIL"
    exit 1
fi


cat << EOF > splice
        // DO-NOT-DELETE bocca.splicer.begin(mypkg.foobar.entries)
        one,
        two,
        three
        // DO-NOT-DELETE bocca.splicer.end(mypkg.foobar.entries)
EOF
$1-merge -A 'DO-NOT-DELETE bocca.splicer' -B 'DO-NOT-DELETE bocca.splicer' --from=splice --to=ports/sidl/mypkg.foobar.sidl
if ! test "x$?" = "x0" ; then
  echo "merge failed"
  echo "FAIL"
  exit 1
fi


./configure
make clean all

if ! test "x$?" = "x0"; then
    echo "Make failed"
    echo "FAIL"
    exit 1
fi

echo "Make succeeded: Check output manually for confirmation of correct build orders."

echo "PASS"
exit 0
