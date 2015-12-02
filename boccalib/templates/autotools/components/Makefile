# ----------- Avoid making changes below this line :-) ---------------------

SERVER_BUILD = 1

# The common.make file contains CCA and Babel settings, as well as 
# compilation targets for all languages.
ifeq ($(shell if test -f ../buildutils/make.vars.common ; then echo "0"; else echo "1"; fi),0)
        include ../buildutils/make.vars.common
        # this also includes make.project, make.vars.user
else
        $(error "Please run configure in the top-level directory before invoking make")
endif

COMPONENTS_DIR := $(shell bash -c "pwd -P")

# Include SIDL file, package, and component descriptions
include make.components

#### Component settings derived from the COMPONENTS variable in make.components
COMPONENT_SIDL_SYMBOLS = $(foreach comp, $(COMPONENTS), $(strip $(shell echo $(comp) | sed -e 's|-.*||g')))
# For now treat classes the same as components
COMPONENT_SIDL_SYMBOLS += $(foreach comp, $(CLASSES), $(strip $(shell echo $(comp) | sed -e 's|-.*||g')))
COMPONENT_CLEAN_MAKEFILES=$(addsuffix /Makefile,$(COMPONENT_SIDL_SYMBOLS))

LIB_DIR = $(COMPONENTS_DIR)/lib

COMPONENT_DIRS = $(COMPONENT_SIDL_SYMBOLS)
ifndef COMPONENT_TARGET
	COMPONENT_TARGET = all
endif

# Parallel make
ifeq ($(MAKELEVEL),0)
    #PBUILD_FLAG=$(PMAKE_OPTS)
    # parallel builds currently don't work, will be fixed in future
    PBUILD_FLAG=
else
    PBUILD_FLAG=
endif
MYCOLOR = $(MAGENTA)

CLIENT_SIDL_FILES=$(strip $(sort $(PORT_SIDL_FILES) $(CLASS_SIDL_FILES)))
CLIENT_LIB_TARGETS=$(strip $(sort $(PORT_LIB_TARGETS) $(CLASS_LIB_TARGETS)))

# Variables to export to submakes
export INSTALL_TARGET
export COMPONENT_TOP_DIR=$(COMPONENTS_DIR)
export QUIET

#==================================================================================
# Top-level server build (for all components and classes)

#-----------------------------------------------------------------------------------------	
#### The following targets build all of the component libraries

all: check_top_dir RESULT-clean $(COMPONENT_DIRS) post-build-user
	@-if test -f .make-result ; then \
		echo "Build summary:"; \
		cat .make-result; \
		echo "### To test instantiation of successfully built components, run 'make check' ###"; \
	fi
	@-$(RM) .make-result

#-----------------------------------------------------------------------------------------
check_top_dir:
	@if ! test "$(COMPONENTS_DIR)" = "$(PROJECT_TOP_DIR)/components"; then \
		echo "***Project directory has changed. Please run configure in the top-level project directory."; \
		exit 1; \
	fi

#-----------------------------------------------------------------------------------------	
#### Build clients for ports, external entities, classes, and components depend on
include $(UTILS_DIR)/make.rules.common

#-----------------------------------------------------------------------------------------	
#### Generate impls and build this project's classes and components
$(COMPONENT_DIRS): check_top_dir pre-build-user $(EXT_LIB_TARGETS) $(PORT_LIB_TARGETS) $(CLASS_LIB_TARGETS) $(CLASS_SYMBOLS)
	@if [ ! -f $@/Makefile ]; then \
		echo "# Common makefile fragment" > $@/Makefile; \
		echo "RELATIVE_TOP=../.." >> $@/Makefile; \
		echo "COMPONENT=$@" >> $@/Makefile; \
		echo "include "'$$(RELATIVE_TOP)/buildutils/make.server' >> $@/Makefile; \
	fi; \
	if [ ! -f $@/make.vars.user ]; then if [ -e $(UTILS_DIR)/make.vars.user ]; then \
		sed -e "s|@SIDLNAME@|$@|g" $(UTILS_DIR)/make.vars.user >  $@/make.vars.user; \
	fi; fi; \
	if [ ! -f $@/make.rules.user ]; then if [ -e $(UTILS_DIR)/make.rules.user ]; then \
		cp $(UTILS_DIR)/make.rules.user $@/make.rules.user; \
	fi; fi; 
	$(HIDE_LIBTOOL)if [ ! -f "$@/.$@.babel.make.depends" ]; then \
		if [ "x$(QUIET)" = "x" ] ; then echo ""; echo "   [s] Building class/component $(MYCOLOR)$@$(BLACK): "; fi; \
		if [ "x$(DEBUG)" != "x" ]; then echo "DEBUG: $(MAKE) $(CCA_MAKEFLAGS) -C $@ COMPONENT=$@ DEBUG=$(DEBUG) .gencode"; fi; \
		$(MAKE) $(CCA_MAKEFLAGS) -C $@ COMPONENT=$@ DEBUG=$(DEBUG) .gencode; \
		$(UTILS_DIR)/combineBabelMakes.sh $@ >/dev/null; \
		if [ "x$(DEBUG)" != "x" ]; then echo "DEBUG: $(MAKE) $(CCA_MAKEFLAGS) -C $@ COMPONENT=$@ DEBUG=$(DEBUG) $(COMPONENT_TARGET)"; fi; \
		$(MAKE) $(CCA_MAKEFLAGS) -C $@ COMPONENT=$@ COMPONENT_TOP_DIR=$(COMPONENTS_DIR) DEBUG=$(DEBUG) $(COMPONENT_TARGET);  \
	else \
		if [ "x$(QUIET)" = "x" ] ; then echo "   [s] Building class/component $(MYCOLOR)$@$(BLACK): "; fi; \
		if [ "x$(DEBUG)" != "x" ]; then echo "DEBUG: $(MAKE) $(CCA_MAKEFLAGS) -C $@ COMPONENT=$@ DEBUG=$(DEBUG) $(COMPONENT_TARGET)"; fi; \
		$(MAKE) $(CCA_MAKEFLAGS) -C $@ COMPONENT=$@ $(COMPONENT_TARGET);  \
		if [ "x$(INSTALL_TARGET)" = "xinstall" ]; then  \
			$(MAKE) $(CCA_MAKEFLAGS) $(PBUILD_FLAG) -C $@ COMPONENT=$@ COMPONENT_TOP_DIR=$(COMPONENTS_DIR) DEBUG=$(DEBUG) install; \
		fi; \
	fi

post-build-user:: $(COMPONENT_DIRS)

install: pre-install-user install-all post-install-user

install-all: $(COMPONENT_DIRS)
	@if [ "x$(DEBUG)" != "x" ]; then echo "DEBUG: $(LIBTOOL) --mode=finish $(HIDE_COMPILE) $(INSTALL_LIB_DIR);"; fi; 
	$(HIDE_LIBTOOL)$(LIBTOOL) --mode=finish $(INSTALL_LIB_DIR)

RESULT-clean:
	@-$(RM) .make-result


#-----------------------------------------------------------------------------------------
#### The check target checks whether the components can be loaded and instantiated
check: check_top_dir test1 check-user

test1:
	@echo "### Test library load and instantiation for the following languages: $(LANGUAGES)"
	@-if test -f $(COMPONENT_TOP_DIR)/tests/instantiation.gen.rc; then \
		$(SH) $(UTILS_DIR)/testComponent.sh \
			--ccafe-rc $(COMPONENT_TOP_DIR)/tests/instantiation.gen.rc \
			--cca-dir $(INSTALL_DATA_DIR)/cca --lib-dir $(INSTALL_LIB_DIR) \
			--ccafe-config $(CCAFE_CONFIG) ; \
	else \
		echo "No CCA components to test for instantiation."; \
	fi

testgui:
	@echo "### Test with the Ccaffeine GUI (note that the ccafe-gui package must be installed in the same location as Ccaffeine for this to work)"
	$(HIDE_LIBTOOL)-if test -f $(COMPONENT_TOP_DIR)/tests/guitest.gen.rc; then \
		$(SH) $(UTILS_DIR)/testComponent.sh --gui --ccafe-rc \
			$(COMPONENT_TOP_DIR)/tests/guitest.gen.rc \
			--cca-dir $(INSTALL_DATA_DIR)/cca --lib-dir $(INSTALL_LIB_DIR) \
			--ccafe-config $(CCAFE_CONFIG) ; \
	else \
		echo "No CCA components to test for gui."; \
	fi
		
#-----------------------------------------------------------------------------------------
# Run arbitrary user scripts defined in the USER_TESTS variable (make.components)
user-tests: 
	@-if [ "x$(USER_TESTS)$(components_TESTS)" != "x" ] ; then \
		$(MAKE) $(CCA_MAKEFLAGS) $(sort $(USER_TESTS) $(components_TESTS)); \
	else \
		echo "No user tests specified with the variable USER_TESTS in make.components"; \
	fi

$(sort $(USER_TESTS) $(components_TESTS)): 
	@-echo "### Running user script"; \
	$(SH) $(UTILS_DIR)/testComponent.sh --ccafe-rc $(COMPONENT_TOP_DIR)/tests/$@ \
		--cca-dir $(INSTALL_DATA_DIR)/cca --lib-dir $(INSTALL_LIB_DIR) \
		--ccafe-config $(CCAFE_CONFIG) $(CCAFE_OTHERARGS)

#-----------------------------------------------------------------------------------------
# Installation check (instantiation only)
install-check:
	@echo "### Test installed library load and instantiation for the following languages: $(LANGUAGES)"
	$(SH) $(UTILS_DIR)/testComponent.sh --ccafe-rc $(COMPONENT_TOP_DIR)/tests/instantiation.installed.gen.rc \
		--cca-dir $(INSTALL_DATA_DIR)/cca --lib-dir $(INSTALL_LIB_DIR) --ccafe-config $(CCAFE_CONFIG) 

#-----------------------------------------------------------------------------------------
#### The clean target invokes 'make clean' in each component directory# Use PBUILD_FLAG instead of PMAKE_OPTS in submakes (ports/ components/) to avoid

clean:
	@-for component in $(COMPONENT_SIDL_SYMBOLS) ; do \
		echo "#### make $@ in components/$$component"; \
	  	if [ -f $$component/Makefile ]; then \
	  		if [ "x$(DEBUG)" = "x1" ]; then echo "$(MAKE) $(CCA_MAKEFLAGS) $(PBUILD_FLAG) -C $$component COMPONENT_TOP_DIR=$(COMPONENTS_DIR) $@; "; fi; \
	  		$(MAKE) $(CCA_MAKEFLAGS) $(PBUILD_FLAG) -C $$component COMPONENT_TOP_DIR=$(COMPONENTS_DIR) $@; \
	  	fi; \
	done;
	$(HIDE_LIBTOOL)if [ "$(MAKELEVEL)" = "0" ]; then $(MAKE) $(CCA_MAKEFLAGS) -C clients clean; fi
	$(HIDE_LIBTOOL)$(RM)  lib/*.la lib/*.so lib/*.cca lib/*.dylib lib/*.a tests/*.log tests/*.gen.rc */babel.make.all
	$(HIDE_LIBTOOL)$(MAKE) $(CCA_MAKEFLAGS) clean-user

distclean: 
	@-for component in $(COMPONENT_SIDL_SYMBOLS) ; do \
		echo "#### make $@ in $$component"; \
	  	if [ -f $$component/Makefile ]; then \
	  		$(MAKE) $(CCA_MAKEFLAGS) $(PMAKE_OPTS) -C $$component $@; \
	  	fi; \
	done;
	$(HIDE_LIBTOOL)if [ "$(MAKELEVEL)" = "0" ]; then $(MAKE) $(CCA_MAKEFLAGS) -C clients clean; fi
	$(HIDE_LIBTOOL)-$(RM) -rf $(COMPONENT_CLEAN_MAKEFILES) \
		lib/*.cca lib/lib* include tests/*.log tests/*.gen.rc \
		*~ *.make.package .*babel.make.package 
	$(HIDE_LIBTOOL)$(MAKE) $(CCA_MAKEFLAGS) distclean-user

.PHONY: $(COMPONENT_DIRS) lib RESULT-clean user-tests clean distclean .msg check_top_dir \
	$(USER_TARGETS) $(USER_PHONY)

#-----------------------------------------------------------------------------------------
# User-specified rules for components top-level build
ifeq ($(shell if test -f make.rules.user ; then echo "0"; else echo "1"; fi),0)
    include make.rules.user
endif

debug:
	@echo "COMPONENT_DIRS=$(COMPONENT_DIRS)"
	@echo "CCAFE_CONFIG=$(CCAFE_CONFIG)"
	@echo "INSTALL_DATA_DIR=$(INSTALL_DATA_DIR)"
	@echo "User targets (phony)=$(USER_TARGETS) $(USER_PHONY)"
