# ---- Edit below this line only if you know what you are doing ----

CLIENT_BUILD=1
export PORT_BUILD:=1
# The common.make file contains CCA and Babel settings, as well as 
# compilation targets for all languages.
ifeq ($(shell if test -f ../buildutils/make.vars.common ; then echo "0"; else echo "1"; fi),0)
	include ../buildutils/make.vars.common
	# this also includes make.project, make.vars.user
else
	$(error "Please run configure in the top-level directory before invoking make")
endif

CLIENT_TOP_DIR = $(PROJECT_TOP_DIR)/ports

# The sort doesn't work as it gets rid of dependencies between clients, will regenerate
# properly at some point in the future (the value for INTERFACE_DEPS)
#ifeq ($(INSTALL_TARGET),install)
#    SIDL_SYMBOLS = $(INTERFACES) $(PORTS)
#else
#    ifeq ($(INSTALL_TARGET),clean)
#        SIDL_SYMBOLS=$(INTERFACES) $(PORTS)
#    else
#        SIDL_SYMBOLS = $(sort $(INTERFACE_DEPS))
#    endif
#endif

SIDL_SYMBOLS= $(INTERFACES) $(PORTS)


include ../buildutils/make.client.toplevel
