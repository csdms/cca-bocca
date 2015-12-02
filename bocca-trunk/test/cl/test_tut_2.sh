#!/bin/sh
# test tutorial doc build
# and BOCCA needs to point to the bocca executable if not in 
# path by default.
# it's likely the makfile doesn't report error correctly on this one.
echo "ARGS= $*"
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
cd $TDIR
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $TDIR failed"	
	echo "BROKEN"
	exit 1
fi
if ! test -f .firstpassok; then
	echo "no tutorial build to gen docs for"
	echo "XFAIL"
	exit 1
fi
export BOCCA=$1
cd *
cd doc
make
x=$?
if ! test "x$x" = "x0"; then
	echo "make failed for tutorial doc"
	echo "FAIL"
	out=1
fi
if test "x$out" = "x0"; then
	echo "PASS"
fi
exit $out
