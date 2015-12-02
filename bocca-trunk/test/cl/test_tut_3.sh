#!/bin/sh
# test tutorial transfer old to new literal version
# CCA_TUTORIAL_ROOT needs to point to a directory containing
#  misc-handouts  ppt-template  src           for the tutorial
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
TDIR=bocca
rm -rf $TDIR
mkdir $TDIR
cd $TDIR
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $TDIR failed"	
	echo "BROKEN"
	exit 1
fi
export BOCCA=$1
bindir=`dirname $1`
export PATH=$bindir:"$PATH"
export TUTORIAL_HOME=$CCA_TUTORIAL_ROOT
msg=`$CCA_TUTORIAL_ROOT/hands-on/bocca/do-hog/do-bocca-hog`
if ! test -d "bocca/myProject"; then
	echo "missing myProject"
	echo "FAIL"
	exit 1
fi
echo "PASS"
