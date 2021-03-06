# User-defined top-level settings
# The common.make file contains CCA and Babel settings, as well as 
# compilation targets for all languages.
ifeq ($(shell if test -f buildutils/make.vars.common ; then echo "0"; else echo "1"; fi),0)
    include buildutils/make.vars.common
    # this also includes make.project and make.vars.user
else
    $(error "Please run configure in the top-level directory before invoking make")
endif

MYDIR := $(shell bash -c "pwd -P")

# Get mpi option from ccaffeine
USE_MPI=$(shell ${CCAFE_CONFIG} --var CCAFE_USEMPI)

# get rid of symlinks with pwd -P so we can be sure the path is unique
CURDIR = $(shell bash -c "pwd -P")
ABS_TOP_PROJ_DIR = $(shell bash -c "cd $(PROJECT_TOP_DIR);pwd -P")

ifndef SUBDIRS
	SUBDIRS = external ports components depl
endif

NUM_PARALLEL_JOBS = $(shell echo "$(PMAKE_OPTS)" | sed -e 's| *-j *||')
ifeq ($(strip $(NUM_PARALLEL_JOBS)),)
	NUM_PARALLEL_JOBS=1
endif

ifneq ($(NUM_PARALLEL_JOBS),1)
	ifeq ($(findstring -j,$(MAKEFLAGS)),)
		PBUILD_FLAG = -j $(NUM_PARALLEL_JOBS)
	endif
endif

CLIENTDIRS = external ports components/clients

all: pre-build-user components post-build-user
	@-echo "################ Finished building everything #################"
	@-echo "####### You can run some simple tests with 'make check' #######"

$(CLIENTDIRS): pre-build-user
	@if ! test "$(CURDIR)" = "$(ABS_TOP_PROJ_DIR)"; then echo "***Project directory has changed. Please run configure."; exit 1; fi
	$(HIDE_LIBTOOL)if [ -d $@ ]; then \
		if [ "x$(wildcard $@/sidl/*.sidl)" != "x" ] || [ "x$@" = "xcomponents/clients" -a "x$(wildcard components/sidl/*.sidl)" != "x" ]; then \
			echo "# ======================================================================="; \
			echo "# Building in $@/, languages: $(SUPPORTED_COMPONENT_LANGUAGES)"; \
			echo "# ======================================================================="; \
			$(MAKE) $(CCA_MAKEFLAGS) FROMTOP=1 LANGUAGES="$(SUPPORTED_COMPONENT_LANGUAGES)" -C $@ all; \
		else \
			echo "# ======================================================================="; \
			echo "# No SIDL files in $@/sidl, skipping build for $@"; \
			echo "# ======================================================================="; \
		fi \
	fi

components: $(CLIENTDIRS)
	@if ! test "$(CURDIR)" = "$(ABS_TOP_PROJ_DIR)"; then echo "***Project directory has changed. Please run configure."; exit 1; fi
	$(HIDE_LIBTOOL)if [ -d $@ ]; then \
		if [ "x$(wildcard $@/sidl/*.sidl)" != "x" ]; then \
			echo "# ======================================================================="; \
			echo "# Building in $@/, languages: $(SUPPORTED_COMPONENT_LANGUAGES)"; \
			echo "# ======================================================================="; \
			$(MAKE) $(CCA_MAKEFLAGS) -C $@ all; \
		else \
			echo "# ======================================================================="; \
			echo "# No SIDL files in $@/sidl, skipping build for $@"; \
			echo "# ======================================================================="; \
		fi \
	fi
	
post-build-user:: components

install: pre-install-user install-all post-install-user

install-all:
	$(HIDE_LIBTOOL)for dir in $(CLIENTDIRS) components; do \
		$(MAKE) $(CCA_MAKEFLAGS) -C $$dir INSTALL_LANGUAGES="$(INSTALL_LANGUAGES)" install; \
	done
	@-if ! test -d $(libdir) ; then $(UTILS_DIR)/mkdirhier $(libdir) >& /dev/null; fi
	@-if ! test -d $(bindir) ; then $(UTILS_DIR)/mkdirhier $(bindir) >& /dev/null; fi
	$(INSTALL) utils/$(PROJECT_NAME)-config $(bindir)
	$(INSTALL_DATA) utils/config-data $(libdir)/$(PROJECT_NAME).config-data
	@-echo "################### Finished installing everything ####################"
	@-echo "####### You can run some simple tests with 'make install-check' #######"

check: 
	$(MAKE) $(CCA_MAKEFLAGS) -C components check
	$(MAKE) $(CCA_MAKEFLAGS) check-user
	
install-check:
	$(MAKE) $(CCA_MAKEFLAGS) -C components install-check

testgui: 
	$(MAKE) $(CCA_MAKEFLAGS) -C components testgui

user-tests:
	$(MAKE) $(CCA_MAKEFLAGS) -C components user-tests

clean:
	$(HIDE_LIBTOOL)for dir in $(CLIENTDIRS) components depl; do \
		$(MAKE) $(CCA_MAKEFLAGS) -C $$dir clean; \
	done
	-@$(RM) -r install/lib install/include/*.h* install/include/*.mod install/share
	@-touch .cleaned
	$(HIDE_LIBTOOL)$(MAKE) $(CCA_MAKEFLAGS) clean-user

# does not do a complete job but gets low-hanging fruit.
distclean: clean
	-@$(RM)  \#* *~ components/babel.make.all
	-@find . -name '.#*' -o -name '#*' | xargs rm
	$(HIDE_LIBTOOL)for dir in $(SUBDIRS); do \
		$(MAKE) $(CCA_MAKEFLAGS) -C $$dir $(PBUILD_FLAG) distclean; \
	done
	$(HIDE_LIBTOOL)$(MAKE) $(CCA_MAKEFLAGS) distclean-user

.PHONY: $(CLIENTDIRS) components install-ports install-components $(USER_TARGETS) $(USER_PHONY)

# User-specified top-level build rules
ifeq ($(shell if test -f make.rules.user ; then echo "0"; else echo "1"; fi),0)
    include make.rules.user
endif
