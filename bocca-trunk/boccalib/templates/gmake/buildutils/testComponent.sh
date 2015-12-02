#!/bin/bash

usage () {
	echo -e "\nUsage:\n  sh testComponent.sh  [--gui | --gui-backend --port <portnum>] --ccafe-rc <rcfile> --cca-dir <cca_dir> --lib-dir <lib_dir> --ccafe-config <ccafe-config>\n\n"\
		"This script creates a small Ccaffeine resource control (rc) script fragment\n"\
		"that sets the dynamic library search path to a component's <lib_dir>.\n"\
		" Arguments: \n"\
		"	--help 	: display this help and exit.\n"\
		"	--batch	: if this option is given, run ccaffeine in batch mode, otherwise\n"\
		"		use command-line interface.\n"\
		"	--gui	: if this option is given, run the ccaffeine gui, otherwise\n"\
		"		use command-line interface.\n"\
		"	--gui-backend: if this option is given, run the framework in a mode\n"\
		"		appropriate for use with a remote GUI.\n"\
		"	--port <portnum>: port number if running in client/server mode, e.g.,\n"\
		"		with --gui or --gui-backend; default is 8082.\n"\
		"	--ccafe-rc <rcfile>: rcfile is the full path name of the target\n"\
		"		Ccaffeine RC file\n"\
		"	--cca-dir <cca_dir>: cca_dir is the full path to the directory\n"\
		"		containing .cca and .scl files.\n"\
		"	--lib-dir <lib_dir>: lib_dir is the full path location of the dynamic\n"\
		"		libraries\n"\
		"	--ccafe-config <ccafe-config>: ccafe-config is the full path to the\n"\
		"		ccafe-config executable \n" > /dev/stderr
}

if [ $# -lt 6 ];  then
	usage
	exit 1;
fi

# Process command-line options
gui="0"
guibackend="0"
port="8082"
ccafeconfig=""
ccafe=""
ccadir=""
libdir=""
rcfilearg=""

while [ $# -gt 0 ]; do
	case "$1" in
		--help)
			usage;
			exit 0;
			;;
		--ccafe-rc)
			if [ $# -lt 2 ]; then usage; exit 1; fi;
			rcfilearg=$2;
			shift; shift;
			;;
		--cca-dir)
			if [ $# -lt 2 ]; then usage; exit 1; fi;
			ccadir=$2;
			shift; shift;
			;;
		--lib-dir)
			if [ $# -lt 2 ]; then usage; exit 1; fi;
			libdir=$2;
			shift; shift;
			;;
		--ccafe-config)
			if [ $# -lt 2 ]; then usage; exit 1; fi;
			ccafeconfig=$2; 
			shift; shift;
			;;
		--gui)
			gui="1"; 
			batch=0
			shift;
			;;
		--gui-backend)
			guibackend="1";
			batch=0
			shift;
			;;
                --batch)
			batch=1;
			guibackend="0";
			gui="0";
			shift;
			;;
		--port)
			port=$2;
			shift; shift;
			;;
		*)
			usage;
			exit 1;
			;;
	esac
done


if [ "x$rcfilearg" = "x" ] || [ ! -f "$rcfilearg" ]; then
	echo "Missing ccaffeine script: $rcfilearg"; 
	usage; 
	exit 1;
fi

if [ "x$ccafeconfig" = "x" ]; then 
	norun="1";
else
	norun="0";
	if [ ! -f "$ccafeconfig" ] || [ ! -x "$ccafeconfig" ]; then 
		echo "Specified value for ccafe-config does not exist or is not executable: $ccafeconfig";
		exit 1;
	fi
	if test "x$batch" = "x"; then
		ccafe=`$ccafeconfig --var CCAFE_SINGLE`
		if [ ! -f "$ccafe" ] || [ ! -x "$ccafe" ]; then 
			echo "Cannot find ccafe-single executable using $ccafeconfig --var CCAFE_SINGLE";
			exit 1;
		fi
	else
		ccafe=`$ccafeconfig --var CCAFE_BATCH`
		if [ ! -f "$ccafe" ] || [ ! -x "$ccafe" ]; then 
			echo "Cannot find ccafe-batch executable using $ccafeconfig --var CCAFE_BATCH";
			exit 1;
		fi
	fi
fi

if [ "x$ccadir" = "x" ] || [ ! -d "$ccadir" ]; then echo "Specified .cca and .scl directory does not exist: $ccadir"; fi
if [ "x$libdir" = "x" ] || [ ! -d "$libdir" ]; then echo "Specified component library directory does not exist: $libdir"; fi


# End of command-line argument processing
#-----------------------------------------

instantiate_only="0"

if [ ! -f "$rcfilearg" ] ; then 
    echo -e "*** Error: Could not run tests, didn't find $rcfilearg file."; 
    exit 1;
fi 
rcfiledir=`dirname $rcfilearg`

if [ "x`grep \"^go \" $rcfilearg`" = "x" ] ; then
  if [ "x`grep \"^connect \" $rcfilearg`" = "x" ] ; then
    echo "Running instantiation tests only";
    instantiate_only="1";
  fi 
fi

if [ "x`echo $rcfilearg | grep \.incl`" != "x" ]; then 
    rcfile="`echo $rcfilearg | sed -e 's|\.incl||'`";
else
    rcfile=$rcfilearg
fi
# Handle cases when the directory with the input rc file is not writeable
rcfilename=`basename $rcfile`
outdir=`dirname $rcfile`
if [ ! -w $rcfiledir ]; then 
    if [ "x$TMPDIR" != "x" ]; then 
         if [ -d $TMPDIR -a -w $TMPDIR ]; then 
             outdir=$TMPDIR 
         else 
             outdir=$HOME
         fi
    else 
         outdir=$HOME
    fi
fi
rcfile="$outdir/$rcfilename"

if [ "x`echo $rcfilearg | grep \.incl`" != "x" ]; then 
    sed -e "/@CCA_COMPONENT_PATH@/ s|@CCA_COMPONENT_PATH@|${ccadir}|" $rcfilearg > $rcfile;
elif [ "x`grep CCA_COMPONENT_PATH $rcfile`" != "x" ]; then
    sed -i1 -e "/@CCA_COMPONENT_PATH@/ s|@CCA_COMPONENT_PATH@|${ccadir}|" $rcfile;
    if [ -f $rcfile"1" ]; then /bin/rm -f $rcfile"1"; fi
else
    # If rcfile contains a full path, replace it with the libpath given to 
    # this script.
    if [ "`dirname $rcfilearg`" != "`dirname $rcfile`" ]; then
         cp $rcfilearg $rcfile;
    fi
    sed -i".bk" -e "s|^path set /.*$|path set ${ccadir}|" $rcfile;
    /bin/rm -f "$rcfile.bk" 
fi

if [ "$norun" == "1" ]; then
	exit 0;
fi

ccaspecconfig=`$ccafeconfig --var CCAFE_CCA_SPEC_BABEL_CONFIG`
guiprefix=`$ccafeconfig --var CCAFE_bindir`
CCASPEC_libdir=`$ccaspecconfig --var CCASPEC_libdir `
CCASPEC_pkglibdir=`$ccaspecconfig --var CCASPEC_pkglibdir `
CCASPEC_BABEL_libdir=`$ccaspecconfig --var CCASPEC_BABEL_libdir`
CCASPEC_BABEL_LANGUAGES=`$ccaspecconfig --var CCASPEC_BABEL_LANGUAGES`

babelconfig=`$ccaspecconfig --var CCASPEC_BABEL_BABEL_CONFIG`
babelconfig_version=`$babelconfig --version`

jvmlib=`$babelconfig --query-var=JVM_LIBDIR`
if test "x$jvmlib" = "x"; then
  # not tolerant of whitespace in lib dir names. may create
  # redundant path elements.
  jnihack=`$babelconfig --query-var=JNI_LDFLAGS| sed -e 's%^-L%%g' -e 's% -L% %g' -e 's% -R% %g' -e 's%^-R%%g' -e 's% %:%g'`
  JVMPATH=$jnihack
else
  # the right way, but fails under b1.0.x
  javalib=`$babelconfig --query-var=JAVA_LIBDIR`
  JVMPATH=$jvmlib:$javalib
fi

# Env. variable settings
LD_RUN_PATH=$libdir:$CCASPEC_BABEL_libdir:$CCASPEC_libdir:$JVMPATH
if [ "x$LD_LIBRARY_PATH" = "x" ] ; then
  LD_LIBRARY_PATH=$LD_RUN_PATH:
else
  LD_LIBRARY_PATH=$libdir:$CCASPEC_BABEL_libdir:$CCASPEC_libdir:$JVMPATH:$LD_LIBRARY_PATH
fi
export LD_RUN_PATH
export LD_LIBRARY_PATH

# Handle Macs
SYSTEM=`uname`
if [ "x$SYSTEM" = "xDarwin" ] ; then 
   DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH
   export DYLD_LIBRARY_PATH
fi

if [ -n "`echo $CCASPEC_BABEL_LANGUAGES | grep python`" ] ; then
   PYTHON_VER="python`$ccaspecconfig --var CCASPEC_BABEL_PYTHON_VERSION`"
   PYTHONPATH=$libdir/$PYTHON_VER/site-packages:$CCASPEC_pkglibdir/$PYTHON_VER/site-packages:$PYTHONPATH

   if [ -d $CCASPEC_BABEL_libdir/../lib64 ] ; then
	  PYTHONPATH=$CCASPEC_BABEL_libdir/../lib64/$PYTHON_VER/site-packages:$PYTHONPATH ;
   else
	  PYTHONPATH=$CCASPEC_BABEL_libdir/$PYTHON_VER/site-packages:$PYTHONPATH: ;
   fi
   #echo PYTHONPATH=$PYTHONPATH
   export  PYTHONPATH
fi

if [ -n "`echo $CCASPEC_BABEL_LANGUAGES | grep java`" ] ; then 
   CCASPEC_BABEL_VERSION=`$ccaspecconfig --var CCASPEC_BABEL_VERSION`
   CLASSPATH=$CCASPEC_BABEL_libdir/sidl-$babelconfig_version.jar:$CCASPEC_BABEL_libdir/sidlstub_$babelconfig_version.jar:$CCASPEC_libdir/cca-spec.jar:$libdir/java:$CLASSPATH
   echo "###"
   echo LDPATH=$LD_LIBRARY_PATH
   echo "###"
   echo PYTHONPATH=$PYTHONPATH
   echo "###"
   echo CLASSPATH=$CLASSPATH
   echo "###"
   export CLASSPATH
fi

logfile="$outdir/$rcfilename.log"
	
if [ "x$gui" = "x1" ]; then 
	echo "Test script: $rcfile"; 
	($guiprefix/gui-backend.sh --port $port --ccafe-rc $rcfile > $logfile 2>&1) &
	sleep 5; 
	$guiprefix/gui.sh --port $port --bgColor=255,255,255 --tutorialMode
	exit 0;
else
    if [ "x$guibackend" = "x1" ]; then 
		echo "Test script: $rcfile"; 
		$guiprefix/gui-backend.sh --port $port --ccafe-rc $rcfile
		exit 0;
    fi
fi


if [ "x`grep quit $rcfile`" = "x" ] && [ "x$gui" = "x0" ] && [ "x$guibackend" = "x0" ]; then echo "quit" >> $rcfile; fi; 
if test "x$CCAFE_VALGRIND" = "x"; then
	:
else
	echo "Using $CCAFE_VALGRIND on"
 	echo "$ccafe --ccafe-rc $rcfile > $logfile 2>&1" ; 
fi
# CCAFE_VALGRIND cannot be used for gdb. it could be used for any sane
# profiler however.
$CCAFE_VALGRIND $ccafe --ccafe-rc $rcfile > $logfile 2>&1 ; 
echo "Test script: $rcfile"; 
echo "Log file: $logfile"
if [ "$instantiate_only" != "1" ] ; then
	successful=`grep "specific go command successful" $logfile | wc -l`
	expected=`egrep "^go " $rcfile | wc -l`
	if [  "x$successful" != "x0" -a "x$successful" = "x$expected" ]; then 
	    echo -e "SUCCESS:"
	    echo -e "==> Test passed, go command(s) executed successfully (see $logfile)."; 
	    exit 0;
	else 
	    echo -e "*** Error: Some run tests did NOT succeed, go command failed (see $logfile)."; 
	    exit 1;
	fi 
else # Instantiation test only
	successful=`grep "instantiate" $rcfile | wc -l`;
	expected=`grep "successfully instantiated" $logfile | wc -l`;
	if [ "x$successful" != "x0" -a "x$successful" = "x$expected" ]; then 
	    echo -e "SUCCESS:"
	    echo -e "==> Instantiation tests passed for all built components (see $logfile)."; 
	    exit 0;
	else 
	    echo -e "*** Error: Instantiation failed for some built components (see $logfile)."; 
	    grep "instantiation failed" $logfile; 
	    exit 1;
	fi 
fi
