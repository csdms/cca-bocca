#!/bin/bash

# Try to determine the number of CPUs or cores for various systems; this is incomplete, 
# so the default is 1

system=`uname`
cputype=`uname -m`
ncores=1

if [ "x$cputype" = "xi386" -o "x$cputype" = "xi586" -o "x$cputype" = "xi686" \
   -o "x$cputype" = "xx86_64" ] ; then 
  if [ "x$system" = "xLinux" ] ; then 
    if [ -e "/proc/cpuinfo" ] ; then
      ncores=`grep "^processor" /proc/cpuinfo | wc -l`
    fi
  elif [ "x$system" = "xDarwin" ] ; then
    ncores=`system_profiler  -detailLevel mini | grep "Number Of Cores" | sed -e 's/Number Of Cores: //'`
  fi
fi  

echo $ncores
