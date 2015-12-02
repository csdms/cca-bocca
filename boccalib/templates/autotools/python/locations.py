import sys, os, re
import cct._debug

import builders.locations as locationTemplate
from graph.boccagraph import *
from cct import *
from cct._util import *

class LocationManager(locationTemplate.LocationManagerInterface):
    '''An interface for querying locations of sources, objects, and libraries.'''
    def __init__(self, project):
        self.project = project
        pass
    
    def projectMoved(self):
        '''Compares known project path to actual current project paths and if they 
        don't match, returns a triplet True, oldpath, newpath. 
        If the project has not been relocated since it was configured, this 
        method returns False, None, None.
        '''
        from fileinput import FileInput
        projectConfigFile = os.path.join(self.project.getDir(),'make.project')
        if os.path.exists(projectConfigFile):
            # The project has been configured 
            for line in FileInput(projectConfigFile):
                m = re.match("^\s*PROJECT_TOP_DIR\s*=", line)
                if m: 
                    topdirline=line
                    break
            if topdirline:
                topdir = topdirline.split('=')[1].strip()
                if topdir.endswith(os.sep): topdir=topdir[:-1]

                projDir = self.project.getDir()
                if projDir.endswith(os.sep): projDir=projDir[:-1]

                if projDir != topdir:
                    return True, topdir, projDir

        return False, None, None
    
    def getLanguages(self):
        '''Returns the list of languages with which the project has been configured.
        '''
        from fileinput import FileInput
        langs = []
        projectConfigFile = os.path.join(self.project.getDir(),'make.project')
        if not os.path.exists(projectConfigFile):
            err('Could not find project build configuration file %s. You may need to run configure in the top-level project directory.' % projectConfigFile)
        langline = ''
        for line in FileInput(projectConfigFile):
            m = re.match("USER_LANGUAGES =", line)
            if m:
                langline = line
        if langline is not '':
            langs = langline.split('=')[1].strip().split()
        #print >>DEBUGSTREAM, 'LocationManager: langugages = ' + str(langs)
        return langs
    
    def getComponentLoc(self):
        ''' Returns a list of directories containing source code for components
        in this project (relative to top-level project directory)
        '''
        dirlist = ['components']
        return dirlist
    
    def getPortLoc(self):
        ''' Returns a list of directories containing source code for ports
        in this project (relative to top-level project directory)
        '''
        dirlist = ['ports']
        return dirlist
    
    def getSIDLDirs(self, vertex):
        ''' Returns a list of directories containing SIDL files for the specified vertex.
        '''
        dirlist = []
        if vertex.kind == 'project':
            dirlist = [os.path.join('ports','sidl'), os.path.join('components','sidl')]
        elif vertex.kind in ['interface', 'port', 'enum']:
            dirlist = [os.path.join('ports','sidl')]
        elif vertex.kind in ['class', 'component']:
            dirlist = [os.path.join('components','sidl')]
        return dirlist

    def getSIDLLoc(self, vertex):
        '''Returns a 2-tuple (dir, [filelist]) containing the relative path (w.r.t. project) 
        and names of SIDL files.'''    
        dir = None
        flist = []
        if vertex.kind in ['interface','port', 'enum']:
            dir = os.path.join('ports','sidl')
            flist = [vertex.symbol+'.sidl']
        elif vertex.kind in ['class', 'component']:
            dir = os.path.join('components','sidl')
            flist = [vertex.symbol+'.sidl']    
        return dir, flist
    
    def getExternalLoc(self):
        ''' Returns a list of directories containing source code for clients 
        for external SIDL dependencies (relative to top-level project directory)
        '''
        dirlist = ['external']
        return dirlist 
    
    def getImplLoc(self, vertex):
        '''Returns a 2-tuple (dir, [filelist]) containing the relative path (w.r.t. project)
         of impl files.
        '''
        mydir = None
        flist = []

        # The two dictionaries below are not used since each vertex knows its files (in theory)
        implHeaders = { 'c': ['_Impl.h'], 'cxx': ['_Impl.hxx'], 'f77': [], 'f90': [], 
                        'f03': [], 'java': [], 'python': [] }
        implSources = { 'c': ['_Impl.c'], 'cxx': ['_Impl.cxx'], 'f77': ['_Impl.f'],
                        'f90': ['_Mod.F90', '_Impl.F90'], 'f03': ['_Mod.F03', '_Impl.F03'],
                        'java': ['.java','_Impl.java'], 'python': ['_Module.c', '_Impl.py']}

        if vertex.kind in ['class','component']:
            mydir = os.path.join('components', vertex.symbol)
            if vertex._b_language in ['python', 'java']:                
                packages = vertex.symbol.split('.')[:-1]
                for p in packages: mydir = os.path.join(mydir,p)
            if vertex._b_implHeader: flist.append(re.sub(mydir,'',vertex._b_implHeader).strip(os.path.sep))
            if vertex._b_implSource: flist.append(re.sub(mydir,'',vertex._b_implSource).strip(os.path.sep))
        return mydir, flist
    
    def getGlueLoc(self, vertex, language, server=True):
        '''Returns a 2-tuple (dir, [filelist]) containing the relative path
        (w.r.t. project) of the generated glue code and the file names of the 
        glue sources.
       
        @param vertex: the project vertex (e.g., interface, port, class, component,
        enum) for which the file info is to be generated. 

        @param language: the language for which the glue code file information
        is to be returned; one of c, cxx, f90, f77, f03, java, python. 
                
        @param server: indicates whether the location is for a server or 
        client code (using the Babel meaning of client and server).
        '''
        mydir = None
        flist = []
        
        if language not in self.getLanguages():
            err('Unknown loanguage specified when calling the location manager: %s' \
                + '. Known languages are %s', (language, str(self.getLanguages())))

        # First, determine the directory
        if vertex.kind in ['port','interface','enum']:
            mydir = os.path.join('ports',language)
        elif vertex.kind in ['class','component']:
            if server:
                mydir = os.path.join('components',vertex.symbol,'glue')
            else:
                mydir = os.path.join('components','clients',language)
                
        # Now the list of source files (for now we ignore the headers since automake is 
        # supposed to figure out the dependencies automatically).

        # Language-specific glue code (the common case is handled separately near the end of this method)
        glueSources = { 'c': ['_Stub.c','_Skel.c'], 'cxx': ['_Skel.cxx'], 'f77': ['_fStub.c','_fSkel.c'],
                        'f90': ['_fStub.c','_fSkel.c','_type.F90','.F90'], 
                        'f03': ['_fStub.c','_fSkel.c','_type.F03','.F03'],
                        'java': ['_jniStub.c', '_jniSkel.c'], 'python': ['_pSkel.c','_pLaunch.c']}
            
        fnames = vertex.symbol.split('.')           # split symbol name into packages 
        un_name = vertex.symbol.replace('.','_')    # complete name using underscores

        # "Glue" code for all types of SIDL entities, for both client and server

        # IOR files present in all the languages
        current = fnames[0]
        flist.extend([current + '.c', current + '_IOR.c']) 
        for f in fnames[1:]: 
            current += '_' + f
            flist.extend([current + '.c', current + '_IOR.c']) 

        # Now for the language-specific ones:
        flist.extend([un_name + x for x in glueSources[language]])

        return mydir, flist
    
    def getUserBuildfilesLoc(self, vertex):
        '''Returns a 2-tuple (dir, [filelist]) containing the relative path (w.r.t. project)
         of user makefile stub files.
        '''
        mydir = None
        flist = []
        if vertex.kind in ['class','component']:
            mydir = 'components'
            flist = ['make.vars.user', 'make.rules.user', os.path.join(vertex.symbol,'make.vars.user'), os.path.join(vertex.symbol,'make.rules.user')]
        elif vertex.kind in ['interface','port','enum']:
            mydir = 'ports'
            flist = ['make.vars.user', 'make.rules.user']
        elif vertex.kind == 'project':
            mydir = '.'
            flist = ['make.vars.user', 'make.rules.user', os.path.join('external','make.vars.user'), os.path.join('external','make.rules.user')]
        elif vertex.kind == 'package':
            mydir = '.'
            for v in vertex.dependents():
                dir, files = self.getUserBuildfilesLoc(v)
                for f in files:
                    flist.append(os.path.join(dir,f))
        return mydir, flist

    def getBuildLibLoc(self, vertex, lang=None, client=False):
        '''Returns a list of directories containing libraries correponding to a vertex in the build tree.'''
        dirs = []
        if vertex.kind == 'port' or vertex.kind == 'interface':
            if not lang:
                for lang in self.getLanguages():
                    tmp = os.path.join('ports',vertex.symbol,lang)
                    if lang == 'python':
                        tmp = os.path.join(tmp,os.sep.join(vertex.symbol.split('.')[:-1]))    
                    dirs.append(tmp)
            else:
                tmp = os.path.join('ports',vertex.symbol,lang)
                if lang == 'python':
                    tmp = os.path.join(tmp,os.sep.join(vertex.symbol.split('.')[:-1]))    
                dirs.append(tmp)
        elif vertex.kind == 'class' or vertex.kind == 'component':
            if client:
                tmp=os.path.join('components','clients',vertex.symbol,lang)
                if lang == 'python':
                    tmp=os.path.join(tmp,os.pathsep.join(vertex.symbol.split('.')[:-1]))
                dirs.append(tmp)
            else:
                dirs.append(os.path.join('components',vertex.symbol))
        return dirs
    
    def getBuildLibs(self,vertex, lang=None, client=False, for_install=False, filename=None):
        '''@return: a [filelist] containing the relative path (w.r.t. project)
        of library names in the build tree. 
        
        @param vertex: the project graph vertex representing the code that will
            be built in this library.
        @param lang: optional string specifying the source language.
        @param client: True if this is a client library name, False if it's a server
            library name (for the Babel meanings of client/server).
        @param for_install: a boolean used in cases when a separate library must 
        be linked prior to installation, as is usually the case when using libtool.
        @param filename: a string to use for the base filename, if not specified, it 
            is computed by this method based on the symbol information.
        '''
        flist = []
        symbol = vertex.symbol                 
        subdir = 'build'
        if vertex.kind in ['interface', 'port', 'enum']:
            if not vertex._b_sidlFile: topdir = 'external'
            else: topdir = 'ports'
            if not lang:
                for lang in self.getLanguages():
                    subdir=lang
                    if for_install: subdir = os.path.join(lang,'.install')
                    if lang == 'python' and vertex.kind != 'enum':
                        # Python library name must correspond to the module name.
                        # Babel does not generate a C file for enums in python, thus no library.
                        parts= symbol.split('.')
                        flist.append(os.path.join(topdir,symbol, subdir, os.sep.join(parts[:-1]), parts[-1] + '.so'))
                    else:
                        if not filename: filename = 'lib' + symbol + '-' + lang
                        flist.append(os.path.join(topdir,symbol, subdir, filename + '-' + lang + '.la'))
            else:
                if lang == 'python' and vertex.kind != 'enum':
                    # Python library name must correspond to the module name.
                    # Babel does not generate a C file for enums in python, thus no library.
                    parts= symbol.split('.')
                    flist.append(os.path.join(topdir,symbol, lang, os.sep.join(parts[:-1]), parts[-1] + '.so'))
                else:
                    subdir = lang
                    if for_install: subdir = os.path.join(lang,'.install')
                    flist.append(os.path.join(topdir,symbol, subdir,'lib' + symbol + '-' + lang + '.la'))
        elif vertex.kind in ['class', 'component']:
            if client:
                if lang == 'python':
                    # Python library name must correspond to the module name.
                    parts= symbol.split('.')
                    flist.append(os.path.join('components','clients',symbol,lang, os.sep.join(parts[:-1]), parts[-1] + '.so'))
                else:
                    subdir = lang
                    if for_install: subdir = os.path.join(lang,'.install')
                    if not filename: filename = 'lib' + symbol
                    flist.append(os.path.join('components','clients',symbol, subdir, filename + '-' + lang + '.la'))
            else:
                flist.append(os.path.join('components',symbol,'lib' + symbol + '.la'))
            
        #print >>DEBUGSTREAM, 'LocationManager: buildlibs for ' + vertex.symbol + ' = ' + str(flist)
        print 'LocationManager: buildlibs for ' + vertex.symbol + ' = ' + str(flist)
        return flist

    def getInstallLibLoc(self,vertex):
        '''Returns the location of the library corresponding to vertex in the installation location.'''
        mydir = None
        raise NotImplementedError        
        return mydir
    
    def getInstallIncludeLoc(self,vertex):
        '''Returns the include path correponding to vertex in the installation location.'''
        dir = None
        raise NotImplementedError        
        return dir    
    
    
    #=============== Private methods
    def _convert_template(self, template, opener='[', closer=']'):
        opener = re.escape(opener)
        closer = re.escape(closer)
        pattern = re.compile(opener + '([_A-Za-z.][_A-Za-z0-9.]*)' + closer)
        return re.sub(pattern, r'%(\1)s', template.replace('%','%%'))
    
    def _getProjectDir(self):
        return self.project.getDir()
