#!/bin/bash
# Test an external uses port with multiple sidl files, using the real Performance.sidl 
# file split into two parts (version 1.7.2)
# TODO: add checks for expected outputs, currently only return values checked.

source util.sh

cd $2
if [ ! -d ext1 ]; then mkdir ext1; fi

export BOCCA=$1
export BOCCATEST=`pwd`/ext1

createExtFiles() {
    # Create the external sidl
    mkdir $BOCCATEST/externaldir

cat <<EOF > $BOCCATEST/externaldir/Performance1.sidl
package Performance version 1.7.2 
{
  interface Timer 
  { /* Start/stop the Timer */ 
    void start(); 
    void stop();

    /* Set Profile Parameter */
    void setParam1L(in long value, in string name);

    /* Set/get the Timer name */ 
    void setName(in string name);
    string getName();

    /* Set/get Timer type information (e.g., signature of the routine) */ 
    void setType(in string name);
    string getType();

    /* Set/get the group name associated with the Timer */
    void setGroupName(in string name);
    string getGroupName();

    /* Set/get the group id associated with the Timer */ 
    void setGroupId(in long group);
    long getGroupId();
  }

  interface Phase 
  { /* Start/stop the Phase */ 
    void start(); 
    void stop();

    /* Set Profile Parameter */
    void setParam1L(in long value, in string name);

    /* Set/get the Phase name */ 
    void setName(in string name);
    string getName();

    /* Set/get Phase type information (e.g., signature of the routine) */ 
    void setType(in string name);
    string getType();

    /* Set/get the group name associated with the Phase */
    void setGroupName(in string name);
    string getGroupName();

    /* Set/get the group id associated with the Phase */ 
    void setGroupId(in long group);
    long getGroupId();
  }

  /* Query interface to obtain timing information */ 
  interface Query
  { 
    /* Get the list of Timer and Counter names */ 
    array<string> getTimerNames();
    array<string> getCounterNames();
 
    /* Get the timer data */
    void getTimerData(in array<string> timerList, 
      out array<double, 2> counterExclusive, 
      out array<double, 2> counterInclusive, out array<int> numCalls, 
      out array<int> numChildCalls, out array<string> counterNames,
      out int numCounters);

    /* User Event query interface */
    array<string> getEventNames();
    void getEventData(in array<string> eventList, out array<int> numSamples,
		      out array<double> max, out array<double> min,
		      out array<double> mean, out array<double> sumSqr);

    /* Writes instantaneous profile to disk in a dump file. */
    void dumpProfileData();

    /* Writes instantaneous profile to disk in a dump file with a specified prefix. */
    void dumpProfileDataPrefix(in string prefix);
  

    /* Writes the instantaneous profile to disk in a dump file whose name
     * contains the current timestamp. */
     void dumpProfileDataIncremental();
  
    /* Writes the list of timer names to a dump file on the disk */
     void dumpTimerNames();
  
    /* Writes the profile of the given set of timers to the disk. */
    void dumpTimerData(in array<string> timerList);
  
    /* Writes the profile of the given set of timers to the disk. The dump
     * file name contains the current timestamp when the data was dumped. */
    void dumpTimerDataIncremental(in array<string> timerList);


  }


  /* Memory Tracker interface */
  interface MemoryTracker 
  {
      /* track heap memory at a given place */
      void trackHere();
      /* enable interrupt driven memory tracking */
      void enableInterruptTracking();
      /* set the interrupt interval, default is 10 seconds */
      void setInterruptInterval(in int value);
      /* disable tracking (both interrupt driven and manual) */
      void enable();
      /* enable tracking (both interrupt driven and manual)*/
      void disable();
  }

  /* Memory Headroom Tracker interface */
  interface MemoryHeadroomTracker 
  {
      /* track heap memory at a given place */
      void trackHere();
      /* enable interrupt driven memory tracking */
      void enableInterruptTracking();
      /* set the interrupt interval, default is 10 seconds */
      void setInterruptInterval(in int value);
      /* disable tracking (both interrupt driven and manual) */
      void enable();
      /* enable tracking (both interrupt driven and manual)*/
      void disable();
  }

  /* User defined event profiles for application specific events */ 
  interface Event
  { /* Set the name of the event */ 
    void setName(in string name);

    /* Trigger the event */ 
    void trigger(in double data);
  }

  /* User defined context events for application specific events */ 
  interface ContextEvent
  {
    /* Trigger the event */ 
    void trigger(in double data);

    /* Enable the context tracking on this event */ 
    void enable();

    /* Disable the context tracking on this event */ 
    void disable();
  }


  /* Interface for runtime instrumentation control based on groups */
  interface Control
  { /* Enable/disable group id */
    void enableGroupId(in long id);
    void disableGroupId(in long id);
  
    /* Enable/disable group name */
    void enableGroupName(in string name);
    void disableGroupName(in string name);
  
    /* Enable/disable all groups */
    void enableAllGroups();
    void disableAllGroups();
  }

}
EOF

cat <<EOF2 > $BOCCATEST/externaldir/Performance2.sidl
package Performance version 1.7.2 
{
  /* Interface to create performance component instances */
  interface Measurement extends gov.cca.Port
  { /* Create a Timer */ 
    Timer createTimer(); 
    Timer createTimerWithName(in string name); 
    Timer createTimerWithNameType(in string name, in string type); 
    Timer createTimerWithNameTypeGroup(in string name, in string type, in string group);


    Phase createPhase(); 
    Phase createPhaseWithName(in string name); 
    Phase createPhaseWithNameType(in string name, in string type); 
    Phase createPhaseWithNameTypeGroup(in string name, in string type, in string group);
      
    /* Create a Query interface */ 
    Query createQuery(); 

    /* Create a MemoryTracker interface */ 
    MemoryTracker createMemoryTracker(); 

    /* Create a MemoryHeadroomTracker interface */ 
    MemoryHeadroomTracker createMemoryHeadroomTracker(); 

    /* Create a User Defined Event interface */ 
    Event createEvent(); 
    Event createEventWithName(in string name); 

    /* Create a User Defined Context Event interface */
    ContextEvent createContextEventWithName(in string name); 

    /* Create a Control interface for selectively enabling and disabling
     * the instrumentation based on groups */ 
    Control createControl(); 
  }

  /* Monitor Port for MasterMind component */
  interface Monitor extends gov.cca.Port {
    void startMonitoring(in string rname);
    void stopMonitoring(in string rname, in array<string> paramNames, in array<double> paramValues);
    void setFileName(in string rname, in string fname);
    void dumpData(in string rname);
    void dumpDataFileName(in string rname, in string fname);
    void destroyRecord(in string rname);
  }

  interface PerfParam extends gov.cca.Port {
    int getPerformanceData(in string rname, out array<double, 2> data, in bool reset);
    int getCompMethNames(out array<string> cm_names); 
  }
}

EOF2
}

# First project
pdir=myProject
prefix=$BOCCATEST/installtest
cd $BOCCATEST && /bin/rm -rf *

createExtFiles

checkCmd "FAIL" "$BOCCA create project $pdir" "could not create a project" "$pdir/make.project"

checkCmd "BROKEN" "cd $BOCCATEST/$pdir" "could not cd to $BOCCATEST/$pdir"
cd $BOCCATEST/$pdir

checkCmd "FAIL" "$BOCCA create port integrator.IntegratorPort" "could not create IntegratorPort" "ports/sidl/integrator.IntegratorPort.sidl"

checkCmd "FAIL" "$BOCCA create component integrators.IntegratorProxy --language=cxx --provides=IntegratorPort@IntegratorPortProvide --uses=IntegratorPort@IntegratorPortUse --uses=Performance.Measurement@measurePerformance@$BOCCATEST/externaldir/Performance1.sidl,$BOCCATEST/externaldir/Performance2.sidl" "could not create integrators.IntegratorProxy"

checkCmd "FAIL" "./configure --prefix=$prefix" "could not configure project" "make.project utils/$pdir-config"

checkCmd "FAIL" "make" "could not build project" "install/share/cca/integrators.IntegratorProxy.cca"

checkCmd "FAIL" "make check" "could not instantiate built components" 

checkCmd "FAIL" "make install" "could not install component" "$prefix/share/cca/integrators.IntegratorProxy.cca $prefix/lib/libintegrators.IntegratorProxy.la $prefix/bin/$pdir-config $prefix/lib/$pdir.config-data"

checkCmd "FAIL" "make install-check" "install-check did not succeed" 

echo "PASS"
exit 0
