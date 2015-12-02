#!/bin/bash
# Test an external uses port with multiple sidl files, using the real Performance.sidl 
# file split into two parts (version 1.7.2)
# TODO: add checks for expected outputs, currently only return values checked.

source util.sh

topProjDir="rarray"
cd $2
if [ ! -d $topProjDir ]; then mkdir $topProjDir; fi

export BOCCA=$1
export BOCCATEST=`pwd`/$topProjDir

createExtFiles() {
    # Create the external sidl
    mkdir $BOCCATEST/externaldir

cat <<EOF > $BOCCATEST/externaldir/rar.sidl

package x  version 0.0 {
  /* This class does 
     something interesting 
  */
  class y {
        static void load1[Float](inout array<> a1, in rarray<float,1> values(m),
in int m);
        static void load2[Float](inout array<> a2, in rarray<float,2>
values(m,n), in int m, in int n);
        static void load3[Float](inout array<> a3,
                in rarray<float,3> values(m,n,p) ,
                in int m,
                in int n,
                in int p);
        static void load3(in rarray<float,7> values(m,n,p,p2,p3,p4,p5) , in int m, in int n, 
		in int p, in int p2, in int p3, in int p4, in int p5);
  }
}
EOF

}

# First project
pdir=rar
prefix=$BOCCATEST/installtest
cd $BOCCATEST && /bin/rm -rf *

createExtFiles

checkCmd "FAIL" "$BOCCA create project $pdir" "could not create a project" "$pdir/make.project"

checkCmd "BROKEN" "cd $BOCCATEST/$pdir" "could not cd to $BOCCATEST/$pdir"
cd $BOCCATEST/$pdir

checkCmd "FAIL" "$BOCCA create class NewClass --import-sidl=x.y@$BOCCATEST/externaldir/rar.sidl" "could not create NewClass with import from existing SIDL" "components/sidl/rar.NewClass.sidl"

checkCmd "FAIL" "./configure --prefix=$prefix" "could not configure project" "make.project utils/$pdir-config"

checkCmd "FAIL" "make" "could not build project" "install/share/cca/$pdir.NewClass.cca"

echo "PASS"
exit 0
