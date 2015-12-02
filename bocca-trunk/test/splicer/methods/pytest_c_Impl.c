/*
 * File:          pytest_c_Impl.c
 * Symbol:        pytest.c-v0.0
 * Symbol Type:   class
 * Babel Version: 1.0.6
 * Description:   Server-side implementation for pytest.c
 * 
 * WARNING: Automatically generated; only changes within splicers preserved
 * 
 */

/*
 * DEVELOPERS ARE EXPECTED TO PROVIDE IMPLEMENTATIONS
 * FOR THE FOLLOWING METHODS BETWEEN SPLICER PAIRS.
 */

/*
 * Symbol "pytest.c" (version 0.0)
 */

#include "pytest_c_Impl.h"
#include "sidl_NotImplementedException.h"
#include "sidl_Exception.h"

/* DO-NOT-DELETE splicer.begin(pytest.c._includes) */
/* Bocca generated code. bocca.protected.begin(pytest.c._includes) */
#include <stdlib.h>
#include <string.h>
#include "sidl_SIDLException.h"

#define _BOCCA_CTOR_MESSAGES 0
#ifdef _BOCCA_STDERR
#include <stdio.h>
#include "sidl_String.h"
#ifdef _BOCCA_CTOR_PRINT
#undef _BOCCA_CTOR_MESSAGES
#define _BOCCA_CTOR_MESSAGES 1
#endif /* _BOCCA_CTOR_PRINT */
#endif /* _BOCCA_STDERR */
/* Bocca generated code. bocca.protected.end(pytest.c._includes) */

/* Insert-UserCode-Here {pytest.c._includes} (includes and arbitrary code) */

/* DO-NOT-DELETE splicer.end(pytest.c._includes) */

#define SIDL_IOR_MAJOR_VERSION 1
#define SIDL_IOR_MINOR_VERSION 0
/*
 * Static class initializer called exactly once before any user-defined method is dispatched
 */

#undef __FUNC__
#define __FUNC__ "impl_pytest_c__load"

#ifdef __cplusplus
extern "C"
#endif
void
impl_pytest_c__load(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(pytest.c._load) */
    /* Insert-Code-Here {pytest.c._load} (static class initializer method) */
    
    /* DO-DELETE-WHEN-IMPLEMENTING exception.begin() */
    /* 
     * This method has not been implemented.
     */
    SIDL_THROW(*_ex, sidl_NotImplementedException,     "This method has not been implemented");
  EXIT:;
    /* DO-DELETE-WHEN-IMPLEMENTING exception.end() */
    
    /* DO-NOT-DELETE splicer.end(pytest.c._load) */
  }
}
/*
 * Class constructor called when the class is created.
 */

#undef __FUNC__
#define __FUNC__ "impl_pytest_c__ctor"

#ifdef __cplusplus
extern "C"
#endif
void
impl_pytest_c__ctor(
  /* in */ pytest_c self,
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
  /* DO-NOT-DELETE splicer.begin(pytest.c._ctor) */
    
  /* bocca-default-code. User may edit or delete.begin(pytest.c._ctor) */
   struct pytest_c__data *dptr = 
                (struct pytest_c__data*)malloc(sizeof(struct pytest_c__data));
   if (dptr) {
      memset(dptr, 0, sizeof(struct pytest_c__data));
   }
   pytest_c__set_data(self, dptr);
   #if _BOCCA_CTOR_MESSAGES
     fprintf(stderr, "CTOR pytest.c: %s constructed data %p in self %p\n", __FUNC__, dptr, self);
   #endif /* _BOCCA_CTOR_MESSAGES */
  /* bocca-default-code. User may edit or delete.end(pytest.c._ctor) */

  /* initialize user elements of dptr here */
  /* Insert-UserCode-Here {pytest.c._ctor} (constructor method) */

  /* DO-NOT-DELETE splicer.end(pytest.c._ctor) */
  }
}

/*
 * Special Class constructor called when the user wants to wrap his own private data.
 */

#undef __FUNC__
#define __FUNC__ "impl_pytest_c__ctor2"

#ifdef __cplusplus
extern "C"
#endif
void
impl_pytest_c__ctor2(
  /* in */ pytest_c self,
  /* in */ void* private_data,
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(pytest.c._ctor2) */
    /* Insert-Code-Here {pytest.c._ctor2} (special constructor method) */
    
    /* DO-DELETE-WHEN-IMPLEMENTING exception.begin() */
    /* 
     * This method has not been implemented.
     */
    SIDL_THROW(*_ex, sidl_NotImplementedException,     "This method has not been implemented");
  EXIT:;
    /* DO-DELETE-WHEN-IMPLEMENTING exception.end() */
    
    /* DO-NOT-DELETE splicer.end(pytest.c._ctor2) */
  }
}
/*
 * Class destructor called when the class is deleted.
 */

#undef __FUNC__
#define __FUNC__ "impl_pytest_c__dtor"

#ifdef __cplusplus
extern "C"
#endif
void
impl_pytest_c__dtor(
  /* in */ pytest_c self,
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
  /* DO-NOT-DELETE splicer.begin(pytest.c._dtor) */
  /* deinitialize user elements of dptr here */
  /* Insert-UserCode-Here {pytest.c._dtor} (destructor method) */
    
  /* bocca-default-code. User may edit or delete.begin(pytest.c._dtor) */
   struct pytest_c__data *dptr = 
                pytest_c__get_data(self);
   if (dptr) {
      free(dptr);
      pytest_c__set_data(self, NULL);
   }
   #if _BOCCA_CTOR_MESSAGES
     fprintf(stderr, "DTOR pytest.c: %s freed data %p in self %p\n", __FUNC__, dptr, self);
   #endif /* _BOCCA_CTOR_MESSAGES */
  /* bocca-default-code. User may edit or delete.end(pytest.c._dtor) */

  /* DO-NOT-DELETE splicer.end(pytest.c._dtor) */
  }
}

/*
 * Method:  boccaSetServices[]
 */

#undef __FUNC__
#define __FUNC__ "impl_pytest_c_boccaSetServices"

#ifdef __cplusplus
extern "C"
#endif
void
impl_pytest_c_boccaSetServices(
  /* in */ pytest_c self,
  /* in */ gov_cca_Services services,
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
/* DO-NOT-DELETE splicer.begin(pytest.c.boccaSetServices) */
/* Bocca generated code. bocca.protected.begin(pytest.c.boccaSetServices) */
   struct pytest_c__data *pd;
   gov_cca_ComponentRelease   compRelease = NULL;
   sidl_BaseInterface throwaway_excpt = NULL; /* for use in EXIT block only. */
   int dr_services=0; /* assume releaseServices will not be called if setServices fails */
   

   gov_cca_TypeMap typeMap = NULL;
   gov_cca_Port port = NULL;

   pd = pytest_c__get_data(self);
   if (pd == NULL) {
     SIDL_THROW(*_ex, sidl_SIDLException, "NULL data pointer in pytest.c boccaSetServices");
   }

   pd->d_services = services;
   gov_cca_Services_addRef(services, _ex); SIDL_CHECK(*_ex);
   dr_services=1;


  /* Create a typemap  */
   typeMap = gov_cca_Services_createTypeMap(pd->d_services, _ex); SIDL_CHECK(*_ex);
   /* We must pass the exception back up; the framework is hosed and not our problem. */

  /* Cast myself to gov.cca.Port */
   port = gov_cca_Port__cast(self, _ex); SIDL_CHECK(*_ex);

   /* Provide a pytest.x port with port name MYX */
   gov_cca_Services_addProvidesPort(pd->d_services,   
                       port,
                       "MYX",
                       "pytest.x",
                       typeMap,
                       _ex); SIDL_CHECK(*_ex);

   gov_cca_Port_deleteRef(port, _ex); port = NULL; SIDL_CHECK(*_ex);

  /* Register a use port of type pytest.x with port name YOURX */  
   gov_cca_Services_registerUsesPort(pd->d_services,   
                   "YOURX",
                   "pytest.x",
                   typeMap,
                   _ex); SIDL_CHECK(*_ex);

   gov_cca_TypeMap_deleteRef(typeMap,_ex); typeMap = NULL; SIDL_CHECK(*_ex);

   /* Cast myself to gov.cca.ComponentRelease */
   compRelease = gov_cca_ComponentRelease__cast(self, _ex); SIDL_CHECK(*_ex);
   gov_cca_Services_registerForRelease(pd->d_services, compRelease, _ex); SIDL_CHECK(*_ex);
   gov_cca_ComponentRelease_deleteRef(compRelease, _ex); compRelease = NULL; SIDL_CHECK(*_ex);
   return;

   /* exceptions exit through here, where we clean up memory references. */
EXIT:;
   if (dr_services != 0) { 
     gov_cca_Services_deleteRef(services, &throwaway_excpt); SIDL_CLEAR(throwaway_excpt);
     services = NULL;
   }
   if (compRelease != NULL) {
     gov_cca_ComponentRelease_deleteRef(compRelease, &throwaway_excpt); SIDL_CLEAR(throwaway_excpt);
     compRelease = NULL;
   }

   if (typeMap != NULL) {
     gov_cca_TypeMap_deleteRef(typeMap, &throwaway_excpt); SIDL_CLEAR(throwaway_excpt);
     port = NULL;
   }
   if (port != NULL) {
     gov_cca_Port_deleteRef(port, &throwaway_excpt); SIDL_CLEAR(throwaway_excpt);
     port = NULL;
   }

   return;

/* Bocca generated code. bocca.protected.end(pytest.c.boccaSetServices) */
/* DO-NOT-DELETE splicer.end(pytest.c.boccaSetServices) */
  }
}

/*
 * Method:  boccaReleaseServices[]
 */

#undef __FUNC__
#define __FUNC__ "impl_pytest_c_boccaReleaseServices"

#ifdef __cplusplus
extern "C"
#endif
void
impl_pytest_c_boccaReleaseServices(
  /* in */ pytest_c self,
  /* in */ gov_cca_Services services,
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
/*  DO-NOT-DELETE splicer.begin(pytest.c.boccaReleaseServices) */
/*  Bocca generated code. bocca.protected.begin(pytest.c.boccaReleaseServices) */

   struct pytest_c__data *pd;
   sidl_BaseInterface throwaway_excpt = NULL;
   sidl_BaseInterface dummy_excpt = NULL;
   char *errMsg=NULL;
   /* our policy is to trap and optionally print all port-related messages,
      attempting to eliminate all ports. */


   /* UN-Provide a pytest.x port with port name MYX */
   gov_cca_Services_removeProvidesPort(services, "MYX", &throwaway_excpt);
   errMsg = "Error: Could not removeProvidesPort(\"MYX\")";
   pytest_c_checkException(self, throwaway_excpt, errMsg, FALSE, &dummy_excpt);

  /* Un-Register a use port of type pytest.x with port name YOURX */  
   gov_cca_Services_unregisterUsesPort(services, "YOURX", &throwaway_excpt);
   errMsg= "Error: Could not unregisterUsesPort(\"YOURX\")";
   pytest_c_checkException(self, throwaway_excpt, errMsg, FALSE, &dummy_excpt);

   gov_cca_Services_deleteRef(services, _ex); SIDL_CHECK(*_ex);
   services = NULL;
   pd = pytest_c__get_data(self);
   if (pd == NULL) {
     SIDL_THROW(*_ex, sidl_SIDLException, "NULL data pointer in pytest.c boccaSetServices");
   }
   pd->d_services = NULL;
   return;

EXIT:;
   return;
/*  Bocca generated code. bocca.protected.end(pytest.c.boccaReleaseServices) */
/*  DO-NOT-DELETE splicer.end(pytest.c.boccaReleaseServices)) */
  }
}

/*
 * Method:  checkException[]
 */

#undef __FUNC__
#define __FUNC__ "impl_pytest_c_checkException"

#ifdef __cplusplus
extern "C"
#endif
void
impl_pytest_c_checkException(
  /* in */ pytest_c self,
  /* in */ sidl_BaseInterface excpt,
  /* in */ const char* msg,
  /* in */ sidl_bool fatal,
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
/*  DO-NOT-DELETE splicer.begin(pytest.c.checkException) */

/*  Bocca generated code. bocca.protected.begin(pytest.c.checkException) */
#ifdef _BOCCA_STDERR
   sidl_BaseException be = NULL;
   char *etext=NULL;
#endif
   
   if (SIDL_CATCH(excpt, "sidl.BaseException")) {
#ifdef _BOCCA_STDERR
      be  = sidl_BaseException__cast(excpt, _ex); SIDL_CLEAR(*_ex);
      etext = sidl_BaseException_getNote(be, _ex); SIDL_CLEAR(*_ex);
      fprintf(stderr, "pytest.c: %s \n%s\n", msg,etext);
      sidl_String_free(etext);
      if (be != NULL) { 
        sidl_BaseException_deleteRef(be, _ex); SIDL_CLEAR(*_ex);
        be = NULL;
      }
#endif
      SIDL_CLEAR(excpt);
      if (fatal) exit(1);
   }
   return;
   
/*  Bocca generated code. bocca.protected.end(pytest.c.checkException) */
    
/*  DO-NOT-DELETE splicer.end(pytest.c.checkException) */
  }
}

/*
 * Method:  boccaForceUsePortInclude[]
 */

#undef __FUNC__
#define __FUNC__ "impl_pytest_c_boccaForceUsePortInclude"

#ifdef __cplusplus
extern "C"
#endif
void
impl_pytest_c_boccaForceUsePortInclude(
  /* in */ pytest_c self,
  /* in */ pytest_x dummy0,
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
  /* DO-NOT-DELETE splicer.begin(pytest.c.boccaForceUsePortInclude) */
  /* Bocca generated code. bocca.protected.begin(pytest.c.boccaForceUsePortInclude) */
    (void)self;
    (void)dummy0;

  /* Bocca generated code. bocca.protected.end(pytest.c.boccaForceUsePortInclude) */
  /* DO-NOT-DELETE splicer.end(pytest.c.boccaForceUsePortInclude) */
  }
}

/*
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

#undef __FUNC__
#define __FUNC__ "impl_pytest_c_setServices"

#ifdef __cplusplus
extern "C"
#endif
void
impl_pytest_c_setServices(
  /* in */ pytest_c self,
  /* in */ gov_cca_Services services,
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
  /* DO-NOT-DELETE splicer.begin(pytest.c.setServices) */

  /* bocca-default-code. User may edit or delete.begin(pytest.c.setServices) */
    impl_pytest_c_boccaSetServices(self, services, _ex); SIDL_CHECK(*_ex);
  /* bocca-default-code. User may edit or delete.end(pytest.c.setServices) */
  
  /*  Insert-UserCode-Here {pytest.c.setServices} (setServices method) */

EXIT:;
    /* Insert additional exception cleanup here if needed. */
    return;

  /* DO-NOT-DELETE splicer.end(pytest.c.setServices) */
  }
}

/*
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

#undef __FUNC__
#define __FUNC__ "impl_pytest_c_releaseServices"

#ifdef __cplusplus
extern "C"
#endif
void
impl_pytest_c_releaseServices(
  /* in */ pytest_c self,
  /* in */ gov_cca_Services services,
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
  /* DO-NOT-DELETE splicer.begin(pytest.c.releaseServices) */

  /*  Insert-UserCode-Here {pytest.c.releaseServices} (releaseServices method) */

  /* bocca-default-code. User may edit or delete.begin(pytest.c.releaseServices) */
    impl_pytest_c_boccaReleaseServices(self, services, _ex); SIDL_CHECK(*_ex);
    return;
  /* bocca-default-code. User may edit or delete.end(pytest.c.releaseServices) */

EXIT:;
    /* Insert additional exception cleanup here if needed. */
    return;

  /* DO-NOT-DELETE splicer.end(pytest.c.releaseServices) */
  }
}
/* Babel internal methods, Users should not edit below this line. */
struct gov_cca_CCAException__object* 
  impl_pytest_c_fconnect_gov_cca_CCAException(const char* url, sidl_bool ar, 
  sidl_BaseInterface *_ex) {
  return gov_cca_CCAException__connectI(url, ar, _ex);
}
struct gov_cca_CCAException__object* impl_pytest_c_fcast_gov_cca_CCAException(
  void* bi, sidl_BaseInterface* _ex) {
  return gov_cca_CCAException__cast(bi, _ex);
}
struct gov_cca_Component__object* impl_pytest_c_fconnect_gov_cca_Component(
  const char* url, sidl_bool ar, sidl_BaseInterface *_ex) {
  return gov_cca_Component__connectI(url, ar, _ex);
}
struct gov_cca_Component__object* impl_pytest_c_fcast_gov_cca_Component(void* 
  bi, sidl_BaseInterface* _ex) {
  return gov_cca_Component__cast(bi, _ex);
}
struct gov_cca_ComponentRelease__object* 
  impl_pytest_c_fconnect_gov_cca_ComponentRelease(const char* url, sidl_bool ar,
  sidl_BaseInterface *_ex) {
  return gov_cca_ComponentRelease__connectI(url, ar, _ex);
}
struct gov_cca_ComponentRelease__object* 
  impl_pytest_c_fcast_gov_cca_ComponentRelease(void* bi, sidl_BaseInterface* 
  _ex) {
  return gov_cca_ComponentRelease__cast(bi, _ex);
}
struct gov_cca_Port__object* impl_pytest_c_fconnect_gov_cca_Port(const char* 
  url, sidl_bool ar, sidl_BaseInterface *_ex) {
  return gov_cca_Port__connectI(url, ar, _ex);
}
struct gov_cca_Port__object* impl_pytest_c_fcast_gov_cca_Port(void* bi, 
  sidl_BaseInterface* _ex) {
  return gov_cca_Port__cast(bi, _ex);
}
struct gov_cca_Services__object* impl_pytest_c_fconnect_gov_cca_Services(const 
  char* url, sidl_bool ar, sidl_BaseInterface *_ex) {
  return gov_cca_Services__connectI(url, ar, _ex);
}
struct gov_cca_Services__object* impl_pytest_c_fcast_gov_cca_Services(void* bi, 
  sidl_BaseInterface* _ex) {
  return gov_cca_Services__cast(bi, _ex);
}
struct pytest_c__object* impl_pytest_c_fconnect_pytest_c(const char* url, 
  sidl_bool ar, sidl_BaseInterface *_ex) {
  return pytest_c__connectI(url, ar, _ex);
}
struct pytest_c__object* impl_pytest_c_fcast_pytest_c(void* bi, 
  sidl_BaseInterface* _ex) {
  return pytest_c__cast(bi, _ex);
}
struct pytest_x__object* impl_pytest_c_fconnect_pytest_x(const char* url, 
  sidl_bool ar, sidl_BaseInterface *_ex) {
  return pytest_x__connectI(url, ar, _ex);
}
struct pytest_x__object* impl_pytest_c_fcast_pytest_x(void* bi, 
  sidl_BaseInterface* _ex) {
  return pytest_x__cast(bi, _ex);
}
struct sidl_BaseClass__object* impl_pytest_c_fconnect_sidl_BaseClass(const 
  char* url, sidl_bool ar, sidl_BaseInterface *_ex) {
  return sidl_BaseClass__connectI(url, ar, _ex);
}
struct sidl_BaseClass__object* impl_pytest_c_fcast_sidl_BaseClass(void* bi, 
  sidl_BaseInterface* _ex) {
  return sidl_BaseClass__cast(bi, _ex);
}
struct sidl_BaseInterface__object* impl_pytest_c_fconnect_sidl_BaseInterface(
  const char* url, sidl_bool ar, sidl_BaseInterface *_ex) {
  return sidl_BaseInterface__connectI(url, ar, _ex);
}
struct sidl_BaseInterface__object* impl_pytest_c_fcast_sidl_BaseInterface(void* 
  bi, sidl_BaseInterface* _ex) {
  return sidl_BaseInterface__cast(bi, _ex);
}
struct sidl_ClassInfo__object* impl_pytest_c_fconnect_sidl_ClassInfo(const 
  char* url, sidl_bool ar, sidl_BaseInterface *_ex) {
  return sidl_ClassInfo__connectI(url, ar, _ex);
}
struct sidl_ClassInfo__object* impl_pytest_c_fcast_sidl_ClassInfo(void* bi, 
  sidl_BaseInterface* _ex) {
  return sidl_ClassInfo__cast(bi, _ex);
}
struct sidl_RuntimeException__object* 
  impl_pytest_c_fconnect_sidl_RuntimeException(const char* url, sidl_bool ar, 
  sidl_BaseInterface *_ex) {
  return sidl_RuntimeException__connectI(url, ar, _ex);
}
struct sidl_RuntimeException__object* impl_pytest_c_fcast_sidl_RuntimeException(
  void* bi, sidl_BaseInterface* _ex) {
  return sidl_RuntimeException__cast(bi, _ex);
}
