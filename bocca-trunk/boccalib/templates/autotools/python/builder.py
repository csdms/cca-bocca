import os, re, fileinput, string, random
from sets import Set
import builders.builder as builderTemplate
from cct._err import *
from cct._file import *
from cct._debug import DEBUGSTREAM, WARN
from cct._util import fileManager, Globals, addProjectMetadirs, getPythonVersion, getHash
from cct.project import Project
from splicers.Operations import mergeFileIntoString

class Builder(builderTemplate.BuilderDefault):
    def __init__(self, modulePath, project):
        '''Constructor
        @param modulePath the directory containing the implementation of the Builder implementation.
        '''
        # The parent constructor sets the self.locationManager variable
        builderTemplate.BuilderDefault.__init__(self,modulePath, project)
        self.local_lib_path = os.path.join('install','lib')
        self.regen_messages = 'verbose'
        self.autoregenimpls = 'enabled'
        self.autochecksidl = 'disabled'
        self.timing = 'disabled'
        self.colors = 'enabled'
        if self.project is not None:
            defaults = self.project.getDefaults()
            if defaults is not None: 
                if 'Project' in defaults.sections(): 
                    if defaults.has_option('Project','autoregenimpls'): 
                        self.autoregenimpls = re.split('\W+',defaults.get('Project','autoregenimpls'))[0]
                    if defaults.has_option('Project','regen_messages'): 
                        self.regen_messages = re.split('\W+',defaults.get('Project','regen_messages'))[0]
                    if defaults.has_option('Project','autochecksidl'): 
                        self.autochecksidl = re.split('\W+',defaults.get('Project','autochecksidl'))[0]
                    if defaults.has_option('Project','timing'): 
                        self.timing = re.split('\W+',defaults.get('Project','timing'))[0]
                    if defaults.has_option('Project','use_colors'): 
                        self.colors = re.split('\W+',defaults.get('Project','use_colors'))[0]
        pass

    def specializeTemplate(self):
        '''At project creation, specialize the general project template to 
        match the current project.
        '''
        # Set PROJECT_TOP_DIR in make.project file 

        projectName = self.project.getName()
        projectDir = self.project.getDir()
        try: 
            pcpath=os.path.join(projectDir,'utils')
            os.system("mv " + os.path.join(pcpath,"__tcejorp__-config.in") \
                      + " "+  os.path.join(pcpath , projectName+'-config.in'))
            os.system("mv " + os.path.join(pcpath,"__tcejorp__-config.h.in") \
                      + " "+  os.path.join(pcpath , projectName+'-config.h.in'))
            os.system("sed -i1 -e 's|__tcejorp__|" + projectName + "|' " \
                      + os.path.join(projectDir,'configure'))
            if os.path.exists(os.path.join(projectDir,'configure.in')):
                os.system("sed -i1 -e 's|__tcejorp__|" + projectName + "|' " \
                      + os.path.join(projectDir,'configure.in'))
            if os.path.exists(os.path.join(projectDir,'configure.ac')):
                os.system("sed -i1 -e 's|__tcejorp__|" + projectName + "|' " \
                      + os.path.join(projectDir,'configure.ac'))
            os.system("sed -i1 -e 's|@PACKAGE_TARNAME@|" + projectName + "|' " \
                      + "-e 's|@PROJECT_NAME@|" + projectName + "|' " \
                      + "-e 's|@PROJECT_TOP_DIR@|" + projectDir + "|' " \
                      + "-e 's|@MAKE_OPTS@| -j" + str(numcores) + "|' " \
                      + os.path.join(projectDir,'make.project'))
            os.system("sed -i1 -e 's|@PROJECT_TOP_DIR@|" + projectDir \
                        + "|' -e 's|@BOCCA_IO_FLAGS@|-D_BOCCA_STDERR|' " 
                      + os.path.join(projectDir,'buildutils','make.vars.common'))
        except: 
            pass 
        try: 
            os.unlink(os.path.join(projectDir,'configure1'))
            os.unlink(os.path.join(projectDir,'configure.ac1'))
            os.unlink(os.path.join(projectDir,'make.project1'))
            os.unlink(os.path.join(projectDir, 'buildutils', 'make.vars.common1'))
        except: pass
        
        pass

    def rename(self, oldProjectName, newProjectName, oldProjectVersion, 
               newProjectVersion, oldProjectDir):
        '''Update project build system when the project is renamed.'''
        
        # Update the configure and project.make files
        #try: 
        projectDir = self.project.getDir()
        pcpath=os.path.join(projectDir,'utils')
        os.system("cd " + projectDir 
                  + "; mv " + os.path.join(pcpath,oldProjectName + "-config.in")
                  + " utils" + os.path.sep + newProjectName +"-config.in")
        os.system("cd " + projectDir 
                  + "; mv " + os.path.join(pcpath,oldProjectName + "-config.h.in")
                  + " utils" + os.path.sep + newProjectName +"-config.h.in")
        cmd = "cd " + projectDir \
            + "; sed -i1 -e \"s|PROJECT_NAME=" + oldProjectName \
                + "|PROJECT_NAME=" + newProjectName  + "|\" " \
            + "-e \"s|PACKAGE_NAME=\'" + oldProjectName \
                + "\'|PACKAGE_NAME=\'" + newProjectName + "\'|\" " \
            + "-e \"s|PACKAGE_TARNAME=\'" + oldProjectName \
                + "\'|PACKAGE_TARNAME=\'" + newProjectName + "\'|\" " \
            + "-e \"s|PACKAGE_VERSION=\'.*\'|PACKAGE_VERSION=\'" \
                + newProjectVersion + "\'|\" " \
            + "-e \"s|PACKAGE_STRING=\'.*\'|PACKAGE_STRING=\'" \
                + newProjectName + " " + newProjectVersion + "\'|\" " \
            + "-e \"s|" + oldProjectName + "\(.*\) " + oldProjectVersion + "|" \
                + newProjectName + "\1 " + newProjectVersion + "\'|\" " \
            + "-e \"s|doc/" + oldProjectName + "|" + newProjectName + "|\" " \
            + "-e \"s|" + oldProjectName + "-config |" + newProjectName + "-config |\" " \
            + "-e \"s|" + oldProjectName + "-config\.h|" + newProjectName + "-config.h|\" " \
            + " configure"
        os.system(cmd)
        if os.path.exists(os.path.join(projectDir,'configure.in')): configsuf='in'
        else: configsuf='ac'
        os.system("cd " + projectDir \
                  + "; sed -i1 -e 's|PROJECT_NAME=" + oldProjectName \
                    + "|PROJECT_NAME=" + newProjectName  + "|' " \
                  + "-e 's|AC_INIT(" + oldProjectName + ",|AC_INIT(" \
                    + newProjectName + ",|' " \
                  + "-e 's|" + oldProjectName + "-config.h\]|" + newProjectName \
                    + "-config.h\]|' " \
                  + "-e 's|" + oldProjectName + "-config |" + newProjectName \
                    + "-config |' configure." + configsuf)
        os.system("cd " + projectDir \
                  + "; sed -i1 -e 's|PROJECT_NAME=" + oldProjectName \
                    + "|PROJECT_NAME=" + newProjectName  + "|' " \
                  + "-e 's|PACKAGE_TARNAME=.*$|PACKAGE_TARNAME=" \
                    + newProjectName  + "|' " \
                  + "-e 's|PROJECT_TOP_DIR = " + oldProjectDir \
                    + "|PROJECT_TOP_DIR=" + projectDir + "|' make.project")
        print >>sys.stderr, 'Bocca WARNING: Remember to rerun configure.'
        #except: pass 
        try: 
            os.unlink(os.path.join(projectDir,'configure1'))
            os.unlink(os.path.join(projectDir,'configure.' + configsuf + '1'))
            os.unlink(os.path.join(projectDir,'make.project1'))
        except: pass


        pass    
    
    def update(self, buildFilesOnly=False, quiet=False, genSIDL=False):
        '''Given a new project graph, update build information. 
        @param buildFilesOnly: Only update files containing component and port info.
        '''

        status = 0
        if self.changedList or buildFilesOnly:

            if not quiet: 
                if self.changedList:
                    items = ''
                    for i in self.changedList: items += i.symbol + ', '
                    if items.endswith(', '): items = items[:-2]
                    print "Updating makefiles (for " +items + ")..."
                else: print "Updating makefiles..."
            if self.timing == 'enabled': 
                import time
                t1 = time.time()
                
                
            # Check whether project was moved since the last time it was configured.
            moved,oldpath,newpath = self.locationManager.projectMoved()
            if moved:
                print >>DEBUGSTREAM, "This project appears to have moved from " \
                    + str(oldpath) + " to " + str(newpath) +". Updating paths..."
                # Remove make.vars.common to force users to rerun configure
                if os.path.exists(os.path.join(newpath,'buildutils','make.vars.common')):
                    os.unlink(os.path.join(newpath,'buildutils','make.vars.common'))
                # update all babel generated files (basically sed oldpath to newpath)
                os.path.walk(newpath,self._fixPathsInMakefiles,arg={'oldpath':oldpath,'newpath':newpath})
    
            
            # First, detect cycles
            pgraph = Globals().getGraph(self.project.getName())
            cycles = pgraph.find_cycles()
            
            # Create Makefile.am file, order vertex list clients-first
           
            makefile_am = self._generateMakefileAm()
            makefile_am_path = os.path.join(self.project.getDir(),'Makefile.am')
            print 'Makefile.am:\n',makefile_am
            try:
                BFileManager().writeStringToFile(makefile_am_path,makefile_am)
            except IOError,e:
                err('Could not write to file ' + makefile_am_path + ': ' + str(e))
            
            # Copy user files and create makefile if they don't already exist
            if self.changedList:
                for vertex in self.changedList:
                    if vertex.kind == 'component' or vertex.kind == 'class':
                        # Genereate BOCCA/Dir-projName files if not there
                        myDir = os.path.join(self.project.getDir(),
                                             self.locationManager.getComponentLoc()[0],
                                             vertex.symbol)
                        if not os.path.exists(os.path.join(myDir,'BOCCA','Dir-' + self.project.getName())):
                            addProjectMetadirs(self.project.getName(),
                                               topDir=myDir,rootDir=self.project.getDir())
                        
        
                
        if self.changedList \
                and (self.autoregenimpls == 'enabled' or self.autochecksidl == 'enabled' or genSIDL) \
                and not buildFilesOnly:               
            for vertex in self.changedList:
                if vertex.kind in ['class', 'component']:
                    if not vertex.project: vertex.project = self.project
                    if genSIDL:
                        status = self.genSIDL(vertex)
                        if status != 0: 
                            err('Builder could not generate SIDL for ' + vertex.kind + ' ' + vertex.symbol)
                    if self.autoregenimpls == 'enabled':
                        status = self.genImpls(vertex)
                        if status != 0: 
                            err('Builder could not generate code with Babel for ' + vertex.kind + ' ' + vertex.symbol)
                    elif self.autochecksidl == 'enabled':
                        status = self.invokeBabel(vertex, checkSIDLOnly=True)

                elif self.autochecksidl == 'enabled':
                    status = self.invokeBabel(vertex, checkSIDLOnly=True)
        
        if self.timing == 'enabled':
            t2 = time.time()
            print '%s took %0.2f s' % ('builder plugin update', (t2-t1))
            
        self.changedList = []
        return status
    
    # def genSIDL(self, vertex): default method is fine.

    def genImpls(self, vertex):
        retcode = 0
        command = ''
        if vertex.kind in ['class', 'component', 'interface', 'port', 'enum']:
            retcode = self.invokeBabel(vertex)
        if retcode == 130:
            err('user interrupt')
        if retcode != 0:
            err('SIDL error, check output from call to Babel for clues', 4) 
                
        return retcode

    def changed(self, vertexList):
        '''This is how the builder is notified of changes to a list of vertices.
        The build system will perform whatever actions are necessary on these
        vertices during a subsequent update call.
        '''
        self.changedList.extend(vertexList)
        return self.changedList
    
    def remove(self, vertexList):
        ''' Removes build-relevant information associated with vertices in vertexList.
        Returns 0 upon success, 1 otherwise.
        '''
        import glob
        project, pgraph = Globals().getProjectAndGraph(self.project.getName())
        projectDir = project.getDir()
        for vertex in vertexList:
            print >>DEBUGSTREAM, 'removing build system artifacts for ' + vertex.symbol
            if vertex.kind in ['interface','port', 'enum']:
                mydir = os.path.join(projectDir,self.locationManager.getPortLoc()[0])
                libs = glob.glob(os.path.join(mydir, 'lib', 'lib' + vertex.symbol + 'Port-*.la'))
                libs += glob.glob(os.path.join(mydir, 'lib', '*', 'lib' + vertex.symbol + 'Port-*.*'))
                for lib in libs:
                    try: fileManager.rmdir(lib,trash=False,nobackup=True)
                    except: pass
            elif vertex.kind in ['class','component']:
                mydir = os.path.join(projectDir,self.locationManager.getComponentLoc()[0])
                libs = glob.glob(os.path.join(mydir, 'lib', 'lib' + vertex.symbol + '.*'))
                for lib in libs:
                    try: fileManager.rm(lib,trash=False,nobackup=True)
                    except: pass
            else: return 0

            if os.path.exists(os.path.join(mydir,vertex.symbol)):
                try: fileManager.rmdir(os.path.join(mydir,vertex.symbol),trash=True)
                except: pass
        return 0


    def mergeBuildfiles(self, source, target, sourceProjectName='external'):
        '''Merges 'source' into 'target' if the buildfiles are determined
        to be compatible.  Note that this does not necessarily rely on the splicer code.
        '''

        # TODO: Implement this!
        raise NotImplementedException

#-------- Private methods

    def _getDependencyLists(self, vertexlist):
        '''This helper method generates dictionaries containing the vertex 
        dependencies information.
        
        @param vertexlist: the vertex list for which dependencies are returned 
        @return: clientdeps and impldeps, dictionaries indexed by vertex whose
                 values are lists containing vertices on which 
                the key vertex depends.
        '''

        clientdeps = {}        # Clients on which this vertex depends
        impldeps = {}          # Impls on which this vertex depends
        for vertex in vertexlist:
            clientdeps[vertex] = []
            impldeps[vertex] = []
            for v in vertex.dependencies():
                
                if v.kind not in ['port','interface','component','class','enum']:
                    continue
                
                known = False
                for pkg in Globals().getKnownPackages():
                    if v.symbol.startswith(pkg):
                        known = True
                if known: continue
                
                if v.kind in ['port','interface','enum']:
                    clientdeps[vertex].append(v)
                
                if v.kind in ['class','component']:
                    impldeps[vertex].append(v)
              
        return clientdeps, impldeps
    
    def _generateMakefileAm(self, vertexlist=[]):
        '''This method generates the one and only Makefile.am file for the project, 
        which must reside in the top-level project directory. This is necessary to 
        be able to handle complex dependencies, for example, cycles in the dependency
        graph. If you don't like it, feel free to write another builder plugin.
        
        @param vertexlist: the list of vertices for which build information is 
                            to be generated.
        '''
        
        buf = ''
        buildableList = ['class','component','interface','port','enum']
        
        # Store library info in a dictionary, indexed by library name.
        #     Each dictionary value is a tuple (vertexset,sourcefiles)
        #     containing a Set of vertices and corresponding source files
        libraries = {}    # dict indexed by library name, containing lists of vertices and source files
        libinfo = {}      # dict indexed by vertex, containing library names
        headers = []
        allsources = Set()
        allsidlfiles = Set()
        alldirs = Set()
        all_libraries = Set()
        cleanfiles = Set()
        # First, detect cycles
        if self.project:
            project, pgraph = Globals().getProjectAndGraph(self.project.getName())
        else:
            project, pgraph = Globals().getProjectAndGraph()
        
        print >>DEBUGSTREAM, '[Builder] Finding cycles in the project graph...'
        
        cycles = pgraph.find_cycles() # a list of Sets
        
        print >>DEBUGSTREAM, '[Builder] Finished looking for cycles in the project graph.'
        
        if not vertexlist: 
            vertexlist = self.project.getVertexList(kinds=['port','interface', 'enum', 'component', 'class'])
        
        # Dependencies
        clientdeps, impldeps = self._getDependencyLists(vertexlist)

       
        # Generate automake library info. 
        #     We must put all the symbols in a cycle in the same library because
        #     linking separate libraries in the case of mutual dependencies is impossible.
        libnames = []
        libname = ''
        for cycle in cycles:
            # Generate library names and temporarily associate them with vertices
            # These values are not stored in the persistent representation of the graph
            print >>DEBUGSTREAM, '[Builder] Processing cycle:', [x.symbol for x in cycle]
            if len(cycle) == 1:
                for vertex in cycle: 
                    if vertex.kind in buildableList:
                        libname = 'lib' + vertex.symbol 
            else:
                symstring = ''
                shortname = project.symbol + '_'
                for vertex in cycle:
                    if vertex.kind not in buildableList: continue
                    symstring += vertex.symbol
                    shortname += vertex.symbol.split('.')[-1]
                # For now, I'm abandoning hashing -- the lib names are very unreadable
                # and chances of libname conflicts between projects are microscopic -BN
                #libname = 'lib' + shortname + getHash(symstring)
                libname = 'lib' + shortname
                counter = 1
                while libname + str(counter) in libnames: counter += 1
                libname += '_' + str(counter)
    
            if libname:
                libname += '.la'
                libnames.append(libname)
                libraries[libname] = (cycle,self._getSources(cycle))
                for vertex in cycle:
                    if vertex.kind not in buildableList: continue
                    libinfo[vertex] = os.path.join(self.local_lib_path,libname)
                all_libraries.add(os.path.join(self.local_lib_path,libname))
            
        
        buf += self._format('lib_LTLIBRARIES = ' + ' '.join(all_libraries))
         
        for lib, (cycle,files) in libraries.items():
            
            # SOURCES variable for each library
            amlibname = lib.lower().replace('.','_').replace('-','_')
            sources = ' '.join(libraries[lib][1])
            allsources = allsources.union(Set(libraries[lib][1]))
            
            # SIDL dependencies
            for v in cycle:
                sidldir, sidlfiles = self.locationManager.getSIDLLoc(v)
                if v.kind in ['class','component']: subdir = os.path.join('components',v.symbol)
                else: subdir = os.path.join('ports',v.symbol)
                babelstamp = os.path.join(subdir,'babel-stamp') 
                #sources = self._getSources([v])

                buf += '\n' + self._format(sources.strip() + ' : ' \
                            + babelstamp)
                
                sidlfiles = [os.path.join(sidldir,f) for f in sidlfiles]
                allsidlfiles = allsidlfiles.union(Set(sidlfiles))
                buf += '\n' + self._format(babelstamp + ' : ' \
                            + ' '.join(sidlfiles)) + '\n'
            
                # libname_SOURCES
                buf += self._format(amlibname + '_SOURCES = ' + sources) + '\n'
                            
                # Inter-library dependencies
                # libname_LDADD
                allmydeps = Set()
                if v.kind in ['class','component','enum','interface','port']:
                    # These are the only SIDL entities that can have libraries associated with them
                    for dv in clientdeps[v]: allmydeps.add(libinfo(dv) + v._b_language + '.la')
                    for dv in impldeps[v]: allmydeps.add(libinfo(dv) + '.la')
                
                if len(allmydeps) > 0:
                    buf += self._format(amlibname + '_LDADD = ' + ' '.join(allmydeps)) + '\n'
                
                # libname_DEPENDENCIES (maybe needed)
                
            
            # Keep track of all directories involved in the build
            if v.kind in ['class','component','enum','interface','port']:
                for files in libraries[lib]:
                    for f in files: 
                        if isinstance(f,str):
                            alldirs = alldirs.union(Set([os.path.dirname(f)]))
        

        # Custom targets (per SIDL symbol, not per library), dependencies
        for v in vertexlist:
        
            if v.kind in ['class','component']: subdir = os.path.join('components',v.symbol)
            else: subdir = os.path.join('ports',v.symbol)
            
           
            # Babel invocation
            babel_cmd = self.getBabelCommandString(v)
            if not babel_cmd: continue
            
            babel_cmd = self._format('\t' + babel_cmd, indent='\t\t')
            print >>DEBUGSTREAM, 'Inserting Babel command:\n', babel_cmd
            buf += '\n\n' + os.path.join(subdir,'babel-stamp') + ' : ' \
                + os.path.join('$(PROJECT_TOP_DIR)',self.locationManager.getSIDLLoc(v)[1][0]) + '\n'
            buf += '\t@rm -f ' + os.path.join(subdir,'babel-temp') + '\n'
            buf += '\t@touch ' + os.path.join(subdir,'babel-temp') + '\n'
            buf += babel_cmd + '\n'
            buf += '\t@mv -f ' + os.path.join(subdir,'babel-temp') + ' $@\n'
            buf += '\n'
            cleanfiles.add(os.path.join(subdir,'babel-stamp'))
            
            # Extract header info (for include_HEADERS)
            headers.extend([f for f in allsources for suffix in ['.hxx','.h','.mod'] if f.endswith(suffix)])
                    
        # Global automake variables 
        
        # AM_CPPFLAGS (include all project subdirs + external ones)
        buf += '\n\n' + self._format('AM_CPPFLAGS = ' + ' '.join(['-I' + dir for dir in alldirs]))
        
        # include_HEADERS
        buf += '\n\n' + self._format('include_HEADERS = ' + ' '.join(headers))
        
        # BUILT_SOURCES -- basically all the Babel-generated sources; this tells 
        # automake to generate them first before building
        buf += '\n\n' + self._format('BUILT_SOURCES = ' + ' '.join(allsources))
 
        # CLEANFILES        
        buf += '\n\n' + self._format('CLEANFILES = ' + ' '.join(cleanfiles))
        
        buf += '\n'
        return buf
    
    def _format(self, thestring, indent='    '):
        '''Return nicely formatted string for inclusion in makefile.'''
        pos = 0
        maxpos = len(thestring)
        if maxpos < 80: return thestring
        linelimit = 70

        space = re.compile(r' ')
        newstring = ''
        while pos < maxpos-linelimit:
            nearend = pos + linelimit - indent.count('\t')*4 - indent.count(' ')
            m = space.search(thestring[nearend:])
            if m: newpos = nearend + m.start()
            else: newpos = maxpos
            line = thestring[pos:newpos]
            if newpos < 2*(linelimit-10): newstring += line    # first line
            else: newstring += ' \\\n' + indent + line
            pos = newpos
            
        if pos < len(thestring): newstring += thestring[pos:]
        return newstring 

    
    def _createMakeDependsString(self, vertexlist, kinds=['class','component']):
        # Dependencies on sidl within this project (TODO: dependencies on other things)
        # Babel croaks when given env. variables in input names, so the 
        result = ''
        extSymbols = ''
        allSidlDeps = ''
        allClassDeps = ''
        buildableList = ['class','component','interface','port','enum']

        for vertex in vertexlist:
            if vertex.kind not in buildableList: continue
            if vertex.getAttr('removed'): continue
            if vertex.symbol.startswith('sidl.') or vertex.symbol.startswith('gov.cca.') or vertex.symbol.startswith('ccaffeine.'): continue
            portdeps = ''             # ports/interfaces within project on which vertex depends
            classSidlDeps = ''        # sidl files for classes/components on which vertex depends
            classInterfaceDeps = ''   # if vertex is component or class, the interfaces/ports on which it depends
            portClassDeps = ''        # if vertex is port/interface, the classes/components on which it depends
            classIncludes = ''        # include paths for headers of classes/comps on which vertex depends
            classLibs = ''            # libraries (-llibname) list for classes/comps on which vertex depends
            classdeps = ''            # classes/components within project on which vertex depends

            mysidl = os.path.join('$(PROJECT_TOP_DIR)',vertex._b_sidlFile)   
                
            for v in vertex.dependencies():
                if v.symbol.startswith('sidl.') or v.symbol.startswith('gov.cca.') \
                    or v.symbol.startswith('ccaffeine.'): continue
                if v.kind not in ['port', 'interface', 'component', 'class', 'enum']: continue
                if v._b_sidlFile and not v._b_sidlFile.startswith(os.sep):
                    if v.kind in ['port', 'interface', 'enum']:
                        portdeps += ' ' + os.path.join('$(PROJECT_TOP_DIR)', v._b_sidlFile)
                        if vertex.kind in ['class','component']:
                            classInterfaceDeps += v.symbol + ' ' 
                            if vertex._b_language != 'python': 
                                classLibs += ' -l' + v.symbol + '-' + vertex._b_language 
                    else:
                        classdeps += ' ' + v.symbol
                        classSidlDeps += ' ' + os.path.join('$(PROJECT_TOP_DIR)', v._b_sidlFile)
                        classIncludes += ' -I' + os.path.join('..', v.symbol) \
                                + ' -I' + os.path.join('..', v.symbol, 'glue') \
                                + ' $(INCLUDES_' + v.symbol + ')'
                        if v._b_language != 'python': 
                            classLibs += ' -l' + v.symbol + ' $(LIBS_' + v.symbol + ')'
                        if vertex.kind in ['port','interface','enum']:
                            portClassDeps += v.symbol + ' '
                    
                # Now do client dependencies on other SIDL elements
                clientLibDeps = ''
                languages = self.locationManager.getLanguages()
                if 'python' in languages:
                    languages = ['python', '$(LANGUAGE)']
                else:
                    languages = ['$(LANGUAGE)']
                for lang in languages:
                    deps = ''
                    install_deps = ''
                    for v in vertex.dependencies():
                        if v.kind not in buildableList: continue
                        if v.symbol.startswith('sidl.') or v.symbol.startswith('gov.cca.') \
                            or v.symbol.startswith('ccaffeine.'): continue
                        deps += ' ' + os.path.join('$(PROJECT_TOP_DIR)',self.locationManager.getBuildLibs(v,lang,client=True)[0])
                        install_deps += ' ' + os.path.join('$(PROJECT_TOP_DIR)',self.locationManager.getBuildLibs(v,lang,client=True,for_install=True)[0])
                    if deps:
                        mylib = os.path.join('$(PROJECT_TOP_DIR)',
                                             self.locationManager.getBuildLibs(vertex,lang,client=True)[0])
                        clientLibDeps += mylib + ' : ' + deps + '\n'
                        if lang != 'python':
                            mylib = os.path.join('$(PROJECT_TOP_DIR)',
                                                 self.locationManager.getBuildLibs(vertex,lang,client=True,for_install=True)[0])
                            clientLibDeps += mylib + ' : ' + install_deps + '\n'
                
                if clientLibDeps: allSidlDeps += clientLibDeps

            if portdeps: allSidlDeps += 'PORT_SIDL_DEPS_' + vertex.symbol + ' = ' + portdeps + '\n'
            
            # Dependencies of classes or components on interfaces
            if classInterfaceDeps: allSidlDeps += 'INTERFACE_DEPS += ' + classInterfaceDeps + '\n'
            
            # Dependencies of interfaces or ports on classes or components
            if portClassDeps: allSidlDeps += 'CLASS_DEPS += ' + portClassDeps + '\n'
            
            if classdeps: 
                result += vertex.symbol + ' : ' + classdeps + '\n'
                allClassDeps += classdeps
            if classSidlDeps: allSidlDeps += 'CLASS_SIDL_DEPS_' + vertex.symbol + ' = ' + classSidlDeps + '\n'
            
            # External file dependencies
            extSymbolDeps, extSidlDeps, extLibs, extSymSidl = self._getExternalDeps(vertex)
            if extLibs: classLibs += extLibs
            if extSymbolDeps: 
                result += 'EXT_SYMBOL_DEPS_' + vertex.symbol + ' = ' + extSymbolDeps + '\n'
            if extSidlDeps: 
                allSidlDeps += 'EXT_SIDL_DEPS_' + vertex.symbol + ' = ' + extSidlDeps.replace(',',' ') + '\n'  
            if extSymSidl: 
                result += extSymSidl 
                extSymbols += extSymSidl

            # SIDL_DEPS settings go only in component/class client make snippet...
            if vertex.kind == 'class': allSidlDeps += 'CLASS_CLIENTS += ' + vertex.symbol + '\n'
            if vertex.kind == 'component': allSidlDeps += 'COMPONENT_CLIENTS += ' + vertex.symbol + '\n'
            result += allSidlDeps

            # Now generate the include and libs for dependencies
            if classIncludes: result += 'INCLUDES_' + vertex.symbol + ' = ' + classIncludes + '\n'
            if classLibs: result += 'LIBS_' + vertex.symbol + ' = ' + classLibs + '\n'
        if result: result += '\n'
            
        return result, extSymbols, allSidlDeps, allClassDeps  

    def _getSources(self, vertexset):
        sources = []
        for v in vertexset:
            print >>DEBUGSTREAM, '[builder] getSources for vertex', v
            if v.kind in ['class', 'component', 'interface', 'port', 'enum']:
                dir, files = self.locationManager.getGlueLoc(v,v._b_language)
                sources.extend([os.path.join(dir,x) for x in files])
                if v.kind in ['class','component']:
                    dir, files = self.locationManager.getImplLoc(v)
                    sources.extend([os.path.join(dir,x) for x in files])

        # TODO
        
        return sources
    
    def _getExternalDeps(self, vertex):
        ''' Generates the makefile snippets with information about external SIDL dependencies.'''
        extSymbolDeps = ''
        extSidlDeps = ''
        extSymSidl = ''
        extLibs = ''
        for sym in vertex._b_externalSidlFiles.keys():
            f = vertex._getExternalSIDLPath(sym)
            if f:
                extSymbolDeps += ' ' + sym
                extSidlDeps += ' ' + f
                if vertex.kind in ['class','component']: extLibs += ' -l' + sym + '-' + vertex._b_language 
                extSymSidl += 'EXT_SYMBOL_SIDL_' + sym + ' = ' + f.replace(',',' ') + '\n'
        for v in vertex.dependencies():
            for sym in v._b_externalSidlFiles.keys():
                f = vertex._getExternalSIDLPath(sym) 
                if f:
                    extSymbolDeps += ' ' + sym
                    extSidlDeps += f.replace(',',' ')
                    if vertex.kind in ['class','component']: extLibs += ' -l' + sym + '-' + vertex._b_language 
                    extSymSidl += 'EXT_SYMBOL_SIDL_' + sym + ' = ' + f.replace(',',' ') + '\n'
        if extSymbolDeps: extSymSidl += 'EXTERNAL_SIDL_SYMBOLS += ' + extSymbolDeps + '\n' 
        if extSidlDeps: extSymSidl += 'EXT_SIDL_FILES += ' + extSidlDeps.replace(',',' ') + '\n' + extSymSidl.replace(',',' ')
        return extSymbolDeps, extSidlDeps, extLibs, extSymSidl

    def _genMakefiles(self, vertex, mydir):
        compdir = os.path.join(self.project.getDir(), 'components', vertex.symbol)
        tdir = os.path.join(self.project.getDir(), 'buildutils')
        for f in ['make.vars.user', 'make.rules.user']:
            if not os.path.exists(os.path.join(compdir, f)):
                BFileManager().copyfile(os.path.join(tdir, f), os.path.join(compdir, f), nobackup=True)
        reldir = os.path.join('..', '..')
        makefile = os.path.join(compdir, 'Makefile')
        if not os.path.exists(makefile):
            f = BFileManager().open(makefile, 'w')
            # Compute relative path to top-level project dir

            #                            if vertex._b_language in ['python','java']:
            #                                for i in range(vertex.symbol.count('.')):
            #                                    reldir = os.path.join(reldir,'..')
            f.write('# Common makefile fragment\n' + 'RELATIVE_TOP=' + reldir + '\n' + 'include $(RELATIVE_TOP)/buildutils/make.server')
            f.close()
        
        if vertex._b_language in ['python', 'java']:
            impldir, flist = self.locationManager.getImplLoc(vertex)
            impldir = os.path.join(self.project.getDir(), impldir)
            makefile = os.path.join(impldir, 'Makefile')
            if not os.path.exists(makefile):
                f = BFileManager().open(makefile, 'w')
                f.write('# Bocca-generated file, do not modify\n'
                        + 'ifndef MAKECMDGOALS\n    MAKECMDGOALS=all\nendif\n'
                        + '$(MAKECMDGOALS):\n'
                        + '\t$(MAKE) -C ' + mydir + ' $@\n')
                f.close()
        return

    def _fixPathsInMakefiles(self, arg,dirname,fnames):
        '''Visitor function to replace all occurrences of incorrect project paths with 
        the correct project path.'''
        
        oldpath = arg['oldpath']
        newpath = arg['newpath']
        
        # babel.make.depends, babel.make.all, .*.babel.make.depends, *.lo
        filenameregexp = re.compile(r"""
               .*babel\.make\.depends$            # Babel-generated
             | babel\.make\.all$                  # Build system-generated
             | .*\.lo$                            # Libtool-generated
            """, re.VERBOSE)
        libnameregexp = re.compile(".*\.la$")
        files = os.listdir(dirname)
        for f in files:
            fpath = os.path.join(dirname,f)
            # Remove libtool libraries to force relinking
            if libnameregexp.match(f):
                os.unlink(fpath)
                continue
            
            m = filenameregexp.match(f)
            if not m: continue
            
            atime = os.path.getatime(fpath)
            mtime = os.path.getmtime(fpath)
            # Replace all occurrences of oldpath with newpath in the file
            for line in fileinput.input(fpath,inplace=1):
                lineno = 0
                lineno = string.find(line, oldpath)
                if lineno >0:
                    line =line.replace(oldpath, newpath)
                sys.stdout.write(line)    
            # Reset accessed and mod times
            os.utime(fpath, (atime, mtime))                    
