dnl CCAFECONFIG
dnl input: none
dnl output:
dnl CCAFECONFIG- output variable set to the result found, or the empty string.
dnl HAVE_CCAFE- 1 if found, empty if not.
dnl Generates warning if no satisfactory result.
dnl
AC_DEFUN([CCAFECONFIG],
[
AC_ARG_VAR([CCAFE_CONFIG],[
	CCAFE_CONFIG=/full/pathname/of/ccafe-config;
	We prefer --with-ccafe-config=/path/ccafe-config, but either works.])
AC_ARG_WITH(ccafe-config,
[
Location of ccafe-config program:
  --with-ccafe-config=/usr/local/bin/ccafe-config[version_number]
            Specify the particular babel config info script.
            This option overrides environment variable CCAFE_CONFIG.
] , , [with_ccafe_config=no])

# if not in env, define as dummy.
if test -z "$CCAFE_CONFIG"; then
	CCAFE_CONFIG=_search
fi

case "$with_ccafe_config" in
    no)
        ;;
    yes)
        with_ccafe_config="no"
        AC_MSG_ERROR([--with-ccafe-config must be given the path of the script.])
        ;;
    *)
        if test -d $with_ccafe_config ; then
          AC_MSG_ERROR([--with-ccafe-config must be given the path of the script, not a directory.])
        fi
        if ! test -x $with_ccafe_config ; then
          AC_MSG_ERROR([--with-ccafe-config=$with_ccafe_config: $with_ccafe_config not executable])
        fi
        CCAFE_CONFIG=$with_ccafe_config
	AC_MSG_NOTICE([Took user specified $CCAFE_CONFIG])
        ;;
esac

if test "x$CCAFE_CONFIG" = "x_search" ; then
	CCAFE_CONFIG=""
	AC_PATH_PROG([CCAFE_CONFIG],[ccafe-config]) 
fi

HAVE_CCAFE=1
if test -z "$CCAFE_CONFIG"; then
	AC_MSG_WARN([ccafe-config not found in path or specified with options.
	Some convenience defaults will not be available, but projects can still be
	generated.])
	HAVE_CCAFE=0
else
	CCA_SPEC_BABEL_CONFIG=`$CCAFE_CONFIG --var CCAFE_CCA_SPEC_BABEL_CONFIG`
	if test "x$CCA_SPEC_BABEL_CONFIG" = "x"; then
		AC_MSG_WARN([ccafe-config not found in path or specified with options.
	Some convenience defaults will not be available, but projects can still be
	generated.])
	else
		BABEL_CONFIG=`$CCA_SPEC_BABEL_CONFIG --var CCASPEC_BABEL_BABEL_CONFIG`
	fi
fi		

AC_SUBST(CCAFE_CONFIG)
AC_SUBST(HAVE_CCAFE)

])
