! 
! File:          ppF_testX_Impl.F90
! Symbol:        ppF.testX-v0.0
! Symbol Type:   class
! Babel Version: 1.0.6
! Description:   Server-side implementation for ppF.testX
! 
! WARNING: Automatically generated; only changes within splicers preserved
! 
! 


! 
! Symbol "ppF.testX" (version 0.0)
! 


#include "sidl_NotImplementedException_fAbbrev.h"
#include "gov_cca_CCAException_fAbbrev.h"
#include "gov_cca_ports_GoPort_fAbbrev.h"
#include "gov_cca_ports_ParameterPortFactory_fAbbrev.h"
#include "gov_cca_Port_fAbbrev.h"
#include "sidl_RuntimeException_fAbbrev.h"
#include "gov_cca_ports_ParameterGetListener_fAbbrev.h"
#include "sidl_BaseException_fAbbrev.h"
#include "sidl_BaseClass_fAbbrev.h"
#include "ppF_testX_fAbbrev.h"
#include "gov_cca_ports_ParameterSetListener_fAbbrev.h"
#include "gov_cca_ComponentRelease_fAbbrev.h"
#include "gov_cca_Services_fAbbrev.h"
#include "sidl_ClassInfo_fAbbrev.h"
#include "gov_cca_Component_fAbbrev.h"
#include "sidl_BaseInterface_fAbbrev.h"
! DO-NOT-DELETE splicer.begin(_miscellaneous_code_start)

! Insert-UserDecl-Here 

#include "gov_cca_TypeMap_fAbbrev.h"
#include "sidl_SIDLException_fAbbrev.h"

! Bocca generated code. bocca.protected.begin(_miscellaneous_code_start)


! bocca_update_exception. Used only in implementing BOCCA_SIDL_CHECK_F90
        logical function bue_ppF_testX(except, meth, lin) RESULT(bue)
        use sidl
        use sidl_BaseInterface
        use sidl_RuntimeException
        implicit none
        type(sidl_BaseInterface_t) :: except, etmp
        type(sidl_RuntimeException_t) :: rex
!       logical bue
        integer lin
        character (LEN=*) meth, myfilename
        parameter(myfilename='ppF_testX_Impl.F90')

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
#define BOCCA_EXTERNAL \
   external bue_ppF_testX ; \
   logical bue_ppF_testX

! call BOCCA_SIDL_CLEAR_F90(except)
#define BOCCA_SIDL_CLEAR_F90(except) \
  boccaClearException(self,except)

! BOCCA_SIDL_CHECK_F90(ex,methodandmessagestring) to jump to exit if
! exception ex was thrown. See SIDL_CHECK documentation for C in babel.
#define BOCCA_SIDL_CHECK_F90(except,method) \
  if ( bue_ppF_testX(except, method) ) goto BOCCAEXIT

! call BOCCA_SIDL_THROW_F90(except, messagestring) 
! generate new exception and jump to exit. See SIDL_THROW doc for C in babel.
#define BOCCA_SIDL_THROW_F90(except, messagestring) \
  boccaThrowException(self, messagestring, except); \
  goto BOCCAEXIT

        
! Bocca generated code. bocca.protected.end(_miscellaneous_code_start)

! or  Insert-UserDecl-Here 

! DO-NOT-DELETE splicer.end(_miscellaneous_code_start)




! 
! Method:  _ctor[]
! Class constructor called when the class is created.
! 

recursive subroutine ppF_testX__ctor_mi(self, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
  ! DO-NOT-DELETE splicer.begin(ppF.testX._ctor.use)
  ! Insert-Code-Here {ppF.testX._ctor.use} (use statements)
  ! DO-NOT-DELETE splicer.end(ppF.testX._ctor.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX._ctor)

! Insert-UserDecl-Here

! bocca-default-code. User may edit or delete.begin(ppF.testX._ctor)
  ! Access private data
  type(ppF_testX_wrap) :: dp
  integer i
  ! Allocate memory and initialize
  allocate(dp%d_private_data) ! crash if out of memory
  call set_null(dp%d_private_data%d_services)
  call set_null(dp%d_private_data%ppf)
  do i=1,9
    call set_null(dp%d_private_data%tmlist(i))
  end do
  dp%d_private_data%numtests = 0

! Insert-UserCode-Here

  call ppF_testX__set_data_m(self, dp)
#ifdef _BOCCA_STDERR
    write(*, *) 'CTOR ppF.testX: F90 allocated'
#endif
! bocca-default-code. User may edit or delete.end(ppF.testX._ctor)


! DO-NOT-DELETE splicer.end(ppF.testX._ctor)
end subroutine ppF_testX__ctor_mi


! 
! Method:  _ctor2[]
! Special Class constructor called when the user wants to wrap his own private data.
! 

recursive subroutine ppF_testX__ctor2_mi(self, private_data, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
  ! DO-NOT-DELETE splicer.begin(ppF.testX._ctor2.use)
  ! Insert-Code-Here {ppF.testX._ctor2.use} (use statements)
  ! DO-NOT-DELETE splicer.end(ppF.testX._ctor2.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  type(ppF_testX_wrap) :: private_data
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX._ctor2)
! Insert-Code-Here {ppF.testX._ctor2} (_ctor2 method)
 
! DO-DELETE-WHEN-IMPLEMENTING exception.begin() 
! 
! This method has not been implemented
! 
  type(sidl_BaseInterface_t) :: throwaway
  type(sidl_NotImplementedException_t) :: notImpl
  call new(notImpl, exception)
  call setNote(notImpl, 'Not Implemented', exception)
  call cast(notImpl, exception,throwaway)
  call deleteRef(notImpl,throwaway)
  return
! DO-DELETE-WHEN-IMPLEMENTING exception.end() 
 
! DO-NOT-DELETE splicer.end(ppF.testX._ctor2)
end subroutine ppF_testX__ctor2_mi


! 
! Method:  _dtor[]
! Class destructor called when the class is deleted.
! 

recursive subroutine ppF_testX__dtor_mi(self, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
  ! DO-NOT-DELETE splicer.begin(ppF.testX._dtor.use)
  ! Insert-Code-Here {ppF.testX._dtor.use} (use statements)
  ! DO-NOT-DELETE splicer.end(ppF.testX._dtor.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX._dtor)

! bocca-default-code. User may edit or delete.begin(ppF.testX._dtor)
  ! Access private data
  type(ppF_testX_wrap) :: dp
  ! Insert-UserDecl-Here 

  call ppF_testX__get_data_m(self,dp)

  ! Insert-UserCode-Here 

#ifdef _BOCCA_STDERR
    write(*, *) 'DTOR ppF.testX: F90 deallocating'
#endif
  deallocate(dp%d_private_data)
  ! FIXME deallocate/deleteRef private if needed.
! bocca-default-code. User may edit or delete.end(ppF.testX._dtor)

  ! Insert-UserCode-Here , alternatively

! DO-NOT-DELETE splicer.end(ppF.testX._dtor)
end subroutine ppF_testX__dtor_mi


! 
! Method:  _load[]
! Static class initializer called exactly once before any user-defined method is dispatched
! 

recursive subroutine ppF_testX__load_mi(exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
  ! DO-NOT-DELETE splicer.begin(ppF.testX._load.use)
  ! Insert-Code-Here {ppF.testX._load.use} (use statements)
  ! DO-NOT-DELETE splicer.end(ppF.testX._load.use)
  implicit none
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX._load)
! Insert-Code-Here {ppF.testX._load} (_load method)
 
! DO-DELETE-WHEN-IMPLEMENTING exception.begin() 
! 
! This method has not been implemented
! 
  type(sidl_BaseInterface_t) :: throwaway
  type(sidl_NotImplementedException_t) :: notImpl
  call new(notImpl, exception)
  call setNote(notImpl, 'Not Implemented', exception)
  call cast(notImpl, exception,throwaway)
  call deleteRef(notImpl,throwaway)
  return
! DO-DELETE-WHEN-IMPLEMENTING exception.end() 
 
! DO-NOT-DELETE splicer.end(ppF.testX._load)
end subroutine ppF_testX__load_mi


! 
! Method:  boccaSetServices[]
! 

recursive subroutine ppF_testX_boccaSetServices_mi(self, services, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_Services
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
! DO-NOT-DELETE splicer.begin(ppF.testX.boccaSetServices.use)
  use gov_cca_ComponentRelease
  use gov_cca_TypeMap
  use gov_cca_Port
! DO-NOT-DELETE splicer.end(ppF.testX.boccaSetServices.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  type(gov_cca_Services_t) :: services ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX.boccaSetServices)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(ppF.testX.boccaSetServices)
  
  type(ppF_testX_wrap) :: dp
  type(SIDL_BaseInterface_t) :: throwaway 
  type(gov_cca_ComponentRelease_t) :: cr
  logical dr_services, dr_port, dr_cr, dr_typeMap

  type(gov_cca_TypeMap_t)    :: typeMap 
  type(gov_cca_Port_t)       :: port

  BOCCA_EXTERNAL
  ! not crashing if something fails requires good bookkeeping and exception handling.
  dr_services= .false. 
  dr_port= .false. 
  dr_cr= .false. 

  ! Access private data
  call ppF_testX__get_data_m(self, dp)
  ! Set my reference to the services handle
  dp%d_private_data%d_services = services
  ! Increment reference count for the services subroutine parameter
  call addRef(services, exception)
  BOCCA_SIDL_CHECK_F90(exception,'ppF.testX failed addref(services)')
  dr_services = .true.


  call createTypeMap(dp%d_private_data%d_services, typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'ppF.testX failed to createTypeMap')

  dr_port = .false.
  call cast(self, port, exception)
  BOCCA_SIDL_CHECK_F90(exception,'ppF.testX is not Port')
  dr_port = .true.

! Add gov.cca.ports.GoPort:go provides port
  call addProvidesPort(dp%d_private_data%d_services, port, &
       'go', 'gov.cca.ports.GoPort', &
       typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'ppF.testX failed addProvidesPort go ')

  dr_port = .false.
  call deleteRef(port,exception)
  BOCCA_SIDL_CHECK_F90(exception,'ppF.testX failed deleteRef(port)')

! Register gov.cca.ports.ParameterPortFactory:ParameterPortFactory uses port
  call registerUsesPort(dp%d_private_data%d_services, &
      'ParameterPortFactory', 'gov.cca.ports.ParameterPortFactory', &
      typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'ppF.testX failed registerUsesPort ParameterPortFactory')

  dr_typeMap = .false.
  call deleteRef(typeMap,exception)
  BOCCA_SIDL_CHECK_F90(exception,'ppF.testX.boccaSetServices: failed deleteRef(typeMap)')

! Register component ppF.testX for release by the framework 
  call cast(self, cr, exception)
  BOCCA_SIDL_CHECK_F90(exception,'ppF.testX.boccaSetServices: is not ComponentRelease')
  call registerForRelease(dp%d_private_data%d_services, cr, exception)
  BOCCA_SIDL_CHECK_F90(exception,'ppF.testX.boccaSetServices: failed registerForRelease')
  call deleteRef(cr, exception)
  BOCCA_SIDL_CHECK_F90(exception,'ppF.testX.boccaSetServices: failed deleteRef(cr)')
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

  if (dr_port) then
      call deleteRef(port, throwaway)
      call BOCCA_SIDL_CLEAR_F90(throwaway)
  endif
  if (dr_typeMap) then
      call deleteRef(typeMap, throwaway)
      call BOCCA_SIDL_CLEAR_F90(throwaway)
  endif

   return
! Bocca generated code. bocca.protected.end(ppF.testX.boccaSetServices)
! DO-NOT-DELETE splicer.end(ppF.testX.boccaSetServices)
end subroutine ppF_testX_boccaSetServices_mi


! 
! Method:  boccaReleaseServices[]
! 

recursive subroutine boccaReleaseServick8bdjlfvu3_mi(self, services,           &
  exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_Services
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
  ! DO-NOT-DELETE splicer.begin(ppF.testX.boccaReleaseServices.use)
  ! Insert-Code-Here {ppF.testX.boccaReleaseServices.use} (use statements)
  ! DO-NOT-DELETE splicer.end(ppF.testX.boccaReleaseServices.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  type(gov_cca_Services_t) :: services ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX.boccaReleaseServices)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(ppF.testX.boccaReleaseServices)
  type(ppF_testX_wrap) :: dp
  type(SIDL_BaseInterface_t) :: excpt, throwaway
! trap and optionally print all port-related exceptions. ignore others.

! Access private data
  BOCCA_EXTERNAL
  call ppF_testX__get_data_m(self, dp)
  call deleteRef(dp%d_private_data%d_services, throwaway)
  call set_null(dp%d_private_data%d_services)
  call BOCCA_SIDL_CLEAR_F90(throwaway)

! Un-provide gov.cca.ports.GoPort port with port name go 
  call removeProvidesPort(services, 'go', excpt)
  call checkException(self, excpt, &
      'Error: Could not removeProvidesPort go', &
      .false., throwaway &
  )

! Release gov.cca.ports.ParameterPortFactory port with port name ParameterPortFactory 
  call unregisterUsesPort(services, 'ParameterPortFactory', excpt)
  call checkException(self, excpt,  &
       'Error calling unregisterUsesPort ParameterPortFactory', &
       .false., throwaway &
  )

  return
! Bocca generated code. bocca.protected.end(ppF.testX.boccaReleaseServices)
! DO-NOT-DELETE splicer.end(ppF.testX.boccaReleaseServices)
end subroutine boccaReleaseServick8bdjlfvu3_mi


! 
! Method:  checkException[]
! 

recursive subroutine ppF_testX_checkException_mi(self, excpt, msg, fatal,      &
  exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
! DO-NOT-DELETE splicer.begin(ppF.testX.checkException.use)
! Bocca generated code. bocca.protected.begin(ppF.testX.checkException.use)
  use sidl_BaseException
! Bocca generated code. bocca.protected.end(ppF.testX.checkException.use)
! DO-NOT-DELETE splicer.end(ppF.testX.checkException.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  type(sidl_BaseInterface_t) :: excpt ! inout
  character (len=*) :: msg ! in
  logical :: fatal ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX.checkException)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(ppF.testX.checkException)

  type(sidl_BaseInterface_t) :: throwaway  ! unused exception
  type(sidl_BaseException_t) :: be
  character (LEN=4096) val

  if (not_null(excpt)) then
#ifdef _BOCCA_STDERR
    write(*, *) 'ppF.testX: ', msg
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
    if (fatal) stop 'ppF.testX.checkException called with fatal .true.'
  end if
  return
! Bocca generated code. bocca.protected.end(ppF.testX.checkException)
    
! DO-NOT-DELETE splicer.end(ppF.testX.checkException)
end subroutine ppF_testX_checkException_mi


! 
! Method:  boccaClearException[]
! 

recursive subroutine boccaClearExceptioc5id18af85_mi(self, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
  ! DO-NOT-DELETE splicer.begin(ppF.testX.boccaClearException.use)
  ! Insert-Code-Here {ppF.testX.boccaClearException.use} (use statements)
  ! DO-NOT-DELETE splicer.end(ppF.testX.boccaClearException.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX.boccaClearException)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(ppF.testX.boccaClearException)
        type(sidl_BaseInterface_t) :: etmp
        if (not_null(exception)) then
            call deleteRef(exception, etmp)
        endif
! Bocca generated code. bocca.protected.end(ppF.testX.boccaClearException)
! DO-NOT-DELETE splicer.end(ppF.testX.boccaClearException)
end subroutine boccaClearExceptioc5id18af85_mi


! 
! Method:  boccaThrowException[]
! 

recursive subroutine boccaThrowExceptioej30cx26_4_mi(self, message, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
! DO-NOT-DELETE splicer.begin(ppF.testX.boccaThrowException.use)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(ppF.testX.boccaThrowException.use)
        use sidl_SIDLException
! Bocca generated code. bocca.protected.end(ppF.testX.boccaThrowException.use)
! DO-NOT-DELETE splicer.end(ppF.testX.boccaThrowException.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  character (len=*) :: message ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX.boccaThrowException)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(ppF.testX.boccaThrowException)
        type (sidl_BaseInterface_t) :: except
        type (sidl_SIDLException_t) :: einst
        character (LEN=*) myfilename
        parameter(myfilename='ppF_testX_Impl.F90')
        call new(einst, except)
        ! clear except here?
        call add(einst, myfilename, 0, message, except)
        ! clear except here?
        call cast(einst, exception, except)
        call deleteRef(einst,except)
        ! clear except here?
        return
! Bocca generated code. bocca.protected.end(ppF.testX.boccaThrowException)
! DO-NOT-DELETE splicer.end(ppF.testX.boccaThrowException)
end subroutine boccaThrowExceptioej30cx26_4_mi


! 
! Method:  boccaForceUsePortInclude[]
!  This function should never be called, but helps babel generate better code. 
! 

recursive subroutine boccaForceUsePortIep1sg0z3ac_mi(self, dummy0, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_ports_ParameterPortFactory
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
  ! DO-NOT-DELETE splicer.begin(ppF.testX.boccaForceUsePortInclude.use)
  ! Insert-Code-Here {ppF.testX.boccaForceUsePortInclude.use} (use statements)
  ! DO-NOT-DELETE splicer.end(ppF.testX.boccaForceUsePortInclude.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  type(gov_cca_ports_ParameterPortFactory_t) :: dummy0 ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX.boccaForceUsePortInclude)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(ppF.testX.boccaForceUsePortInclude)
  return
! Bocca generated code. bocca.protected.end(ppF.testX.boccaForceUsePortInclude)
! DO-NOT-DELETE splicer.end(ppF.testX.boccaForceUsePortInclude)
end subroutine boccaForceUsePortIep1sg0z3ac_mi


! 
! Method:  setServices[]
!  Starts up a component presence in the calling framework.
! @param services the component instance's handle on the framework world.
! Contracts concerning Svc and setServices:
! 
! The component interaction with the CCA framework
! and Ports begins on the call to setServices by the framework.
! 
! This function is called exactly once for each instance created
! by the framework.
! 
! The argument Svc will never be nil/null.
! 
! Those uses ports which are automatically connected by the framework
! (so-called service-ports) may be obtained via getPort during
! setServices.
! 

recursive subroutine ppF_testX_setServices_mi(self, services, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_Services
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
  ! DO-NOT-DELETE splicer.begin(ppF.testX.setServices.use)
  ! Insert-Code-Here {ppF.testX.setServices.use} (use statements)
  use gov_cca_Port
  use gov_cca_ports_ParameterPortFactory
  
  ! DO-NOT-DELETE splicer.end(ppF.testX.setServices.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  type(gov_cca_Services_t) :: services ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX.setServices)

! ! ! extra variables for handling the parameterportfactory and port

  type(ppF_testX_wrap) :: dp
  type(gov_cca_Port_t) :: port
  type(SIDL_BaseInterface_t) :: throwaway
  type(SIDL_BaseInterface_t) :: dumex
  logical dr_port ! if dr_X true, the deleteRef(X) is needed before return.
  logical ParameterPortFactory_fetched  ! true if releaseport is needed for this port.
  type(gov_cca_ports_ParameterPortFactory_t) ::  ParameterPortFactory

! ! ! error message strings catalog
  character (LEN=*) errMsg0_ParameterPortFactory
  character (LEN=*) errMsg1_ParameterPortFactory
  character (LEN=*) errMsg2_ParameterPortFactory
  parameter(errMsg0_ParameterPortFactory= &
    'ppF.testX: Error setServices() getPort(ParameterPortFactory) failed.')
  parameter(errMsg1_ParameterPortFactory= &
    'ppF.testX: Error casting gov.cca.Port ParameterPortFactory to type gov.cca.ports.ParameterPortFactory')
  parameter(errMsg2_ParameterPortFactory= &
     'ppF.testX: Error in deleteRef(port) while getting ParameterPortFactory')
! ! ! end extra variables for handling the parameterportfactory and port

! bocca-default-code. User may edit or delete.begin(ppF.testX.setServices)
  BOCCA_EXTERNAL

  call boccaSetServices(self, services, exception) 
  BOCCA_SIDL_CHECK_F90(exception , 'setServices')

! ! 
  call set_null(port)
  call set_null(throwaway)
  call set_null(dumex)
  dr_port = .false.
  call ppF_testX__get_data_m(self,dp);

  /* Use a gov.cca.ports.ParameterPortFactory port with port name ParameterPortFactory */
  call getPort(services,"ParameterPortFactory", port, throwaway)
  BOCCA_SIDL_CHECK_F90(exception , errMsg0_ParameterPortFactory)

  ParameterPortFactory_fetched = .true. ! even if the next cast fails, must releasePort.
  call cast(port, ParameterPortFactory, exception) 
  BOCCA_SIDL_CHECK_F90(exception, errMsg1_ParameterPortFactory)
  dp%d_private_data%ppf = ParameterPortFactory
  call addRef(dp%d_private_data%ppf, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'addRef ppf error')



BOCCAEXIT continue ! target point for normal and error cleanup. do not delete.

  if (not_null(port)) then
    call deleteRef(port,throwaway)
    call checkException(self, throwaway, 'cleanup port error', .false., dumex)
    call set_null(port)
  endif



    return

! bocca-default-code. User may edit or delete.end(ppF.testX.setServices)

! DO-NOT-DELETE splicer.end(ppF.testX.setServices)
end subroutine ppF_testX_setServices_mi


! 
! Method:  releaseServices[]
! Shuts down a component presence in the calling framework.
! @param services the component instance's handle on the framework world.
! Contracts concerning Svc and setServices:
! 
! This function is called exactly once for each callback registered
! through Services.
! 
! The argument Svc will never be nil/null.
! The argument Svc will always be the same as that received in
! setServices.
! 
! During this call the component should release any interfaces
! acquired by getPort().
! 
! During this call the component should reset to nil any stored
! reference to Svc.
! 
! After this call, the component instance will be removed from the
! framework. If the component instance was created by the
! framework, it will be destroyed, not recycled, The behavior of
! any port references obtained from this component instance and
! stored elsewhere becomes undefined.
! 
! Notes for the component implementor:
! 1) The component writer may perform blocking activities
! within releaseServices, such as waiting for remote computations
! to shutdown.
! 2) It is good practice during releaseServices for the component
! writer to remove or unregister all the ports it defined.
! 

recursive subroutine ppF_testX_releaseServices_mi(self, services, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_Services
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
  ! DO-NOT-DELETE splicer.begin(ppF.testX.releaseServices.use)

  ! Insert-Code-Here {ppF.testX.releaseServices.use} (use statements)
  use gov_cca_ports_ParameterPortFactory
  use gov_cca_TypeMap

  ! DO-NOT-DELETE splicer.end(ppF.testX.releaseServices.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  type(gov_cca_Services_t) :: services ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX.releaseServices)
  type(ppF_testX_wrap) :: dp
  type(SIDL_BaseInterface_t) :: dumex, throwaway
  integer i
  character (LEN=*) errMsg1_ParameterPortFactory
  character (LEN=*) errMsg2_ParameterPortFactory
  character (LEN=*) errMsg3_ParameterPortFactory
  character (LEN=*) errMsg4_ParameterPortFactory
  parameter(errMsg1_ParameterPortFactory = &
     'ppF.testX: Error in removeParameterPort.')
  parameter(errMsg2_ParameterPortFactory = &
     'ppF.testX: Error in deleteRef for TypeMap.')
  parameter(errMsg3_ParameterPortFactory= &
     'ppF.testX: Error calling releasePort(ParameterPortFactory). Continuing.')
  parameter(errMsg4_ParameterPortFactory = &
     'ppF.testX: Error in deleteRef for port ParameterPortFactory. Continuing.')

! bocca-default-code. User may edit or delete.begin(ppF.testX.releaseServices)
    BOCCA_EXTERNAL

! ! ! clean up parameterportfactory at shutdown.

    call set_null(dumex)
    call set_null(throwaway)
    call ppF_testX__get_data_m(self,dp)
    do i=1,dp%d_private_data%numtests
      if ( not_null( dp%d_private_data%tmlist(i) ) ) then
        call removeParameterPort(dp%d_private_data%ppf, dp%d_private_data%tmlist(i), services, throwaway)
        call checkException(self, throwaway, errMsg1_ParameterPortFactory, .false., dumex)
        call deleteRef(dp%d_private_data%tmlist(i), throwaway)
        call set_null(dp%d_private_data%tmlist(i))
        call checkException(self, throwaway, errMsg2_ParameterPortFactory, .false., dumex)
      endif
    enddo
    ! release ParameterPortFactory, held from setServices
    if (not_null(dp%d_private_data%ppf) ) then
      call releasePort(services, 'ParameterPortFactory', throwaway)
      call checkException(self, throwaway, errMsg3_ParameterPortFactory, .false., dumex)
      call deleteRef(dp%d_private_data%ppf,throwaway)
      call set_null(dp%d_private_data%ppf)
      call checkException(self, throwaway, errMsg4_ParameterPortFactory, .false., dumex)
    endif

    call boccaReleaseServices(self, services, exception)
    BOCCA_SIDL_CHECK_F90(exception , 'releaseServices')
    return
    
! Exit route when there are exceptions
BOCCAEXIT      continue

    ! Insert cleanup code here if needed.

    return

! bocca-default-code. User may edit or delete.end(ppF.testX.releaseServices)
! DO-NOT-DELETE splicer.end(ppF.testX.releaseServices)
end subroutine ppF_testX_releaseServices_mi


! 
! Method:  updatedParameterValue[]
!  The component wishing to be told after a parameter is changed
! implements this function.
! @param portName the name of the port (typemap) on which the
! value was set.
! @param fieldName the name of the value in the typemap.
! 

recursive subroutine updatedParameterVandzkr3wg2z_mi(self, portName,           &
  fieldName, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
  ! DO-NOT-DELETE splicer.begin(ppF.testX.updatedParameterValue.use)
  ! Insert-Code-Here {ppF.testX.updatedParameterValue.use} (use statements)
  ! DO-NOT-DELETE splicer.end(ppF.testX.updatedParameterValue.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  character (len=*) :: portName ! in
  character (len=*) :: fieldName ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX.updatedParameterValue)
! Insert-Code-Here {ppF.testX.updatedParameterValue} (updatedParameterValue method)
 
  write(*,*) 'ppF: updateParameterValue called for port ' , portName , 'field', fieldName
  return
 
! DO-NOT-DELETE splicer.end(ppF.testX.updatedParameterValue)
end subroutine updatedParameterVandzkr3wg2z_mi


! 
! Method:  updateParameterPort[]
!  Inform the listener that someone is about to fetch their 
! typemap. The return should be true if the listener
! has changed the ParameterPort definitions.
! 

recursive subroutine updateParameterPorpuoax7wsb5_mi(self, portName, retval,   &
  exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
  ! DO-NOT-DELETE splicer.begin(ppF.testX.updateParameterPort.use)
  ! Insert-Code-Here {ppF.testX.updateParameterPort.use} (use statements)
  ! DO-NOT-DELETE splicer.end(ppF.testX.updateParameterPort.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  character (len=*) :: portName ! in
  logical :: retval ! out
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX.updateParameterPort)
! Insert-Code-Here {ppF.testX.updateParameterPort} (updateParameterPort method)
 
  write(*,*) 'ppF: updateParameterPort called for port ' , portName 
  retval = .false.
  return
! DO-NOT-DELETE splicer.end(ppF.testX.updateParameterPort)
end subroutine updateParameterPorpuoax7wsb5_mi


! 
! Method:  go[]
!  
! Execute some encapsulated functionality on the component. 
! Return 0 if ok, -1 if internal error but component may be 
! used further, and -2 if error so severe that component cannot
! be further used safely.
! 

recursive subroutine ppF_testX_go_mi(self, retval, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use ppF_testX
  use ppF_testX_impl
  ! DO-NOT-DELETE splicer.begin(ppF.testX.go.use)

  ! Insert-Code-Here {ppF.testX.go.use} (use statements)
  use gov_cca_TypeMap
  use gov_cca_Port
  use gov_cca_ports_ParameterPort
  use gov_cca_ports_ParameterPortFactory
  use gov_cca_Services
  use gov_cca_ports_ParameterGetListener
  use gov_cca_ports_ParameterSetListener

  ! DO-NOT-DELETE splicer.end(ppF.testX.go.use)
  implicit none
  type(ppF_testX_t) :: self ! in
  integer (kind=sidl_int) :: retval ! out
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(ppF.testX.go)

! Insert-User-Declarations-Here

  type(gov_cca_Port_t) :: port
  type(gov_cca_ports_ParameterPortFactory_t) :: ppf
  type(gov_cca_ports_ParameterPort_t) :: pp
  type(gov_cca_ports_ParameterGetListener_t) :: getlistener
  type(gov_cca_ports_ParameterSetListener_t) :: setlistener
  type(gov_cca_Services_t) :: services 
  type(SIDL_BaseInterface_t) :: throwaway
  type(SIDL_BaseInterface_t) :: dumex
  type(gov_cca_TypeMap_t) :: tm, tmcopy
  type(ppF_testX_wrap) :: dp
  integer numtests
  character(LEN=13) title
  character(LEN=5) pname
  character(LEN=11) suffix
  character(LEN=1024) svar ! we don't know how big it will be. >1024 will be lost
  logical dr_port ! if dr_port true, the deleteRef(port) is needed before return.
  logical pp_fetched ! if dr_X true, the releaseport pp is needed before return.
  logical noName

! ! ! error message strings catalog
  character (LEN=*) errMsg1_ParameterPort ! fixme
  character (LEN=*) errMsg3_ParameterPort ! fixme
  character (LEN=*) errMsg4_ParameterPort ! fixme
  parameter(errMsg1_ParameterPort= &
    'ppF.testX: Error casting gov.cca.Port pp to type gov.cca.ports.ParameterPort')
  parameter(errMsg3_ParameterPort= &
    'ppF.testX: Error go() releasePort(PP_n) failed.')
  parameter(errMsg4_ParameterPort= &
    'ppF.testX: Error in deleteRef(pp) while leaving go')

  BOCCA_EXTERNAL
  
  call set_null(services)
  call set_null(pp)
  call set_null(setlistener)
  call set_null(getlistener)
  call set_null(ppf)
  call set_null(port)
  call set_null(throwaway)
  call set_null(dumex)
  dr_port = .false.
  pp_fetched = .false.
  noName = .false.
  pname = 'PP_N' ! port instance name template. replace N
  title =  'Test title N' ! port instance name template. replace N
  suffix = '1234567890a'
  retval = -2 ! die if we don't detect success

  call ppF_testX__get_data_m(self,dp);
  services =  dp%d_private_data%d_services
  ppf =  dp%d_private_data%ppf

  ! these should never happen unless there is a bug elsewhere.
  if (is_null(ppf) ) then
    call BOCCA_SIDL_THROW_F90(exception, 'NULL ppf pointer in ppF.testX.go()')
  endif
  if (is_null(services) ) then
    call BOCCA_SIDL_THROW_F90(exception, 'NULL d_services pointer in ppF.testX.go()')
  endif

  if (dp%d_private_data%numtests .gt. 10) then
    write (*,*) "ppFTEST: no more parameter ports will be defined."
    retval = 0
    goto BOCCAEXIT
  endif

  dp%d_private_data%numtests = dp%d_private_data%numtests +1
  numtests = dp%d_private_data%numtests

  pname(4:4) = suffix(numtests:numtests)
  title(12:12) = suffix(numtests:numtests)

  !
  ! we store the parameters in a typemap which must be part
  ! of the object private data.
  ! For entertainment, we have a list of parameter ports
  ! which grows when go() is called.
  !
  call createTypeMap(services, tm, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go() failed to make map')
  dp%d_private_data%tmlist(numtests) = tm
  call addRef( dp%d_private_data%tmlist(numtests), exception)


  !
  ! define the data in the map
  !
  call initParameterData(ppf, tm, pname, exception)
  call setBatchTitle(ppf, tm, title, exception)

  call addRequestBoolean(ppf, tm, 'noName', &
	'var to test if default group is used', &
        'anon group', .true., exception)

  call setGroupName(ppf,tm, 'Named Set1', exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed Set1')

  call addRequestInt(ppf, tm, 'iVar', 'a ranged test int', &
'int test', 5_sidl_int, 0_sidl_int, 10_sidl_int, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed iVar')

  call addRequestLong(ppf, tm, 'jVar', 'a ranged test long', &
        'long test', -50_sidl_long, -100_sidl_long, 0_sidl_long, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed jVar')


  call setGroupName(ppf,tm, 'Named Set2', exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed Set2')

  call addRequestDouble(ppf, tm, 'dVar', 'a ranged test double', &
        'double test', -50._sidl_double, -100._sidl_double, 0._sidl_double,  exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed dVar')

  call addRequestFloat(ppf, tm, 'fVar', 'a ranged test float', &
        'float test', 50._sidl_float, -1000._sidl_float, 1000._sidl_float, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed fVar')
  

  call setGroupName(ppf,tm, 'Named Set3', exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed Set3')

  call addRequestString(ppf, tm, 'sVar', 'a free test string', &
        'string any test', 'some value', exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed sVar')

  call addRequestString(ppf, tm, 'sList', 'a choice test string', &
        'string choice test', 'some value', exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed sList')

  call addRequestStringChoice(ppf, tm, 'sList', 'choice1',  exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed choice1')

  call addRequestStringChoice(ppf, tm, 'sList', 'choice3',  exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed choice3')

  call addRequestStringChoice(ppf, tm, 'sList', 'choice2',  exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed choice2')

  write (*,*) 'ppFTEST: defined tm details for: ', pname
  
  !
  ! sign up for change events on this map
  !

  ! tell us when someone is asking for our parameters
  ! in case we want to change things before telling them.
  call cast(self, getlistener, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'wow, failed getlistener cast')
  call registerUpdater(ppf, dp%d_private_data%tmlist(numtests), getlistener, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'Failed registerUpdater')
  call deleteRef(getlistener,exception)
  BOCCA_SIDL_CHECK_F90(exception, 'Failed deleteref(getlistener)')

  ! tell us when someone is setting our parameters
  ! in case we need to update internal values based on input.
  call cast(self, setlistener, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'wow, failed setlistener cast')
  call registerUpdatedListener(ppf, dp%d_private_data%tmlist(numtests), setlistener, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'failed registerUpdatedListener')
  call deleteRef(setlistener,exception)
  BOCCA_SIDL_CHECK_F90(exception, 'Failed deleteref(setlistener)')
 

  !
  ! publish the parameter port/map pair
  !

  call addParameterPort(ppf, dp%d_private_data%tmlist(numtests), services, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'go failed addParameterPort')
  write (*,*) 'ppFTEST: published port ', pname

  !
  ! now use the 'get your own provides' feature in the spec to test
  ! the port the framework is providing on our behalf.
  !

  call getPort(services, pname, port, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'Cannot getport that just published')
  pp_fetched = .true.
  dr_port = .true.

  call cast(port, pp, exception) 
  BOCCA_SIDL_CHECK_F90(exception, errMsg1_ParameterPort)

  call readConfigurationMap(pp, tmcopy, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'failed readconfig')

  call getString(tmcopy, 'sVar', "failed svar fetch", svar, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'getString failed')
  write(*,*) 'ppFTEST: sVar = ', svar

  call getBool(tmcopy, 'noName', .false., noName, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'getBool failed')
  write(*,*) 'ppFTEST: noName = ', noName, ' (should be true)'
  
  ! modify the local map copy. not changed in tm until writeConfigurationMap
  call putBool(tmcopy, 'noName', .false., exception)
  BOCCA_SIDL_CHECK_F90(exception, 'putBool tmpcopy failed')
  call getBool(tmcopy, 'noName', .true., noName, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'getBool tmcopy failed')
  write(*,*) 'ppFTEST: noName = ', noName, ' (should be false)'

  ! commit the batch of changes from tmcopy into the parameter port
  call writeConfigurationMap(pp, tmcopy, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'writeConfigurationMap failed')

  call deleteRef(tmcopy, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'tmcopy deleteref1 failed')

  ! fetch a fresh copy. this should be a different object.
  call readConfigurationMap(pp, tmcopy, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'failed readconfig 2')

  ! make sure the change we committed stuck.
  call getBool(tmcopy, 'noName', .true., noName, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'getBool tmcopy 2 failed')
  write(*,*) 'ppFTEST: on refetch noName = ', noName, ' (should be false)'

  retval = 0

BOCCAEXIT continue ! target point for normal and error cleanup. do not delete.

  if (not_null(tmcopy)) then
    call deleteRef(tmcopy, throwaway)
    call checkException(self, throwaway, 'cleanup tmcopy error', .false., dumex)
    call set_null(tmcopy)
  endif
  if (dr_port .and. not_null(port)) then
    call deleteRef(port,throwaway)
    call checkException(self, throwaway, 'cleanup port error', .false., dumex)
    call set_null(port)
  endif

  ! release pp
  if (pp_fetched) then
    call releasePort(services, pname, throwaway)
    call checkException(self, throwaway, errMsg3_ParameterPort, .false., dumex)
    
    if ( not_null(pp) ) then
      call deleteRef(pp, throwaway)
      call checkException(self, throwaway, errMsg4_ParameterPort, .false., dumex)
      call set_null(pp)
    endif

  endif

 
 
! DO-NOT-DELETE splicer.end(ppF.testX.go)
end subroutine ppF_testX_go_mi


! DO-NOT-DELETE splicer.begin(_miscellaneous_code_end)
! Insert-Code-Here {_miscellaneous_code_end} (extra code)
! DO-NOT-DELETE splicer.end(_miscellaneous_code_end)
