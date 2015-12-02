dnl gnu make and version check:

AC_DEFUN( [CHECK_GNU_MAKE], 
	[ AC_CACHE_CHECK( for GNU make,_cv_gnu_make_command,
                _cv_gnu_make_command='' ;
dnl Search all the common names for GNU make
                for a in "$MAKE" make gmake gnumake ; do
                        if test -z "$a" ; then continue ; fi ;
[                       if  ( sh -c "$a --version" 2> /dev/null | grep GNU 2>&1 > /dev/null ) ;  then
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
]
        ) ;
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


dnl    CCAFE_PATH_TO_FILE(VARIABLE, TEST_FILES, PATH, 
dnl	 [ RUN_IF_FOUND, [RUN_IF_NOT_FOUND)

dnl    Test for the presence of file(s) (TEST_FILES) in the given colon
dnl    separated list of directory paths (PATH).  If all of the files for a
dnl    given path element are present, it sets VARIABLE to the matching PATH
dnl    element and calls AC_SUBST on it.  The files appear in TEST_FILES as a
dnl    space separated list.  The last two arguments are run if a path to the
dnl    files is found or not found respectively.
AC_DEFUN(CCAFE_PATH_TO_FILE,
[
var="$1"
testFiles="$2"
path="$3"

result=_searching
paths=`echo $path|tr ":" " "`
for chome in $paths ; do
    for testFile in $testFiles ; do
	    if ! test -f $chome/$testFile ; then
		    result=_searching
		    break
	    fi	
	    result=$chome	
    done
    if test "$result" = "$chome" ; then
	    $1=$result
	    if test -n '$4' ; then
		# if found
		  $4 
	    fi
	    echo "       found: $result"
	    break;
    fi
done
if test "$result" = _searching ; then
	if test -n '$5' ; then
	      #if not found
		$5
	fi
fi
]
)

dnl
dnl CCAFE_ENV_CHECK( VAR, [MESSAGE-IF-FOUND], [MESSAGE-IF-NOT-FOUND] )
dnl checks that VARNAME is or isn't defined.
dnl When no MESSAGE-IFs are supplied, defaults to printing yes/no.
dnl Side-effects: none, other than message output.
dnl internally used variables are all prefixed cec_.
dnl Internal variables (less prefix):
dnl yes, no, var_eval, var_val, empty_eval, empty_test, there.
dnl on normal completion: 
dnl cec_there == 1 if the variable is set (includes empty value)
dnl cec_there == 0 if not set.
dnl Bugs: 
dnl This macro would be 3 lines if we could assume bash syntax is portable.
dnl It even works when checking for environment variables with the
dnl value cec_not_there.
AC_DEFUN(CCAFE_ENV_CHECK,
[
	if test -z "$1"  ; then
		AC_MSG_RESULT(CCAFE env_check called with empty VAR argument)
	else
		AC_MSG_CHECKING(environment for $1)
# build a line which echos the name in $1
# get the value of that var
		cec_var_eval="echo $"`echo $1`
		cec_var_val=`eval $cec_var_eval`
		if test -z "$cec_var_val" ; then
# either its there, not there or 0 len
# 0 len may be meaningful so we need to distinguish.
# at this point we don't need to worry about overwriting its value
# temporarily since it's at most empty.
			cec_empty_eval="echo \${"`echo $1`"-cec_not_there}"
			cec_empty_test=`eval $cec_empty_eval`
			if test "X$cec_empty_test" = "Xcec_not_there" ; then
				cec_there=0
			else
				cec_there=1
			fi
		else
			cec_there=1
		fi
		cec_yes=yes
		cec_no=no
		ifelse([$2], , : , [cec_yes="$2"])
		ifelse([$3], , : , [cec_no="$3"])
		if test $cec_there -eq 1 ; then
			AC_MSG_RESULT($cec_yes)
		else
			AC_MSG_RESULT($cec_no)
		fi
	fi
]
)

#------------------------------------------------------------------------------
#  see if the user gave us the location of clueful make
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_PROG_GMAKE,
[
AC_ARG_WITH(gmake, 
    [Location of gmake:
  --with-gmake=EXECUTABLE
                          The location of gmake.  Give the full path:
                              --with-gmake='/share/bizarre/bin/gmake' ] ,
    , [with_gmake=yes])

case "$with_gmake" in
    no)
        ccatut_have_gmake=no
        ;;
    yes)
        #  User didn't give the option or didn't give useful
       #  information, search for it ourselves
        with_gmake=_searching
        ;;
    *)
        #  Only the library was specified
        GMAKE="$with_gmake"
        ;;
esac

if test "$with_gmake" = _searching ; then
    AC_CHECK_PROG(gmake_1, gmake, gmake, NONE)
    if test ! "$gmake_1" = NONE ; then
        GMAKE="$gmake_1"
    fi
fi
AC_SUBST(GMAKE)
]
)

AC_DEFUN(CCATUT_PROG_JAVA,
[
# jdk for java2/swing
ccatut_java_dirs="
    $JAVA_HOME
    $JAVA_HM
    /usr/local/jdk1.2.2
    $HOME/jdk1.2.2
    /usr/local/jdk
    /opt/local/jdk1.2.2
    /opt/local/jdk
    $prefix/jdk1.2.2
    $prefix/jdk
"

# java_home

if test "$target_os" = "macosx" ; then
    # MacOSX comes with complete Java package installed
    AC_PATH_PROG(JAVA_HM, javac, , /usr/bin)
    JAVA_HM="/usr"
else
    AC_ARG_WITH(jdk12,
        [Location of jdk 1.2. Give the full path:
      --with-jdk12=JAVA_HOME] , , [with_jdk12=_searching])
    case "$with_jdk12" in
	no)
	    AC_MSG_WARN([Option '--without-jdk12' may result in reduced functionality.])
	    ;;
	yes)
	    with_jdk12=_searching
	    ;;
	*)
	    JAVA_HM="$with_jdk12"
	    ;;
    esac

    if test "$with_jdk12" = _searching ; then
        AC_MSG_RESULT([Searching for jdk 1.2 or later])
        for jhome in $ccatut_java_dirs ; do
            AC_PATH_PROG(JAVA_HM, javac, , $jhome/bin)
            if test ! -z "$JAVA_HM" ; then
                AC_MSG_RESULT([Found $JAVA_HM.])
                break
            fi
        done
    else
        AC_PATH_PROG(JAVA_HM, javac, , $with_jdk12/bin)
    fi
    if test -z "$JAVA_HM" ; then
	AC_MSG_RESULT([Cannot find jdk 1.2 or later.])
        AC_MSG_WARN([Without jdk 1.2, functionality may be reduced.  You may
	want to re-run configure with a --with-jdk12=JAVA_HOME option.])
    fi
    # find the jni header to get version
    jhome=`echo $JAVA_HM | sed 's/\/javac$//' | sed 's/\/bin$//'`
    java_header_file=$jhome/include/jni.h
    jni_h_version=`grep JDK1_2 $java_header_file | sed 's/#define //'`
    # or we could attempt 
    # version=`$JAVA_HM -version 2>&1 |grep \"1.2 | sed 's/java version "//' |sed 's/"//'`

    # check for java2-ness
    AC_EGREP_HEADER(JDK1_2, $java_header_file, [ JAVA_HM=$jhome], [ JAVA_HM=no_java_found ])
    if test ! "X$jni_h_version" = "XJDK1_2" ; then
        AC_MSG_ERROR([JDK {$jhome} is the wrong version, apparently.
                      Use --with-jdk12=JAVA_HOME for a jdk1.2 or compatible version,])
    fi
    JAVA_HM=$jhome
fi
AC_SUBST(JAVA_HM)
]
)


dnl CCAFE_AC_PREFIX(DEFAULT)
dnl *************************** out of date wrt ac 2.6x... ******************
dnl *************************** out of date wrt ac 2.6x... ******************
dnl *************************** out of date wrt ac 2.6x... ******************
dnl --------------------------------------------------------------------
dnl Side effects: updates all the prefix related variables using
dnl DEFAULT if prefix has not been properly defined by now.
dnl fully expands the values, too.
dnl --------------------------------------------------------------------
AC_DEFUN(CCAFE_AC_PREFIX,
[
  if test -z "$1" ; then
    AC_MSG_ERROR([Ccafe_ac_prefix macro requires a default path.])
  fi
  if test -z "$prefix" -o "$prefix" = "NONE"; then
    prefix=$1;
  fi
  if test -z "$datadir" -o "$datadir" = "NONE/share" -o "$datadir" = '${prefix}/share' ; then
    datadir="$prefix/share";
  fi
  if test -z "$sysconfdir" -o "$sysconfdir" = "NONE/etc" -o "$sysconfdir" = '${prefix}/etc' ; then
    sysconfdir="$prefix/etc";
  fi
  if test -z "$sharedstatedir" -o "$sharedstatedir" = "NONE/com" -o "$sharedstatedir" = '${prefix}/com' ; then
    sharedstatedir="$prefix/com";
  fi
  if test -z "$localstatedir" -o "$localstatedir" = "NONE/var" -o "$localstatedir" = '${prefix}/var' ; then
    localstatedir="$prefix/var";
  fi
  if test -z "$includedir" -o "$includedir" = "NONE/include" -o "$includedir" = '${prefix}/include' ; then
    includedir="$prefix/include";
  fi
  if test -z "$infodir" -o "$infodir" = "NONE/info" -o "$infodir" = '${prefix}/info' ; then
    infodir="$prefix/info";
  fi
  if test -z "$mandir" -o "$mandir" = "NONE/man" -o "$mandir" = '${prefix}/man' ; then
    mandir="$prefix/man";
  fi
]
)

dnl --------------------------------------------------------------------
dnl requires prefix be define, or does nothing.
dnl --------------------------------------------------------------------
AC_DEFUN(CCAFE_AC_EXEC_PREFIX,
[
  if test -z "$1" ; then
    AC_MSG_ERROR([Ccafe_ac_exec_prefix macro requires a default path.])
  fi
  if test -z "$exec_prefix" -o "$exec_prefix" = "NONE"; then
     exec_prefix=$1;
  fi
  if test -z "$bindir" -o "$bindir" = "NONE/bin" -o "$bindir" = '${exec_prefix}/bin' ; then
    bindir="$exec_prefix/bin";
  fi
  if test -z "$sbindir" -o "$sbindir" = "NONE/sbin" -o "$sbindir" = '${exec_prefix}/sbin'; then
    sbindir="$exec_prefix/sbin";
  fi
  if test -z "$libexecdir" -o "$libexecdir" = "NONE/libexec" -o "$libexecdir" = '${exec_prefix}/libexec' ; then
    libexecdir="$exec_prefix/libexec";
  fi
  if test -z "$libdir" -o "$libdir" = "NONE/lib" -o "$libdir" = '${exec_prefix}/lib' ; then
    libdir="$exec_prefix/lib";
  fi
]
)


dnl CCAFE_CONFIG_ARGS(VAR)
dnl --------------------------------------------------------------------
dnl capture the ./configure arguments in VAR.
dnl --------------------------------------------------------------------
AC_DEFUN(CCAFE_CONFIG_ARGS,
[
  if test -z "$1" ; then
    AC_MSG_ERROR([Ccafe_config_args macro requires a variable name.])
  fi
  $1=[$]*
]
)



dnl    BABEL_CONFIG_VER(VARIABLE, BINVAR, PATH, TEST_FILE,
dnl      [ RUN_IF_FOUND], [RUN_IF_NOT_FOUND])
dnl    Test for the presence of file(s) (TEST_FILE) in the given colon
dnl    separated list of directory paths (PATH).  If all the file 
dnl    is found, it sets VARIABLE to the matching PATH element and
dnl    BINVAR to script found.
dnl    The last two arguments are run if a path to the
dnl    files is found or not found respectively.
dnl Side effects:
dnl   If variable BABEL_CONFIG is predefined to contain
dnl   the name of an appropriate executable, then we get
dnl   that as BINVAR and its root as VARIABLE.

AC_DEFUN(BABEL_CONFIG_VER,
[

  
dnl AC_MSG_RESULT([entering babel_path_to_config_ver])
p2cv_var="$1"
p2cv_binvar="$2"
p2cv_path="$3"
p2cv_testFile="$4"
p2cv_config="no"
p2cv_ok=no

if test "x$BABEL_CONFIG" != "x" ; then
  if test -x $BABEL_CONFIG ; then
    p2cv_config=$BABEL_CONFIG
    p2cv_path=`$BABEL_CONFIG --query-var=prefix`
    p2cv_result=$p2cv_path
    $1=$p2cv_result
    $2=$p2cv_config
    p2cv_ok=yes
    if test -n '$5' ; then
      # if found
      $5 
    fi
dnl    AC_MSG_RESULT([found $BABEL_CONFIG])
  else
    AC_MSG_WARN([Ignoring env BABEL_CONFIG pointing to non-executable $BABEL_CONFIG.])
  fi
fi

if test "$p2cv_ok" = "no" ; then

  p2cv_tmpfile=`pwd`/.p2cv_tmpfile

  # for path elements
  # if ! element/testfile exists, res=search
  # for file-* w/ver number, try highest number
  # and work down. ver must end in a digit

  p2cv_result=_searching
  p2cv_paths=`echo $p2cv_path|tr ":" " "`
  for chome in $p2cv_paths ; do
dnl    AC_MSG_RESULT([trying $chome])
    if test -x $chome/$p2cv_testFile ; then
        p2cv_result=$chome
        p2cv_config=$chome/$p2cv_testFile
        $1=$p2cv_result
        $2=$p2cv_config
        if test -n '$5' ; then
            # if found
              $5 
        fi
dnl        AC_MSG_RESULT([found basenamed file])
        break
    fi  

    if test -d $chome ; then
        pushd $chome > /dev/null
        flist="${p2cv_testFile}*"
        popd > /dev/null
        /bin/rm -f $p2cv_tmpfile
        for fname in $flist ; do
          echo $fname >> $p2cv_tmpfile
        done
        flist=`cat $p2cv_tmpfile | sort -n -r`
        /bin/rm -f $p2cv_tmpfile
        for fname in $flist ; do
            if test -x $chome/$fname ; then
                p2cv_result=$chome
                p2cv_config=$chome/$fname
                $1=$p2cv_result
                $2=$p2cv_config
                if test -n '$5' ; then
                    # if found
                  $5 
                fi
dnl                AC_MSG_RESULT([       found: $p2cv_result/$fname])
                break;
            fi
        done
    fi
  done
  # not found anywhere
  if test "$p2cv_result" = _searching ; then
dnl    AC_MSG_RESULT([        nothing found])
    p2cv_result=no
    if test -n '$6' ; then
      #if not found
        $6
    fi
  fi
  # end of search for config with ver.

dnl end of p2cv_ok no test
fi
dnl AC_MSG_RESULT([leaving babel_path_to_config_ver])
]
)


dnl CCAFECONFIG
dnl input: none
dnl output:
dnl CCAFECONFIG- output variable set to the result found, or the empty string.
dnl HAVE_CCAFE- 1 if found, empty if not.
dnl Generates warning if no satisfactory result.
dnl
AC_DEFUN(CCAFECONFIG,
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

dnl CCASPECBABELCONFIG
dnl input: none
dnl output:
dnl CCASPECBABELCONFIG- output variable set to the result found, or the empty string.
dnl HAVE_CCASPECBABEL- 1 if found, empty if not.
dnl Generates warning if no satisfactory result.
dnl
AC_DEFUN(CCASPECBABELCONFIG,
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


dnl BABELCONFIG
dnl input: none
dnl output:
dnl BABELCONFIG- output variable set to the result found, or the empty string.
dnl HAVE_BABEL- 1 if found, empty if not.
dnl Generates error if no satisfactory result.
dnl
AC_DEFUN(BABELCONFIG,
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

dnl macro CCA_BUNDLE_TAG([SEARCHPATH])
dnl --------------------------------------------------------------------
dnl Cause the variable CCA_BUNDLE_VERSION defined by configure.
dnl The value set will be developer unless the file CCA_BUNDLE_RELEASE is found.
dnl The default search path is $ac_aux_dir:. 
dnl If a SEARCHPATH is given it will be checked, then the default.
dnl This macro should be used after AC_CONFIG_AUX_DIR.
dnl The value if the file is found will be the first line of the file up to
dnl but not including the first whitespace.
dnl Side effects:
dnl substitutes CCA_BUNDLE_VERSION
dnl --------------------------------------------------------------------
AC_DEFUN(CCA_BUNDLE_TAG,
[
AC_MSG_CHECKING([CCA_BUNDLE_RELEASE])
CCA_BUNDLE_VERSION=developer
cbr_searchpath="$1:$ac_aux_dir:$srcdir:."
cbr_paths=`echo $cbr_searchpath|tr ":" " "`
for rdir in $cbr_paths ; do
	if test -d $rdir; then
		f=$rdir/CCA_BUNDLE_RELEASE
		if test -f $f ; then
			CCA_BUNDLE_VERSION=`cat $f | sed q`
			for rword in $CCA_BUNDLE_VERSION ; do
				CCA_BUNDLE_VERSION=$rword
				break
			done
			break
		fi
		f=$rdir/RELEASE
		if test -f $f ; then
			CCA_BUNDLE_VERSION=`cat $f | sed q`
			for rword in $CCA_BUNDLE_VERSION ; do
				CCA_BUNDLE_VERSION=$rword
				break
			done
			break
		fi
	fi
done
AC_SUBST(CCA_BUNDLE_VERSION)
AC_MSG_RESULT([ $CCA_BUNDLE_VERSION])
]
)

AC_DEFUN(RUBYSHELL,
[
# ---------------------------------------------------------------------------
# Ruby installation
# ---------------------------------------------------------------------------
AC_ARG_VAR([RUBY],[Ruby shell used])
AC_ARG_WITH(ruby, 
    [Location of ruby:
	  --with-ruby=EXECUTABLE
		  The location of the ruby (or jruby) shell.
		  Give the full path: --with-ruby='/home/rob/bin/jruby' ],
    , [with_ruby=yes])

case "$with_ruby" in
	no)
		AC_MSG_WARN([Option '--without-ruby' given. Proceeding.])
	;;
	yes)
		#  User didn't give the option or didn't give useful
		#  information, search for it ourselves
		with_ruby=_searching
	;;
	*)
		RUBY="$with_ruby"
	;;
esac

if test "$with_ruby" = _searching ; then
	AC_PATH_PROG(RUBY, ruby)
fi
HAVE_RUBY=1
if test -z "$RUBY"; then
	HAVE_RUBY=0
	AC_MSG_WARN([No ruby found or given causes some prototype scripts to be unusable.])
else 
	if test -d "$RUBY"; then
		AC_MSG_ERROR([$RUBY seems to be a directory.])
	fi
	if ! test -x "$RUBY"; then
		AC_MSG_ERROR([$RUBY is not executable.])
	fi
fi
AC_SUBST(HAVE_RUBY)

])

AC_DEFUN(PYTHONSHELL,
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

AC_DEFUN(JAVASHELL,
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

AC_DEFUN(MAKETUT05CONFIG,
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

AC_DEFUN(SUBST_DEPENDENCY_VARS,
[
# DEPENDENCY_VARS
BABEL_VERSION=`$BABEL_CONFIG --version`
if test "x$HAVE_CCASPECBABEL" = "x1"; then
CCASPEC_VERSION=`$CCA_SPEC_BABEL_CONFIG --var CCASPEC_VERSION`
CCASPEC_BABEL_VERSION=`$CCA_SPEC_BABEL_CONFIG --var CCASPEC_BABEL_VERSION`
CCASPEC_BABEL_BRANCH=`$CCA_SPEC_BABEL_CONFIG --var CCASPEC_BABEL_BRANCH`
CCASPEC_BABEL_BRANCH_MAJOR=`$CCA_SPEC_BABEL_CONFIG --var CCASPEC_BABEL_BRANCH_MAJOR`
CCASPEC_BABEL_BRANCH_MINOR=`$CCA_SPEC_BABEL_CONFIG --var CCASPEC_BABEL_BRANCH_MINOR`
CCASPEC_BABEL_BRANCH_PATCH=`$CCA_SPEC_BABEL_CONFIG --var CCASPEC_BABEL_BRANCH_PATCH`
CCASPEC_BABEL_SNAPSHOT=`$CCA_SPEC_BABEL_CONFIG --var CCASPEC_BABEL_SNAPSHOT`
else
CCASPEC_VERSION=0.0.0
CCASPEC_BABEL_VERSION=0.0.0
CCASPEC_BABEL_BRANCH=0
CCASPEC_BABEL_BRANCH_MAJOR=0
CCASPEC_BABEL_BRANCH_MINOR=0
CCASPEC_BABEL_BRANCH_PATCH=0
CCASPEC_BABEL_SNAPSHOT=0
fi

AC_SUBST(CCASPEC_VERSION)
AC_SUBST(BABEL_VERSION)
AC_SUBST(CCASPEC_BABEL_VERSION)
AC_SUBST(CCASPEC_BABEL_BRANCH)
AC_SUBST(CCASPEC_BABEL_BRANCH_MAJOR)
AC_SUBST(CCASPEC_BABEL_BRANCH_MINOR)
AC_SUBST(CCASPEC_BABEL_BRANCH_PATCH)
AC_SUBST(CCASPEC_BABEL_SNAPSHOT)
])
