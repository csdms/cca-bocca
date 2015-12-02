dnl BABELCONFIG
dnl input: none
dnl output:
dnl BABELCONFIG- output variable set to the result found, or the empty string.
dnl HAVE_BABEL- 1 if found, empty if not.
dnl Generates error if no satisfactory result.
dnl
AC_DEFUN([BABELCONFIG],
[
AC_ARG_VAR([BABEL_CONFIG],[
	BABEL_CONFIG=/full/pathname/of/babel-config;
	We prefer --with-babel-config=/path/babel-config, but either works.])
AC_ARG_WITH(babel-config,
[
Location of babel-config program:
  --with-babel-config=/usr/local/bin/babel-config[version_number]
            Specify the particular babel config info script.
            This option overrides environment variable BABEL_CONFIG.
] , , [with_babel_config=no])

# if not in env, define as dummy.
if test -z "$BABEL_CONFIG"; then
	BABEL_CONFIG=_search
fi

case "$with_babel_config" in
    no)
        ;;
    yes)
        with_babel_config="no"
        AC_MSG_ERROR([--with-babel-config must be given the path of the script.])
        ;;
    *)
        if test -d $with_babel_config ; then
          AC_MSG_ERROR([--with-babel-config must be given the path of the script, not a directory.])
        fi
        if ! test -x $with_babel_config ; then
          AC_MSG_ERROR([--with-babel-config=$with_babel_config: $with_babel_config not executable])
        fi
        BABEL_CONFIG=$with_babel_config
	AC_MSG_NOTICE([Took user specified $BABEL_CONFIG])
        ;;
esac

if test "x$BABEL_CONFIG" = "x_search" ; then
	BABEL_CONFIG=""
	AC_PATH_PROG([BABEL_CONFIG],[babel-config]) 
fi

if test -z "$BABEL_CONFIG"; then
	AC_MSG_ERROR([babel-config not found in path or specified with options.
	Try  --with-babel-config=/path/to/babel-config.])
else
	if test -d $BABEL_CONFIG ; then
		AC_MSG_ERROR([$BABEL_CONFIG appears to be a directory. It must be a program.])
	fi
	if ! test -x $BABEL_CONFIG ; then
		AC_MSG_ERROR([$BABEL_CONFIG must be executable.])
	fi
fi
HAVE_BABEL=1
AC_SUBST(HAVE_BABEL)

]
)
