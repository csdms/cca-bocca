! 
! File:          pytest_f_Impl.F90
! Symbol:        pytest.f-v0.0
! Symbol Type:   class
! Babel Version: 1.0.6
! Description:   Server-side implementation for pytest.f
! 
! WARNING: Automatically generated; only changes within splicers preserved
! 
! 


! 
! Symbol "pytest.f" (version 0.0)
! 


#include "sidl_NotImplementedException_fAbbrev.h"
#include "gov_cca_CCAException_fAbbrev.h"
#include "gov_cca_ComponentRelease_fAbbrev.h"
#include "pytest_f_fAbbrev.h"
#include "gov_cca_Services_fAbbrev.h"
#include "sidl_ClassInfo_fAbbrev.h"
#include "gov_cca_Port_fAbbrev.h"
#include "gov_cca_Component_fAbbrev.h"
#include "pytest_x_fAbbrev.h"
#include "sidl_BaseInterface_fAbbrev.h"
#include "sidl_RuntimeException_fAbbrev.h"
#include "sidl_BaseException_fAbbrev.h"
#include "sidl_BaseClass_fAbbrev.h"
! DO-NOT-DELETE splicer.begin(_miscellaneous_code_start)

! Bocca generated code. bocca.protected.begin(_miscellaneous_code_start)

! bocca_update_exception. Would be nice if this were part of babel f90 binding.
! such that a f90 version of C SIDL_CHECK existed.
        logical function bue_pytest_f(except, meth, lin) RESULT(bue)
        use sidl
        use sidl_BaseInterface
        use sidl_RuntimeException
        implicit none
        type(sidl_BaseInterface_t) :: except, etmp
        type(sidl_RuntimeException_t) :: rex
        logical bue
        integer lin
        character (LEN=*) meth, myfilename
        parameter(myfilename='pytest_f_Impl.F90')

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

! bocca_clear_exception. Would be nice if this were part of babel f90 binding.
! such that a f90 version of C SIDL_CLEAR existed.
        subroutine bce_pytest_f(exception)
        use sidl
        use sidl_BaseInterface
        type(sidl_BaseInterface_t) :: exception, etmp
        if (not_null(exception)) then
            call deleteRef(exception, etmp)
        endif
        return
        end

! Exit statement not normally reached (or needed) unless BOCCA_SIDL_CHECK_F90
! is used and finds an exception. 
#define BOCCAEXIT 20331
! Any method using BOCCA_SIDL_CHECK_F90 must start user code with BOCCA_EXTERNAL
#define BOCCA_EXTERNAL \
   external bce_pytest_f ; \
   external bue_pytest_f ; \
   logical bue_pytest_f

#define BOCCA_SIDL_CLEAR_F90(except) \
  bce_pytest_f(except)

#define BOCCA_SIDL_CHECK_F90(except,method) \
  if ( bue_pytest_f(except, method) ) goto BOCCAEXIT

! Bocca generated code. bocca.protected.end(_miscellaneous_code_start)

! Insert-UserDecl-Here

! DO-NOT-DELETE splicer.end(_miscellaneous_code_start)




! 
! Method:  _ctor[]
! Class constructor called when the class is created.
! 

recursive subroutine pytest_f__ctor_mi(self, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use pytest_f
  use pytest_f_impl
  ! DO-NOT-DELETE splicer.begin(pytest.f._ctor.use)
  ! Insert-Code-Here {pytest.f._ctor.use} (use statements)
  ! DO-NOT-DELETE splicer.end(pytest.f._ctor.use)
  implicit none
  type(pytest_f_t) :: self ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(pytest.f._ctor)

! Insert-UserDecl-Here

! bocca-default-code. User may edit or delete.begin(pytest.f._ctor)
  ! Access private data
  type(pytest_f_wrap) :: dp
  ! Allocate memory and initialize
  allocate(dp%d_private_data) ! crash if out of memory
  call set_null(dp%d_private_data%d_services)
  call pytest_f__set_data_m(self, dp)
#ifdef _BOCCA_STDERR
    write(*, *) 'CTOR pytest.f: F90 allocated'
#endif
! bocca-default-code. User may edit or delete.end(pytest.f._ctor)

! Insert-UserCode-Here

! DO-NOT-DELETE splicer.end(pytest.f._ctor)
end subroutine pytest_f__ctor_mi


! 
! Method:  _ctor2[]
! Special Class constructor called when the user wants to wrap his own private data.
! 

recursive subroutine pytest_f__ctor2_mi(self, private_data, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use pytest_f
  use pytest_f_impl
  ! DO-NOT-DELETE splicer.begin(pytest.f._ctor2.use)
  ! Insert-Code-Here {pytest.f._ctor2.use} (use statements)
  ! DO-NOT-DELETE splicer.end(pytest.f._ctor2.use)
  implicit none
  type(pytest_f_t) :: self ! in
  type(pytest_f_wrap) :: private_data
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(pytest.f._ctor2)
! Insert-Code-Here {pytest.f._ctor2} (_ctor2 method)
 
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
 
! DO-NOT-DELETE splicer.end(pytest.f._ctor2)
end subroutine pytest_f__ctor2_mi


! 
! Method:  _dtor[]
! Class destructor called when the class is deleted.
! 

recursive subroutine pytest_f__dtor_mi(self, exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use pytest_f
  use pytest_f_impl
  ! DO-NOT-DELETE splicer.begin(pytest.f._dtor.use)
  ! Insert-Code-Here {pytest.f._dtor.use} (use statements)
  ! DO-NOT-DELETE splicer.end(pytest.f._dtor.use)
  implicit none
  type(pytest_f_t) :: self ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(pytest.f._dtor)
! bocca-default-code. User may edit or delete.begin(pytest.f._dtor)
  ! Access private data
  type(pytest_f_wrap) :: dp
  ! Insert-UserCode-Here Needs to be allowed and is not. FIXME bocca.
  call pytest_f__get_data_m(self,dp)
#ifdef _BOCCA_STDERR
    write(*, *) 'DTOR pytest.f: F90 deallocating'
#endif
  deallocate(dp%d_private_data)
! bocca-default-code. User may edit or delete.end(pytest.f._dtor)
! DO-NOT-DELETE splicer.end(pytest.f._dtor)
end subroutine pytest_f__dtor_mi


! 
! Method:  _load[]
! Static class initializer called exactly once before any user-defined method is dispatched
! 

recursive subroutine pytest_f__load_mi(exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use pytest_f
  use pytest_f_impl
  ! DO-NOT-DELETE splicer.begin(pytest.f._load.use)
  ! Insert-Code-Here {pytest.f._load.use} (use statements)
  ! DO-NOT-DELETE splicer.end(pytest.f._load.use)
  implicit none
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(pytest.f._load)
! Insert-Code-Here {pytest.f._load} (_load method)
 
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
 
! DO-NOT-DELETE splicer.end(pytest.f._load)
end subroutine pytest_f__load_mi


! 
! Method:  boccaSetServices[]
! 

recursive subroutine pytest_f_boccaSetServices_mi(self, services, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_Services
  use sidl_BaseInterface
  use sidl_RuntimeException
  use pytest_f
  use pytest_f_impl
! DO-NOT-DELETE splicer.begin(pytest.f.boccaSetServices.use)
  use gov_cca_CCAException
  use gov_cca_ComponentRelease
  use gov_cca_TypeMap
  use gov_cca_Port
! DO-NOT-DELETE splicer.end(pytest.f.boccaSetServices.use)
  implicit none
  type(pytest_f_t) :: self ! in
  type(gov_cca_Services_t) :: services ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(pytest.f.boccaSetServices)
! Bocca generated code. bocca.protected.begin(pytest.f.boccaSetServices)
  
  type(pytest_f_wrap) :: dp
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
  call pytest_f__get_data_m(self, dp)
  ! Set my reference to the services handle
  dp%d_private_data%d_services = services
  ! Increment reference count for the services subroutine parameter
  call addRef(services, exception)
  BOCCA_SIDL_CHECK_F90(exception,'boccaSetServices:addref(services)')
  dr_services = .true.


  call createTypeMap(dp%d_private_data%d_services, typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'boccaSetServices:createTypeMap')

  dr_port = .false.
  call cast(self, port, exception)
  BOCCA_SIDL_CHECK_F90(exception,'pytest.f.boccaSetServices: is not gov.cca.Port')
  dr_port = .true.

! Add pytest.x:MYX provides port
  call addProvidesPort(dp%d_private_data%d_services, port, &
       'MYX', 'pytest.x', &
       typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'pytest.f.boccaSetServices: failed addProvidesPort MYX ')

  dr_port = .false.
  call deleteRef(port,exception)
  BOCCA_SIDL_CHECK_F90(exception,'pytest.f.boccaSetServices: failed deleteRef(port)')

! Register pytest.x:YOURX uses port
  call registerUsesPort(dp%d_private_data%d_services, &
      'YOURX', 'pytest.x', &
      typeMap, exception)
  BOCCA_SIDL_CHECK_F90(exception,'pytest.f.boccaSetServices: failed registerUsesPort YOURX')

  dr_typeMap = .false.
  call deleteRef(typeMap,exception)
  BOCCA_SIDL_CHECK_F90(exception,'pytest.f.boccaSetServices: failed deleteRef(typeMap)')

! Register component pytest.f for release by the framework 
  call cast(self, cr, exception)
  BOCCA_SIDL_CHECK_F90(exception,'pytest.f.boccaSetServices: is not ComponentRelease')
  call registerForRelease(dp%d_private_data%d_services, cr, exception)
  BOCCA_SIDL_CHECK_F90(exception,'pytest.f.boccaSetServices: failed registerForRelease')
  call deleteRef(cr, exception)
  BOCCA_SIDL_CHECK_F90(exception,'pytest.f.boccaSetServices: failed deleteRef(cr)')
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
! Bocca generated code. bocca.protected.end(pytest.f.boccaSetServices)
! DO-NOT-DELETE splicer.end(pytest.f.boccaSetServices)
end subroutine pytest_f_boccaSetServices_mi


! 
! Method:  boccaReleaseServices[]
! 

recursive subroutine boccaReleaseServicu_aim8_8ci_mi(self, services,           &
  exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_Services
  use sidl_BaseInterface
  use sidl_RuntimeException
  use pytest_f
  use pytest_f_impl
  ! DO-NOT-DELETE splicer.begin(pytest.f.boccaReleaseServices.use)
  ! Insert-Code-Here {pytest.f.boccaReleaseServices.use} (use statements)
  ! DO-NOT-DELETE splicer.end(pytest.f.boccaReleaseServices.use)
  implicit none
  type(pytest_f_t) :: self ! in
  type(gov_cca_Services_t) :: services ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(pytest.f.boccaReleaseServices)
! Bocca generated code. bocca.protected.begin(pytest.f.boccaReleaseServices)
  type(pytest_f_wrap) :: dp
  type(SIDL_BaseInterface_t) :: excpt, throwaway
  character (LEN=*) msg1, msg2
  parameter( msg1='Error: Could not removeProvidesPort @PORT_INSTANCE@')
  parameter( msg2='Error calling unregisterUsesPort @PORT_INSTANCE@')
! trap and optionally print all port-related exceptions. ignore others.

! Access private data
  BOCCA_EXTERNAL
  call pytest_f__get_data_m(self, dp)
  call deleteRef(dp%d_private_data%d_services, throwaway)
  call set_null(dp%d_private_data%d_services)
  call BOCCA_SIDL_CLEAR_F90(throwaway)

! Un-provide pytest.x port with port name MYX 
  call removeProvidesPort(services, 'MYX', excpt)
  call checkException(self, excpt,  msg1, .false., throwaway)

! Release pytest.x port with port name YOURX 
  call unregisterUsesPort(services, 'YOURX', excpt)
  call checkException(self, excpt, msg2, .false., throwaway)

  return
! Bocca generated code. bocca.protected.end(pytest.f.boccaReleaseServices)
! DO-NOT-DELETE splicer.end(pytest.f.boccaReleaseServices)
end subroutine boccaReleaseServicu_aim8_8ci_mi


! 
! Method:  checkException[]
! 

recursive subroutine pytest_f_checkException_mi(self, excpt, msg, fatal,       &
  exception)
  use sidl
  use sidl_NotImplementedException
  use sidl_BaseInterface
  use sidl_RuntimeException
  use pytest_f
  use pytest_f_impl
! DO-NOT-DELETE splicer.begin(pytest.f.checkException.use)
! Bocca generated code. bocca.protected.begin(pytest.f.checkException.use)
  use sidl_BaseException
! Bocca generated code. bocca.protected.end(pytest.f.checkException.use)
! DO-NOT-DELETE splicer.end(pytest.f.checkException.use)
  implicit none
  type(pytest_f_t) :: self ! in
  type(sidl_BaseInterface_t) :: excpt ! inout
  character (len=*) :: msg ! in
  logical :: fatal ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(pytest.f.checkException)

! Bocca generated code. bocca.protected.begin(pytest.f.checkException)

  type(sidl_BaseInterface_t) :: throwaway  ! unused exception
  type(sidl_BaseException_t) :: be
  character (LEN=513) val

  if (not_null(excpt)) then
#ifdef _BOCCA_STDERR
    write(*, *) 'pytest.f: ', msg
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
    if (fatal) stop 'pytest.f.checkException called with fatal .true.'
  end if
  return
! Bocca generated code. bocca.protected.end(pytest.f.checkException)
    
! DO-NOT-DELETE splicer.end(pytest.f.checkException)
end subroutine pytest_f_checkException_mi


! 
! Method:  boccaForceUsePortInclude[]
! 

recursive subroutine boccaForceUsePortIm8vpei6rd5_mi(self, dummy0, exception)
  use sidl
  use sidl_NotImplementedException
  use pytest_x
  use sidl_BaseInterface
  use sidl_RuntimeException
  use pytest_f
  use pytest_f_impl
  ! DO-NOT-DELETE splicer.begin(pytest.f.boccaForceUsePortInclude.use)
  ! Insert-Code-Here {pytest.f.boccaForceUsePortInclude.use} (use statements)
  ! DO-NOT-DELETE splicer.end(pytest.f.boccaForceUsePortInclude.use)
  implicit none
  type(pytest_f_t) :: self ! in
  type(pytest_x_t) :: dummy0 ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(pytest.f.boccaForceUsePortInclude)
! Bocca generated code. bocca.protected.begin(pytest.f.boccaForceUsePortInclude)
  return
! Bocca generated code. bocca.protected.end(pytest.f.boccaForceUsePortInclude)
! DO-NOT-DELETE splicer.end(pytest.f.boccaForceUsePortInclude)
end subroutine boccaForceUsePortIm8vpei6rd5_mi


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

recursive subroutine pytest_f_setServices_mi(self, services, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_Services
  use sidl_BaseInterface
  use sidl_RuntimeException
  use pytest_f
  use pytest_f_impl
  ! DO-NOT-DELETE splicer.begin(pytest.f.setServices.use)
  ! Insert-Code-Here {pytest.f.setServices.use} (use statements)
  ! DO-NOT-DELETE splicer.end(pytest.f.setServices.use)
  implicit none
  type(pytest_f_t) :: self ! in
  type(gov_cca_Services_t) :: services ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(pytest.f.setServices)
! bocca-default-code. User may edit or delete.begin(pytest.f.setServices)
    BOCCA_EXTERNAL
    call boccaSetServices(self, services, exception) 
    BOCCA_SIDL_CHECK_F90(exception , 'setServices')

    ! Insert-UserCode-Here

    return

! Exit route when there are exceptions
BOCCAEXIT      continue
    ! Insert cleanup code here if needed.
    return
! bocca-default-code. User may edit or delete.end(pytest.f.setServices)

! DO-NOT-DELETE splicer.end(pytest.f.setServices)
end subroutine pytest_f_setServices_mi


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

recursive subroutine pytest_f_releaseServices_mi(self, services, exception)
  use sidl
  use sidl_NotImplementedException
  use gov_cca_CCAException
  use gov_cca_Services
  use sidl_BaseInterface
  use sidl_RuntimeException
  use pytest_f
  use pytest_f_impl
  ! DO-NOT-DELETE splicer.begin(pytest.f.releaseServices.use)
  ! Insert-Code-Here {pytest.f.releaseServices.use} (use statements)
  ! DO-NOT-DELETE splicer.end(pytest.f.releaseServices.use)
  implicit none
  type(pytest_f_t) :: self ! in
  type(gov_cca_Services_t) :: services ! in
  type(sidl_BaseInterface_t) :: exception ! out

! DO-NOT-DELETE splicer.begin(pytest.f.releaseServices)

! bocca-default-code. User may edit or delete.begin(pytest.f.releaseServices)
    BOCCA_EXTERNAL

! Insert-UserCode-Here {pytest.f.releaseServices} (releaseServices method)

    call boccaReleaseServices(self, services, exception)
    BOCCA_SIDL_CHECK_F90(exception , 'releaseServices')
    return
    
! Exit route when there are exceptions
BOCCAEXIT      continue
    ! Insert cleanup code here if needed.
    return

! bocca-default-code. User may edit or delete.end(pytest.f.releaseServices)
! DO-NOT-DELETE splicer.end(pytest.f.releaseServices)
end subroutine pytest_f_releaseServices_mi


! DO-NOT-DELETE splicer.begin(_miscellaneous_code_end)
! Insert-Code-Here {_miscellaneous_code_end} (extra code)
! DO-NOT-DELETE splicer.end(_miscellaneous_code_end)
