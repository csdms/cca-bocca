AC_DEFUN([JAVASHELL],
[
# ---------------------------------------------------------------------------
# Java installation
# ---------------------------------------------------------------------------
JAVACOMP=0
AC_ARG_VAR([JAVA],[Java used if not supported in the babel installed.])
AC_ARG_VAR([JAVAC],[Javac used if not supported in the babel installed.])
# let user override babel java for our build (if they're nuts).
AC_ARG_WITH(java, 
    [Location of java:
	  --with-java=EXECUTABLE
		  The location of java.
		  Give the full path: --with-java='/home/norris/bin/java' ],
    , [with_java=yes])

if test "$with_java" = "yes" -a "x$HAVE_BABEL" = "x1" ; then
	JAVA=`$BABEL_CONFIG --which-var=JAVA`
	JAVAC=`$BABEL_CONFIG --which-var=JAVAC`
	$BABEL_CONFIG --with-java
	x=$?
	AC_MSG_NOTICE([Took java and javac values from babel-config])
	if test "x$x" = "x0"; then
		JAVACOMP=1
	else
		AC_MSG_NOTICE([This babel installation does not support java components.])
	fi
	with_java="frombabel"
fi

case "$with_java" in
	no)
		AC_MSG_WARN([Option '--without-java' given. Proceeding.])
	;;
	yes)
		#  User didn't give the option or didn't give useful
		#  information, search for it ourselves
		with_java=_searching
	;;
	frombabel)
		: ; # user didn't override the babel values.
	;;
	*)
		JAVA="$with_java"
		JAVAC="$with_java"c
	;;
esac

if test -z "$JAVA"; then
	if test "$with_java" = _searching ; then
		AC_PATH_PROG(JAVA, java)
		AC_PATH_PROG(JAVAC, javac)
	fi
fi

HAVE_JAVA=1
if test -z "$JAVA"; then
	HAVE_JAVA=0
	AC_MSG_WARN([No java found or given causes some prototype scripts to be unusable.])
else 
	if test -d "$JAVA"; then
		AC_MSG_ERROR([$JAVA seems to be a directory.])
	fi
	if ! test -x "$JAVA"; then
		AC_MSG_ERROR([$JAVA is not executable.])
	fi
fi
AC_SUBST(HAVE_JAVA)

])
