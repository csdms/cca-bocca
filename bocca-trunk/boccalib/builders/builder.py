import sys, os
from cct._err import err
from graph.boccagraph import *

class BuilderInterface:
    '''A pure interface to different build system implementations.
       Implementors may save some effort by deriving from BuilderDefault instead.
       The general idea is that the Bocca graph tracks SIDL symbols, but the
       builder plugin must be:
       -) informed when new symbols appear.
       -) informed when a symbol or its dependencies SIDL is changed in a way that 
          may cause a generated impl to be out of date.
       And the plugin *may* be capable of responding to:
       -) deletion of a symbol.
       -) renaming of a symbol.
    '''
    
    def __init__(self, modulePath, project):
        '''Constructor
        @param modulePath the directory containing the implementation of the BuilderInterface
        and associated LocationManager.
        '''
        raise NotImplementedError   
    
    def specializeTemplate(self):
        '''At project creation, specialize the general project template to 
        match the current project.
        '''
        raise NotImplementedError   
    
    def rename(self, oldProjectName, newProjectName, oldProjectVersion, newProjectVersion, oldProjectDir):
        '''Update project build system when the project is renamed.'''
        raise NotImplementedError   

    def update(self, buildFilesOnly=False, quiet=False):
        '''Given a new project graph, update build information. 
           Generally this means regenerating some or all of the build scripts in the project.
        '''
        raise NotImplementedError        
    
    def genSIDL(self, vertex):
        '''Generates SIDL files corresponding to the vertex argument.
           Return is status (Unix-like)
        '''
        raise NotImplementedError        

    def genImpls(self, vertex):
        '''Generates Impls corresponding to the vertex argument.
        Returns status code (Unix-like)
        '''
        raise NotImplementedError
    
    def changed(self, vertexList):
        '''This is how the builder is notified of changes to a list of vertices.
        The build system will perform whatever actions are necessary on these
        vertices during a subsequent update call.
        '''
        raise NotImplementedError
    
    def remove(self, vertexList):
        ''' Removes build-relevant information associated with vertices in vertexList.
        Returns 0 upon success, 1 otherwise.
        '''
        raise NotImplementedError

    def mergeBuildfiles(self, target, source, sourceProjectName='external'):
        '''Merges 'source' into 'target' if the buildfiles are determined
        to be compatible.  Note that this does not necessarily rely on the splicer code.
        '''
        raise NotImplementedError
        
#################################################################################################
class BuilderDefault(BuilderInterface):
    '''A default implementation of base interface. Some common functionality exists,
       if the LocationManager abstraction is used properly.
       Adds project, locationManager and changedList members to self.
    '''
    
    def __init__(self, modulePath, project):
        '''Constructor
        Must be called from every derived plugin before rest of plugin's init.
        @param modulePath the directory containing the implementation of the BuilderInterface
        '''
        if str(project.__class__) != 'project.Project':
            err("Builder plugin: invoking update on a vertex that is not a Project: " + str(project.__class__))

        self.project = project      
        # Load the local LocationManagerInterface implementation
        try:
            (file,filename,description) = imp.find_module('locations',[modulePath])
            locations = imp.load_module('locations', file, filename, description)
        except ImportError,e:
            err('Builder: Could not import locations module from ' + modulePath + ': ' + str(e))
        try:
            LocationManagerClass = getattr(locations,'LocationManager')
        except AttributeError,e:
            err('Builder: Could not find LocationManager class for current build template in ' + modulePath+ ': ' + str(e))
            
        self.locationManager =self.project.getLocationManager()
        self.changedList = []

        pass
    
    def specializeTemplate(self):
        '''At project creation, specialize the general project template to 
        match the current project.
        @return silently if called on an incomplete derived class.
        '''
        if self.__class__ is BuilderDefault: raise NotImplementedError   
        pass
    
    def rename(self, oldProjectName, newProjectName, oldProjectVersion, newProjectVersion, oldProjectDir):
        '''Update project build system when the project is renamed.
        @return silently if called on an incomplete derived class.
        '''
        if self.__class__ is BuilderDefault: raise NotImplementedError   
        pass

    def update(self, buildFilesOnly=False, quiet=False):
        '''Given a new project graph, update build information. 
        @param buildFilesOnly: Only update files contaning component and port info.
        @return silently if called on an incomplete derived class.
        '''
        if self.__class__ is BuilderDefault: raise NotImplementedError        
        status = 0
        return status
    
    def genSIDL(self, vertex):
        '''Generates SIDL files corresponding to the vertex argument.
        Derived builders may wrap this or reuse as is.
        @return status of createSIDL operation.
        '''
        status = 0
        if vertex.kind in ['class', 'component', 'interface', 'port', 'enum']:
            status = vertex.createSIDL()
        return status

    def genImpls(self, vertex):
        '''Generates Impls corresponding to the vertex argument.
        @return silently if called on an incomplete derived class.
        '''
        if self.__class__ is BuilderDefault: raise NotImplementedError
        status = 0
        return status
    
    def changed(self, vertexList):
        '''This is how the builder is notified of changes to a list of vertices.
        The build system will perform whatever actions are necessary on these
        vertices during a subsequent update call.
        '''
        if self.__class__ is BuilderDefault: raise NotImplementedError
        return self.changedList
    
    def remove(self, vertexList):
        ''' Removes build-relevant information associated with vertices in vertexList.
        Returns 0 upon success, 1 otherwise. Remove is hard; the default result is failed.
        '''
        if self.__class__ is BuilderDefault: raise NotImplementedError
        return 1

    def mergeBuildfiles(self, target, source, sourceProjectName='external'):
        '''Merges 'source' into 'target' if the buildfiles are determined
        to be compatible.  Note that this does not necessarily rely on the splicer code.
        '''
        if self.__class__ is BuilderDefault: raise NotImplementedError
        pass
     
    #       
    # --- The following methods are not part of the standard interface but are likely
    #     to be useful to multiple builder plugin implementations. ----
    #
    def getBabelCommandString(self, vertex, checkSIDLOnly=False):
        '''Returns the string containing the complete babel invocation for generating
        client or server code for the specified vertex.
        
        @param vertex: the vertex correponding to the SIDL symbol for which code
                    will be generated by the constructed Babel command
        @param checkSIDLOnly: if True, do not generate code, just check the syntax of 
                    the SIDL definition corresponding to vertex.
        @return the Babel command string.
        '''
        if self.__class__ is BuilderDefault: raise NotImplementedError
        
        if vertex.kind not in ['interface', 'port', 'class', 'component', 'enum']: return ''
        if vertex.getAttr('removed'): return ''
        
        babelcmd = ''
        extra_babel_options = ''

        project, pgraph = Globals().getProjectAndGraph()
        ccaVars = Globals().getCCAVars()
        if len(ccaVars) == 0:
            err('[sidlclass] could not load CCA settings from defaults file')

        sidlIncludes = Set()
        if vertex.kind in ['port', 'component']:
            sidlIncludes.add(Globals().getCCAVars(projectName=project.symbol)['CCA_sidl'])
       
        if vertex._b_xmlRepos: otherRepos = ' -R'.join([' '] + vertex._b_xmlRepos)
        else: otherRepos = ''
        
        # Keep a list of unique paths in inclpaths and check each new path against it before
        # adding an -I option for it (since Babel 1.0.8 crashes for duplicate paths), bocca issue 217
        inclpaths = []
        if vertex._b_externalSidlFiles: 
            extFiles = []
            for sym in vertex._b_externalSidlFiles.keys():
                files = vertex._getExternalSIDLPath(sym).split(',')
                if files:
                    for f in files:
                        fname = f.strip()
                        if fname and not fname in inclpaths: 
                            extFiles.append(fname)
                            inclpaths.append(fname)
            for f in extFiles: 
                sidlIncludes.add(f)
        
        extFiles = []
        for v in vertex.dependencies():

            if v.kind not in ['port', 'interface', 'component','class', 'enum']: continue
            if v.getAttr('removed'): continue
            
            thepath = ''
            if v.symbol.startswith('gov.cca'):
                sidlIncludes.add(Globals().getCCAVars(projectName=project.getName())['CCA_sidl'])
                continue
            if v._b_sidlFile:
                if not v._b_sidlFile.startswith(os.sep):
                    thepath = os.path.join(project.getDir(), v._b_sidlFile)
                else:
                    thepath = v._b_sidlFile
                if not thepath.strip() in inclpaths:
                    if thepath.strip():
                        sidlIncludes.add(thepath)
                        inclpaths.append(thepath)
            # Check for external SIDL files in 
            if v._b_externalSidlFiles: 
                extFiles = []
                for sym in v._b_externalSidlFiles.keys():
                    files = v._getExternalSIDLPath(sym).split(',')
                    if files:
                        for f in files:
                            if not f in inclpaths: 
                                extFiles.append(f)
                                inclpaths.append(f)
                for f in extFiles: sidlIncludes.add(f)
        
        if len(sidlIncludes) > 0:
            sidlIncludesString = ' -I'.join(sidlIncludes)
            sidlIncludesString = ' -I'+sidlIncludesString
        else:
            sidlIncludesString = ''
            
        print >>DEBUGSTREAM, 'SIDL files this class depends on:\n\t' \
                + sidlIncludesString \
                + '\n\texternal: ' + str(extFiles)
       
        if not ccaVars["CCASPEC_BABEL_BRANCH"].startswith('1.0'):
            extra_babel_options = ' --cca-mode --rename-splicers '
 
        if checkSIDLOnly and self.autochecksidl == 'enabled':

            babelcmd = '%s -p %s %s %s %s' % (ccaVars['CCASPEC_BABEL_BABEL'], \
                                              sidlIncludesString, otherRepos,
                                              extra_babel_options,
                                              os.path.join(project.getDir(), vertex._b_sidlFile))
            
        if vertex.kind in ['class','component']:
            if vertex.project: theproject = vertex.project
            else: theproject = project
            # Generate Impl files
            outdir = os.path.join(project.getDir(), 'components', vertex.symbol)
            babelOptions = '-s %s -u -m .%s. -o %s' % \
                   (vertex._b_language, vertex.symbol, outdir)
            print >> DEBUGSTREAM, 'Builder execute prep babelOptions: ' + babelOptions
            print >> DEBUGSTREAM, 'Builder execute prep sidlIncludesString: ' + sidlIncludesString
            babelcmd = '%s %s %s %s %s %s' % (ccaVars['CCASPEC_BABEL_BABEL'], babelOptions, 
                                              sidlIncludesString, otherRepos, extra_babel_options,
                                              os.path.join(theproject.getDir(), vertex._b_sidlFile))
   
        return babelcmd
    
    def invokeBabel(self, vertex, checkSIDLOnly = False):
        '''This method invokes Babel to validate the SIDL for interfaces, ports, classes, and components
        and/or to generate the implementation code for classes and components.
        
        @param vertex: the vertex correponding to the SIDL symbol for which code
                    will be generated by the constructed Babel command
        @param checkSIDLOnly: if True, do not generate code, just check the syntax of 
                    the SIDL definition corresponding to vertex. 
        @return the error code returned by Babel 
        '''
        
        if self.__class__ is BuilderDefault: raise NotImplementedError

        if vertex.kind not in ['interface', 'port', 'class', 'component', 'enum']: return 0
        if vertex.getAttr('removed'): return 0
        
        retcode = 0

        if checkSIDLOnly and self.autochecksidl == 'enabled':

            babelcmd = self.getBabelCommandString(vertex, checkSIDLOnly)

            print >> DEBUGSTREAM, 'Builder executing ' + babelcmd        
            if self.regen_messages == 'verbose': 
                print 'Using Babel to validate the SIDL for %s %s ...' % (vertex.kind, vertex.symbol)
            retcode = os.system(babelcmd)
            return retcode / 256 # get exit code
            
        if vertex.kind in ['class','component']:
            # Generate Impl files
            
            babelcmd = self.getBabelCommandString(vertex, checkSIDLOnly)
            print >> DEBUGSTREAM, 'Builder executing: ' + babelcmd
            
            if self.regen_messages == 'verbose': 
                print 'Babel updating the %s implementation of %s %s ...' % (vertex._b_language, vertex.kind, vertex.symbol)
            
            retcode = os.system(babelcmd)
            retcode = retcode / 256  # get exit code
            # if babel was happy, check for bogus splicing and whine if found
            dir,files = self.locationManager.getImplLoc(vertex)
            if retcode == 0 and files:
                targetSrc= os.path.join(vertex.project.getDir(), vertex._b_implSource )
                print >> DEBUGSTREAM, '(re)generated ' + targetSrc
                if os.path.exists(targetSrc): 
                    grepline = 'grep -i "BEGIN UNREFERENCED" ' + targetSrc
                    hits = os.popen(grepline)
                    for line in hits:
                        print 'BOCCA Warning: Regenerated Impl file' , targetSrc, "has UNREFERENCED splicer blocks."
                        print 'BOCCA Warning: bocca edit -i', vertex.symbol, 'to fix.'
                        break
                    if vertex._b_implHeader is not None and len(vertex._b_implHeader) > 0:
                        targetHdr= os.path.join(vertex.project.getDir(), vertex._b_implHeader)
                        if os.path.exists(targetHdr): 
                            print >> DEBUGSTREAM, '(re)generated ' + targetHdr
                            grepline = 'grep -i "BEGIN UNREFERENCED" ' + targetHdr
                            hits = os.popen(grepline)
                            for line in hits:
                                print 'BOCCA Warning: Regenerated file' , targetHdr, "has UNREFERENCED splicer blocks."
                                print 'BOCCA Warning: bocca edit -m', vertex.symbol, 'to fix.'
                                break
        
        return retcode
