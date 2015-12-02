#!/bin/bash
		
ulangs=$1
blangs=$2
langs="" 
for i in $ulangs; do 
	for j in $blangs; do 
		if test "x$i" = "x$j" ; then 
			langs="$langs $i"; 
			if test "x$j" = "xcxx"; then
				langs="$langs"; 
			fi;
			if test "x$j" = "xf77"; then
				:
				# langs="$langs f77_31"; 
			fi;
		fi; 
	done; 
done; 
echo $langs
