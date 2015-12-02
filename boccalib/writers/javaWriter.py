from writers.sourceWriter import SourceWriter

def getWriterParameters():
    return (JavaWriter.language, JavaWriter.babelVersions, JavaWriter.dialect)
 
class JavaWriter(SourceWriter):
    language = 'java'
    dialect = 'standard'
    commentLineStart = "// "
    babelVersions = ['1.0.X', '1.1.X', '1.2.X', '1.4.X', '1.5.X']

    def __init__(self, kind = 'component'):
        SourceWriter.__init__(self, kind)

#---------------------------------------------------------------------------------
    def getImplHeaderCode(self, componentSymbol):
        buf = """
    // DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._data)

    // """+self.protKey+""".begin(@CMPT_TYPE@._data)
    gov.cca.Services    """+self.servicesVariable+""";
    public boolean bocca_print_errs = true;
    // """+self.protKey+""".end(@CMPT_TYPE@._data)
    // DO-NOT-DELETE splicer.end(@CMPT_TYPE@._data)
"""    
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf

#---------------------------------------------------------------------------------
    def getHeaderCode(self, componentSymbol):
        buf ="// "+componentSymbol
        return buf
        
#---------------------------------------------------------------------------------
    def getSetServicesCode(self, componentSymbol):
        buf = """ 
  // DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.setServices)

  // Insert-Code-Here {@CMPT_TYPE@.setServices} (setServices method prolog)

  // """+self.onceKey+""".begin(@CMPT_TYPE@.setServices)
     """+self.boccaServicesMethod+"""(services); 
  // """+self.onceKey+""".end(@CMPT_TYPE@.setServices)

  // Insert-Code-Here {@CMPT_TYPE@.setServices} (setServices method epilog)

  // DO-NOT-DELETE splicer.end(@CMPT_TYPE@.setServices)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf

#---------------------------------------------------------------------------------
# Set services is expected to forward exceptions if the framework generates them.
# There is no reason to believe a component can handle framework exceptions other
# than when the component is asking for a special service port the framework does not provide.
#
    def getAuxiliarySetServicesMethod(self, componentSymbol, provides=[], uses=[]):
        buf = """
// DO-NOT-DELETE splicer.begin(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
// DO-NOT-EDIT-BOCCA
// """+self.protKey+""".begin(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
"""
# Add ports declarations (if needed)
        if (len(provides) + len(uses) > 0):
            buf += """
   gov.cca.TypeMap typeMap;
   gov.cca.Port    port;
"""
# Component Registration code            
        buf +="""
   this."""+self.servicesVariable+""" = services;
"""
        if (len(provides) + len(uses) > 0):
            buf += """
   typeMap = this."""+self.servicesVariable+""".createTypeMap();
"""
            if (len(provides) > 0):
                buf +="""
   port = (gov.cca.Port)(this);

"""
# Provide port(s) code
            for portInstance in provides:
                portBuf = """
  // Provide a @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
   try{
      this."""+self.servicesVariable+""".addProvidesPort(port, // the implementing object
                                      "@PORT_INSTANCE@", // the name the user sees
                                      "@PORT_TYPE@", // the sidl name of the port type
                                      typeMap); // extra properties
   } catch ( gov.cca.CCAException.Wrapper ex )  {
      String msg = "Error calling addProvidesPort(port,\\"@PORT_INSTANCE@\\", "
          + "\\"@PORT_TYPE@\\", typeMap) ";
      ex.add(msg);
      throw ex;
   }    
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                                  replace('@PORT_TYPE@', portInstance.getType())
                buf += portBuf
            
# Use port(s) code
            for portInstance in uses:
                portBuf = """
  // Use a @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
   try{
      this."""+self.servicesVariable+""".registerUsesPort("@PORT_INSTANCE@", // name the user sees
                                       "@PORT_TYPE@", // sidl name of the port type
                                       typeMap); // extra properties
   } catch ( gov.cca.CCAException.Wrapper ex )  {
      String msg = "Error calling registerUsesPort(\\"@PORT_INSTANCE@\\", "
              + "\\"@PORT_TYPE@\\", typeMap) ";
      ex.add(msg);
      throw ex;
   }
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
                buf += portBuf
            buf += """
"""   
# Finish up, register for component release, and replace vars

        buf +="""
   gov.cca.ComponentRelease cr = (gov.cca.ComponentRelease)this; // CAST
   this."""+self.servicesVariable+""".registerForRelease(cr);
   return;
// """+self.protKey+""".end(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
// DO-NOT-DELETE splicer.end(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf

#---------------------------------------------------------------------------------
    def getGoCode(self, componentSymbol, uses=[]):
        buf = """
// DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.go)
@BOCCA_GO_PROLOG@

  // If this try/catch block is rewritten by the user, we will not change it.
  try {
    // All port instances may be rechecked for null before calling in user code.
    // Java will throw a null object exception when using the port if it's null.
    // The port instance names used in registerUsesPort appear as local variable
    // names here.

    // Insert-UserCode-Here {@CMPT_TYPE@.go} 

    // BEGIN REMOVE ME BLOCK
    sidl.SIDLException ex = new sidl.SIDLException();
    ex.setNote("USER FORGOT TO FILL IN THEIR FUNCTION @CMPT_TYPE@.go()");
    sidl.BaseException.Wrapper bex =
      (sidl.BaseException.Wrapper)sidl.BaseException.Wrapper._cast(ex);
    throw bex;
    // END REMOVE ME BLOCK


  } catch (sidl.BaseException.Wrapper ex) {
    bocca_status = -2;
    if (bocca_print_errs) {
      System.err.println("SIDL Exception in user go code: "+ ex.getNote() );
      System.err.println("Returning 2 from go()");
    }
  } catch (java.lang.Exception jex) {
    bocca_status = -2;
    if (bocca_print_errs) {
      if (((sidl.BaseInterface)jex).isType("sidl.BaseException")) {
        System.err.println("sidl Exception in user go code: " 
                           + ((sidl.BaseException)jex).getNote() );
      } else {
        System.err.println("java Exception in user go code: "+ jex.getMessage());
      }
      System.err.println("Returning 2 from go()");
    }
    // If unknown exceptions in the user code are tolerable and restart is ok, 
    // use bocca_status -1 instead.
    // 2 means the component is so confused that it and probably the application
    // should be destroyed.
  }

@BOCCA_GO_EPILOG@
// DO-NOT-DELETE splicer.end(@CMPT_TYPE@.go)
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
    def getGoPrologCode(self, componentSymbol, uses={}):
        buf = """

// """+self.protKey+""".begin(@CMPT_TYPE@.go:boccaGoProlog)
  int bocca_status = 0;
  // The user's code should set bocca_status 0 if computation proceeded ok.
  // The user's code should set bocca_status -1 if computation failed but might
  // succeed on another call to go(), e.g. wheh a required port is not yet connected.
  // The user's code should set bocca_status -2 if the computation failed and can
  // never succeed in a future call.
  // The users's code should NOT use return in this function;
  // Exceptions that are not caught in user code will be converted to status 2.
"""
# Add local uses ports variables:
        if len(uses) > 0:
            buf += """
  gov.cca.Port port = null;
"""
            # Use port(s) code
            for portInstance in uses:
                portnativetype = portInstance.getType()
                portBuf = """
  boolean @PORT_INSTANCE@_fetched = false;
  if (bocca_status == 0) { // skip further getports if problem occurs.
    // Use a @PORT_TYPE@ port with port name @PORT_INSTANCE@, unless we've hit 
    // a problem already.
    try{
      port = this."""+self.servicesVariable+""".getPort("@PORT_INSTANCE@");
    } catch ( gov.cca.CCAException.Wrapper ex )  {
      // we will continue with port nil (never successfully assigned) and set a flag.
      if (bocca_print_errs) {
        System.err.println("Error calling getPort(\\"@PORT_INSTANCE@\\")" 
                          + ex.getNote());
        System.err.println("Continuing without @PORT_INSTANCE@");
      }
    }
    @NATIVE_PORT_TYPE@ @PORT_INSTANCE@;
    if ( port != null  ) {
      @PORT_INSTANCE@_fetched = true; // even if the next cast fails, must release.
      @PORT_INSTANCE@ = ( @NATIVE_PORT_TYPE@.Wrapper ) 
                  @NATIVE_PORT_TYPE@.Wrapper._cast((gov.cca.Port.Wrapper)port);
      if (@PORT_INSTANCE@ == null) {
        if (bocca_print_errs) {
          System.err.println("@CMPT_TYPE@: Error casting gov.cca.Port "
                  + "@PORT_INSTANCE@ to type @NATIVE_PORT_TYPE@");
        }
        bocca_status = -1;
      } 
    } 
  } 
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType()).\
                              replace('@NATIVE_PORT_TYPE@', portnativetype)
                buf += portBuf
            # end for uName
            buf += """
"""   
        # Finish up, and replace class vars
        buf +="""
  if (bocca_status == 0) { 
// skip user code if we already have an unexpected error. go to cleanup.
// """+self.protKey+""".end(@CMPT_TYPE@.go:boccaGoProlog)

"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
#---------------------------------------------------------------------------------
    def getGoEpilogCode(self, componentSymbol, uses=[]):

        buf = """
// """+self.protKey+""".begin(@CMPT_TYPE@.go:boccaGoEpilog)
  } // cleanup
"""
# release local uses ports variables:
        if len(uses) > 0:
            # release port(s) code
            for portInstance in uses:
                portBuf = """
  // release @PORT_INSTANCE@ 
  if (@PORT_INSTANCE@_fetched) {
    @PORT_INSTANCE@_fetched = false;
    try{
      this."""+self.servicesVariable+""".releasePort("@PORT_INSTANCE@");
    } catch ( gov.cca.CCAException.Wrapper ex )  {
      if (bocca_print_errs) {
        System.err.println("@CMPT_TYPE@: Error calling "
            + "releasePort(\\"@PORT_INSTANCE@\\"): " + ex.getNote()); 
      }
    }
    // java port reference will be dropped when function exits, 
    // but we must tell framework.
  }
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName())
                buf += portBuf
            # end for uName
            buf += """
"""   
        # Finish up, and replace class vars
        buf +="""
  return bocca_status;
// """+self.protKey+""".end(@CMPT_TYPE@.go:boccaGoEpilog)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
#---------------------------------------------------------------------------------
    def getAuxiliaryReleaseServicesMethod(self, componentSymbol, provides=[], uses=[]):
        buf = """
  // DO-NOT-EDIT-BOCCA
  // DO-NOT-DELETE splicer.begin(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
  // """+self.protKey+""".begin(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")

   this."""+self.servicesVariable+"""=null;
"""
# Un-provide provides ports
        for portInstance in provides:
           portBuf = """
  // Un-provide @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
  try{
    services.removeProvidesPort("@PORT_INSTANCE@");
  } catch ( gov.cca.CCAException.Wrapper ex )  {
    if (bocca_print_errs) {
      System.err.print("@CMPT_TYPE@: Error calling removeProvidesPort" 
          + "(\\"@PORT_INSTANCE@\\"): " + ex.getNote());
    }
  }
"""
           portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                             replace('@PORT_TYPE@', portInstance.getType())
           buf += portBuf
           
# Use port(s) code
        for portInstance in uses:
           portBuf = """
  // Release @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
  try{
    services.unregisterUsesPort("@PORT_INSTANCE@");
  } catch ( gov.cca.CCAException.Wrapper ex )  {
    if (bocca_print_errs) {
      System.err.println("@CMPT_TYPE@: Error calling unregisterUsesPort"
          + "(\\"@PORT_INSTANCE@\\"): " +ex.getNote());
    }
  }
"""
           portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                             replace('@PORT_TYPE@', portInstance.getType())
           buf += portBuf
           
# Finish up, and substitute values
        buf += """
   return;
  // """+self.protKey+""".end(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
    
  // DO-NOT-DELETE splicer.end(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
    
#---------------------------------------------------------------------------------
    def getReleaseMethod(self, componentSymbol):
        buf = """
  // DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.releaseServices)

  // Insert-Code-Here {@CMPT_TYPE@.releaseServices} (releaseServices method prolog)

  // """+self.onceKey+""".end(@CMPT_TYPE@.releaseServices)
     """+self.boccaReleaseMethod+"""(services); 
  // """+self.onceKey+""".end(@CMPT_TYPE@.releaseServices)

  // Insert-Code-Here {@CMPT_TYPE@.releaseServices} (releaseServices method epilog)

  // DO-NOT-DELETE splicer.end(@CMPT_TYPE@.releaseServices)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
    
#---------------------------------------------------------------------------------
    def getForceUsePortCode(self, componentSymbol, numitems=0, depthstring=""):
        buf = """
  // DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""")
  // DO-NOT-EDIT-BOCCA
  // """+self.protKey+""".begin(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""")
"""
        count=0
        if numitems > 0:
            buf += "    Object o;\n"
        for i in range(0,numitems):
            buf += "    o = dummy"+str(count)+";\n"
            count += 1
        buf += """
  // """+self.protKey+""".end(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""")
  // DO-NOT-DELETE splicer.end(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""")
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
    

