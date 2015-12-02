#!/usr/bin/env python

import os, sys, distutils.sysconfig

def gen():
    mypath = os.path.dirname(os.path.realpath(sys.argv[0]))
    libdirname = distutils.sysconfig.get_config_var('LIB')
    if libdirname is None: 
        # True for python versions < 2.5
        libdirname = 'lib'
 
    boccapyPath = os.path.abspath(os.path.join(mypath, '..'))
    boccalibPath = os.path.join(boccapyPath, 'boccalib')
    scriptsPath = os.path.join(boccapyPath, 'scripts')
    os.environ['PYTHONPATH'] = boccapyPath + ':' +  boccalibPath + ':' + os.path.join(boccalibPath,'cct') + ':' + scriptsPath
    docpath = os.path.join(boccapyPath,'doc','html')
    os.chdir(docpath)
    # Clean up old docs
    for f in os.listdir(docpath): 
        if f.endswith('.html'): os.remove(f)
    print 'Generating HTML documentation in', docpath
    os.execvpe('pydoc', ['pydoc', '-w', boccapyPath], os.environ)
    
if __name__ == '__main__':
    gen()
