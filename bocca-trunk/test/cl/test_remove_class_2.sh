#!/bin/bash
# derive from boyana's test script.
# TODO: add checks for expected outputs, currently only return values checked.
source util.sh

TDIR=rmClass2

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

create "class" "myproj.ClassToRemove" 

create "class" "myproj.SomeClass" "--requires=ClassToRemove" 
merge "class" "myproj.SomeClass" "void foo(in myproj.ClassToRemove x);"

checkCmd "FAIL" "$BOCCA remove SomeClass" "could not remove class" "!components/sidl/myproj.SomeClass.sidl !components/myproj.SomeClass/myproj_SomeClass_Impl.hxx !components/myproj.SomeClass/myproj_SomeClass_Impl.cxx"

checkCmd "FAIL" "$BOCCA display project" "could not display project"

checkCmd "FAIL" "./configure" "could not configure project" "utils/config-data"

checkCmd "FAIL" "make" "could not build project" 

echo "PASS"
exit 0
