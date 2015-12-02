# ---- Edit below this line only if you know what you are doing ----
# The order of variable definitions and file inclusions matters!

CLIENT_BUILD=1
export EXTERNAL_BUILD:=1

MYDIR := $(shell bash -c "pwd -P")

# The common.make file contains CCA and Babel settings, as well as 
# compilation targets for all languages.
ifeq ($(shell if test -f ../buildutils/make.vars.common ; then echo "0"; else echo "1"; fi),0)
	include ../buildutils/make.vars.common
	# this also includes make.project, make.vars.user
else
	$(error "Please run configure in the top-level directory before invoking make")
endif


ifeq ($(SIDL_SYMBOLS),)
    SIDL_SYMBOLS=$(EXTERNAL_SIDL_SYMBOLS)
endif

ifeq ($(SIDL_FILES),)
    SIDL_FILES=$(EXTERNAL_SIDL_FILES)
endif

ifeq ($(SIDL_FILES),)
    SIDL_FILES = $(wildcard sidl/*.sidl)
endif

CLIENT_TOP_DIR = $(PROJECT_TOP_DIR)/external

include ../buildutils/make.client.toplevel


