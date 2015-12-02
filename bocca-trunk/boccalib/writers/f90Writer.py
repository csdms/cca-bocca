from writers.sourceWriter import SourceWriter

#---------------------------------------------------------------------------------
def getWriterParameters():
     return (F90Writer.language, F90Writer.babelVersions, F90Writer.dialect)
 
class F90Writer(SourceWriter):
    language = 'f90'
    dialect = 'standard'
    commentLineStart = "C    "
    babelVersions = ['1.0.X', '1.1.X', '1.2.X', '1.4.X', '1.5.X']

#---------------------------------------------------------------------------------
    def __init__(self, kind='component'):
        SourceWriter.__init__(self, kind)
    
#---------------------------------------------------------------------------------
    def getImplHeaderCode(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """ 
! DO-NOT-DELETE splicer.begin(_miscellaneous_code_start)

! Insert-UserDecl-Here 

#include "gov_cca_TypeMap_fAbbrev.h"
#include "sidl_SIDLException_fAbbrev.h"

! """+self.protKey+""".begin(_miscellaneous_code_start)


! bocca_update_exception. Used only in implementing BOCCA_SIDL_CHECK_F90
        logical function bue_@CMPT_TYPE_UBAR@(except, meth, lin) RESULT(bue)
        use sidl
        use sidl_BaseInterface
        use sidl_RuntimeException
        implicit none
        type(sidl_BaseInterface_t) :: except, etmp
        type(sidl_RuntimeException_t) :: rex
!       logical bue
        integer lin
        character (LEN=*) meth, myfilename
        parameter(myfilename='@CMPT_TYPE_UBAR@_Impl.F90')

        bue = .false.
        if ( not_null(except) ) then
          bue = .true.
          call cast(except, rex, etmp)
          if (not_null(rex)) then
             call add(rex, myfilename, 0_sidl_int, meth, etmp)
             call deleteRef(rex, etmp)
          endif
        endif
        return
        end

! Exit statement not normally reached (or needed) unless BOCCA_SIDL_CHECK_F90
! is used and finds an exception. 
#define BOCCAEXIT 20331

! Any method using BOCCA_SIDL_CHECK_F90 must start user code with BOCCA_EXTERNAL
! or equivalent. If the result of this macro is a line too long, the
! f90 user will have to put the equivalent in manually unless their freeform f90
! compiler supports unlimited length lines (e.g. -ffree-line-length-none).
#define BOCCA_EXTERNAL \\
   external bue_@CMPT_TYPE_UBAR@ ; \\
   logical bue_@CMPT_TYPE_UBAR@

! call BOCCA_SIDL_CLEAR_F90(except)
#define BOCCA_SIDL_CLEAR_F90(except) \\
  boccaClearException(self,except)

! BOCCA_SIDL_CHECK_F90(ex,methodandmessagestring) to jump to exit if
! exception ex was thrown. See SIDL_CHECK documentation for C in babel.
#define BOCCA_SIDL_CHECK_F90(except,method) \\
  if ( bue_@CMPT_TYPE_UBAR@(except, method) ) goto BOCCAEXIT

! call BOCCA_SIDL_THROW_F90(except, messagestring) 
! generate new exception and jump to exit. See SIDL_THROW doc for C in babel.
#define BOCCA_SIDL_THROW_F90(except, messagestring) \\
  boccaThrowException(self, messagestring, except); \\
  goto BOCCAEXIT

        
! """+self.protKey+""".end(_miscellaneous_code_start)

! or  Insert-UserDecl-Here 

! DO-NOT-DELETE splicer.end(_miscellaneous_code_start)

! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.boccaClearException)
! DO-NOT-EDIT-BOCCA
! """+self.protKey+""".begin(@CMPT_TYPE@.boccaClearException)
        type(sidl_BaseInterface_t) :: etmp
        if (not_null(exception)) then
            call deleteRef(exception, etmp)
        endif
! """+self.protKey+""".end(@CMPT_TYPE@.boccaClearException)
! DO-NOT-DELETE splicer.end(@CMPT_TYPE@.boccaClearException)

! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.boccaThrowException.use)
! DO-NOT-EDIT-BOCCA
! """+self.protKey+""".begin(@CMPT_TYPE@.boccaThrowException.use)
        use sidl_SIDLException
! """+self.protKey+""".end(@CMPT_TYPE@.boccaThrowException.use)
! DO-NOT-DELETE splicer.end(@CMPT_TYPE@.boccaThrowException.use)

! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.boccaThrowException)
! DO-NOT-EDIT-BOCCA
! """+self.protKey+""".begin(@CMPT_TYPE@.boccaThrowException)
        type (sidl_BaseInterface_t) :: except
        type (sidl_SIDLException_t) :: einst
        character (LEN=*) myfilename
        parameter(myfilename='@CMPT_TYPE_UBAR@_Impl.F90')
        call new(einst, except)
        ! clear except here?
        call add(einst, myfilename, 0_sidl_int, message, except)
        ! clear except here?
        call cast(einst, exception, except)
        call deleteRef(einst,except)
        ! clear except here?
        return
! """+self.protKey+""".end(@CMPT_TYPE@.boccaThrowException)
! DO-NOT-DELETE splicer.end(@CMPT_TYPE@.boccaThrowException)

"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
        return buf
    
#---------------------------------------------------------------------------------
    def getConstructorCode(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """ 
! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._ctor)

! Insert-UserDecl-Here

! """+self.onceKey+""".begin(@CMPT_TYPE@._ctor)
  ! Access private data
  type(@CMPT_TYPE_UBAR@_wrap) :: dp
  ! Allocate memory and initialize
  allocate(dp%d_private_data) ! crash if out of memory
  """
        if (self.kind == 'component'):
            buf = buf + "call set_null(dp%d_private_data%"+self.servicesVariable+")"
        buf +="""
! Insert-UserCode-Here

  call @CMPT_TYPE_UBAR@__set_data_m(self, dp)
#ifdef _BOCCA_STDERR
    write(*, *) 'CTOR @CMPT_TYPE@: F90 allocated'
#endif
! """+self.onceKey+""".end(@CMPT_TYPE@._ctor)


! DO-NOT-DELETE splicer.end(@CMPT_TYPE@._ctor)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
        return buf
    
#---------------------------------------------------------------------------------
    def getDestructorCode(self, componentSymbol):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """ 
! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@._dtor)

! """+self.onceKey+""".begin(@CMPT_TYPE@._dtor)
  ! Access private data
  type(@CMPT_TYPE_UBAR@_wrap) :: dp
  ! Insert-UserDecl-Here 

  call @CMPT_TYPE_UBAR@__get_data_m(self,dp)

  ! Insert-UserCode-Here 

#ifdef _BOCCA_STDERR
    write(*, *) 'DTOR @CMPT_TYPE@: F90 deallocating'
#endif
  deallocate(dp%d_private_data)
! """+self.onceKey+""".end(@CMPT_TYPE@._dtor)

  ! Insert-UserCode-Here , alternatively

! DO-NOT-DELETE splicer.end(@CMPT_TYPE@._dtor)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
        return buf
    
#---------------------------------------------------------------------------------
    def getHeaderCode(self, componentSymbol):
        buf = """
! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.use)

! Insert use statements here...

! """+self.protKey+""".begin(@CMPT_TYPE@.use)
  ! CCA framework services module
  use gov_cca_Services
! """+self.protKey+""".end(@CMPT_TYPE@.use)

! DO-NOT-DELETE splicer.end(@CMPT_TYPE@.use)

! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.private_data)

! Insert user's private data here.

! """+self.protKey+""".begin(@CMPT_TYPE@.private_data)"""
        if (self.kind == 'component'):
            buf += """
  ! Handle to framework Services object
  type(gov_cca_Services_t) :: """+self.servicesVariable+"""
! """+self.protKey+""".end(@CMPT_TYPE@.private_data)

! DO-NOT-DELETE splicer.end(@CMPT_TYPE@.private_data)
"""    
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
        
#---------------------------------------------------------------------------------
    def getSetServicesCode(self, componentSymbol):
        methodName = self.boccaServicesMethod
        buf = """ 
! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.setServices)
! """+self.onceKey+""".begin(@CMPT_TYPE@.setServices)
    BOCCA_EXTERNAL

    ! Insert-UserCode-Here

    call @METHOD_NAME@(self, services, exception) 
    BOCCA_SIDL_CHECK_F90(exception , 'setServices')

    ! Insert-UserCode-Here

    return

! Exit route when there are exceptions
BOCCAEXIT      continue
    ! Insert cleanup code here if needed.
    return
! """+self.onceKey+""".end(@CMPT_TYPE@.setServices)

! DO-NOT-DELETE splicer.end(@CMPT_TYPE@.setServices)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@METHOD_NAME@', methodName)
        return buf
   
#---------------------------------------------------------------------------------
    def getAuxiliarySetServicesMethod(self, componentSymbol, provides=[], uses=[]):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@."""+self.boccaServicesMethod+""".use)
  use gov_cca_ComponentRelease
  use gov_cca_TypeMap
  use gov_cca_Port
! DO-NOT-DELETE splicer.end(@CMPT_TYPE@."""+self.boccaServicesMethod+""".use)

! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
! DO-NOT-EDIT-BOCCA
! """+self.protKey+""".begin(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
  
  type(@CMPT_TYPE_UBAR@_wrap) :: dp
  type(SIDL_BaseInterface_t) :: throwaway 
  type(gov_cca_ComponentRelease_t) :: cr
  logical dr_services, dr_port, dr_cr, dr_typeMap
"""
# Add ports declarations (if needed)
        if (len(provides) + len(uses) > 0):
            buf += """
  type(gov_cca_TypeMap_t)    :: typeMap 
  type(gov_cca_Port_t)       :: port
"""
        buf +="""
  BOCCA_EXTERNAL
  ! not crashing if something fails requires good bookkeeping and exception handling.
  dr_services= .false. 
  dr_port= .false. 
  dr_cr= .false. 
"""
# Component Registration code            
        buf +="""
  ! Access private data
  call @CMPT_TYPE_UBAR@__get_data_m(self, dp)
  ! Set my reference to the services handle
  dp%d_private_data%"""+self.servicesVariable+""" = services
  ! Increment reference count for the services subroutine parameter
  call addRef(services, exception)
  BOCCA_SIDL_CHECK_F90(exception,'@CMPT_TYPE@ failed addref(services)')
  dr_services = .true.

"""
        if (len(provides) + len(uses) > 0):
        
            buf += """
  call createTypeMap(dp%d_private_data%"""+self.servicesVariable+""", typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'@CMPT_TYPE@ failed to createTypeMap')
"""
            if (len(provides) > 0):
                buf +="""
  dr_port = .false.
  call cast(self, port, exception)
  BOCCA_SIDL_CHECK_F90(exception,'@CMPT_TYPE@ is not Port')
  dr_port = .true.
"""
# Provide port(s) code
            for portInstance in provides:
                portBuf = """
! Add @PORT_TYPE@:@PORT_INSTANCE@ provides port
  call addProvidesPort(dp%d_private_data%"""+self.servicesVariable+""", port, &
       '@PORT_INSTANCE@', '@PORT_TYPE@', &
       typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'@CMPT_TYPE@ failed addProvidesPort @PORT_INSTANCE@ ')
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
                buf += portBuf

            if (len(provides) > 0):
                buf+="""
  dr_port = .false.
  call deleteRef(port,exception)
  BOCCA_SIDL_CHECK_F90(exception,'@CMPT_TYPE@ failed deleteRef(port)')
"""
            
# Use port(s) code
            for portInstance in uses:
                portBuf = """
! Register @PORT_TYPE@:@PORT_INSTANCE@ uses port
  call registerUsesPort(dp%d_private_data%"""+self.servicesVariable+""", &
      '@PORT_INSTANCE@', '@PORT_TYPE@', &
      typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'@CMPT_TYPE@ failed registerUsesPort @PORT_INSTANCE@')
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@PORT_TYPE@', portInstance.getType())
                buf += portBuf
            buf += """
  dr_typeMap = .false.
  call deleteRef(typeMap,exception)
  BOCCA_SIDL_CHECK_F90(exception,'@CMPT_TYPE@."""+self.boccaServicesMethod+""": failed deleteRef(typeMap)')
"""
# Finish up,
        buf +="""
! Register component @CMPT_TYPE@ for release by the framework 
  call cast(self, cr, exception)
  BOCCA_SIDL_CHECK_F90(exception,'@CMPT_TYPE@."""+self.boccaServicesMethod+""": is not ComponentRelease')
  call registerForRelease(dp%d_private_data%"""+self.servicesVariable+""", cr, exception)
  BOCCA_SIDL_CHECK_F90(exception,'@CMPT_TYPE@."""+self.boccaServicesMethod+""": failed registerForRelease')
  call deleteRef(cr, exception)
  BOCCA_SIDL_CHECK_F90(exception,'@CMPT_TYPE@."""+self.boccaServicesMethod+""": failed deleteRef(cr)')
  return
   
BOCCAEXIT   continue
  if (dr_services) then
      call deleteRef(services, throwaway)
      call BOCCA_SIDL_CLEAR_F90(throwaway)
  endif
  if (dr_cr) then
      call deleteRef(cr, throwaway)
      call BOCCA_SIDL_CLEAR_F90(throwaway)
  endif
"""
        if (len(provides) + len(uses) > 0):
            buf += """
  if (dr_port) then
      call deleteRef(port, throwaway)
      call BOCCA_SIDL_CLEAR_F90(throwaway)
  endif
  if (dr_typeMap) then
      call deleteRef(typeMap, throwaway)
      call BOCCA_SIDL_CLEAR_F90(throwaway)
  endif
"""
        buf += """
   return
! """+self.protKey+""".end(@CMPT_TYPE@."""+self.boccaServicesMethod+""")
! DO-NOT-DELETE splicer.end(@CMPT_TYPE@."""+self.boccaServicesMethod+""")"""

        buf = buf.replace('@CMPT_TYPE_UBAR@', cmpt_ubar).\
                  replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
#---------------------------------------------------------------------------------
    def getReleaseMethod(self, componentSymbol):
        buf = """
! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.releaseServices)

! """+self.onceKey+""".begin(@CMPT_TYPE@.releaseServices)
    BOCCA_EXTERNAL

! Insert-UserCode-Here {@CMPT_TYPE@.releaseServices} (releaseServices method)

    call """+self.boccaReleaseMethod+"""(self, services, exception)
    BOCCA_SIDL_CHECK_F90(exception , 'releaseServices')
    return
    
! Exit route when there are exceptions
BOCCAEXIT      continue

    ! Insert cleanup code here if needed.

    return

! """+self.onceKey+""".end(@CMPT_TYPE@.releaseServices)
! DO-NOT-DELETE splicer.end(@CMPT_TYPE@.releaseServices)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
#---------------------------------------------------------------------------------
    def getAuxiliaryReleaseServicesMethod(self, componentSymbol, provides=[], uses=[]):
        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
! DO-NOT-EDIT-BOCCA
! """+self.protKey+""".begin(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
  type(@CMPT_TYPE_UBAR@_wrap) :: dp
  type(SIDL_BaseInterface_t) :: excpt, throwaway
! trap and optionally print all port-related exceptions. ignore others.
"""
# forget stored services object
        buf +="""
! Access private data
  BOCCA_EXTERNAL
  call @CMPT_TYPE_UBAR@__get_data_m(self, dp)
  call deleteRef(dp%d_private_data%"""+self.servicesVariable+""", throwaway)
  call set_null(dp%d_private_data%"""+self.servicesVariable+""")
  call BOCCA_SIDL_CLEAR_F90(throwaway)
"""

# Un-provide provides ports
        for portInstance in provides:
           portBuf = """
! Un-provide @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
  call removeProvidesPort(services, '@PORT_INSTANCE@', excpt)
  call checkException(self, excpt, &
      'Error: Could not removeProvidesPort @PORT_INSTANCE@', &
      .false., throwaway &
  )
"""
           portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                             replace('@PORT_TYPE@', portInstance.getType())
           buf += portBuf
           
# Use port(s) release code
        for portInstance in uses:
           portBuf = """
! Release @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
  call unregisterUsesPort(services, '@PORT_INSTANCE@', excpt)
  call checkException(self, excpt,  &
       'Error calling unregisterUsesPort @PORT_INSTANCE@', &
       .false., throwaway &
  )
"""
           portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                             replace('@PORT_TYPE@', portInstance.getType())
           buf += portBuf
           
# Finish up, and substitute values
        buf += """
  return
! """+self.protKey+""".end(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
! DO-NOT-DELETE splicer.end(@CMPT_TYPE@."""+self.boccaReleaseMethod+""")
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar)
        return buf
    
#---------------------------------------------------------------------------------
    def getCheckExceptionMethod(self, componentSymbol):
        buf = """
! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.checkException.use)
! """+self.protKey+""".begin(@CMPT_TYPE@.checkException.use)
  use sidl_BaseException
! """+self.protKey+""".end(@CMPT_TYPE@.checkException.use)
! DO-NOT-DELETE splicer.end(@CMPT_TYPE@.checkException.use)

! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.checkException)
! DO-NOT-EDIT-BOCCA
! """+self.protKey+""".begin(@CMPT_TYPE@.checkException)

  type(sidl_BaseInterface_t) :: throwaway  ! unused exception
  type(sidl_BaseException_t) :: be
  character (LEN=4096) val

  if (not_null(excpt)) then
#ifdef _BOCCA_STDERR
    write(*, *) '@CMPT_TYPE@: ', msg
    write(*, *) 'Exception was: '
    call cast(excpt, be, throwaway)
    call BOCCA_SIDL_CLEAR_F90(throwaway)
    if (not_null(be)) then
      call getNote(be, val, throwaway)
      call BOCCA_SIDL_CLEAR_F90(throwaway)
      write(*,*) val
      call deleteRef(be, throwaway)
      call BOCCA_SIDL_CLEAR_F90(throwaway)
      call BOCCA_SIDL_CLEAR_F90(excpt)
    endif
#endif
    if (fatal) stop '@CMPT_TYPE@.checkException called with fatal .true.'
  end if
  return
! """+self.protKey+""".end(@CMPT_TYPE@.checkException)
    
! DO-NOT-DELETE splicer.end(@CMPT_TYPE@.checkException)
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
    
#---------------------------------------------------------------------------------
    def getForceUsePortCode(self, componentSymbol, numitems=0, depthstring=""):
        buf = """
! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""")
! DO-NOT-EDIT-BOCCA
! """+self.protKey+""".begin(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""")
  return
! """+self.protKey+""".end(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""")
! DO-NOT-DELETE splicer.end(@CMPT_TYPE@.boccaForceUsePortInclude"""+depthstring+""")
"""
        buf = buf.replace('@CMPT_TYPE@', componentSymbol)
        return buf
    
    
#---------------------------------------------------------------------------------
    def getGoCode(self, componentSymbol, uses=[]):
        buf = """
! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.go.use)

! """+self.protKey+""".begin(@CMPT_TYPE@.go.use) 
  use gov_cca_Port
"""
        ulist = []
        for portInstance in uses:
            portnativetype = portInstance.getType().replace('.', '_')
            if (not portnativetype in ulist):
                buf += ("  use "+portnativetype + "\n")
        buf +="""
! """+self.protKey+""".end(@CMPT_TYPE@.go.use) 

! DO-NOT-DELETE splicer.end(@CMPT_TYPE@.go.use)

! DO-NOT-DELETE splicer.begin(@CMPT_TYPE@.go)

@BOCCA_GO_PROLOG@


! When this block is rewritten by the user, we will not change it.
! All port instances should be rechecked for NULL before calling in user code.
! Not all ports need be connected in arbitrary use.
! The port instance names used in registerUsesPort appear as local variable
! names here with the suffix __p added.

!    Insert-Code-Here {@CMPT_TYPE@.go} */

! BEGIN REMOVE ME BLOCK
#ifdef _BOCCA_STDERR
  write(*,*) 'USER FORGOT TO FILL IN THEIR FUNCTION @CMPT_TYPE@.go.'
#endif
! END REMOVE ME BLOCK


!    If unknown exceptions in the user code are tolerable and restart is ok, 
!    set bocca_status -1 instead.
!    -2 means the component is so confused that it and probably the application 
!    should be destroyed.
! 

@BOCCA_GO_EPILOG@

! Insert-User-Exception-Cleanup-Here 

  retval = bocca_status
! DO-NOT-DELETE splicer.end(@CMPT_TYPE@.go)
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
  type(gov_cca_Port_t) :: port
  type(gov_cca_Services_t) :: services 
  type(SIDL_BaseInterface_t) :: throwaway
  type(SIDL_BaseInterface_t) :: dumex
  type(@CMPT_TYPE_UBAR@_wrap) :: dp
  logical dr_port ! if dr_X true, the deleteRef(X) is needed before return.
"""
        buf = """

! Insert-User-Declarations-Here

! """+self.protKey+""".begin(@CMPT_TYPE@.go:boccaGoProlog)

  integer bocca_status
!  The user's code should set bocca_status 0 if computation proceeded ok.
!  The user's code should set bocca_status -1 if computation failed but might
!  succeed on another call to go(), e.g. wheh a required port is not yet connected.
!  The user's code should set bocca_status -2 if the computation failed and can
!  never succeed in a future call.
!  The users's code should NOT use return in this function;
!  Exceptions that are not caught in user code will be converted to status -2.
! 
"""
# Add local uses ports variables:
        if len(uses) == 0:
            buf += """
  bocca_status=0
"""
        if len(uses) > 0:
            buf += """
@DECLS@

  BOCCA_EXTERNAL
  ! not crashing if something fails requires good bookkeeping and exception handling.
  call set_null(services)
  call set_null(port)
  call set_null(throwaway)
  call set_null(dumex)
  dr_port = .false.
  bocca_status = 0
  call @CMPT_TYPE_UBAR@__get_data_m(self,dp);
  services =  dp%d_private_data%"""+self.servicesVariable+"""

  if (is_null(services) ) then
    call BOCCA_SIDL_THROW_F90(exception, 'NULL """+self.servicesVariable+""" pointer in @CMPT_TYPE@.go()')
  endif
"""
            # Use port(s) code
            for portInstance in uses:
                portnativetype = portInstance.getType().replace('.', '_')
                portBuf = """
  ! Use a @PORT_TYPE@ port with port name @PORT_INSTANCE@ 
  call getPort(services,"@PORT_INSTANCE@", port, throwaway)
  if ( not_null(throwaway) ) then
    call set_null(port)
    call checkException(self, throwaway, errMsg0_@PORT_INSTANCE@, .false., dumex)
    ! we will continue with port null (never successfully assigned) and set a flag.
  endif
"""
                decls +="""
  type(@NATIVE_PORT_TYPE@_t) ::  @PORT_INSTANCE@__p	! non-null if specific uses port obtained. 
  logical @PORT_INSTANCE@_fetched            ! true if releaseport is needed for this port.
  character (LEN=*) errMsg0_@PORT_INSTANCE@
  character (LEN=*) errMsg1_@PORT_INSTANCE@
  character (LEN=*) errMsg2_@PORT_INSTANCE@
  character (LEN=*) errMsg3_@PORT_INSTANCE@
  character (LEN=*) errMsg4_@PORT_INSTANCE@
  parameter(errMsg0_@PORT_INSTANCE@= &
    '@CMPT_TYPE@: Error go() getPort(@PORT_INSTANCE@) failed.')
  parameter(errMsg1_@PORT_INSTANCE@= &
    '@CMPT_TYPE@: Error casting gov.cca.Port @PORT_INSTANCE@ to type @PORT_TYPE@')
  parameter(errMsg2_@PORT_INSTANCE@= &
     '@CMPT_TYPE@: Error in deleteRef(port) while getting @PORT_INSTANCE@')
  parameter(errMsg3_@PORT_INSTANCE@= &
     '@CMPT_TYPE@: Error calling releasePort(@PORT_INSTANCE@). Continuing.')
  parameter(errMsg4_@PORT_INSTANCE@ = &
     '@CMPT_TYPE@: Error in deleteRef for port @PORT_INSTANCE@. Continuing.')
"""
                portBuf += """
  call set_null( @PORT_INSTANCE@__p)
  @PORT_INSTANCE@_fetched = .false.
  if ( not_null(port)) then
    @PORT_INSTANCE@_fetched = .true. ! even if the next cast fails, must releasePort.
    call cast(port, @PORT_INSTANCE@__p, exception) 
    BOCCA_SIDL_CHECK_F90(exception, errMsg1_@PORT_INSTANCE@)
    call deleteRef(port, exception)
    call set_null(port) 
    BOCCA_SIDL_CHECK_F90(exception, errMsg2_@PORT_INSTANCE@)
  endif
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
! """+self.protKey+""".end(@CMPT_TYPE@.go:boccaGoProlog) 

"""
        buf = buf.replace('@DECLS@',decls).\
                  replace('@CMPT_TYPE_UBAR@', cmpt_ubar).\
                  replace('@CMPT_TYPE@', componentSymbol)
        return buf

#---------------------------------------------------------------------------------
    def getGoEpilogCode(self, componentSymbol, uses=[]):

        cmpt_ubar = componentSymbol.replace('.', '_')
        buf = """
BOCCAEXIT continue ! target point for normal and error cleanup. do not delete.
! """+self.protKey+""".begin(@CMPT_TYPE@.go:boccaGoEpilog) 
"""
# release local uses ports variables:
        if len(uses) > 0:
            buf +="""
  if (not_null(port)) then
    call deleteRef(port,throwaway)
    call checkException(self, throwaway, 'cleanup port error', .false., dumex)
    call set_null(port)
  endif
"""
            # release port(s) code
            for portInstance in uses:
                portnativetype = portInstance.getType().replace('.', '_')
                portBuf = """
  ! release @PORT_INSTANCE@
  if (@PORT_INSTANCE@_fetched) then
    @PORT_INSTANCE@_fetched = .false.
    call releasePort(services, '@PORT_INSTANCE@', throwaway)
    call checkException(self, throwaway, errMsg3_@PORT_INSTANCE@, .false., dumex)
    
    if ( not_null(@PORT_INSTANCE@__p) ) then
      call deleteRef(@PORT_INSTANCE@__p, throwaway)
      call checkException(self, throwaway, errMsg4_@PORT_INSTANCE@, .false., dumex)
      call set_null(@PORT_INSTANCE@__p)
    endif

  endif
"""
                portBuf = portBuf.replace('@PORT_INSTANCE@', portInstance.getName()).\
                              replace('@NATIVE_PORT_TYPE@', portnativetype)
                buf += portBuf
            # end for uName
            buf += """
"""
        # Finish up, and replace class vars
        buf +="""
! """+self.protKey+""".end(@CMPT_TYPE@.go:boccaGoEpilog) 
"""
        buf = buf.replace('@CMPT_TYPE_UBAR@', cmpt_ubar).\
                  replace('@CMPT_TYPE@', componentSymbol)
        return buf


#---------------------------------------------------------------------------------
