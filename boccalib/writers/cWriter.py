from writers.sourceWriter import SourceWriter

def getWriterParameters():
    return (CWriter.language, CWriter.babelVersions, CWriter.dialect)
 
class CWriter(SourceWriter):
    language = 'c'
    dialect = 'standard'
    babelVersions = ['1.1.X','1.2.X','1.4.X', '1.5.X', '2.0.X']
    commentLineStart = "/* "
    commentLineEnd = "*/"

#---------------------------------------------------------------------------------
    def __init__(self, kind = 'component'):
        SourceWriter.__init__(self, kind)
    
#---------------------------------------------------------------------------------
    def getImplHeaderCode(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf ="""
/* DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._includes) */

/* Insert-UserCode-Here {@CMPT_TYPE@._includes} (includes and arbitrary code) */

/* """+self.protKey+""".begin(@CMPT_TYPE@._includes) */
#include <stdlib.h>
#include <string.h>
#include "sidl_SIDLException.h"

#define _BOCCA_CTOR_MESSAGES 0

#ifdef _BOCCA_STDERR

#define BOCCA_FPRINTF fprintf
#include <stdio.h>
#include "sidl_String.h"
#ifdef _BOCCA_CTOR_PRINT
#undef _BOCCA_CTOR_MESSAGES
#define _BOCCA_CTOR_MESSAGES 1
#endif /* _BOCCA_CTOR_PRINT */

#else /* _BOCCA_STDERR */
#define BOCCA_FPRINTF boccaPrintNothing
#endif /* _BOCCA_STDERR */

static int
boccaPrintNothing(void *v, const char * s, ...)
{
  (void)v; (void)s;
  return 0;
}
/* """+self.protKey+""".end(@CMPT_TYPE@._includes) */

/* Insert-UserCode-Here {@CMPT_TYPE@._includes} (includes and arbitrary code) */

/* DO-NOT-DELETE splicer.end(@CMPT_TYPE@._includes) */

"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
        return buf

#---------------------------------------------------------------------------------
    def getHeaderCode(self, componentSymbol):
        buf = """
  /* DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._data) */

  /* """+self.protKey+""".begin(@CMPT_TYPE@._data) */
  /* Handle to framework services object */
  gov_cca_Services """+self.servicesVariable+""";
  /* """+self.protKey+""".end(@CMPT_TYPE@._data) */

  /* Put other private data members here... */

  /* DO-NOT-DELETE splicer.end(@CMPT_TYPE@._data) */
"""    
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
        
#---------------------------------------------------------------------------------
    def getDestructorCode(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
  /* DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._dtor) */

  /* deinitialize user elements of dptr here */
  /* Insert-UserCode-Here {@CMPT_TYPE@._dtor} (destructor method) */
    
  /* """+self.onceKey+""".begin(@CMPT_TYPE@._dtor) */
   struct @CMPT_TYPE_UBAR@__data *dptr = 
                @CMPT_TYPE_UBAR@__get_data(self);
   if (dptr) {
      free(dptr);
      @CMPT_TYPE_UBAR@__set_data(self, NULL);
   }
   #if _BOCCA_CTOR_MESSAGES
     BOCCA_FPRINTF(stderr, "DTOR @CMPT_TYPE@: %s freed data %p in self %p\\n", 
                   __FUNC__, dptr, self);
   #endif /* _BOCCA_CTOR_MESSAGES */
  /* """+self.onceKey+""".end(@CMPT_TYPE@._dtor) */

  /* DO-NOT-DELETE splicer.end(@CMPT_TYPE@._dtor) */
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
        return buf
            
#---------------------------------------------------------------------------------
    def getConstructorCode(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
  /* DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._ctor) */

  /* Insert-UserDecl-Here {@CMPT_TYPE@._ctor} (constructor method) */
    
  /* """+self.onceKey+""".begin(@CMPT_TYPE@._ctor) */
   struct @CMPT_TYPE_UBAR@__data *dptr = 
       (struct @CMPT_TYPE_UBAR@__data*)malloc(sizeof(struct @CMPT_TYPE_UBAR@__data));
   if (dptr) {
      memset(dptr, 0, sizeof(struct @CMPT_TYPE_UBAR@__data));
   }
   @CMPT_TYPE_UBAR@__set_data(self, dptr);
   #if _BOCCA_CTOR_MESSAGES
     BOCCA_FPRINTF(stderr, 
        "CTOR @CMPT_TYPE@: %s constructed data %p in self %p\\n", 
        __FUNC__, dptr, self);
   #endif /* _BOCCA_CTOR_MESSAGES */
  /* """+self.onceKey+""".end(@CMPT_TYPE@._ctor) */

  /* initialize user elements of dptr here */
  /* Insert-UserCode-Here {@CMPT_TYPE@._ctor} (constructor method) */

  /* DO-NOT-DELETE splicer.end(@CMPT_TYPE@._ctor) */
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
        return buf
            
#---------------------------------------------------------------------------------
    def getSetServicesCode(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        methodName = 'impl_'+ cmpt_ubar + '_' + self.boccaServicesMethod
        buf = """ 
  /* DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.setServices) */

  /*  Insert-UserDecl-Here {@CMPT_TYPE@.setServices} (setServices method) */

  /* """+self.onceKey+""".begin(@CMPT_TYPE@.setServices) */
    """+methodName+"""(self, services, _ex); SIDL_CHECK(*_ex);
  /* """+self.onceKey+""".end(@CMPT_TYPE@.setServices) */
  
  /*  Insert-UserCode-Here {@CMPT_TYPE@.setServices} (setServices method) */

EXIT:;
    /* Insert additional exception cleanup here if needed. */
    return;

  /* DO-NOT-DELETE splicer.end(@CMPT_TYPE@.setServices) */
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf

#---------------------------------------------------------------------------------
    def getAuxiliarySetServicesMethod(self, componentSymbol, provides=[], uses=[]):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
/* DO-NOT-DELETE splicer.begin(@CMPT_TYPE@."""+self.boccaServicesMethod+""") */
/* DO-NOT-EDIT-BOCCA */
/* """+self.protKey+""".begin(@CMPT_TYPE@."""+self.boccaServicesMethod+""") */
   struct @CMPT_TYPE_UBAR@__data *pd;
   gov_cca_ComponentRelease   compRelease = NULL;
   sidl_BaseInterface throwaway_excpt = NULL; /* for use in EXIT block only. */
   int dr_services=0; /* assume releaseServices will not be called if setServices fails */
   
"""
# Add ports declarations (if needed)
        if (len(provides) + len(uses) > 0):
            buf += """
   gov_cca_TypeMap typeMap = NULL;
   gov_cca_Port port = NULL;
"""
# Component Registration code            
        buf +="""
   pd = @CMPT_TYPE_UBAR@__get_data(self);
   if (pd == NULL) {
     SIDL_THROW(*_ex, sidl_SIDLException, 
          "NULL data pointer in @CMPT_TYPE@ """+self.boccaServicesMethod+"""");
   }

   pd->"""+self.servicesVariable+""" = services;
   gov_cca_Services_addRef(services, _ex); SIDL_CHECK(*_ex);
   dr_services=1;

"""
        if (len(provides) + len(uses) > 0):
            buf += """
  /* Create a typemap  */
   typeMap = gov_cca_Services_createTypeMap(pd->"""+self.servicesVariable+""", _ex); 
   SIDL_CHECK(*_ex);
   /* We must pass the exception back up; the framework is hosed and not our problem. */
"""
            if (len(provides) > 0):
                buf +="""
  /* Cast myself to gov.cca.Port */
   port = gov_cca_Port__cast(self, _ex); SIDL_CHECK(*_ex);
"""
# Provide port(s) code
            for portInstance in provides:
                portBuf = """
   /* Provide a @PORT_TYPE@ port with port name @PORT_INSTANCE@ */
   gov_cca_Services_addProvidesPort(pd->"""+self.servicesVariable+""",   
                                    port,		/* the implementing object */
                                    "@PORT_INSTANCE@", /* the name seen by the user */
                                    "@PORT_TYPE@", /* sidl name of the port type. */
                                    typeMap,            /* extra properties */
                                    _ex); SIDL_CHECK(*_ex);
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                                  replace('@PORT_TYPE@', portInstance.getType())
                buf += portBuf

            if (len(provides) > 0):
                buf += """
   gov_cca_Port_deleteRef(port, _ex); port = NULL; SIDL_CHECK(*_ex);
"""
            
# Use port(s) code
            for portInstance in uses:
                portBuf = """
  /* Register a use port of type @PORT_TYPE@ with port name @PORT_INSTANCE@ */  
   gov_cca_Services_registerUsesPort(pd->"""+self.servicesVariable+""",   
                                     "@PORT_INSTANCE@", /* the name seen by the user */
                                     "@PORT_TYPE@", /* sidl name of the port type. */
                                     typeMap, /* extra properties */
                                     _ex); SIDL_CHECK(*_ex);
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
                buf += portBuf
            buf += """
   gov_cca_TypeMap_deleteRef(typeMap,_ex); typeMap = NULL; SIDL_CHECK(*_ex);
"""   
# Finish up, and replace vars

        buf +="""
   /* Cast myself to gov.cca.ComponentRelease */
   compRelease = gov_cca_ComponentRelease__cast(self, _ex); SIDL_CHECK(*_ex);
   gov_cca_Services_registerForRelease(pd->"""+self.servicesVariable+""", 
                                       compRelease, _ex);
   SIDL_CHECK(*_ex);
   gov_cca_ComponentRelease_deleteRef(compRelease, _ex); compRelease = NULL; 
   SIDL_CHECK(*_ex);
   return;

   /* exceptions exit through here, where we clean up memory references. */
EXIT:;
   if (dr_services != 0) { 
     gov_cca_Services_deleteRef(services, &throwaway_excpt); 
     SIDL_CLEAR(throwaway_excpt);
     services = NULL;
   }
   if (compRelease != NULL) {
     gov_cca_ComponentRelease_deleteRef(compRelease, &throwaway_excpt); 
     SIDL_CLEAR(throwaway_excpt);
     compRelease = NULL;
   }
"""
        if (len(provides) + len(uses) > 0):
            buf += """
   if (typeMap != NULL) {
     gov_cca_TypeMap_deleteRef(typeMap, &throwaway_excpt); 
     SIDL_CLEAR(throwaway_excpt);
     port = NULL;
   }
   if (port != NULL) {
     gov_cca_Port_deleteRef(port, &throwaway_excpt); 
     SIDL_CLEAR(throwaway_excpt);
     port = NULL;
   }
"""
        buf += """
   return;

/* """+self.protKey+""".end(@CMPT_TYPE@."""+self.boccaServicesMethod+""") */
/* DO-NOT-DELETE splicer.end(@CMPT_TYPE@."""+self.boccaServicesMethod+""") */
"""
        buf = buf.replace('@CMPT_TYPE_UBAR@', cmpt_ubar).\
                  replace('@CMPT_TYPE@', componentSymbol)
        return buf

#---------------------------------------------------------------------------------
    def getAuxiliaryReleaseServicesMethod(self, componentSymbol, provides=[], uses=[]):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
/*  DO-NOT-DELETE splicer.begin(@CMPT_TYPE@."""+self.boccaReleaseMethod+""") */
/* DO-NOT-EDIT-BOCCA */
/*  """+self.protKey+""".begin(@CMPT_TYPE@."""+self.boccaReleaseMethod+""") */

   struct @CMPT_TYPE_UBAR@__data *pd;
   sidl_BaseInterface throwaway_excpt = NULL;
   sidl_BaseInterface dummy_excpt = NULL;
   char *errMsg=NULL;
   /* our policy is to trap and optionally print all port-related messages,
      attempting to eliminate all ports. */

"""
# Un-provide Provide port(s) code
        for portInstance in provides:
            portBuf = """
   /* UN-Provide a @PORT_TYPE@ port with port name @PORT_INSTANCE@ */
   gov_cca_Services_removeProvidesPort(services, "@PORT_INSTANCE@", 
                                       &throwaway_excpt);
   errMsg = "Error: Could not removeProvidesPort(\\"@PORT_INSTANCE@\\")";
   @CMPT_TYPE_UBAR@_checkException(self, throwaway_excpt, errMsg, FALSE, 
                                   &dummy_excpt);
"""
            portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
            buf += portBuf

# Unregister uses port(s) code
        for portInstance in uses:
            portBuf = """
  /* Un-Register a use port of type @PORT_TYPE@ with port name @PORT_INSTANCE@ */  
   gov_cca_Services_unregisterUsesPort(services, "@PORT_INSTANCE@", 
                                       &throwaway_excpt);
   errMsg= "Error: Could not unregisterUsesPort(\\"@PORT_INSTANCE@\\")";
   @CMPT_TYPE_UBAR@_checkException(self, throwaway_excpt, errMsg, FALSE, 
                                   &dummy_excpt);
"""
            portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
            buf += portBuf
# Finish up, and substitute values
        buf += """
   services = NULL;
   pd = @CMPT_TYPE_UBAR@__get_data(self);
   if (pd == NULL) {
     SIDL_THROW(*_ex, sidl_SIDLException, 
        "NULL data pointer in @CMPT_TYPE@ """+self.boccaServicesMethod+"""");
   }
   gov_cca_Services_deleteRef(pd->"""+self.servicesVariable+""", _ex); 
   SIDL_CHECK(*_ex);
   pd->"""+self.servicesVariable+""" = NULL;
   return;

EXIT:;
   return;
/*  """+self.protKey+""".end(@CMPT_TYPE@."""+self.boccaReleaseMethod+""") */
/*  DO-NOT-DELETE splicer.end(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")) */
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
        return buf
    
#---------------------------------------------------------------------------------
    def getReleaseMethod(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        methodName = 'impl_'+ cmpt_ubar + '_' + self.boccaReleaseMethod
        buf = """ 
  /* DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.releaseServices) */

  /*  Insert-UserCode-Here {@CMPT_TYPE@.releaseServices} (releaseServices method) */

  /* """+self.onceKey+""".begin(@CMPT_TYPE@.releaseServices) */
    """+methodName+"""(self, services, _ex); SIDL_CHECK(*_ex);
    return;
  /* """+self.onceKey+""".end(@CMPT_TYPE@.releaseServices) */

EXIT:;
    /* Insert additional exception cleanup here if needed. */
    return;

  /* DO-NOT-DELETE splicer.end(@CMPT_TYPE@.releaseServices) */
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
#---------------------------------------------------------------------------------
    def getCheckExceptionMethod(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
/*  DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.checkException) */
/* DO-NOT-EDIT-BOCCA */
/*  """+self.protKey+""".begin(@CMPT_TYPE@.checkException) */
#ifdef _BOCCA_STDERR
   sidl_BaseException be = NULL;
   char *etext=NULL;
#endif
   
   if (SIDL_CATCH(excpt, "sidl.BaseException")) {
#ifdef _BOCCA_STDERR
      be  = sidl_BaseException__cast(excpt, _ex); SIDL_CLEAR(*_ex);
      etext = sidl_BaseException_getNote(be, _ex); SIDL_CLEAR(*_ex);
      fprintf(stderr, "@CMPT_TYPE@: %s \\n%s\\n", msg,etext);
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
   
/*  """+self.protKey+""".end(@CMPT_TYPE@.checkException) */
    
/*  DO-NOT-DELETE splicer.end(@CMPT_TYPE@.checkException) */
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
        return buf
    
#---------------------------------------------------------------------------------
    def getForceUsePortCode(self, componentSymbol, numitems=0, depthstring=""):
        buf = """
  /* DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""") */
/* DO-NOT-EDIT-BOCCA */
  /* """+self.protKey+""".begin(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""") */
    (void)self;
"""
        count=0
        for i in range(1,numitems+1):
            buf += "    (void)dummy"+str(count)+";\n"
            count += 1
        buf += """
  /* """+self.protKey+""".end(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""") */
  /* DO-NOT-DELETE splicer.end(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""") */
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
    
#---------------------------------------------------------------------------------
    def getGoCode(self, componentSymbol, uses=[]):
        buf = """
/* DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.go) */

  /* User action portion is in the middle at the next Insert-UserCode-Here line. */
@BOCCA_GO_PROLOG@


  /* When this block is rewritten by the user, we will not change it.
     All port instances should be rechecked for NULL before calling in user code.
     Not all ports need be connected in arbitrary use.
     The port instance names used in registerUsesPort appear as local variable
     names here.
     'return' should not be used here; set bocca_status instead.
   */

  /* Insert-UserCode-Here {@CMPT_TYPE@.go} */

  /* BEGIN REMOVE ME BLOCK */
  BOCCA_FPRINTF(stderr, 
        "USER FORGOT TO FILL IN THEIR GO FUNCTION %s:%d.\\n",
        __FILE__,__LINE__);
  /* END REMOVE ME BLOCK */

  /* If unknown exceptions in the user code are tolerable and restart is ok, 
     set bocca_status -1 instead.
     -2 means the component is so confused that it and probably the component 
     or application should be destroyed.
   */

@BOCCA_GO_EPILOG@

/* Insert-User-Exception-Cleanup-Here */

  return bocca_status;
/* DO-NOT-DELETE splicer.end(@CMPT_TYPE@.go) */
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        prolog = self.getGoPrologCode(componentSymbol, uses)
        epilog = self.getGoEpilogCode(componentSymbol, uses)
        buf=buf.replace("@BOCCA_GO_PROLOG@", prolog)
        buf=buf.replace("@BOCCA_GO_EPILOG@", epilog)
        return buf

#---------------------------------------------------------------------------------
# The prolog does not set policy for handling unconnected ports.
# It handles these exceptions and sets easy to use flags.
# In the case of casting exceptions, somebody lied somewhere (or got a string wrong)
# and we forward the exception appropriately as we cannot continue correctly.
    def getGoPrologCode(self, componentSymbol, uses=[]):
        cmpt_ubar = componentSymbol.replace('.', '_')
        decls="""
  gov_cca_Port port = NULL;
  gov_cca_Services services = NULL;
  sidl_BaseInterface throwaway_excpt = NULL;
  sidl_BaseInterface dummy_excpt = NULL;
  struct @CMPT_TYPE_UBAR@__data *pd = NULL;
  const char *errMsg = NULL;
"""
        buf = """

  /* Insert-User-Declarations-Here */

/* """+self.protKey+""".begin(@CMPT_TYPE@.go:boccaGoProlog) */

  int bocca_status = 0;
  /* The user's code should set bocca_status 0 if computation proceeded ok.
  // The user's code should set bocca_status -1 if computation failed but might
  // succeed on another call to go(), e.g. wheh a required port is not yet connected.
  // The user's code should set bocca_status -2 if the computation failed and can
  // never succeed in a future call.
  // The users's code should NOT use return in this function;
  // Exceptions that are not caught in user code will be converted to status -2.
  */
"""
# Add local uses ports variables:
        if len(uses) > 0:
            buf += """
@DECLS@

  pd = @CMPT_TYPE_UBAR@__get_data(self);
  if (pd == NULL) {
    SIDL_THROW(*_ex, sidl_SIDLException, 
       "NULL object data pointer in @CMPT_TYPE@.go()");
  }
  services = pd->"""+self.servicesVariable+""";
  if (services == NULL) {
    SIDL_THROW(*_ex, sidl_SIDLException, 
        "NULL pd->"""+self.servicesVariable+""" pointer in @CMPT_TYPE@.go()");
  }
"""
            # Use port(s) code
            for portInstance in uses:
                portnativetype = portInstance.getType().replace('.', '_')
                portBuf = """
  /* Use a @PORT_TYPE@ port with port name @PORT_INSTANCE@ */
  port = gov_cca_Services_getPort(services,"@PORT_INSTANCE@", &throwaway_excpt);
  if (throwaway_excpt != NULL) {
    port = NULL;
    errMsg="go() getPort(@PORT_INSTANCE@) failed.";
    @CMPT_TYPE_UBAR@_checkException(self, throwaway_excpt, errMsg, 
                                    FALSE, &dummy_excpt);
    /* we will continue with port NULL (never successfully assigned) and set a flag. */
    BOCCA_FPRINTF(stderr, 
         "@CMPT_TYPE@: Error calling getPort(\\"@PORT_INSTANCE@\\") at %s:%d. Continuing.\\n",
         __FILE__ , __LINE__ -8 );
  }
"""
                decls +="""
  @NATIVE_PORT_TYPE@ @PORT_INSTANCE@ = NULL;	/* non-null if specific uses port obtained. */
  int @PORT_INSTANCE@_fetched = FALSE;		/* true if releaseport is needed for this port. */
"""
                portBuf += """
  if ( port != NULL ) {
    @PORT_INSTANCE@_fetched = TRUE; /* even if the next cast fails, must releasePort. */
    errMsg="@CMPT_TYPE@: Error casting gov.cca.Port @PORT_INSTANCE@ to type @PORT_TYPE@";
    @PORT_INSTANCE@ = @NATIVE_PORT_TYPE@__cast(port, _ex); SIDL_CHECK(*_ex);
    gov_cca_Port_deleteRef(port,_ex); port = NULL; SIDL_CHECK(*_ex);
  }
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType()).\
                              replace('@NATIVE_PORT_TYPE@', portnativetype)
                decls = decls.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType()).\
                              replace('@NATIVE_PORT_TYPE@', portnativetype)
                buf += portBuf
            # end for uName
            buf += """
"""
        # Finish up, and replace class vars
        buf +="""
/* """+self.protKey+""".end(@CMPT_TYPE@.go:boccaGoProlog) */

"""
        buf = buf.replace('@DECLS@',decls).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar).\
                  replace('@CMPT_TYPE@', componentSymbol)
        return buf

#---------------------------------------------------------------------------------
    def getGoEpilogCode(self, componentSymbol, uses=[]):

        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
EXIT:; /* target point for normal and error cleanup. do not delete. */
/* """+self.protKey+""".begin(@CMPT_TYPE@.go:boccaGoEpilog) */
"""
# release local uses ports variables:
        if len(uses) > 0:
            # release port(s) code
            for portInstance in uses:
                portnativetype = portInstance.getType().replace('.', '_')
                portBuf = """
  /* release @PORT_INSTANCE@ */
  if (@PORT_INSTANCE@_fetched) {
    @PORT_INSTANCE@_fetched = FALSE;
    gov_cca_Services_releasePort(services,"@PORT_INSTANCE@",&throwaway_excpt);
    if ( throwaway_excpt != NULL) {
      errMsg= "@CMPT_TYPE@: Error calling releasePort(\\"@PORT_INSTANCE@\\"). Continuing.";
      @CMPT_TYPE_UBAR@_checkException(self, throwaway_excpt, errMsg, FALSE, &dummy_excpt);
    }
    if (@PORT_INSTANCE@ != NULL) {
      @NATIVE_PORT_TYPE@_deleteRef(@PORT_INSTANCE@, &throwaway_excpt);
      errMsg = "Error in @NATIVE_PORT_TYPE@_deleteRef for @CMPT_TYPE@ port @PORT_INSTANCE@";
      @CMPT_TYPE_UBAR@_checkException(self, throwaway_excpt, errMsg, FALSE, &dummy_excpt);
      @PORT_INSTANCE@ = NULL;
    }
  }
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@NATIVE_PORT_TYPE@', portnativetype)
                buf += portBuf
            # end for uName
            buf += """
"""
        # Finish up, and replace class vars
        buf +="""
/* """+self.protKey+""".end(@CMPT_TYPE@.go:boccaGoEpilog) */
"""
        buf = buf.replace('@CMPT_TYPE_UBAR@', cmpt_ubar).\
                  replace('@CMPT_TYPE@', componentSymbol)
        return buf

