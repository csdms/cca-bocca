#!/bin/bash
# Test an external uses port with multiple sidl files, using the real Performance.sidl 
# file split into two parts (version 1.7.2)
# TODO: add checks for expected outputs, currently only return values checked.

source util.sh

topProjDir="ext2"
cd $2
if [ ! -d $topProjDir ]; then mkdir $topProjDir; fi

export BOCCA=$1
export BOCCATEST=`pwd`/$topProjDir

createExtFiles() {
    # Create the external sidl
    mkdir $BOCCATEST/externaldir

cat <<EOF > $BOCCATEST/externaldir/lisi.sidl
package lisibase version 0.0
{
	enum SparseStruct
	{
		CSR,	
		COO,
		MSR,
		VBR,
		FEM,
	}


  interface Matrix {
	int setRow(in rarray<double,1> Row(NumLocalRow),
		   in int NumLocalRow);
	}

  interface SparseSolver {

	int initialize(in long comm);

  int setBlockSize(in int bs);	

	/**
	* Assume that block row partitioning
	*/
	int setStartRow(in int startrow);
	int setLocalRows(in int rows);
	int setLocalNNZ(in int nnz);
	int setGlobalCols(in int cols);
  int setOffset(in int offset);
	
	int setupMatrix[few_args](in rarray<double,1> Values(NNZ),
                    in rarray<int,1> Rows(NNZ),
                    in rarray<int,1> Columns(NNZ),
                    in int NNZ);
	
	int setupMatrix[media_args](in rarray<double,1> Values(NNZ),
                    in rarray<int,1> Rows(RowsLength),
                    in rarray<int,1> Columns(NNZ),
                    in SparseStruct DataStruct,
                    in int RowsLength,
                    in int NNZ);
	
	int setupRHS(in rarray<double,1> RightHandSide(NumLocalRow),
		        in int NumLocalRow);
                
	int solve(inout rarray<double,1> Solution(NumLocalRow), 
			    inout rarray<double,1> Status(StatusLength),
			    in int NumLocalRow,
			    in int StatusLength);


	int set(in string key, in string value);
	int setInt(in string key, in int value);
	int setBool(in string key, in bool value);
	int setDouble(in string key, in double value);

	string get_all();

	}

}
EOF

}

# First project
pdir=lisi
prefix=$BOCCATEST/installtest
cd $BOCCATEST && /bin/rm -rf *

createExtFiles

checkCmd "FAIL" "$BOCCA create project $pdir" "could not create a project" "$pdir/make.project"

checkCmd "BROKEN" "cd $BOCCATEST/$pdir" "could not cd to $BOCCATEST/$pdir"
cd $BOCCATEST/$pdir

checkCmd "FAIL" "$BOCCA create port Solver --extends=lisibase.SparseSolver@$BOCCATEST/externaldir/lisi.sidl" "could not create Solver port" "ports/sidl/lisi.Solver.sidl"

checkCmd "FAIL" "$BOCCA create component MultiLevel --provides=Solver@fine --uses=Solver@coarse" "could not create lisi.MultiLevel" "components/sidl/lisi.MultiLevel.sidl"

checkCmd "FAIL" "./configure --prefix=$prefix" "could not configure project" "make.project utils/$pdir-config"

checkCmd "FAIL" "make" "could not build project" "install/share/cca/lisi.MultiLevel.cca"

checkCmd "FAIL" "make check" "could not instantiate built components" 

checkCmd "FAIL" "make install" "could not install component" "$prefix/share/cca/lisi.MultiLevel.cca $prefix/lib/liblisi.MultiLevel.la $prefix/bin/$pdir-config $prefix/lib/$pdir.config-data"

checkCmd "FAIL" "make install-check" "install-check did not succeed" 

echo "PASS"
exit 0
