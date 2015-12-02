from writers.sourceWriter import SourceWriter

def getWriterParameters():
    return (PythonWriter.language, PythonWriter.babelVersions, PythonWriter.dialect)
 
class PythonWriter(SourceWriter):
    language = 'python'
    dialect = 'standard'
    babelVersions = ['1.0.X', '1.1.X', '1.2.X', '1.4.X', '1.5.X']

# -------------------------------
    def __init__(self, kind = 'component'):
        SourceWriter.__init__(self, kind)
    
# -------------------------------
    def getConstructorCode(self, componentSymbol):
        buf = """
# DO-NOT-DELETE splicer.begin(_before_type)
import sys
# DO-NOT-DELETE splicer.end(_before_type)

# DO-NOT-DELETE splicer.begin(__init__)

    # Put your code here...

    # """+self.protKey+""".begin(@CMPT_TYPE@._init)"""
        if (self.kind == 'component'):
            buf +="""
    self."""+self.servicesVariable+""" = None"""
        buf +=""" 
    self.bocca_print_errs = True
    # """+self.protKey+""".end(@CMPT_TYPE@._init) 

# DO-NOT-DELETE splicer.end(__init__)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf

# -------------------------------
    def getSetServicesCode(self, componentSymbol):
        buf = """ 
    # DO-NOT-DELETE splicer.begin(setServices)

    # Put your code here... prolog

    # """+self.onceKey+""".begin(setServices)
    self."""+self.boccaServicesMethod+"""(services)
    # """+self.onceKey+""".end(setServices)

    # Put your code here... epilog

    # DO-NOT-DELETE splicer.end(setServices)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
# -------------------------------
    def getAuxiliarySetServicesMethod(self, componentSymbol, provides=[], uses=[]):
        buf = """
# DO-NOT-DELETE splicer.begin("""+self.boccaServicesMethod+""")
# DO-NOT-EDIT-BOCCA
# """+self.protKey+""".begin("""+self.boccaServicesMethod+""") 
    self."""+self.servicesVariable+""" = services
"""
# Add ports declarations (if needed)
        if (len(provides) + len(uses) > 0):
            buf += """
    # Create a typemap
    mymap = services.createTypeMap()
    
"""
            if (len(provides) > 0):
                buf +="""
    port = gov.cca.Port.Port(self.__IORself)  # CAST 
    if not port:
      ex = sidl.SIDLException.SIDLException()
      ex.setNote(__name__,0, 'Error casting self @CMPT_TYPE@ to to gov.cca.Port')
      raise sidl.SIDLException._Exception, ex
"""
# Provide port(s) code
            for portInstance in provides:
                portBuf = """
    # Provide a @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
    try:
      self."""+self.servicesVariable+""".addProvidesPort(port,    # the implementing object
                              '@PORT_INSTANCE@',       # the name the user will see
                              '@PORT_TYPE@',          # the sidl name of the port type.
                              mymap);         # extra properties.
    except sidl.BaseException._Exception, e:
      (etype, eobj, etb) = sys.exc_info()
      eobj.add(__name__, 0, 'Error - could not addProvidesPort(port, ' \
          + '"@PORT_INSTANCE@","@PORT_TYPE@",mymap)')
      raise sidl.BaseException._Exception, e
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                                  replace('@PORT_TYPE@', portInstance.getType())
                buf += portBuf
            
# Use port(s) code
            for portInstance in uses:
                portBuf = """
    # Register a use port of type @PORT_TYPE@ with port name @PORT_INSTANCE@
    try:
      self."""+self.servicesVariable+""".registerUsesPort('@PORT_INSTANCE@',   # the name the user will see
                                '@PORT_TYPE@',     # the sidl name of the port type.
                                mymap);       # extra properties.
    except sidl.BaseException._Exception, e:
      (etype, eobj, etb) = sys.exc_info()
      eobj.add(__name__, 0, 'Error - could not registerUsesPort'\
               + '("@PORT_INSTANCE@","@PORT_TYPE@",mymap)')
      raise sidl.BaseException._Exception, e
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
                buf += portBuf
# Finish up, and replace vars

        buf +="""
    compRelease = gov.cca.ComponentRelease.ComponentRelease(self.__IORself)
    try:
      self."""+self.servicesVariable+""".registerForRelease(compRelease)
    except sidl.BaseException._Exception, e:
      (etype, eobj, etb) = sys.exc_info()
      eobj.exception.add(__name__,0, 
             'Error - could not registerForRelease(self) in @CMPT_TYPE@')
      raise sidl.BaseException._Exception, e
      
    return
# """+self.protKey+""".end("""+self.boccaServicesMethod+""")
# DO-NOT-DELETE splicer.end("""+self.boccaServicesMethod+""")
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
# -------------------------------
    def getReleaseMethod(self, componentSymbol):
        buf = """
    # DO-NOT-DELETE splicer.begin(releaseServices)
    
    # put your code here ... prolog

    # """+self.onceKey+""".begin(releaseServices)
    self."""+self.boccaReleaseMethod+"""(services)
    # """+self.onceKey+""".end(releaseServices)

    # put your code here ... epilog

    # DO-NOT-DELETE splicer.end(releaseServices)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf

# -------------------------------
    def getAuxiliaryReleaseServicesMethod(self, componentSymbol, provides=[], uses=[]):
        buf = """
    # DO-NOT-DELETE splicer.begin("""+self.boccaReleaseMethod+""")
    # DO-NOT-EDIT-BOCCA
    # """+self.protKey+""".begin(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
    self."""+self.servicesVariable+""" = None
"""
# Un-provide Provide port(s) code
        for portInstance in provides:
            portBuf = """
    # UN-Provide a @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
    try:
      services.removeProvidesPort('@PORT_INSTANCE@')
    except sidl.BaseException._Exception, e:
      (etype, eobj, etb) = sys.exc_info()
      eobj.exception.add(__name__,0, 'Error - could not remove provided port ' \
          + '@PORT_TYPE@:@PORT_INSTANCE@')
      raise sidl.BaseException._Exception, e
"""
            portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
            buf += portBuf
            
# Use port(s) code
        for portInstance in uses:
            portBuf = """
    # Un-Register a use port of type @PORT_TYPE@ with port name @PORT_INSTANCE@
    try:
      services.unregisterUsesPort('@PORT_INSTANCE@')
    except sidl.BaseException._Exception, e:
      (etype, eobj, etb) = sys.exc_info()
      eobj.exception.add(__name__,0, 'Error - could not ' \
              + 'unregisterUsesPort("@PORT_INSTANCE@")')
      raise sidl.BaseException._Exception, e
"""
            portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
            buf += portBuf
# Finish up, and replace vars

        buf +="""
    return
    # """+self.protKey+""".end(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
    # DO-NOT-DELETE splicer.end("""+self.boccaReleaseMethod+""")
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf

# -------------------------------
    def getCheckExceptionMethod(self, componentSymbol):
        buf = ""
        return buf

# -------------------------------
    def getGoCode(self, componentSymbol, uses=[]):
        buf = """
    # DO-NOT-DELETE splicer.begin(go)
@BOCCA_GO_PROLOG@

        # If this try/catch block is rewritten by the user, we will not change it.
        try:
            try:
                # The user might not require all ports to be connected in all configurations.
                # Each uses port is available as the local variable with the same name.
                # Those that are properly connected will be a value other than None.
                # the proper test for an unavailable port is "if not portinstancename:"

                # Insert-Code-Here {@CMPT_TYPE@.go} 

                # BEGIN REMOVE ME BLOCK
                ex = sidl.SIDLException.SIDLException()
                ex.setNote("USER FORGOT TO FILL IN THEIR FUNCTION @CMPT_TYPE@.go()")
                raise sidl.SIDLException._Exception, ex
                # END REMOVE ME BLOCK

            except sidl.BaseException._Exception, e:
                bocca_status = -2
                if self.bocca_print_errs:
                    (etype, eobj, etb) = sys.exc_info()
                    msg="@CMPT_TYPE@: Error in go() execution: "+eobj.exception.getNote()
                    print >>sys.stderr,'Exception:', msg
                # if specific exceptions in the user code are tolerable 
                # and restart is ok, bocca_status -1 instead.
                # 2 means the component is so confused that it and probably 
	        # the application should be destroyed.
            except Exception,e:
                bocca_status = -2
                if self.bocca_print_errs:
                    print >> sys.stderr, 'Exception in @CMPT_TYPE@ go():'+str(e)
            except:
                bocca_status = -2
                print >> sys.stderr, 'Unclassified Exception in @CMPT_TYPE@ go()'
        finally:
            # always executed.
            pass
        # This version of TryExceptFinally for compatibility with python 2.3 and up

@BOCCA_GO_EPILOG@

    # DO-NOT-DELETE splicer.end(go)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        prolog = self.getGoPrologCode(componentSymbol, uses)
        epilog = self.getGoEpilogCode(componentSymbol, uses)
        buf=buf.replace("@BOCCA_GO_PROLOG@", prolog)
        buf=buf.replace("@BOCCA_GO_EPILOG@", epilog)
        return buf

# -------------------------------
    def getGoPrologCode(self, componentSymbol, uses=[]):
        buf = """

# """+self.protKey+""".begin(go:boccaGoProlog)
    bocca_status = 0
    # The user's code should set bocca_status 0 if computation proceeded ok.
    # The user's code should set bocca_status -1 if computation failed but might
    # succeed on another call to go(), e.g. when a required port is not yet connected.
    # The user's code should set bocca_status -2 if the computation failed and can
    # never succeed in a future call.
    # The users's code should NOT use return in this function;
    # Exceptions that are not caught in user code will be converted to status 2.
"""
# Add local uses ports variables:
        if len(uses) > 0:
            # Use port(s) code
            for portInstance in uses:
                portnativetype = portInstance.getType()
                nlist = portnativetype.split(".")
                portLeaf = nlist[len(nlist)-1]
                portBuf = """
    if bocca_status == 0: # skip this getport if a problem already occured.
        # Use a @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
        try:
            port = self."""+self.servicesVariable+""".getPort("@PORT_INSTANCE@")
        except sidl.BaseException._Exception, e:
            port = None
            if self.bocca_print_errs:
                (etype, eobj, etb) = sys.exc_info()
                msg="@CMPT_TYPE@: Error calling getPort('@PORT_INSTANCE@'): "\
                    + eobj.exception.getNote()
                print >>sys.stderr,'Exception:', msg
   
        @PORT_INSTANCE@_fetched = False;
        if not port:
            if self.bocca_print_errs:
                print '@CMPT_TYPE@: getPort("@PORT_INSTANCE@") returned nil.'
        else:
            @PORT_INSTANCE@_fetched = True # even if the next cast fails, must release.
            @PORT_INSTANCE@ = @NATIVE_PORT_TYPE@.@NATIVE_PORT_LEAF@(port);
            if not @PORT_INSTANCE@:
                bocca_status = -1
                if self.bocca_print_errs:
                    print "@CMPT_TYPE@: Error casting port gov.cca.Port to "\
                        + "@PORT_INSTANCE@ type @NATIVE_PORT_TYPE@"
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType()).\
                              replace('@NATIVE_PORT_TYPE@', portnativetype).\
                              replace('@NATIVE_PORT_LEAF@', portLeaf)
                buf += portBuf
            # end for uName
            buf += """
"""   
        # Finish up, and replace class vars
        buf +="""
    if bocca_status == 0: # all is ok so far and we do the user code, else cleanup and return.
        # user code indents to match this.
# """+self.protKey+""".end(go:boccaGoProlog)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
# -------------------------------
    def getGoEpilogCode(self, componentSymbol, uses=[]):

        buf = """
# """+self.protKey+""".begin(go:boccaGoEpilog)
        # end user code.
    # end if bocca_status == 0.
"""
# release local uses ports variables:
        if len(uses) > 0:
            # release port(s) code
            for portInstance in uses:
                portBuf = """
    # release @PORT_INSTANCE@ 
    if @PORT_INSTANCE@_fetched:
        @PORT_INSTANCE@_fetched = False
        try:
            self."""+self.servicesVariable+""".releasePort("@PORT_INSTANCE@")
        except sidl.BaseException._Exception, e:
            port = None
            if self.bocca_print_errs:
                (etype, eobj, etb) = sys.exc_info()
                msg="@CMPT_TYPE@: Error calling releasePort('@PORT_INSTANCE@'): "\
                    + eobj.exception.getNote()
                print >>sys.stderr,'Exception:', msg
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName())
                buf += portBuf
            # end for uName
            buf += """
"""   
        # Finish up, and replace class vars
        buf +="""
    return bocca_status
# """+self.protKey+""".end(go:boccaGoEpilog)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf

    
#---------------------------------------------------------------------------------
    def getForceUsePortCode(self, componentSymbol, numitems=0, depthstring=""):
        buf = """
    # DO-NOT-DELETE splicer.begin(boccaForceUsePortInclude"""+depthstring+""")
    # DO-NOT-EDIT-BOCCA
    # """+self.protKey+""".begin(boccaForceUsePortInclude"""+depthstring+""")
"""
        count=0
        for i in range(0,numitems):
            buf += "    o"+str(count)+" = dummy"+str(count)+"\n"
            count += 1
        buf += "    return"
        buf += """
    # """+self.protKey+""".end(boccaForceUsePortInclude"""+depthstring+""")
    # DO-NOT-DELETE splicer.end(boccaForceUsePortInclude"""+depthstring+""")
"""
        return buf
