/*
 * File:          ccaffeine_TypeMap_Impl.h
 * Symbol:        ccaffeine.TypeMap-v0.3
 * Symbol Type:   class
 * Babel Version: 1.0.0
 * Description:   Server-side implementation for ccaffeine.TypeMap
 * 
 * WARNING: Automatically generated; only changes within splicers preserved
 * 
 */

#ifndef included_ccaffeine_TypeMap_Impl_h
#define included_ccaffeine_TypeMap_Impl_h

#ifndef included_sidl_header_h
#include "sidl_header.h"
#endif
#ifndef included_ccaffeine_TypeMap_h
#include "ccaffeine_TypeMap.h"
#endif
#ifndef included_gov_cca_TypeMap_h
#include "gov_cca_TypeMap.h"
#endif
#ifndef included_gov_cca_TypeMismatchException_h
#include "gov_cca_TypeMismatchException.h"
#endif
#ifndef included_sidl_BaseClass_h
#include "sidl_BaseClass.h"
#endif
#ifndef included_sidl_BaseInterface_h
#include "sidl_BaseInterface.h"
#endif
#ifndef included_sidl_ClassInfo_h
#include "sidl_ClassInfo.h"
#endif
#ifndef included_sidl_RuntimeException_h
#include "sidl_RuntimeException.h"
#endif

/* DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._includes) */
/* Insert-Code-Here {ccaffeine.TypeMap._includes} (include files) */
/* DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._includes) */

/*
 * Private data for class ccaffeine.TypeMap
 */

struct ccaffeine_TypeMap__data {
  /* DO-NOT-DELETE splicer.begin(ccaffeine.TypeMap._data) */
  /* Insert-Code-Here {ccaffeine.TypeMap._data} (private data members) */
  int ignore; /* dummy to force non-empty struct; remove if you add data */
  /* DO-NOT-DELETE splicer.end(ccaffeine.TypeMap._data) */
};

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Access functions for class private data and built-in methods
 */

extern struct ccaffeine_TypeMap__data*
ccaffeine_TypeMap__get_data(
  ccaffeine_TypeMap);

extern void
ccaffeine_TypeMap__set_data(
  ccaffeine_TypeMap,
  struct ccaffeine_TypeMap__data*);

extern
void
impl_ccaffeine_TypeMap__load(
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap__ctor(
  /* in */ ccaffeine_TypeMap self,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap__ctor2(
  /* in */ ccaffeine_TypeMap self,
  /* in */ void* private_data,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap__dtor(
  /* in */ ccaffeine_TypeMap self,
  /* out */ sidl_BaseInterface *_ex);

/*
 * User-defined object methods
 */

extern struct ccaffeine_TypeMap__object* 
  impl_ccaffeine_TypeMap_fconnect_ccaffeine_TypeMap(const char* url,
  sidl_bool ar, sidl_BaseInterface *_ex);
extern struct ccaffeine_TypeMap__object* 
  impl_ccaffeine_TypeMap_fcast_ccaffeine_TypeMap(void* bi,
  sidl_BaseInterface* _ex);
extern struct gov_cca_TypeMap__object* 
  impl_ccaffeine_TypeMap_fconnect_gov_cca_TypeMap(const char* url, sidl_bool ar,
  sidl_BaseInterface *_ex);
extern struct gov_cca_TypeMap__object* 
  impl_ccaffeine_TypeMap_fcast_gov_cca_TypeMap(void* bi,
  sidl_BaseInterface* _ex);
extern struct gov_cca_TypeMismatchException__object* 
  impl_ccaffeine_TypeMap_fconnect_gov_cca_TypeMismatchException(const char* url,
  sidl_bool ar, sidl_BaseInterface *_ex);
extern struct gov_cca_TypeMismatchException__object* 
  impl_ccaffeine_TypeMap_fcast_gov_cca_TypeMismatchException(void* bi,
  sidl_BaseInterface* _ex);
extern struct sidl_BaseClass__object* 
  impl_ccaffeine_TypeMap_fconnect_sidl_BaseClass(const char* url, sidl_bool ar,
  sidl_BaseInterface *_ex);
extern struct sidl_BaseClass__object* 
  impl_ccaffeine_TypeMap_fcast_sidl_BaseClass(void* bi,
  sidl_BaseInterface* _ex);
extern struct sidl_BaseInterface__object* 
  impl_ccaffeine_TypeMap_fconnect_sidl_BaseInterface(const char* url,
  sidl_bool ar, sidl_BaseInterface *_ex);
extern struct sidl_BaseInterface__object* 
  impl_ccaffeine_TypeMap_fcast_sidl_BaseInterface(void* bi,
  sidl_BaseInterface* _ex);
extern struct sidl_ClassInfo__object* 
  impl_ccaffeine_TypeMap_fconnect_sidl_ClassInfo(const char* url, sidl_bool ar,
  sidl_BaseInterface *_ex);
extern struct sidl_ClassInfo__object* 
  impl_ccaffeine_TypeMap_fcast_sidl_ClassInfo(void* bi,
  sidl_BaseInterface* _ex);
extern struct sidl_RuntimeException__object* 
  impl_ccaffeine_TypeMap_fconnect_sidl_RuntimeException(const char* url,
  sidl_bool ar, sidl_BaseInterface *_ex);
extern struct sidl_RuntimeException__object* 
  impl_ccaffeine_TypeMap_fcast_sidl_RuntimeException(void* bi,
  sidl_BaseInterface* _ex);
extern
void
impl_ccaffeine_TypeMap_initialize(
  /* in */ ccaffeine_TypeMap self,
  /* in */ void* opaque_TypeMap_addr,
  /* out */ sidl_BaseInterface *_ex);

extern
gov_cca_TypeMap
impl_ccaffeine_TypeMap_cloneTypeMap(
  /* in */ ccaffeine_TypeMap self,
  /* out */ sidl_BaseInterface *_ex);

extern
gov_cca_TypeMap
impl_ccaffeine_TypeMap_cloneEmpty(
  /* in */ ccaffeine_TypeMap self,
  /* out */ sidl_BaseInterface *_ex);

extern
int32_t
impl_ccaffeine_TypeMap_getInt(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ int32_t dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
int64_t
impl_ccaffeine_TypeMap_getLong(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ int64_t dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
float
impl_ccaffeine_TypeMap_getFloat(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ float dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
double
impl_ccaffeine_TypeMap_getDouble(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ double dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
struct sidl_fcomplex
impl_ccaffeine_TypeMap_getFcomplex(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ struct sidl_fcomplex dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
struct sidl_dcomplex
impl_ccaffeine_TypeMap_getDcomplex(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ struct sidl_dcomplex dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
char*
impl_ccaffeine_TypeMap_getString(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ const char* dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
sidl_bool
impl_ccaffeine_TypeMap_getBool(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ sidl_bool dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
struct sidl_int__array*
impl_ccaffeine_TypeMap_getIntArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<int> */ struct sidl_int__array* dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
struct sidl_long__array*
impl_ccaffeine_TypeMap_getLongArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<long> */ struct sidl_long__array* dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
struct sidl_float__array*
impl_ccaffeine_TypeMap_getFloatArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<float> */ struct sidl_float__array* dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
struct sidl_double__array*
impl_ccaffeine_TypeMap_getDoubleArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<double> */ struct sidl_double__array* dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
struct sidl_fcomplex__array*
impl_ccaffeine_TypeMap_getFcomplexArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<fcomplex> */ struct sidl_fcomplex__array* dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
struct sidl_dcomplex__array*
impl_ccaffeine_TypeMap_getDcomplexArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<dcomplex> */ struct sidl_dcomplex__array* dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
struct sidl_string__array*
impl_ccaffeine_TypeMap_getStringArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<string> */ struct sidl_string__array* dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
struct sidl_bool__array*
impl_ccaffeine_TypeMap_getBoolArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<bool> */ struct sidl_bool__array* dflt,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putInt(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ int32_t value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putLong(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ int64_t value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putFloat(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ float value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putDouble(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ double value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putFcomplex(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ struct sidl_fcomplex value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putDcomplex(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ struct sidl_dcomplex value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putString(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ const char* value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putBool(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in */ sidl_bool value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putIntArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<int> */ struct sidl_int__array* value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putLongArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<long> */ struct sidl_long__array* value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putFloatArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<float> */ struct sidl_float__array* value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putDoubleArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<double> */ struct sidl_double__array* value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putFcomplexArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<fcomplex> */ struct sidl_fcomplex__array* value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putDcomplexArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<dcomplex> */ struct sidl_dcomplex__array* value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putStringArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<string> */ struct sidl_string__array* value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_putBoolArray(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* in array<bool> */ struct sidl_bool__array* value,
  /* out */ sidl_BaseInterface *_ex);

extern
void
impl_ccaffeine_TypeMap_remove(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* out */ sidl_BaseInterface *_ex);

extern
struct sidl_string__array*
impl_ccaffeine_TypeMap_getAllKeys(
  /* in */ ccaffeine_TypeMap self,
  /* in */ enum gov_cca_Type__enum t,
  /* out */ sidl_BaseInterface *_ex);

extern
sidl_bool
impl_ccaffeine_TypeMap_hasKey(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* out */ sidl_BaseInterface *_ex);

extern
enum gov_cca_Type__enum
impl_ccaffeine_TypeMap_typeOf(
  /* in */ ccaffeine_TypeMap self,
  /* in */ const char* key,
  /* out */ sidl_BaseInterface *_ex);

extern struct ccaffeine_TypeMap__object* 
  impl_ccaffeine_TypeMap_fconnect_ccaffeine_TypeMap(const char* url,
  sidl_bool ar, sidl_BaseInterface *_ex);
extern struct ccaffeine_TypeMap__object* 
  impl_ccaffeine_TypeMap_fcast_ccaffeine_TypeMap(void* bi,
  sidl_BaseInterface* _ex);
extern struct gov_cca_TypeMap__object* 
  impl_ccaffeine_TypeMap_fconnect_gov_cca_TypeMap(const char* url, sidl_bool ar,
  sidl_BaseInterface *_ex);
extern struct gov_cca_TypeMap__object* 
  impl_ccaffeine_TypeMap_fcast_gov_cca_TypeMap(void* bi,
  sidl_BaseInterface* _ex);
extern struct gov_cca_TypeMismatchException__object* 
  impl_ccaffeine_TypeMap_fconnect_gov_cca_TypeMismatchException(const char* url,
  sidl_bool ar, sidl_BaseInterface *_ex);
extern struct gov_cca_TypeMismatchException__object* 
  impl_ccaffeine_TypeMap_fcast_gov_cca_TypeMismatchException(void* bi,
  sidl_BaseInterface* _ex);
extern struct sidl_BaseClass__object* 
  impl_ccaffeine_TypeMap_fconnect_sidl_BaseClass(const char* url, sidl_bool ar,
  sidl_BaseInterface *_ex);
extern struct sidl_BaseClass__object* 
  impl_ccaffeine_TypeMap_fcast_sidl_BaseClass(void* bi,
  sidl_BaseInterface* _ex);
extern struct sidl_BaseInterface__object* 
  impl_ccaffeine_TypeMap_fconnect_sidl_BaseInterface(const char* url,
  sidl_bool ar, sidl_BaseInterface *_ex);
extern struct sidl_BaseInterface__object* 
  impl_ccaffeine_TypeMap_fcast_sidl_BaseInterface(void* bi,
  sidl_BaseInterface* _ex);
extern struct sidl_ClassInfo__object* 
  impl_ccaffeine_TypeMap_fconnect_sidl_ClassInfo(const char* url, sidl_bool ar,
  sidl_BaseInterface *_ex);
extern struct sidl_ClassInfo__object* 
  impl_ccaffeine_TypeMap_fcast_sidl_ClassInfo(void* bi,
  sidl_BaseInterface* _ex);
extern struct sidl_RuntimeException__object* 
  impl_ccaffeine_TypeMap_fconnect_sidl_RuntimeException(const char* url,
  sidl_bool ar, sidl_BaseInterface *_ex);
extern struct sidl_RuntimeException__object* 
  impl_ccaffeine_TypeMap_fcast_sidl_RuntimeException(void* bi,
  sidl_BaseInterface* _ex);
#ifdef __cplusplus
}
#endif
#endif
