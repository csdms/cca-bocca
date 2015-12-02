from writers.sourceWriter import SourceWriter

def getWriterParameters():
    return (CxxWriter.language, CxxWriter.babelVersions, CxxWriter.dialect)
 
class CxxWriter(SourceWriter):
    language = 'cxx'
    dialect = 'standard'
    commentLineStart = "// "
    babelVersions = ['1.0.X', '1.1.X', '1.2.X', '1.4.X', '1.5.X']
    usecio=False

    def __init__(self, kind = 'component'):
        SourceWriter.__init__(self, kind)

    def iolines(self, clines, cxxlines):
        if self.usecio:
            return clines
        return cxxlines

#---------------------------------------------------------------------------------
    def getImplHeaderCode(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf ="""
  // DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._includes)

  // Insert-UserCode-Here {@CMPT_TYPE@._includes:prolog} (additional includes or code)

  // """+self.protKey+""".begin(@CMPT_TYPE@._includes)

#define _BOCCA_CTOR_MESSAGES 0
  // If -D_BOCCA_STDERR is given to the compiler, diagnostics print to stderr.
  // In production use, probably want not to use -D_BOCCA_STDERR.
#ifdef _BOCCA_STDERR
"""+self.iolines("""
#include <cstdio>
#define BOCCA_FPRINTF fprintf
""","""
#include <iostream>
""")+"""
#ifdef _BOCCA_CTOR_PRINT
#undef _BOCCA_CTOR_MESSAGES
#define _BOCCA_CTOR_MESSAGES 1
#endif // _BOCCA_CTOR_PRINT 
#else  // _BOCCA_STDERR
"""+self.iolines("""
#define BOCCA_FPRINTF this->boccaPrintNothing
""","""
""")+"""
#endif // _BOCCA_STDERR
"""+self.iolines("""
  // A function that absorbs arguments and prints nothing. Exists because
  // macro varargs in c++ is not standard.
int
@NATIVE_CMPT_TYPE@_impl::boccaPrintNothing(void *v, const char * s, ...)
{
  (void)v; (void)s;
  return 0;
}
""","""
""")+"""

  // If -D_BOCCA_BOOST is given to the compiler, exceptions and diagnostics 
  // will include function names for boost-understood compilers.
  // If boost is not available (and therefore ccaffeine is not in use), 
  // -D_BOCCA_BOOST can be omitted and function names will not be included in 
  // messages.
#ifndef _BOCCA_BOOST
#define BOOST_CURRENT_FUNCTION ""
#else
#include <boost/current_function.hpp>
#endif

  // This is intended to simplify exception throwing as SIDL_THROW does for C.
#define BOCCA_THROW_CXX(EX_CLS, MSG) \\
{ \\
    EX_CLS ex = EX_CLS::_create(); \\
    ex.setNote( MSG ); \\
    ex.add(__FILE__, __LINE__, BOOST_CURRENT_FUNCTION); \\
    throw ex; \\
}

  // This simplifies exception extending and rethrowing in c++, like 
  // SIDL_CHECK in C. EX_OBJ must be the caught exception and is extended with 
  // msg and file/line/func added. Continuing the throw is up to the user.
#define BOCCA_EXTEND_THROW_CXX(EX_OBJ, MSG, LINEOFFSET) \\
{ \\
  std::string msg = std::string(MSG) + std::string(BOOST_CURRENT_FUNCTION); \\
  EX_OBJ.add(__FILE__,__LINE__ + LINEOFFSET, msg); \\
}


  // """+self.protKey+""".end(@CMPT_TYPE@._includes)

  // Insert-UserCode-Here {@CMPT_TYPE@._includes:epilog} (additional includes or code)

  // DO-NOT-DELETE splicer.end(@CMPT_TYPE@._includes)
"""
        compnativetype = componentSymbol.replace('.', '::')
	buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
		  replace('@NATIVE_CMPT_TYPE@', compnativetype).\
		  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
	return buf

#---------------------------------------------------------------------------------
    def getHeaderCode(self, componentSymbol):
	buf = """
  // DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._implementation)

  // Insert-UserCode-Here(@CMPT_TYPE@._implementation)

  // """+self.protKey+""".begin(@CMPT_TYPE@._implementation)
  
   gov::cca::Services    """+self.servicesVariable+"""; // our cca handle.
"""+self.iolines("""
   int boccaPrintNothing(void *, const char *, ...); // util. function for cio
""",""" 
""")+"""
  // """+self.protKey+""".end(@CMPT_TYPE@._implementation)

  // DO-NOT-DELETE splicer.end(@CMPT_TYPE@._implementation)
"""    
	buf = buf.replace('@CMPT_TYPE@', componentSymbol)
	return buf
	
#---------------------------------------------------------------------------------
    def getDestructorCode(self, componentSymbol):
        buf = """
  // DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._dtor)
  // Insert-UserCode-Here {@CMPT_TYPE@._dtor} (destructor method) 
    
  // """+self.onceKey+""".begin(@CMPT_TYPE@._dtor) 
   #if _BOCCA_CTOR_MESSAGES
"""+self.iolines("""
     BOCCA_FPRINTF(stderr, "DTOR @CMPT_TYPE@: %s destroying %p\\n", 
                   BOOST_CURRENT_FUNCTION , this);
""","""
     std::cerr << "DTOR @CMPT_TYPE@: " << BOOST_CURRENT_FUNCTION 
               << " destructing " << this << std::endl;
""")+"""
   #endif // _BOCCA_CTOR_MESSAGES 
  // """+self.onceKey+""".end(@CMPT_TYPE@._dtor) 

  // DO-NOT-DELETE splicer.end(@CMPT_TYPE@._dtor)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
            
#---------------------------------------------------------------------------------
    def getConstructorCode(self, componentSymbol):
        buf = """
  // DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._ctor)
    
  // Insert-UserCode-Here {@CMPT_TYPE@._ctor:prolog} (constructor method) 

  // """+self.onceKey+""".begin(@CMPT_TYPE@._ctor)
   #if _BOCCA_CTOR_MESSAGES
"""+self.iolines("""
     BOCCA_FPRINTF(stderr, "CTOR @CMPT_TYPE@: %s constructing %p\\n", 
                   BOOST_CURRENT_FUNCTION , this );
""","""
     std::cerr << "CTOR @CMPT_TYPE@: " << BOOST_CURRENT_FUNCTION 
               << " constructing " << this << std::endl;
""")+"""
   #endif // _BOCCA_CTOR_MESSAGES
  // """+self.onceKey+""".end(@CMPT_TYPE@._ctor)

  // Insert-UserCode-Here {@CMPT_TYPE@._ctor:epilog} (constructor method)

  // DO-NOT-DELETE splicer.end(@CMPT_TYPE@._ctor)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf

#---------------------------------------------------------------------------------
    def getSetServicesCode(self, componentSymbol):
        buf = """ 
  // DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.setServices)

  // Insert-UserCode-Here{@CMPT_TYPE@.setServices:prolog}

  // """+self.onceKey+""".begin(@CMPT_TYPE@.setServices)
     """+self.boccaServicesMethod+"""(services); 
  // """+self.onceKey+""".end(@CMPT_TYPE@.setServices)
  
  // Insert-UserCode-Here{@CMPT_TYPE@.setServices:epilog}

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
	cmpt_ubar = componentSymbol.replace('.', '_')
	buf = """
  // DO-NOT-DELETE splicer.begin(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
  // DO-NOT-EDIT-BOCCA
  // """+self.protKey+""".begin(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
"""
# Add ports declarations (if needed)
	if (len(provides) + len(uses) > 0):
	    buf += """
  gov::cca::TypeMap typeMap;
  gov::cca::Port    port;
"""
# Component Registration code            
	buf +="""
  this->"""+self.servicesVariable+""" = services;
"""
	if (len(provides) + len(uses) > 0):
	    buf += """
  typeMap = this->"""+self.servicesVariable+""".createTypeMap();
"""
	    if (len(provides) > 0):
		buf +="""
  port = ::babel_cast< gov::cca::Port>(*this);
  if (port._is_nil()) {
    BOCCA_THROW_CXX( ::sidl::SIDLException , 
                     "@CMPT_TYPE@: Error casting self to gov::cca::Port");
  } 

"""
# Provide port(s) code
	    for portInstance in provides:
		portBuf = """
  // Provide a @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
  try{
    this->"""+self.servicesVariable+""".addProvidesPort(
                   port,              // implementing object
                   "@PORT_INSTANCE@", // port instance name
                   "@PORT_TYPE@",     // full sidl type of port
                   typeMap);          // properties for the port
  } catch ( ::gov::cca::CCAException ex )  {
    BOCCA_EXTEND_THROW_CXX(ex, 
        "@CMPT_TYPE@: Error calling addProvidesPort(port,"
        "\\"@PORT_INSTANCE@\\", \\"@PORT_TYPE@\\", typeMap) ", -2);
    throw;
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
    this->"""+self.servicesVariable+""".registerUsesPort(
                   "@PORT_INSTANCE@", // port instance name
                   "@PORT_TYPE@",     // full sidl type of port
                    typeMap);         // properties for the port
  } catch ( ::gov::cca::CCAException ex )  {
    BOCCA_EXTEND_THROW_CXX(ex,
       "@CMPT_TYPE@: Error calling registerUsesPort(\\"@PORT_INSTANCE@\\", "
       "\\"@PORT_TYPE@\\", typeMap) ", -2);
    throw;
  }
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
                buf += portBuf
            buf += """
"""   
# Finish up, register for component release, and replace vars

        buf +="""
  gov::cca::ComponentRelease cr = 
        ::babel_cast< gov::cca::ComponentRelease>(*this);
  this->"""+self.servicesVariable+""".registerForRelease(cr);
  return;
  // """+self.protKey+""".end(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
    
  // DO-NOT-DELETE splicer.end(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
"""
        buf = buf.replace('@CMPT_TYPE_UBAR@', cmpt_ubar).\
                  replace('@CMPT_TYPE@', componentSymbol)
        return buf

#---------------------------------------------------------------------------------
    def getGoCode(self, componentSymbol, uses=[]):
        buf = """
// DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.go)
// User editable portion is in the middle at the next Insert-UserCode-Here line.
@BOCCA_GO_PROLOG@

  // When this try/catch block is rewritten by the user, we will not change it.
  try {

    // All port instances should be rechecked for ._not_nil before calling in 
    // user code. Not all ports need be connected in arbitrary use.
    // The uses ports appear as local variables here named exactly as on the 
    // bocca commandline.

    // Insert-UserCode-Here {@CMPT_TYPE@.go} 

    // REMOVE ME BLOCK.begin(@CMPT_TYPE@.go)
"""+self.iolines("""
    BOCCA_FPRINTF(stderr,"USER FORGOT TO FILL IN THEIR GO FUNCTION HERE.\\n");
""","""
#ifdef _BOCCA_STDERR
    std::cerr << "USER FORGOT TO FILL IN THEIR GO FUNCTION HERE." << std::endl;
#endif
""")+"""
    // REMOVE ME BLOCK.end(@CMPT_TYPE@.go)

  } 
  // If unknown exceptions in the user code are tolerable and restart is ok, 
  // return -1 instead. -2 means the component is so confused that it and 
  // probably the application should be destroyed.
  // babel requires exact exception catching due to c++ binding of interfaces.
  catch (gov::cca::CCAException ex) {
    bocca_status = -2;
    std::string enote = ex.getNote();
"""+self.iolines("""
    BOCCA_FPRINTF(stderr,"CCAException in user go code: %s\\n",enote.c_str());
    BOCCA_FPRINTF(stderr,"Returning -2 from go()");
""","""
#ifdef _BOCCA_STDERR
    std::cerr << "CCAException in user go code: " << enote << std::endl;
    std::cerr << "Returning -2 from go()" << std::endl;;
#endif
""")+"""
  }
  catch (sidl::RuntimeException ex) {
    bocca_status = -2;
    std::string enote = ex.getNote();
"""+self.iolines("""
    BOCCA_FPRINTF(stderr,"RuntimeException in user go code: %s\\n",enote.c_str());
    BOCCA_FPRINTF(stderr,"Returning -2 from go()");
""","""
#ifdef _BOCCA_STDERR
    std::cerr << "RuntimeException in user go code: " << enote << std::endl;
    std::cerr << "Returning -2 from go()" << std::endl;;
#endif
""")+"""
  }
  catch (sidl::SIDLException ex) {
    bocca_status = -2;
    std::string enote = ex.getNote();
"""+self.iolines("""
    BOCCA_FPRINTF(stderr,"SIDLException in user go code: %s\\n",enote.c_str());
    BOCCA_FPRINTF(stderr,"Returning -2 from go()");
""","""
#ifdef _BOCCA_STDERR
    std::cerr << "SIDLException in user go code: " << enote << std::endl;
    std::cerr << "Returning -2 from go()" << std::endl;;
#endif
""")+"""
  }
  catch (sidl::BaseException ex) {
    bocca_status = -2;
    std::string enote = ex.getNote();
"""+self.iolines("""
    BOCCA_FPRINTF(stderr,"BaseException in user go code: %s\\n",enote.c_str());
    BOCCA_FPRINTF(stderr,"Returning -2 from go()");
""","""
#ifdef _BOCCA_STDERR
    std::cerr << "BaseException in user go code: " << enote << std::endl;
    std::cerr << "Returning -2 from go()" << std::endl;;
#endif
""")+"""
  }
  catch (std::exception ex) {
    bocca_status = -2;
"""+self.iolines("""
    BOCCA_FPRINTF(stderr, "C++ exception in user go code: %s\\n", ex.what());
    BOCCA_FPRINTF(stderr, "Returning -2 from go()");
""","""
#ifdef _BOCCA_STDERR
    std::cerr << "C++ exception in user go code: " << ex.what() << std::endl;
    std::cerr << "Returning -2 from go()"  << std::endl;
#endif
""")+"""
  }
  catch (...) {
    bocca_status = -2;
"""+self.iolines("""
    BOCCA_FPRINTF(stderr, "Odd exception in user go code\\n");
    BOCCA_FPRINTF(stderr,  "Returning -2 from go()\\n");
""","""
#ifdef _BOCCA_STDERR
    std::cerr << "Odd exception in user go code " << std::endl;
    std::cerr << "Returning -2 from go()" << std::endl;
#endif
""")+"""
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
    def getGoPrologCode(self, componentSymbol, uses=[]):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """

// """+self.protKey+""".begin(@CMPT_TYPE@.go:boccaGoProlog)
  int bocca_status = 0;
  // The user's code should set bocca_status 0 if computation proceeded ok.
  // The user's code should set bocca_status -1 if computation failed but might
  // succeed on another call to go(), e.g. when a required port is not yet 
  // connected.
  // The user's code should set bocca_status -2 if the computation failed and 
  // can never succeed in a future call.
  // The user's code should NOT use return in this function.
  // Exceptions that are not caught in user code will be converted to 
  // status -2.
"""
# Add local uses ports variables:
        if len(uses) > 0:
            buf += """
  gov::cca::Port port;
"""
            # Use port(s) variables
            for portInstance in uses:
                portnativetype = portInstance.getType().replace('.', '::')
                portVarBuf = """
  // nil if not fetched and cast successfully:
  @NATIVE_PORT_TYPE@ @PORT_INSTANCE@; 
  // True when releasePort is needed (even if cast fails):
  bool @PORT_INSTANCE@_fetched = false; """
                portVarBuf = portVarBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType()).\
                              replace('@NATIVE_PORT_TYPE@', portnativetype)
                buf += portVarBuf
            # Use port(s) code
            for portInstance in uses:
                portnativetype = portInstance.getType().replace('.', '::')
                portBuf = """
  // Use a @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
  try{
    port = this->"""+self.servicesVariable+""".getPort("@PORT_INSTANCE@");
  } catch ( ::gov::cca::CCAException ex )  {
    // we will continue with port nil (never successfully assigned) and 
    // set a flag.
"""+self.iolines("""
    BOCCA_FPRINTF(stderr,"@CMPT_TYPE@: Error calling getPort("
              "\\"@PORT_INSTANCE@\\") at %s:%d: %s\\n" ,
              __FILE__ , __LINE__ -5 , ex.getNote().c_str());
""","""
#ifdef _BOCCA_STDERR
    std::cerr << "@CMPT_TYPE@: Error calling getPort(\\"@PORT_INSTANCE@\\") "
              " at " << __FILE__ << ":" << __LINE__ -5 << ": " << ex.getNote() 
              << std::endl;
#endif // _BOCCA_STDERR
""")+"""
  }
  if ( port._not_nil() ) {
    // even if the next cast fails, must release.
    @PORT_INSTANCE@_fetched = true; 
    @PORT_INSTANCE@ = ::babel_cast< @NATIVE_PORT_TYPE@ >(port);
    if (@PORT_INSTANCE@._is_nil()) {
"""+self.iolines("""
      BOCCA_FPRINTF(stderr,"@CMPT_TYPE@: Error casting gov::cca::Port "
                    "@PORT_INSTANCE@ to type @NATIVE_PORT_TYPE@\\n");
""","""
#ifdef _BOCCA_STDERR
      std::cerr << "@CMPT_TYPE@: Error casting gov::cca::Port "
                << "@PORT_INSTANCE@ to type "
                << "@NATIVE_PORT_TYPE@" << std::endl;
#endif //_BOCCA_STDERR
""")+"""
      goto BOCCAEXIT; // we cannot correctly continue. clean up and leave.
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
// """+self.protKey+""".end(@CMPT_TYPE@.go:boccaGoProlog)

"""
        buf = buf.replace('@CMPT_TYPE_UBAR@', cmpt_ubar).\
                  replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
#---------------------------------------------------------------------------------
    def getGoEpilogCode(self, componentSymbol, uses=[]):

        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
  BOCCAEXIT:; // target point for error and regular cleanup. do not delete.
// """+self.protKey+""".begin(@CMPT_TYPE@.go:boccaGoEpilog)
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
      this->"""+self.servicesVariable+""".releasePort("@PORT_INSTANCE@");
    } catch ( ::gov::cca::CCAException ex )  {
"""+self.iolines("""
      BOCCA_FPRINTF(stderr,"@CMPT_TYPE@: Error calling releasePort("
                "\\"@PORT_INSTANCE@\\") at %s:%d: %s\\n",
                __FILE__ , __LINE__ -4, ex.getNote().c_str());
""","""
#ifdef _BOCCA_STDERR
      std::cerr << "@CMPT_TYPE@: Error calling releasePort("
                << "\\"@PORT_INSTANCE@\\") at " 
                << __FILE__ << ":" << __LINE__ -4 << ": " << ex.getNote() 
                << std::endl;
#endif // _BOCCA_STDERR
""")+"""
    }
    // c++ port reference will be dropped when function exits, but we 
    // must tell framework.
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
        buf = buf.replace('@CMPT_TYPE_UBAR@', cmpt_ubar).\
                  replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
#---------------------------------------------------------------------------------
    def getAuxiliaryReleaseServicesMethod(self, componentSymbol, provides=[], uses=[]):
        buf = """
  // DO-NOT-DELETE splicer.begin(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
  // DO-NOT-EDIT-BOCCA
  // """+self.protKey+""".begin(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
  this->"""+self.servicesVariable+"""=0;

"""
# Un-provide provides ports
        for portInstance in provides:
           portBuf = """
  // Un-provide @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
  try{
    services.removeProvidesPort("@PORT_INSTANCE@");
  } catch ( ::gov::cca::CCAException ex )  {
"""+self.iolines("""
    BOCCA_FPRINTF(stderr,"@CMPT_TYPE@: Error calling removeProvidesPort("
              "\\"@PORT_INSTANCE@\\") at %s:%d: %s\\n" ,
              __FILE__ , __LINE__ -4,  ex.getNote().c_str() );
""","""
#ifdef _BOCCA_STDERR
    std::cerr << "@CMPT_TYPE@: Error calling removeProvidesPort("
              << "\\"@PORT_INSTANCE@\\") at " 
              << __FILE__ << ": " << __LINE__ -4 << ": " << ex.getNote() 
              << std::endl;
#endif // _BOCCA_STDERR
""")+"""
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
  } catch ( ::gov::cca::CCAException ex )  {
"""+self.iolines("""
    BOCCA_FPRINTF(stderr, "@CMPT_TYPE@: Error calling unregisterUsesPort("
              "\\"@PORT_INSTANCE@\\") at %s:%d: %s\\n",
              __FILE__ , __LINE__ -4 , ex.getNote().c_str() );
""","""
#ifdef _BOCCA_STDERR
    std::cerr << "@CMPT_TYPE@: Error calling unregisterUsesPort("
              << "\\"@PORT_INSTANCE@\\") at " 
              << __FILE__ << ":" << __LINE__ -4 << ": " << ex.getNote() 
              << std::endl;
#endif // _BOCCA_STDERR
""")+"""
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

  // Insert-UserCode-Here {@CMPT_TYPE@.releaseServices} 

  // """+self.onceKey+""".begin(@CMPT_TYPE@.releaseServices)
     """+self.boccaReleaseMethod+"""(services);
  // """+self.onceKey+""".end(@CMPT_TYPE@.releaseServices)
    
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
        for i in range(0,numitems):
            buf += "    (void)dummy"+str(count)+";\n"
            count += 1
        buf += """
  // """+self.protKey+""".end(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""")
  // DO-NOT-DELETE splicer.end(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""")
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
