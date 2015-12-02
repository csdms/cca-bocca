// 
// File:          pp_testX_Impl.hxx
// Symbol:        pp.testX-v0.0
// Symbol Type:   class
// Babel Version: 1.0.6
// Description:   Server-side implementation for pp.testX
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 

#ifndef included_pp_testX_Impl_hxx
#define included_pp_testX_Impl_hxx

#ifndef included_sidl_cxx_hxx
#include "sidl_cxx.hxx"
#endif
#ifndef included_pp_testX_IOR_h
#include "pp_testX_IOR.h"
#endif
#ifndef included_gov_cca_CCAException_hxx
#include "gov_cca_CCAException.hxx"
#endif
#ifndef included_gov_cca_Component_hxx
#include "gov_cca_Component.hxx"
#endif
#ifndef included_gov_cca_ComponentRelease_hxx
#include "gov_cca_ComponentRelease.hxx"
#endif
#ifndef included_gov_cca_Services_hxx
#include "gov_cca_Services.hxx"
#endif
#ifndef included_gov_cca_ports_GoPort_hxx
#include "gov_cca_ports_GoPort.hxx"
#endif
#ifndef included_gov_cca_ports_ParameterGetListener_hxx
#include "gov_cca_ports_ParameterGetListener.hxx"
#endif
#ifndef included_gov_cca_ports_ParameterSetListener_hxx
#include "gov_cca_ports_ParameterSetListener.hxx"
#endif
#ifndef included_pp_testX_hxx
#include "pp_testX.hxx"
#endif
#ifndef included_sidl_BaseClass_hxx
#include "sidl_BaseClass.hxx"
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


// DO-NOT-DELETE splicer.begin(pp.testX._includes)
// Insert-Code-Here {pp.testX._includes} (includes or arbitrary code)

#include "gov_cca_ports_ParameterPortFactory.hxx"
#include "gov_cca_ports_ParameterPort.hxx"
#include "gov_cca_ports_GoPort.hxx"
//#include "util/IO.h"
#include <vector>
//#include "gov_cca.hxx"

// DO-NOT-DELETE splicer.end(pp.testX._includes)

namespace pp { 

  /**
   * Symbol "pp.testX" (version 0.0)
   */
  class testX_impl : public virtual ::pp::testX 
  // DO-NOT-DELETE splicer.begin(pp.testX._inherits)
  // Insert-Code-Here {pp.testX._inherits} (optional inheritance here)
  // Put additional inheritance here...
  // DO-NOT-DELETE splicer.end(pp.testX._inherits)
  {

  // All data marked protected will be accessable by 
  // descendant Impl classes
  protected:

    bool _wrapped;

  // DO-NOT-DELETE splicer.begin(pp.testX._implementation)

  // Insert-UserCode-Here(pp.testX._implementation)

  // Bocca generated code. bocca.protected.begin(pp.testX._implementation)
  
   gov::cca::Services    d_services; // our cca handle.
 

  // Bocca generated code. bocca.protected.end(pp.testX._implementation)


    gov::cca::ports::ParameterPortFactory ppf;
    gov::cca::ports::ParameterPort pp;
    gov::cca::Services svc;
    std::vector< gov::cca::TypeMap > pplist;
    int numtests;
    
  // DO-NOT-DELETE splicer.end(pp.testX._implementation)

  public:
    // default constructor, used for data wrapping(required)
    testX_impl();
    // sidl constructor (required)
    // Note: alternate Skel constructor doesn't call addref()
    // (fixes bug #275)
    testX_impl( struct pp_testX__object * s ) : StubBase(s,true), _wrapped(
      false) { _ctor(); }

    // user defined construction
    void _ctor();

    // virtual destructor (required)
    virtual ~testX_impl() { _dtor(); }

    // user defined destruction
    void _dtor();

    // true if this object was created by a user newing the impl
    inline bool _isWrapped() {return _wrapped;}

    // static class initializer
    static void _load();

  public:

    /**
     * user defined non-static method.
     */
    void
    boccaSetServices_impl (
      /* in */::gov::cca::Services services
    )
    // throws:
    //     ::gov::cca::CCAException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    boccaReleaseServices_impl (
      /* in */::gov::cca::Services services
    )
    // throws:
    //     ::gov::cca::CCAException
    //     ::sidl::RuntimeException
    ;


    /**
     *  This function should never be called, but helps babel generate better code. 
     */
    void
    boccaForceUsePortInclude_impl() ;

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
    setServices_impl (
      /* in */::gov::cca::Services services
    )
    // throws:
    //     ::gov::cca::CCAException
    //     ::sidl::RuntimeException
    ;


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
    releaseServices_impl (
      /* in */::gov::cca::Services services
    )
    // throws:
    //     ::gov::cca::CCAException
    //     ::sidl::RuntimeException
    ;


    /**
     *  
     * Execute some encapsulated functionality on the component. 
     * Return 0 if ok, -1 if internal error but component may be 
     * used further, and -2 if error so severe that component cannot
     * be further used safely.
     */
    int32_t
    go_impl() ;

    /**
     *  Inform the listener that someone is about to fetch their 
     * typemap. The return should be true if the listener
     * has changed the ParameterPort definitions.
     */
    bool
    updateParameterPort_impl (
      /* in */const ::std::string& portName
    )
    ;


    /**
     *  The component wishing to be told after a parameter is changed
     * implements this function.
     * @param portName the name of the port (typemap) on which the
     * value was set.
     * @param fieldName the name of the value in the typemap.
     */
    void
    updatedParameterValue_impl (
      /* in */const ::std::string& portName,
      /* in */const ::std::string& fieldName
    )
    ;

  };  // end class testX_impl

} // end namespace pp

// DO-NOT-DELETE splicer.begin(pp.testX._misc)
// Insert-Code-Here {pp.testX._misc} (miscellaneous things)
// Put miscellaneous things here...
// DO-NOT-DELETE splicer.end(pp.testX._misc)

#endif
