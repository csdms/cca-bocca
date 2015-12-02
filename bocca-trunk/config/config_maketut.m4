AC_DEFUN([CONFIG_MAKETUT],
[
AC_PROG_MAKE_SET
# user cannot make install by default-- must configure.
PREFIX=""
# user gets all by default
LANGUAGES="`$BABEL_CONFIG --query-var=BABEL_SUPPORTED_LANGUAGES`"
# user gets 2 by default and we need a config switch later.
MAKE_OPTS="-j 2"
EXTRA_PYTHON_LIBS=""
AC_SUBST(PREFIX)
AC_SUBST(LANGUAGES)
AC_SUBST(MAKE_OPTS)
AC_SUBST(EXTRA_PYTHON_LIBS)
]
)
