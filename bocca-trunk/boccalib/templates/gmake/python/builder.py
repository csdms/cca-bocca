import os, re, fileinput, string
from sets import Set
import builders.builder as builderTemplate
from cct._err import *
from cct._file import *
from cct._debug import DEBUGSTREAM, WARN
from cct._util import fileManager, Globals, addProjectMetadirs
from cct.project import Project
from splicers.Operations import mergeFileIntoString

class Builder(builderTemplate.BuilderDefault):
    def __init__(self, modulePath, project):
        '''Constructor
        @param modulePath the directory containing the implementation of the Builder implementation.
        '''
        # The parent constructor sets the self.locationManager variable
        builderTemplate.BuilderDefault.__init__(self,modulePath, project)
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
                    if defaults.has_option('Project','regen_messages'): self.regen_messages = re.split('\W+',defaults.get('Project','regen_messages'))[0]
                    if defaults.has_option('Project','autochecksidl'): self.autochecksidl = re.split('\W+',defaults.get('Project','autochecksidl'))[0]
                    if defaults.has_option('Project','timing'): self.timing = re.split('\W+',defaults.get('Project','timing'))[0]
                    if defaults.has_option('Project','use_colors'): self.colors = re.split('\W+',defaults.get('Project','use_colors'))[0]
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
            os.unlink(os.path.join(projectDir,'configure.in1'))
            os.unlink(os.path.join(projectDir,'make.project1'))
            os.unlink(os.path.join(projectDir, 'buildutils', 'make.vars.common1'))
        except: pass
        try:
            os.system("chmod a+x "+os.path.join(projectDir,'configure.ac'))
            os.system("chmod a+x "+os.path.join(projectDir,'configure'))
        except: pass
        
        pass

    def rename(self, oldProjectName, newProjectName, oldProjectVersion, newProjectVersion, oldProjectDir):
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
        @param buildFilesOnly: Only update files contaning component and port info.
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
    
                
            # Update component and port list files
        
            # Update component information
            compMakeFile = os.path.join(self.project.getDir(), self.locationManager.getComponentLoc()[0], "make.components")
            
            deps, extSymbols, allSidlDeps, classdeps = self._createMakeDependsString(self.project.getVertexList(kinds=['component','class']),kinds=['component','class'])
            result = self._createComponentsMakeString(self.project.getVertexList(kinds=['component','class'],ignore_action='contains'), classdeps) + '\n' + deps
                
            # Create the make.components file (changed in 0.5.6 to not include any user content)
            try:
                BFileManager().writeStringToFile(compMakeFile,result)
            except IOError,e:
                err('Could not write to file ' + compMakeFile + ': ' + str(e))
                
            # Update port and other client information
            clientMakeFile = os.path.join(self.project.getDir(), 'buildutils', 'make.symbols')

            deps, extSymbols2, allSidlDeps2, classdeps2 = self._createMakeDependsString(self.project.getVertexList(kinds=['port','interface', 'enum']),
                                                                                        kinds=['port','interface', 'enum'])
            result = self._createPortsMakeString(self.project.getVertexList(kinds=['port','interface', 'enum', 'component', 'class'])) + '\n' + deps
            
            # Create external make info file
            if extSymbols or extSymbols2:              
                result += extSymbols + extSymbols2
            
            # Create class/components clients file (for component/class client builds only)
            if allSidlDeps or allSidlDeps2:                
                result += allSidlDeps+allSidlDeps2 
                
            if classdeps:
                result += 'CLASS_CLASS_DEPS = ' + classdeps
                
            try:
                BFileManager().writeStringToFile(clientMakeFile,result)
            except IOError,e:
                err('Could not write to file ' + clientMakeFile + ': ' + str(e))

            # Copy user files and create makefile if they don't already exist
            if self.changedList:
                for vertex in self.changedList:
                    if vertex.kind == 'component' or vertex.kind == 'class':
                        # Genereate BOCCA/Dir-projName files if not there
                        myDir = os.path.join(self.project.getDir(),self.locationManager.getComponentLoc()[0],vertex.symbol)
                        if not os.path.exists(os.path.join(myDir,'BOCCA','Dir-' + self.project.getName())):
                            addProjectMetadirs(self.project.getName(),topDir=myDir,rootDir=self.project.getDir())
                        self._genMakefiles(vertex, myDir)
                        
                                # Client makefiles for python
                    if 'python' in self.locationManager.getLanguages():
                        # Generate bocca_setup.py file (Babel-generated setup.py is not used since it doesn't work with newer Pythons):
                        bdir,bfiles=self.locationManager.getBuildfilesLoc(vertex, client_only=True)
                        thedir = os.path.join(bdir,vertex.symbol,'python')
                        if not os.path.exists(os.path.join(thedir,'bocca_setup.py')):
                            if not os.path.exists(thedir): os.makedirs(thedir)
                            f = BFileManager().open(os.path.join(thedir,'bocca_setup.py'), 'w')
                            f.write(self._genSetupPy(vertex))
                            f.close()

                        
                
        if self.changedList and (self.autoregenimpls == 'enabled' or self.autochecksidl == 'enabled' or genSIDL) and not buildFilesOnly:               
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
        for vertex in vertexList:
            print >>DEBUGSTREAM, 'removing build system artifacts for ' + vertex.symbol
            projectDir = self.project.getDir()
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

    def mergeBuildfiles(self, target, source, sourceProjectName='external'):
        '''Merges 'source' into 'target' if the buildfiles are determined
        to be compatible.  Note that this does not necessarily rely on the splicer code.
        '''

        print "Merging makefile "+source+" into makefile "+target+"..."

        localTarget = target[target.rfind('/')+1:]
        if localTarget != source[source.rfind('/')+1:]:
            # The files aren't compatible, ignore merge
            return False
        success = False
        if 'vars' in localTarget.split('.'):
            success = self._mergeVars(target, source, sourceProjectName)
        elif 'rules' in localTarget.split('.'):
            success = self._mergeRules(target, source, sourceProjectName)

        return success

#-------- Private methods

    def _createPortsMakeString(self, vertexlist):
        result = ''     
        if self.colors == 'enabled': result += 'USE_COLORS = 1\n'
        portsdir = self.locationManager.getPortLoc()[0] + os.sep
        ports = []
        interfaces = []
        classes = []
        components = []
        sidlfiles = ''
        alldeps = ''
        for vertex in vertexlist:
            if vertex.getAttr('removed'): continue
            if vertex.symbol.startswith('sidl.') or vertex.symbol.startswith('gov.cca.') or vertex.symbol.startswith('ccaffeine.'): continue
            requires = vertex.getAttr('requires')
            if vertex.kind == 'port':
                extends=None
                if vertex.getAttr('extends'):
                    extends = vertex.getAttr('extends').keys()
                ports.append( (vertex.symbol, extends, requires) )
            if vertex.kind == 'enum' or vertex.kind == 'interface': 
                extends=None
                if vertex.getAttr('extends'):
                    extends = vertex.getAttr('extends').keys()
                interfaces.append( (vertex.symbol, extends, requires ) )
            if vertex.kind == 'component':
                extends=None
                implall=None
                if vertex._b_extends:
                    extends = vertex._b_extends.keys()[0]
                if vertex._b_implements:
                    implall = vertex._b_implements.keys()
                components.append( (vertex.symbol, vertex._b_language, vertex._b_uses, vertex._b_provides, extends, requires, implall) )
            if vertex.kind == 'class':
                extends=None
                implall=None
                if vertex._b_extends:
                    extends = vertex._b_extends.keys()[0]
                if vertex._b_implements:
                    implall = vertex._b_implements.keys()
                classes.append( (vertex.symbol, vertex._b_language, extends, requires, implall) )
        
        # Sorting for aesthetic purposes makes the build (with dependencies) clumsier and potentially slower
        #interfaces.sort()
        #ports.sort()
        result += sidlfiles
        result += '\n\n'
        for i, e, r in ports:
            result += '\nPORTS \t+= ' + i +'\n'
            result += 'CCA_TYPE_'+ i + '= PORT\n'
            if e:
                for k in e:
                    result += 'SIDL_EXTENDS_' + i + ' += ' + k +'\n'
            if r:
                for k in r:
                    result += 'SIDL_REQUIRES_' + i + ' += ' + k +'\n'
        for i, e, r in interfaces:
            result += '\nINTERFACES \t+= ' + i +'\n'
            result += 'CCA_TYPE_'+ i + '= INTERFACE\n'
            if e:
                for k in e:
                    result += 'SIDL_EXTENDS_' + i + ' += ' + k +'\n'
            if r:
                for k in r:
                    result += 'SIDL_REQUIRES_' + i + ' += ' + k +'\n'
        for i , j, u, p, e, r, ia in components:
            result += '\nCCA_TYPE_'+ i + '= COMPONENT\n'
            result += 'CCA_LANG_'+ i + '= '+ j +'\n'
            if u:
                for k in u:
                    result += 'CCA_USES_' + i + ' += ' +k.getType()+ '@' +k.getName() +'\n'
            if p:
                for k in p:
                    result += 'CCA_PROVIDES_' + i + ' += ' +k.getType()+ '@' +k.getName() +'\n'
            if e:
                result += 'SIDL_EXTENDS_' + i + ' = ' + e +'\n'
            if r:
                for k in r:
                    result += 'SIDL_REQUIRES_' + i + ' += ' + k +'\n'
            if ia:
                for k in ia:
                    result += 'SIDL_IMPALL_' + i + ' += ' + k + '\n'
        for i, j, e, r, ia in classes:
            result += '\nCCA_TYPE_'+ i + '= CLASS\n'
            result += 'CCA_LANG_'+ i + '= '+ j +'\n'
            if e:
                result += 'SIDL_EXTENDS_' + i + ' = ' + e +'\n'
            if r:
                for k in r:
                    result += 'SIDL_REQUIRES_' + i + ' += ' + k +'\n'
            if ia:
                for k in ia:
                    result += 'SIDL_IMPALL_' + i + ' += ' + k + '\n'

        return result 
    
    def _createComponentsMakeString(self, vertexlist, classdeps):
        locManager = self.project.getLocationManager()
        result = '# DO-NOT-DELETE bocca.splicer.begin(components)\n'
        result += '# DO-NOT-DELETE bocca.splicer.end(components)\n'     
        result += '# The following target should not be modified by users, it is necessary\n' \
        + '# for building component client libraries\n' \
        + 'ifdef GET_SIDL_DEPS\n' \
        + 'get-sidl-deps:\n' \
        + '\t@echo $(PORT_SIDL_DEPS_$(GET_SIDL_DEPS))\n' \
        + '\t$(CLASS_SIDL_DEPS_$(GET_SIDL_DEPS))\n' \
        + '\t$(EXT_SIDL_DEPS_$(GET_SIDL_DEPS))\n' \
        + '.PHONY: get-sidl-deps make.components\n' \
        + 'endif\n'
   
        comps = {}
        classes = {}
        languages = []
        complist = []
        classlist = []
        for vertex in vertexlist:
            if vertex.getAttr('removed'): continue
            libname = locManager.getBuildLibs(vertex,vertex._b_language)[0]
            if vertex.kind == 'component': 
                comps[vertex.symbol] = vertex._b_language
                if vertex._b_language not in languages: languages.append(vertex._b_language)
                complist.append(vertex.symbol + '-' + vertex._b_language)
            if vertex.kind == 'class': 
                classes[vertex.symbol] = vertex._b_language
                if vertex._b_language not in languages: languages.append(vertex._b_language)
                classlist.append(vertex.symbol + '-' + vertex._b_language)
        if self.colors == 'enabled': result += 'USE_COLORS = 1\n'
        if languages: result += 'LANGUAGES = ' + ' '.join(languages) + '\n'
        
        # Sorting the components and classes for purely aesthetical purposes makes the 
        # dependency handling in the makefile uglier and slower; 
        # TODO: generate the component 
        # list in dependency-induced order instead.
        ckeys = comps.keys()
        ckeys.sort()
        for k in ckeys: 
            result += 'COMPONENTS \t\t+= ' + k + '-' + comps[k] + '\n'
            result += 'CCA_TYPE_'+ k + '= COMPONENT\n'
            result += 'CCA_IMPL_'+ k + '= '+ comps[k]+'\n'
        ckeys = classes.keys()
        ckeys.sort()
        for k in ckeys: 
            result += 'CLASSES \t\t+= ' + k + '-' + classes[k] + '\n'
            result += 'CCA_TYPE_'+ k + '= CLASS\n'
            result += 'CCA_IMPL_'+ k + '= '+ classes[k]+'\n'
        result += '\n'
    
        return result
    
    
    def _createMakeDependsString(self, vertexlist, kinds=['class','component']):
        # Dependencies on sidl within this project (TODO: dependencies on other things)
        # Babel croaks when given env. variables in input names, so the 
        result = ''
        extSymbols = ''
        allSidlDeps = ''
        allClassDeps = ''
        for vertex in vertexlist:
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
                if v.symbol.startswith('sidl.') or v.symbol.startswith('gov.cca.') or v.symbol.startswith('ccaffeine.'): continue
                if v.kind not in ['port', 'interface', 'component', 'class', 'enum']: continue
                if v._b_sidlFile and not v._b_sidlFile.startswith(os.sep):
                    if v.kind in ['port', 'interface', 'enum']:
                        portdeps += ' ' + os.path.join('$(PROJECT_TOP_DIR)', v._b_sidlFile)
                        if vertex.kind in ['class','component']:
                            classInterfaceDeps += v.symbol + ' ' 
                            if vertex._b_language != 'python': classLibs += ' -l' + v.symbol + '-' + vertex._b_language 
                    else:
                        classdeps += ' ' + v.symbol
                        classSidlDeps += ' ' + os.path.join('$(PROJECT_TOP_DIR)', v._b_sidlFile)
                        classIncludes += ' -I' + os.path.join('..', v.symbol) \
                                + ' -I' + os.path.join('..', v.symbol, 'glue') \
                                + ' $(INCLUDES_' + v.symbol + ')'
                        if v._b_language != 'python': classLibs += ' -l' + v.symbol + ' $(LIBS_' + v.symbol + ')'
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
                        if v.kind not in ['class','component','interface','port','enum']: continue
                        if v.symbol.startswith('sidl.') or v.symbol.startswith('gov.cca.') or v.symbol.startswith('ccaffeine.'): continue
                        deps += ' ' + os.path.join('$(PROJECT_TOP_DIR)',self.locationManager.getBuildLibs(v,lang,client=True)[0])
                        install_deps += ' ' + os.path.join('$(PROJECT_TOP_DIR)',self.locationManager.getBuildLibs(v,lang,client=True,for_install=True)[0])
                    if deps:
                        mylib = os.path.join('$(PROJECT_TOP_DIR)',self.locationManager.getBuildLibs(vertex,lang,client=True)[0])
                        clientLibDeps += mylib + ' : ' + deps + '\n'
                        if lang != 'python':
                            mylib = os.path.join('$(PROJECT_TOP_DIR)',self.locationManager.getBuildLibs(vertex,lang,client=True,for_install=True)[0])
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
            if extSymbolDeps: result += 'EXT_SYMBOL_DEPS_' + vertex.symbol + ' = ' + extSymbolDeps + '\n'
            if extSidlDeps: allSidlDeps += 'EXT_SIDL_DEPS_' + vertex.symbol + ' = ' + extSidlDeps.replace(',',' ') + '\n'  
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
    
    def _getSources(self, vertex):
        sources = '$(IORSRCS) $(IMPLSRCS) $(STUBSRCS) $(SKELSRCS) '
        if vertex._b_language is 'f90':
            sources += '$(ARRAYMODULESRCS) $(IMPLMODULESRCS) $(TYPEMODULESRCS) $(STUBMODULESRCS)'
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
                    extSidlDeps += " " + f.replace(',',' ')
                    if vertex.kind in ['class','component']: extLibs += ' -l' + sym + '-' + vertex._b_language 
                    extSymSidl += 'EXT_SYMBOL_SIDL_' + sym + ' = ' + f.replace(',',' ') + '\n'
        if extSymbolDeps: 
            extSymSidl += 'EXTERNAL_SIDL_SYMBOLS += ' + extSymbolDeps + '\n' 
        if extSidlDeps: 
            flist = extSidlDeps.replace(',',' ')
            # uniquify the mess
            d = dict()
            for i in flist.split(" "):
                d[i] = 1
            uflist = d.keys()
            fstring = " ".join(uflist)
            extSymSidl += 'EXT_SIDL_FILES += ' + fstring + '\n'
            extSidlDeps = fstring
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
            if not os.path.exists(impldir):
                try: os.system('mkdir -p ' + impldir) 
                except: pass
            if os.path.exists(impldir) and not os.path.exists(makefile):
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

    def _mergeVars(self, target, source, sourceProjectName):
        '''Merges make.vars.user files identified by source and target together.
        Variables from source which share a name with variables in the target
        are renamed to VARNAME_sourceProjectName and backreferenced in the original
        VARNAME.

        The file format is:

        TARGET
        # ---- Source from sourceProjectName ----
        MODIFIED_SOURCE
        
        Anything which is not a variable is not modified in any way.  Returns True.
        '''

        # Read source first
        sourceInput = BFileManager().open(source, 'r')
        
        sourceLines = []
        sourceVars = {} # {varName, [rename=True|False, value]}
        for line in [line.strip() for line in sourceInput.readlines()]:
            # Handle addition of variables to the var list
            varName, sep, value = line.partition('=')
            if len(sep) != 0:
                varName = varName.strip()
                splitVarName = varName.split()
                # Stub in the variable name for resubstitution later if necessary
                if len(splitVarName) == 1:
                    sourceVars[varName] = [False, value.strip()]
                    sourceLines.append(varName)
                    continue
            sourceLines.append(line)

        sourceInput.close()
        targetInput = BFileManager().open(target, 'r')

        # Read target and identify identical vars
        targetLines = []
        targetVars = []
        for line in [line.strip() for line in targetInput.readlines()]:
            varName, sep, value = line.partition('=')
            if len(sep) != 0:
                varName = varName.strip()
                if varName in sourceVars.keys():
                    sourceVars[varName] = [True, sourceVars[varName][1]]
                    targetLines.append(varName+sep+'$('+varName+'_'+sourceProjectName+') '+value)
                    continue
            targetLines.append(line)

        targetInput.close()

        # Output
        targetOutput = BFileManager().open(target, 'w')
        for line in targetLines:
            targetOutput.write(line+'\n')

        targetOutput.write('\n\n# ---- Contents of make.vars.user from ' + sourceProjectName + ' ----\n\n')

        for line in sourceLines:
            if line in sourceVars.keys():
                if sourceVars[line][0]:
                    targetOutput.write(line+'_'+sourceProjectName)
                else:
                    targetOutput.write(line)
                targetOutput.write('='+sourceVars[line][1]+'\n')
            else:
                targetOutput.write(line+'\n')

        return True

    def _mergeRules(self, target, source, sourceName):
        '''Merges make.rules.user files identified by source and target together.
        Rules from source which share a name with rules in the target
        are renamed to RULE_sourceProjectName and made a dependency of the
        target rule.

        If there is a conflicting rule based on a variable name (e.g. $(SOURCEFILES): ...)
        then a warning is printed and the rule from the SOURCE is stubbed out inside comments
        so that a user can handle renaming the variable or simply migrating the rule into
        the target.

        If there is a variable outside a rule, the merge prints a warning that it may not
        have been performed properly.

        The file format is:

        TARGET
        # ---- Source from sourceProjectName ----
        MODIFIED_SOURCE

        Anything which is not a rule declaration is not modified in any way.  Always
        returns true (merges can always be performed - they just may generate warnings).
        '''

        # Read source first
        sourceInput = BFileManager().open(source, 'r')
        sourceRules = {} # {rules, [[deps], [content], commentOut=True|False]}
        sourceLines = []

        currentRule = ''
        deps = []
        ruleBuffer = []
        insideRule = False
        doubleRule = False
        for line in [line.rstrip() for line in sourceInput.readlines()]:
            if insideRule:
                if line.startswith((' ', '\t', '\n')):
                    ruleBuffer.append(line)
                else:
                    sourceRules[currentRule] = [deps, ruleBuffer, doubleRule, False]
                    sourceLines.append(line)

                    currentRule = ''
                    deps = []
                    ruleBuffer = []
                    insideRule = False
                    doubleRule = False
            else:
                currentRule, sep, depLine = line.partition(':')
                if len(sep) != 0 and not currentRule.startswith('#'):
                    insideRule = True
                    # Handle :: rules
                    if depLine.startswith(':'):
                        depLine = depLine[1:]
                        doubleRule = True
                    sourceLines.append(currentRule)
                    deps = depLine.strip().split()
                else:
                    currentRule = ''

                    # Check for variable and print warning
                    varName, sep, value = line.partition('=')
                    if len(sep) != 0:
                        if len(varName.split()) == 1:
                            warn('Variable '+varName.strip()+' imported from source project '+sourceName
                                 +'may conflict with local variable name, edit by hand to check')
                    sourceLines.append(line)

        # Handle EOF before proper termination of rule buffer
        if len(ruleBuffer) != 0:
            sourceRules[currentRule] = [deps, ruleBuffer, doubleRule, False]

        sourceInput.close()
        targetInput = BFileManager().open(target, 'r')

        targetLines = []
        sourceReplacements = {}
        for line in [line.rstrip() for line in targetInput.readlines()]:
            currentRule, sep, depLine = line.partition(':')
            if len(sep) == 0 or (len(depLine.lstrip()) != 0 and depLine.lstrip()[0] == ':'): # Double-colon rules should not be modified
                targetLines.append(line)
            else:
                rules = currentRule.split()
                for sourceRule in sourceRules.keys():
                    foundRule = False
                    for rule in rules:
                        if rule in sourceRule.split():
                            if rule.find('$') != -1:
                                warn('Source rule '+rule+' is a variable name: Commenting out in '
                                     +'merge, manage by hand.')
                                sourceRules[rule] = [sourceRules[rule][0], sourceRules[rule][1], 
                                                     sourceRules[rules][2], True]
                            else:
                                newRule = rule+'_'+sourceName
                                sourceReplacements[rule] = newRule
                                depLine += ' '+newRule
                            foundRule = True
                            break
                    if foundRule: break
                targetLines.append(currentRule + sep + depLine)

        targetInput.close()
        
        targetOutput = BFileManager().open(target, 'w')
        
        for line in targetLines:
            targetOutput.write(line+'\n')

        targetOutput.write('\n\n# ---- Contents of make.rules.user from ' + sourceName + ' ----\n\n')

        for line in sourceLines:
            if not line in sourceRules.keys():
                targetOutput.write(line+'\n')
            else:
                newCompleteRule = ''
                deps, content, doubleRule, commentOut = sourceRules[line]
                sep = ':'
                if doubleRule: sep += ':'
                if commentOut:
                    targetOutput.write('# ---- Variable rule conflict: Resolve manually ----\n')
                    targetOutput.write('#'+line+sep+" ".join(deps)+'\n')
                    for ruleContent in content:
                        targetOutput.write('#'+ruleContent+'\n')
                    continue
                for rule in line.split():
                    if rule in sourceReplacements.keys():
                        newCompleteRule += sourceReplacements[rule] + ' '
                    else:
                        newCompleteRule += rule + ' '
                targetOutput.write(newCompleteRule+sep)
                for dep in deps:
                    if dep in sourceReplacements.keys():
                        targetOutput.write(" "+sourceReplacements[dep])
                    else:
                        targetOutput.write(" "+dep)
                targetOutput.write('\n')
                for contentLine in content:
                    targetOutput.write(contentLine+'\n')

        targetOutput.close()

        return True

    def _genSetupPy(self,vertex):
        setupstr = """#! /usr/bin/env python
# Build file for Python modules
import sys
from re import compile
from distutils.core import setup, Extension

inc_re = compile('^--include-dirs=(.*)$')
lib_re = compile('^--library-dirs=(.*)$')
exlib_re = compile('^--extra-library=(.*)$')
old_argv = sys.argv
sys.argv = []
inc_dirs = ['.']
lib_dirs = []
libs = ['sidl']

for i in old_argv:
  m = inc_re.match(i)
  if (m):
    if (len(m.group(1))): inc_dirs.extend(m.group(1).split(':'))
  else:
    m = lib_re.match(i)
    if (m):
      if (len(m.group(1))): lib_dirs.extend(m.group(1).split(':'))
    else:
      m = exlib_re.match(i)
      if (m):
        if (len(m.group(1))): libs.extend(m.group(1).split(':'))
      else:
        sys.argv.append(i)
setup(name='@NAME@',
  include_dirs=inc_dirs,
  headers = [
    @HEADER@
  ],
  packages = [
@PKGS@
  ],
  ext_modules = [
    @EXT_MODULES@
  ])
"""
        extmodulesstr = """Extension('@SYMBOL@',
      [@CMODULE@
      ],
      library_dirs=lib_dirs,
      libraries=libs)"""
      
        dir = None
        packages = vertex.symbol.split('.')[:-1]
        dir = packages[0]
        for p in packages[1:]: dir = os.path.join(dir,p)
        name = vertex.symbol.replace('.','_')
        cModule = "'" + os.path.join(dir,name+'_Module.c') + "'"
        header = "'" + name+'_Module.h' + "'"
        pkg = vertex.symbol[:vertex.symbol.rfind('.')]
        pkgstr = "    '"+pkg+"'"
        while pkg.find('.')>0:
            pkg = pkg[:pkg.rfind('.')]
            if pkg != '': pkgstr = "    '"+pkg+"',\n" + pkgstr
            
        if vertex.kind != 'enum':
            setupstr = setupstr.replace('@EXT_MODULES@',extmodulesstr)
        else:
            setupstr = setupstr.replace('@EXT_MODULES@','')
            
        setupstr = setupstr.replace('@NAME@', name).\
                            replace('@PKGS@',pkgstr).\
                            replace('@SYMBOL@', vertex.symbol)
        if vertex.kind != 'enum':
            setupstr = setupstr.replace('@HEADER@', header).\
                                replace('@CMODULE@',cModule)
        else:
            setupstr = setupstr.replace('@HEADER@', '').\
                                replace('@CMODULE@','')
            
        return setupstr
    
