// 
// File:          ccaffeine_TypeMap_Impl.cxx
// Symbol:        ccaffeine.TypeMap-v0.3
// Symbol Type:   class
// Babel Version: 1.0.0
// Description:   Server-side implementation for ccaffeine.TypeMap
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 
#include "ccaffeine_TypeMap_Impl.hxx"

// 
// Includes for all method dependencies.
// 
#ifndef included_gov_cca_Type_hxx
#include "gov_cca_Type.hxx"
#endif
#ifndef included_gov_cca_TypeMap_hxx
#include "gov_cca_TypeMap.hxx"
#endif
#ifndef included_gov_cca_TypeMismatchException_hxx
#include "gov_cca_TypeMismatchException.hxx"
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
#ifndef included_sidl_NotImplementedException_hxx
#include "sidl_NotImplementedException.hxx"
#endif
#line 12 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
// DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._includes)
#include <vector>
#include <algorithm>

#include "babel_compat.hh"
#include "ccaffeine_TypeMismatchException.hxx"
#include "dc/babel.new/ccafe-bind/BabelHelper.hh"

template<class InputIterator, class OutputIterator>
OutputIterator copy_key( InputIterator first1, InputIterator last1,
			 OutputIterator first2);

int ccaffeine::TypeMap_impl::genSerial = 0;

#ifdef CCAFE_AUDIT
#define NILWHINE(FNAME) \
	IO_dn2(" " FNAME " called with null ctm. %d ",serial);
#else
#define NILWHINE(FNAME)
#endif


// DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._includes)
#line 61 "server/ccaffeine_TypeMap_Impl.cxx"

// speical constructor, used for data wrapping(required).  Do not put code here unless you really know what you're doing!
ccaffeine::TypeMap_impl::TypeMap_impl() : StubBase(reinterpret_cast< 
  void*>(::ccaffeine::TypeMap::_wrapObj(reinterpret_cast< void*>(this))),
  false) , _wrapped(true){ 
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._ctor2)
  // Insert-Code-Here {ccaffeine.TypeMap._ctor2} (ctor2)
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._ctor2)
}

// user defined constructor
void ccaffeine::TypeMap_impl::_ctor() {
#line 38 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._ctor)
  // add construction details here
#ifdef CCAFE_AUDIT
  serial = nextNum();
  IO_dn2("ccaffeine::TypeMap_impl _ctor %d", serial);
#endif
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._ctor)
#line 82 "server/ccaffeine_TypeMap_Impl.cxx"
}

// user defined destructor
void ccaffeine::TypeMap_impl::_dtor() {
#line 49 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._dtor)
  // add destruction details here
#ifdef CCAFE_AUDIT
  IO_dn2("ccaffeine::TypeMap_impl _dtor %d", serial);
  serial = -serial;
#endif
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._dtor)
#line 95 "server/ccaffeine_TypeMap_Impl.cxx"
}

// static class initializer
void ccaffeine::TypeMap_impl::_load() {
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._load)
  // Insert-Code-Here {ccaffeine.TypeMap._load} (class initialization)
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._load)
}

// user defined static methods: (none)

// user defined non-static methods:
/**
 *  unless this function is properly called,
 * the ccaffeine::TypeMap in question will do
 * nothing but generate exceptions.
 */
void
ccaffeine::TypeMap_impl::initialize_impl (
  /* in */void* opaque_TypeMap_addr ) 
{
#line 71 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.initialize)
#ifdef CCAFE_AUDIT
  IO_dn2("TypeMap_impl init %d", serial);
#endif
  if (opaque_TypeMap_addr == 0) { 
#ifdef CCAFE_AUDIT
  IO_dn2("TypeMap_impl init %d called with null", serial);
#endif
    return;
  }
  ::ccafeopq::TypeMap_shared *otm_addr = 0;
  otm_addr = static_cast< ::ccafeopq::TypeMap_shared * >(opaque_TypeMap_addr);
  ctm = *otm_addr;
  if (!ctm) {
    NILWHINE("initialize")
    return;
  }

  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.initialize)
#line 137 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 *  Create an exact copy of this Map 
 */
::gov::cca::TypeMap
ccaffeine::TypeMap_impl::cloneTypeMap_impl () 

{
#line 100 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.cloneTypeMap)

  // 1. create a second ccafe TypeMap locally and a second babel wrapper locally.
	// If the original wrapper is hollow (huh?) send out
	// a new hollow one.
  ccaffeine::TypeMap m = ccaffeine::TypeMap::_create();

  if ( !ctm  ) {
#ifdef CCAFE_AUDIT
   IO_dn2("cloneTypeMap called on empty wrapper %d",serial);
#endif
  }
  else {
    ::ccafeopq::TypeMap_shared newguts = ctm->cloneData();
    // 2. make the new ccafe thing into  a void *.
    ::ccafeopq::TypeMap_shared * gut_addr = 0;
    void *v = 0;
    gut_addr = &newguts;
    v = static_cast<void *>(gut_addr);
    // 3. init the babel wrapper.
    m.initialize(v);
  }
  return m;


  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.cloneTypeMap)
#line 174 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 *  Create a new Map with no key/value associations. 
 */
::gov::cca::TypeMap
ccaffeine::TypeMap_impl::cloneEmpty_impl () 

{
#line 136 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.cloneEmpty)
  // 1. create a second ccafe TypeMap locally and a second babel wrapper locally.
  ccaffeine::TypeMap m = ccaffeine::TypeMap::_create();
  if (! ctm  ) {
#ifdef CCAFE_AUDIT
   IO_dn2("cloneEmpty called on empty wrapper %d",serial);
#endif //CCAFE_AUDIT
  }
  else {
    ::ccafeopq::TypeMap_shared newguts = ctm->cloneEmpty();
    // 2. make the new ccafe thing into  a void *.
    ::ccafeopq::TypeMap_shared * gut_addr = 0;
    void *v = 0;
    gut_addr = &newguts;
    v = static_cast<void *>(gut_addr);
    // 3. init the babel wrapper.
    m.initialize(v);
  }
  return m;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.cloneEmpty)
#line 205 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getInt[]
 */
int32_t
ccaffeine::TypeMap_impl::getInt_impl (
  /* in */const ::std::string& key,
  /* in */int32_t dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 168 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getInt)
#define EXTRACT(TYPE, FNAME) \
  try { \
	  if (!ctm) { \
		  NILWHINE(FNAME) \
		  return dflt; \
	  } \
	  return ctm->get##TYPE(key, dflt); \
  } \
  catch ( ::ccafeopq::TypeMismatchException &e) \
  { \
    /* convert */ \
    ccaffeine::TypeMismatchException ex = ::ccaffeine::TypeMismatchException::_create(); \
    ex.initializeTypes( BabelHelper::babelType(e.getRequestedType()), \
		   BabelHelper::babelType(e.getActualType())); \
    ex.SIDL_EXCEPTION_setMessage( e.getMessage()); \
    ex.SIDL_EXCEPTION_addToTrace( __FILE__, __LINE__, FNAME); \
    throw ex; \
  } \
  catch ( ::ccafeopq::Exception &e2) \
  { \
    ::ccaffeine::CCAException ex = ::ccaffeine::CCAException::_create(); \
    ex.setCCAExceptionType( \
      BabelHelper::babelExceptionType(e2.getType())); \
    ex.SIDL_EXCEPTION_setMessage( e2.getMessage()); \
    ex.SIDL_EXCEPTION_addToTrace( __FILE__, __LINE__, FNAME); \
    throw ex; \
  } \
  /* not reached */ \
  return dflt 

  EXTRACT(Int, "getInt");

  // return getType( d_key2int, key, gov::cca::Int, dflt );
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getInt)
#line 255 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getLong[]
 */
int64_t
ccaffeine::TypeMap_impl::getLong_impl (
  /* in */const ::std::string& key,
  /* in */int64_t dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 215 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getLong)
  // return getType( d_key2long, key, gov::cca::Long, dflt );
  EXTRACT(Long, "getLong");
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getLong)
#line 274 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getFloat[]
 */
float
ccaffeine::TypeMap_impl::getFloat_impl (
  /* in */const ::std::string& key,
  /* in */float dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 231 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getFloat)
  EXTRACT(Float, "getFloat");
  // return getType( d_key2float, key, gov::cca::Float, dflt );
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getFloat)
#line 293 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getDouble[]
 */
double
ccaffeine::TypeMap_impl::getDouble_impl (
  /* in */const ::std::string& key,
  /* in */double dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 247 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getDouble)
  EXTRACT(Double, "getDouble");
  // return getType( d_key2double, key, gov::cca::Double, dflt );
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getDouble)
#line 312 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getFcomplex[]
 */
::std::complex<float>
ccaffeine::TypeMap_impl::getFcomplex_impl (
  /* in */const ::std::string& key,
  /* in */const ::std::complex<float>& dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 263 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getFcomplex)
  // return getType( d_key2fcomplex, key, gov::cca::Fcomplex, dflt );
  EXTRACT(Fcomplex, "getFcomplex");
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getFcomplex)
#line 331 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getDcomplex[]
 */
::std::complex<double>
ccaffeine::TypeMap_impl::getDcomplex_impl (
  /* in */const ::std::string& key,
  /* in */const ::std::complex<double>& dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 279 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getDcomplex)
  // return getType( d_key2dcomplex, key, gov::cca::Dcomplex, dflt );
  EXTRACT(Dcomplex, "getDcomplex");
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getDcomplex)
#line 350 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getString[]
 */
::std::string
ccaffeine::TypeMap_impl::getString_impl (
  /* in */const ::std::string& key,
  /* in */const ::std::string& dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 295 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getString)
  // return getType( d_key2string, key, gov::cca::String, dflt );
  EXTRACT(String, "getString");
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getString)
#line 369 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getBool[]
 */
bool
ccaffeine::TypeMap_impl::getBool_impl (
  /* in */const ::std::string& key,
  /* in */bool dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 311 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getBool)
  // return getType( d_key2bool, key, gov::cca::Bool, dflt );
  EXTRACT(Bool, "getBool");
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getBool)
#line 388 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getIntArray[]
 */
::sidl::array<int32_t>
ccaffeine::TypeMap_impl::getIntArray_impl (
  /* in */const ::std::string& key,
  /* in array<int> */::sidl::array<int32_t> dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 327 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getIntArray)
  // return getType( d_key2intArray, key, gov::cca::IntArray, dflt );
	

#define EXTRACTARRAY(PRIM, TYPE, FNAME) \
  if (!ctm) { \
	  NILWHINE(FNAME) \
	  return dflt; \
  } \
  ::std::vector< PRIM > vdflt = convertToVector(dflt); \
  try { \
    ::std::vector< PRIM > val = ctm->get##TYPE( key, vdflt ); \
    return convertToSidlArray( val ); \
  } \
  catch ( ::ccafeopq::TypeMismatchException &e) \
  { \
    /* convert */ \
    ccaffeine::TypeMismatchException ex; \
    ex.initializeTypes( BabelHelper::babelType(e.getRequestedType()), \
		   BabelHelper::babelType(e.getActualType())); \
    ex.SIDL_EXCEPTION_setMessage( e.getMessage()); \
    ex.SIDL_EXCEPTION_addToTrace( __FILE__, __LINE__, FNAME); \
    throw ex; \
  } \
  catch ( ::ccafeopq::Exception &e2) \
  { \
    ::ccaffeine::CCAException ex = ::ccaffeine::CCAException::_create(); \
    ex.setCCAExceptionType( \
      BabelHelper::babelExceptionType(e2.getType())); \
    ex.SIDL_EXCEPTION_setMessage( e2.getMessage()); \
    ex.SIDL_EXCEPTION_addToTrace( __FILE__, __LINE__, FNAME); \
    throw ex; \
  } \
  /* not reached */ \
  return dflt
  EXTRACTARRAY(int32_t, IntArray, "getIntArray");

  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getIntArray)
#line 441 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getLongArray[]
 */
::sidl::array<int64_t>
ccaffeine::TypeMap_impl::getLongArray_impl (
  /* in */const ::std::string& key,
  /* in array<long> */::sidl::array<int64_t> dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 377 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getLongArray)
  // return getType( d_key2longArray, key, gov::cca::LongArray, dflt );
  EXTRACTARRAY(SIDL_LONG_ARRAY1_PRIMITIVE, LongArray, "getLongArray"); 
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getLongArray)
#line 460 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getFloatArray[]
 */
::sidl::array<float>
ccaffeine::TypeMap_impl::getFloatArray_impl (
  /* in */const ::std::string& key,
  /* in array<float> */::sidl::array<float> dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 393 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getFloatArray)
  EXTRACTARRAY(float, FloatArray, "getFloatArray");
  // return getType( d_key2floatArray, key, gov::cca::FloatArray, dflt );
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getFloatArray)
#line 479 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getDoubleArray[]
 */
::sidl::array<double>
ccaffeine::TypeMap_impl::getDoubleArray_impl (
  /* in */const ::std::string& key,
  /* in array<double> */::sidl::array<double> dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 409 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getDoubleArray)
  EXTRACTARRAY(double, DoubleArray, "getDoubleArray");
  // return getType( d_key2doubleArray, key, gov::cca::DoubleArray, dflt );
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getDoubleArray)
#line 498 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getFcomplexArray[]
 */
::sidl::array< ::sidl::fcomplex>
ccaffeine::TypeMap_impl::getFcomplexArray_impl (
  /* in */const ::std::string& key,
  /* in array<fcomplex> */::sidl::array< ::sidl::fcomplex> dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 425 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getFcomplexArray)
  // return getType( d_key2fcomplexArray, key, gov::cca::FcomplexArray, dflt );
  EXTRACTARRAY( sidl::fcomplex, FcomplexArray, "getFcomplexArray");
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getFcomplexArray)
#line 517 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getDcomplexArray[]
 */
::sidl::array< ::sidl::dcomplex>
ccaffeine::TypeMap_impl::getDcomplexArray_impl (
  /* in */const ::std::string& key,
  /* in array<dcomplex> */::sidl::array< ::sidl::dcomplex> dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 441 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getDcomplexArray)
  EXTRACTARRAY( sidl::dcomplex, DcomplexArray, "getDcomplexArray");
  // return getType( d_key2dcomplexArray, key, gov::cca::DcomplexArray, dflt );
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getDcomplexArray)
#line 536 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getStringArray[]
 */
::sidl::array< ::std::string>
ccaffeine::TypeMap_impl::getStringArray_impl (
  /* in */const ::std::string& key,
  /* in array<string> */::sidl::array< ::std::string> dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 457 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getStringArray)
  EXTRACTARRAY( ::std::string, StringArray, "getStringArray");
  // return getType( d_key2stringArray, key, gov::cca::StringArray, dflt );
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getStringArray)
#line 555 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  getBoolArray[]
 */
::sidl::array<bool>
ccaffeine::TypeMap_impl::getBoolArray_impl (
  /* in */const ::std::string& key,
  /* in array<bool> */::sidl::array<bool> dflt ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 473 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getBoolArray)
  // return getType( d_key2boolArray, key, gov::cca::BoolArray, dflt );
  EXTRACTARRAY( bool, BoolArray, "getBoolArray");
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getBoolArray)
#line 574 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 *  
 * Assign a key and value. Any value previously assigned
 * to the same key will be overwritten so long as it
 * is of the same type. If types conflict, an exception occurs.
 */
void
ccaffeine::TypeMap_impl::putInt_impl (
  /* in */const ::std::string& key,
  /* in */int32_t value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 491 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putInt)
#define INSERT(TYPE, FNAME) \
  if (!ctm) { \
	  NILWHINE(FNAME) \
	  return; \
  } \
  try { \
    ctm->put##TYPE(key, value); \
  } \
  catch ( ::ccafeopq::TypeMismatchException &e) \
  { \
    /* convert */ \
    ccaffeine::TypeMismatchException ex = ::ccaffeine::TypeMismatchException::_create(); \
    ex.initializeTypes( BabelHelper::babelType(e.getRequestedType()), \
		   BabelHelper::babelType(e.getActualType())); \
    ex.SIDL_EXCEPTION_setMessage( e.getMessage()); \
    ex.SIDL_EXCEPTION_addToTrace( __FILE__, __LINE__, FNAME); \
    throw ex; \
  } \
  catch ( ::ccafeopq::Exception &e2) \
  { \
    ::ccaffeine::CCAException ex = ::ccaffeine::CCAException::_create(); \
    ex.setCCAExceptionType( \
      BabelHelper::babelExceptionType(e2.getType())); \
    ex.SIDL_EXCEPTION_setMessage( e2.getMessage()); \
    ex.SIDL_EXCEPTION_addToTrace( __FILE__, __LINE__, FNAME); \
    throw ex; \
  } \
  return 
  INSERT(Int,"putInt");
  // remove( key );
  // d_key2type[key] = gov::cca::Int;
  // d_key2int[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putInt)
#line 626 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putLong[]
 */
void
ccaffeine::TypeMap_impl::putLong_impl (
  /* in */const ::std::string& key,
  /* in */int64_t value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 537 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putLong)
  INSERT(Long,"putLong");
  // remove( key );
  // d_key2type[key] = gov::cca::Long;
  // d_key2long[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putLong)
#line 647 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putFloat[]
 */
void
ccaffeine::TypeMap_impl::putFloat_impl (
  /* in */const ::std::string& key,
  /* in */float value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 555 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putFloat)
  INSERT(Float,"putFloat");
  // remove( key );
  // d_key2type[key] = gov::cca::Float;
  // d_key2float[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putFloat)
#line 668 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putDouble[]
 */
void
ccaffeine::TypeMap_impl::putDouble_impl (
  /* in */const ::std::string& key,
  /* in */double value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 573 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putDouble)
  INSERT(Double,"putDouble");
  // remove( key );
  // d_key2type[key] = gov::cca::Double;
  // d_key2double[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putDouble)
#line 689 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putFcomplex[]
 */
void
ccaffeine::TypeMap_impl::putFcomplex_impl (
  /* in */const ::std::string& key,
  /* in */const ::std::complex<float>& value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 591 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putFcomplex)
  INSERT(Fcomplex,"putFcomplex");
  // remove( key );
  // d_key2type[key] = gov::cca::Fcomplex;
  // d_key2fcomplex[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putFcomplex)
#line 710 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putDcomplex[]
 */
void
ccaffeine::TypeMap_impl::putDcomplex_impl (
  /* in */const ::std::string& key,
  /* in */const ::std::complex<double>& value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 609 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putDcomplex)
  INSERT(Dcomplex,"putDcomplex");
  // remove( key );
  // d_key2type[key] = gov::cca::Dcomplex;
  // d_key2dcomplex[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putDcomplex)
#line 731 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putString[]
 */
void
ccaffeine::TypeMap_impl::putString_impl (
  /* in */const ::std::string& key,
  /* in */const ::std::string& value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 627 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putString)
  INSERT(String,"putString");
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putString)
#line 749 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putBool[]
 */
void
ccaffeine::TypeMap_impl::putBool_impl (
  /* in */const ::std::string& key,
  /* in */bool value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 642 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putBool)
  INSERT(Bool,"putBool");
  // remove( key );
  // d_key2type[key] = gov::cca::Bool;
  // d_key2bool[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putBool)
#line 770 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putIntArray[]
 */
void
ccaffeine::TypeMap_impl::putIntArray_impl (
  /* in */const ::std::string& key,
  /* in array<int> */::sidl::array<int32_t> value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 660 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putIntArray)
#define INSERTARRAY(PRIM, TYPE, FNAME)  \
  if (!ctm) { \
	  NILWHINE(FNAME) \
	  return; \
  } \
  ::std::vector< PRIM > vdflt = convertToVector(value); \
  try { \
    ctm->put##TYPE( key, vdflt ); \
  } \
  catch ( ::ccafeopq::TypeMismatchException &e) \
  { \
    /* convert */ \
    ccaffeine::TypeMismatchException ex = ::ccaffeine::TypeMismatchException::_create(); \
    ex.initializeTypes( BabelHelper::babelType(e.getRequestedType()), \
		   BabelHelper::babelType(e.getActualType())); \
    ex.SIDL_EXCEPTION_setMessage( e.getMessage()); \
    ex.SIDL_EXCEPTION_addToTrace( __FILE__, __LINE__, FNAME); \
    throw ex; \
  } \
  catch ( ::ccafeopq::Exception &e2) \
  { \
    ::ccaffeine::CCAException ex = ::ccaffeine::CCAException::_create(); \
    ex.setCCAExceptionType( \
      BabelHelper::babelExceptionType(e2.getType())); \
    ex.SIDL_EXCEPTION_setMessage( e2.getMessage()); \
    ex.SIDL_EXCEPTION_addToTrace( __FILE__, __LINE__, FNAME); \
    throw ex; \
  } \
  /* not reached */ \
  return 
  INSERTARRAY(int32_t, IntArray, "putIntArray");
  // remove( key );
  // d_key2type[key] = gov::cca::IntArray;
  // d_key2intArray[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putIntArray)
#line 821 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putLongArray[]
 */
void
ccaffeine::TypeMap_impl::putLongArray_impl (
  /* in */const ::std::string& key,
  /* in array<long> */::sidl::array<int64_t> value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 708 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putLongArray)
  INSERTARRAY(SIDL_LONG_ARRAY1_PRIMITIVE, LongArray, "putLongArray");
  // remove( key );
  // d_key2type[key] = gov::cca::Long;
  // d_key2longArray[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putLongArray)
#line 842 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putFloatArray[]
 */
void
ccaffeine::TypeMap_impl::putFloatArray_impl (
  /* in */const ::std::string& key,
  /* in array<float> */::sidl::array<float> value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 726 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putFloatArray)
  INSERTARRAY(float, FloatArray, "putFloatArray");
  // remove( key );
  // d_key2type[key] = gov::cca::FloatArray;
  // d_key2floatArray[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putFloatArray)
#line 863 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putDoubleArray[]
 */
void
ccaffeine::TypeMap_impl::putDoubleArray_impl (
  /* in */const ::std::string& key,
  /* in array<double> */::sidl::array<double> value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 744 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putDoubleArray)
  INSERTARRAY(double, DoubleArray, "putDoubleArray");
  // remove( key );
  // d_key2type[key] = gov::cca::DoubleArray;
  // d_key2doubleArray[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putDoubleArray)
#line 884 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putFcomplexArray[]
 */
void
ccaffeine::TypeMap_impl::putFcomplexArray_impl (
  /* in */const ::std::string& key,
  /* in array<fcomplex> */::sidl::array< ::sidl::fcomplex> value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 762 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putFcomplexArray)
  INSERTARRAY(sidl::fcomplex, FcomplexArray, "putFcomplexArray");
  // remove( key );
  // d_key2type[key] = gov::cca::FcomplexArray;
  // d_key2fcomplexArray[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putFcomplexArray)
#line 905 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putDcomplexArray[]
 */
void
ccaffeine::TypeMap_impl::putDcomplexArray_impl (
  /* in */const ::std::string& key,
  /* in array<dcomplex> */::sidl::array< ::sidl::dcomplex> value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 780 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putDcomplexArray)
  INSERTARRAY(sidl::dcomplex, DcomplexArray, "putDcomplexArray");
  // remove( key );
  // d_key2type[key] = gov::cca::DcomplexArray;
  // d_key2dcomplexArray[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putDcomplexArray)
#line 926 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putStringArray[]
 */
void
ccaffeine::TypeMap_impl::putStringArray_impl (
  /* in */const ::std::string& key,
  /* in array<string> */::sidl::array< ::std::string> value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 798 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putStringArray)
  INSERTARRAY( ::std::string, StringArray, "putStringArray");
  // remove( key );
  // d_key2type[key] = gov::cca::StringArray;
  // d_key2stringArray[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putStringArray)
#line 947 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 * Method:  putBoolArray[]
 */
void
ccaffeine::TypeMap_impl::putBoolArray_impl (
  /* in */const ::std::string& key,
  /* in array<bool> */::sidl::array<bool> value ) 
// throws:
//     ::gov::cca::TypeMismatchException
//     ::sidl::RuntimeException
{
#line 816 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.putBoolArray)
  INSERTARRAY( bool, BoolArray, "putBoolArray");
  // remove( key );
  // d_key2type[key] = gov::cca::BoolArray;
  // d_key2boolArray[key] = value;
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.putBoolArray)
#line 968 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 *  Make the key and associated value disappear from the object. 
 */
void
ccaffeine::TypeMap_impl::remove_impl (
  /* in */const ::std::string& key ) 
{
#line 832 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.remove)
  if (!ctm) {
    NILWHINE("remove")
    return;
  }
  ctm->remove(key);
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.remove)
#line 986 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 *  
 * Get all the names associated with a particular type
 * without exposing the data implementation details.  The keys
 * will be returned in an arbitrary order. If type specified is
 * NoType (no specification) all keys of all types are returned.
 */
::sidl::array< ::std::string>
ccaffeine::TypeMap_impl::getAllKeys_impl (
  /* in */::gov::cca::Type t ) 
{
#line 852 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.getAllKeys)
  // std::vector<char*> names;
  // You've gotta be kidding...
  // Babel forces me to create arrays of malloc'd strings?
  // god, this begs for a c++ IOR.
  // for (size_t = i; i < len; i++) {
  //    names[i] = strdup(onames[i].c_str());
  // }
  // looks like this was fixed sometime recently.
  size_t len;
  ::std::vector< ::std::string > onames = 
	  ctm->getAllKeys( BabelHelper::opaqueType(t));
  len = onames.size();
  sidl::array<std::string> myarray = sidl::array<std::string>::create1d( onames.size() );
  size_t i=0;
  for( ; i < len ; i++) {
#ifdef HAVE_BABEL_PATCH_0_7_0
    myarray.set( onames[i], i );
#else
    /* 074 and later array api */
    myarray.set( i , onames[i] );
#endif
  }
  return myarray;

  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.getAllKeys)
#line 1027 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 *  Return true if the key exists in this map 
 */
bool
ccaffeine::TypeMap_impl::hasKey_impl (
  /* in */const ::std::string& key ) 
{
#line 888 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.hasKey)
  if (!ctm) {
    NILWHINE("hasKey")
    return false;
  }
  // return ( d_key2type.find(key) != d_key2type.end() );
  return ctm->hasKey(key);
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.hasKey)
#line 1046 "server/ccaffeine_TypeMap_Impl.cxx"
}

/**
 *  Return the type of the value associated with this key 
 */
::gov::cca::Type
ccaffeine::TypeMap_impl::typeOf_impl (
  /* in */const ::std::string& key ) 
{
#line 906 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
  // DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap.typeOf)
  if (!ctm) {
    NILWHINE("typeOf")
    return gov::cca::Type_NoType;
  }
  return BabelHelper::babelType(ctm->typeOf(key));
  // DO-NOT-DELETE splicer.end(ccaffeine.TypeMap.typeOf)
#line 1064 "server/ccaffeine_TypeMap_Impl.cxx"
}


#line 916 "/home/baallan/cca/build/dccafe-b100.0/cxx/dc/babel.new/babel-cca/ccaffeine_TypeMap_Impl.cxx"
// DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._misc)

template <class Scalar > 
sidl::array< Scalar > ccaffeine::TypeMap_impl::convertToSidlArray( ::std::vector< Scalar > & val )
{
  size_t len = val.size(); 
#ifdef CCAFE_AUDIT
  // IO_dn2("ccaffeine::TypeMap_impl::convertToSidlArray input len: %d.", len);
#endif
  sidl::array< Scalar > myarray = sidl::array< Scalar >::create1d( len ); 
  size_t i=0; 
  for( ; i < len ; i++) { 
    /* 074 and later array api */ 
    myarray.set( i , val[i] );
  } 
#ifdef CCAFE_AUDIT
//  int slen = myarray.upper(0) - myarray.lower(0) +1;
//  IO_dn2("ccaffeine::TypeMap_impl::convertToSidlArray output len: %d.", slen);
#endif
  return myarray;
}

template <class Scalar >
::std::vector< Scalar > ccaffeine::TypeMap_impl::convertToVector( sidl::array< Scalar > & val )
{
  int len = (val.upper(0) - val.lower(0)) + 1; 
#ifdef CCAFE_AUDIT
//  IO_dn2("ccaffeine::TypeMap_impl::convertToVector input len: %d.", len);
#endif
  ::std::vector< Scalar > res(len);
  int bottom = val.lower(0);
  for(int i=0; i < len ; i++) { 
    res[i] = ( val.get(bottom + i) );
  }
#ifdef CCAFE_AUDIT
//  IO_dn2("ccaffeine::TypeMap_impl::convertToVector output len: %d.", res.size());
#endif
  return res;
}

::ccaffeine::TypeMap 
ccaffeine::TypeMap_impl::babelWrap( ::ccafeopq::TypeMap_shared ctm_)
{
  if (!ctm_) {
#ifdef CCAFE_AUDIT
  IO_dn1("ccaffeine::TypeMap_impl babelWrap got null ctm_");
#endif
  }
  ::ccafeopq::TypeMap_shared * tm_addr;
  tm_addr = &ctm_;
  void *vp;
  vp = static_cast<void *>(tm_addr);

  ::ccaffeine::TypeMap btm = ::ccaffeine::TypeMap::_create();
  btm.initialize(vp);
  return btm;
}

// DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._misc)
#line 1128 "server/ccaffeine_TypeMap_Impl.cxx"

