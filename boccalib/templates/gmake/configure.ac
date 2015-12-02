dnl Process this file with autoconf >= 2.60 to produce a configure script:
dnl    aclocal -I config
dnl    autoconf 
dnl
dnl Customizing for specific projects should be put in
dnl the section below marked:
dnl # User configure checks. Begin.
dnl # User configure checks. End.
dnl and in the final ac_output related macro calls.
dnl
dnl As of 0.4.2, bocca never edits configure.ac. 
dnl configure.ac is usually the most precious of all code in a project.
dnl There are no plans that it ever will edit configure.ac. 
dnl Some hypothetical 
dnl upgrade assistant script may in the future read a configure.ac and
dnl generate a suggested replacement file under the name
dnl configure.ac.suggested.

#--------------------------------------------------------------------
#       Disable caching since it seems to get in the way
#       more times than it helps us.
#--------------------------------------------------------------------
define([AC_CACHE_LOAD], )dnl
define([AC_CACHE_SAVE], )dnl


# Make sure we're us.
AC_INIT(__tcejorp__, 0.0.0, yourname@yourhost)
AC_PREREQ(2.60) 

dnl The user should change make.vars.user in the next line
dnl to something unique to one of their ports or components
dnl eventually.
AC_CONFIG_SRCDIR(make.vars.user)
AC_CONFIG_AUX_DIR([config])


# Make sure we use bash
AC_CHECK_PROG(BASH, bash, `which bash`, /bin/bash)

# enforce make 3.8 or later.
BOCCA_CHECK_GNU_MAKE

# Check for libutil.a (needed on Fedore Core 2 for python 2.3.4)
EXTRA_PYTHON_LIBS=""
AC_CHECK_LIB(util,openpty,[EXTRA_PYTHON_LIBS="$EXTRA_PYTHON_LIBS -lutil"])

AC_PREFIX_DEFAULT([`pwd`/install])

BPACKAGE_TARNAME=PACKAGE_TARNAME
AC_ARG_WITH(ccafe-config,
	[  
  --with-ccafe-config=/path/to/ccafe-config       full path to ccafe-config executable],
	, [with_ccafe_config=`which ccafe-config 2>/dev/null`])

if test -z "$with_ccafe_config" && test -f make.project; then
	AC_MSG_NOTICE( [ Hmmm. no --with-ccafe-config specified, but we have make.project ] )
	AC_MSG_CHECKING( [ ccafe-config specified in file make.project ] )
	with_ccafe_config=`grep -E '^\s*CCAFE_CONFIG.*/ccafe-config\s*$' make.project|sed -e 's/=/ /'|awk  '{print $2}'`
	if test -n "$with_ccafe_config";then
		AC_MSG_RESULT([got it.])
	else
		AC_MSG_RESULT([nope.])
	fi
fi
#  === if $with_ccafe_config still empty, bail ===
if test -z "$with_ccafe_config"; then
	AC_MSG_ERROR([--with-ccafe-config must be given, we can't find ccafe-config any other way.])
fi
if test -d "$with_ccafe_config" ; then
	AC_MSG_ERROR([--with-ccafe-config must be given the path of the script, not a directory.])
fi
if ! test -f "$with_ccafe_config" ; then
	AC_MSG_ERROR([$with_ccafe_config executable not found, use --with-ccafe-config to specify the full path location.])
fi
if ! test -x "$with_ccafe_config" ; then
	AC_MSG_ERROR([--with-ccafe-config=$with_ccafe_config: $with_ccafe_config not executable.])
fi
CCAFE_CONFIG="$with_ccafe_config"

AC_ARG_VAR([BOCCA],[path of the bocca executable])
AC_ARG_WITH(bocca,
        [
  --with-bocca=/path/to/bocca       full path to bocca executable],
        , [with_bocca=_search])
case "$with_bocca" in
        no) AC_MSG_NOTICE([bocca not found. some utils/ scripts will not be working.]
        ;;
        yes)
        with_bocca=_search
        ;;
        *) BOCCA=$with_bocca
        ;;
esac

if test "$with_bocca" = "_search"; then
        AC_PATH_PROG([BOCCA],[bocca],[_search])
fi
#  === if $with_ccafe_config still empty, bail ===
if test -z "$BOCCA" -o "$BOCCA" = "_search"; then
        AC_MSG_NOTICE([--with-bocca=/where/is/bocca must be given to enable bocca-based utilities.])
else
	if test -d "$BOCCA" ; then
		AC_MSG_ERROR([--with-bocca must be given the path of the script, not a directory.])
	fi
	if test -x "$BOCCA" ; then
		:
	else
		AC_MSG_ERROR([--with-bocca=$BOCCA: $BOCCA not executable.])
	fi
fi

AC_ARG_ENABLE(update-bocca,
	[  --enable-update-bocca           Turn on bocca config -u automatically after configure.],
	, [ enableval=no ])
case $enableval in
  yes) BOCCA_CONFIG_UPDATE="bocca config -u"
  ;;
  *) : 
  ;;
esac

# we could just query and include the sh vars file, but we want to be more targetted
# so we know what we depend on explicitly.
CCASPEC_MAKEINCL=`$with_ccafe_config --var CCAFE_BABEL_CCA_CONFIG`
CCASPEC_CONFIG=`$with_ccafe_config --var CCAFE_CCA_SPEC_BABEL_CONFIG`
CCASPEC_BABEL_LANGUAGES=`grep CCASPEC_BABEL_LANGUAGES $CCASPEC_MAKEINCL | sed -e 's/^CCASPEC_BABEL_LANGUAGES=//'`
CCASPEC_GENCCAXML=`$CCASPEC_CONFIG --var CCASPEC_GENCCAXML`

# add f77_31 if babel, spec overlooked it.
echo $CCASPEC_BABEL_LANGUAGES |grep f77_31
f77_31inlist=$?
if test "$f77_31inlist" = "0" ; then
	:
else
	echo $CCASPEC_BABEL_LANGUAGES |grep f77
	f77inlist=$?
	if test "$f77inlist" = "0"; then
		: CCASPEC_BABEL_LANGUAGES="$CCASPEC_BABEL_LANGUAGES f77_31"
	fi
fi

AC_ARG_WITH(languages, 
	[  --with-languages="LANG1 LANG2 LANG3 ..."        list of languages (e.g., "c cxx f90 python java"); 
                                                  by default all Babel-supported languages are available],
	, [with_languages="$CCASPEC_BABEL_LANGUAGES"])

LANGUAGES="$with_languages"

echo configure: Configuring with languages: $LANGUAGES

PROJECT_NAME=__tcejorp__
PROJECT_TOP_DIR=`dirname $0`
CURRENT_DIRECT=`/bin/pwd`
cd $PROJECT_TOP_DIR
PROJECT_TOP_DIR=`/bin/pwd`
cd $CURRENT_DIRECT
unset CURRENT_DIRECT

AC_ARG_WITH(numpmake, 
	[  --with-numpmake=n                          Number of processes to use in parallel make invocation (default = 1);], 
	, [with_numpmake="auto"])

if test "$with_numpmake" = "auto"; then
	# Try to determine number of cores automatically
	with_numpmake=`$PROJECT_TOP_DIR/buildutils/numcores.py`
	if test "$?" != "0"; then with_numpmake=1; fi
	if test "x$with_numpmake" = "x"; then with_numpmake=1; fi
fi

MAKE_OPTS="-j $with_numpmake"

AC_MSG_NOTICE([Project source dir apparently $PROJECT_TOP_DIR])
AC_MSG_NOTICE([Using $with_numpmake processe(s) in calls to make.])

if test "x$CCASPEC_GENCCAXML" = "x"; then
  CCASPEC_GENCCAXML=$PROJECT_TOP_DIR/buildutils/fakedepl.sh
  AC_MSG_NOTICE([Unindexed genccaxml in cca-spec-babel installation.])
else
  if ! test -x $CCASPEC_GENCCAXML; then
    AC_MSG_NOTICE([Unexecutable genccaxml in cca-spec-babel installation: $CCASPEC_GENCCAXML.])
    CCASPEC_GENCCAXML=$PROJECT_TOP_DIR/buildutils/fakedepl.sh
  fi
fi

AC_PROG_MAKE_SET()

BOCCA_IO_FLAGS="-D_BOCCA_STDERR"
AC_ARG_ENABLE(cxx-func-names,
	[  --enable-cxx-function-names     Turn on reporting of function names that requires boost.],
	, [ enableval=no ])
case $enableval in
  yes) BOCCA_IO_FLAGS="$BOCCA_IO_FLAGS -D_BOCCA_BOOST"
  ;;
  *)
  ;;
esac
AC_ARG_ENABLE(ctor-messages,
	[  --enable-ctor-messages          Turn on bocca informational printing from some ctor, dtor.],
	, [ enableval=no ])
case $enableval in
  yes) BOCCA_IO_FLAGS="$BOCCA_IO_FLAGS -D_BOCCA_CTOR_PRINT"
  ;;
  *)
  ;;
esac

all_boccafiles="make.project buildutils/make.vars.common utils/run-gui.sh utils/bocca-gui-backend.sh utils/__tcejorp__-config utils/config-data"

AC_SUBST(CCAFE_CONFIG)
AC_SUBST(CCASPEC_GENCCAXML)
AC_SUBST(LANGUAGES)
AC_SUBST(PREFIX)
AC_SUBST(EXTRA_PYTHON_LIBS)
AC_SUBST(MAKE_OPTS)
AC_SUBST(SET_MAKE)
AC_SUBST(PROJECT_NAME)
AC_SUBST(PROJECT_TOP_DIR)
AC_SUBST(BOCCA)
AC_SUBST(BOCCA_IO_FLAGS)
AC_SUBST(BPACKAGE_TARNAME)

#--------------------------------------------------------------------
# User configure checks. Begin.
#--------------------------------------------------------------------
#--------------------------------------------------------------------
# Here put checks for external package paths, etc.
#
# Output variable destinations (add to make.project.in):

# make.project (global)
#	Add variables for global external dependencies (like the prefix at
#	which another package used by all components is installed) to
#	make.project.in.
#	Then, in components/make.vars.user, define the components_ variables
#	derived from the configure variable.
#
# make.project (per component)
#	Add variables specific to a single component (e.g. pkgX.compY)
#	by defining global make variables such as 
#	EXTRA_PREFIX_pkgX.compY and then assigning from them in 
#	make.vars.user in the individual component directory, eg.
#	components/pkgX.compY/make.vars.user:
#		LIBS=$(EXTRA_LIBS_pkgX.compY)
#		INCLUDES=$(EXTRA_INCLUDES_pkgX.compY)
#
# Note:
#	If bocca also needs to be informed of the value because you 
#	use bocca for ongoing development/deployment of your project, 
#	make the calls to bocca config at this time also. Typically,
#	bocca needs to be informed when the external dependency 
#	includes needed include paths, lib paths, or SIDL. E.g:
#		FIXME need to put example here.
#--------------------------------------------------------------------

# insert user-autoconf-here

#--------------------------------------------------------------------
# User configure checks. End.
#--------------------------------------------------------------------


AC_CONFIG_HEADERS([utils/__tcejorp__-config.h])

AC_CONFIG_FILES($all_boccafiles $user_files)

AC_CONFIG_COMMANDS([outmsg],
[ chmod a+x utils/run-gui.sh utils/bocca-gui-backend.sh; $BOCCA_CONFIG_UPDATE ],
[ chmod +x utils/run-gui.sh utils/bocca-gui-backend.sh; $BOCCA_CONFIG_UPDATE]
)

dnl this goes last, per autoconf doc, or accconfigcommands don't get run.
AC_OUTPUT
