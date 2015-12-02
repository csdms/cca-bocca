#!/bin/bash
# derive from boyana's test script.
# TODO: add checks for expected outputs, currently only return values checked.
source util.sh

TDIR=rmComp1

cd $2
if [ ! -d $TDIR ]; then mkdir $TDIR; fi

export BOCCA=$1
export BMERGE=$1-merge
export BOCCATEST=`pwd`/$TDIR

# First project
cd $BOCCATEST && /bin/rm -rf *
checkCmd "FAIL" "$BOCCA create project myproj" "could not create a project" "myproj/make.project"

checkCmd "BROKEN" "cd $BOCCATEST/myproj" "could not cd to $BOCCATEST/myproj"
cd $BOCCATEST/myproj

create "port" "myproj.SomePort"
merge "port" "myproj.SomePort" "void foo();"

create "component" "myproj.SomeComp" "-p SomePort" 

checkCmd "FAIL" "$BOCCA remove SomeComp" "could not remove class" "!components/sidl/myproj.SomeComp.sidl !components/myproj.SomeComp/myproj_SomeComp_Impl.hxx !components/myproj.SomeComp/myproj_SomeComp_Impl.cxx"

checkCmd "FAIL" "$BOCCA display project" "could not display project"

checkCmd "FAIL" "./configure" "could not configure project" "utils/config-data"

checkCmd "FAIL" "make" "could not build project" 

echo "PASS"
exit 0
