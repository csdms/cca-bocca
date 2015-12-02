! 
! File:          bpF_testX_Mod.F90
! Symbol:        bpF.testX-v0.0
! Symbol Type:   class
! Babel Version: 1.0.6
! Description:   Server-side private data module for bpF.testX
! 
! WARNING: Automatically generated; only changes within splicers preserved
! 
! 

#include "sidl_BaseInterface_fAbbrev.h"
#include "bpF_testX_fAbbrev.h"
module bpF_testX_impl

! DO-NOT-DELETE splicer.begin(bpF.testX.use)

! Insert use statements here...
#include "gov_cca_TypeMap_fAbbrev.h"

  use gov_cca_TypeMap
! Bocca generated code. bocca.protected.begin(bpF.testX.use)
  ! CCA framework services module
  use gov_cca_Services
! Bocca generated code. bocca.protected.end(bpF.testX.use)

! DO-NOT-DELETE splicer.end(bpF.testX.use)

  private :: wrapObj_s

  interface wrapObj
  module procedure wrapObj_s
  end interface

  type bpF_testX_priv
    sequence
! DO-NOT-DELETE splicer.begin(bpF.testX.private_data)

! Insert user's private data here.

! Bocca generated code. bocca.protected.begin(bpF.testX.private_data)
  ! Handle to framework Services object
  type(gov_cca_Services_t) :: d_services
  type(gov_cca_TypeMap_t) :: d_tunables
! Bocca generated code. bocca.protected.end(bpF.testX.private_data)

! DO-NOT-DELETE splicer.end(bpF.testX.private_data)
  end type bpF_testX_priv

  type bpF_testX_wrap
    sequence
    type(bpF_testX_priv), pointer :: d_private_data
  end type bpF_testX_wrap

  contains

  recursive subroutine wrapObj_s(private_data, retval, exception)
    use bpF_testX
    use sidl_BaseInterface
    implicit none
    ! out bpF_testX retval
    type(bpF_testX_t) , intent(out) :: retval
    ! out sidl_BaseInterface exception
    type(sidl_BaseInterface_t) , intent(out) :: exception
    ! in bpF_testX_wrap private_data
    type(bpF_testX_wrap), intent(in) :: private_data
    external bpF_testX_wrapObj_m
    call bpF_testX_wrapObj_m(private_data, retval, exception)
   end subroutine wrapObj_s
end module bpF_testX_impl
