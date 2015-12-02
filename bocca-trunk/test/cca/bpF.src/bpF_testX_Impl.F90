! 
! File:          bpF_testX_Impl.F90
! Symbol:        bpF.testX-v0.0
! Symbol Type:   class
! Babel Version: 1.0.6
! Description:   Server-side implementation for bpF.testX
! 
! WARNING: Automatically generated; only changes within splicers preserved
! 
! 


! 
! Symbol "bpF.testX" (version 0.0)
! 


#include "sidl_NotImplementedException_fAbbrev.h"
#include "gov_cca_CCAException_fAbbrev.h"
#include "gov_cca_ports_GoPort_fAbbrev.h"
#include "gov_cca_ports_BasicParameterPort_fAbbrev.h"
#include "gov_cca_Port_fAbbrev.h"
#include "sidl_RuntimeException_fAbbrev.h"
#include "sidl_BaseException_fAbbrev.h"
#include "sidl_BaseClass_fAbbrev.h"
#include "gov_cca_TypeMap_fAbbrev.h"
#include "gov_cca_ComponentRelease_fAbbrev.h"
#include "gov_cca_Services_fAbbrev.h"
#include "sidl_ClassInfo_fAbbrev.h"
#include "bpF_testX_fAbbrev.h"
#include "gov_cca_Component_fAbbrev.h"
#include "sidl_BaseInterface_fAbbrev.h"
#include "sidl_string_fAbbrev.h"
! DO-NOT-DELETE splicer.begin(_miscellaneous_code_start)

! Insert-UserDecl-Here 

#include "gov_cca_TypeMap_fAbbrev.h"
#include "sidl_SIDLException_fAbbrev.h"

! Bocca generated code. bocca.protected.begin(_miscellaneous_code_start)


! bocca_update_exception. Used only in implementing BOCCA_SIDL_CHECK_F90
        logical function bue_bpF_testX(except, meth, lin) RESULT(bue)
        use sidl
        use sidl_BaseInterface
        use sidl_RuntimeException
        implicit none
        type(sidl_BaseInterface_t) :: except, etmp
        type(sidl_RuntimeException_t) :: rex
!       logical bue
        integer lin
        character (LEN=*) meth, myfilename
        parameter(myfilename='bpF_testX_Impl.F90')

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
   external bue_bpF_testX ; \
   logical bue_bpF_testX

! call BOCCA_SIDL_CLEAR_F90(except)
#define BOCCA_SIDL_CLEAR_F90(except) \
  boccaClearException(self,except)

! BOCCA_SIDL_CHECK_F90(ex,methodandmessagestring) to jump to exit if
! exception ex was thrown. See SIDL_CHECK documentation for C in babel.
#define BOCCA_SIDL_CHECK_F90(except,method) \
  if ( bue_bpF_testX(except, method) ) goto BOCCAEXIT

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

recursive subroutine bpF_testX__ctor_mi(self, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX._ctor.use)
  ! Insert-Code-Here {bpF.testX._ctor.use} (use statements)
  ! DO-NOT-DELETE splicer.end(bpF.testX._ctor.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX._ctor)

! Insert-UserDecl-Here

! bocca-default-code. User may edit or delete.begin(bpF.testX._ctor)
  ! Access private data
  type(bpF_testX_wrap) :: dp
  ! Allocate memory and initialize
  allocate(dp%d_private_data) ! crash if out of memory
  call set_null(dp%d_private_data%d_services)

! Insert-UserCode-Here

  call bpF_testX__set_data_m(self, dp)
#ifdef _BOCCA_STDERR
    write(*, *) 'CTOR bpF.testX: F90 allocated'
#endif
! bocca-default-code. User may edit or delete.end(bpF.testX._ctor)


! DO-NOT-DELETE splicer.end(bpF.testX._ctor)
end subroutine bpF_testX__ctor_mi


! 
! Method:  _ctor2[]
! Special Class constructor called when the user wants to wrap his own private data.
! 

recursive subroutine bpF_testX__ctor2_mi(self, private_data, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX._ctor2.use)
  ! Insert-Code-Here {bpF.testX._ctor2.use} (use statements)
  ! DO-NOT-DELETE splicer.end(bpF.testX._ctor2.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(bpF_testX_wrap) :: private_data
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX._ctor2)
! Insert-Code-Here {bpF.testX._ctor2} (_ctor2 method)
 
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
 
! DO-NOT-DELETE splicer.end(bpF.testX._ctor2)
end subroutine bpF_testX__ctor2_mi


! 
! Method:  _dtor[]
! Class destructor called when the class is deleted.
! 

recursive subroutine bpF_testX__dtor_mi(self, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX._dtor.use)
  ! Insert-Code-Here {bpF.testX._dtor.use} (use statements)
  ! DO-NOT-DELETE splicer.end(bpF.testX._dtor.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX._dtor)

! bocca-default-code. User may edit or delete.begin(bpF.testX._dtor)
  ! Access private data
  type(bpF_testX_wrap) :: dp
  ! Insert-UserDecl-Here 

  call bpF_testX__get_data_m(self,dp)

  ! Insert-UserCode-Here 

#ifdef _BOCCA_STDERR
    write(*, *) 'DTOR bpF.testX: F90 deallocating'
#endif
  deallocate(dp%d_private_data)
! bocca-default-code. User may edit or delete.end(bpF.testX._dtor)

  ! Insert-UserCode-Here , alternatively

! DO-NOT-DELETE splicer.end(bpF.testX._dtor)
end subroutine bpF_testX__dtor_mi


! 
! Method:  _load[]
! Static class initializer called exactly once before any user-defined method is dispatched
! 

recursive subroutine bpF_testX__load_mi(exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX._load.use)
  ! Insert-Code-Here {bpF.testX._load.use} (use statements)
  ! DO-NOT-DELETE splicer.end(bpF.testX._load.use)
  implicit none
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX._load)
! Insert-Code-Here {bpF.testX._load} (_load method)
 
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
 
! DO-NOT-DELETE splicer.end(bpF.testX._load)
end subroutine bpF_testX__load_mi


! 
! Method:  boccaSetServices[]
! 

recursive subroutine bpF_testX_boccaSetServices_mi(self, services, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_Services
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
! DO-NOT-DELETE splicer.begin(bpF.testX.boccaSetServices.use)
  use gov_cca_ComponentRelease
  use gov_cca_TypeMap
  use gov_cca_Port
! DO-NOT-DELETE splicer.end(bpF.testX.boccaSetServices.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(gov_cca_Services_t) :: services ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX.boccaSetServices)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(bpF.testX.boccaSetServices)
  
  type(bpF_testX_wrap) :: dp
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
  call bpF_testX__get_data_m(self, dp)
  ! Set my reference to the services handle
  dp%d_private_data%d_services = services
  ! Increment reference count for the services subroutine parameter
  call addRef(services, exception)
  BOCCA_SIDL_CHECK_F90(exception,'bpF.testX failed addref(services)')
  dr_services = .true.


  call createTypeMap(dp%d_private_data%d_services, typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'bpF.testX failed to createTypeMap')

  dr_port = .false.
  call cast(self, port, exception)
  BOCCA_SIDL_CHECK_F90(exception,'bpF.testX is not Port')
  dr_port = .true.

! Add gov.cca.ports.GoPort:go provides port
  call addProvidesPort(dp%d_private_data%d_services, port, &
       'go', 'gov.cca.ports.GoPort', &
       typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'bpF.testX failed addProvidesPort go ')

! Add gov.cca.ports.BasicParameterPort:tuner provides port
  call addProvidesPort(dp%d_private_data%d_services, port, &
       'tuner', 'gov.cca.ports.BasicParameterPort', &
       typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'bpF.testX failed addProvidesPort tuner ')

  dr_port = .false.
  call deleteRef(port,exception)
  BOCCA_SIDL_CHECK_F90(exception,'bpF.testX failed deleteRef(port)')

! Register gov.cca.ports.BasicParameterPort:tunertest uses port
  call registerUsesPort(dp%d_private_data%d_services, &
      'tunertest', 'gov.cca.ports.BasicParameterPort', &
      typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'bpF.testX failed registerUsesPort tunertest')

  dr_typeMap = .false.
  call deleteRef(typeMap,exception)
  BOCCA_SIDL_CHECK_F90(exception,'bpF.testX.boccaSetServices: failed deleteRef(typeMap)')

! Register component bpF.testX for release by the framework 
  call cast(self, cr, exception)
  BOCCA_SIDL_CHECK_F90(exception,'bpF.testX.boccaSetServices: is not ComponentRelease')
  call registerForRelease(dp%d_private_data%d_services, cr, exception)
  BOCCA_SIDL_CHECK_F90(exception,'bpF.testX.boccaSetServices: failed registerForRelease')
  call deleteRef(cr, exception)
  BOCCA_SIDL_CHECK_F90(exception,'bpF.testX.boccaSetServices: failed deleteRef(cr)')
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
! Bocca generated code. bocca.protected.end(bpF.testX.boccaSetServices)
! DO-NOT-DELETE splicer.end(bpF.testX.boccaSetServices)
end subroutine bpF_testX_boccaSetServices_mi


! 
! Method:  boccaReleaseServices[]
! 

recursive subroutine boccaReleaseServiczb0brjwl1y_mi(self, services,           &
  exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_Services
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX.boccaReleaseServices.use)
  ! Insert-Code-Here {bpF.testX.boccaReleaseServices.use} (use statements)
  ! DO-NOT-DELETE splicer.end(bpF.testX.boccaReleaseServices.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(gov_cca_Services_t) :: services ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX.boccaReleaseServices)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(bpF.testX.boccaReleaseServices)
  type(bpF_testX_wrap) :: dp
  type(SIDL_BaseInterface_t) :: excpt, throwaway
! trap and optionally print all port-related exceptions. ignore others.

! Access private data
  BOCCA_EXTERNAL
  call bpF_testX__get_data_m(self, dp)
  call deleteRef(dp%d_private_data%d_services, throwaway)
  call set_null(dp%d_private_data%d_services)
  call BOCCA_SIDL_CLEAR_F90(throwaway)

! Un-provide gov.cca.ports.GoPort port with port name go 
  call removeProvidesPort(services, 'go', excpt)
  call checkException(self, excpt, &
      'Error: Could not removeProvidesPort go', &
      .false., throwaway &
  )

! Un-provide gov.cca.ports.BasicParameterPort port with port name tuner 
  call removeProvidesPort(services, 'tuner', excpt)
  call checkException(self, excpt, &
      'Error: Could not removeProvidesPort tuner', &
      .false., throwaway &
  )

! Release gov.cca.ports.BasicParameterPort port with port name tunertest 
  call unregisterUsesPort(services, 'tunertest', excpt)
  call checkException(self, excpt,  &
       'Error calling unregisterUsesPort tunertest', &
       .false., throwaway &
  )

  return
! Bocca generated code. bocca.protected.end(bpF.testX.boccaReleaseServices)
! DO-NOT-DELETE splicer.end(bpF.testX.boccaReleaseServices)
end subroutine boccaReleaseServiczb0brjwl1y_mi


! 
! Method:  checkException[]
! 

recursive subroutine bpF_testX_checkException_mi(self, excpt, msg, fatal,      &
  exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
! DO-NOT-DELETE splicer.begin(bpF.testX.checkException.use)
! Bocca generated code. bocca.protected.begin(bpF.testX.checkException.use)
  use sidl_BaseException
! Bocca generated code. bocca.protected.end(bpF.testX.checkException.use)
! DO-NOT-DELETE splicer.end(bpF.testX.checkException.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(sidl_BaseInterface_t) :: excpt ! inout
  character (len=*) :: msg ! in
  logical :: fatal ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX.checkException)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(bpF.testX.checkException)

  type(sidl_BaseInterface_t) :: throwaway  ! unused exception
  type(sidl_BaseException_t) :: be
  character (LEN=4096) val

  if (not_null(excpt)) then
#ifdef _BOCCA_STDERR
    write(*, *) 'bpF.testX: ', msg
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
    if (fatal) stop 'bpF.testX.checkException called with fatal .true.'
  end if
  return
! Bocca generated code. bocca.protected.end(bpF.testX.checkException)
    
! DO-NOT-DELETE splicer.end(bpF.testX.checkException)
end subroutine bpF_testX_checkException_mi


! 
! Method:  boccaClearException[]
! 

recursive subroutine boccaClearExceptios23f_kal0e_mi(self, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX.boccaClearException.use)
  ! Insert-Code-Here {bpF.testX.boccaClearException.use} (use statements)
  ! DO-NOT-DELETE splicer.end(bpF.testX.boccaClearException.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX.boccaClearException)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(bpF.testX.boccaClearException)
        type(sidl_BaseInterface_t) :: etmp
        if (not_null(exception)) then
            call deleteRef(exception, etmp)
        endif
! Bocca generated code. bocca.protected.end(bpF.testX.boccaClearException)
! DO-NOT-DELETE splicer.end(bpF.testX.boccaClearException)
end subroutine boccaClearExceptios23f_kal0e_mi


! 
! Method:  boccaThrowException[]
! 

recursive subroutine boccaThrowExceptiog5o504qr0__mi(self, message, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
! DO-NOT-DELETE splicer.begin(bpF.testX.boccaThrowException.use)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(bpF.testX.boccaThrowException.use)
        use sidl_SIDLException
! Bocca generated code. bocca.protected.end(bpF.testX.boccaThrowException.use)
! DO-NOT-DELETE splicer.end(bpF.testX.boccaThrowException.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  character (len=*) :: message ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX.boccaThrowException)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(bpF.testX.boccaThrowException)
        type (sidl_BaseInterface_t) :: except
        type (sidl_SIDLException_t) :: einst
        character (LEN=*) myfilename
        parameter(myfilename='bpF_testX_Impl.F90')
        call new(einst, except)
        ! clear except here?
        call add(einst, myfilename, 0, message, except)
        ! clear except here?
        call cast(einst, exception, except)
        call deleteRef(einst,except)
        ! clear except here?
        return
! Bocca generated code. bocca.protected.end(bpF.testX.boccaThrowException)
! DO-NOT-DELETE splicer.end(bpF.testX.boccaThrowException)
end subroutine boccaThrowExceptiog5o504qr0__mi


! 
! Method:  boccaForceUsePortInclude[]
!  This function should never be called, but helps babel generate better code. 
! 

recursive subroutine boccaForceUsePortIa2jpbvkt47_mi(self, dummy0, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_ports_BasicParameterPort
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX.boccaForceUsePortInclude.use)
  ! Insert-Code-Here {bpF.testX.boccaForceUsePortInclude.use} (use statements)
  ! DO-NOT-DELETE splicer.end(bpF.testX.boccaForceUsePortInclude.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(gov_cca_ports_BasicParameterPort_t) :: dummy0 ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX.boccaForceUsePortInclude)
! DO-NOT-EDIT-BOCCA
! Bocca generated code. bocca.protected.begin(bpF.testX.boccaForceUsePortInclude)
  return
! Bocca generated code. bocca.protected.end(bpF.testX.boccaForceUsePortInclude)
! DO-NOT-DELETE splicer.end(bpF.testX.boccaForceUsePortInclude)
end subroutine boccaForceUsePortIa2jpbvkt47_mi


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

recursive subroutine bpF_testX_setServices_mi(self, services, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_Services
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX.setServices.use)
  ! Insert-Code-Here {bpF.testX.setServices.use} (use statements)
  use gov_cca_TypeMap
  ! DO-NOT-DELETE splicer.end(bpF.testX.setServices.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(gov_cca_Services_t) :: services ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX.setServices)
! bocca-default-code. User may edit or delete.begin(bpF.testX.setServices)
    type(bpF_testX_wrap) :: dp
    BOCCA_EXTERNAL
    call bpF_testX__get_data_m(self, dp)

    call boccaSetServices(self, services, exception) 
    BOCCA_SIDL_CHECK_F90(exception , 'setServices')

! set up the data map for the basic parameter port.
    call createTypeMap(services, dp%d_private_data%d_tunables, exception)
    BOCCA_SIDL_CHECK_F90(exception,'bpF.testX failed to createTypeMap')
    call addRef(dp%d_private_data%d_tunables, exception)
    BOCCA_SIDL_CHECK_F90(exception,'bpF.testX parameters addref failed.')

    call putInt(dp%d_private_data%d_tunables, "i1", 2_sidl_int, exception)
    BOCCA_SIDL_CHECK_F90(exception,'bpF.testX init i1 failed.')

    call putString(dp%d_private_data%d_tunables, "s1", "fred", exception)
    BOCCA_SIDL_CHECK_F90(exception,'bpF.testX init s1 failed.')

    return

! Exit route when there are exceptions
BOCCAEXIT      continue
    ! Insert cleanup code here if needed.
    return
! bocca-default-code. User may edit or delete.end(bpF.testX.setServices)

! DO-NOT-DELETE splicer.end(bpF.testX.setServices)
end subroutine bpF_testX_setServices_mi


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

recursive subroutine bpF_testX_releaseServices_mi(self, services, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_Services
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX.releaseServices.use)
  use gov_cca_TypeMap
  ! DO-NOT-DELETE splicer.end(bpF.testX.releaseServices.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(gov_cca_Services_t) :: services ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX.releaseServices)

    type(sidl_BaseInterface_t) :: throwaway
    type(bpF_testX_wrap) :: dp
    
    call bpF_testX__get_data_m(self, dp)
    call set_null(throwaway)

    call boccaReleaseServices(self, services, exception)
    
    call deleteRef(dp%d_private_data%d_tunables, throwaway)
    call BOCCA_SIDL_CLEAR_F90(throwaway)
    call set_null(dp%d_private_data%d_tunables)

    ! We just suppressed any deleteref exception that may happen.
    ! If anything bad happened in boccaReleaseServices, the
    ! caller will have to handle it.

    return

! DO-NOT-DELETE splicer.end(bpF.testX.releaseServices)
end subroutine bpF_testX_releaseServices_mi


! 
! Method:  go[]
!  
! Execute some encapsulated functionality on the component. 
! Return 0 if ok, -1 if internal error but component may be 
! used further, and -2 if error so severe that component cannot
! be further used safely.
! 

recursive subroutine bpF_testX_go_mi(self, retval, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX.go.use)

/* Bocca generated code. bocca.protected.begin(bpF.testX.go.use) */
  use gov_cca_Port
  use gov_cca_ports_BasicParameterPort
/* Bocca generated code. bocca.protected.end(bpF.testX.go.use) */
   use gov_cca_TypeMap

  ! DO-NOT-DELETE splicer.end(bpF.testX.go.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  integer (kind=sidl_int) :: retval ! out
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX.go)



! Insert-User-Declarations-Here
  type(gov_cca_TypeMap_t) :: otherParameters
  integer (kind=sidl_int) :: i1
  character (len=512) :: s1

! Bocca generated code. bocca.protected.begin(bpF.testX.go:boccaGoProlog)

  integer bocca_status
!  The user's code should set bocca_status 0 if computation proceeded ok.
!  The user's code should set bocca_status -1 if computation failed but might
!  succeed on another call to go(), e.g. wheh a required port is not yet connected.
!  The user's code should set bocca_status -2 if the computation failed and can
!  never succeed in a future call.
!  The users's code should NOT use return in this function;
!  Exceptions that are not caught in user code will be converted to status -2.
! 


  type(gov_cca_Port_t) :: port
  type(gov_cca_Services_t) :: services 
  type(SIDL_BaseInterface_t) :: throwaway
  type(SIDL_BaseInterface_t) :: dumex
  type(bpF_testX_wrap) :: dp
  logical dr_port ! if dr_X true, the deleteRef(X) is needed before return.

  type(gov_cca_ports_BasicParameterPort_t) ::  tunertest__p	! non-null if specific uses port obtained. 
  logical tunertest_fetched            ! true if releaseport is needed for this port.
  character (LEN=*) errMsg0_tunertest
  character (LEN=*) errMsg1_tunertest
  character (LEN=*) errMsg2_tunertest
  character (LEN=*) errMsg3_tunertest
  character (LEN=*) errMsg4_tunertest
  parameter(errMsg0_tunertest= &
    'bpF.testX: Error go() getPort(tunertest) failed.')
  parameter(errMsg1_tunertest= &
    'bpF.testX: Error casting gov.cca.Port tunertest to type gov.cca.ports.BasicParameterPort')
  parameter(errMsg2_tunertest= &
     'bpF.testX: Error in deleteRef(port) while getting tunertest')
  parameter(errMsg3_tunertest= &
     'bpF.testX: Error calling releasePort(tunertest). Continuing.')
  parameter(errMsg4_tunertest = &
     'bpF.testX: Error in deleteRef for port tunertest. Continuing.')


  BOCCA_EXTERNAL
  ! not crashing if something fails requires good bookkeeping and exception handling.
  call set_null(services)
  call set_null(port)
  call set_null(throwaway)
  call set_null(dumex)
  dr_port = .false.
  bocca_status = 0
  call bpF_testX__get_data_m(self,dp);
  services =  dp%d_private_data%d_services

  if (is_null(services) ) then
    call BOCCA_SIDL_THROW_F90(exception, 'NULL d_services pointer in bpF.testX.go()')
  endif

  /* Use a gov.cca.ports.BasicParameterPort port with port name tunertest */
  call getPort(services,"tunertest", port, throwaway)
  if ( not_null(throwaway) ) then
    call set_null(port)
    call checkException(self, throwaway, errMsg0_tunertest, .false., dumex)
    ! we will continue with port null (never successfully assigned) and set a flag.
  endif

  call set_null( tunertest__p)
  tunertest_fetched = .false.
  if ( not_null(port)) then
    tunertest_fetched = .true. ! even if the next cast fails, must releasePort.
    call cast(port, tunertest__p, exception) 
    BOCCA_SIDL_CHECK_F90(exception, errMsg1_tunertest)
    call deleteRef(port, exception)
    call set_null(port) 
    BOCCA_SIDL_CHECK_F90(exception, errMsg2_tunertest)
  endif


/* Bocca generated code. bocca.protected.end(bpF.testX.go:boccaGoProlog) */

  if (is_null(tunertest__p)) then
    bocca_status = -1 ! not connected. try again later
    goto BOCCAEXIT
  endif

  call set_null(otherParameters)
  i1 = 0
  call readConfigurationMap(tunertest__p, otherParameters, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'Error getting otherParameters') 

  call getInt(otherParameters, 'i1', -1, i1, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'Error getting i1') 
  write(*,*) 'BPF from otherParameters got i1= ', i1

  s1 = CHAR(0)
  call getString(otherParameters, 's1', 'dummydefault', s1, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'Error getting s1') 
  write(*,*) 'BPF from otherParameters got s1= ', s1

  call putInt(otherParameters, 'i1', 888888_sidl_int, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'Error setting i1 in local copy') 

  call putString(otherParameters, 's1', 'myUPPERSTRING', exception)
  BOCCA_SIDL_CHECK_F90(exception, 'Error setting s1 in local copy') 

  call writeConfigurationMap(tunertest__p, otherParameters, exception)
  BOCCA_SIDL_CHECK_F90(exception, 'Error pushing parameter set to other component') 

!    If unknown exceptions in the user code are tolerable and restart is ok, set bocca_status -1 instead.
!    -2 means the component is so confused that it and probably the application should be
!    destroyed.
! 


BOCCAEXIT continue ! target point for normal and error cleanup. do not delete.

  ! clean up our customized variables.
  if (not_null(otherParameters)) then
    call deleteRef(otherParameters, throwaway)
    call checkException(self, throwaway, 'err deleting otherParameters', .false., dumex)
    call set_null(otherParameters)
  endif

/* Bocca generated code. bocca.protected.begin(bpF.testX.go:boccaGoEpilog) */

  if (not_null(port)) then
    call deleteRef(port,throwaway)
    call checkException(self, throwaway, 'cleanup port error', .false., dumex)
    call set_null(port)
  endif

  ! release tunertest
  if (tunertest_fetched) then
    tunertest_fetched = .false.
    call releasePort(services, 'tunertest', throwaway)
    call checkException(self, throwaway, errMsg3_tunertest, .false., dumex)
    
    if ( not_null(tunertest__p) ) then
      call deleteRef(tunertest__p, throwaway)
      call checkException(self, throwaway, errMsg4_tunertest, .false., dumex)
      call set_null(tunertest__p)
    endif

  endif


/* Bocca generated code. bocca.protected.end(bpF.testX.go:boccaGoEpilog) */


  retval = bocca_status
 
 
! DO-NOT-DELETE splicer.end(bpF.testX.go)
end subroutine bpF_testX_go_mi


! 
! Method:  readConfigurationMap[]
!  Return a TypeMap of runtime configuration parameters. 
! It is recommended that the map returned be a clone/copy of the
! a privately held map, not a shared object reference.
! 

recursive subroutine readConfigurationMda0z34egqo_mi(self, retval, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_TypeMap
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX.readConfigurationMap.use)
  ! Insert-Code-Here {bpF.testX.readConfigurationMap.use} (use statements)
  ! DO-NOT-DELETE splicer.end(bpF.testX.readConfigurationMap.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(gov_cca_TypeMap_t) :: retval ! out
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX.readConfigurationMap)
 
  type(bpF_testX_wrap) :: dp

  call bpF_testX__get_data_m(self,dp);

  ! copy our private data into retval.
  call cloneTypeMap(dp%d_private_data%d_tunables, retval, exception)
  ! if there is an exception, we are lazy and let the caller handle it.
  ! The most we could do would be add to the stack trace.
 
! DO-NOT-DELETE splicer.end(bpF.testX.readConfigurationMap)
end subroutine readConfigurationMda0z34egqo_mi


! 
! Method:  writeConfigurationMap[]
!  Copy the parameter values given in map into the
! internal map, for those parameters which
! are already defined by the internal map.
! The outsider does not get to cause arbitrary
! keys to be copied into the internal map.
! @throws gov.cca.CCAException if TypeMap operations fail.
! 

recursive subroutine writeConfiguration2m94vvwzhg_mi(self, map, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_TypeMap
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX.writeConfigurationMap.use)
  use gov_cca_Type
  ! DO-NOT-DELETE splicer.end(bpF.testX.writeConfigurationMap.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(gov_cca_TypeMap_t) :: map ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX.writeConfigurationMap)
  ! this implementation of writeConfigurationMap
  ! assumes (hard codes) the parameter names and types allowed.
  ! a generic version is possible by looping over the d_tunables
  ! and checking for matches with the input map.
  ! The way shown here is compatible with private storage
  ! in forms other than d_tunables.

  type(bpF_testX_wrap) :: dp
  logical :: mapHasKey
  integer (kind=sidl_enum) :: fieldType
  integer (kind=sidl_int) :: itmp
  character (len=512) :: stmp

  BOCCA_EXTERNAL
  call bpF_testX__get_data_m(self,dp);
  itmp = 0
  fieldType = NoType

  if (not_null(map)) then
    ! copy i1 into our data
    call hasKey(map, 'i1', mapHasKey, exception)
    BOCCA_SIDL_CHECK_F90(exception, 'writeConfigurationMap i1 search') 
    if (mapHasKey) then
      call typeOf(map, 'i1', fieldType, exception)
      BOCCA_SIDL_CHECK_F90(exception, 'i1 typeof error') 
      if (fieldType .eq. Int) then
        call getInt(map, 'i1', itmp, itmp, exception)
        BOCCA_SIDL_CHECK_F90(exception, 'i1 getint error') 
        call putInt(dp%d_private_data%d_tunables, 'i1', itmp, exception)
        BOCCA_SIDL_CHECK_F90(exception, 'i1 putint error') 
      endif
    endif

    ! copy s1 into our data
    call hasKey(map, 's1', mapHasKey, exception)
    BOCCA_SIDL_CHECK_F90(exception, 'writeConfigurationMap s1 search') 
    if (mapHasKey) then
      call typeOf(map, 's1', fieldType, exception)
      BOCCA_SIDL_CHECK_F90(exception, 's1 typeof error') 
      if (fieldType .eq. String) then
        stmp = char(0)
        call getString(map, 's1', stmp, stmp, exception)
        BOCCA_SIDL_CHECK_F90(exception, 's1 getstring error') 
        call putString(dp%d_private_data%d_tunables, 's1', stmp, exception)
        BOCCA_SIDL_CHECK_F90(exception, 's1 putstring error') 
      endif
    endif

  endif

  
BOCCAEXIT  continue
 
  return
! DO-NOT-DELETE splicer.end(bpF.testX.writeConfigurationMap)
end subroutine writeConfiguration2m94vvwzhg_mi


! 
! Method:  readConfigurationKeys[]
!  Fetch the list of keys in the TypeMap that are
! for public configuration purposes. Other values found in
! the TypeMap must not be changed.
! 

recursive subroutine readConfigurationKm2nx5lwgss_mi(self, retval, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use bpF_testX
  use sidl_string_array
  use bpF_testX_impl
  ! DO-NOT-DELETE splicer.begin(bpF.testX.readConfigurationKeys.use)
  ! Insert-Code-Here {bpF.testX.readConfigurationKeys.use} (use statements)
  ! DO-NOT-DELETE splicer.end(bpF.testX.readConfigurationKeys.use)
  implicit none
  type(bpF_testX_t) :: self ! in
  type(sidl_string_1d) :: retval ! out
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(bpF.testX.readConfigurationKeys)
! Insert-Code-Here {bpF.testX.readConfigurationKeys} (readConfigurationKeys method)
 
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
 
! DO-NOT-DELETE splicer.end(bpF.testX.readConfigurationKeys)
end subroutine readConfigurationKm2nx5lwgss_mi


! DO-NOT-DELETE splicer.begin(_miscellaneous_code_end)
! Insert-Code-Here {_miscellaneous_code_end} (extra code)
! DO-NOT-DELETE splicer.end(_miscellaneous_code_end)
