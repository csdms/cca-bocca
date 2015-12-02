#!/bin/bash

usage () {
	echo -e "\nUsage:\n  sh fakedepl.sh  kind sym -o outfile other switches\n\n"\
		"This script is a dummy for old versions of cca-spec-babel lacking genccaxml\n"\
		"most args are ignored.\n"\
		"\n" > /dev/stderr
}

if [ $# -lt 3 ];  then
	usage
	exit 1;
fi

# Process command-line options
kind=$1
sym=$2
shift
shift
out="dummy"
while [ $# -gt 0 ]; do
	case "$1" in
		-o)
			out=$2
			break
			;;
		*)
			shift
			;;
	esac
done


if [ "x$kind" = "x" ] || [ "x$sym" = "x" ]; then
	echo "fakedepl.sh args wrong"
	usage; 
	exit 1;
fi

if test "x$out" = "xdummy"; then
	out="${sym}_depl.xml"
fi
if test -f $out; then
	exit 0;
fi
cat << EOF > $out
<xml version="1.0" ?>
<!-- dummy file. upgrade your cca-spec-babel if you want the real thing. >
EOF

exit 0
