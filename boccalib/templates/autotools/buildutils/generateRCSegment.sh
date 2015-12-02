#!/bin/bash

usage () {
	echo -e "\nUsage:\n\tsh $0  <rcfile> <lib_dir> [component_name]\n\n"\
		"This script adds a small Ccaffeine resource control (rc) script fragment\n"\
		"that set the dynamic  library search path to <lib_dir> and instantiates\n"\
		"the component <component>.\n"\
		"If component_name is omitted, only the path directive is inserted.\n"\
		"If <rcfile> exists and does not already contain this component, the\n"\
		"new commands are appended to <file>\n"\
		" Arguments: \n"\
		"            rcfile is the full path name of the target Ccaffeine RC file\n"\
		"                   if the filename contains '_gui', an RC script appropriate\n"\
		"                   for the Ccaffeine GUI will be generated.\n"\
		"	     lib_dir is the full path location of the dynamic libraries\n"\
		"            component_name is the fully qualified name fo the component\n" > /dev/stderr
}

if [ $# -lt 2 ];  then
	usage
	exit 1;
fi

rcfile=$1
lib=$2
notgui="0"
if [ "x`echo $rcfile | grep gui`" = "x" ]; then notgui="1"; fi

if [ ! -f "$rcfile" ] ; then  
	echo "#!ccaffeine bootstrap file. "  > $rcfile
	echo "# ------- don't change anything ABOVE this line.-------------" >> $rcfile 
	echo "path set $lib" >> $rcfile
fi 
if [ $# -ne 3 ]; then exit 0; fi

# Get rid of quit
grep -v "^quit" $rcfile > $rcfile.tmp; mv $rcfile.tmp $rcfile

component=$3

match=`grep "^#${component}#" $rcfile`
if [ "x$match" = "x" ] ; then 
	instance=`echo "$component" | sed 's/\./_/g'`; 
	echo -e "\n#${component}#" >> $rcfile;
	echo -e "\nrepository get-global $component" >> $rcfile;
	if [ "x$notgui" = "x1" ]; then 
cat << EOF >> $rcfile; 
instantiate $component $instance
display component $instance
remove $instance
EOF
fi
fi
