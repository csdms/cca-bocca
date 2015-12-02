#!/bin/bash
		
# This script combines babel.make files (that use component-specific prefixes, 
# see documentation for the -m option to babel) into one file, babel.make.all.
# The script should be invoked in the directory where the impls reside.
# Currently C, C++, and Fortran client and server are supported.

BABEL_MAKE_ALL=babel.make.all

rm -f ${BABEL_MAKE_ALL}

if test "xx$1" != "xx" ; then
	searchdir=$1
else
	searchdir=.
fi

srcKinds=(IORSRCS STUBSRCS SKELSRCS IMPLSRCS IMPLMODULESRCS TYPEMODULESRCS STUBMODULESRCS ARRAYMODULESRCS PYMOD_SRCS PYTHONADMIN PYTHONSRC LAUNCHSRCS)

babelMakeFiles=`find $searchdir -name ".*babel.make" -print | sed -e 's|^./||'`
touch ${BABEL_MAKE_ALL}

#for element in "${srcKinds[@]}" ; do
#	echo "$element = " >> $BABEL_MAKE_ALL
#done

for babelMake in $babelMakeFiles ; do
	if test -e $babelMake ; then 
		d=`dirname $babelMake`
		for element in "${srcKinds[@]}" ; 
			do
				# Clumsy, but easy
				srcs=`sed -e :a -e '/\\\\$/N; s/\\\\\\n//; ta' $babelMake | grep $element | sed -e 's/^.* = *//g'`;
				if test "x$srcs" != "x" ; then
					# prepend directory to each src
					newsrcs=""
					for s in $srcs ; do 
						if test "$d" != "."; then 
							newsrcs="$newsrcs $d/$s"
						else
							newsrcs="$newsrcs $s"
						fi
					done
					echo "$element:=\$(strip \$($element) $newsrcs)" >> $BABEL_MAKE_ALL
				fi
			done
	fi
done

babelMakeDependsFiles=`find $searchdir -name ".*babel.make.depends" -print | sed -e 's|^./||'`
for babelMakeDepends in $babelMakeDependsFiles ; do
	if test -e $babelMakeDepends ; then
		# The grep -Ev is needed to get around a Babel bug in the F90 dependencies
		cat $babelMakeDepends | grep -Ev ': \w+$' >> $BABEL_MAKE_ALL;
	fi
done
echo $BABEL_MAKE_ALL
