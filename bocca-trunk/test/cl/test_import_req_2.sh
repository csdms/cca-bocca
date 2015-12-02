#!/bin/sh
# test class creation with import. particularly concerned with comments
# output must be inspected manually until we have a canonical answer.
cd $2
if ! test "x$?" = "x0" ; then
	echo "changing to scratch directory $2 failed"	
	echo "BROKEN"
	exit 1
fi
rm -rf iir2
mkdir iir2
cd iir2

msg=`$1 create project -p mypkg myproj`
if ! test -d "$2/iir2/myproj/BOCCA"; then
	echo "missing myproj/BOCCA"
	echo "FAIL"
	exit 1
fi
cd myproj
merge="${1}-merge -l sidl -A bocca.splicer -B bocca.splicer"
./configure
cat  << EOF > in.gob.ccb.Subscription.sidl
// DO-NOT-DELETE bocca.splicer.begin(gob.comment)

// Insert-UserCode-Here {gob.comment} (Insert your package comments here)

// DO-NOT-DELETE bocca.splicer.end(gob.comment)
package blob version 0.0 {

    // DO-NOT-DELETE bocca.splicer.begin(blob.ccb.comment)

    // Insert-UserCode-Here {blob.ccb.comment} (Insert your package comments here)

    // DO-NOT-DELETE bocca.splicer.end(blob.ccb.comment)
    package ccb {

        // DO-NOT-DELETE bocca.splicer.begin(blob.ccb.Subscription.comment)

        /** Interface to Event Service for a event subscriber. In order to get
      events delivered to us we use this service to get a Subscription
      and register a listener to this Subscription. In order to force
      the event service to process the events in the queue, a subscriber
      may call processEvents() */

        // DO-NOT-DELETE bocca.splicer.end(blob.ccb.Subscription.comment)
        interface Subscription
        {
            // DO-NOT-DELETE bocca.splicer.begin(blob.ccb.Subscription.methods)

            /**
            *  Adds a listener to the collection of listeners for this Subscription.
            * 
            * @listenerKey - It is used as an index to a unique mapping
            * and the parameter \em theListener is a
            * reference to the /em Listener object.
            * @theListener - A pointer to the object that will listen for events.
            */
            void registerEventListener(in string listenerKey, in EventListener theListener) throws EventServiceException;                   

            /**
            Removes a listener from the collection of listeners for this Topic.
            @listenerKey - It is used as an index to remove this listener.
            */
            void unregisterEventListener(in string listenerKey);                    

            /** Returns the name for this Subscription object */
            string getSubscriptionName();                   

            // DO-NOT-DELETE bocca.splicer.end(blob.ccb.Subscription.methods)
        }
    }
}
EOF

TNAME=gob
PNAME=$TNAME.ccb
ENAME=$TNAME.ccb
dpsidl=ports/sidl


$1 create package $TNAME --version=0.0
if test "$?" != "0"; then echo "FAIL"; exit 1; fi

$1 create package $PNAME --version=0.0
if test "$?" != "0"; then echo "FAIL"; exit 1; fi

$1 create package $PNAME.ports --version=0.0
if test "$?" != "0"; then echo "FAIL"; exit 1; fi

$1 create interface $PNAME.EventServiceException --extends=gov.cca.CCAException
if test "$?" != "0"; then echo "FAIL"; exit 1; fi

$1 create interface $PNAME.Event --extends=sidl.io.Serializable  --requires=gov.cca.TypeMap
if test "$?" != "0"; then echo "FAIL"; exit 1; fi
# $1 change interface $PNAME.Event --import-sidl=$ENAME.Event@$psidl/$ENAME.Event.sidl
# if test "$?" != "0"; then echo "FAIL"; exit 1; fi

$1 create interface $PNAME.EventListener --requires=$PNAME.Event
if test "$?" != "0"; then exit 1; fi
# $1 change interface $PNAME.EventListener --import-sidl=$ENAME.EventListener@$psidl/$ENAME.EventListener.sidl
# if test "$?" != "0"; then exit 1; fi

$1 create interface $PNAME.Subscription --requires=$PNAME.EventServiceException --requires=$PNAME.EventListener
if test "$?" != "0"; then exit 1; fi

$merge -F ./in.$ENAME.Subscription.sidl -T $dpsidl/$ENAME.Subscription.sidl --from-type=blob.ccb.Subscription --to-type=gob.ccb.Subscription
if test "$?" != "0"; then echo "FAIL: bocca-merge" ; exit 1; fi

if grep getSubscriptionName $dpsidl/$ENAME.Subscription.sidl ; then
	:
else
	echo "FAIL: bocca-merge did not work as expected."
	exit 1;
fi

$1 edit -t  $PNAME.Subscription
if test "$?" != "0"; then echo "FAIL: bocca edit -t" ; exit 1; fi


$1 create interface $PNAME.Subscription2 --requires=$PNAME.EventServiceException --requires=$PNAME.EventListener \
--import-sidl=blob.ccb.Subscription@in.$ENAME.Subscription.sidl
if test "$?" != "0"; then 
	echo "FAIL: combined requies, import not working"
	exit 1; 
fi

if grep getSubscriptionName $dpsidl/$ENAME.Subscription2.sidl ; then
	:
else
	echo "FAIL: bocca combined requires/import failed silently."
	exit 1;
fi
echo PASS
exit 0
