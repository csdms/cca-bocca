/*
 * File:          Driver_Impl.java
 * Symbol:        myproj.Driver-v0.0
 * Symbol Type:   class
 * Babel Version: 1.0.6
 * Description:   Server-side implementation for myproj.Driver
 * 
 * WARNING: Automatically generated; only changes within splicers preserved
 * 
 */

package myproj;

import gov.cca.CCAException;
import gov.cca.Component;
import gov.cca.ComponentRelease;
import gov.cca.Port;
import gov.cca.Services;
import gov.cca.ports.GoPort;
import myproj.IntegratorPort;
import sidl.BaseClass;
import sidl.BaseInterface;
import sidl.ClassInfo;
import sidl.RuntimeException;

// DO-NOT-DELETE splicer.begin(myproj.Driver._imports)
// Insert-Code-Here {myproj.Driver._imports} (additional imports)
// DO-NOT-DELETE splicer.end(myproj.Driver._imports)

/**
 * Symbol "myproj.Driver" (version 0.0)
 */
public class Driver_Impl extends Driver
{

   // DO-NOT-DELETE splicer.begin(myproj.Driver._data)

   // Bocca generated code. bocca.protected.begin(myproj.Driver._data)
    gov.cca.Services    d_services;
    public boolean bocca_print_errs = true;
   // Bocca generated code. bocca.protected.end(myproj.Driver._data)
    // DO-NOT-DELETE splicer.end(myproj.Driver._data)

  static { 
  // DO-NOT-DELETE splicer.begin(myproj.Driver._load)
  // Insert-Code-Here {myproj.Driver._load} (class initialization)
  // DO-NOT-DELETE splicer.end(myproj.Driver._load)
  }

  /**
   * User defined constructor
   */
  public Driver_Impl(long IORpointer){
    super(IORpointer);
    // DO-NOT-DELETE splicer.begin(myproj.Driver.Driver)
    // Insert-Code-Here {myproj.Driver.Driver} (constructor)
    // DO-NOT-DELETE splicer.end(myproj.Driver.Driver)
  }

  /**
   * Back door constructor
   */
  public Driver_Impl(){
    d_ior = _wrap(this);
    // DO-NOT-DELETE splicer.begin(myproj.Driver._wrap)
    // Insert-Code-Here {myproj.Driver._wrap} (_wrap)
    // DO-NOT-DELETE splicer.end(myproj.Driver._wrap)
  }

  /**
   * User defined destructing method
   */
  public void dtor() throws Throwable{
    // DO-NOT-DELETE splicer.begin(myproj.Driver._dtor)
    // Insert-Code-Here {myproj.Driver._dtor} (destructor)
    // DO-NOT-DELETE splicer.end(myproj.Driver._dtor)
  }

  /**
   * finalize method (Only use this if you're sure you need it!)
   */
  public void finalize() throws Throwable{
    // DO-NOT-DELETE splicer.begin(myproj.Driver.finalize)
    // Insert-Code-Here {myproj.Driver.finalize} (finalize)
    // DO-NOT-DELETE splicer.end(myproj.Driver.finalize)
  }

  // user defined static methods: (none)

  // user defined non-static methods:
  /**
   * Method:  boccaSetServices[]
   */
  public void boccaSetServices_Impl (
    /*in*/ gov.cca.Services services ) 
    throws gov.cca.CCAException.Wrapper, 
    sidl.RuntimeException.Wrapper
  {
// DO-NOT-DELETE splicer.begin(myproj.Driver.boccaSetServices)
// Bocca generated code. bocca.protected.begin(myproj.Driver.boccaSetServices)

   gov.cca.TypeMap typeMap;
   gov.cca.Port    port;

   d_services = services;

   typeMap = d_services.createTypeMap();

   port = (gov.cca.Port)(this);


  // Provide a myproj.IntegratorPort port with port name myfoo 
   try{
      d_services.addProvidesPort(port,
					"myfoo",
					"myproj.IntegratorPort",
					typeMap);
   } catch ( gov.cca.CCAException.Wrapper ex )  {
      String msg = "Error calling addProvidesPort(port,\"myfoo\", \"myproj.IntegratorPort\", typeMap) ";
      ex.add(msg);
      throw ex;
   }    

  // Provide a gov.cca.ports.GoPort port with port name run 
   try{
      d_services.addProvidesPort(port,
					"run",
					"gov.cca.ports.GoPort",
					typeMap);
   } catch ( gov.cca.CCAException.Wrapper ex )  {
      String msg = "Error calling addProvidesPort(port,\"run\", \"gov.cca.ports.GoPort\", typeMap) ";
      ex.add(msg);
      throw ex;
   }    

  // Use a myproj.IntegratorPort port with port name integrate 
   try{
      d_services.registerUsesPort("integrate",
                                         "myproj.IntegratorPort",
                                         typeMap);
   } catch ( gov.cca.CCAException.Wrapper ex )  {
      String msg = "Error calling registerUsesPort(\"integrate\", \"myproj.IntegratorPort\", typeMap) ";
      ex.add(msg);
      throw ex;
   }


   gov.cca.ComponentRelease cr = (gov.cca.ComponentRelease)this; // CAST
   d_services.registerForRelease(cr);
   return;
// Bocca generated code. bocca.protected.end(myproj.Driver.boccaSetServices)
// DO-NOT-DELETE splicer.end(myproj.Driver.boccaSetServices)
  }

  /**
   * Method:  boccaReleaseServices[]
   */
  public void boccaReleaseServices_Impl (
    /*in*/ gov.cca.Services services ) 
    throws gov.cca.CCAException.Wrapper, 
    sidl.RuntimeException.Wrapper
  {
  // DO-NOT-DELETE splicer.begin(myproj.Driver.boccaReleaseServices)
  // Bocca generated code. bocca.protected.begin(myproj.Driver.boccaReleaseServices)

   d_services=null;

  // Un-provide myproj.IntegratorPort port with port name myfoo 
  try{
    services.removeProvidesPort("myfoo");
  } catch ( gov.cca.CCAException.Wrapper ex )  {
    if (bocca_print_errs) {
      System.err.print("myproj.Driver: Error calling removeProvidesPort(\"myfoo\"): " +ex.getNote());
    }
  }

  // Un-provide gov.cca.ports.GoPort port with port name run 
  try{
    services.removeProvidesPort("run");
  } catch ( gov.cca.CCAException.Wrapper ex )  {
    if (bocca_print_errs) {
      System.err.print("myproj.Driver: Error calling removeProvidesPort(\"run\"): " +ex.getNote());
    }
  }

  // Release myproj.IntegratorPort port with port name integrate 
  try{
    services.unregisterUsesPort("integrate");
  } catch ( gov.cca.CCAException.Wrapper ex )  {
    if (bocca_print_errs) {
      System.err.println("myproj.Driver: Error calling unregisterUsesPort(\"integrate\"): " +ex.getNote());
    }
  }

   return;
  // Bocca generated code. bocca.protected.end(myproj.Driver.boccaReleaseServices)
    
  // DO-NOT-DELETE splicer.end(myproj.Driver.boccaReleaseServices)
  }

  /**
   * Method:  boccaForceUsePortInclude[]
   */
  public void boccaForceUsePortInclude_Impl (
    /*in*/ myproj.IntegratorPort dummy0 ) 
    throws sidl.RuntimeException.Wrapper
  {
  // DO-NOT-DELETE splicer.begin(myproj.Driver.boccaForceUsePortInclude)
  // Bocca generated code. bocca.protected.begin(myproj.Driver.boccaForceUsePortInclude)
    Object o;
    o = dummy0;

  // Bocca generated code. bocca.protected.end(myproj.Driver.boccaForceUsePortInclude)
  // DO-NOT-DELETE splicer.end(myproj.Driver.boccaForceUsePortInclude)
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
  public void setServices_Impl (
    /*in*/ gov.cca.Services services ) 
    throws gov.cca.CCAException.Wrapper, 
    sidl.RuntimeException.Wrapper
  {
  // DO-NOT-DELETE splicer.begin(myproj.Driver.setServices)
  // bocca-default-code. User may edit or delete.begin(myproj.Driver.setServices)

     boccaSetServices(services); 
  
  // Insert-Code-Here {myproj.Driver.setServices} (setServices method)

  // bocca-default-code. User may edit or delete.end(myproj.Driver.setServices)
  // DO-NOT-DELETE splicer.end(myproj.Driver.setServices)
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
  public void releaseServices_Impl (
    /*in*/ gov.cca.Services services ) 
    throws gov.cca.CCAException.Wrapper, 
    sidl.RuntimeException.Wrapper
  {
  // DO-NOT-DELETE splicer.begin(myproj.Driver.releaseServices)
  // bocca-default-code. User may edit or delete.end(myproj.Driver.releaseServices)
    // Insert-Code-Here {myproj.Driver.releaseServices} (releaseServices method)

     boccaReleaseServices(services); 

  // bocca-default-code. User may edit or delete.end(myproj.Driver.releaseServices)
  // DO-NOT-DELETE splicer.end(myproj.Driver.releaseServices)
  }


  // DO-NOT-DELETE splicer.begin(myproj.Driver._misc)
  // Insert-Code-Here {myproj.Driver._misc} (miscellaneous)
  // DO-NOT-DELETE splicer.end(myproj.Driver._misc)

} // end class Driver

