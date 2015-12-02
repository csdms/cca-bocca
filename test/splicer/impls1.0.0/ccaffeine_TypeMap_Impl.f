C       
C       File:          ccaffeine_TypeMap_Impl.f
C       Symbol:        ccaffeine.TypeMap-v0.3
C       Symbol Type:   class
C       Babel Version: 1.0.0
C       Description:   Server-side implementation for ccaffeine.TypeMap
C       
C       WARNING: Automatically generated; only changes within splicers preserved
C       
C       


C       
C       Symbol "ccaffeine.TypeMap" (version 0.3)
C       
C        This is a wrapper class. It cannot be successfully
C       constructed directly from component or client code.
C       Only the ccaffeine framework
C       internals know how to initialize this object.
C       Components must use Services.createTypeMap.
C       


C       DO-NOT-DELETE splicer.begin(_miscellaneous_code_start)
C       Insert-Code-Here {_miscellaneous_code_start} (extra code)
C       DO-NOT-DELETE splicer.end(_miscellaneous_code_start)




C       
C       Method:  _ctor[]
C       Class constructor called when the class is created.
C       

        subroutine ccaffeine_TypeMap__ctor_fi(self, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._ctor)
C       Insert-Code-Here {ccaffeine.TypeMap._ctor} (_ctor method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._ctor)
        end


C       
C       Method:  _ctor2[]
C       Special Class constructor called when the user wants to wrap his own private data.
C       

        subroutine ccaffeine_TypeMap__ctor2_fi(self, private_data,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in opaque private_data
        integer*8 private_data
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._ctor2)
C       Insert-Code-Here {ccaffeine.TypeMap._ctor2} (_ctor2 method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._ctor2)
        end


C       
C       Method:  _dtor[]
C       Class destructor called when the class is deleted.
C       

        subroutine ccaffeine_TypeMap__dtor_fi(self, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._dtor)
C       Insert-Code-Here {ccaffeine.TypeMap._dtor} (_dtor method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._dtor)
        end


C       
C       Method:  _load[]
C       Static class initializer called exactly once before any user-defined method is dispatched
C       

        subroutine ccaffeine_TypeMap__load_fi(exception)
        implicit none
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._load)
C       Insert-Code-Here {ccaffeine.TypeMap._load} (_load method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._load)
        end


C       
C       Method:  initialize[]
C        unless this function is properly called,
C       the ccaffeine::TypeMap in question will do
C       nothing but generate exceptions.
C       

        subroutine ccaffeine_TypeMap_initialize_fi(self,
     &     opaque_TypeMap_addr, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in opaque opaque_TypeMap_addr
        integer*8 opaque_TypeMap_addr
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.initialize)
C       Insert-Code-Here {ccaffeine.TypeMap.initialize} (initialize method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.initialize)
        end


C       
C       Method:  cloneTypeMap[]
C        Create an exact copy of this Map 
C       

        subroutine ccaffeine_TypeMap_cloneTypeMap_fi(self, retval,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        out gov.cca.TypeMap retval
        integer*8 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.cloneTypeMap)
C       Insert-Code-Here {ccaffeine.TypeMap.cloneTypeMap} (cloneTypeMap method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.cloneTypeMap)
        end


C       
C       Method:  cloneEmpty[]
C        Create a new Map with no key/value associations. 
C       

        subroutine ccaffeine_TypeMap_cloneEmpty_fi(self, retval,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        out gov.cca.TypeMap retval
        integer*8 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.cloneEmpty)
C       Insert-Code-Here {ccaffeine.TypeMap.cloneEmpty} (cloneEmpty method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.cloneEmpty)
        end


C       
C       Method:  getInt[]
C       

        subroutine ccaffeine_TypeMap_getInt_fi(self, key, dflt, retval,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in int dflt
        integer*4 dflt
C        out int retval
        integer*4 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getInt)
C       Insert-Code-Here {ccaffeine.TypeMap.getInt} (getInt method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getInt)
        end


C       
C       Method:  getLong[]
C       

        subroutine ccaffeine_TypeMap_getLong_fi(self, key, dflt, retval,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in long dflt
        integer*8 dflt
C        out long retval
        integer*8 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getLong)
C       Insert-Code-Here {ccaffeine.TypeMap.getLong} (getLong method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getLong)
        end


C       
C       Method:  getFloat[]
C       

        subroutine ccaffeine_TypeMap_getFloat_fi(self, key, dflt,
     &     retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in float dflt
        real dflt
C        out float retval
        real retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getFloat)
C       Insert-Code-Here {ccaffeine.TypeMap.getFloat} (getFloat method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getFloat)
        end


C       
C       Method:  getDouble[]
C       

        subroutine ccaffeine_TypeMap_getDouble_fi(self, key, dflt,
     &     retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in double dflt
        double precision dflt
C        out double retval
        double precision retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getDouble)
C       Insert-Code-Here {ccaffeine.TypeMap.getDouble} (getDouble method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getDouble)
        end


C       
C       Method:  getFcomplex[]
C       

        subroutine ccaffeine_TypeMap_getFcomplex_fi(self, key, dflt,
     &     retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in fcomplex dflt
        complex dflt
C        out fcomplex retval
        complex retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getFcomplex)
C       Insert-Code-Here {ccaffeine.TypeMap.getFcomplex} (getFcomplex method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getFcomplex)
        end


C       
C       Method:  getDcomplex[]
C       

        subroutine ccaffeine_TypeMap_getDcomplex_fi(self, key, dflt,
     &     retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in dcomplex dflt
        double complex dflt
C        out dcomplex retval
        double complex retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getDcomplex)
C       Insert-Code-Here {ccaffeine.TypeMap.getDcomplex} (getDcomplex method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getDcomplex)
        end


C       
C       Method:  getString[]
C       

        subroutine ccaffeine_TypeMap_getString_fi(self, key, dflt,
     &     retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in string dflt
        character*(*) dflt
C        out string retval
        character*(*) retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getString)
C       Insert-Code-Here {ccaffeine.TypeMap.getString} (getString method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getString)
        end


C       
C       Method:  getBool[]
C       

        subroutine ccaffeine_TypeMap_getBool_fi(self, key, dflt, retval,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in bool dflt
        logical dflt
C        out bool retval
        logical retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getBool)
C       Insert-Code-Here {ccaffeine.TypeMap.getBool} (getBool method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getBool)
        end


C       
C       Method:  getIntArray[]
C       

        subroutine ccaffeine_TypeMap_getIntArray_fi(self, key, dflt,
     &     retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<int> dflt
        integer*8 dflt
C        out array<int> retval
        integer*8 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getIntArray)
C       Insert-Code-Here {ccaffeine.TypeMap.getIntArray} (getIntArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getIntArray)
        end


C       
C       Method:  getLongArray[]
C       

        subroutine ccaffeine_TypeMap_getLongArray_fi(self, key, dflt,
     &     retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<long> dflt
        integer*8 dflt
C        out array<long> retval
        integer*8 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getLongArray)
C       Insert-Code-Here {ccaffeine.TypeMap.getLongArray} (getLongArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getLongArray)
        end


C       
C       Method:  getFloatArray[]
C       

        subroutine ccaffeine_TypeMap_getFloatArray_fi(self, key, dflt,
     &     retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<float> dflt
        integer*8 dflt
C        out array<float> retval
        integer*8 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getFloatArray)
C       Insert-Code-Here {ccaffeine.TypeMap.getFloatArray} (getFloatArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getFloatArray)
        end


C       
C       Method:  getDoubleArray[]
C       

        subroutine ccaffeine_TypeMap_getDoubleArray_fi(self, key, dflt,
     &     retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<double> dflt
        integer*8 dflt
C        out array<double> retval
        integer*8 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getDoubleArray)
C       Insert-Code-Here {ccaffeine.TypeMap.getDoubleArray} (getDoubleArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getDoubleArray)
        end


C       
C       Method:  getFcomplexArray[]
C       

        subroutine ccaffeine_TypeMap_getFcomplexArray_fi(self, key,
     &     dflt, retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<fcomplex> dflt
        integer*8 dflt
C        out array<fcomplex> retval
        integer*8 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getFcomplexArray)
C       Insert-Code-Here {ccaffeine.TypeMap.getFcomplexArray} (getFcomplexArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getFcomplexArray)
        end


C       
C       Method:  getDcomplexArray[]
C       

        subroutine ccaffeine_TypeMap_getDcomplexArray_fi(self, key,
     &     dflt, retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<dcomplex> dflt
        integer*8 dflt
C        out array<dcomplex> retval
        integer*8 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getDcomplexArray)
C       Insert-Code-Here {ccaffeine.TypeMap.getDcomplexArray} (getDcomplexArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getDcomplexArray)
        end


C       
C       Method:  getStringArray[]
C       

        subroutine ccaffeine_TypeMap_getStringArray_fi(self, key, dflt,
     &     retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<string> dflt
        integer*8 dflt
C        out array<string> retval
        integer*8 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getStringArray)
C       Insert-Code-Here {ccaffeine.TypeMap.getStringArray} (getStringArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getStringArray)
        end


C       
C       Method:  getBoolArray[]
C       

        subroutine ccaffeine_TypeMap_getBoolArray_fi(self, key, dflt,
     &     retval, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<bool> dflt
        integer*8 dflt
C        out array<bool> retval
        integer*8 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getBoolArray)
C       Insert-Code-Here {ccaffeine.TypeMap.getBoolArray} (getBoolArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getBoolArray)
        end


C       
C       Method:  putInt[]
C        
C       Assign a key and value. Any value previously assigned
C       to the same key will be overwritten so long as it
C       is of the same type. If types conflict, an exception occurs.
C       

        subroutine ccaffeine_TypeMap_putInt_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in int value
        integer*4 value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putInt)
C       Insert-Code-Here {ccaffeine.TypeMap.putInt} (putInt method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putInt)
        end


C       
C       Method:  putLong[]
C       

        subroutine ccaffeine_TypeMap_putLong_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in long value
        integer*8 value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putLong)
C       Insert-Code-Here {ccaffeine.TypeMap.putLong} (putLong method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putLong)
        end


C       
C       Method:  putFloat[]
C       

        subroutine ccaffeine_TypeMap_putFloat_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in float value
        real value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putFloat)
C       Insert-Code-Here {ccaffeine.TypeMap.putFloat} (putFloat method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putFloat)
        end


C       
C       Method:  putDouble[]
C       

        subroutine ccaffeine_TypeMap_putDouble_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in double value
        double precision value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putDouble)
C       Insert-Code-Here {ccaffeine.TypeMap.putDouble} (putDouble method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putDouble)
        end


C       
C       Method:  putFcomplex[]
C       

        subroutine ccaffeine_TypeMap_putFcomplex_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in fcomplex value
        complex value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putFcomplex)
C       Insert-Code-Here {ccaffeine.TypeMap.putFcomplex} (putFcomplex method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putFcomplex)
        end


C       
C       Method:  putDcomplex[]
C       

        subroutine ccaffeine_TypeMap_putDcomplex_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in dcomplex value
        double complex value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putDcomplex)
C       Insert-Code-Here {ccaffeine.TypeMap.putDcomplex} (putDcomplex method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putDcomplex)
        end


C       
C       Method:  putString[]
C       

        subroutine ccaffeine_TypeMap_putString_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in string value
        character*(*) value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putString)
C       Insert-Code-Here {ccaffeine.TypeMap.putString} (putString method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putString)
        end


C       
C       Method:  putBool[]
C       

        subroutine ccaffeine_TypeMap_putBool_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in bool value
        logical value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putBool)
C       Insert-Code-Here {ccaffeine.TypeMap.putBool} (putBool method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putBool)
        end


C       
C       Method:  putIntArray[]
C       

        subroutine ccaffeine_TypeMap_putIntArray_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<int> value
        integer*8 value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putIntArray)
C       Insert-Code-Here {ccaffeine.TypeMap.putIntArray} (putIntArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putIntArray)
        end


C       
C       Method:  putLongArray[]
C       

        subroutine ccaffeine_TypeMap_putLongArray_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<long> value
        integer*8 value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putLongArray)
C       Insert-Code-Here {ccaffeine.TypeMap.putLongArray} (putLongArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putLongArray)
        end


C       
C       Method:  putFloatArray[]
C       

        subroutine ccaffeine_TypeMap_putFloatArray_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<float> value
        integer*8 value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putFloatArray)
C       Insert-Code-Here {ccaffeine.TypeMap.putFloatArray} (putFloatArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putFloatArray)
        end


C       
C       Method:  putDoubleArray[]
C       

        subroutine ccaffeine_TypeMap_putDoubleArray_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<double> value
        integer*8 value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putDoubleArray)
C       Insert-Code-Here {ccaffeine.TypeMap.putDoubleArray} (putDoubleArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putDoubleArray)
        end


C       
C       Method:  putFcomplexArray[]
C       

        subroutine ccaffeine_TypeMap_putFcomplexArray_fi(self, key,
     &     value, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<fcomplex> value
        integer*8 value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putFcomplexArray)
C       Insert-Code-Here {ccaffeine.TypeMap.putFcomplexArray} (putFcomplexArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putFcomplexArray)
        end


C       
C       Method:  putDcomplexArray[]
C       

        subroutine ccaffeine_TypeMap_putDcomplexArray_fi(self, key,
     &     value, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<dcomplex> value
        integer*8 value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putDcomplexArray)
C       Insert-Code-Here {ccaffeine.TypeMap.putDcomplexArray} (putDcomplexArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putDcomplexArray)
        end


C       
C       Method:  putStringArray[]
C       

        subroutine ccaffeine_TypeMap_putStringArray_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<string> value
        integer*8 value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putStringArray)
C       Insert-Code-Here {ccaffeine.TypeMap.putStringArray} (putStringArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putStringArray)
        end


C       
C       Method:  putBoolArray[]
C       

        subroutine ccaffeine_TypeMap_putBoolArray_fi(self, key, value,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        in array<bool> value
        integer*8 value
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putBoolArray)
C       Insert-Code-Here {ccaffeine.TypeMap.putBoolArray} (putBoolArray method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putBoolArray)
        end


C       
C       Method:  remove[]
C        Make the key and associated value disappear from the object. 
C       

        subroutine ccaffeine_TypeMap_remove_fi(self, key, exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.remove)
C       Insert-Code-Here {ccaffeine.TypeMap.remove} (remove method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.remove)
        end


C       
C       Method:  getAllKeys[]
C        
C       Get all the names associated with a particular type
C       without exposing the data implementation details.  The keys
C       will be returned in an arbitrary order. If type specified is
C       NoType (no specification) all keys of all types are returned.
C       

        subroutine ccaffeine_TypeMap_getAllKeys_fi(self, t, retval,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in gov.cca.Type t
        integer*4 t
C        out array<string> retval
        integer*8 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getAllKeys)
C       Insert-Code-Here {ccaffeine.TypeMap.getAllKeys} (getAllKeys method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getAllKeys)
        end


C       
C       Method:  hasKey[]
C        Return true if the key exists in this map 
C       

        subroutine ccaffeine_TypeMap_hasKey_fi(self, key, retval,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        out bool retval
        logical retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.hasKey)
C       Insert-Code-Here {ccaffeine.TypeMap.hasKey} (hasKey method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.hasKey)
        end


C       
C       Method:  typeOf[]
C        Return the type of the value associated with this key 
C       

        subroutine ccaffeine_TypeMap_typeOf_fi(self, key, retval,
     &     exception)
        implicit none
C        in ccaffeine.TypeMap self
        integer*8 self
C        in string key
        character*(*) key
C        out gov.cca.Type retval
        integer*4 retval
C        out sidl.BaseInterface exception
        integer*8 exception

C       DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.typeOf)
C       Insert-Code-Here {ccaffeine.TypeMap.typeOf} (typeOf method)
C       
C       This method has not been implemented
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
C       DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.typeOf)
        end


C       DO-NOT-DELETE splicer.begin(_miscellaneous_code_end)
C       Insert-Code-Here {_miscellaneous_code_end} (extra code)
C       DO-NOT-DELETE splicer.end(_miscellaneous_code_end)
