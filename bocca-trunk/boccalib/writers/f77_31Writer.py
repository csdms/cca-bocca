from writers.sourceWriter import SourceWriter

def getWriterParameters():
     return (F77_31Writer.language, F77_31Writer.babelVersions, F77_31Writer.dialect)
 
class F77_31Writer(SourceWriter):
    language = 'f77_31'
    dialect = 'standard'
    babelVersions = ['1.0.X', '1.1.X', '1.2.X','1.4.X', '1.5.X']
    commentLineStart = "C    "

    def __init__(self, kind = 'component'):
        SourceWriter.__init__(self, kind)
    
    def getConstructorCode(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
C       DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._ctor)

C       """+self.onceKey+""".begin(@CMPT_TYPE@._ctor)
C	User instance data storage:
C	Increase boccaNSTATES by one for every babel object you want to store
C	in the stateArray instance data. Only babel opaque objects (including array
C	references), can be stored in the stateArray.
C
C	User objects are indexed in stateArray (1:boccaNSTATES); element 0
C	of stateArray belongs to bocca.
C
        integer*4 boccaNSTATES
        parameter (boccaNSTATES=0)

C       Insert-UserDeclarations-Here


C       We use a SIDL opaque array to store private data. Each entry
C       will coresspond to a one of the following
C       1- A SIDL reference to an object,
C       2- An array of SIDL objects, or
C       3- An array of basic SIDL array types. 
C       
C       The mapping between entries in those arrays and individual state 
C       fields needs to be documented and maintaned by the developers.
C
        integer*8  stateArray
        integer*4  stateSize  
        
        stateSize = 1 + MAX(boccaNSTATES,0)
        
        call sidl_opaque__array_create1d_f(stateSize, stateArray)
        if (stateArray .eq. 0) then
           write(*,*) '@CMPT_TYPE@ 
     &     ERROR: creating state array. Object will be useless.'
           return
        endif
        call @CMPT_TYPE_UBAR@__set_data_f(self, stateArray)

C       Insert-UserInitializationCode-Here 

C       """+self.onceKey+""".end(@CMPT_TYPE@._ctor)
C       DO-NOT-DELETE splicer.end(@CMPT_TYPE@._ctor)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
        return buf
            
    def getDestructorCode(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
C       DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._dtor)
C       """+self.onceKey+""".begin(@CMPT_TYPE@._dtor)

C       Insert-UserCleanupDeclarationsCode-Here {@CMPT_TYPE@:_dtor} (_dtor method)

C       Cleaning up the other stateArray elements is the users's problem.
C       bocca takes care of element 0.
C
        integer*8  stateArray, excpt, exdummy, knull

        call @CMPT_TYPE_UBAR@__get_data_f(
     & self, stateArray)
        knull=0
        call @CMPT_TYPE_UBAR@__set_data_f(
     & self, knull)
        
        call sidl_opaque__array_deleteRef_f(stateArray, excpt)
        if (excpt .ne. 0) then
            call sidl_BaseException_deleteRef_f(excpt, exdummy)
        endif
        
C	Insert-UserCleanupCode-Here

C       """+self.onceKey+""".begin(@CMPT_TYPE@._dtor)
C       DO-NOT-DELETE splicer.end(@CMPT_TYPE@._dtor)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
        return buf
            
    def getSetServicesCode(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        methodName = cmpt_ubar + '_boccaSetServices_f'
        buf = """ 
C       DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.setServices)
C       """+self.onceKey+""".begin(@CMPT_TYPE@.setServices)

        call @METHOD_NAME@(
     & self, services, exception)  
C FIXME need to check and propagate exception here.

C       Insert-Code-Here {@CMPT_TYPE@.setServices} (setServices method)

C       """+self.onceKey+""".end(@CMPT_TYPE@.setServices)
C       DO-NOT-DELETE splicer.end(@CMPT_TYPE@.setServices)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@METHOD_NAME@', methodName)
        return buf
   
    def getAuxiliarySetServicesMethod(self, componentSymbol, provides=[], uses=[]):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
C       DO-NOT-DELETE splicer.begin(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
C       """+self.protKey+""".begin(@CMPT_TYPE@."""+self.boccaServicesMethod+""")

        integer *8  stateArray
        integer *8  """+self.servicesVariable+"""
        integer *8  compRelease
"""
# Add ports declarations (if needed)
        if (len(provides) + len(uses) > 0):
            buf += """
        integer *8 typeMap
        integer *8 port
"""
# Component Registration code            
        buf +="""
        call @CMPT_TYPE_UBAR@__get_data_f(
     & self, stateArray)
        if (stateArray .eq. 0) then
           write(*,*) '@CMPT_TYPE@: 
     &  ERROR: Null stateArray'
           return
        end if
        """+self.servicesVariable+""" = services
        call sidl_opaque__array_set1_f(stateArray, 
     &   0, """+self.servicesVariable+""")
        call gov_cca_Services_addRef_f(
     & """+self.servicesVariable+""", exception)
"""
# Port and TypeMap declaration
        if (len(provides) + len(uses) > 0):
            buf += """
        call gov_cca_Services_createTypeMap_f(
     &              """+self.servicesVariable+""", 
     &              typeMap,
     &              exception)
        if (exception .ne. 0) then 
           print *, '@CMPT_TYPE@: 
     &  Error creating type map'
           return
        endif
"""
            if (len(provides) > 0):
                buf +="""
        call @CMPT_TYPE_UBAR@__cast2_f(
     & self,
     &                  'gov.cca.Port', 
     &                  port,
     &                  exception)
        if (exception .ne. 0) then
           print *, '@CMPT_TYPE@: 
     &  Error casting self to gov.cca.Port'
           call gov_cca_TypeMap_deleteRef_f(
     &            typeMap, 
     &            exception) 
           return
        end if
        """
# Provide port(s) code
            for portInstance in provides:
                portBuf = """
C       Add @PORT_TYPE@:@PORT_INSTANCE@ provides port
        call gov_cca_Services_addProvidesPort_f(
     &       """+self.servicesVariable+""", 
     &       port, 
     &       '@PORT_INSTANCE@', 
     &       '@PORT_TYPE@', 
     &       typeMap, 
     &       exception)
        if (exception .ne. 0) then
           print *, '@CMPT_TYPE@: 
     &  Error in call to addProvidesPort()'
           call gov_cca_TypeMap_deleteRef_f(
     &            typeMap, 
     &            exception)
           return 
        end if
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
                buf += portBuf
            buf += """
           call gov_cca_Port_deleteRef_f(
     &            port, 
     &            exception) 
"""

# Use port(s) code
            for portInstance in uses:
                portBuf = """
C       Register @PORT_TYPE@:@PORT_INSTANCE@ uses port
        call gov_cca_Services_registerUsesPort_f(
     &       """+self.servicesVariable+""",
     &       '@PORT_INSTANCE@', 
     &       '@PORT_TYPE@', 
     &       typeMap, 
     &       exception)
        if (exception .ne. 0) then
           print *, '@CMPT_TYPE@: 
     &         Error in call to registerUsesPort()'
           call gov_cca_TypeMap_deleteRef_f(
     &            typeMap, 
     &            exception)
           return
        end if
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
                buf += portBuf
            buf += """
        call gov_cca_TypeMap_deleteRef_f(
     &         typeMap, 
     &         exception)
"""   
# Finish up, and replace vars

        buf +="""
        call @CMPT_TYPE_UBAR@__cast2_f(
     &                  self,
     &                  'gov.cca.ComponentRelease', 
     &                  compRelease,
     &                  exception)
        if (exception .ne. 0) then
           print *, '@CMPT_TYPE@: 
     &  Error casting self to gov.cca.ComponentRelease'
           stop
C FIXME exceptions, not stops.
        end if
        call gov_cca_Services_registerForRelease_f(
     &      """+self.servicesVariable+""",
     &      compRelease,
     &      exception)
        if (exception .ne. 0) then
           print *, '@CMPT_TYPE@: 
     &  Error calling registerForRelease()'
        end if
        return
        end
C       """+self.protKey+""".end(@CMPT_TYPE@."""+self.boccaServicesMethod+""")

C       DO-NOT-DELETE splicer.end(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
"""
        buf = buf.replace('@CMPT_TYPE_UBAR@', cmpt_ubar).\
                  replace('@CMPT_TYPE@', componentSymbol)
        return buf

#---------------------------------------------------------------------------------
    def getAuxiliaryReleaseServicesMethod(self, componentSymbol, provides=[], uses=[]):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
C       DO-NOT-DELETE splicer.begin(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
C       """+self.protKey+""".begin(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")

        integer *8  stateArray, knull
"""
# Access private data
        buf +="""
        call @CMPT_TYPE_UBAR@__get_data_f(
     &          self, stateArray)
        if (stateArray .eq. 0) then
C          fail silently, we've failed a lot before this is reached.
           return
        end if
        knull=0
        call sidl_opaque__array_set1_f(stateArray, 0, knull)
        call gov_cca_Services_deleteRef_f(services, exception)
"""
# Unprovide provides port(s) code
        for portInstance in provides:
            portBuf = """
C       Remove @PORT_TYPE@:@PORT_INSTANCE@ provides port
        call gov_cca_Services_removeProvidesPort_f(
     &       services, 
     &       '@PORT_INSTANCE@', 
     &       exception)
        if (exception .ne. 0) then
           print *, '@CMPT_TYPE@: 
     &  Error in call to removeProvidesPort()'
           stop 
C FIXME exceptions, not stops.
        end if
"""
            portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
            buf += portBuf
            
# Unregister use port(s) code
            for portInstance in uses:
                portBuf = """
C       UnRegister @PORT_TYPE@:@PORT_INSTANCE@ uses port
        call gov_cca_Services_unregisterUsesPort_f(
     &       services,
     &       '@PORT_INSTANCE@',
     &       exception)
        if (exception .ne. 0) then
           print *, '@CMPT_TYPE@: 
     &         Error in call to unregisterUsesPort()'
           stop
C FIXME exceptions, not stops.
        end if
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
                buf += portBuf
                
# Finish up, and substitute values
        buf += """
        return
C       """+self.protKey+""".end(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
C       DO-NOT-DELETE splicer.end(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
        return buf
    


#---------------------------------------------------------------------------------
    def getReleaseMethod(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        methodName = cmpt_ubar + "_"+self.boccaReleaseMethod+"_f"
        buf = """
C       DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.releaseServices)

C       Insert-Code-Here {@CMPT_TYPE@.releaseServices} (releaseServices method)

C       """+self.onceKey+""".begin(@CMPT_TYPE@.releaseServices)
        call @METHOD_NAME@(
     & self, services, exception)  
C FIXME need to amend and propagate exceptions here.
C       """+self.onceKey+""".end(@CMPT_TYPE@.releaseServices)
    
C       DO-NOT-DELETE splicer.end(@CMPT_TYPE@.releaseServices)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar).\
                  replace('@METHOD_NAME@', methodName)
        return buf
    

    
#---------------------------------------------------------------------------------
    def getForceUsePortCode(self, componentSymbol, numitems=0, depthstring=""):
        buf = """
C       DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""") */
C       """+self.protKey+""".begin(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""") */
        return
C       """+self.protKey+""".end(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""") */
C       DO-NOT-DELETE splicer.end(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""") */
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf

    
