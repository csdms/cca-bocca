// 
// File:          pytest_cxx_Impl.cxx
// Symbol:        pytest.cxx-v0.0
// Symbol Type:   class
// Babel Version: 1.0.6
// Description:   Server-side implementation for pytest.cxx
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 
#include "pytest_cxx_Impl.hxx"

// 
// Includes for all method dependencies.
// 
#ifndef included_gov_cca_CCAException_hxx
#include "gov_cca_CCAException.hxx"
#endif
#ifndef included_gov_cca_Services_hxx
#include "gov_cca_Services.hxx"
#endif
#ifndef included_pytest_x_hxx
#include "pytest_x.hxx"
#endif
#ifndef included_sidl_BaseInterface_hxx
#include "sidl_BaseInterface.hxx"
#endif
#ifndef included_sidl_ClassInfo_hxx
#include "sidl_ClassInfo.hxx"
#endif
#ifndef included_sidl_RuntimeException_hxx
#include "sidl_RuntimeException.hxx"
#endif
#ifndef included_sidl_NotImplementedException_hxx
#include "sidl_NotImplementedException.hxx"
#endif
   // DO-NOT-DELETE splicer.begin(pytest.cxx._includes)


   // Bocca generated code. bocca.protected.begin(pytest.cxx._includes)

#define _BOCCA_CTOR_MESSAGES 0
// If -D_BOCCA_STDERR is given to the compiler, diagnostics print to stderr.
// In production use, probably want not to use -D_BOCCA_STDERR.
#ifdef _BOCCA_STDERR
#include <iostream>
#ifdef _BOCCA_CTOR_PRINT
#undef _BOCCA_CTOR_MESSAGES
#define _BOCCA_CTOR_MESSAGES 1
#endif /* _BOCCA_CTOR_PRINT */
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


   // Bocca generated code. bocca.protected.end(pytest.cxx._includes)


   // DO-NOT-DELETE splicer.end(pytest.cxx._includes)

// speical constructor, used for data wrapping(required).  Do not put code here unless you really know what you're doing!
pytest::cxx_impl::cxx_impl() : StubBase(reinterpret_cast< void*>(
  ::pytest::cxx::_wrapObj(reinterpret_cast< void*>(this))),false) , _wrapped(
  true){ 
  // DO-NOT-DELETE splicer.begin(pytest.cxx._ctor2)
  // Insert-Code-Here {pytest.cxx._ctor2} (ctor2)
  // DO-NOT-DELETE splicer.end(pytest.cxx._ctor2)
}

// user defined constructor
void pytest::cxx_impl::_ctor() {
  /* DO-NOT-DELETE splicer.begin(pytest.cxx._ctor) */
    
  /* bocca-default-code. User may edit or delete.begin(pytest.cxx._ctor) */
   #if _BOCCA_CTOR_MESSAGES
     std::cerr << "CTOR pytest.cxx: " << BOOST_CURRENT_FUNCTION << " constructing " << this << std::endl;
   #endif /* _BOCCA_CTOR_MESSAGES */
  /* bocca-default-code. User may edit or delete.end(pytest.cxx._ctor) */

  /* Insert-UserCode-Here {pytest.cxx._ctor} (constructor method) */

  /* DO-NOT-DELETE splicer.end(pytest.cxx._ctor) */
}

// user defined destructor
void pytest::cxx_impl::_dtor() {
  /* DO-NOT-DELETE splicer.begin(pytest.cxx._dtor) */
  /* Insert-UserCode-Here {pytest.cxx._dtor} (destructor method) */
    
  /* bocca-default-code. User may edit or delete.begin(pytest.cxx._dtor) */
   #if _BOCCA_CTOR_MESSAGES
     std::cerr << "DTOR pytest.cxx: " << BOOST_CURRENT_FUNCTION << " destructing " << this << std::endl;
   #endif /* _BOCCA_CTOR_MESSAGES */
  /* bocca-default-code. User may edit or delete.end(pytest.cxx._dtor) */

  /* DO-NOT-DELETE splicer.end(pytest.cxx._dtor) */
}

// static class initializer
void pytest::cxx_impl::_load() {
  // DO-NOT-DELETE splicer.begin(pytest.cxx._load)
  // Insert-Code-Here {pytest.cxx._load} (class initialization)
  // DO-NOT-DELETE splicer.end(pytest.cxx._load)
}

// user defined static methods: (none)

// user defined non-static methods:
/**
 * Method:  boccaSetServices[]
 */
void
pytest::cxx_impl::boccaSetServices_impl (
  /* in */::gov::cca::Services services ) 
// throws:
//     ::gov::cca::CCAException
//     ::sidl::RuntimeException
{
// DO-NOT-DELETE splicer.begin(pytest.cxx.boccaSetServices)
// Bocca generated code. bocca.protected.begin(pytest.cxx.boccaSetServices)

   gov::cca::TypeMap typeMap;
   gov::cca::Port    port;

   d_services = services;

   typeMap = d_services.createTypeMap();

   port = ::babel_cast< gov::cca::Port>(*this);
   if (port._is_nil()) {
      BOCCA_THROW_CXX( ::sidl::SIDLException , "pytest.cxx: Error casting self to gov::cca::Port");
   } 


  // Provide a pytest.x port with port name MYX 
   try{
      d_services.addProvidesPort(port,
					"MYX",
					"pytest.x",
					typeMap);
   } catch ( ::gov::cca::CCAException ex )  {
      BOCCA_EXTEND_THROW_CXX(ex, "pytest.cxx: Error calling addProvidesPort(port,\"MYX\", \"pytest.x\", typeMap) ", -2);
      throw;
   }    

  // Use a pytest.x port with port name YOURX 
   try{
      d_services.registerUsesPort("YOURX",
                                         "pytest.x",
                                         typeMap);
   } catch ( ::gov::cca::CCAException ex )  {
      BOCCA_EXTEND_THROW_CXX(ex,"pytest.cxx: Error calling registerUsesPort(\"YOURX\", \"pytest.x\", typeMap) ", -2);
      throw;
   }


   gov::cca::ComponentRelease cr = ::babel_cast< gov::cca::ComponentRelease>(*this);
   d_services.registerForRelease(cr);
   return;
// Bocca generated code. bocca.protected.end(pytest.cxx.boccaSetServices)
    
// DO-NOT-DELETE splicer.end(pytest.cxx.boccaSetServices)
}

/**
 * Method:  boccaReleaseServices[]
 */
void
pytest::cxx_impl::boccaReleaseServices_impl (
  /* in */::gov::cca::Services services ) 
// throws:
//     ::gov::cca::CCAException
//     ::sidl::RuntimeException
{
  // DO-NOT-DELETE splicer.begin(pytest.cxx.boccaReleaseServices)
  // Bocca generated code. bocca.protected.begin(pytest.cxx.boccaReleaseServices)
   d_services=0;


  // Un-provide pytest.x port with port name MYX 
  try{
    services.removeProvidesPort("MYX");
  } catch ( ::gov::cca::CCAException ex )  {
#ifdef _BOCCA_STDERR
    std::cerr << "pytest.cxx: Error calling removeProvidesPort(\"MYX\") at " 
              << __FILE__ << ": " << __LINE__ -4 << ": " << ex.getNote() << std::endl;
#endif // _BOCCA_STDERR
  }

  // Release pytest.x port with port name YOURX 
  try{
    services.unregisterUsesPort("YOURX");
  } catch ( ::gov::cca::CCAException ex )  {
#ifdef _BOCCA_STDERR
    std::cerr << "pytest.cxx: Error calling unregisterUsesPort(\"YOURX\") at " 
              << __FILE__ << ":" << __LINE__ -4 << ": " << ex.getNote() << std::endl;
#endif // _BOCCA_STDERR
  }

   return;
  // Bocca generated code. bocca.protected.end(pytest.cxx.boccaReleaseServices)
    
  // DO-NOT-DELETE splicer.end(pytest.cxx.boccaReleaseServices)
}

/**
 * Method:  boccaForceUsePortInclude[]
 */
void
pytest::cxx_impl::boccaForceUsePortInclude_impl (
  /* in */::pytest::x dummy0 ) 
{
  // DO-NOT-DELETE splicer.begin(pytest.cxx.boccaForceUsePortInclude)
  // Bocca generated code. bocca.protected.begin(pytest.cxx.boccaForceUsePortInclude)
    (void)dummy0;

  // Bocca generated code. bocca.protected.end(pytest.cxx.boccaForceUsePortInclude)
  // DO-NOT-DELETE splicer.end(pytest.cxx.boccaForceUsePortInclude)
}

/**
 *  Starts up a component presence in the calling framework.
 * @param services the component instance's handle on the framework world.
 * Contracts concerning Svc and setServices:
 * 
 * The component interaction with the CCA framework
 * and Ports begins on the call to setServices by the framework.
 * 
 * This function is called exactly once for each instance created
 * by the framework.
 * 
 * The argument Svc will never be nil/null.
 * 
 * Those uses ports which are automatically connected by the framework
 * (so-called service-ports) may be obtained via getPort during
 * setServices.
 */
void
pytest::cxx_impl::setServices_impl (
  /* in */::gov::cca::Services services ) 
// throws:
//     ::gov::cca::CCAException
//     ::sidl::RuntimeException
{
  // DO-NOT-DELETE splicer.begin(pytest.cxx.setServices)

  // bocca-default-code. User may edit or delete.begin(pytest.cxx.setServices)
     boccaSetServices(services); 
  // bocca-default-code. User may edit or delete.end(pytest.cxx.setServices)
  
  // DO-NOT-DELETE splicer.end(pytest.cxx.setServices)
}

/**
 * Shuts down a component presence in the calling framework.
 * @param services the component instance's handle on the framework world.
 * Contracts concerning Svc and setServices:
 * 
 * This function is called exactly once for each callback registered
 * through Services.
 * 
 * The argument Svc will never be nil/null.
 * The argument Svc will always be the same as that received in
 * setServices.
 * 
 * During this call the component should release any interfaces
 * acquired by getPort().
 * 
 * During this call the component should reset to nil any stored
 * reference to Svc.
 * 
 * After this call, the component instance will be removed from the
 * framework. If the component instance was created by the
 * framework, it will be destroyed, not recycled, The behavior of
 * any port references obtained from this component instance and
 * stored elsewhere becomes undefined.
 * 
 * Notes for the component implementor:
 * 1) The component writer may perform blocking activities
 * within releaseServices, such as waiting for remote computations
 * to shutdown.
 * 2) It is good practice during releaseServices for the component
 * writer to remove or unregister all the ports it defined.
 */
void
pytest::cxx_impl::releaseServices_impl (
  /* in */::gov::cca::Services services ) 
// throws:
//     ::gov::cca::CCAException
//     ::sidl::RuntimeException
{
  // DO-NOT-DELETE splicer.begin(pytest.cxx.releaseServices)


  // bocca-default-code. User may edit or delete.begin(pytest.cxx.releaseServices)
     boccaReleaseServices(services);
  // bocca-default-code. User may edit or delete.end(pytest.cxx.releaseServices)
    
  // DO-NOT-DELETE splicer.end(pytest.cxx.releaseServices)
}


// DO-NOT-DELETE splicer.begin(pytest.cxx._misc)
// Insert-Code-Here {pytest.cxx._misc} (miscellaneous code)
// DO-NOT-DELETE splicer.end(pytest.cxx._misc)

