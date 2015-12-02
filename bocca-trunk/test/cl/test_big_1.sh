#!/bin/bash
# derive from boyana's test script.
# TODO: add checks for expected outputs, currently only return values checked.
source util.sh

cd $2
if [ ! -d big1 ]; then mkdir big1; fi

export BOCCA=$1
export BOCCATEST=`pwd`/big1

# First project
cd $BOCCATEST && /bin/rm -rf *
checkCmd "FAIL" "$BOCCA create project testproj1" "could not create a project" "testproj1/make.project"

checkCmd "BROKEN" "cd $BOCCATEST/testproj1" "could not cd to $BOCCATEST/testproj1"
cd $BOCCATEST/testproj1

checkCmd "FAIL" "$BOCCA create interface mypkg.test.SomeInterface" "could not create an interface" "ports/sidl/mypkg.test.SomeInterface.sidl"

checkCmd "FAIL" "$BOCCA create interface -e mypkg.test.SomeInterface mypkg.test.SomeOtherInterface" "could not create an interfaace extending another interface" "ports/sidl/mypkg.test.SomeOtherInterface.sidl"

checkCmd "FAIL" "$BOCCA create port MyPort" "could not create a port using short symbol name" "ports/sidl/testproj1.MyPort.sidl"

checkCmd "FAIL" "$BOCCA create port mypkg.test.APort" "could not create a port" "ports/sidl/mypkg.test.APort.sidl"

checkCmd "FAIL" "$BOCCA create port -e mypkg.test.SomeInterface -e mypkg.test.APort mypkg.test.AnotherPort" "could not create a port that extends an interface and a port" "ports/sidl/mypkg.test.AnotherPort.sidl"

checkCmd "FAIL" "$BOCCA create port -e mypkg.test.SomeOtherInterface -e mypkg.test.APort mypkg.test.ThirdPort" "could not create a port that extends an interface and a port" "ports/sidl/mypkg.test.ThirdPort.sidl"

checkCmd "FAIL" "$BOCCA remove interface SomeInterface" "could not remove interface" "!ports/sidl/mypkg.test.SomeInterface.sidl"

checkCmd "FAIL" "$BOCCA rename interface SomeOtherInterface NewInterface" "could not rename interface" "!ports/sidl/mypkg.test.SomeOtherInterface.sidl ports/sidl/mypkg.test.NewInterface.sidl"

checkCmd "FAIL" "$BOCCA create component -p mypkg.test.AnotherPort@AnotherPort -lcxx mypkg.test.AComponent" "could not create a component that provides a port" "components/sidl/mypkg.test.AComponent.sidl"

checkCmd "FAIL" "$BOCCA create component -u mypkg.test.APort@APort  -lc mypkg.test.AnotherComponent" "could not create a component that uses a port"  "components/sidl/mypkg.test.AnotherComponent.sidl"

checkCmd "FAIL" "$BOCCA create component -p mypkg.test.ThirdPort@ThirdPort -u mypkg.test.APort@APort mypkg.test.ThirdComponent" "could not create a component that uses and provides ports" "components/sidl/mypkg.test.ThirdComponent.sidl"

checkCmd "FAIL" "$BOCCA create component TransientComp" "components/sidl/testproj1.TransientComp.sidl"

checkCmd "FAIL" "$BOCCA rename component TransientComp PermanentComp" "could not rename component" "!components/sidl/testproj1.TransientComp.sidl components/sidl/testproj1.PermanentComp.sidl"

checkCmd "FAIL" "$BOCCA display project" "could not display project"

checkCmd "FAIL" "./configure" "could not configure project" "utils/config-data"

checkCmd "FAIL" "make" "could not build project" "install/share/cca/mypkg.test.AComponent.cca install/share/cca/mypkg.test.ThirdComponent.cca install/share/cca/mypkg.test.AnotherComponent.cca  install/share/cca/testproj1.PermanentComp.cca"

checkCmd "FAIL" "make check" "could not instantiate components" 

# Second project
checkCmd "BROKEN" "cd $BOCCATEST" "could not cd to $BOCCATEST"
cd $BOCCATEST
checkCmd "FAIL" "$BOCCA create project -p mypkg.test -lf90 testproj2" "could not create a project with specified package and language" "testproj2/make.project"

checkCmd "BROKEN" "cd $BOCCATEST/testproj2" "could not cd to $BOCCATEST/testproj2"
cd $BOCCATEST/testproj2
checkCmd "FAIL" "$BOCCA display project testproj2" "could not display specified project"

checkCmd "FAIL" "$BOCCA create port mypkg.test.SolverPort" "could not add a port" "ports/sidl/mypkg.test.SolverPort.sidl"
checkCmd "FAIL" "$BOCCA create component AComponent -p SolverPort" "could not add a component with default language" "components/sidl/mypkg.test.AComponent.sidl"
echo "PASS"
exit 0
