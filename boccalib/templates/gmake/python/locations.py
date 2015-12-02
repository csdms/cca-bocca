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
        if vertex.kind == 'class' or vertex.kind == 'component':
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
            err('Unknown language specified when calling the location manager: %s' \
                + '. Known languages are %s', (language, str(self.getLanguages())))
            
        if vertex.kind in ['port','interface','enum']:
            mydir = os.path.join('ports',language)
        elif vertex.kind in ['class','component']:
            if server:
                mydir = os.path.join('components',vertex.symbol,'glue')
            else:
                mydir = os.path.join('components','clients',language)
                
        # This builder plugin does not need the file list, so we don't
        # compute it in this method (this can be added in the future if needed).
        return mydir, flist
    
    def getBuildfilesLoc(self, vertex, client_only=False):
        '''Returns a 2-tuple (dir, [fileset]) containing the relative path (w.r.t project)
        of the makefiles (and some makefile input files) used in the build process which 
        the user should NOT edit.  This includes the top-level configure.

        Note that there may be some overlap here with how builder.py determines where to generate
        makefiles.'''

        mydir = None
        flist = []
        if vertex.kind in ['class', 'component']:
            if not client_only:
                mydir = 'components'
                flist.extend(['Makefile', 'make.components', os.path.join(vertex.symbol, 'Makefile')])
            else:
                mydir = os.path.join('components','clients')
                flist.extend(['Makefile','bocca_setup.py'])
                
        elif vertex.kind in ['interface', 'port', 'enum']:
            mydir = 'ports'
            flist = ['Makefile','bocca_setup.py']
        elif vertex.kind == 'project':
            mydir = '.'
            flist = ['Makefile', 'make.project', 'make.project.in', 
                     'configure', 'configure.ac', 'configure.ac1',
                     os.path.join('external', 'Makefile')]
        elif vertex.kind == 'package':
            mydir = '.'
            for v in vertex.dependents():
                dir, files = self.getBuildfilesLoc(v)
                for f in files:
                    flist.append(os.path.join(dir,f))

        return mydir, flist

    def getExtraDirsLoc(self, vertex):
        '''Returns a tuple (topdir, [subdirs]) containing the relative path (w.r.t project)
        of 'extra' directories that are needed to build a bocca project.'''

        mydir = None
        dirlist = []
        if vertex.kind in ['class', 'component']:
            mydir = 'components'
            dirlist = ['clients', 'tests']
        elif vertex.kind == 'project':
            mydir = '.'
            dirlist = ['buildutils', 'config', 'depl', 'utils']
        elif vertex.kind == 'package':
            for v in vertex.dependents():
                dir, subdirs = self.getExtraDirsLoc(v)
                for d in subdirs:
                    dirlist.append(os.path.join(dir, d))

        return mydir, dirlist
                

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
        '''Returns a list of directories containing libraries corresponding to a vertex in the build tree.'''
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
        '''Returns a [filelist] containing the relative path (w.r.t. project)
        of library names in the build tree. 
        
        @param vertex: the project graph vertex representing the code that will
            be built in this library.
        @param lang: optional string specifying the source language.
        @param client: True if this is a client library name, False if it's a server
            library name (for the Babel meanings of client/server).
        @param for_install: a boolean used in cases when a separate library must 
        be linked prior to installation, as is usually the case when using libtool.
        @param filename: a string to use for the base filename, if not specified, it 
            is computed by this method based on the symbol information.        '''
        flist = []
        symbol = vertex.symbol                 
        if vertex.kind in ['interface', 'port', 'enum']:
            if not vertex._b_sidlFile: topdir = 'external'
            else: topdir = 'ports'
            if not lang:
                for lang in self.getLanguages():
                    subdir=lang
                    if for_install: subdir = os.path.join(lang,'.install')
                    if lang == 'python':
                        parts= symbol.split('.')
                        if vertex.kind == 'enum':
                            flist.append(os.path.join(topdir,symbol, subdir, os.sep.join(parts[:-1]), parts[-1] + '.pystamp'))
                        else:
                            flist.append(os.path.join(topdir,symbol, subdir, os.sep.join(parts[:-1]), parts[-1] + '.so'))
                    else:
                        flist.append(os.path.join(topdir,symbol, subdir,'lib' + symbol + '-' + lang + '.la'))
            else:
                if lang == 'python':
                    parts= symbol.split('.')
                    if vertex.kind == 'enum':
                        flist.append(os.path.join(topdir,symbol, lang, os.sep.join(parts[:-1]), parts[-1] + '.pystamp'))
                    else:
                        flist.append(os.path.join(topdir,symbol, lang, os.sep.join(parts[:-1]), parts[-1] + '.so'))
                else:
                    subdir = lang
                    if for_install: subdir = os.path.join(lang,'.install')
                    flist.append(os.path.join(topdir,symbol, subdir,'lib' + symbol + '-' + lang + '.la'))
        elif vertex.kind in ['class', 'component']:
            if client:
                if lang == 'python':
                    parts= symbol.split('.')
                    flist.append(os.path.join('components','clients',symbol,lang, os.sep.join(parts[:-1]), parts[-1] + '.so'))
                else:
                    subdir = lang
                    if for_install: subdir = os.path.join(lang,'.install')
                    flist.append(os.path.join('components','clients',symbol, subdir, 'lib' + symbol + '-' + lang + '.la'))
            else:
                flist.append(os.path.join('components',symbol,'lib' + symbol + '.la'))
            
        #print >>DEBUGSTREAM, 'LocationManager: buildlibs for ' + vertex.symbol + ' = ' + str(flist)
        return flist

    def getInstallLibLoc(self,vertex):
        '''Returns the location of the library corresponding to vertex in the installation location.'''
        mydir = None
        raise NotImplementedError        
        return mydir
    
    def getInstallIncludeLoc(self,vertex):
        '''Returns the include path corresponding to vertex in the installation location.'''
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
