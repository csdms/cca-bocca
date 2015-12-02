#!/bin/sh
# CCA_TUTORIAL_ROOT needs to point to a directory containing
# omake, smake, emake
# and BOCCA needs to point to the bocca executable if not in 
# path by default.
# This script operates on a *copy* of the tutorial tree,
# which can take some time to make if it's full of junk.
# It's likely the makfile doesn't report all errors correctly on this one.
if test "x$CCA_TOOLS_ROOT" = "x"; then
  echo "XFAIL: no CCA_TOOLS_ROOT defined."
  exit 1
fi
if test "x$CCA_TUTORIAL_ROOT" = "x"; then
  echo "XFAIL: no CCA_TUTORIAL_ROOT defined."
  exit 1
fi
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
TDIR=tut1
rm -rf $TDIR
mkdir $TDIR
cd $TDIR
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $TDIR failed"	
	echo "BROKEN"
	exit 1
fi

export BOCCA=$1
morepath=`dirname $BOCCA`
export PATH="$morepath:$PATH"
if ! test -d $CCA_TUTORIAL_ROOT; then
	echo "CCA_TUTORIAL_ROOT set but does not point to a directory"
	echo "FAIL"
	exit 1
fi
if ! test -d $CCA_TUTORIAL_ROOT/src-ex; then
	echo "CCA_TUTORIAL_ROOT but does not contain expected source code"
	echo "FAIL"
	exit 1
fi
msg=`cp -a $CCA_TUTORIAL_ROOT .`
rm -rf .firstpassok
cd *
export CCA_TUTORIAL_ROOT=`pwd`
export TUTORIAL_HOME=$CCA_TUTORIAL_ROOT

./omake clean all
x=$?
if ! test "x$x" = "x0"; then
	echo "make failed for ode tutorial"
	echo "FAIL"
	exit 1
fi

./emake clean all
x=$?
if ! test "x$x" = "x0"; then
	echo "make failed for ex tutorial"
	echo "FAIL"
	exit 1
fi

./emake check
x=$?
if ! test "x$x" = "x0"; then
	echo "make check failed for ex tutorial"
	echo "FAIL"
	exit 1
fi

./smake clean all
x=$?
if ! test "x$x" = "x0"; then
	echo "make failed for pde tutorial"
	echo "FAIL"
	exit 1
fi

if test "x$out" = "x0"; then
	echo "PASS"
	cd ..
	touch .firstpassok
fi
exit $out
