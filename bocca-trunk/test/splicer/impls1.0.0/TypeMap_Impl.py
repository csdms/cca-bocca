#
# File:          TypeMap_Impl.py
# Symbol:        ccaffeine.TypeMap-v0.3
# Symbol Type:   class
# Babel Version: 1.0.0
# Description:   Implementation of sidl class ccaffeine.TypeMap in Python.
# 
# WARNING: Automatically generated; changes will be lost
# 
#


""" This is a wrapper class. It cannot be successfully
constructed directly from component or client code.
Only the ccaffeine framework
internals know how to initialize this object.
Components must use Services.createTypeMap.
"""

# DO-NOT-DELETE splicer.begin(_initial)
# Insert-Code-Here {_initial} ()
# DO-NOT-DELETE splicer.end(_initial)

import ccaffeine.TypeMap
import gov.cca.Type
import gov.cca.TypeMap
import gov.cca.TypeMismatchException
import sidl.BaseClass
import sidl.BaseInterface
import sidl.ClassInfo
import sidl.RuntimeException
import sidl.NotImplementedException

# DO-NOT-DELETE splicer.begin(_before_type)
# Insert-Code-Here {_before_type} ()
# DO-NOT-DELETE splicer.end(_before_type)

class TypeMap:
  """\
 This is a wrapper class. It cannot be successfully
constructed directly from component or client code.
Only the ccaffeine framework
internals know how to initialize this object.
Components must use Services.createTypeMap.
"""

# All calls to sidl methods should use __IORself

# Normal Babel creation pases in an IORself. If IORself == None
# that means this Impl class is being constructed for native delegation
  def __init__(self, IORself = None):
    if (IORself == None):
      self.__IORself = ccaffeine.TypeMap.TypeMap(impl = self)
    else:
      self.__IORself = IORself
# DO-NOT-DELETE splicer.begin(__init__)
# Insert-Code-Here {__init__} ()
# DO-NOT-DELETE splicer.end(__init__)

# Returns the IORself (client stub) of the Impl, mainly for use
# with native delegation
  def _getStub(self):
    return self.__IORself

  def initialize(self, opaque_TypeMap_addr):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # opaque opaque_TypeMap_addr
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

    """\
 unless this function is properly called,
the ccaffeine::TypeMap in question will do
nothing but generate exceptions.
"""
# DO-NOT-DELETE splicer.begin(initialize)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(initialize)

  def cloneTypeMap(self):
    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # gov.cca.TypeMap _return
    #

    """\
 Create an exact copy of this Map 
"""
# DO-NOT-DELETE splicer.begin(cloneTypeMap)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(cloneTypeMap)

  def cloneEmpty(self):
    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # gov.cca.TypeMap _return
    #

    """\
 Create a new Map with no key/value associations. 
"""
# DO-NOT-DELETE splicer.begin(cloneEmpty)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(cloneEmpty)

  def getInt(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # int dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # int _return
    #

# DO-NOT-DELETE splicer.begin(getInt)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getInt)

  def getLong(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # long dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # long _return
    #

# DO-NOT-DELETE splicer.begin(getLong)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getLong)

  def getFloat(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # float dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # float _return
    #

# DO-NOT-DELETE splicer.begin(getFloat)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getFloat)

  def getDouble(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # double dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # double _return
    #

# DO-NOT-DELETE splicer.begin(getDouble)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getDouble)

  def getFcomplex(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # fcomplex dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # fcomplex _return
    #

# DO-NOT-DELETE splicer.begin(getFcomplex)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getFcomplex)

  def getDcomplex(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # dcomplex dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # dcomplex _return
    #

# DO-NOT-DELETE splicer.begin(getDcomplex)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getDcomplex)

  def getString(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # string dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # string _return
    #

# DO-NOT-DELETE splicer.begin(getString)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getString)

  def getBool(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # bool dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # bool _return
    #

# DO-NOT-DELETE splicer.begin(getBool)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getBool)

  def getIntArray(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<int> dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # array<int> _return
    #

# DO-NOT-DELETE splicer.begin(getIntArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getIntArray)

  def getLongArray(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<long> dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # array<long> _return
    #

# DO-NOT-DELETE splicer.begin(getLongArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getLongArray)

  def getFloatArray(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<float> dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # array<float> _return
    #

# DO-NOT-DELETE splicer.begin(getFloatArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getFloatArray)

  def getDoubleArray(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<double> dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # array<double> _return
    #

# DO-NOT-DELETE splicer.begin(getDoubleArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getDoubleArray)

  def getFcomplexArray(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<fcomplex> dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # array<fcomplex> _return
    #

# DO-NOT-DELETE splicer.begin(getFcomplexArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getFcomplexArray)

  def getDcomplexArray(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<dcomplex> dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # array<dcomplex> _return
    #

# DO-NOT-DELETE splicer.begin(getDcomplexArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getDcomplexArray)

  def getStringArray(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<string> dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # array<string> _return
    #

# DO-NOT-DELETE splicer.begin(getStringArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getStringArray)

  def getBoolArray(self, key, dflt):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<bool> dflt
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # array<bool> _return
    #

# DO-NOT-DELETE splicer.begin(getBoolArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getBoolArray)

  def putInt(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # int value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

    """\
 
Assign a key and value. Any value previously assigned
to the same key will be overwritten so long as it
is of the same type. If types conflict, an exception occurs.
"""
# DO-NOT-DELETE splicer.begin(putInt)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putInt)

  def putLong(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # long value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putLong)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putLong)

  def putFloat(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # float value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putFloat)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putFloat)

  def putDouble(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # double value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putDouble)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putDouble)

  def putFcomplex(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # fcomplex value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putFcomplex)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putFcomplex)

  def putDcomplex(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # dcomplex value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putDcomplex)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putDcomplex)

  def putString(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # string value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putString)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putString)

  def putBool(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # bool value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putBool)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putBool)

  def putIntArray(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<int> value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putIntArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putIntArray)

  def putLongArray(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<long> value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putLongArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putLongArray)

  def putFloatArray(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<float> value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putFloatArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putFloatArray)

  def putDoubleArray(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<double> value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putDoubleArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putDoubleArray)

  def putFcomplexArray(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<fcomplex> value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putFcomplexArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putFcomplexArray)

  def putDcomplexArray(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<dcomplex> value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putDcomplexArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putDcomplexArray)

  def putStringArray(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<string> value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putStringArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putStringArray)

  def putBoolArray(self, key, value):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    # array<bool> value
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

# DO-NOT-DELETE splicer.begin(putBoolArray)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(putBoolArray)

  def remove(self, key):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
# None
    #

    """\
 Make the key and associated value disappear from the object. 
"""
# DO-NOT-DELETE splicer.begin(remove)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(remove)

  def getAllKeys(self, t):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # gov.cca.Type t
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # array<string> _return
    #

    """\
 
Get all the names associated with a particular type
without exposing the data implementation details.  The keys
will be returned in an arbitrary order. If type specified is
NoType (no specification) all keys of all types are returned.
"""
# DO-NOT-DELETE splicer.begin(getAllKeys)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(getAllKeys)

  def hasKey(self, key):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # bool _return
    #

    """\
 Return true if the key exists in this map 
"""
# DO-NOT-DELETE splicer.begin(hasKey)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(hasKey)

  def typeOf(self, key):
    #
    # sidl EXPECTED INCOMING TYPES
    # ============================
    # string key
    #

    #
    # sidl EXPECTED RETURN VALUE(s)
    # =============================
    # gov.cca.Type _return
    #

    """\
 Return the type of the value associated with this key 
"""
# DO-NOT-DELETE splicer.begin(typeOf)
    #
    # This method has not been implemented
    #

    noImpl = sidl.NotImplementedException.NotImplementedException()
    noImpl.setNote("This method has not been implmented.")
    raise  sidl.NotImplementedException._Exception, noImpl
# DO-NOT-DELETE splicer.end(typeOf)

# DO-NOT-DELETE splicer.begin(_final)
# Insert-Code-Here {_final} ()
# DO-NOT-DELETE splicer.end(_final)
