// 
// File:          ccaffeine_TypeMap_Impl.hxx
// Symbol:        ccaffeine.TypeMap-v0.3
// Symbol Type:   class
// Babel Version: 1.0.0
// Description:   Server-side implementation for ccaffeine.TypeMap
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 

#ifndef included_ccaffeine_TypeMap_Impl_hxx
#define included_ccaffeine_TypeMap_Impl_hxx

#ifndef included_sidl_cxx_hxx
#include "sidl_cxx.hxx"
#endif
#ifndef included_ccaffeine_TypeMap_IOR_h
#include "ccaffeine_TypeMap_IOR.h"
#endif
#ifndef included_ccaffeine_TypeMap_hxx
#include "ccaffeine_TypeMap.hxx"
#endif
#ifndef included_gov_cca_Type_hxx
#include "gov_cca_Type.hxx"
#endif
#ifndef included_gov_cca_TypeMap_hxx
#include "gov_cca_TypeMap.hxx"
#endif
#ifndef included_gov_cca_TypeMismatchException_hxx
#include "gov_cca_TypeMismatchException.hxx"
#endif
#ifndef included_sidl_BaseClass_hxx
#include "sidl_BaseClass.hxx"
#endif
#ifndef included_sidl_BaseInterface_hxx
#include "sidl_BaseInterface.hxx"
#endif
#ifndef included_sidl_ClassInfo_hxx
#include "sidl_ClassInfo.hxx"
#endif
#ifndef included_sidl_RuntimeException_hxx
#include "sidl_RuntimeException.hxx"
#endif


#line 43 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.hxx"
// DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._includes)
// #include <map>
// #include <utility> // need pair<T,U>
#include "dc/export/AllExport.hh"
#include "ccaffeine_CCAException.hxx"
/*
 * The implementation here is now that of the pure c++ version
 * done by ben allan, wrapped in babel.
 * It doesn't make evil assumptions about underlying
 * implementations of the sort that require reinterpret cast.
 * 
 */
// DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._includes)
#line 61 "server/ccaffeine_TypeMap_Impl.hxx"

namespace ccaffeine { 

  /**
   * Symbol "ccaffeine.TypeMap" (version 0.3)
   * 
   *  This is a wrapper class. It cannot be successfully
   * constructed directly from component or client code.
   * Only the ccaffeine framework
   * internals know how to initialize this object.
   * Components must use Services.createTypeMap.
   */
  class TypeMap_impl : public virtual ::ccaffeine::TypeMap 
#line 69 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.hxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._inherits)
  // Put additional inheritance here...
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._inherits)
#line 79 "server/ccaffeine_TypeMap_Impl.hxx"
  {

  // All data marked protected will be accessable by 
  // descendant Impl classes
  protected:

    bool _wrapped;

#line 79 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.hxx"
    // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._implementation)
    ::ccafeopq::TypeMap_shared ctm;

    template <class Scalar > sidl::array< Scalar > 
      convertToSidlArray( ::std::vector< Scalar > & val );

    template <class Scalar > ::std::vector< Scalar > 
      convertToVector( sidl::array< Scalar > & val );

    int serial;
    static int nextNum() { genSerial++; return genSerial; }
    static int genSerial;

  public:

    static ::ccaffeine::TypeMap babelWrap( ::ccafeopq::TypeMap_shared ctm_);
    
    // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._implementation)
#line 107 "server/ccaffeine_TypeMap_Impl.hxx"

  public:
    // default constructor, used for data wrapping(required)
    TypeMap_impl();
    // sidl constructor (required)
    // Note: alternate Skel constructor doesn't call addref()
    // (fixes bug #275)
    TypeMap_impl( struct ccaffeine_TypeMap__object * s ) : StubBase(s,true),
      _wrapped(false) { _ctor(); }

    // user defined construction
    void _ctor();

    // virtual destructor (required)
    virtual ~TypeMap_impl() { _dtor(); }

    // user defined destruction
    void _dtor();

    // true if this object was created by a user newing the impl
    inline bool _isWrapped() {return _wrapped;}

    // static class initializer
    static void _load();

  public:


    /**
     *  unless this function is properly called,
     * the ccaffeine::TypeMap in question will do
     * nothing but generate exceptions.
     */
    void
    initialize_impl (
      /* in */void* opaque_TypeMap_addr
    )
    ;


    /**
     *  Create an exact copy of this Map 
     */
    ::gov::cca::TypeMap
    cloneTypeMap_impl() ;

    /**
     *  Create a new Map with no key/value associations. 
     */
    ::gov::cca::TypeMap
    cloneEmpty_impl() ;
    /**
     * user defined non-static method.
     */
    int32_t
    getInt_impl (
      /* in */const ::std::string& key,
      /* in */int32_t dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    int64_t
    getLong_impl (
      /* in */const ::std::string& key,
      /* in */int64_t dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    float
    getFloat_impl (
      /* in */const ::std::string& key,
      /* in */float dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    double
    getDouble_impl (
      /* in */const ::std::string& key,
      /* in */double dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    ::std::complex<float>
    getFcomplex_impl (
      /* in */const ::std::string& key,
      /* in */const ::std::complex<float>& dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    ::std::complex<double>
    getDcomplex_impl (
      /* in */const ::std::string& key,
      /* in */const ::std::complex<double>& dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    ::std::string
    getString_impl (
      /* in */const ::std::string& key,
      /* in */const ::std::string& dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    bool
    getBool_impl (
      /* in */const ::std::string& key,
      /* in */bool dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    ::sidl::array<int32_t>
    getIntArray_impl (
      /* in */const ::std::string& key,
      /* in array<int> */::sidl::array<int32_t> dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    ::sidl::array<int64_t>
    getLongArray_impl (
      /* in */const ::std::string& key,
      /* in array<long> */::sidl::array<int64_t> dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    ::sidl::array<float>
    getFloatArray_impl (
      /* in */const ::std::string& key,
      /* in array<float> */::sidl::array<float> dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    ::sidl::array<double>
    getDoubleArray_impl (
      /* in */const ::std::string& key,
      /* in array<double> */::sidl::array<double> dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    ::sidl::array< ::sidl::fcomplex>
    getFcomplexArray_impl (
      /* in */const ::std::string& key,
      /* in array<fcomplex> */::sidl::array< ::sidl::fcomplex> dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    ::sidl::array< ::sidl::dcomplex>
    getDcomplexArray_impl (
      /* in */const ::std::string& key,
      /* in array<dcomplex> */::sidl::array< ::sidl::dcomplex> dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    ::sidl::array< ::std::string>
    getStringArray_impl (
      /* in */const ::std::string& key,
      /* in array<string> */::sidl::array< ::std::string> dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    ::sidl::array<bool>
    getBoolArray_impl (
      /* in */const ::std::string& key,
      /* in array<bool> */::sidl::array<bool> dflt
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;


    /**
     *  
     * Assign a key and value. Any value previously assigned
     * to the same key will be overwritten so long as it
     * is of the same type. If types conflict, an exception occurs.
     */
    void
    putInt_impl (
      /* in */const ::std::string& key,
      /* in */int32_t value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putLong_impl (
      /* in */const ::std::string& key,
      /* in */int64_t value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putFloat_impl (
      /* in */const ::std::string& key,
      /* in */float value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putDouble_impl (
      /* in */const ::std::string& key,
      /* in */double value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putFcomplex_impl (
      /* in */const ::std::string& key,
      /* in */const ::std::complex<float>& value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putDcomplex_impl (
      /* in */const ::std::string& key,
      /* in */const ::std::complex<double>& value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putString_impl (
      /* in */const ::std::string& key,
      /* in */const ::std::string& value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putBool_impl (
      /* in */const ::std::string& key,
      /* in */bool value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putIntArray_impl (
      /* in */const ::std::string& key,
      /* in array<int> */::sidl::array<int32_t> value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putLongArray_impl (
      /* in */const ::std::string& key,
      /* in array<long> */::sidl::array<int64_t> value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putFloatArray_impl (
      /* in */const ::std::string& key,
      /* in array<float> */::sidl::array<float> value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putDoubleArray_impl (
      /* in */const ::std::string& key,
      /* in array<double> */::sidl::array<double> value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putFcomplexArray_impl (
      /* in */const ::std::string& key,
      /* in array<fcomplex> */::sidl::array< ::sidl::fcomplex> value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putDcomplexArray_impl (
      /* in */const ::std::string& key,
      /* in array<dcomplex> */::sidl::array< ::sidl::dcomplex> value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putStringArray_impl (
      /* in */const ::std::string& key,
      /* in array<string> */::sidl::array< ::std::string> value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;

    /**
     * user defined non-static method.
     */
    void
    putBoolArray_impl (
      /* in */const ::std::string& key,
      /* in array<bool> */::sidl::array<bool> value
    )
    // throws:
    //     ::gov::cca::TypeMismatchException
    //     ::sidl::RuntimeException
    ;


    /**
     *  Make the key and associated value disappear from the object. 
     */
    void
    remove_impl (
      /* in */const ::std::string& key
    )
    ;


    /**
     *  
     * Get all the names associated with a particular type
     * without exposing the data implementation details.  The keys
     * will be returned in an arbitrary order. If type specified is
     * NoType (no specification) all keys of all types are returned.
     */
    ::sidl::array< ::std::string>
    getAllKeys_impl (
      /* in */::gov::cca::Type t
    )
    ;


    /**
     *  Return true if the key exists in this map 
     */
    bool
    hasKey_impl (
      /* in */const ::std::string& key
    )
    ;


    /**
     *  Return the type of the value associated with this key 
     */
    ::gov::cca::Type
    typeOf_impl (
      /* in */const ::std::string& key
    )
    ;

  };  // end class TypeMap_impl

} // end namespace ccaffeine

#line 585 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.hxx"
// DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._misc)
// Put miscellaneous things here...
// DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._misc)
#line 631 "server/ccaffeine_TypeMap_Impl.hxx"

#endif
