// 
// File:          ccafe1_StarterComponent_Impl.cc
// Symbol:        ccafe1.StarterComponent-v0.1
// Symbol Type:   class
// Description:   Server-side implementation for ccafe1.StarterComponent
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 
#include "ccafe1_StarterComponent_Impl.hh"

// DO-NOT-DELETE splicer.begin(ccafe1.StarterComponent._includes)
// Put additional includes or other arbitrary code here...
// DO-NOT-DELETE splicer.end(ccafe1.StarterComponent._includes)

// user defined constructor
void ccafe1::StarterComponent_impl::_ctor() {
  // DO-NOT-DELETE splicer.begin(ccafe1.StarterComponent._ctor)
  // add construction details here
  // DO-NOT-DELETE splicer.end(ccafe1.StarterComponent._ctor)
}

// user defined destructor
void ccafe1::StarterComponent_impl::_dtor() {
  // DO-NOT-DELETE splicer.begin(ccafe1.StarterComponent._dtor)
  // add destruction details here
  // DO-NOT-DELETE splicer.end(ccafe1.StarterComponent._dtor)
}

// user defined static methods: (none)

// user defined non-static methods:
/**
 * Execute some encapsulated functionality on the component. 
 * Return 0 if ok, -1 if internal error but component may be 
 * used further, and -2 if error so severe that component cannot
 * be further used safely.
 */
int32_t
ccafe1::StarterComponent_impl::go () 
throw () 

{
  // DO-NOT-DELETE splicer.begin(ccafe1.StarterComponent.go)

  gov::cca::Port outPrt = svc.getPort("output");
  // = operator does a cast ...
  if(outPrt._not_nil()) {
    ccafe3::StringConsumerPort sc = ::babel_cast< ccafe3::StringConsumerPort >(outPrt);
    sc.setString("Hello World");
    svc.releasePort("output");
  }
  return 0;
  // DO-NOT-DELETE splicer.end(ccafe1.StarterComponent.go)
}

/**
 * Obtain Services handle, through which the 
 * component communicates with the framework. 
 * This is the one method that every CCA Component
 * must implement. The component will be called
 * with a nil/null Services pointer when it is
 * to shut itself down.
 */
void
ccafe1::StarterComponent_impl::setServices (
  /*in*/ ::gov::cca::Services services ) 
throw () 
{
  // DO-NOT-DELETE splicer.begin(ccafe1.StarterComponent.setServices)
	// we can either insert the boilerplate here or #include it.
	// to stomp always on user mods, we keep the same splice key as babel.
  // DO-NOT-DELETE splicer.end(ccafe1.StarterComponent.setServices)
}


// DO-NOT-DELETE splicer.begin(ccafe1.StarterComponent._misc)
// Put miscellaneous code here
// DO-NOT-DELETE splicer.end(ccafe1.StarterComponent._misc)

