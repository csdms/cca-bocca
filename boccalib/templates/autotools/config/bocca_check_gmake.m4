dnl gnu make and version check:

AC_DEFUN([BOCCA_CHECK_GNU_MAKE], 
	[ AC_CACHE_CHECK( for GNU make,_cv_gnu_make_command, [
                _cv_gnu_make_command='' ;
dnl Search all the common names for GNU make
                for a in "$MAKE" make gmake gnumake ; do
                        if test -z "$a" ; then continue ; fi ;
                       if  ( sh -c "$a --version" 2> /dev/null | grep GNU 2>&1 > /dev/null ) ;  then
				b=`$a --version | grep GNU | sed -e 's/^[[A-Z,a-z ]]*//g'`
				case "$b" in
				3.6*) c="$a is a too old version of gnu make ($b)";
					continue;
				;;
				3.7*) c="$a is a too old version of gnu make ($b)";
					continue;
				;;
				*)
                                        _cv_gnu_make_command=$a ;
				;;
				esac
                                break;
                        fi
                done ;
]) ;
	dnl If there was a GNU version, then set @ifGNUmake@ to the empty string, '#' otherwise
        if test  "x$_cv_gnu_make_command" != "x"  ; then
                ifGNUmake='' ;
                ifnotGNUmake='#' ;
		if ! test "x$c" = "x"; then
			AC_MSG_WARN([Ignoring $c
Be sure to invoke the build using $_cv_gnu_make_command.
])
		fi
        else
                ifGNUmake='#' ;
                ifnotGNUmake='' ;
                AC_MSG_RESULT("Not found");
                if ! test "x$c" = "x"; then
			extramsg=$c
		fi
		AC_MSG_ERROR([GNU make must be used and must be later than 3.79. Try setting 
environment variable MAKE to a more current gnu make. $c])
        fi
        AC_SUBST(ifnotGNUmake)
        AC_SUBST(ifGNUmake)
] )

