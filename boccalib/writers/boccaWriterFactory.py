import os
import writers
from writers import *
from cct._util import DEBUGSTREAM, Globals
from cct._err import err

def BoccaWriterFactory():
    '''Helper function to ensure exactly one instance of the BoccaWriterFactory_Singleton class exists'''
    factory = None
    try:
        factory = BoccaWriterFactory_Singleton()
    except BoccaWriterFactory_Singleton, s:
        factory = s
    return factory

class BoccaWriterFactory_Singleton (object):
    def __init__(self):
        self.writers = {}
        for modName in writerModules:
            writerClassName = modName[0].upper()+modName[1:]
            mod = getattr(writers, modName)
            writerClass = getattr(mod, writerClassName)
            (lang, versionList, dialect) = mod.getWriterParameters()
            key = lang + ':' + '|'.join(versionList) + ':' + dialect
            self.writers[key] = (writerClass, None)
        
    def getWriter (self, language, dialect, babelVersion='', kind = 'component'):
        ccaVars = Globals().getCCAVars()
        if len(ccaVars) == 0:
            err('[BoccaWriterFactory] could not load CCA settings from defaults file')
        if babelVersion is '': 
            # The CCASPEC_BABEL_VERSION has a timestamp instead of a version for nightly
            # tarballs, so call babel to determine version
            cmd = ccaVars['CCASPEC_BABEL_BABEL'] + ' --version'
            try:
                f = os.popen(cmd)
                lines = f.readlines()
                for l in lines:
                    cl = l.strip()
                    if cl.startswith('Babel version'): babelVersion = l.split()[-1]
            except:
                err('[BoccaWriterFactory] Could not determine Babel version')
                
        print >> DEBUGSTREAM, '[BoccaWriterFactory] Babel version is ' + str(babelVersion)
        
        # Handle nightly Babel tarballs, which don't have a regular version number
        if babelVersion.count('.') == 0:
            if 'CCASPEC_BABEL_SNAPSHOT' in ccaVars.keys():
                if ccaVars['CCASPEC_BABEL_SNAPSHOT'] == '1':
                    babelVersion = ccaVars['CCASPEC_BABEL_BRANCH']
        
        if babelVersion.count('.') == 0:
            # Sometimes the version number is in that variable, whether it's a snapshot or not
            if 'CCASPEC_BABEL_BRANCH' in ccaVars.keys():
                babelVersion = ccaVars['CCASPEC_BABEL_BRANCH']

        if babelVersion.count('.') == 0:
            err('[BoccaWriterFactory] Invalid Babel version encountered')

        for key in self.writers.keys():
            (lang, versionList, dial) = key.split(':')
            versionList = versionList.split('|')
            if (lang != language):
                continue
            if (dial != dialect):
                continue
            (major, minor, patch) = babelVersion.upper().split('.')
            matchingVer = ''
            for v in versionList:
                v_elements = v.upper().split('.')
                v_major = v_elements[0]
                v_minor='X'
                v_patch='X'
                if (len(v_elements) > 3):
                    err('Invalid supported Babel version number ' + 
                        v + ' in class ' + str(self.writers[key][0]), 2)
                if(len(v_elements) == 2):
                    v_minor = v_elements[1]
                elif (len(v_elements) == 3):
                    v_minor = v_elements[1]
                    v_patch = v_elements[2]
                match = False
                if (v_major == 'X'):
                    match = True
                    matchingVer = v
                    break
                if (v_major != major):
                    continue
                if (v_minor == 'X'):
                    match = True
                    matchingVer = v
                    break
                if (v_minor != minor):
                    continue
                if (v_patch == 'X'):
                    match = True
                    matchingVer = v
                    break
                if (v_patch != patch):
                    continue
            if (not match):
                print >> DEBUGSTREAM, 'Babel version', babelVersion , 'NOT matched by writer versions', versionList
                continue
            print >> DEBUGSTREAM, 'Babel version', babelVersion , 'is matched by writer version', matchingVer
            (classRef, classInstance) = self.writers[key]
            if (classInstance == None):
                classInstance = classRef(kind)
                self.writers[key] = (classRef, classInstance)
            classInstance.setBabelVersion(babelVersion)
            return classInstance
        err('No writer supports ' + language + ' for Babel version ' + babelVersion + ' and dialect ' + dialect, 1)
                        
