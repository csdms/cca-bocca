#!/bin/sh
# in-project help test
cd $2
rm -rf help3
mkdir help3
cd help3
x=$?
if ! test "$x" = "0"; then
        echo "changing to scratch directory $2 failed"
        echo "BROKEN"
        exit 1
fi
msg=`$1 create project myproj`
if ! test -d "$2/help3/myproj/BOCCA"; then
        echo "missing myproj/BOCCA"
        echo "FAIL"
        exit 1
fi
cd myproj
actions="help create change display remove rename fakeVerb"
subjects="fakeNoun project package interface port sidlclass component application"
# TODO: update those as new features are added
xfailpairs="change_project remove_project remove_package rename_package remove_sidlclass remove_component"

echo "CHECKING $1 help for i in $subjects"

err=0
badsubs=""
badacts=""
for i in $subjects; do
	echo "SUBJECT  $i: ******************************************* "
	$1 help $i
	x=$?
	if test "$x" = "0"; then
		echo "$1 help $i RETURNED ($x)"
		for a in $actions; do
			echo "CHECKING ACTION $i $a: ----------------"
			echo "INVOCATION: $1 $a $i --help"
			$1 $a $i --help
			y=$?
			if test "$y" = "0"; then
				echo "successful."
			else
				if test "$i" = "fakeNoun"; then
					echo "Correctly found error on fakeNoun."
					continue
				fi
				if test "$a" = "fakeVerb"; then
					echo "Correctly found error on fakeVerb."
				else
					xfail=0
					for xf in $xfailpairs; do
						if test "$xf" = "${a}_$i"; then xfail=1; break; fi
					done
					if test "$xfail" = "1"; then 
						echo "XFAIL($y): help missing for $a $i"
					else
						echo "FAIL($y): help missing for $a $i"
					fi
					err=1
					badacts="$badacts ${a}_$i"
				fi
			fi
		done
	else
		if  test "x$i" = "xfakeNoun"; then
			echo "Correctly found error on fakeNoun."
		else
			echo "FAIL($x): help found MISSING($?) subject $i"
			badsubs="$badsubs $i"
			err=1
		fi
	fi
done

if test "$err" = "0"; then
	echo PASS
	exit 0
else
	echo "help system reported error???"
	echo "FAIL"
	for i in $badsubs; do
		echo "bad subject (missing module?): $i"
	done
	for i in $badacts; do
		echo "bad action_subcommand: $i"
	done
	exit 1
fi
