dnl Support routines for ConArtist
dnl
dnl BOCCA_CHECK_SVN()
dnl
AC_DEFUN([BOCCA_CHECK_SVN],[
  AC_MSG_CHECKING([Subversion exectuable (svn)])
  AC_ARG_WITH(svn,
    [  --with-svn              Specify location of subversion install (optional)] ,
    [  SVN_=$withval ]
  )
  SVN_EXECUTABLE=""

  if test "x$SVN_" = "x"; then
    svn_places="/usr/local /usr"
    for place in $svn_places; do
      if test -d $place; then
        if test -x "$place/bin/svn"; then 
           SVN_EXECUTABLE="$place/bin/svn"
           break
        fi
      fi
    done
  else
    if test -x "$SVN_/bin/svn"; then 
       SVN_EXECUTABLE="$SVN_/bin/svn"
    fi
  fi

  if test "x$SVN_EXECUTABLE" = "x" ; then
    AC_MSG_RESULT([Could not find svn (that's ok).])
  else
    AC_MSG_RESULT([$SVN_EXECUTABLE])
  fi
  AC_SUBST(SVN_EXECUTABLE)
])

