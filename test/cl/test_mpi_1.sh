#!/bin/sh
# test simplest mpi component creation.
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf mpi1
mkdir mpi1
cd mpi1

#ymmv
if test "x$MPI_PREFIX" = "x"; then
	echo "Assuming Ben's mpi, which is probably a bad idea."
	MPI_PREFIX=/home/baallan/mpi/pgi/om123
fi
MPIINCDIR="$MPI_PREFIX/include"
MPIINC="-I$MPIINCDIR"
MPILIB="$MPI_PREFIX/lib"
if ! test -d $MPIINCDIR; then
	echo "XFAIL: need to define your MPI_PREFIX for this test script."
	exit 1
fi
msg=`$1 create project mpitest`
if ! test -d "$2/mpi1/mpitest/BOCCA"; then
	echo "missing mpi1/mpitest/BOCCA"
	echo "FAIL"
	exit 1
fi
cd mpitest
./configure --prefix=/tmp/mpitest2
CCAFECONFIG=`$1 config --query-var=ccafe_config | grep -v '^#'`
echo CCAFECONFIG=$CCAFECONFIG
CCAFESIDL="`$CCAFECONFIG --var CCAFE_pkgdatadir`/ccafe.sidl"
echo CCAFESIDL=$CCAFESIDL
CCAFEINCL="`$CCAFECONFIG --var CCAFE_pkgincludedir`/dc/babel.new/babel-cca/server"
CCAFEINCL2="`$CCAFECONFIG --var CCAFE_pkgincludedir`/util"
BMERGE=$1-merge

msg=`$1 create port x`
if ! test -f ports/sidl/mpitest.x.sidl; then
	echo "missing mpitest/ports/sidl/mpitest.x.sidl"
	echo "FAIL"
	exit 1
fi
echo "TRYING"
$1 create component cxx -l cxx --provides=mpitest.x@myx --uses=mpitest.x@yourx --uses=ccaffeine.ports.MPIService@MPIService@$CCAFESIDL --go=GO
if ! test -f components/sidl/mpitest.cxx.sidl; then
	echo "missing mpitest/components/sidl/mpitest.cxx.sidl"
	echo "FAIL"
	exit 1
fi
echo "INCLUDES=-I$CCAFEINCL -I$CCAFEINCL2 $MPIINC">> components/mpitest.cxx/make.vars.user
usingmpich=`ls $MPILIB/libmpich* | wc -l`
if test "$usingmpich" != "0"; then
	echo "LIBS=-R$MPILIB -L$MPILIB -lmpi -lmpichcxx">> components/mpitest.cxx/make.vars.user
else
	echo "LIBS=-R$MPILIB -L$MPILIB -lmpi -lmpi_cxx">> components/mpitest.cxx/make.vars.user
fi
if ! test "x$?" = "x0"; then
	echo "problem configuring mpitest/"
	echo "FAIL"
	exit 1
fi
echo "COMPILING Component ======================"
# Babel >= 1.2 renames the includes splicer to hincludes
cat << EOH >> fred.hxx.splice
//_includes 
  // DO-NOT-DELETE splicer.begin(mpitest.cxx._includes)
#include "noSeekMPI.h"
#include <mpi.h> // or use the c++ header for your mpi if available.
  // DO-NOT-DELETE splicer.end(mpitest.cxx._includes)

//_hincludes 
  // DO-NOT-DELETE splicer.begin(mpitest.cxx._hincludes)
#include "noSeekMPI.h"
#include <mpi.h> // or use the c++ header for your mpi if available.
  // DO-NOT-DELETE splicer.end(mpitest.cxx._hincludes)

//_implementation
    // DO-NOT-DELETE splicer.begin(mpitest.cxx._implementation)
    ::ccaffeine::ports::MPIService mpiService;
    int64_t commSIDL; 
    MPI_Comm commC; 
   // Bocca generated code. bocca.protected.begin(mpitest.cxx._implementation)
    gov::cca::Services    d_services;
   // Bocca generated code. bocca.protected.end(mpitest.cxx._implementation)

    // DO-NOT-DELETE splicer.end(mpitest.cxx._implementation)
EOH

cat << EOC >> fred.cxx.splice
// _includes
   // DO-NOT-DELETE splicer.begin(mpitest.cxx._includes)
#include "noSeekMPI.h" // destroy the SEEK macros from mpi2
#include <iostream> // note: this is probably a dumb thing to do in a real mpi code
   // Bocca generated code. bocca.protected.begin(mpitest.cxx._includes)

// If -D_BOCCA_STDERR is given to the compiler, diagnostics print to stderr.
// In production use, probably want not to use -D_BOCCA_STDERR.
#ifdef _BOCCA_STDERR
#include <iostream>
#endif // _BOCCA_STDERR

// If -D_BOCCA_BOOST is given to the compiler, exceptions and diagnostics will
// include function names for boost-understood compilers.
// If boost is not available (and therefore ccaffeine is not in use),
// -D_BOCCA_BOOST can be omitted and function names will not be included in messages.
#ifndef _BOCCA_BOOST
#define BOOST_CURRENT_FUNCTION ""
#else
#include <boost/current_function.hpp>
#endif

// This is intended to simplify exception throwing as SIDL_THROW does for C.
// Unfortunately there is no SIDL_THROW_CXX in babel yet.
#define BOCCA_THROW_CXX(EX_CLS, MSG) {     EX_CLS ex = EX_CLS::_create();     ex.setNote( MSG );     ex.add(__FILE__, __LINE__, BOOST_CURRENT_FUNCTION);     throw ex; }

// This simplifies exception extending and rethrowing in c++, like SIDL_CHECK in C.
// EX_OBJ must be the caught exception and is extended with msg and file/line/func added.
// Continuing the throw is up to the user.
#define BOCCA_EXTEND_THROW_CXX(EX_OBJ, MSG, LINEOFFSET) {   std::string msg = std::string(MSG) + std::string(BOOST_CURRENT_FUNCTION);   EX_OBJ.add(__FILE__,__LINE__ + LINEOFFSET, msg); }


   // Bocca generated code. bocca.protected.end(mpitest.cxx._includes)


   // DO-NOT-DELETE splicer.end(mpitest.cxx._includes)

// _go:
   // DO-NOT-DELETE splicer.begin(mpitest.cxx.go)
  int rank=-1, size=-1; 

  ::gov::cca::Port        gp;

  if (mpiService._not_nil()) {
# if 0 // still need to define the port elseswhere in the test.
    // get the port ...
    ::parallel::MPICommUser cu; 
    gp = d_services.getPort("CommUser"); 
    cu = ::babel_cast< ::parallel::MPICommUser >(gp);
  
    if(cu._is_nil()) { 
      std::cerr << "pdrivers.CXXDriverMPI not connected to a MPICommUser" << std::endl;
    } else {
      // set the communicator on another component that needs it for real work.
      cu.setComm(commSIDL); 
      d_services.releasePort("CommUser");  
    }
#endif
    int err = MPI_Comm_rank(commC,&rank);
    if (err != MPI_SUCCESS) {
      return -2; // we're really hosed if we can't get rank.
    }
    err = MPI_Comm_size(commC,&size);
    if (err != MPI_SUCCESS) {
      return -2; // we're really hosed if we can't get size.
    }
 
    std::cout <<"Comm rank = " << rank << " of " << size << std::endl;
    return 0; 
  } else {
    std::cerr << "MPI component not connected to MPIService." << std::endl;
    return -1;
  }
   // DO-NOT-DELETE splicer.end(mpitest.cxx.go)

//_setServices:
   // DO-NOT-DELETE splicer.begin(mpitest.cxx.setServices)
  boccaSetServices(services);
  ::gov::cca::Port ms;
  ms = d_services.getPort("MPIService");
  if (ms._is_nil()) { 
    commSIDL = 0;
    commC = MPI_COMM_NULL;
    std::cerr << "MPI component in a framework not providing MPIService." << std::endl;
  } else {
    mpiService = ::babel_cast< ::ccaffeine::ports::MPIService >(ms); // BABEL CAST operation.
    commSIDL = mpiService.getComm();
    MPI_Fint commF = (MPI_Fint)commSIDL;
    commC = MPI_Comm_f2c(commF);
  }
   // DO-NOT-DELETE splicer.end(mpitest.cxx.setServices)

//_releaseServices:
   // DO-NOT-DELETE splicer.begin(mpitest.cxx.releaseServices)
  mpiService.releaseComm(commSIDL);
  commC = MPI_COMM_NULL;
  commSIDL = 0;
  if (mpiService._not_nil()) {
    d_services.releasePort("MPI");
  }
  mpiService = 0; 
  boccaReleaseServices(services);
   // DO-NOT-DELETE splicer.end(mpitest.cxx.releaseServices)
EOC
$BMERGE --from fred.hxx.splice --to components/mpitest.cxx/mpitest_cxx_Impl.hxx
$BMERGE --from fred.cxx.splice --to components/mpitest.cxx/mpitest_cxx_Impl.cxx
make
x=$?
if test "x$x" = "x0"; then
	:
else
	echo "problem compiling mpitest/components/mpitest.cxx/"
	echo "FAIL"
	exit 1
fi
echo "CHECKING install ========== "
make install
if ! test "x$?" = "x0"; then
	echo "problem with make install for mpitest/"
	echo "FAIL"
	exit 1
fi

echo "CHECKING Component ========================"
export CCAFE_USE_MPI=1
export SIDL_DEBUG_DLOPEN=1
make check
if ! test "x$?" = "x0"; then
	echo "problem with make check for mpitest/"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
