#!/bin/bash
# derive from boyana's test script.
# TODO: add checks for expected outputs, currently only return values checked.
source util.sh

cd $2
if [ ! -d renameEnumTest ]; then mkdir renameEnumTest; fi

export BOCCA=$1
export BMERGE=$1-merge
export BOCCATEST=`pwd`/renameEnumTest

# First project
cd $BOCCATEST && /bin/rm -rf *
checkCmd "FAIL" "$BOCCA create project testEnum" "could not create a project" "testEnum/make.project"

checkCmd "BROKEN" "cd $BOCCATEST/testEnum" "could not cd to $BOCCATEST/testEnum"
cd $BOCCATEST/testEnum

checkCmd "FAIL" "$BOCCA create enum mypkg.test.SomeEnum" "could not create an enum" "ports/sidl/mypkg.test.SomeEnum.sidl"

cat << EOF > splice
        // DO-NOT-DELETE bocca.splicer.begin(mypkg.test.SomeEnum.entries)
        one,
        two,
        three
        // DO-NOT-DELETE bocca.splicer.end(mypkg.test.SomeEnum.entries)
EOF
$BMERGE -A 'DO-NOT-DELETE bocca.splicer' -B 'DO-NOT-DELETE bocca.splicer' --from=splice --to=ports/sidl/mypkg.test.SomeEnum.sidl
if ! test "x$?" = "x0" ; then
  echo "merge failed"
  echo "FAIL"
  exit 1
fi

checkCmd "FAIL" "$BOCCA create interface mypkg.test.SomeInterface --requires=mypkg.test.SomeEnum" "could not create an interface" "ports/sidl/mypkg.test.SomeInterface.sidl"

cat << EOF > splice
        // DO-NOT-DELETE bocca.splicer.begin(mypkg.test.SomeInterface.methods)
        void doSomething(in mypkg.test.SomeEnum enumArg);
        // DO-NOT-DELETE bocca.splicer.end(mypkg.test.SomeInterface.methods)
EOF
$BMERGE -A 'DO-NOT-DELETE bocca.splicer' -B 'DO-NOT-DELETE bocca.splicer' --from=splice --to=ports/sidl/mypkg.test.SomeInterface.sidl
if ! test "x$?" = "x0" ; then
  echo "merge failed"
  echo "FAIL"
  exit 1
fi

checkCmd "FAIL" "$BOCCA create component  mypkg.test.someComponent --implements=mypkg.test.SomeInterface" "could not create a component" "components/sidl/mypkg.test.someComponent.sidl"

checkCmd "FAIL" "$BOCCA create component mypkg.test.someOtherComponent --requires=mypkg.test.SomeEnum" "could not create a component" "components/sidl/mypkg.test.someOtherComponent.sidl"

cat << EOF > splice
        // DO-NOT-DELETE bocca.splicer.begin(mypkg.test.someOtherComponent.methods)
        void doSomethingElse(in mypkg.test.SomeEnum enumArg);
        // DO-NOT-DELETE bocca.splicer.end(mypkg.test.someOtherComponent.methods)
EOF
$BMERGE -A 'DO-NOT-DELETE bocca.splicer' -B 'DO-NOT-DELETE bocca.splicer' --from=splice --to=ports/sidl/mypkg.test.SomeInterface.sidl
if ! test "x$?" = "x0" ; then
  echo "merge failed"
  echo "FAIL"
  exit 1
fi

checkCmd "FAIL" "$BOCCA rename enum mypkg.test.SomeEnum mypkg.test.SomeNewEnum" "could not rename an enum" "ports/sidl/mypkg.test.SomeNewEnum.sidl"

checkCmd "FAIL" "$BOCCA display project" "could not display project"

checkCmd "FAIL" "./configure" "could not configure project" "utils/config-data"

checkCmd "FAIL" "make" "could not build project" "install/share/cca/mypkg.test.someComponent.cca install/share/cca/mypkg.test.someOtherComponent.cca "

checkCmd "FAIL" "make check" "could not instantiate components" 

echo "PASS"
exit 0
