import os, sys, re
import cct._err, cct._debug, cct._validate
import splicers.Source
from splicers.Operations import renameFromFile, mergeFileIntoString, mergeFromString
from cct._util import *
from cct._file import *
from graph.boccagraph import *

class Interface(BVertex):
    def __init__(self, action = '__init__', args = None, project = None, modulePath = None,
                 symbol=None, version='0.0', graph=None, kind='interface'):
        '''bocca <verb> interface [options] SIDL_SYMBOL
        
        <verb> is one of create, change, remove, rename, display. For documentation on
        specific verbs, use 'bocca help <verb> interface'
        '''
        self.extends = {}
        self.newsymbol = None # For rename/copy
        self.isCopy = False
        self._b_sidlFile=''
        self.tab = '    '
        self._b_xmlRepos = []
        self._b_externalSidlFiles = {}
        self.displayAll = False
        BVertex.__init__(self,action,args,project,modulePath,kind,symbol,version,graph)
        # Use self.setAttr(key,value) to set various interface attributes 
        return

    def initCopy(self, copyInterface):
        self.isCopy = True

        self._b_xmlRepos = copyInterface._b_xmlRepos
        self._b_externalSidlFiles = copyInterface._b_externalSidlFiles

        # Necessary to process extension/implementation symbols in graph or Externals[]
        # correctly
        if (self.kind != 'enum'):
            extends = copyInterface.getAttr('extends')
            if (extends is not None and len(extends) > 0):
                self.options.sidlsymbol_and_location = []

                for key, value in extends.iteritems():
                    sidlsymbol_and_location = key[:]
                    if value != '%local%':
                        sidlsymbol_and_location = key + ":" + value
                    self.options.sidlsymbol_and_location.append(sidlsymbol_and_location)

            requires = copyInterface.getAttr('requires')
            if (requires is not None and len(requires) > 0):
                for symbol in requires:
                    requirement = symbol
                    if symbol in copyInterface._b_externalSidlFiles.keys():
                        requirement += ":" + copyInterface._b_externalSidlFiles[symbol]
                    self.options.required_symbol.append(requirement)
                                
        BVertex.initCopy(self, copyInterface)
                                
        if (self.kind != 'enum'):
            self._processCommonCreateAndChangeArgs()
        
    def defineArgs(self,action):
        if action == 'create' or action == 'change':
            self.parser.add_option('-e', '--extends', dest='sidlsymbol_and_location', action='append',
                                   help='a SIDL interface that the ' + self.kind + ' being created extends (optional). ' 
                                   + 'Multiple --extends options can be specified. '
                                   + 'If SIDL_SYMBOL is an existing external interface, the file containing its definition must be '
                                   + 'specified immediately following the the SIDL_SYMBOL, ' 
                                   + 'e.g., --extends pkg.SomeInterface@/path/to/somefile.sidl (Babel-generated XML files are allowed, as well).'
                                   + 'To change the location of the SIDL file associated with an interface, use'
                                   + 'the "change ' + self.kind + ' +  SIDL_SYMBOL --sourcefile/-s FILENAME" command')
            
            self.parser.add_option('-x', '--xml', dest='xmlRepos', action='append',
                                  help='path to external XML repositories containing specification of the interfaces '
                                  + 'and/or classes referenced by this ' + self.kind + '. ' 
                                  + 'Multiple instances of the --xml option '
                                  + 'can be used to specify multiple repository paths.')
                
            self.parser.set_defaults(sidlsymbol_and_location=[], sidlFiles=[], xmlRepos=[])
            
            self._defineDependencyArgs()    # in BVertex
            self._defineImportArgs()        
            self._defineDpathArgs()        # in BVertex
        if action == 'create':
            pass
        elif action == 'edit' or action == 'whereis':
            self.parser.add_option('-s', '--sidl', dest='editsidl', action='store_true',
                                   help="Edit the sidl file (the default)")
            self.parser.add_option('-t', '--touch', dest='touchsidl', action='store_true',
                                   help="Touch the sidl file as if bocca edit changed it.")
            self.parser.add_option('-r', '--build-rules', dest='editrules', action='store_true',
                                   help="Edit the make.rules.user file")
            self.parser.add_option('-V', '--build-vars', dest='editvars', action='store_true',
                                   help="Edit the make.vars.user file")
            self.parser.set_defaults(editsidl=True, touchsidl=False, editrules=False, editvars=False)
        elif action == 'change':
            pass
        elif action == 'display':
            self.parser.add_option('-d', '--dirs', dest="mydirs", action='store_true',
                                   help="Show a list of directories containing user-editable files; this can be used as input for revision control operations.")
            self.parser.add_option('-f', '--files', dest="myfiles", action='store_true',
                               help="Show a list of user-editable files, which can be used as input for revision control operations.")
            self.parser.set_defaults(mydirs=False, myfiles=False)
        elif action == 'rename':
            pass
        elif action == 'remove':
            pass
        elif action == 'usage':
            pass
        elif action == 'copy':
            pass
        else:
            err('Interface verb "' + action + '" NOT implemented yet.', 3)

        return

    def processArgs(self, action):
        """ Validates and if necessary canonicalizes the command line arguments for
        this subject, which are parsed into self.options.
        Exits nonzero if user gives bad input.
        """
        if action == 'create':
            self._processCreateArgs()
        elif action == 'change':
            self._processChangeArgs()
        elif action == 'edit' or action == 'whereis':
            self._processEditArgs()
        elif action == 'rename':
            self._processRenameArgs()
        elif action == 'remove':
            self._processRemoveArgs()
        elif action == 'display': 
            self._processDisplayArgs()
        elif action == 'copy':
            self._processCopyArgs()
        return 
    
    
    
    def graphvizString(self): return 'shape=hexagon color=lightyellow1 fontname="Palatino-Italic"'
        
    def commonCreateAndChange(self, project, pgraph):
        
        dpathdata = self._processDpathOptions()
        self._updateDpaths(dpathdata, sidlname=self.symbol)

        retcode = self._checkExtends()
        if retcode != 0: err('could not extend interfaces: ' + self.options.sidlsymbol_and_location)
        
        self.updateProjectState(project, pgraph)
        
        return 0
    
    def create(self):
        """ create interface INTERFACE [--extends/-e SIDL_SYMBOL{FILE}]
        
        Creates an interface with the name INTERFACE, optionally extending SIDL_SYMBOL.
        INTERFACE and SIDL_SYMBOL are both SIDL types. If INTERFACE is not fully 
        qualified, e.g., MyPort instead of somepackage.MyPort, the port will be added 
        to the default package for the project, usually the same as the project name.        
        """
        
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        
        self.validateNewSymbol(pgraph)  # From BVertex
 
        print >>DEBUGSTREAM,'create ' + self.kind + ', name = ', self.symbol


        retcode = self.commonCreateAndChange(project, pgraph)
        
        self.createSIDLFile(project, pgraph)
        #pgraph.saveGraphvizFile()
        
        if self.sidlImports: 
            self.handleSIDLImports(replaceEnums=self.isCopy, mergeBuildfiles=self.options.mergebuilds)
            if retcode != 0: err('could not import SIDL')
        else:
            self.project.getBuilder().autochecksidl = 'disabled'
            
        self.project.getBuilder().changed([self])
        self.project.getBuilder().update()
        
        pgraph.save()
            
        print >>DEBUGSTREAM, 'create ' + self.kind + ' returning with code ' + str(retcode)
        return retcode
    
    def copy(self):
        """copy interface FROM_SIDL_SYMBOL TO_SIDL_SYMBOL
        """
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        copyVertex = Interface('create', [self.newsymbol], project=self.project, modulePath=self.modulePath,
                               symbol=self.newsymbol, version=self.version, graph=pgraph)
        copyVertex.initCopy(self)

        copyVertex.oldsymbol = self.symbol
        copyVertex.sidlImports = { self._b_sidlFile : ['%all'] }
        
        return copyVertex.create()
 
        
    def change(self):
        """change interface [options] SIDL_SYMBOL

        """
            
        project, pgraph = Globals().getProjectAndGraph(self.project.symbol)
        self.validateExistingSymbol(pgraph)
        
        retcode = self.commonCreateAndChange(project, pgraph)
        
        if self.sidlImports: 
            self.handleSIDLImports(mergeBuildfiles=self.options.mergebuilds)
            if retcode != 0: err('could not import SIDL')

        self.project.getBuilder().changed([self] + list(self.dependents()))
        self.project.getBuilder().update()
        
        pgraph.save()
        
        return 0

    def display(self):
        """display interface SIDL_SYMBOL
        
        """
        if self.displayAll:
            project, graph = Globals().getProjectAndGraph(projectName=self.projectName)
            if project:
                if self.options.mydirs:
                    dirs = []
                    dirs.extend(project.getLocationManager().getPortLoc())
                    dirs.extend(project.getLocationManager().getSIDLDirs(self))
                    dstr=''
                    for d in dirs: dstr += os.path.join(project.getDir(),d) + ' ' 
                    print dstr
                if self.options.myfiles:
                    filestr = ''
                    for v in project.getVertexList(kinds=[self.kind]):
                        files = v._getMyUserFiles(project)
                        filestr += ' '.join(files)
                    print filestr
                if not (self.options.mydirs or self.options.myfiles):
                    for v in project.getVertexList(kinds=[self.kind]):
                        print v.prettystr(), '\n'
            graph.save()
        else:
            if self.options.mydirs:
                dirs = self.project.getLocationManager().getPortLoc()
                dirs.extend(self.project.getLocationManager().getSIDLDirs(self))
                dstr = ''
                for d in dirs: dstr += os.path.join(self.project.getDir(),d) + ' ' 
                print dstr
            if self.options.myfiles:
                print ' '.join(self._getMyUserFiles(None))
            if not (self.options.mydirs or self.options.myfiles):
                return BVertex.display(self)
    
    def whereis(self):
        return self.edit()

    def edit(self):
        '''edit interface SIDL_SYMBOL options
        '''     
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        self.validateExistingSymbol(pgraph)
                
        print >>DEBUGSTREAM,'edit ' + self.kind + ', name = ', self.symbol
        
        if self.action == 'whereis':
            printonly = True
        else:
            printonly = False

        # do everything we would do if the file had been edited with editfile
        if self.options.touchsidl:
            sidlfile = os.path.join(project.getDir(), self._b_sidlFile)
            if not sidlfile:
                err('Cannot find SIDL file : ' + str(sidlfile))
            print >>DEBUGSTREAM, 'touching ' + sidlfile
            self.project.getBuilder().changed([self] + list(self.dependents()))
            self.project.getBuilder().update()
        elif self.options.editrules:
            makefileInfo = self.project.getLocationManager().getUserBuildfilesLoc(self)
            makefile = os.path.join(project.getDir(), os.path.join(makefileInfo[0], makefileInfo[1][1]))

            self.modifyFile(makefile, printonly)
        elif self.options.editvars:
            makefileInfo = self.project.getLocationManager().getUserBuildfilesLoc(self)
            makefile = os.path.join(project.getDir(), os.path.join(makefileInfo[0], makefileInfo[1][0]))

            self.modifyFile(makefile, printonly)
        elif self.options.editsidl:
            sidlfile = os.path.join(project.getDir(), self._b_sidlFile)

            self.modifyFile(sidlfile, printonly)
        return 0
    
    def modifyFile(self, file, printonly):
        if not file:
            err('Cannot find file: %s' % str(file))
        print >>DEBUGSTREAM, 'editing ' + file

        changed = False
        try:
            changed = editFile(file, printonly, self.method)
        except:
            err('Could not edit file: %s' % str(file))

        if changed:
            self.project.getBuilder().changed([self] + list(self.dependents()))
            self.project.getBuilder().update()
        return
        
    def remove(self):
        """remove interface [options] SIDL_SYMBOL
        
        Remove the specified interface from the project.
        """
        
        if len(self.args) != 1:
            self.usage(exitcode=4,errmsg='[remove ' + self.kind + '] The SIDL interface symbol must be specified.')
           
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        self.validateExistingSymbol(pgraph)

        print >>DEBUGSTREAM,'remove ' + self.kind + ', name = ', self.symbol
        
        dependents = list(self.dependents())

        # Remove the old SIDL file
        fileManager.rm(os.path.join(self.project.getDir(),self._b_sidlFile))
        
        # Remove build artifacts
        self.setAttr('removed',True)
        self.project.getBuilder().remove([self])

        print >>DEBUGSTREAM, 'removing references for ', self.symbol
        
        
        # Now change all references in dependent vertices
        for v in dependents:
            v.removeInternalSymbol(self.symbol)
            
        # Remove vertex from project graph, including all connected edges 
        pgraph.removeVertex(self)

        print >>DEBUGSTREAM, 'updating builder for ', self.symbol

        self.project.getBuilder().changed([self] + dependents)
        self.project.getBuilder().update()
        
        # Save project graph
        retcode = pgraph.save()
        print >>DEBUGSTREAM, 'remove ' + self.kind + ' returning with code', retcode
        return retcode
    
    def rename(self):
        """rename interface [options] SIDL_SYMBOL NEWSIDL_SYMBOL
        
        Rename the interface specified with the SIDL symbol SIDL_SYMBOL to NEWSIDL_SYMBOL.
        The SIDL file containing the interface definition is also renamed.
        """
        if len(self.args) != 2:
            self.usage(exitcode=4,errmsg='[rename ' + self.kind + '] The old and new SIDL interface names must be specified.')
            self.newsymbol = self.args[1]
           
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        
        self.validateExistingSymbol(pgraph)
        
        if self.newsymbol is None: 
            # TODO: Also add actual check for valid SIDL symbol names
            err('invalid SIDL symbol name: ' + str(self.newsymbol))
            
        status,self.newsymbol = cct._validate.sidlType(self.newsymbol,defaultPackage=self.symbol[0:self.symbol.rfind('.')], kind=self.kind, graph=pgraph)
        flag, v = pgraph.containsSIDLSymbol(self.newsymbol)
        if flag:
            err('[rename ' + self.kind + '] the specified SIDL symbol already exists: ' + v.prettystr(), 4)
 
        print >>DEBUGSTREAM,'rename ' + self.kind + ', name = ', self.symbol, ' to ', self.newsymbol
        
        # Read in current code
        oldFileName = os.path.join(self.project.getDir(), self._b_sidlFile)
        oldPkg = self.symbol[0:self.symbol.rfind('.')]
        newPkg = self.newsymbol[0:self.symbol.rfind('.')]
    
        # Remove buld artifacts
        self.project.getBuilder().remove([self])
            
        # Update the graph
        oldsymbol = self.symbol
        self.changeSymbol(self.newsymbol)
        
        if oldPkg != newPkg:
            pkg = project.addNestedPackages(symbol=self.symbol[0:self.symbol.rfind('.')])
            edge = BEdge(pkg, self, pgraph, action='contains')  # Connect with parent package, this adds self to graph

        newFileName = os.path.join(project.getDir(),self.project.getLocationManager().getSIDLLoc(self)[0],self.newsymbol+'.sidl')        
        #self.setAttr('sidlFileName', newFileName)
        self._b_sidlFile = os.path.join(self.project.getLocationManager().getSIDLLoc(self)[0], self.newsymbol+'.sidl')
        print >>DEBUGSTREAM, '[rename interface] vertex changed to: ' + str(self)
        
        # Do the actual rename
        result = renameFromFile(targetName=newFileName, srcName=oldFileName, 
                                targetBuffer=self.createSIDLString(newFileName,project,pgraph),
                                targetKey=self.getSIDLSplicerKey(), 
                                sourceKey=self.getSIDLSplicerKey(), 
                                oldtype=oldsymbol, newtype=self.newsymbol,
                                warn=False)
        if result != 0 or not os.path.exists(newFileName):
            err('rename ' + self.kind + ' failed to create a new SIDL file: ' + newFileName)

        # Remove the old file
        fileManager.rm(oldFileName)
        
        # Now change all references in dependent vertices
        for v in self.dependents():
            v.renameInternalSymbol(oldsymbol, self.symbol)
        
        print >> DEBUGSTREAM, '$$$$ dependents = ', self.dependents()
        self.project.getBuilder().changed([self] + list(self.dependents()))
        self.project.getBuilder().update()
        
        # Save project graph
        self.saveProjectState(pgraph, graphviz=True)
        print >>DEBUGSTREAM, 'rename ' + self.kind + ' returning with code 0'
        return 0

    
   
# -------------- Inherited "protected" methods
    def renameInternalSymbol(self, oldsymbol, newsymbol):
        '''Replaces any internal references to oldsymbol with newsymbol.'''
        deps = self.getAttr('requires')
        if (deps):
            if (oldsymbol in deps) :
                deps.remove(oldsymbol)
                deps.append(newsymbol)
                self.setAttr('requires', deps)
            if not self.project:
                self.project, graph = Globals().getProjectAndGraph(self.projectName)
            fd = fileManager.open(os.path.join(self.project.getDir(), self._b_sidlFile), "r")
            newBuf = fd.read()
            fd.close()
            newBuf = newBuf.replace(oldsymbol, newsymbol)
            fd = fileManager.open(os.path.join(self.project.getDir(), self._b_sidlFile), "w")
            fd.write(newBuf)
            fd.close()
            
        extends = self.getAttr('extends')  # dictionary of extended symbol and their locations
        if not extends: return 0
        if oldsymbol not in extends.keys():
            return 0

        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        if not self.project: self.project = project
        slist = pgraph.findSymbol(newsymbol)
        newvertex = slist[0]

        # Update the symbol in the list of symbols extended by this vertex
        extends[newvertex.symbol] = newvertex._b_sidlFile
        del extends[oldsymbol]
        self.setAttr('extends',extends)
        self.extends = extends
                
        # Merge the original file with the SIDL (string) with the renamed symbol
        retcode = self._mergeSIDLFileWithNewString(replaceIdentical=False)
        if retcode != 0:
            err('could not rename symbol ' + oldsymbol + ' to ' + newsymbol + ' in ' + self.symbol)
        if self.project is None: self.project = project

        return retcode
    
    def removeInternalSymbol(self, symbol):
        ''' Removes any internal references to symbol.'''
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        if not self.project: self.project = project
        extends = self.getAttr('extends')  # dictionary of extended symbol and their locations

        if not extends: return 0
        if symbol not in extends.keys():
            return 0

        # Remove the symbol from the list of symbols this vertex extends
        # If this vertex was extending a port that's being removed, we need to 
        # add gov.cca.Port to the current vertex extends dictionary.
        vlist = pgraph.findSymbol(symbol)
        if not vlist: return 0
        v = vlist[0]
        v_extends = v.getAttr('extends')
        if v_extends and 'gov.cca.Port' not in extends.keys() and 'gov.cca.Port' in v_extends.keys():
            extends['gov.cca.Port'] = '%local%'
        del extends[symbol]
        self.setAttr('extends',extends)
        self.extends = extends
                
        print >>DEBUGSTREAM, 'removeInternalSymbol: new extends =' + str(self.extends)
        # Merge the original SIDL file with the SIDL (stirng) with the symbol removed
        retcode = self._mergeSIDLFileWithNewString(replaceIdentical=False)
        if retcode != 0:
            err('could not remove symbol ' + symbol + ' from ' + self.symbol)

        return retcode
        
        
# ---------------------------------------------------
# -------------------- Private methods --------------

    def createSIDLString(self, sidlFileName, project, pgraph, extraSplicerComment=False):
        '''Create a list of lines that will go in the SIDL file.'''
        symbols = self.symbol.split('.')
        nsyms = len(symbols)
        shortInterfaceName = symbols[-1]
        extends = self.getAttr('extends')
        if not extends: extends = {}

        pkg = pgraph.findSymbol(symbol=symbols[0],kind='package')
        if len(pkg) != 1:
            errmsg = 'missing or ambiguous package name encountered: ' + symbols[0] 
            if len(pkg) > 1: errmsg += '(possibilities are ' + str(pkg) + ')'
            err(errmsg)
            
        defaults = project.getDefaults()
        topPackage = pkg[0]
        topVersion = topPackage.version
        pkgsymbol = topPackage.symbol
        buf = ''
        
        buf += topPackage.getCommentSplicerString(extraSplicerComment=extraSplicerComment)
        buf += 'package ' + symbols[0] + ' version ' + topVersion + ' {\n' 
        tab = int(re.split('\W+', defaults.get('SIDL','tab_size'))[0])*' '  # get rid of comments
        indent = 0
        # Handle nested packages
        for shortPkg in symbols[1:nsyms-1]:
            indent += 1
            pkgsymbol = pkgsymbol + '.' + shortPkg
            pkgs = pgraph.findSymbol(symbol=pkgsymbol, kind='package')
            if len(pkgs) != 1:
                errmsg = 'missing or ambiguous package name encountered: ' + pkgsymbol 
                if len(pkg) > 1: errmsg += '(possibilities are ' + str(pkg) + ')'
                err(errmsg)
            pkg = pkgs[0]
            if pkg is None: err('[create ' + self.kind + '] Package not properly added to graph, could not create sidl file.')
            buf += pkg.getCommentSplicerString(indentstr=indent*tab, extraSplicerComment=extraSplicerComment)
            if pkg.version != topVersion and pkg.version != '0.0':
                buf += indent*tab + 'package ' + shortPkg + ' version ' + pkg.version + ' {\n' 
            else:
                buf += indent*tab + 'package ' + shortPkg + ' {\n' 
               
        indent += 1
        save_indent = indent
        # Handle interfaces being extended if any specified with --extends/-e
        if len(extends) == 0:
            buf += self.getCommentSplicerString(indentstr=indent*tab, extraSplicerComment=extraSplicerComment)
            buf += indent*tab + 'interface ' + shortInterfaceName + '\n'     
        else:
            # Interfaces being extended (if any). TODO: should we check whether these exist?
            interfaces = extends.keys()
            buf += self.getCommentSplicerString(indentstr=indent*tab, extraSplicerComment=extraSplicerComment)
            firstline = indent*tab + 'interface ' + shortInterfaceName + ' extends ' + interfaces[0]
            buf += firstline
            if len(interfaces)>1: buf += ',\n'
            else: buf += '\n'
            indentstr = firstline.find(interfaces[0])*' '
            for i in range(1,len(interfaces)-1):
                buf += indentstr + interfaces[i] + ',\n' 
            if len(interfaces) > 1: buf += indentstr + interfaces[-1] + '\n'
            
        indent = save_indent

        buf += indent*tab + '{\n'
        indent += 1
        indentstr = indent*tab 
        self.setAttr('methodsIndent', indent)
        buf += self.getSIDLSplicerBeginString(indentstr, tag = self.symbol + '.methods', 
                                              extraSplicerComment=extraSplicerComment, 
                                              insertComment='Insert your ' + self.kind + ' methods here') 
        buf += self.getSIDLSplicerEndString(indentstr, tag = self.symbol + '.methods') 
            
        indent -= 1
        buf += indent * tab + '}\n'
        
        for i in range(1,nsyms-1):
            indent -= 1
            buf += indent*tab + '}\n'
        indent = 0
        buf += '}\n'
        
        print >>DEBUGSTREAM, buf
               
        return buf

    def createSIDL(self):
        self.createSIDLFile()
        return 0
    
    def createSIDLFile(self, project = None, pgraph = None):
        if not project or not pgraph:
            project,pgraph = Globals().getProjectAndGraph(self.projectName)

        print >> DEBUGSTREAM, 'Creating SIDL file for ', self.symbol
        print >> DEBUGSTREAM, 'SIDLLoc = ', self.project.getLocationManager().getSIDLLoc(self)
        sidlFileName = os.path.join(self.project.getLocationManager().getSIDLLoc(self)[0],self.symbol+'.sidl')
        if os.path.exists(os.path.join(self.project.getDir(),sidlFileName)):
            err('[create ' + self.kind + '] ' + self.kind + ' SIDL file already exists: ' + sidlFileName,3)
        
        #self.setAttr('sidlFileName',sidlFileName)    
        self._b_sidlFile = sidlFileName

        sidlFileName = os.path.join(self.project.getDir(),sidlFileName)
        sidlSrc = splicers.Source.Source()
        status, msg = sidlSrc.loadString(input=sidlFileName, key='bocca.splicer', 
                                         linebuf=self.createSIDLString(sidlFileName, project, pgraph, extraSplicerComment=True), 
                                         warn=False)
        
        if status != 0:
            err(msg,status)
        print >>DEBUGSTREAM, '['+self.kind+'] loaded sidl file: ' + self._b_sidlFile

        sidlSrc.write(sidlFileName, rejectSave=False)
        print >>DEBUGSTREAM, '[create ' + self.kind + '] Interface sidl file was created:', sidlFileName

        return 
        
    def updateProjectState(self, project, pgraph):
        # Add packages if not already in the graph
        
        if self.action == 'create':
            pkg = project.addNestedPackages(symbol=self.symbol[0:self.symbol.rfind('.')])
            edge = BEdge(pkg, self, pgraph, action='contains')  # Connect with parent package, this adds self to graph
        
        # Add edges to interfaces being extended (if any) and any other dependencies
        if len(self.extends) > 0:
            self.extends, syms = self._validateProjectSymbols(pgraph, self.extends)
            for i in self.extends.keys():
                vlist = pgraph.findSymbol(i,kind='interface')
                
                if len(vlist) == 0: 
                    # Try a port
                    vlist = pgraph.findSymbol(i,kind='port')
                else:
                    v = vlist[0]
                if len(vlist) == 0:
                    # Create an interface vertex
                    v = Interface(symbol=i, project=self, version=self.version)
                else:
                    v = vlist[0]
                edge = BEdge(v, self, pgraph,action='extends')
                     
            ext = self.getAttr('extends')                
            if not ext: 
                self.setAttr('extends',self.extends)
            else: 
                ext.update(self.extends)
                self.setAttr('extends', ext)
            
        self.handleNonInheritanceDependencies()
                    
        return
    
    def prettystr(self):
        project, graph = Globals().getProjectAndGraph()
        s =  self.kind + ' ' + self.symbol + ' ' + self.version 

        extends = self.getAttr('extends')
        if extends and len(extends) > 0:
            s += '\n\textends interfaces: ' + ', '.join(extends.keys()) 
                    
        otherdeps = self.getAttr('requires')
        if otherdeps:
            s += '\n\tdepends on these symbols:\n\t  ' + ', '.join(otherdeps)  + '\n'
            
        mysidldir, sidlfiles = project.getLocationManager().getSIDLLoc(self)
        s += '\n\tSIDL definition: ' + os.path.join(mysidldir,sidlfiles[0])

        return s

    ##---------------------------------------------------------------------------------------------------
    ##                        ------------- Private methods -----------------------
    ##---------------------------------------------------------------------------------------------------
    
    def _processCommonCreateAndChangeArgs(self):
        # --extends option
        if len(self.options.sidlsymbol_and_location) > 0:
            print >> DEBUGSTREAM, 'sidlsymbol_and_location = ', self.options.sidlsymbol_and_location
            self.extends = self._processSymbolAssociationOptions(self.options.sidlsymbol_and_location, '--extends/-e')

        if self.options.xmlRepos:
            warn("--xml option is deprecated. Use depl.xml files and --dpath options instead.")
            self._b_xmlRepos = self.options.xmlRepos
            for r in self._b_xmlRepos:
                if not os.path.exists(r):
                    err("Specified XML repository " + r + " does not exist", 3)
                if not os.path.isdir(r):
                    err("Specified XML repository location " + r + " is not a directory.", 3)
                      
        self._processDependencyArgs()
        
        # --import-sidl option
        if self.options.sidlimports:
            self._processImportArgs()
        pass
    
    def _processCreateArgs(self):

        if len(self.args) < 1:
            self.usage(exitcode=4,errmsg='[create ' + self.kind 
                       + '] A SIDL ' + self.kind 
                       + ' name (e.g. packageName.sidlSymbol) is required for '
                       + self.kind + ' creation.')

        self.symbol = self.args[0]
        self._processCommonCreateAndChangeArgs()
        
        pass

    def _processCopyArgs(self):
        """ Process command line arguments passed to "interface copy" command
        """
        from cct._validate import sidlType as validateSIDLType
        options = self.options
        args = self.args

        project,graph = Globals().getProjectAndGraph(self.projectName)

        if len(self.args) != 2:
            self.usage(exitcode=4,errmsg='[copy ' + self.kind + \
                       '] The old and new SIDL types names must be specified.')
# Figure out old class name and package name
        if not self.symbol: self.symbol = args[0]
        self.validateExistingSymbol(graph)
        self.newsymbol = args[1]
        
        status,self.newsymbol = validateSIDLType(self.newsymbol,
                                defaultPackage=self.symbol[0:self.symbol.rfind('.')], 
                                kind=self.kind, graph=graph)
        flag, v = graph.containsSIDLSymbol(self.newsymbol)
        if flag:
            err('[copy ' + self.kind + '] the specified SIDL symbol already exists: ' 
                + v.prettystr(), 4)
        
        print >> DEBUGSTREAM, 'Interface: Copying ', self.symbol , 'to ', self.newsymbol
        #self.symbol = self.newsymbol
        pass
    
    def _processChangeArgs(self):
        if len(self.args) < 1:
            self.usage(exitcode=4,errmsg='[change ' + self.kind + '] The SIDL ' + self.kind + ' symbol must be specified.')
            
        self._processCommonCreateAndChangeArgs()
        
        self.symbol = self.args[0]
        pass
    
    def _processEditArgs(self):
        if len(self.args) > 2 or len(self.args) < 1:
            self.usage(exitcode=4,errmsg='[edit ' + self.kind + '] <SIDL symbol> [optional babel splice name].')
        self.symbol = self.args[0]
        if len(self.args) == 2:
            self.method = self.args[1]
        else:
            self.method = None
        pass

    def _processRenameArgs(self):
        if len(self.args) != 2:
            self.usage(exitcode=4,errmsg='[rename ' + self.kind + '] The old and new SIDL interface types must be specified.')

        if self.symbol is None:
            self.symbol = self.args[0]
        self.newsymbol = self.args[1]
        pass

    def _processRemoveArgs(self):
        if len(self.args) != 1:
            self.usage(exitcode=4, errmsg='[remove ' + self.kind + '] The SIDL interface type must be specified.')
            
        if self.symbol is None:
            self.symbol = self.args[0] 
        pass
    
    def _processDisplayArgs(self):
        if len(self.args) < 1:
            # display all
            self.displayAll = True
            if not self.symbol: self.symbol = 'temp'
        pass

    def _defineImportArgs(self):
        self.parser.set_defaults(sidlimports=[], mergebuilds=True)
        self.parser.add_option('--import-sidl', dest='sidlimports', action='append', 
                               help='A SIDL file from which to import a specified interface or several interfaces, ' 
                               + 'e.g., --import-sidl="pkg.MySolverInterface,pkg.MyMatrixInterface@/path/to/file.sidl". ' 
                               + 'If no interface is specified (only the SIDL filename is given), all methods from '
                               + 'interfaces in the SIDL file are imported into the specified project ' + self.kind + '.')
        self.parser.add_option('--no-merge-buildfiles', dest='mergebuilds', action='store_false',
                               help="If the SIDL being imported is from another bocca project, do "
                               + "not merge together build files.")
        pass

    def _checkExtends(self):
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        
        # Check whether parents already extend some of these interfaces (Python gets very unhappy
        # when port B extends both port A (which extends gov.cca.Port) and gov.cca.Port
        for v in self.dependencies():
            if v.symbol in self.extends.keys():
                del self.extends[v.symbol]
            
        existing = self.getAttr('extends')
        # Check for multiple identical types
        for t in self.extends.keys():
            if self.extends.keys().count(t) > 1:
                err('An interface cannot be extended more than once: ' + str(t))
            if existing and t in existing.keys():
                err('This ' + self.kind + ' already extends this interface: ' + str(t))
                
        # Now check the vertices in the extends option
        for symbol in self.extends.keys():
            plist = pgraph.findSymbol(symbol)
            if not plist: continue
            parentextends = plist[0].getAttr('extends')
            if not parentextends: continue
            for sym in parentextends.keys():
                if sym in self.extends.keys():
                    del self.extends[sym]
                    
        if self.extends: self.setAttr('extends',self.extends)
        
        return 0
    
    def _mergeSIDLFileWithNewString(self, replaceIdentical=False, targetFile=None):
        # Merge the original file with the newly generated SIDL (string) incorporating changes to parent interfaces   
        warn = False
        if 'BOCCA_DEBUG' in os.environ.keys():
            if os.environ['BOCCA_DEBUG'] == "1":
                warn = True    
                
        project,pgraph = Globals().getProjectAndGraph(self.projectName)    
        if targetFile is None: targetFile = os.path.join(project.getDir(),self._b_sidlFile)
                
        sidlFile = os.path.join(project.getDir(),self._b_sidlFile)    
        result = mergeFileIntoString(targetName=targetFile, 
                                 targetString=self.createSIDLString(sidlFile,project,pgraph),
                                 srcName=sidlFile,
                                 targetKey=self.getSIDLSplicerKey(), 
                                 sourceKey=self.getSIDLSplicerKey(), 
                                 insertFirst=False, warn=warn, verbose=False, 
                                 replaceIdentical=replaceIdentical)

        try:
            fileManager.writeStringToFile(sidlFile,result)
        except IOError,e:
            err('Could not write to file ' + sidlFile + ': ' + str(e))
        return 0
    
    def _getMyUserFiles(self, project=None, fullpath=True):
        # Get a list of user files (usually for revision control interactions)
        if not project:
            if not self.project: project, graph = Globals().getProjectAndGraph(projectName=self.projectName)
            else: project = self.project
        files = []
        sidldir, sidlfiles = project.getLocationManager().getSIDLLoc(self)
        makedir, makefiles = project.getLocationManager().getUserBuildfilesLoc(self)
        if fullpath:
            for f in sidlfiles: files.append(os.path.join(project.getDir(),sidldir,f))
            for f in makefiles: files.append(os.path.join(project.getDir(),makedir,f))
        else:
            for f in sidlfiles: files.append(os.path.join(sidldir,f))
            for f in makefiles: files.append(os.path.join(makedir,f))
        return files
