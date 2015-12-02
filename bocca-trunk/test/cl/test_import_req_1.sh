#!/bin/sh
# test class creation with import. particularly concerned with comments
# output must be inspected manually until we have a canonical answer.
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf iir1
mkdir iir1
cd iir1

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/iir1/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
./configure
cat  << EOF > x.sidl
// DO-NOT-DELETE bocca.splicer.begin(gob.comment)

// Insert-UserCode-Here {gob.comment} (Insert your package comments here)

// DO-NOT-DELETE bocca.splicer.end(gob.comment)
package gob version 0.0 {

    // DO-NOT-DELETE bocca.splicer.begin(gob.ccb.comment)

    // Insert-UserCode-Here {gob.ccb.comment} (Insert your package comments here)

    // DO-NOT-DELETE bocca.splicer.end(gob.ccb.comment)
    package ccb {

        // DO-NOT-DELETE bocca.splicer.begin(gob.ccb.Event.comment)

        // Insert-UserCode-Here {gob.ccb.Event.comment} (Insert your interface comments here)

        // DO-NOT-DELETE bocca.splicer.end(gob.ccb.Event.comment)
        interface Event extends sidl.io.Serializable
        {
            // DO-NOT-DELETE bocca.splicer.begin(gob.ccb.Event.methods)

            /** Return the event's header. The header is usually generated
            by the framework and holds bookkeeping information
            */
            gov.cca.TypeMap getHeader();                    

            /** Returs the event's body. The body is the information the 
            publisher is sending to the subscribers
            */
            gov.cca.TypeMap getBody();              

            // DO-NOT-DELETE bocca.splicer.end(gob.ccb.Event.methods)
        }
    }
}

EOF

msg=`$1 create interface mypkg.bar --requires=gov.cca.TypeMap`
if ! test "x$?" = "x0" ; then
	echo "FAIL: could not use requires of a cca type."
	exit 1
fi
if ! test -f ports/sidl/mypkg.bar.sidl; then
	echo "missing ports/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi

msg=`$1 change interface mypkg.bar --import-sidl=gob.ccb.Event@x.sidl`
if ! test "x$?" = "x0" ; then
	echo "FAIL: could not use import sidl with previously required cca type."
	exit 1
fi

msg=`$1 create interface mypkg.foo --requires=gov.cca.TypeMap --import-sidl=gob.ccb.Event@x.sidl`
if ! test "x$?" = "x0" ; then
	echo "FAIL: could not use requires and import-sidl simultaneously with import dependent on requires type"
	exit 1
fi
if ! test -f ports/sidl/mypkg.foo.sidl; then
	echo "missing ports/sidl/mypkg.foo.sidl"
	echo "FAIL"
	exit 1
fi

echo PASS
exit 0
