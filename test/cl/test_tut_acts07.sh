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
TDIR=tutacts07
rm -rf $TDIR
mkdir $TDIR
cd $TDIR
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $TDIR failed"	
	echo "BROKEN"
	exit 1
fi
export BOCCA=$1
msg=`$CCA_TUTORIAL_ROOT/bin/gen-bocca-fid`
if ! test -d "src-acts07"; then
	echo "missing src-acts07"
	echo "FAIL"
	exit 1
fi
patch -p0 << EOF
--- src-acts07/components/drivers.F90Driver/drivers_F90Driver_Impl.F90.x	2007-08-20 16:04:22.000000000 -0700
+++ src-acts07/components/drivers.F90Driver/drivers_F90Driver_Impl.F90	2007-08-20 16:07:49.000000000 -0700
@@ -67,13 +67,6 @@
 ! Bocca generated code. bocca.protected.end(drivers.F90Driver:ctor)
 ! Insert the implementation here...
 
-  ! Access private data
-  type(drivers_F90Driver_wrap) :: dp
-  ! Allocate memory and initialize
-  allocate(dp%d_private_data)
-  call set_null(dp%d_private_data%frameworkServices)
-  call drivers_F90Driver__set_data_m(self, dp)
-
 ! DO-NOT-DELETE splicer.end(drivers.F90Driver._ctor)
 end subroutine drivers_F90Driver__ctor_mi

EOF 
exit 0
patch -p0 << EOF
--- src-acts07/components/integrators.MonteCarlo/integrators_MonteCarlo_Impl.F90.x	2007-08-20 16:03:50.000000000 -0700
+++ src-acts07/components/integrators.MonteCarlo/integrators_MonteCarlo_Impl.F90	2007-08-20 16:10:00.000000000 -0700
@@ -72,12 +72,6 @@
 ! Bocca generated code. bocca.protected.end(integrators.MonteCarlo:ctor)
 ! Insert the implementation here...
 
-  ! Access private data
-  type(integrators_MonteCarlo_wrap) :: dp
-  ! Allocate memory and initialize
-  allocate(dp%d_private_data)
-  call set_null(dp%d_private_data%frameworkServices)
-  call integrators_MonteCarlo__set_data_m(self, dp)
 
 ! DO-NOT-DELETE splicer.end(integrators.MonteCarlo._ctor)
 end subroutine integrators_MonteCarlo__ctor_mi

EOF
cd src-acts07
if test "x$TESTMAKE" = "x"; then
	:
else
  make
fi
x=$?
if ! test "x$x" = "x0"; then
	echo "make failed for tutorial"
	echo "FAIL"
	out=1
fi
if test "x$out" = "x0"; then
	echo "PASS"
fi
exit $out
