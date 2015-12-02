! 
! File:          ppF_testX_Mod.F90
! Symbol:        ppF.testX-v0.0
! Symbol Type:   class
! Babel Version: 1.0.6
! Description:   Server-side private data module for ppF.testX
! 
! WARNING: Automatically generated; only changes within splicers preserved
! 
! 

#include "sidl_BaseInterface_fAbbrev.h"
#include "ppF_testX_fAbbrev.h"
module ppF_testX_impl

! DO-NOT-DELETE splicer.begin(ppF.testX.use)

! Insert include statements here
#include "gov_cca_ports_ParameterPortFactory_fAbbrev.h"
#include "gov_cca_ports_ParameterPort_fAbbrev.h"
#include "gov_cca_TypeMap_fAbbrev.h"

! Insert use statements here...
  use gov_cca_ports_ParameterPortFactory
  use gov_cca_ports_ParameterPort
  use gov_cca_TypeMap

! Bocca generated code. bocca.protected.begin(ppF.testX.use)
  ! CCA framework services module
  use gov_cca_Services
! Bocca generated code. bocca.protected.end(ppF.testX.use)

! DO-NOT-DELETE splicer.end(ppF.testX.use)

  private :: wrapObj_s

  interface wrapObj
  module procedure wrapObj_s
  end interface

  type ppF_testX_priv
    sequence
! DO-NOT-DELETE splicer.begin(ppF.testX.private_data)

! Insert user's private data here.

! Bocca generated code. bocca.protected.begin(ppF.testX.private_data)
  ! Handle to framework Services object
  type(gov_cca_Services_t) :: d_services
  type(gov_cca_ports_ParameterPortFactory_t) :: ppf
  type(gov_cca_TypeMap_t) :: tmlist(1:9)
  integer numtests;


! Bocca generated code. bocca.protected.end(ppF.testX.private_data)

! DO-NOT-DELETE splicer.end(ppF.testX.private_data)
  end type ppF_testX_priv

  type ppF_testX_wrap
    sequence
    type(ppF_testX_priv), pointer :: d_private_data
  end type ppF_testX_wrap

  contains

  recursive subroutine wrapObj_s(private_data, retval, exception)
    use ppF_testX
    use sidl_BaseInterface
    implicit none
    ! out ppF_testX retval
    type(ppF_testX_t) , intent(out) :: retval
    ! out sidl_BaseInterface exception
    type(sidl_BaseInterface_t) , intent(out) :: exception
    ! in ppF_testX_wrap private_data
    type(ppF_testX_wrap), intent(in) :: private_data
    external ppF_testX_wrapObj_m
    call ppF_testX_wrapObj_m(private_data, retval, exception)
   end subroutine wrapObj_s
end module ppF_testX_impl
