""" A file full of misc checking routines.
Typically each returns a status (0=ok) and a string or object.
"""
from cct._err import *
from boccaversion import bocca_version
import re, os

def language(n):
    """returns (int status, string canonicalLanguageName)
"""
    validlangs = ['c', 'cxx', 'f77', 'f77_31', 'f90', 'java', 'python']
    if n in validlangs:
        return (0,n)
    if n in ['C', 'cc']:
        return (0,'c')
    if n in ['c++', 'C++', 'CXX', 'cpp']:
        return (0,'cxx')
    if n in ['Java', 'JAVA', 'jdk', 'JDK']:
        return (0,'java')
    if n in ['Python', 'PYTHON']:
        return (0,'python')
    if n in ['fortran77', 'F77']:
        return (0,'f77')
    if n in ['fortran77_31', 'F77_31']:
        return (0,'f77_31')
    if n in ['fortran90', 'F90', 'FORTRAN']:
        return (0,'f90')
    err(str(n) + " is an unknown Bocca language. Valid languages are " + ', '.join(validlangs) + '.' )

def validateDialect(lang, dial):
    status, l = language(lang)
    if status != 0:
        return (1, 'unknown')
    if l in ['c', 'java', 'f77', 'f90', 'f77_31', 'python']:
        if dial in ['standard']:
            return (0, 'standard')
    if l == 'cxx':
        if dial in ['standard', 'cio']:
            return (0, dial)
    err(str(dial) + " is an unknown dialect of " + lang )

def sidlType(symbol, defaultPackage, kind='any', graph=None, sidlFile=None):
    '''Returns (int status, string fullyQualifiedType).
    Checks whether specified type is in this project and if not, 
    returns the fully qualified symbol using the default package.'''
    status = 0
    fqsymbol = symbol
    if symbol.count('.') == 0:
        # Short type specified
        #warn('Adding non-fully qualified ' + symbol + ' to package ' + defaultPackage + '.')
        status = 1
        fqsymbol = defaultPackage + '.' + symbol
    # TODO: move the filename checks here, too.
    return (status,fqsymbol)
    

def validateSymbolOption(val):
    '''Validates the values of options that contain SIDL symbol references, e.g., the 
    value of --extends/--implements/--uses/--provides/--requires, etc.
    '''
    status = 0

    # Greedy match
    p = re.match(r'\A[\.\_\w]+[@[\w\\'+os.path.sep+r'\._,:\-]+]*?',val)

    if not p: 
        p2 = re.match(r'\A[\.\_\w@]+\\'+os.path.sep+r'[\w\\'+os.path.sep+r'\._,:\-]+?',val)
        if not p2:
            return (1,0)
        else:
            if p2.end() != len(val):
                return (1,p.end())
        return (1,0)
    
    if p.end() != len(val):
        return (1,p.end())
    
    return (status,p.end())

def boccaVersion(val):
    '''Returns True if this Bocca version is compatible with the project, False otherwise.
    '''
    status = False
    if val.count('.') != 2:
       print >>sys.stderr, 'Bocca ERROR: invalid Bocca version string found: %s' % val
       sys.exit(1)
    major, minor, patch = bocca_version.split('.')
    arg_major, arg_minor, arg_patch = val.split('.')
    # Check whether this bocca version is at least as new as the one with which the project 
    # was created. Using versions of Bocca older then the one with which a project was created
    # is not supported.
    if arg_major <= major and arg_minor <= minor and arg_patch <= patch:
        status = True 
    return status


def validateVersionNumber(val):
    '''Returns True if this is a valid SIDL symbol version number, False otherwise.
    '''
    status = False
    if val.count('.') == 1:
        if re.match(r'^\d+\.\d+$',val): return True
    elif val.count('.') == 2:
        if re.match(r'^\d+\.\d+\.\d+$', val): return True
    else:
        return False    