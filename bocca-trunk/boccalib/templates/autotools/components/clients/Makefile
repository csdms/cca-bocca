# ---- Edit below this line only if you know what you are doing ----

CLIENT_BUILD=1
export COMPONENT_CLIENT_BUILD:=1

# The common.make file contains CCA and Babel settings, as well as 
# compilation targets for all languages.
ifeq ($(shell if test -f ../../buildutils/make.vars.common ; then echo "0"; else echo "1"; fi),0)
	include ../../buildutils/make.vars.common
	# this also includes make.project, make.vars.user
else
	$(error "Please run configure in the top-level directory before invoking make")
endif

CLIENT_TOP_DIR = $(PROJECT_TOP_DIR)/components/clients
SIDL_DIR = $(PROJECT_TOP_DIR)/components/sidl
LOCAL_PREFIX = $(PROJECT_TOP_DIR)/components/clients

RELATIVE_TOP=../../../..

ifndef SIDL_SYMBOLS
ifeq ($(INSTALL_TARGET),install)
    SIDL_SYMBOLS=$(COMPONENT_CLIENTS) $(CLASS_CLIENTS)
else
    ifeq ($(INSTALL_TARGET),clean)
        SIDL_SYMBOLS=$(COMPONENT_CLIENTS) $(CLASS_CLIENTS)
    else
        SIDL_SYMBOLS=$(sort $(CLASS_DEPS) $(CLASS_CLASS_DEPS))
    endif
endif
endif

ifneq ($(SIDL_SYMBOLS),)
    ifeq ($(SIDL_FILES),)
        SIDL_FILES = $(addprefix $(SIDL_DIR)/,$(addsuffix .sidl,$(SIDL_SYMBOLS)))
    endif
endif

include ../../buildutils/make.client.toplevel



