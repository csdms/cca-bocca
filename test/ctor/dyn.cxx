#include <iostream>
#include "sidl.hxx"

void instantiateTestDynamic(std::string libraryClassName) {

    std::cout << "Babel Component: " << name << " to be instantiated" << std::endl;
    
    gov::cca::Component babelCmpt;
    sidl::BaseClass bc;
    sidl::DLL dll = sidl::Loader::findLibrary(libraryClassName, "ior/impl", sidl::Scope_SCLSCOPE, sidl::Resolve_SCLRESOLVE);
    if (dll._is_nil()) {
      std::cout << ":-( Could not load Babel component using "
             "sidl::Loader::findLibrary for library: " 
		<< libraryClassName << std::endl;
      std::cout << "Seeking Component class: " << libraryClassName << std::endl;
      dump_babel_dl_info();
      return;
    }
    bc = dll.createClass(libraryClassName);
    if (bc._is_nil()) {
      std::cout << ":-( For some reason, even though we loaded the component "
             "successfully, the component could not be instantiated.\n"
             "Is your component linked properly or misspelled?"
             "Just a guess but you might want to try "
             "recompiling *everything*.\n Could not instantiate "
             "component class named:" << libraryClassName << std::endl;
      dump_babel_dl_info();
      return;
    }

    babelCmpt = ::babel_cast<gov::cca::Component> (bc);  // CAST

    if ( babelCmpt._is_nil() ) {
      std::cout << ":-( Could not cast to gov.cca.Component, are you sure your "
             "component subclasses gov.cca.Component?\n"
             " classname: " << className << std::endl;
      dump_babel_dl_info();
    }
}

