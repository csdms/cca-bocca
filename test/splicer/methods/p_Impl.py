#
# File:          p_Impl.py
# Symbol:        pytest.p-v0.0
# Symbol Type:   class
# Babel Version: 1.0.6
# Description:   Implementation of sidl class pytest.p in Python.
# 
# WARNING: Automatically generated; changes will be lost
# 
#


# DO-NOT-DELETE splicer.begin(_initial)
# Insert-Code-Here {_initial} ()
# DO-NOT-DELETE splicer.end(_initial)

import gov.cca.CCAException
import gov.cca.Component
import gov.cca.ComponentRelease
import gov.cca.Port
import gov.cca.Services
import pytest.p
import pytest.x
import sidl.BaseClass
import sidl.BaseInterface
import sidl.ClassInfo
import sidl.RuntimeException
import sidl.NotImplementedException

# DO-NOT-DELETE splicer.begin(_before_type)
import sys
# DO-NOT-DELETE splicer.end(_before_type)

class p:

# All calls to sidl methods should use __IORself

# Normal Babel creation pases in an IORself. If IORself == None
# that means this Impl class is being constructed for native delegation
  def __init__(self, IORself = None):
    if (IORself == None):
      self.__IORself = pytest.p.p(impl = self)
    else:
      self.__IORself = IORself
# DO-NOT-DELETE splicer.begin(__init__)
    # Put your code here...
    # Bocca generated code. bocca.protected.begin(pytest.p._init) 
    self.d_services = None
    self.bocca_print_errs = True
    # Bocca generated code. bocca.protected.end(pytest.p._init) 
# DO-NOT-DELETE splicer.end(__init__)

# Returns the IORself (client stub) of the Impl, mainly for use
# with native delegation
  def _getStub(self):
    return self.__IORself

  def boccaSetServices(self, services):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # gov.cca.Services services
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(boccaSetServices)
# Bocca generated code. bocca.protected.begin(boccaSetServices) 
    self.d_services = services

    # Create a typemap
    mymap = services.createTypeMap()
    

    port = gov.cca.Port.Port(self.__IORself)  # CAST 
    if not port:
      ex = sidl.SIDLException.SIDLException()
      ex.setNote(__name__,0, 'Error casting self pytest.p to to gov.cca.Port')
      raise sidl.SIDLException._Exception, ex

    # Provide a pytest.x port with port name MYX 
    try:
      self.d_services.addProvidesPort(port,
                              'MYX',
                              'pytest.x',
                              mymap);
    except sidl.BaseException._Exception, e:
      (etype, eobj, etb) = sys.exc_info()
      eobj.add(__name__, 0, 'Error - could not addProvidesPort(port,"MYX","pytest.x",mymap)')
      raise sidl.BaseException._Exception, e

    # Register a use port of type pytest.x with port name YOURX
    try:
      self.d_services.registerUsesPort('YOURX',
                                'pytest.x',
                                mymap);
    except sidl.BaseException._Exception, e:
      (etype, eobj, etb) = sys.exc_info()
      eobj.add(__name__, 0, 'Error - could not registerUsesPort("YOURX","pytest.x",mymap)')
      raise sidl.BaseException._Exception, e

    compRelease = gov.cca.ComponentRelease.ComponentRelease(self.__IORself)
    try:
      self.d_services.registerForRelease(compRelease)
    except sidl.BaseException._Exception, e:
      (etype, eobj, etb) = sys.exc_info()
      eobj.exception.add(__name__,0, 'Error - could not registerForRelease(self) in pytest.p')
      raise sidl.BaseException._Exception, e
      
    return
# Bocca generated code. bocca.protected.end(boccaSetServices)
# DO-NOT-DELETE splicer.end(boccaSetServices)

  def boccaReleaseServices(self, services):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # gov.cca.Services services
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

    # DO-NOT-DELETE splicer.begin(boccaReleaseServices)
    # Bocca generated code. bocca.protected.begin(pytest.p.boccaReleaseServices)
    self.d_services = None

    # UN-Provide a pytest.x port with port name MYX 
    try:
      services.removeProvidesPort('MYX')
    except sidl.BaseException._Exception, e:
      (etype, eobj, etb) = sys.exc_info()
      eobj.exception.add(__name__,0, 'Error - could not remove provided port pytest.x:MYX')
      raise sidl.BaseException._Exception, e

    # Un-Register a use port of type pytest.x with port name YOURX
    try:
      services.unregisterUsesPort('YOURX')
    except sidl.BaseException._Exception, e:
      (etype, eobj, etb) = sys.exc_info()
      eobj.exception.add(__name__,0, 'Error - could not unregisterUsesPort("YOURX")')
      raise sidl.BaseException._Exception, e

    return
    # Bocca generated code. bocca.protected.end(pytest.p.boccaReleaseServices)
    # DO-NOT-DELETE splicer.end(boccaReleaseServices)

  def boccaForceUsePortInclude(self, dummy0):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # pytest.x dummy0
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

    # DO-NOT-DELETE splicer.begin(boccaForceUsePortInclude)
    # Bocca generated code. bocca.protected.begin(boccaForceUsePortInclude)
    o0 = dummy0

    # Bocca generated code. bocca.protected.end(boccaForceUsePortInclude)
    # DO-NOT-DELETE splicer.end(boccaForceUsePortInclude)

  def setServices(self, services):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # gov.cca.Services services
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

    """\
 Starts up a component presence in the calling framework.
@param services the component instance's handle on the framework world.
Contracts concerning Svc and setServices:

The component interaction with the CCA framework
and Ports begins on the call to setServices by the framework.

This function is called exactly once for each instance created
by the framework.

The argument Svc will never be nil/null.

Those uses ports which are automatically connected by the framework
(so-called service-ports) may be obtained via getPort during
setServices.
"""
    # DO-NOT-DELETE splicer.begin(setServices)
    # bocca-default-code. User may edit or delete.begin(setServices)

    self.boccaSetServices(services)
  
    # Put your code here...

    # bocca-default-code. User may edit or delete.end(setServices)
    # DO-NOT-DELETE splicer.end(setServices)

  def releaseServices(self, services):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # gov.cca.Services services
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

    """\
Shuts down a component presence in the calling framework.
@param services the component instance's handle on the framework world.
Contracts concerning Svc and setServices:

This function is called exactly once for each callback registered
through Services.

The argument Svc will never be nil/null.
The argument Svc will always be the same as that received in
setServices.

During this call the component should release any interfaces
acquired by getPort().

During this call the component should reset to nil any stored
reference to Svc.

After this call, the component instance will be removed from the
framework. If the component instance was created by the
framework, it will be destroyed, not recycled, The behavior of
any port references obtained from this component instance and
stored elsewhere becomes undefined.

Notes for the component implementor:
1) The component writer may perform blocking activities
within releaseServices, such as waiting for remote computations
to shutdown.
2) It is good practice during releaseServices for the component
writer to remove or unregister all the ports it defined.
"""
    # DO-NOT-DELETE splicer.begin(releaseServices)

    # bocca-default-code. User may edit or delete.begin(releaseServices)
    self.boccaReleaseServices(services)
    # bocca-default-code. User may edit or delete.end(releaseServices)

    # DO-NOT-DELETE splicer.end(releaseServices)

# DO-NOT-DELETE splicer.begin(_final)
# Insert-Code-Here {_final} ()
# DO-NOT-DELETE splicer.end(_final)
