import sys, os
import cct._debug
from graph.boccagraph import *

class LocationManagerInterface:
    '''An interface for querying locations of sources, objects, and libraries.'''
    def __init__(self, project):
        self.project = project
        if self.__class__ is LocationManagerInterface: raise NotImplementedError
        pass
    
    def projectMoved(self):
        '''Compares known project path to actual current project paths and if they 
        don't match, returns a triplet True, oldpath, newpath. 
        If the project has not been relocated since it was configured, this 
        method returns False, None, None.
        '''
        if self.__class__ is LocationManagerInterface: raise NotImplementedError
        return False, None, None
    
    def getLanguages(self):
        '''Returns the list of languages with which the project has been configured.
        '''
        langs = []
        if self.__class__ is LocationManagerInterface: raise NotImplementedError
        return langs
    
    def getComponentLoc(self):
        ''' Returns a list of directories containing source code for components
        in this project  (relative to top-level project directory)
        '''
        dirlist = []
        if self.__class__ is LocationManagerInterface: raise NotImplementedError
        return dirlist

    def getPortLoc(self):
        ''' Returns a list of directories containing source code for ports
        in this project  (relative to top-level project directory)
        '''
        dirlist = []
        if self.__class__ is LocationManagerInterface: raise NotImplementedError
        return dirlist 
    
    def getSIDLDirs(self, vertex):
        ''' Returns a list of directories containing SIDL files for the 
        specified vertex.
        '''
        dirlist = []
        if self.__class__ is LocationManagerInterface: raise NotImplementedError
        return dirlist
           
    def getSIDLLoc(self, vertex):
        '''Returns a 2-tuple (dir, [filelist]) containing the relative path (w.r.t. project) 
        and names of SIDL files.'''    
        mydir = None
        flist = []
        if self.__class__ is LocationManagerInterface: raise NotImplementedError        
        return mydir, flist

    def getExternalLoc(self):
        ''' Returns a list of directories containing source code for clients 
        for external SIDL dependencies (relative to top-level project directory)
        '''
        dirlist = []
        if self.__class__ is LocationManagerInterface: raise NotImplementedError
        return dirlist 
        
    def getImplLoc(self, vertex):
        '''Returns a 2-tuple (dir, [filelist]) containing the relative path (w.r.t. project)
         of impl files.
        
        @param vertex: the project vertex (e.g., interface, port, class, component,
        enum) for which the file info is to be generated. Note that the vertex 
        includes all necessary information, including the language.
        '''
        mydir = None
        flist = []
        if self.__class__ is LocationManagerInterface: raise NotImplementedError        
        return mydir, flist
    
    def getGlueLoc(self, vertex, language, server=True):
        '''Returns a 2-tuple (dir, [filelist]) containing the relative path
        (w.r.t. project) of the generated glue code and the file names of the 
        glue sources.
       
        @param vertex: the project vertex (e.g., interface, port, class, component,
        enum) for which the file info is to be generated. 

        @param language: the language for which the glue code file information
        is to be returned; one of c, cxx, f90, f77, f03, java, python . 
        
        @param server: indicates whether the location is for a server or 
        client code (using the Babel meaning of client and server). 
        '''
        mydir = None
        flist = []
        if self.__class__ is LocationManagerInterface: raise NotImplementedError        
        return mydir, flist

    def getBuildfilesLoc(self, vertex, client_only=False):
        '''Returns a 2-tuple (dir, [fileset]) containing the relative path (w.r.t project)
        of the makefiles (and some makefile input files) used in the build process which 
        the user should NOT edit.  This includes the top-level configure.

        Note that there may be some overlap here with how builder.py determines where to generate
        makefiles.'''
        mydir = None
        flist = []
        if self.__class__ is LocationManagerInterface: raise NotImplementedError        
        return mydir, flist
           
    def getUserBuildfilesLoc(self, vertex):
        '''Returns a 2-tuple (dir, [filelist]) containing the relative path (w.r.t. project)
         of user makefile stub files.
        '''
        mydir = None
        flist = []
        if self.__class__ is LocationManagerInterface: raise NotImplementedError
        return mydir, flist

    def getBuildLibLoc(self,vertex, lang=None, client=False):
        '''Returns a list of directories containing libraries corresponding to a vertex in the build tree.'''
        dirs = []
        if self.__class__ is LocationManagerInterface: raise NotImplementedError        
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
            is computed by this method based on the symbol information.
        '''
        mydir = None
        flist = []
        if self.__class__ is LocationManagerInterface: raise NotImplementedError
        return flist
    
    def getInstallLibLoc(self,vertex):
        '''Returns the location of the library corresponding to vertex in the installation location.'''
        mydir = None
        if self.__class__ is LocationManagerInterface: raise NotImplementedError        
        return mydir
    
    def getInstallIncludeLoc(self,vertex):
        '''Returns the include path corresponding to vertex in the installation location.'''
        mydir = None
        if self.__class__ is LocationManagerInterface: raise NotImplementedError        
        return mydir    
