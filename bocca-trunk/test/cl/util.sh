#!/bin/bash
# Utility functions; to use, add 
#     source util.sh 
# in the beginning of your test script.
# B.N.

checkCmd() {
    # The first (required) argument is the type of failure, e.g., "FAIL", "XFAIL", "BROKEN"
    # The second (required) argument is the command
    # The third (optional) argument is the error message in case of failure
    # The fourth (optional) argument is a list of files which should exist upon successful completion of command.
    fail=$1
    cmd=$2
    if [ "x$3" != "x" ]; then
        msg=": $3"
    else
        msg=""
    fi
    files=""
    if [ "x$4" != "x" ]; then 
        files=$4
    fi
    echo "CHECKING $cmd"
    msg=`$cmd`
    errcode=$?
    if [ "$errcode" != "0" ]; then
        echo "$fail($errcode)$msg."
	if [ "$fail" = "XFAIL" ]; then return 0; fi
        exit 1
    else
        for f in $files; do
        	# When a file path begins with "!", check for non-existence, otherwise check for existence
        	if test "${f:0:1}" = "!" ; then 
        		if test -e "${f:1}" ; then 
        			echo "$fail($errcode): file ${f:1} not renamed/removed."
 	        		if test "$fail" = "XFAIL" ; then return 0; fi
                	exit 1
        		fi
            elif ! test -e "$f" ; then 
                echo "$fail($errcode): file $f not created."
	        	if test "$fail" = "XFAIL" ; then return 0; fi
                exit 1
            fi
        done
        echo "successful."
        return 0
    fi
}

# Shortcut to create a bocca interface, port, class, or component
create() {
    # The first (required) argument is the kind of SIDL symbol
    # The second (required) argument is fully qualified SIDL symbol name
    # The third (optional) argument is any optional arguments to be passed to bocca verbatim
    sidlthingy=$1
    sidlname=$2
	extraargs=$3
    if test "$sidlthingy" = "component" -o "$sidlthingy" = "class" ; then 
		sdir=components
	else
		sdir=ports
    fi
	checkCmd "FAIL" "$BOCCA create $sidlthingy $sidlname $extraargs" "could not create $sidlthingy $sidlname" "$sdir/sidl/$sidlname.sidl"
}

# Shortcut to add a method to an interface, port, class, or component sidl file
merge() {
    # The first (required) argument is the kind of SIDL symbol
    # The second (required) argument is fully qualified SIDL symbol name
    # The third (required) argument is the method name
    sidlthingy=$1
    sidlname=$2
	method=$3

cat << EOF > splice
        // DO-NOT-DELETE bocca.splicer.begin($sidlname.methods)
        $method
        // DO-NOT-DELETE bocca.splicer.end($sidlname.methods)
EOF
	$BMERGE -A 'DO-NOT-DELETE bocca.splicer' -B 'DO-NOT-DELETE bocca.splicer' --from=splice --to=$sdir/sidl/$sidlname.sidl
	if ! test $? ; then
  		echo "merge failed"
  		echo "FAIL"
  		exit 1
	fi
}
