#!/usr/bin/env python

#-----------------------------------
# Debugging support for subjects.

import sys, os, cct._err

class Devnull:
    """ The do nothing writer to replace sys.stderr when we want to see
    no spew.
    """
    def write(self, msg): pass
    def flush(self): pass


DEBUGSTREAM = Devnull()
BLOCKDUMP = False
CFGDUMP = False
WARN = False

if 'BOCCA_DEBUG' in os.environ.keys():
    if os.environ['BOCCA_DEBUG'] == "1":
        DEBUGSTREAM = sys.stderr
        WARN = True
    
