""" This script handles project functions, such as creation,
removal, renaming, and other project-wide modifications.
This script must not be called directly from a command line; it
must be dispatched through dispatcher.py
bocca help project for usage.
"""

import os, sys, stat, shutil, copy
from parse.boccaParse import OptionParser, BoccaConfigParser

import cct._validate
from cct._debug import DEBUGSTREAM, CFGDUMP
from cct._util import *
from cct._err import err
from graph.boccagraph import *
import builders

class Project(BVertex):
    '''bocca <verb> project [options] [arguments]
    
    Perform the action specified by <verb> on the project. Example verbs include
    create, remove, rename, display. For a complete list of verbs, see
    bocca help.
    '''
    def __init__(self, action = '__init__', args = None, project = None, 
                 modulePath = None, symbol=None, version='0.0', graph=None):
        '''bocca <verb> project [options] [arguments]
        
        <verb> is one of create, change, config, remove, rename, display, update. 
        For documentation on specific verbs, use 'bocca help <verb> project'
        '''
        # The self.defaults variable stores default values read from BOCCA/projName.defaults
        self.defaults = None
        self.projectName = symbol
        BVertex.__init__(self, action= action, 
                         args = args, 
                         modulePath = modulePath, 
                         project = project,
                         kind = 'project',
                         symbol = symbol,
                         version = version,
                         graph = graph)
        self._b_boccaVersion = ''
        self._b_babelVersion = ''
        self.dir = None
        self.setAttr('defaultPackage',None)
        self.newname = None
        self.builder = None
        self.locationManager = None

        self.editLevel = None
        return
    
    def defineArgs(self,action):
        '''Defines command line options and defaults for this command. This is 
        invoked in the constructor of the parent class Subcommand.
        '''
        BVertex.defineArgs(self,action)
        if action == 'create' or action == 'change':
            self._defineImportArgs()
            self.parser.add_option("-v", "--version", dest="version", 
                                   help="set the version number for this project "
                                   + "[default is 0.0.0]")
            self.parser.set_defaults(version='')
        if action == 'create':
            self.parser.set_defaults(language='cxx', 
                                     clonelib=True, outdir=".", 
                                     package="_unset", maketemplate="gmake")

            self.parser.add_option("-o", "--output-dir", dest="outdir", 
                                   help="directory in which to create the new "
                                   + "project [default is .]")

            self.parser.add_option("-p", "--package", dest="package", 
                                   help="package name [default is to use the "
                                   + "project name as the package]")

            self.parser.add_option("-l", "--language", dest="language", 
                                   help="default language for project impls "
                                   + "unless overridden [default is cxx]")

            self.parser.add_option("-m", "--make-template", dest="maketemplate", 
                                   help="project build system template to "
                                   + "use [default is gmake]")
            self._defineDpathArgs()
        elif action == 'display':
            self.parser.add_option('-f', '--files', dest="myfiles", action='store_true',
                               help="Show a list of user-editable files, which " 
                               + "can be used as input for revision control operations.")
            self.parser.add_option('-d', '--dirs', dest="mydirs", action='store_true',
                               help="Show a list of directories containing " 
                               + "user-editable files; this can be used as input "
                               + "for revision control operations.")
            self.parser.add_option('-r', '--release-files', dest="releasefiles", action='store_true',
                                   help="Display a list of files needed in a source repository for "+
                                   "a release.")
            self.parser.set_defaults(mydirs=False, myfiles=False, releasefiles=False)
        #elif action == 'remove':
        elif action == 'rename':
            pass
        elif action == 'config':
            self._defineConfigArgs()
        elif action == 'change':
            self._defineDpathArgs()
            pass
        elif action == 'update':
            self._defineUpdateArgs()
        elif action == 'edit':
            self._defineEditArgs()
        else:
            err('Project verb "' + action + '" NOT implemented yet.', 3)

        return

    #------------------------------------------------
    def processArgs(self, action):
        """ Validates and if necessary canonicalizes the command line arguments for
        this subject, which are parsed into self.options.
        Exits nonzero if user gives bad input.
        """
        BVertex.processArgs(self,action)
        if action == 'create':
            if len(self.args) < 1:
                self.usage(exitcode=2,errmsg='[create project]: A project name ' \
                           + 'is required for create project\nbocca help create project')
            
            self.symbol = self.args[-1]  # project name
            
            self.projectName = self.symbol
            if self.options.package == "_unset":
                self.options.package = self.args[0].replace('-','').replace('_','')
                while self.options.package.endswith('.'): 
                    self.options.package = self.options.package.rstrip('.')
                m = re.match(r'[A-Za-z][A-Za-z0-9]*',self.options.package)
                if not m or not (m.start() == 0 and m.end() == len(self.options.package)):
                    err('Invalid SIDL package name derived from project name, '
                        + 'please use the -p option to specify a default package '
                        + 'name (containing only letters or numbers) or pick a '
                        + 'different project name.')
                
            status, self.options.language = cct._validate.language(self.options.language)
            if status:
                self.usage()
        elif action == 'rename':
            if len(self.args) != 1:
                self.usage(exitcode=2,errmsg='[rename project] the new project ' \
                           + 'name was not specified')
            self.newname = self.args[0]
        elif action == 'display':
            if len(self.args) > 0 and self.symbol is None:
                self.symbol = self.args[-1]   # project name
            elif self.projectName is not None:
                self.symbol = self.projectName # which is set earlier in the BVertex constructor
        elif action == 'config': 
            self._processConfigArgs()
        elif action == 'change':
            pass
        elif action == 'update':
            pass
        elif action == 'edit':
            if len(self.args) > 0:
                self.editLevel = self.args[-1]

        if action == 'create' or action == 'change':
            if self.options.version:
                m = re.match(r'\A\d+\.\d+\.\d+\Z', self.options.version)
                if not m: err('Invalid project version, version numbers must '
                              + 'be of the form X.Y.Z, where X, Y, and Z are numbers')
                self.version = self.options.version
            else:
                if action == 'create': self.version = '0.0.0'

            if self.options.sidlimports:
                self._processImportArgs()
        return
        
    #------------------------------------------------
    def create(self):
        """create project [options] projectName

        Creates a project with the specified name.
        """
        import cct._cores

        print >> DEBUGSTREAM, "Project.create called with options ", \
            str(self.options) , " leaving args " , str(self.args)
    
        projectName = self.symbol
        

        # In init only, get the configuration from the template directory, for
        # all other subjects, the project's copy will be used
        templateConfigFile = os.path.abspath(os.path.join(self.modulePath, 
                                                          'templates', 
                                                          'project.defaults'))
        self.defaults = BoccaConfigParser()
        self.defaults.readfp(open(templateConfigFile,'r'))
        
# TODO: document (non-standard) exit codes for Bocca

        # Check if outdir exists and is writable, if not create it.
        if os.path.exists(self.options.outdir):
            mode = os.stat(self.options.outdir)[stat.ST_MODE] 
            if stat.S_ISDIR(mode):
                if not bool(mode & stat.S_IWRITE):
                    err('[create project]: specified output directory name, ' 
                        + self.options.outdir + ', is not writable.')
                    
            else:
                err('[create project]: specified output directory name, ' 
                    + self.options.outdir + ', is not a directory.')
     
        projectDir = os.path.abspath(os.path.join(self.options.outdir,projectName))
        fileManager.setProjectName(projectName)
        fileManager.setProjectDir(projectDir)
        
        # Check if proj already exists in outdir and exit w/error if so, otherwise create it
        if os.path.exists(projectDir):
            err('[create project]: cannot create project in ' + projectDir \
                + ': path already exists.',2)
            
        self.setDir(projectDir)
        
        # The following doesn't create outdir if it already exists, only projectDir.
        # It does create a .bocca subdirectory in the outdir above projectDir.
        dirToAdd = os.path.abspath(os.path.join(os.getcwd(),self.options.outdir))
        try: 
            if not os.path.exists(dirToAdd): os.mkdir(dirToAdd)
        except: print >>DEBUGSTREAM, '[create project] specified output directory ', \
            dirToAdd, ' already exists (that''ok)'
        
        print >> DEBUGSTREAM, '[create project] creating project in directory ', \
            projectDir
    

        # Copy directory structure (build) template to new project
        templateDir = os.path.join(self.modulePath, 'templates', 
                                   self.options.maketemplate)
        
        # First, check to make sure template exists
        if not os.path.exists(templateDir):
            x = os.listdir(os.path.join(self.modulePath,'templates'))
            templates=''
            for f in x: 
                if os.path.isdir(os.path.join(self.modulePath,'templates',f)):
                    templates += f + ', '
            templates = templates[:-2]
            err('invalid build template name specified: %s.\nAvalable templates are: %s.' \
                % (self.options.maketemplate, templates))
            
        # Create project directory
        try:
            fileManager.mkdir(projectDir)
        except IOError,e:
            err('could not create project directory ' + projectDir + ': ' + str(e))
        
        # Copy build template to new project directory
        os.path.walk(templateDir,
                     _copyBuildTemplateFunc,
                     arg={'projectDir':projectDir,'templateDir':templateDir,
                          'skip':['python','__init__.py']})
        # Load the build template python module and instantiate the builder and location manager classes
        self.loadBuildTemplate(os.path.join('templates', self.options.maketemplate))
        print >>DEBUGSTREAM, '[create project] loaded the build template from ', \
            templateDir
               
        # Try to get number of cores for parallel builds
        numcores = cct._cores.get_num_cores()
        
        # Specialize build template for this project
        self.getBuilder().specializeTemplate()
        
        # 1) Create visible BOCCA directories for project metadata that would normally 
        # be under revision control.         
        # 2) Create hidden metadata directories (.bocca) whose contents would
        # normally *not* be under revision control
        addProjectMetadirs(projectName,topDir=projectDir,rootDir=projectDir)
        
        # Put the bocca configuration file in the top-level BOCCA subdir
        defaultsFile = os.path.join('BOCCA',projectName + '.defaults')
        projectConfigFile = os.path.abspath(os.path.join(projectDir,defaultsFile))
        self.setAttr('defaultsFile', defaultsFile)
        try: 
            fileManager.copyfile(templateConfigFile,projectConfigFile)
        except IOError,e: 
            err('could not create project configuration file ' 
                + projectConfigFile + ': ' + str(e))
        
        # Load the defaults file and set the default language for the project
        if projectConfigFile is not None and os.path.exists(projectConfigFile):
             configfp = open(projectConfigFile,'r')
             if configfp is not None: 
                     self.defaults.readfp(configfp)
                     configfp.close()
        self.defaults.set('Babel','default_language',self.options.language)
        dpathdata = self._processDpathOptions()
        self._updateDpaths(dpathdata,defaults=self.defaults)
        self.defaults.write(fileManager.open(projectConfigFile,'w'))
        self.setDefaultLanguage(self.options.language)
        
        # Create project graph and add self to it
        graph = BGraph(name = projectName, path = projectDir, 
                       modulePath = self.modulePath)
        graph.add_v(self)
        print >> DEBUGSTREAM, '[create project] Project graph created successfully'
        globals = Globals()
        print >> DEBUGSTREAM, '[create project] Globals created'
        globals.graphs[self.symbol] = graph
        globals.projects[self.symbol] = self
   
        self.addNestedPackages(self.options.package)
        print >> DEBUGSTREAM, '[create project] Added packages successfully: ', \
            self.options.package
        self.setAttr('defaultPackage', self.options.package)
        
        if self.sidlImports: self.handleSIDLImports(mergeBuildfiles=self.options.mergebuilds)
          
        # Pickle project graph in default location, i.e., projectDir/.bocca/projectName.pickle
        # This is only necessary in the project create method, all other commands don't need 
        # to save the graph explicitly since it's done in the dispatcher upon successful command completion.
        graph.save()
        
        print >> DEBUGSTREAM, '[craete project] graph name = ', graph.name, \
            ', path=', graph.path, ', contents:', graph
        print 'The project was created successfully in ' + projectDir
        return 0

    def change(self):
        """change project [options] projectName

        """
        # Check whether component already exists in project
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        self.validateExistingSymbol(pgraph)
            
        if self.sidlImports: self.handleSIDLImports(mergeBuildfiles=self.options.mergebuilds)
        
        if self.options.version: self.version = self.options.version
        dpathdata = self._processDpathOptions()
        self._updateDpaths(dpathdata)
        
        self.saveProjectState(pgraph, graphviz=True)
            
        print >>DEBUGSTREAM, 'change ' + self.kind + ' returning with code 0'

        return 0
    
    def remove(self):
        """remove project [options] projectName

        """

        return 1
    
    def rename(self):
        """rename project [options] newProjectName
    
        Renames the project in the current directory. If multiple 
        projects are present in the same directory, use 
           'bocca -p <projName> rename project <newProjectName>' 
        to disambiguate.
        """
        
        if self.newname is None:
            self.usage(2,"[rename project] the new project name was not specified.")
            
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        # Save the old name
        if not self.options.force:
            # Ask for confirmation
            response = raw_input('Are you sure you want to change the name of this project "' 
                                 + self.symbol + '" to "' + self.newname + '" (y/n) ? [n] ')
            if not str(response).lower() in ['yes', 'y']:
                return 0
        # Now change the name in the various files that refer to it
        # First, save current path
        curdir = os.path.realpath(os.path.curdir).replace(self.symbol,self.newname)
        oldProjectDir = self.getDir()
        oldProjectName = self.symbol
        oldProjectVersion = self.version
        projectParentDir = os.path.abspath(os.path.join(self.getDir(),'..'))
        projectDir = os.path.join(projectParentDir,self.newname)
                        
        # Remove metafiles
        removeProjectMetafiles(self.symbol,topDir=oldProjectDir,rootDir=oldProjectDir)
        
        # Rename the project defaults file
        try:
            oldProjDefaults = os.path.join(oldProjectDir,'BOCCA', 
                                           oldProjectName+'.defaults')
            newProjDefaults = os.path.join(oldProjectDir,'BOCCA', 
                                           self.newname+'.defaults')
            fileManager.rename(oldProjDefaults, newProjDefaults)
            self.setAttr('defaultsFile', 
                         os.path.join(projectDir, 'BOCCA', 
                                      self.newname + '.defaults'))
        except IOError,e:
            err('could not rename project defaults file ' 
                + oldProjDefaults + ': ' + str(e))        
        
        # Remove pickle file if any
        if os.path.exists(os.path.join(oldProjectDir,'.bocca', 
                                       oldProjectName+'.pickle')):
            try:
                fileManager.rm(os.path.join(oldProjectDir,'.bocca', 
                                            oldProjectName+'.pickle'))
            except IOError,e:
                warn('could not remove pickle file for project ' 
                     + oldProjectName + ': ' + str(e))
        # Remove ASCII serialization file if any
        try:
            fileManager.rm(os.path.join(oldProjectDir,'BOCCA', oldProjectName+'.dat'))
        except IOError,e:
            warn('could not remove ASCII serialization file for project ' 
                 + oldProjectName + ': ' + str(e))

        self.setAttr('oldName', self.symbol)
        pgraph.renameVertex(self,self.newname)
        self.projectName = self.newname
        for v in pgraph.v.values():
            v.projectName = self.projectName
        
        slist = pgraph.findSymbol(self.newname,kind='package')
        if len(slist) == 0: self.addNestedPackages(self.newname,g=pgraph)
            
        # Change default package name to match new project name
        self.setAttr('defaultPackage', self.newname)

        # Rename top-level directory
        os.chdir(projectParentDir)
        print >>DEBUGSTREAM, 'Changed working directory to ' + projectParentDir
        
        if os.path.exists(projectDir):
            err('could not rename project, directory exists: ' + projectDir)
        try:
            # TODO: need to make this undoable, too
            shutil.move(oldProjectDir,projectDir)
        except OSError,e:
            err('could not rename the top-level project directory: ' + str(e))
        fileManager.setProjectDir(os.path.join(projectParentDir,self.newname))
                                  
        # Go back to the same relative location in the new project directory
        os.chdir(curdir)
        print >>DEBUGSTREAM, 'Changed working directory to ' + curdir

        # Add new metafiles
        print >>DEBUGSTREAM, 'Setting project directory to ' + projectDir
        self.setDir(projectDir)
        print >>DEBUGSTREAM, 'Adding project metadirs'
        addProjectMetadirs(self.symbol,topDir=projectDir,rootDir=projectDir)
        
        print >>DEBUGSTREAM, 'Invoking builder rename...'
        self.getBuilder().rename(oldProjectName, self.symbol, oldProjectVersion, self.version, oldProjectDir)

        # Change the name of this graph and save it
        print >>DEBUGSTREAM, 'About to save new project graph.'
        pgraph.name = self.newname
        pgraph.path = projectDir
        pgraph.save()
        
        print >>DEBUGSTREAM, 'saved new graph: ' + str(pgraph)
        
        project,graph = Globals().renameProject(oldProjectName,self.symbol)   
        return 0
    
    def display(self):
        """display project [projectName]
        
        """
        if not validSubdir(self.symbol,os.path.abspath(os.getcwd())):
            err('Specified project, ' + self.symbol + ', not found in this directory.')
        print >>DEBUGSTREAM,'Loaded project', self.symbol, 'in directory', self.getDir()
        
        pgraph = Globals().getGraph(self.symbol)
        
        if self.options.mydirs:
            print ' '.join(self._getDirList())
        
        if self.options.myfiles:
            print ' '.join(self._getFileList())

        if self.options.releasefiles:
            print ' '.join(self._getReleaseFileList())

        if not (self.options.mydirs or self.options.myfiles or self.options.releasefiles):
            print 'Project', self.symbol, self.data, ':', pgraph
        
            # Dot file:
            try:
                pgraph.saveGraphvizFile()
            except:
                warn('Could not create GraphVis (dot) project visualization file: ' 
                     + os.path.join(self.getDir(),'BOCCA',self.symbol+'.dot'))
         
        # For debugging cycles       
        #for s in pgraph.find_cycles():
        #    print 'Cycle: ', [v.symbol for v in s]

        return 0
    
    def config(self):
        '''config project [options]
        
        Displays or modifies the contents of the project defaults file: 
            <project dir>/BOCCA/<project name>.defaults
        '''
        sysconfigfile= os.path.join(self.modulePath,"templates","project.defaults")
        if not self.options:
            self.parser.print_help()
            return 0

        # update
        if self.options and self.options.configupdate:
            print "Updating project configuration from "+sysconfigfile
            projname, projdir = getProjectInfo()
            config=self.getDefaults()
            config.read([sysconfigfile])
            
            buildFilesOnly = True
            #if self._b_babelVersion != autoconfvars.babelVersion:
            #    warn('Using Bocca configured with Babel ' + autoconfvars.babelVersion 
            #         + ', which is incompatible with the Babel version used when creating this project (' 
            #         + self._b_babelVersion + ')')
            
            # Regenerate all build system files
            graph = Globals().getGraph(self.symbol)
            self.getBuilder().changed(list(graph.v.values()))
            self.getBuilder().update(buildFilesOnly=buildFilesOnly)
            
            return
        # remove
        if (not self.options.killvar is None) and len(self.options.killvar) >0:
            killvar = self.options.killvar
            config=self.getDefaults()
            if killvar.find(":") >= 0:
                sec,key = killvar.split(":")
                if config.has_section(sec):
                    try:
                        config.remove_option(sec,key)
                    except Exception, e:
                        print str(e)
            else:
                try:
                    d=config.defaults()
                    del d[killvar]
                except Exception, e:
                    print str(e)
            return 0
        # set
        if (not self.options.setvar is None) and len(self.options.setvar) >0:
            setvar=self.options.setvar
            setval=self.options.setval
            if setval is None:
                err('Nothing specified for --value with --set-var=' + setvar)
                return 1
            config=self.getDefaults()
            if setvar.find(":") >= 0:
                try:
                    sec,key = setvar.split(":")
                    if not config.has_section(sec):
                        config.add_section(sec)
                    config.set(sec,key,setval)
                except:
                    pass
            else:
                try:
                    d=config.defaults()
                    d[setvar]= setval
                except Exception, e:
                    print str(e)
            return 0
        # get
        if (not self.options.var is None) and len(self.options.var) >0:
            var=self.options.var
            config=self.getDefaults()
            if var.find(":") >= 0:
                try:
                    sec,key = var.split(":")
                    x=config.get(sec,key)
                    print x.strip('"')
                except:
                    pass
            else:
                key=var
                for i in config.sections():
                    try:
                        x=config.get(i,var)
                        print x.strip('"')
                    except:
                        pass
                d=config.defaults()
                try:
                    x=d[var]
                    print x.strip('"')
                except:
                    pass
            return 0
        # print system values
        if self.options.system:
            sysconfig = BoccaConfigParser()
            sysconfig.read(sysconfigfile)
            print "# From: "+sysconfigfile
            d=sysconfig.defaults()
            for k,v in d:
                print k, "=" ,v
            for i in sysconfig.sections():
                print "["+ i+ "]"
                for (j, jval) in sysconfig.items(i):
                    print j, "=", jval
            if not self.options.project:
                return 0
            print "####### project configuration #"
        # print project values
        if self.options.project:
            projname, projdir = getProjectInfo()
            config = self.getDefaults()
            d=config.defaults()
            for k,v in d:
                print k, "=" ,v
            for i in config.sections():
                print "["+ i+ "]"
                for (j, jval) in config.items(i):
                    print j, "=", jval
            return 0
 
        self.parser.print_help()
        return 0

    def update(self):
        '''update project [options]
        
        The update command supports options for updating or recovering the 
        default build system files, generating sample cvs or svn commands 
        (but not running cvs or svn), and other functionality for managing 
        bocca upgrades and interactions with revision control systems.
        '''
        print >>DEBUGSTREAM, 'project update: '
        
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        if self.options:
            if self.options.update_build:
                pass
        
            if self.options.store_graph:
                self.saveProjectState(pgraph, graphviz=True)

        # Regenerate build files
        self.getBuilder().changed(list(pgraph.v.values()))
        self.getBuilder().update(buildFilesOnly=True)
        
        #self.parser.print_help()
        return 0

    def edit(self):
        '''edit project [components|ports] <--build-rules|--build-vars>

        The edit command provides support for editing the bocca project's top-level
        makefiles, including makefiles for components and ports.'''
        print >>DEBUGSTREAM, 'project edit: '

        # Set the index for getting the right makefile
        index = -1
        if self.options.editrules:
            index = 1
        if self.options.editvars:
            index = 0

        if index == -1:
            self.parser.print_help()
            err('edit project requires one of: --build-rules, --build-vars')

        makefileInfo = self.getLocationManager().getUserBuildfilesLoc(self)
        localMakefile = makefileInfo[1][index]

        if self.editLevel is not None:
            if self.editLevel == 'components':
                localMakefile = os.path.join(self.getLocationManager().getComponentLoc()[0], localMakefile)
            elif self.editLevel == 'ports':
                localMakefile = os.path.join(self.getLocationManager().getPortLoc()[0], localMakefile)
            else:
                self.parser.print_help()
                err('unrecognized edit type: '+self.editLevel)

        makefile = os.path.join(self.getDir(), localMakefile)

        if not makefile:
            err('Cannot find file: %s' % str(makefile))
        print >>DEBUGSTREAM, 'editing '+str(makefile)
    
        changed = False
        try:
            changed = editFile(makefile, False, None)
        except:
            err('Could not edit file: %s' % str(makefile))

        if changed:
            self.getBuilder().changed([self] + list(self.dependents()))
            self.getBuilder().update()

        return 0
        
    
    def __str__(self): return 'project: ' + self.symbol + ' ' + self.version

#----- End BVertex interface
#------------------------------------------------------------------------------------------

    # The following methods are specific to Project (not part of the BVertex interface)
    def addNestedPackages(self, symbol, package=None, version=None, g=None):
        '''Adds several nested packages simulaneously in project and return the innermost one.'''

        from cct.package import Package
        
        if g is None: g = Globals().getGraph(self.symbol)
        packages = symbol.split('.')
        fullsymbol = packages[0]
        pkg = g.findSymbol(symbol=fullsymbol,kind='package')

        if len(pkg) == 0: 
            top = Package(symbol=fullsymbol, project=self)
        elif len(pkg) > 1:
            err('ambiguous package name encountered: ' 
                + fullsymbol + '(possibilities are ' + str(pkg) + ')')
        else:
            top = pkg[0]
        
        edge = BEdge(self, top, g)

        parent = top
        if len(packages) > 1:
            for i in range(1,len(packages)):
                fullsymbol = fullsymbol + '.' + packages[i]
                pkgs = g.findSymbol(symbol=fullsymbol,kind='package')
                
                if len(pkgs) == 0:
                    if package and fullsymbol == package.symbol:
                        pkg = package
                    else:
                        pkg = Package(symbol=fullsymbol, project=self, version=version)
                    
                    if parent.symbol != pkg.symbol:
                        edge = BEdge(parent, pkg, g)
                elif len(pkgs) == 1:
                    pkg = pkgs[0]
                else:
                    err('ambiguous package name encountered: ' 
                        + str(pkg) + '(possibilities are ' + str([str(x.name) for x in pkgs]) + ')')
                parent = pkg
        else: pkg = top
        return pkg

    def getName(self): return self.symbol
    
    def getDir(self): return self.dir
    def setDir(self, dir): self.dir = dir
    
    def getDefaults(self): 
        '''Returns an instance of ConfigParser contaning project defaults settings.'''
        if self.defaults is None: self.loadDefaults()
        elif len(self.defaults.sections()) is 0: self.loadDefaults()
            
        return self.defaults
    
    def getVertexList(self, kinds=['component'], ignore_action=''):
        '''Returns a list of all vertices of the specified kind in the project'''
        vlist =  []
        project, graph = Globals().getProjectAndGraph(self.symbol)

        #if ignore_action:
        #    graph = graph.filter_copy(ignore_action)
        #    project = graph.findSymbol(self.symbol, kind='project')[0]

        allvertices = BGraph.breadth_first_search(project, ignore_action=ignore_action)[1:]
        for v in allvertices:
            if v.kind in kinds:
                vlist.append(v)

        return vlist
    
    def setup(self,action,args):
        self.parser = OptionParser(getattr(self, action).__doc__) 
        self.defineArgs(action)
        self.options, self.args = self.parser.parse_args(args)
        self.processArgs(action)
        return
    
    def getDefaultsFilePath(self):
        mydir = self.getDir()
        if mydir: return os.path.abspath(os.path.join(mydir, self.getAttr('defaultsFile')))
        return ''
    
    def loadDefaults(self):
        print >>DEBUGSTREAM, "CALLING loadDefaults"
        if self.defaults: return self.defaults
        print >>DEBUGSTREAM, "CALLING loadDefaults actually doing work"
        self.defaults = BoccaConfigParser()
        mydir = self.getDir()
        
        if mydir is not None:
            defaultsFile = os.path.abspath(os.path.join(mydir, self.getAttr('defaultsFile')))
            print >>DEBUGSTREAM, 'Project: Loading defaults from ', defaultsFile
            if defaultsFile is not None and os.path.exists(defaultsFile):
                 configfp = open(defaultsFile,'r')
                 if configfp is not None: 
                     import ConfigParser
                     try:
                         self.defaults.readfp(configfp)
                     except ConfigParser.ParsingError,e:
                         print >>sys.stderr, \
                            'Bocca ERROR: Could not load project ' \
                            + 'defaults file ' + defaultsFile + ': ' + str(e)
                         sys.exit(1)
                     except:
                         print >>sys.stderr, 'Bocca ERROR: Error parsing project ' \
                               + 'defaults file ' + defaultsFile  \
                               + ', check for syntax errors.'
                         sys.exit(1)
                     print >>DEBUGSTREAM, 'Project: Successfully loaded defaults ' \
                               + 'from ', defaultsFile
                     if CFGDUMP:
                         print '. Contents:'
                         self.defaults.write(DEBUGSTREAM)
            else:
                print >>sys.stderr, 'Bocca ERROR: could not load project ' \
                               + 'defaults file: ' + defaultsFile 
                if 'BOCCA_DEBUG' in os.environ.keys() and os.environ['BOCCA_DEBUG'] == '1': 
                    traceback.print_stack()
                    sys.exit(errcode)
               
        return self.defaults 

    def saveDefaults(self):
        print >>DEBUGSTREAM, "CALLING saveDefaults"
        if self.defaults:
            try:
                fp = fileManager.open(os.path.join(self.getDir(),
                                                   self.getAttr('defaultsFile')),'w')
            except:
                err('Could not save project defaults file: ' 
                    + os.path.join(self.getDir(),self.getAttr('defaultsFile')))
            self.defaults.write(fp)
            fp.close()
        pass
    
    def loadBuildTemplate(self,buildTemplateDir=None):
        '''Load the python modules that specify the directory structure 
        and build interface for the build template used in this project.
        '''
        if buildTemplateDir is not None:
            self.setAttr('buildTemplateDir', buildTemplateDir)
        modulePath = os.path.abspath(os.path.join(self.modulePath, 
                                                  self.getAttr('buildTemplateDir'),
                                                  'python'))
        
        # Load the LocationManagerInterface implementation
        try:
            (file,filename,description) = imp.find_module('locations',[modulePath])
            locations = imp.load_module('locations', file, filename, description)
        except ImportError,e:
            err('Could not import locations module from ' + modulePath + ': ' + str(e))
        try:
            LocationManagerClass = getattr(locations,'LocationManager')
        except AttributeError,e:
            err('Could not find LocationManager class for current build template in ' 
                + modulePath+ ': ' + str(e))
            
        locationManager = LocationManagerClass(self)
        self.locationManager = locationManager

    
        # Load the builder interface implementation
        try:
            (file,filename,description) = imp.find_module('builder',[modulePath])
            builder = imp.load_module('builder', file, filename, description)
        except ImportError,e:
            err('Could not import builder module from ' + modulePath+ ': ' + str(e))
        try:
            BuilderClass = getattr(builder,'Builder')
        except AttributeError,e:
            err('Could not find Builder class for current build template in ' 
                + modulePath+ ': ' + str(e))
            
        builder = BuilderClass(modulePath, self)
        self.builder = builder
        return 0

    def setDefaultLanguage(self, lang):
        status, l = cct._validate.language(lang)
        if status:
            err('Specified default language is not supported in this project: ' + \
                lang + '. Valid languages are: ' 
                + ','.join(self.locationManager.getLanguages()))
        self.defaults.set('Babel','default_language',l)
        return
        
    def getDefaultLanguage(self):
        return self.defaults.get('Babel','default_language')
    
    def getDefaultValueQuietly(self, option, section='Project'):
        '''Returns the project.defaults value corresponding to this key or None otherwise.
           Without the whining.'''
        if not self.defaults: self.loadDefaults()
        try:
            optstr = self.defaults.get(section,option)
            if optstr.find('#') >= 0:
                optstr = re.split('#', optstr)[0]  # get rid of comments
        except:
            return None
        return optstr

    def getDefaultValue(self, option, section='Project'):
        '''Returns the project.defaults value corresponding to this key or None otherwise'''
        if not self.defaults: self.loadDefaults()
        try:
            optstr = self.defaults.get(section,option)
            if optstr.find('#') >= 0:
                optstr = re.split('#', optstr)[0]  # get rid of comments
        except:
            warn('Option "%s" not found in section "%s" of the project.defaults file' % (option, section))
            return None
        return optstr

    def getDefaultSectionKeys(self, section='Project'):
        if not self.defaults.has_section(section): return []
        return self.defaults.options(section)
    
    def setDefaultValue(self, option, val, section='Project'):
        '''Sets the default value for the given option''' 
        if not self.defaults: self.loadDefaults()
        if not self.defaults.has_section(section): self.defaults.add_section(section)
        try:
            if option.count(','): options=option.split(',')
            else: options=[option]
            for opt in options:
                self.defaults.set(section,opt,val)
            print >>DEBUGSTREAM, 'setting defaults value in section [' \
                + section + ']: ' + opt + ' = ' + val
        except:
            err('Could not set option in project.defaults file in '
                + 'section %s: %s = %s' % (section,option,val))
        return 0
    
    def removeDefaultValue(self, option, section='Project'):
        '''Sets the default value for the given option''' 
        if not self.defaults: self.loadDefaults()
        if not self.defaults.has_section(section): return 0
        try:
            self.defaults.remove_option(section,option)
            print >>DEBUGSTREAM, 'removed defaults value in section [' \
                + section + ']: ' + option 
        except:
            err('Could not remove option in project.defaults file in '
                + 'section %s: %s' % (section,option))
        return 0
    
    def getBuilder(self):
        return self.builder
    
    def getLocationManager(self):
        return self.locationManager

    
    #====================================================================
    # Private Project methods
    def _defineConfigArgs(self):
        print >>DEBUGSTREAM, "# calling _defineConfigArgs"
        if self.parser.has_option("--dump"):
           print >>DEBUGSTREAM, "# calling _defineConfigArgs again ignored"
           return
        self.parser.add_option('--dump', dest = 'project', action = 'store_true',
                               help = 'display the bocca project settings')
        self.parser.add_option('--system', dest = 'system', action = 'store_true',
                               help = 'display the bocca system-wide default settings')
        self.parser.add_option('-u', '--update', dest = 'configupdate', action = 'store_true',
                               help = 'merge the system defaults into the project '
                               + 'settings and regenerate project-specific ' 
                               + 'build files. Needed after a bocca project is '
                               + 'relocated or after changes to the CCA environment')
        self.parser.add_option('-q', '--query-var', dest = 'var', action = 'store',
                               help = 'print the value of VAR in the project. '
                               + 'VAR may be section:var or just var to match '
                               + 'all sections')
        self.parser.add_option('-r', '--remove-var', dest = 'killvar', action = 'store',
                               help = 'delete the var from the project. VAR must '
                               + 'be section:var or a global default var.')
        self.parser.add_option('-s', '--set-var', dest = 'setvar', action = 'store',
                               help = 'set the value of VAR in the project. VAR '
                               + 'may be section:var or just var for a global default')
        self.parser.add_option('-v', '--value', dest = 'setval', action = 'store',
                               help = 'the value for the set-var in the project.')
        self.parser.set_defaults(project=False, system=False, configupdate=False, 
                                 var=None, setvar=None, setval=None, killvar=None)
        return
    
    def _processConfigArgs(self):
        return


    def _defineUpdateArgs(self):
        self.parser.add_option('-b', '--build', dest="update_build", action='store_true',
                               help="Update all build system files with the "
                               + "ones from the bocca template; old files are "
                               + "backed up. [NOT AVAILABLE YET]")
        self.parser.add_option('--revert-build', dest="revert_build", 
                               action='store_true', help="Revert all build "
                               + "files to the last version used before using "
                               + "update --build. [NOT AVAILABLE YET]")
        self.parser.add_option('--cvs-add', dest="cvs_add", action='store_true',
                               help="Generate cvs add command string for project"
                               + " directories. This does not actually invoke "
                               + "cvs. [NOT AVAILABLE YET]")
        self.parser.add_option('-s', '--store', dest='store_graph', 
                               action='store_true', help="Regenerate the "
                               + "internal project representation (e.g., after "
                               + "upgrading bocca).")
        self.parser.set_defaults(update_build=False, revert_build=False, cvs_add=False)
        return
    
    def _defineImportArgs(self):
        self.parser.set_defaults(sidlimports=[], mergebuilds=True)
        self.parser.add_option('--import-sidl', dest='sidlimports', action='append', 
                               help='A SIDL file from which to import a '
                               + 'specified interface or several interfaces, ' 
                               + 'e.g., --import-sidl="pkg.MySolverInterface,'
                               + 'pkg.MyMatrixInterface:/path/to/file.sidl". ' 
                               + 'If no interface is specified (only the SIDL '
                               + 'filename is given), all packages from '
                               + 'the SIDL file are imported into the ' 
                               + self.kind + '.')
        self.parser.add_option('--no-merge-buildfiles', dest='mergebuilds', action='store_false',
                               help="If the SIDL being imported is from another bocca project, do "
                               + "not merge together build files.")
        pass

    def _defineEditArgs(self):
        self.parser.add_option('-r', '--build-rules', dest='editrules', action='store_true',
                               help="Edit the make.rules.user file")
        self.parser.add_option('-V', '--build-vars', dest='editvars', action='store_true',
                               help="Edit the make.vars.user file")
        self.parser.set_defaults(editrules=False, editvars=False)

        return
    
    def _getDirList(self, fullpath=True):
        dirs = []
        dirs.extend(self.locationManager.getPortLoc())
        dirs.extend(self.locationManager.getComponentLoc())
        dirs.extend(self.locationManager.getExternalLoc())
        dirs.extend(self.locationManager.getSIDLDirs(self))
        for v in self.getVertexList(kinds=['class', 'component']):
            dirs.append(self.locationManager.getImplLoc(v)[0])
        fpdirs = []
        if fullpath:
            for d in dirs: fpdirs.append(os.path.join(self.getDir(),d))
        else: 
            return dirs
        return fpdirs
    
    def _getFileList(self):
        from sets import Set
        files = []
        for v in self.getVertexList(kinds=['interface','port','class','component','enum']):
            files.extend(v._getMyUserFiles())
        makedir, makefiles = self.locationManager.getUserBuildfilesLoc(self)
        for f in makefiles: files.append(os.path.join(self.getDir(),f))
        # remove duplicates
        return list(Set(files))

    def _getReleaseFileList(self):
        from sets import Set

        files = []
        dirs = []

        # Grab directories first; note that the ordering for svn is important here!
        dirs.extend(self._getDirList())

        # Get extra build directories
        builddirs = []
        for v in self.getVertexList(kinds=['interface', 'port', 'class', 'component', 'enum']):
            dir, subdirs = self.locationManager.getExtraDirsLoc(v)
            for d in subdirs:
                builddir = os.path.join(self.getDir(), dir, d)
                builddirs.append(builddir)
                files.extend([os.path.join(builddir, f) for f in filter(lambda x: not (x == 'BOCCA' or x[0] == '.'), os.listdir(builddir))])
        dir, subdirs = self.locationManager.getExtraDirsLoc(self)
        for d in subdirs:
            builddir = os.path.join(self.getDir(), d)
            builddirs.append(builddir)
            files.extend([os.path.join(builddir, f) for f in filter(lambda x: not (x == 'BOCCA' or x[0] == '.'), os.listdir(builddir))])

        # Get glue directories
        for v in self.getVertexList(kinds=['class', 'component']):
            dir, flist = self.locationManager.getGlueLoc(v, v._b_language)
            gluedir = os.path.join(self.getDir(), dir)
            dirs.append(gluedir)
            files.extend([os.path.join(gluedir, f) for f in filter(lambda x: not (x == 'BOCCA' or x[0] == '.'), os.listdir(gluedir))])

        dirs.extend(list(Set(builddirs)))

        # Get files
        files.extend(self._getFileList())

        # Get files for building
        for v in self.getVertexList(kinds=['interface', 'port', 'class', 'component', 'enum']):
            dir, flist = self.locationManager.getBuildfilesLoc(v)
            for f in flist:
                files.append(os.path.join(self.getDir(),dir, f))
        dir, flist = self.locationManager.getBuildfilesLoc(self)
        for f in flist:
            files.append(os.path.join(self.getDir(), f))

        files = list(Set(files))

        return (dirs + files)

    def cleanExternal(self, sym):
        '''
        Checks the project for references to the external symbol 'sym', and removes
        information from the defaults and external/sidl cache if necessary.
        '''

        from cct._util import BFileManager

        print >>DEBUGSTREAM, "Cleaning external symbol: ",sym

        graph = Globals().getGraph(self.projectName)
        vertices = graph.bocca_breadth_first_search(self,
                                                    actions=['', 'extends', 'implements', 'requires', 'contains'])

        externals = []
        for v in vertices:
            externals.extend(v._b_externalSidlFiles.keys())

        if sym in externals:
            return

        fileNames = [file.split('/')[-1] for file in self.getDefaults().get('External', sym).split(',')]
        self.getDefaults().remove_option('External', sym)
        
        externalFiles = []
        for item in self.getDefaults().items('External'):
            externalFiles.extend([file.split('/')[-1] for file in item[1].split(',')])

        dir = os.path.join(self.getDir(), 'external', 'sidl')
        for file in set(fileNames) - set(externalFiles):
            BFileManager().rm(os.path.join(dir, file))
    
#------------- Methods private to Project (should not be called by other classes)
        
def _copyBuildTemplateFunc(arg,dirname,fnames):
    '''Copy files from project template to project.'''
    dirsToAvoid = Globals().getDirsToAvoid()
    projDir = arg['projectDir']
    templateDir = arg['templateDir']
    skip = arg['skip']  # list of relative paths (to proj. root) to skip
    
    dirs = dirname.split(os.path.sep)
    for d in dirsToAvoid: 
        if d in dirs: return
        
    prefix = os.path.commonprefix([templateDir, dirname])
    relativePath = dirname
    if prefix != '': relativePath = dirname.replace(prefix,'').lstrip(os.path.sep)
    else: err('invalid template path encountered: ' + dirname)
    if relativePath in skip:
        print >>DEBUGSTREAM, 'project copy template, skipping directory: ' \
            + relativePath
        return
    
    targetDir = os.path.join(projDir,relativePath)
    if not os.path.exists(targetDir):
        try:
            fileManager.mkdir(targetDir)
        except:
            err('could not copy build template, error creating directory ' 
                + targetDir)
    flist = os.listdir(dirname)
    for f in flist:
        if f in skip: continue
        ff = os.path.join(dirname,f)
        if os.path.isfile(ff):
            targetFile = os.path.join(targetDir,f)
            try:
                shutil.copy(ff,os.path.join(targetDir,f))
            except:
                err('could not copy build template, error copying file ' 
                    + ff + ' to ' + targetFile)
    pass

if __name__ == "__main__":
    project, pgraph = getProject()
    if project is not None:
        pname = project.getName()
        pdir = project.getDir()
#        name,dir = project.getInfo()
        Project(args=sys.argv,project=project,symbol=pname).usage()
    else:
      sys.exit(err('No project found in current directory'))
