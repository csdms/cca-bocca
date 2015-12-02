// 
// File:          pp_testX_Impl.cxx
// Symbol:        pp.testX-v0.0
// Symbol Type:   class
// Babel Version: 1.0.6
// Description:   Server-side implementation for pp.testX
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 
#include "pp_testX_Impl.hxx"

// 
// Includes for all method dependencies.
// 
#ifndef included_gov_cca_CCAException_hxx
#include "gov_cca_CCAException.hxx"
#endif
#ifndef included_gov_cca_Services_hxx
#include "gov_cca_Services.hxx"
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
  // DO-NOT-DELETE splicer.begin(pp.testX._includes)

  // Insert-UserCode-Here {pp.testX._includes:prolog} (additional includes or code)

  // Bocca generated code. bocca.protected.begin(pp.testX._includes)

#define _BOCCA_CTOR_MESSAGES 0
  // If -D_BOCCA_STDERR is given to the compiler, diagnostics print to stderr.
  // In production use, probably want not to use -D_BOCCA_STDERR.
#ifdef _BOCCA_STDERR

#include <iostream>

#ifdef _BOCCA_CTOR_PRINT
#undef _BOCCA_CTOR_MESSAGES
#define _BOCCA_CTOR_MESSAGES 1
#endif // _BOCCA_CTOR_PRINT 
#else  // _BOCCA_STDERR


#endif // _BOCCA_STDERR



  // If -D_BOCCA_BOOST is given to the compiler, exceptions and diagnostics will
  // include function names for boost-understood compilers.
  // If boost is not available (and therefore ccaffeine is not in use), 
  // -D_BOCCA_BOOST can be omitted and function names will not be included in messages.
#ifndef _BOCCA_BOOST
#define BOOST_CURRENT_FUNCTION ""
#else
#include <boost/current_function.hpp>
#endif

  // This is intended to simplify exception throwing as SIDL_THROW does for C.
#define BOCCA_THROW_CXX(EX_CLS, MSG) \
{ \
    EX_CLS ex = EX_CLS::_create(); \
    ex.setNote( MSG ); \
    ex.add(__FILE__, __LINE__, BOOST_CURRENT_FUNCTION); \
    throw ex; \
}

  // This simplifies exception extending and rethrowing in c++, like SIDL_CHECK in C.
  // EX_OBJ must be the caught exception and is extended with msg and file/line/func added.
  // Continuing the throw is up to the user.
#define BOCCA_EXTEND_THROW_CXX(EX_OBJ, MSG, LINEOFFSET) \
{ \
  std::string msg = std::string(MSG) + std::string(BOOST_CURRENT_FUNCTION); \
  EX_OBJ.add(__FILE__,__LINE__ + LINEOFFSET, msg); \
}


  // Bocca generated code. bocca.protected.end(pp.testX._includes)

  // Insert-UserCode-Here {pp.testX._includes:epilog} (additional includes or code)


#include <iostream>

  // DO-NOT-DELETE splicer.end(pp.testX._includes)

// speical constructor, used for data wrapping(required).  Do not put code here unless you really know what you're doing!
pp::testX_impl::testX_impl() : StubBase(reinterpret_cast< void*>(
  ::pp::testX::_wrapObj(reinterpret_cast< void*>(this))),false) , _wrapped(
  true){ 
  // DO-NOT-DELETE splicer.begin(pp.testX._ctor2)
  // Insert-Code-Here {pp.testX._ctor2} (ctor2)
  // DO-NOT-DELETE splicer.end(pp.testX._ctor2)
}

// user defined constructor
void pp::testX_impl::_ctor() {
  // DO-NOT-DELETE splicer.begin(pp.testX._ctor)
    
  // Insert-UserCode-Here {pp.testX._ctor:prolog} (constructor method) 

  // bocca-default-code. User may edit or delete.begin(pp.testX._ctor)
   #if _BOCCA_CTOR_MESSAGES

     std::cerr << "CTOR pp.testX: " << BOOST_CURRENT_FUNCTION << " constructing " << this << std::endl;

   #endif // _BOCCA_CTOR_MESSAGES
  // bocca-default-code. User may edit or delete.end(pp.testX._ctor)

  // Insert-UserCode-Here {pp.testX._ctor:epilog} (constructor method)

  
  numtests = 0;

  // DO-NOT-DELETE splicer.end(pp.testX._ctor)
}

// user defined destructor
void pp::testX_impl::_dtor() {
  // DO-NOT-DELETE splicer.begin(pp.testX._dtor)
  // Insert-UserCode-Here {pp.testX._dtor} (destructor method) 
    
  // bocca-default-code. User may edit or delete.begin(pp.testX._dtor) */
   #if _BOCCA_CTOR_MESSAGES

     std::cerr << "DTOR pp.testX: " << BOOST_CURRENT_FUNCTION << " destructing " << this << std::endl;

   #endif // _BOCCA_CTOR_MESSAGES 
  // bocca-default-code. User may edit or delete.end(pp.testX._dtor) 

  
  svc = 0;

  // DO-NOT-DELETE splicer.end(pp.testX._dtor)
}

// static class initializer
void pp::testX_impl::_load() {
  // DO-NOT-DELETE splicer.begin(pp.testX._load)
  // Insert-Code-Here {pp.testX._load} (class initialization)
  // DO-NOT-DELETE splicer.end(pp.testX._load)
}

// user defined static methods: (none)

// user defined non-static methods:
/**
 * Method:  boccaSetServices[]
 */
void
pp::testX_impl::boccaSetServices_impl (
  /* in */::gov::cca::Services services ) 
// throws:
//     ::gov::cca::CCAException
//     ::sidl::RuntimeException
{
  // DO-NOT-DELETE splicer.begin(pp.testX.boccaSetServices)
  // DO-NOT-EDIT-BOCCA
  // Bocca generated code. bocca.protected.begin(pp.testX.boccaSetServices)

  gov::cca::TypeMap typeMap;
  gov::cca::Port    port;

  this->d_services = services;

  typeMap = this->d_services.createTypeMap();

  port = ::babel_cast< gov::cca::Port>(*this);
  if (port._is_nil()) {
    BOCCA_THROW_CXX( ::sidl::SIDLException , "pp.testX: Error casting self to gov::cca::Port");
  } 


  // Provide a gov.cca.ports.GoPort port with port name go 
  try{
    this->d_services.addProvidesPort(port, // implementing object
                                     "go", // port instance name
                                     "gov.cca.ports.GoPort", // full sidl type of port
                                     typeMap); // properties for the port
  } catch ( ::gov::cca::CCAException ex )  {
    BOCCA_EXTEND_THROW_CXX(ex, "pp.testX: Error calling addProvidesPort(port,\"go\", \"gov.cca.ports.GoPort\", typeMap) ", -2);
    throw;
  }    

  // Provide a gov.cca.ports.ParameterGetListener port with port name pgl 
  try{
    this->d_services.addProvidesPort(port, // implementing object
                                     "pgl", // port instance name
                                     "gov.cca.ports.ParameterGetListener", // full sidl type of port
                                     typeMap); // properties for the port
  } catch ( ::gov::cca::CCAException ex )  {
    BOCCA_EXTEND_THROW_CXX(ex, "pp.testX: Error calling addProvidesPort(port,\"pgl\", \"gov.cca.ports.ParameterGetListener\", typeMap) ", -2);
    throw;
  }    

  // Provide a gov.cca.ports.ParameterSetListener port with port name psl 
  try{
    this->d_services.addProvidesPort(port, // implementing object
                                     "psl", // port instance name
                                     "gov.cca.ports.ParameterSetListener", // full sidl type of port
                                     typeMap); // properties for the port
  } catch ( ::gov::cca::CCAException ex )  {
    BOCCA_EXTEND_THROW_CXX(ex, "pp.testX: Error calling addProvidesPort(port,\"psl\", \"gov.cca.ports.ParameterSetListener\", typeMap) ", -2);
    throw;
  }    


  gov::cca::ComponentRelease cr = ::babel_cast< gov::cca::ComponentRelease>(*this);
  this->d_services.registerForRelease(cr);
  return;
  // Bocca generated code. bocca.protected.end(pp.testX.boccaSetServices)
    
  // DO-NOT-DELETE splicer.end(pp.testX.boccaSetServices)
}

/**
 * Method:  boccaReleaseServices[]
 */
void
pp::testX_impl::boccaReleaseServices_impl (
  /* in */::gov::cca::Services services ) 
// throws:
//     ::gov::cca::CCAException
//     ::sidl::RuntimeException
{
  // DO-NOT-DELETE splicer.begin(pp.testX.boccaReleaseServices)
  // DO-NOT-EDIT-BOCCA
  // Bocca generated code. bocca.protected.begin(pp.testX.boccaReleaseServices)
  this->d_services=0;


  // Un-provide gov.cca.ports.GoPort port with port name go 
  try{
    services.removeProvidesPort("go");
  } catch ( ::gov::cca::CCAException ex )  {

#ifdef _BOCCA_STDERR
    std::cerr << "pp.testX: Error calling removeProvidesPort(\"go\") at " 
              << __FILE__ << ": " << __LINE__ -4 << ": " << ex.getNote() << std::endl;
#endif // _BOCCA_STDERR

  }

  // Un-provide gov.cca.ports.ParameterGetListener port with port name pgl 
  try{
    services.removeProvidesPort("pgl");
  } catch ( ::gov::cca::CCAException ex )  {

#ifdef _BOCCA_STDERR
    std::cerr << "pp.testX: Error calling removeProvidesPort(\"pgl\") at " 
              << __FILE__ << ": " << __LINE__ -4 << ": " << ex.getNote() << std::endl;
#endif // _BOCCA_STDERR

  }

  // Un-provide gov.cca.ports.ParameterSetListener port with port name psl 
  try{
    services.removeProvidesPort("psl");
  } catch ( ::gov::cca::CCAException ex )  {

#ifdef _BOCCA_STDERR
    std::cerr << "pp.testX: Error calling removeProvidesPort(\"psl\") at " 
              << __FILE__ << ": " << __LINE__ -4 << ": " << ex.getNote() << std::endl;
#endif // _BOCCA_STDERR

  }

  return;
  // Bocca generated code. bocca.protected.end(pp.testX.boccaReleaseServices)
    
  // DO-NOT-DELETE splicer.end(pp.testX.boccaReleaseServices)
}

/**
 *  This function should never be called, but helps babel generate better code. 
 */
void
pp::testX_impl::boccaForceUsePortInclude_impl () 

{
  // DO-NOT-DELETE splicer.begin(pp.testX.boccaForceUsePortInclude)
  // DO-NOT-EDIT-BOCCA
  // Bocca generated code. bocca.protected.begin(pp.testX.boccaForceUsePortInclude)

  // Bocca generated code. bocca.protected.end(pp.testX.boccaForceUsePortInclude)
  // DO-NOT-DELETE splicer.end(pp.testX.boccaForceUsePortInclude)
}

/**
 *  Starts up a component presence in the calling framework.
 * @param services the component instance's handle on the framework world.
 * Contracts concerning Svc and setServices:
 * 
 * The component interaction with the CCA framework
 * and Ports begins on the call to setServices by the framework.
 * 
 * This function is called exactly once for each instance created
 * by the framework.
 * 
 * The argument Svc will never be nil/null.
 * 
 * Those uses ports which are automatically connected by the framework
 * (so-called service-ports) may be obtained via getPort during
 * setServices.
 */
void
pp::testX_impl::setServices_impl (
  /* in */::gov::cca::Services services ) 
// throws:
//     ::gov::cca::CCAException
//     ::sidl::RuntimeException
{
  // DO-NOT-DELETE splicer.begin(pp.testX.setServices)

  this->d_services = services;

  gov::cca::TypeMap tm = this->d_services.createTypeMap();

  gov::cca::ports::GoPort gp = ::babel_cast< gov::cca::ports::GoPort>(*this);

  this->d_services.addProvidesPort(gp, std::string("go"),
                          std::string("gov.cca.ports.GoPort"), tm);

  this->d_services.registerUsesPort(std::string("ppf"),
                       std::string("gov.cca.ports.ParameterPortFactory"), tm);

  gov::cca::ComponentRelease cr = ::babel_cast< gov::cca::ComponentRelease>(*this);
  this->d_services.registerForRelease(cr);


  // DO-NOT-DELETE splicer.end(pp.testX.setServices)
}

/**
 * Shuts down a component presence in the calling framework.
 * @param services the component instance's handle on the framework world.
 * Contracts concerning Svc and setServices:
 * 
 * This function is called exactly once for each callback registered
 * through Services.
 * 
 * The argument Svc will never be nil/null.
 * The argument Svc will always be the same as that received in
 * setServices.
 * 
 * During this call the component should release any interfaces
 * acquired by getPort().
 * 
 * During this call the component should reset to nil any stored
 * reference to Svc.
 * 
 * After this call, the component instance will be removed from the
 * framework. If the component instance was created by the
 * framework, it will be destroyed, not recycled, The behavior of
 * any port references obtained from this component instance and
 * stored elsewhere becomes undefined.
 * 
 * Notes for the component implementor:
 * 1) The component writer may perform blocking activities
 * within releaseServices, such as waiting for remote computations
 * to shutdown.
 * 2) It is good practice during releaseServices for the component
 * writer to remove or unregister all the ports it defined.
 */
void
pp::testX_impl::releaseServices_impl (
  /* in */::gov::cca::Services services ) 
// throws:
//     ::gov::cca::CCAException
//     ::sidl::RuntimeException
{
  // DO-NOT-DELETE splicer.begin(pp.testX.releaseServices)

  this->d_services.removeProvidesPort(std::string("go"));
  this->d_services.unregisterUsesPort(std::string("ppf"));
  this->d_services = 0;
  // DO-NOT-DELETE splicer.end(pp.testX.releaseServices)
}

/**
 *  
 * Execute some encapsulated functionality on the component. 
 * Return 0 if ok, -1 if internal error but component may be 
 * used further, and -2 if error so severe that component cannot
 * be further used safely.
 */
int32_t
pp::testX_impl::go_impl () 

{
  // DO-NOT-DELETE splicer.begin(pp.testX.go)
  
  gov::cca::Services svc = this->d_services;
  
  if (svc._is_nil()) {
	  std::cerr <<  "ccafe4::ParameterPortFactoryTest_impl::go: called without Services svc set." << std::endl;
	  return 1;
  }
  char buf[40];
  numtests++;
  sprintf(buf,"%d",numtests);

  gov::cca::TypeMap tm = svc.createTypeMap();
  if (tm._is_nil()) {
    std::cerr <<  "ccafe4::ParameterPortFactoryTest_impl::go: svc.createTypeMap failed." << std::endl;
    return -1;
  }

  pplist.push_back(tm);
  std::string pname = "PP_";
  pname += buf;

  ::gov::cca::Port gcp = svc.getPort("ppf");
  ppf = ::babel_cast< gov::cca::ports::ParameterPortFactory >(gcp);
  if (ppf._is_nil()) {
    std::cerr <<  "ccafe4::ParameterPortFactoryTest_impl::go: called without ppf connected." << std::endl;
    return -1;
  }
  std::cout << "BPPFTEST:  got port ppf" << std::endl;
  ppf.initParameterData(tm, pname);
  std::cout << "BPPFTEST:  init'd tm." << std::endl;
  ::std::string title = "Test PPF for port ";
  title += pname;
  ppf.setBatchTitle(tm, title);
  std::cout << "BPPFTEST:  title set." << std::endl;
  ppf.addRequestBoolean(tm,"noName","var to test if default group gets used","anon group",true);

  std::cout << "BPPFTEST:  bool defined." << std::endl;
  ppf.setGroupName(tm,"Named Set1");
  ppf.addRequestInt(tm,"iVar","a ranged test integer","int test", 5, 0 ,10);

  std::cout << "BPPFTEST:  set1.ivar defined." << std::endl;
#define FULLTEST 1
#if FULLTEST
  ppf.addRequestLong(tm,"jVar","a deranged test long","long test", -50, 0 , -100);

  std::cout << "BPPFTEST:  defining set2." << std::endl;
  ppf.setGroupName(tm,"Named Set2");
  ppf.addRequestDouble(tm,"dVar","a ranged test double","double test", -50, 0 , -100);
  ppf.addRequestFloat(tm,"fVar","a ranged test float","float test", 50, -1000 , 1000);

  std::cout << "BPPFTEST:  defining set3." << std::endl;
  ppf.setGroupName(tm,"Named Set3");
  
  ppf.addRequestString(tm,"sVar","a free test string","string any test", "some value");

  ppf.addRequestString(tm,"sList","a choice test string","string list test", "some value");
  ppf.addRequestStringChoice(tm,"sList","choice 1");
  ppf.addRequestStringChoice(tm,"sList","choice 3");
  ppf.addRequestStringChoice(tm,"sList","choice 2");
  std::cout << "BPPFTEST:  did data adds" << std::endl;

  std::cout << "BPPFTEST:  defining psl." << std::endl;
  // we might want to respond to changes.
  gov::cca::ports::ParameterSetListener psl = *this;
  ppf.registerUpdatedListener(tm, psl);

  std::cout << "BPPFTEST:  defining pgl." << std::endl;
  // we might want to change the params before sharing them
  gov::cca::ports::ParameterGetListener pgl = *this;
  ppf.registerUpdater(tm, pgl); 
  std::cout << "BPPFTEST:  did listener adds" << std::endl;
#endif // FULLTEST
  // publish
  ppf.addParameterPort(tm, svc);
  std::cout << "BPPFTEST:  published port" << std::endl;

  svc.releasePort("ppf");
  std::cout << "BPPFTEST:  released ppf." << std::endl;
  ppf = 0;
  std::cout << "BPPFTEST:  assigned ppf 0." << std::endl;

  gcp = svc.getPort(pname);
  pp = ::babel_cast< gov::cca::ports::ParameterPort > (gcp);
  if (pp._is_nil()) {
    std::cout << "BPPFTEST: getport(" << pname << ") failed." << std::endl;
  }
  std::cout << "BPPFTEST:   got port pp." << std::endl;
  gov::cca::TypeMap ftm = pp.readConfigurationMap();
  std::cout << "BPPFTEST:   read config map from pp." << std::endl;
  std::string svar = ftm.getString("sVar","failed svar fetch");
  std::cout << "BPPFTEST:  sVar = " << svar << std::endl;
  bool noName = ftm.getBool("noName",false);
  std::cout << "BPPFTEST:  noName = " << noName << " (should be true)" << std::endl;
  ftm.putBool("noName",false);
  noName = ftm.getBool("noName",true);
  std::cout << "BPPFTEST:  noName = " << noName << " (should be false)" << std::endl;

  return 0;

  // DO-NOT-DELETE splicer.end(pp.testX.go)
}

/**
 *  Inform the listener that someone is about to fetch their 
 * typemap. The return should be true if the listener
 * has changed the ParameterPort definitions.
 */
bool
pp::testX_impl::updateParameterPort_impl (
  /* in */const ::std::string& portName ) 
{
  // DO-NOT-DELETE splicer.begin(pp.testX.updateParameterPort)
  // Insert-Code-Here {pp.testX.updateParameterPort} (updateParameterPort method)
    
  
	std::cout << "ccafe4::ParameterPortFactoryTest_impl::updateParameterPort(" <<
		portName << ") called." << std::endl;
	return false;

  // DO-NOT-DELETE splicer.end(pp.testX.updateParameterPort)
}

/**
 *  The component wishing to be told after a parameter is changed
 * implements this function.
 * @param portName the name of the port (typemap) on which the
 * value was set.
 * @param fieldName the name of the value in the typemap.
 */
void
pp::testX_impl::updatedParameterValue_impl (
  /* in */const ::std::string& portName,
  /* in */const ::std::string& fieldName ) 
{
  // DO-NOT-DELETE splicer.begin(pp.testX.updatedParameterValue)
    
	std::cout << "ccafe4::ParameterPortFactoryTest_impl::updatedParameterValue(" <<
		portName << ", " << fieldName << ") called." << std::endl;
  // DO-NOT-DELETE splicer.end(pp.testX.updatedParameterValue)
}


// DO-NOT-DELETE splicer.begin(pp.testX._misc)
// Insert-Code-Here {pp.testX._misc} (miscellaneous code)
// Put miscellaneous code here
// DO-NOT-DELETE splicer.end(pp.testX._misc)

