#!/bin/sh

topdir=$1
webdir=$2
tracdir=$3
for i in $topdir/checkout/bocca/test/cl/*.out; do 
	fname=`basename $i`;
	cp -p $i $tracdir/tests/$fname.txt; 
	cp -p $i $webdir/tests/$fname.txt;
done
if [ -e $topdir/logs/bocca/buildstatus.txt ]; then 
	cp -p $topdir/logs/bocca/buildstatus.txt $webdir;
fi

timestamp=`date`
machine=`uname -nro`

# Update html
cat << EOF > $webdir/index.html
<html>
<body>
<h2>Test Results</h2><br>
<p>
<table border="0"><tr><td>Last updated:</td><td>$timestamp</td></tr>
<tr><td>Platform:</td><td>$machine</td></tr>
</table>
<p><a href="buildstatus.txt">CC build info</a></p>
<h3>Summary</h3>
<pre>
EOF

#echo -e "<table><tr>" >> $webdir/index.html
#for result in "PASS" "PENDING" "XFAIL" "FAIL"; do 
#	for line in `grep $result tests/test_z_harness.sh.out.txt`; 
		
if [ -f "$webdir/tests/test_z_harness.sh.out.txt" ]; then 
        cat $webdir/tests/test_z_harness.sh.out.txt >> $webdir/index.html
else
        echo -e "<p>Not available</p>\n" >> $webdir/index.html
fi
echo -e "\n</pre>\n" >> $webdir/index.html

echo -e "\n<h2>Test output files</h2><br>\n" >> $webdir/index.html

for i in `ls $webdir/tests/*.out.txt`; do
  fname=`basename $i`;
  echo -e "<a href="tests/$fname">${fname%.txt}</a><br>\n" >> $webdir/index.html;
done;

echo -e "\n</body>\n</html>" >> $webdir/index.html

exit 0;
