AC_DEFUN([PYTHONSHELL],
[
# ---------------------------------------------------------------------------
# Python installation
# ---------------------------------------------------------------------------
AC_ARG_VAR([PYTHON],[Python shell used if not supported in the babel installed.])

# let user override babel python for our build (if they're nuts).
AC_ARG_WITH(python, 
    [Location of python:
	  --with-python=EXECUTABLE
		  The location of the python shell.
		  Give the full path: --with-python='/home/elwasif/bin/python' ],
    , [with_python=yes])

if test "$with_python" = "yes" -a "x$HAVE_BABEL" = "x1" ; then
	if $BABEL_CONFIG --with-python; then
		PYTHON=`$BABEL_CONFIG --which-var=PYTHON`
		with_python=$PYTHON
		AC_MSG_NOTICE([Took python from babel-config])
	fi
fi

case "$with_python" in
	no)
		AC_MSG_WARN([Option '--without-python' given. Proceeding.])
	;;
	yes)
		#  User didn't give the option or didn't give useful
		#  information, search for it ourselves
		with_python=_searching
	;;
	*)
		PYTHON="$with_python"
	;;
esac

if test "$with_python" = _searching ; then
	AC_PATH_PROG(PYTHON, python)
fi
HAVE_PYTHON=1
if test -z "$PYTHON"; then
	HAVE_PYTHON=0
	AC_MSG_ERROR([No python found or given causes bocca to be unusable.])
else 
	if test -d "$PYTHON"; then
		AC_MSG_ERROR([$PYTHON seems to be a directory.])
	fi
	if ! test -x "$PYTHON"; then
		AC_MSG_ERROR([$PYTHON is not executable.])
	fi
fi
AC_SUBST(HAVE_PYTHON)

])
