C       
C       File:          pytest_g_Impl.f
C       Symbol:        pytest.g-v0.0
C       Symbol Type:   class
C       Babel Version: 1.0.6
C       Description:   Server-side implementation for pytest.g
C       
C       WARNING: Automatically generated; only changes within splicers preserved
C       
C       


C       
C       Symbol "pytest.g" (version 0.0)
C       


C       DO-NOT-DELETE splicer.begin(_miscellaneous_code_start)
C       Insert-Code-Here {_miscellaneous_code_start} (extra code)
C       DO-NOT-DELETE splicer.end(_miscellaneous_code_start)




C       
C       Method:  _ctor[]
C       Class constructor called when the class is created.
C       

        subroutine pytest_g__ctor_fi(self, exception)
        implicit none
C        in pytest.g self
        integer*8 self
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(pytest.g._ctor)

C       bocca-default-code. User may edit or delete.begin(pytest.g._ctor)
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
           write(*,*) 'pytest.g 
     &     ERROR: creating state array. Object will be useless.'
           return
        endif
        call pytest_g__set_data_f(self, stateArray)

C       Insert-UserInitializationCode-Here 

C       bocca-default-code. User may edit or delete.end(pytest.g._ctor)
C       DO-NOT-DELETE splicer.end(pytest.g._ctor)
        end


C       
C       Method:  _ctor2[]
C       Special Class constructor called when the user wants to wrap his own private data.
C       

        subroutine pytest_g__ctor2_fi(self, private_data, exception)
        implicit none
C        in pytest.g self
        integer*8 self
C        in opaque private_data
        integer*8 private_data
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(pytest.g._ctor2)
C       Insert-Code-Here {pytest.g._ctor2} (_ctor2 method)
 
C       DO-DELETE-WHEN-IMPLEMENTING exception.begin() 
C 
C This method has not been implemented
C 
        integer*8 throwaway
        call sidl_NotImplementedException__create_f
     $      (exception, throwaway)
        if (exception .ne. 0) then
           call sidl_NotImplementedException_setNote_f(
     $         exception,
     $         'This method has not been implemented',
     $         throwaway)
        endif
        return
C       DO-DELETE-WHEN-IMPLEMENTING exception.end() 
 
C       DO-NOT-DELETE splicer.end(pytest.g._ctor2)
        end


C       
C       Method:  _dtor[]
C       Class destructor called when the class is deleted.
C       

        subroutine pytest_g__dtor_fi(self, exception)
        implicit none
C        in pytest.g self
        integer*8 self
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(pytest.g._dtor)
C       bocca-default-code. User may edit or delete.begin(pytest.g._dtor)

C       Insert-UserCleanupDeclarationsCode-Here {pytest.g:_dtor} (_dtor method)

C       Cleaning up the other stateArray elements is the users's problem.
C       bocca takes care of element 0.
C
        integer*8  stateArray, excpt, exdummy, knull

        call pytest_g__get_data_f(
     & self, stateArray)
        knull=0
        call pytest_g__set_data_f(
     & self, knull)
        
        call sidl_opaque__array_deleteRef_f(stateArray, excpt)
        if (excpt .ne. 0) then
            call sidl_BaseException_deleteRef_f(excpt, exdummy)
        endif
        
C	Insert-UserCleanupCode-Here

C       bocca-default-code. User may edit or delete.begin(pytest.g._dtor)
C       DO-NOT-DELETE splicer.end(pytest.g._dtor)
        end


C       
C       Method:  _load[]
C       Static class initializer called exactly once before any user-defined method is dispatched
C       

        subroutine pytest_g__load_fi(exception)
        implicit none
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(pytest.g._load)
C       Insert-Code-Here {pytest.g._load} (_load method)
 
C       DO-DELETE-WHEN-IMPLEMENTING exception.begin() 
C 
C This method has not been implemented
C 
        integer*8 throwaway
        call sidl_NotImplementedException__create_f
     $      (exception, throwaway)
        if (exception .ne. 0) then
           call sidl_NotImplementedException_setNote_f(
     $         exception,
     $         'This method has not been implemented',
     $         throwaway)
        endif
        return
C       DO-DELETE-WHEN-IMPLEMENTING exception.end() 
 
C       DO-NOT-DELETE splicer.end(pytest.g._load)
        end


C       
C       Method:  boccaSetServices[]
C       

        subroutine pytest_g_boccaSetServices_fi(self, services, 
     &     exception)
        implicit none
C        in pytest.g self
        integer*8 self
C        in gov.cca.Services services
        integer*8 services
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(pytest.g.boccaSetServices)
C       Bocca generated code. bocca.protected.begin(pytest.g.boccaSetServices)

        integer *8  stateArray
        integer *8  d_services
        integer *8  compRelease

        integer *8 typeMap
        integer *8 port

        call pytest_g__get_data_f(
     & self, stateArray)
        if (stateArray .eq. 0) then
           write(*,*) 'pytest.g: 
     &  ERROR: Null stateArray'
           return
        end if
        d_services = services
        call sidl_opaque__array_set1_f(stateArray, 
     &   0, d_services)
        call gov_cca_Services_addRef_f(
     & d_services, exception)

        call gov_cca_Services_createTypeMap_f(
     &              d_services, 
     &              typeMap,
     &              exception)
        if (exception .ne. 0) then 
           print *, 'pytest.g: 
     &  Error creating type map'
           return
        endif

        call pytest_g__cast2_f(
     & self,
     &                  'gov.cca.Port', 
     &                  port,
     &                  exception)
        if (exception .ne. 0) then
           print *, 'pytest.g: 
     &  Error casting self to gov.cca.Port'
           call gov_cca_TypeMap_deleteRef_f(
     &            typeMap, 
     &            exception) 
           return
        end if
        
C       Add pytest.x:MYX provides port
        call gov_cca_Services_addProvidesPort_f(
     &       d_services, 
     &       port, 
     &       'MYX', 
     &       'pytest.x', 
     &       typeMap, 
     &       exception)
        if (exception .ne. 0) then
           print *, 'pytest.g: 
     &  Error in call to addProvidesPort()'
           call gov_cca_TypeMap_deleteRef_f(
     &            typeMap, 
     &            exception)
           return 
        end if

           call gov_cca_Port_deleteRef_f(
     &            port, 
     &            exception) 

C       Register pytest.x:YOURX uses port
        call gov_cca_Services_registerUsesPort_f(
     &       d_services,
     &       'YOURX', 
     &       'pytest.x', 
     &       typeMap, 
     &       exception)
        if (exception .ne. 0) then
           print *, 'pytest.g: 
     &         Error in call to registerUsesPort()'
           call gov_cca_TypeMap_deleteRef_f(
     &            typeMap, 
     &            exception)
           return
        end if

        call gov_cca_TypeMap_deleteRef_f(
     &         typeMap, 
     &         exception)

        call pytest_g__cast2_f(
     &                  self,
     &                  'gov.cca.ComponentRelease', 
     &                  compRelease,
     &                  exception)
        if (exception .ne. 0) then
           print *, 'pytest.g: 
     &  Error casting self to gov.cca.ComponentRelease'
           stop
C FIXME exceptions, not stops.
        end if
        call gov_cca_Services_registerForRelease_f(
     &      d_services,
     &      compRelease,
     &      exception)
        if (exception .ne. 0) then
           print *, 'pytest.g: 
     &  Error calling registerForRelease()'
        end if
        return
        end
C       Bocca generated code. bocca.protected.end(pytest.g.boccaSetServices)

C       DO-NOT-DELETE splicer.end(pytest.g.boccaSetServices)
        end


C       
C       Method:  boccaReleaseServices[]
C       

        subroutine pytest_g_boccaReleaseServices_fi(self, services, 
     &     exception)
        implicit none
C        in pytest.g self
        integer*8 self
C        in gov.cca.Services services
        integer*8 services
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(pytest.g.boccaReleaseServices)
C       Bocca generated code. bocca.protected.begin(pytest.g.boccaReleaseServices)

        integer *8  stateArray, knull

        call pytest_g__get_data_f(
     &          self, stateArray)
        if (stateArray .eq. 0) then
C          fail silently, we've failed a lot before this is reached.
           return
        end if
        knull=0
        call sidl_opaque__array_set1_f(stateArray, 0, knull)
        call gov_cca_Services_deleteRef_f(services, exception)

C       Remove pytest.x:MYX provides port
        call gov_cca_Services_removeProvidesPort_f(
     &       services, 
     &       'MYX', 
     &       exception)
        if (exception .ne. 0) then
           print *, 'pytest.g: 
     &  Error in call to removeProvidesPort()'
           stop 
C FIXME exceptions, not stops.
        end if

C       UnRegister pytest.x:YOURX uses port
        call gov_cca_Services_unregisterUsesPort_f(
     &       services,
     &       'YOURX',
     &       exception)
        if (exception .ne. 0) then
           print *, 'pytest.g: 
     &         Error in call to unregisterUsesPort()'
           stop
C FIXME exceptions, not stops.
        end if

        return
C       Bocca generated code. bocca.protected.end(pytest.g.boccaReleaseServices)
C       DO-NOT-DELETE splicer.end(pytest.g.boccaReleaseServices)
        end


C       
C       Method:  checkException[]
C       

        subroutine pytest_g_checkException_fi(self, excpt, msg, fatal, 
     &     exception)
        implicit none
C        in pytest.g self
        integer*8 self
C        inout sidl.BaseInterface excpt
        integer*8 excpt
C        in string msg
        character*(*) msg
C        in bool fatal
        logical fatal
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(pytest.g.checkException)
C       Insert-Code-Here {pytest.g.checkException} (checkException method)
 
C       DO-DELETE-WHEN-IMPLEMENTING exception.begin() 
C 
C This method has not been implemented
C 
        integer*8 throwaway
        call sidl_NotImplementedException__create_f
     $      (exception, throwaway)
        if (exception .ne. 0) then
           call sidl_NotImplementedException_setNote_f(
     $         exception,
     $         'This method has not been implemented',
     $         throwaway)
        endif
        return
C       DO-DELETE-WHEN-IMPLEMENTING exception.end() 
 
C       DO-NOT-DELETE splicer.end(pytest.g.checkException)
        end


C       
C       Method:  boccaForceUsePortInclude[]
C       

        subroutine pytest_g_boccaForceUsePortInclude_fi(self, dummy0, 
     &     exception)
        implicit none
C        in pytest.g self
        integer*8 self
C        in pytest.x dummy0
        integer*8 dummy0
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(pytest.g.boccaForceUsePortInclude) */
C       Bocca generated code. bocca.protected.begin(pytest.g.boccaForceUsePortInclude) */
        return
C       Bocca generated code. bocca.protected.end(pytest.g.boccaForceUsePortInclude) */
C       DO-NOT-DELETE splicer.end(pytest.g.boccaForceUsePortInclude) */
        end


C       
C       Method:  setServices[]
C        Starts up a component presence in the calling framework.
C       @param services the component instance's handle on the framework world.
C       Contracts concerning Svc and setServices:
C       
C       The component interaction with the CCA framework
C       and Ports begins on the call to setServices by the framework.
C       
C       This function is called exactly once for each instance created
C       by the framework.
C       
C       The argument Svc will never be nil/null.
C       
C       Those uses ports which are automatically connected by the framework
C       (so-called service-ports) may be obtained via getPort during
C       setServices.
C       

        subroutine pytest_g_setServices_fi(self, services, exception)
        implicit none
C        in pytest.g self
        integer*8 self
C        in gov.cca.Services services
        integer*8 services
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(pytest.g.setServices)
C       bocca-default-code. User may edit or delete.begin(pytest.g.setServices)

        call pytest_g_boccaSetServices_f(
     & self, services, exception)  
C FIXME need to check and propagate exception here.


C       bocca-default-code. User may edit or delete.end(pytest.g.setServices)
C       DO-NOT-DELETE splicer.end(pytest.g.setServices)
        end


C       
C       Method:  releaseServices[]
C       Shuts down a component presence in the calling framework.
C       @param services the component instance's handle on the framework world.
C       Contracts concerning Svc and setServices:
C       
C       This function is called exactly once for each callback registered
C       through Services.
C       
C       The argument Svc will never be nil/null.
C       The argument Svc will always be the same as that received in
C       setServices.
C       
C       During this call the component should release any interfaces
C       acquired by getPort().
C       
C       During this call the component should reset to nil any stored
C       reference to Svc.
C       
C       After this call, the component instance will be removed from the
C       framework. If the component instance was created by the
C       framework, it will be destroyed, not recycled, The behavior of
C       any port references obtained from this component instance and
C       stored elsewhere becomes undefined.
C       
C       Notes for the component implementor:
C       1) The component writer may perform blocking activities
C       within releaseServices, such as waiting for remote computations
C       to shutdown.
C       2) It is good practice during releaseServices for the component
C       writer to remove or unregister all the ports it defined.
C       

        subroutine pytest_g_releaseServices_fi(self, services, 
     &     exception)
        implicit none
C        in pytest.g self
        integer*8 self
C        in gov.cca.Services services
        integer*8 services
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(pytest.g.releaseServices)


C       bocca-default-code. User may edit or delete.begin(pytest.g.releaseServices)
        call pytest_g_boccaReleaseServices_f(
     & self, services, exception)  
C FIXME need to amend and propagate exceptions here.
C       bocca-default-code. User may edit or delete.end(pytest.g.releaseServices)
    
C       DO-NOT-DELETE splicer.end(pytest.g.releaseServices)
        end


C       DO-NOT-DELETE splicer.begin(_miscellaneous_code_end)
C       Insert-Code-Here {_miscellaneous_code_end} (extra code)
C       DO-NOT-DELETE splicer.end(_miscellaneous_code_end)
