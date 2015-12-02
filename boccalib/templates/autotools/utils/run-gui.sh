#!/bin/bash

BOCCA_HOME=/Users/norris/cca/1.0.8-nightly-mpich
CCAFE_CONFIG=/Users/norris/cca/1.0.8-nightly-mpich/bin/ccafe-config
BOCCA=@BOCCA@
if test -x $BOCCA; then
	:
else
	echo "It looks like this project has not been configured yet or not configured with bocca."
	echo "The gui launcher script requires configuration with bocca."
	exit 1
fi

PROJECT_DIR=@PROJECT_TOP_DIR@

$PROJECT_DIR/buildutils/testComponent.sh --gui \
	--ccafe-rc $PROJECT_DIR/components/tests/guitest.gen.rc \
	--cca-dir $PROJECT_DIR/install/share/cca \
	--lib-dir $PROJECT_DIR/install/lib \
	--ccafe-config $CCAFE_CONFIG $*
