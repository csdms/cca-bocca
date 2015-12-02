dnl CCASPECBABELCONFIG
dnl input: none
dnl output:
dnl CCASPECBABELCONFIG- output variable set to the result found, or the empty string.
dnl HAVE_CCASPECBABEL- 1 if found, empty if not.
dnl Generates warning if no satisfactory result.
dnl
AC_DEFUN([CCASPECBABELCONFIG],
[
AC_ARG_VAR([CCA_SPEC_BABEL_CONFIG],[
	CCA_SPEC_BABEL_CONFIG=/full/pathname/of/cca-spec-babel-config;
	We prefer --with-cca-spec-babel-config=/path/cca-spec-babel-config, but either works.])
AC_ARG_WITH(cca-spec-babel-config,
[
Location of cca-spec-babel-config program:
  --with-cca-spec-babel-config=/usr/local/bin/cca-spec-babel-config[version_number]
            Specify the particular babel config info script.
            This option overrides environment variable CCA_SPEC_BABEL_CONFIG.
] , , [with_cca_spec_babel_config=no])

# if not in env, define as dummy.
if test -z "$CCA_SPEC_BABEL_CONFIG"; then
	CCA_SPEC_BABEL_CONFIG=_search
fi

case "$with_cca_spec_babel_config" in
    no)
        ;;
    yes)
        with_cca_spec_babel_config="no"
        AC_MSG_ERROR([--with-cca-spec-babel-config must be given the path of the script.])
        ;;
    *)
        if test -d $with_cca_spec_babel_config ; then
          AC_MSG_ERROR([--with-cca-spec-babel-config must be given the path of the script, not a directory.])
        fi
        if ! test -x $with_cca_spec_babel_config ; then
          AC_MSG_ERROR([--with-cca-spec-babel-config=$with_cca_spec_babel_config: $with_cca_spec_babel_config not executable])
        fi
        CCA_SPEC_BABEL_CONFIG=$with_cca_spec_babel_config
	AC_MSG_NOTICE([Took user specified $CCA_SPEC_BABEL_CONFIG])
        ;;
esac

if test "x$CCA_SPEC_BABEL_CONFIG" = "x_search" ; then
	CCA_SPEC_BABEL_CONFIG=""
	AC_PATH_PROG([CCA_SPEC_BABEL_CONFIG],[cca-spec-babel-config]) 
fi

HAVE_CCASPECBABEL=1
if test -z "$CCA_SPEC_BABEL_CONFIG"; then
	AC_MSG_WARN([cca-spec-babel-config not found in path or specified with options.
	Most features will not be available, but babel-only projects can still be
	generated.])
	HAVE_CCASPECBABEL=0
else
	BABEL_CONFIG=`$CCA_SPEC_BABEL_CONFIG --var CCASPEC_BABEL_BABEL_CONFIG`
fi		

AC_SUBST(CCA_SPEC_BABEL_CONFIG)
AC_SUBST(HAVE_CCASPECBABEL)
])
