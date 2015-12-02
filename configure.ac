#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.
# It's very simple because babel does all the real work for
# discovering system-dependent things that matter.
# All we really need to discover in this file is:
# .) a path to the babel install which 
#    ** need not exist at the time this is built, so
#	long as you don't want to run 'make check'. **
# The babel install needs only exist at user runtime and can be
# specified (overridden) by the user if they are the env-var setting kind
# of user.
# .) a path to python
# .) temporarily a path to ruby
# .) eventually a path to java

AC_INIT(bocca, 0.5.7, bocca-dev@cca-forum.org)

BOCCA_VERSION=$PACKAGE_VERSION
BOCCA_RELEASE=DeadHorse  # Arkansas


AC_CONFIG_AUX_DIR([config])

AC_PREREQ(2.60)
AC_PREFIX_DEFAULT([`pwd`/install])

AC_ARG_VAR([ENV_VAR_LIKE_OPTIONS],[
	./configure VAR=VALUE {other options}
	This syntax lets us define or override environment variables seen 
	while configure runs. --with switches typically override VAR=VALUE.
])
AC_ARG_VAR([NOTE],[ 'VAR=VALUE ./configure ...' is NOT supported.  ])
AC_CONFIG_SRCDIR([scripts/bocca])
CHECK_GNU_MAKE
AC_PROG_INSTALL
CCA_BUNDLE_TAG
AC_SUBST(CCA_BUNDLE_VERSION)
AC_SUBST(BOCCA_VERSION)
AC_SUBST(BOCCA_RELEASE)

# Checks for programs.
# Here is the algorithm:
# Check for babel-config, babel.
#	If babel-config found, use it's java, cc, cxx, shell.
#	Else
#	Check independently for
#		cxx
#		ruby
#		java
#
# Remember: All this configure and build must do is build some
# tools and install them, not run them. Complex checks are run on
# the *installation*.

# Check for ccafe here. Not used in our own build, but in scripts we install.
CCAFECONFIG

# Check for spec here. Not used in our own build, but in scripts we install.
CCASPECBABELCONFIG

# Check for babel here. Not used in our own build, but in scripts we install.
# if ccafeconfig or CCASPECBABELCONFIG found ccafe or the spec, it probably found that babel.
BABELCONFIG

# optional python
# This is the BOCCA python, the babel python may be different-- query
# babel-config when you want babel's.
PYTHONSHELL

dnl ruby no longer in use
dnl # optional ruby
dnl # RUBYSHELL

# optional java
# This is the BOCCA java, the babel python may be different-- query
# babel-config when you want babel's.
JAVASHELL

# things to compute for the tut template make.project default.
CONFIG_MAKETUT

# svn executable (optional) for updating version info during make install
BOCCA_CHECK_SVN

SUBST_DEPENDENCY_VARS

# Checks for header files.
# may eventually choose to depend on boost.

AC_CONFIG_FILES([
varlist
Makefile 
test/cl/Makefile
test/cca/Makefile
boccalib/acboccavars.py
boccalib/templates/project.defaults
boccalib/templates/gmake/make.project
boccalib/templates/gmake/buildutils/make.vars.common
boccalib/templates/gmake/utils/run-gui.sh
boccalib/templates/gmake/utils/bocca-gui-backend.sh
])

AC_CONFIG_COMMANDS([outmsg],
[
echo "Paths:"
echo CCAFE_CONFIG=$CCAFE_CONFIG
echo CCA_SPEC_BABEL_CONFIG=$CCA_SPEC_BABEL_CONFIG
echo BABEL_CONFIG=$BABEL_CONFIG
echo PYTHON=$PYTHON
echo JAVA=$JAVA
echo "---- Features: ---- "
echo HAVE_CCASPECBABEL=$HAVE_CCASPECBABEL
echo HAVE_CCAFE=$HAVE_CCAFE
echo HAVE_BABEL=$HAVE_BABEL
echo HAVE_PYTHON=$HAVE_PYTHON
echo HAVE_JAVA=$HAVE_JAVA
if test "x$JAVACOMP" = "x0"; then
	echo "Java components not supported by this babel installation."
fi
],[
HAVE_BABEL=$HAVE_BABEL
HAVE_CCASPECBABEL=$HAVE_CCASPECBABEL
HAVE_CCAFE=$HAVE_CCAFE
HAVE_JAVA=$HAVE_JAVA
HAVE_PYTHON=$HAVE_PYTHON
CCA_SPEC_BABEL_CONFIG=$CCA_SPEC_BABEL_CONFIG
BABEL_CONFIG=$BABEL_CONFIG
CCAFE_CONFIG=$CCAFE_CONFIG
PYTHON=$PYTHON
JAVA=$JAVA
JAVAC=$JAVAC
JAVACOMP=$JAVACOMP
]
)

AC_OUTPUT
