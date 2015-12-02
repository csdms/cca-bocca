#!/bin/bash

# bocca wrapper on gui-backend to supply the default rc file.
# if you specify another rc file, it will override the default.

BOCCA_HOME=/Users/norris/cca/1.0.8-nightly-mpich
CCAFE_CONFIG=/Users/norris/cca/1.0.8-nightly-mpich/bin/ccafe-config

BOCCA=@BOCCA@

if test -x $BOCCA; then
	:
else
	echo "It looks like this project has not been configured yet. Run configure before using the GUI."
	exit 1
fi

PROJECT_DIR=@PROJECT_TOP_DIR@

#KPATH="`$CCAFE_CONFIG --var CCAFE_bindir`"
#$KPATH/gui-backend.sh  --ccafe-rc $PROJECT_DIR/components/tests/guitest.gen.rc $* &

$PROJECT_DIR/buildutils/testComponent.sh --gui-backend --ccafe-rc $PROJECT_DIR/components/tests/guitest.gen.rc \
	--cca-dir $PROJECT_DIR/install/share/cca --lib-dir $PROJECT_DIR/install/lib --ccafe-config $CCAFE_CONFIG $* 


