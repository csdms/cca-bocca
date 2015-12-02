#!/bin/bash

usage () {
	echo -e "\nUsage:\n\tsh $0 <build_or_install> <client_or_server> <topdir> <language> <symbols>\n\n"\
		"This script returns a list of full-path library names for the specified SIDL symbols.\n"\
		" Arguments: \n"\
		"        build_or_install is either 'install_local' or 'install' based on whether this is the\n" \
		"                build library location or the installed library location.\n" \
		"        client_or_server is either 'client' or 'server. \n" \
		"        topdir is the full path name of the top-level directory for the library\n"\
		"        language is one of: none, c, cxx, f77, f90, python, java.\n" \
		"	     symbols is the list of fully-qualified SIDL symbol names\n" > /dev/stderr

}

if [ $# -lt 4 ];  then
	usage
	exit 1;
fi

client_or_server=$1; shift
build_or_install=$1; shift
topdir=$1; shift;
language=$1; shift;
symbols=$@

libpaths=""

for symbol in $symbols; do
	# Server library
	if [ "$client_or_server" = "server" ]; then
	    if [ "$build_or_install" = "install_local" ] || [ "$language" = "python" ]; then
			libname="$topdir/$symbol/lib$symbol.la"
		else
			libname="$topdir/$symbol/.install/lib$symbol.la"
		fi
	else
		if [ "$build_or_install" = "install_local" ] || [ "$language" = "python" ]; then
			libdir="$topdir/$symbol/$language"
		else
			libdir="$topdir/$symbol/$language/.install"
		fi
		if [ "$language" = "none" ]; then
			libname="$libdir/lib$symbol.la"
		elif [ "$language" = "python" ]; then
			libname="$libdir/`echo $symbol | sed -e 's|\.|/|g'`.so"
		else
			libname="$libdir/lib$symbol-$language.la"
		fi
	fi
	libpaths="$libpaths $libname"
done
echo "$libpaths"
