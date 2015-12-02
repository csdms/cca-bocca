""" Setting up a new project is the job of this script. Anything which
is also done by other cct commands is delegated to those.
This script must not be called directly from a command line; it
must be dispatched through bocca.
bocca init -h for usage.
"""

from cct._debug import DEBUGSTREAM, WARN, BLOCKDUMP
from cct._util import Globals, fileManager, mySplicer, lang_to_fileext, \
    lang_to_headerext, editFile, isBoccaSource, getProjectInfo
from cct._file import BFileManager
from graph.boccagraph import BEdge, BVertex, SymbolError
from cct._err import err, warn
from cct._typedmap import TypedMap
from cct._validate import language as validateLang
from cct._validate import validateDialect
from cct.interface import Interface
from cct._sidlgen import getSidl, getReservedMethods
import os, re
import glob
from sets import Set
from writers.boccaWriterFactory import BoccaWriterFactory
from writers.sourceWriter import SourceWriter
from splicers import Source, Operations
  
class Sidlclass(BVertex): 
    """Add new SIDL class to current project.
    """
    
    def __init__(self, action = '__init__', args = None, project = None, 
                 modulePath = None, symbol=None, kind = 'class', version='0.0', 
                 graph=None):
        '''bocca <verb> class [options] SIDL_SYMBOL
        
        <verb> is one of create, change, remove, rename, display. For 
        documentation on specific verbs, use 'bocca help <verb> sidlclass'
        '''
        print >> DEBUGSTREAM, "UH_SIDLCLASS_INIT", symbol

        self.implImports = {}
        self.new_extends = {}        # Used in create and change
        self.new_implements = {}     # Used in create and change
        self.displayAll = False      # Used in display
        self.displaylangs = ['c', 'cxx', 'f77', 'f77_31', 'f90', 'java', 'python']
        self.graph = None
        if (symbol == 'temp'): 
            BVertex.__init__(self, action = action, 
                               args = args, modulePath = modulePath, 
                               project = project,
                               symbol = symbol, version = version, graph = graph)
            return
        
        self.project = project

        if self.project is not None:
            # Note that project can be None if we ended up here by way 
            # of 'bocca help', which is allowed outside of a project
            self.projectName =self.project.getName()
            info = Globals().getProjectAndGraph(self.projectName)
            self.projectNode = info[0]
            self.graph = info[1]
            self._b_className = None
            self._b_packageName = None
            self.version = None

        self.action = action
        self._b_language = ''
        self.copyLanguage = ''      # Used for copy
        self._b_dialect = ''
        self.copyDialect = ''       # Used for copy
        self._b_xmlRepos = []
        self._b_sidlFile=''
        self._b_implSource=''
        self._b_implHeader=''
        self.symbol=symbol
        self._b_extends={}
        self._b_implements={}
        self._b_beans = TypedMap()   # key: (type, value)
        self.newSymbol = ''          # Used for rename/copy
        self.new_beans = TypedMap()  # Used in create and change
        BVertex.__init__(self, action = action, 
                             args = args, modulePath = modulePath, 
                             project = project, kind = kind, 
                             symbol = symbol, version = version, graph=graph)
        pass

    def initCopy(self, copiedSidlclass):
        self._b_language = copiedSidlclass.copyLanguage
        self._b_dialect = copiedSidlclass.copyDialect
        self._b_xmlRepos = copiedSidlclass._b_xmlRepos
        
        # Necessary to process extension/implementation symbols in graph or Externals[]
        # correctly
        if (len(copiedSidlclass._b_extends) > 0):
            self.options.extended_symbol = ''

            extended_symbol = copiedSidlclass._b_extends.keys()[0]
            value = copiedSidlclass._b_extends.values()[0]
            if (value != '%local%'):
                extended_symbol = extended_symbol +  ":" + value
            self.options.extended_symbol = extended_symbol
        if (len(copiedSidlclass._b_implements) > 0):
            self.options.implemented_symbol = []

            for key, value in copiedSidlclass._b_implements.iteritems():
                implemented_symbol = key[:]  # Copy key
                if value != '%local%':
                    implemented_symbol = implemented_symbol + ":" + value
                self.options.implemented_symbol.append(implemented_symbol)

        requires = copiedSidlclass.getAttr('requires')
        if (requires is not None and len(requires) > 0):
            for symbol in requires:
                requirement = symbol
                if symbol in copiedSidlclass._b_externalSidlFiles.keys():
                    requirement += ":" + copiedSidlclass._b_externalSidlFiles[symbol]
                self.options.required_symbol.append(requirement)

        self.implImports = copiedSidlclass.implImports
        BVertex.initCopy(self, copiedSidlclass)

        # Process extends/implements arguments; avoid processCreateArgs() to skip duplicate
        # -l/-d processing
        self.processCommonCreateAndChangeArgs()
        
# ------------------------------------------------
    def defineArgs(self, action):
        '''Defines command line options and defaults for this command. This is 
           invoked in the constructor of the parent class Subcommand.
        '''
        if (action == 'create'):
            self.defineArgsCreate()
        elif (action == 'copy'):
            self.defineArgsCopy()
        elif (action == 'change'):
            self.defineArgsChange()
        elif (action == 'rename'):
            pass
        elif action == 'display':
            self.defineArgsDisplay()
        elif action == 'edit' or action == 'whereis':
            self.defineArgsEdit()
        elif action == 'remove':
            self.defineArgsRemove()
        else:
            err('Sidlclass verb "' + action + '" NOT implemented yet.', 3)

        return
        
        
# ------------------------------------------------
    def defineCommonArgsCreateAndChange(self):
        '''Defines options common to the create and change operations.'''
        
        self.parser.add_option("-i", "--implements", dest="implemented_symbol", 
                               action="append",
                               help='a SIDL interface that the ' + self.kind 
                               + ' being created implements (optional, can be '
                               + 'repeated). Multiple --extends options can be specified. '
                               + 'If IMPLEMENTED_SYMBOL is an existing external '
                               + 'interface, the file containing its definition must be '
                               + 'specified immediately following the the IMPLEMENTED_SYMBOL, ' 
                               + 'e.g., --implements pkg.SomeInterface@/path/to/somefile.sidl '
                               + '(Babel-generated XML files are allowed, as well).'
                               + 'To change the location of the SIDL file associated '
                               + 'with an interface, use '
                               + 'the "change ' + self.kind + ' +  SIDL_SYMBOL '
                               + '--sourcefile/-s FILENAME" command.')
        self.parser.add_option("-e", "--extends", dest="extended_symbol", 
                               action="store",
                               help='a SIDL class that the ' + self.kind 
                               + ' being created or modified extends (optional). ' 
                               + 'Only one --extends option can be specified. '
                               + 'If EXTENDED_SYMBOL is an existing external '
                               + 'class, the file containing its definition must be '
                               + 'specified immediately following the the EXTENDED_SYMBOL, ' 
                               + 'e.g., --extends pkg.SomeClass@/path/to/somefile.sidl '
                               + '(Babel-generated XML files are allowed, as well).'
                               + 'To change the location of the SIDL file '
                               + 'associated with a class, use'
                               + 'the "change ' + self.kind 
                               + ' +  SIDL_SYMBOL --sourcefile/-s FILENAME" command.')
        
        self._defineDependencyArgs()    # in BVertex
        self._defineImportArgs()        # in BVertex
        self._defineDpathArgs()         # in BVertex
        
        self.parser.add_option("-v", "--version", dest="version",
                               help="SIDL version of the " + self.kind 
                               + " in the form X.Y. If no version specification "
                               + " is given, version '0.0' is used.")
        
        self.parser.add_option("-x", "--xml", dest="xmlRepos", action="append",
                               help='path to external XML repositories containing '
                               + 'specification of the interfaces and/or classes '
                               + 'implemented and/or extended by the new class (or '
                               + 'of symbols referenced by those interfaces). '
                               + 'Multiple repositories can be used (separated '
                               + 'by commas). Alternatively, multiple instances '
                               + 'of the -x option can be used to specify '
                               + 'multiple repositories paths.')

# -L/--libraries is deprecated. It belongs in the appropriate make.vars.user or configure.in
        
    def defineArgsCreate(self):
        '''Defines command line options and defaults for the create action. 
        '''
        # Note that this method must work even when we are outside 
        # a project (for displaying help)
        defaultLanguage = 'cxx'
        defaultDialect = 'standard'
        if self.project is not None:
            defaults = self.project.getDefaults()
            if defaults is not None: 
                if 'Babel' in defaults.sections(): 
                    defaultLanguage = defaults.get('Babel','default_language')
                    try:
                        defaultDialect = defaults.get('Babel','default_dialect')
                    except:
                        pass
            self._b_language = defaultLanguage
            self._b_dialect = defaultDialect
            
        print >> DEBUGSTREAM, "self.__class__.__name__ = ", self.__class__.__name__
        
        self.parser.add_option("-l", "--language", dest="language",
                          help="language for " + self.kind 
                          +" [project default is %s]"%defaultLanguage)
        self.parser.add_option("-d", "--dialect", dest="dialect",
                          help="language dialect for " + self.kind 
                            +" [project default is %s]"%defaultDialect)
        
        self.defineCommonArgsCreateAndChange()
        
        self.parser.set_defaults(language=self._b_language,
                                 dialect=self._b_dialect,
                                 version = '0.0',
                                 xmlRepos=None,
                                 sidlFiles=None,
                                 implements = None,
                                 extends = None)
        return

    def defineArgsCopy(self):
        '''Defines command line options and defaults for the copy action.
        '''
        print >> DEBUGSTREAM, "self.__class__.__name__ = ", self.__class__.__name__
        # Note that this method must work even when we are outside 
        # a project (for displaying help)
        defaultLanguage = 'cxx'
        defaultDialect = 'standard'
        if self.project is not None:
            defaults = self.project.getDefaults()
            if defaults is not None: 
                if 'Babel' in defaults.sections(): 
                    defaultLanguage = defaults.get('Babel','default_language')
                    try:
                        defaultDialect = defaults.get('Babel','default_dialect')
                    except:
                        pass

        self.parser.add_option("-l", "--language", dest="language",
                          help="language for " + self.kind 
                          +" [project default is %s]"%defaultLanguage)
        self.parser.add_option("-d", "--dialect", dest="dialect",
                          help="language dialect for " + self.kind 
                            +" [project default is %s]"%defaultDialect)
        self.parser.add_option("--no-impl", dest="copysrcimpl", action="store_false",
                               help="Don't copy original implementation from source.")

        self.parser.set_defaults(language=None,
                                 dialect=None,
                                 copysrcimpl=True)
    
    def defineArgsChange(self):
        self.defineCommonArgsCreateAndChange()
        self.parser.add_option("--remove-implements", dest="removeImplements", action="append",
                               help="remove implementation statements for the given SIDL symbol.  " 
                               + "Multiple implementations can be removed by repeated --remove-implements options.")
        self.parser.set_defaults(version = self.version,
                                 xmlRepos=None,
                                 sidlFiles=None,
                                 implements = None,
                                 extends = None,
                                 removeImplements=None)
        return
    
    def defineArgsDisplay(self):
        '''Defines command line options for the display action.
        '''
        self.parser.add_option('-d', '--dirs', dest="mydirs", action='store_true',
                               help="Show a list of directories containing "
                               + "user-editable files; this can be used as "
                               + "input for revision control operations.")
        self.parser.add_option('-f', '--files', dest="myfiles", action='store_true',
                               help="Show a list of user-editable files, which "
                               + "can be used as input for revision control operations.")
        self.parser.add_option("-l", "--languages", dest="languages", action='append',
                               help="display all " + self.kind +" elements "
                               + "whose implementations are in the specified "
                               + "language. To specify multiple languages, "
                               + "multiple -l options can be given, or a "
                               + "comma-separated list of languages.")
        self.parser.set_defaults(languages=[], mydirs=False, myfiles=False)
        return
    
    def defineArgsEdit(self):
        self.parser.add_option('-H', '--header', dest='editheader', action='store_true',
                               help="Edit/whereis the header (or module in F90) file")
        self.parser.add_option('-m', '--module', dest='editheader', action='store_true',
                               help="Edit/whereis the header (or module in F90) file")
        self.parser.add_option('-i', '--implementation', dest='editimpl', 
                               action='store_true',
                               help="Edit/whereis the implementation file")
        self.parser.add_option('-s', '--sidl', dest='editsidl', action='store_true',
                               help="Edit/whereis the sidl file (the default)")
        self.parser.add_option('-t', '--touch', dest='touchsidl', action='store_true',
                               help="Touch the sidl file as if bocca edit changed it.")
        self.parser.add_option('-r', '--build-rules', dest='editrules', action='store_true',
                               help="Edit the make.rules.user file")
        self.parser.add_option('-V', '--build-vars', dest='editvars', action='store_true',
                               help="Edit the make.vars.user file")
        self.parser.set_defaults(editheader=False, editimpl=False, editsidl=True, 
                                 touchsidl=False, editrules=False, editvars=False)
        return
    
    def defineArgsRemove(self):
        return
        
   
# ------------------------------------------------
    def processArgs(self, action):
        """ Dispatch argument processing based in required action
        """
        print >> DEBUGSTREAM, "Sidlclass processArgs"
        print >> DEBUGSTREAM, "Sidlclass called with options ", \
                              str(self.options) , " leaving args " , str(self.args)
        # Make sure we have handle to project and graph                              
        info = Globals().getProjectAndGraph(self.projectName)
        self.projectNode = info[0]
        self.graph = info[1]
        if (action == 'create'):
            self.processCreateArgs()
        elif (action == 'copy'):
            self.processCopyArgs()
        elif (action == 'change'):
            self.processChangeArgs()
        elif (action == 'display'):
            self.processDisplayArgs()
        elif (action == 'rename'):
            self.processRenameArgs()
        elif (action == 'edit' or action == 'whereis'):
            self.processEditArgs()
        elif action == 'remove':
            self.processRemoveArgs()
        else:
            err("Action "+ action + " NOT implemented yet", 3)
            
        return
    
    def processCommonCreateAndChangeArgs(self):
        print >> DEBUGSTREAM, "Sidlclass processCommonCreateAndChangeArgs"
        options = self.options
        args = self.args

        if len(args) == 0: 
            self.usage(exitcode=4,errmsg='[' + self.action + ' ' + self.kind 
                       + '] The SIDL symbol argument on which to perform this '
                       + 'command is missing.')
        if len(args) > 1:
            self.usage(exitcode=4,errmsg='[' + self.action + ' ' + self.kind 
                       + '] Only one SIDL symbol argument on which to perform '
                       + 'this command must be given.')
            
        self.symbol = self.args[-1]   # BVertex takes care of prepending default package if necessary
        
# Extract and check external XML repos and SIDL files
        if (options.xmlRepos != None):
            warn("--xml option is deprecated. Use depl.xml files and --dpath options instead.")
            self._b_xmlRepos = ','.join(options.xmlRepos).split(',')
            
        for r in self._b_xmlRepos:
            if not os.path.exists(r):
                err("Specified XML repository " + r + " does not exist.", 3)
            if not os.path.isdir(r):
                err("Specified XML repository location " + r + " is not a directory.", 3)

        dpathdata = self._processDpathOptions()
        self._updateDpaths(dpathdata, sidlname=self.symbol)
                
        if options.extended_symbol:
            self.new_extends = \
                self._processSymbolAssociationOptions([options.extended_symbol], 
                                                      '--extends/-e')
            for i in self.new_extends.keys():
                if i in self._b_extends.keys():
                    err('This ' + self.kind + ' already extends this type: ' + str(i))
            self._b_extends.update(self.new_extends)
                
        if options.implemented_symbol:
            self.new_implements = \
                self._processSymbolAssociationOptions(options.implemented_symbol, 
                                                      '--implements/-i')
            if self.kind == 'component': 
                existing = [x.getType() for x in self._b_provides] + self._b_implements.keys()
            else: 
                existing = self._b_implements.keys()
                
            for i in self.new_implements.keys():
                if i in existing:
                    err('This ' + self.kind + ' already implements this interface: ' + str(i))
                if self.new_implements.keys().count(i) > 1:
                    err('An interface cannot be implemented more than once: ' + str(i))
            self._b_implements.update(self.new_implements)
            
        self._processDependencyArgs()    # in BVertex
        
        if options.sidlimports or options.implimports:
            self._processImportArgs()
                    
        self._b_className = self.symbol.split('.')[-1]
        self._b_packageName = '.'.join(self.symbol.split('.')[:-1])
        
        print >> DEBUGSTREAM, "Sidlclass: className = ", self._b_className, \
            "\nSidlclass: packageName = ", self._b_packageName, \
            "\nSidlclass: implements = ", self._b_implements, \
            "\nSidlclass: extends = ", self._b_extends, \
            "\nSidlclass: new_implements = ", self.new_implements, \
            "\nSidlclass: new_extends = ", self.new_extends, \
            "\nSidlclass: symbol = ", self.symbol, \
            "\nSidlclass: language = ", self._b_language, \
            "\nSidlclass: dialect = ", self._b_dialect, \
            "\nSidlclass: xmlRepos = ", self._b_xmlRepos, \
            "\nSidlclass: sidlFiles = ", self._b_externalSidlFiles, \
            "\nSidlclass: sidlImports = ", self.getSIDLImports(), \
            "\nSidlclass: implImports = ", self.implImports
        
        return

    def processCreateArgs(self):
        """ Process command line arguments passed to the "sidlclass create" command
        """
        print >> DEBUGSTREAM, "Sidlclass processCreateArgs"
        options = self.options
        args = self.args
        # Check for valid impl language
        status, self._b_language = validateLang(options.language)
        print >> DEBUGSTREAM, 'Language after validation: status = ', \
            status, ', language = ', self._b_language
        status, self._b_dialect = validateDialect(self._b_language, options.dialect)
        print >> DEBUGSTREAM, 'Dialect after validation: status = ', \
            status, ', dialect = ', self._b_dialect
    

        self.processCommonCreateAndChangeArgs()
    
        self.version = options.version   
        
        print >> DEBUGSTREAM, "\nSidlclass: version = ", self.version 
        
        return 
   
    def processChangeArgs(self):
        if len(self.args) < 1:
            self.usage(exitcode=4,errmsg='[change ' + self.kind 
                       + '] The SIDL interface symbol must be specified.')
        
        if not self.graph: self.graph = Globals().getGraph(self.projectName)
        # Check whether component already exists in project
        self.symbol = self.args[-1]
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        self.validateExistingSymbol(self.graph)
        
        self.processCommonCreateAndChangeArgs()
        
        return 
    
    
    def processRenameArgs(self):
        """ Process command line arguments passed to the "class rename" command
        """
        from cct._validate import sidlType as validateSIDLType
        options = self.options
        args = self.args
        if len(self.args) != 2:
            self.usage(exitcode=4,errmsg='[rename ' + self.kind + \
                       '] The old and new SIDL types names must be specified.')
# Figure out old class name and package name
        if not self.graph: self.graph = Globals().getGraph(self.projectName)
        if not self.symbol: self.symbol = args[0]
        self.validateExistingSymbol(self.graph)
        self.newSymbol = args[1]
        
        status,self.newSymbol = validateSIDLType(self.newSymbol,
                                defaultPackage=self.symbol[0:self.symbol.rfind('.')], 
                                kind=self.kind, graph=self.graph)
        flag, v = self.graph.containsSIDLSymbol(self.newSymbol)
        if flag:
            err('[rename ' + self.kind + '] the specified SIDL symbol already exists: ' 
                + v.prettystr(), 4)
        
        print >> DEBUGSTREAM, 'Sidlclass: Renaming ', self.symbol , 'to ', self.newSymbol
        #self.symbol = self.newSymbol
        return

    def processRemoveArgs(self):
        """ Process command line arguments passed to the "class rename" command
        """
        options = self.options
        args = self.args
        if len(self.args) != 1:
            self.usage(exitcode=4,errmsg='[remove ' + self.kind + \
                       '] The SIDL symbol must be specified.')
        if self.symbol is None:
                self.symbol = self.args[0] 
                
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        self.validateExistingSymbol(self.graph)
             
        print >>DEBUGSTREAM,'remove ' + self.kind + ', name = ', self.symbol
        return 
    
    def processEditArgs(self):
        """ Process edit command line arguments passed to the "class edit" command
        """
        options = self.options
        args = self.args
        if len(self.args) < 1 or len(self.args) > 2:
            self.usage(exitcode=4,errmsg='[' + self.action+' ' + self.kind + \
                       '] <SIDL symbol> [optional babel splice name].')
        if self.symbol is None:
            self.symbol = self.args[0] 
        if len(self.args) == 2:
            self.method = self.args[1]
        else:
            self.method = None
                
        slist = self.graph.findSymbol(self.symbol,self.kind, self.version)
        print >>DEBUGSTREAM, "Searched", self.action+ ' ' + self.kind + ', name = ', self.symbol
        if len(slist) != 1:
            err('specified ' + self.kind + ' not found in this project: ' + self.symbol)
             
        print >>DEBUGSTREAM, self.action+ ' ' + self.kind + ', name = ', self.symbol
        return 
    
    def processDisplayArgs(self):
        if len(self.args) < 1:
            # display all
            self.displayAll = True
        else:
            self.symbol = self.args[0]
            print >>DEBUGSTREAM, "sidlclass.display args", self.args
        if self.options.languages:
            self.displaylangs = []
            for v in self.options.languages:
                tmplist = v.split(',')
                for lang in tmplist: 
                    status, tmplang = validateLang(lang)
                self.displaylangs.append(tmplang)

        if not self.symbol: self.symbol = 'temp'
        pass

    def processCopyArgs(self):
        """ Process command line arguments passed to "component copy" command
        """
        from cct._validate import sidlType as validateSIDLType
        options = self.options
        args = self.args

        # Check for valid impl language
        status = 0
        if options.language is not None and options.language != self._b_language:
            status, self.copyLanguage = validateLang(options.language)
            self.options.copysrcimpl = False
        else:
            self.copyLanguage = self._b_language
        print >> DEBUGSTREAM, 'Language after validation: status = ', \
            status, ', language = ', self.copyLanguage

        if options.dialect is not None and options.dialect != self._b_dialect:
            status, self.copyDialect = validateDialect(self.copyLanguage, options.dialect)
            self.options.copysrcimpl = False
        else:
            self.copyDialect = self._b_dialect
        print >> DEBUGSTREAM, 'Dialect after validation: status = ', \
            status, ', dialect = ', self.copyDialect

        if len(self.args) != 2:
            self.usage(exitcode=4,errmsg='[copy ' + self.kind + \
                       '] The old and new SIDL types names must be specified.')
# Figure out old class name and package name
        if not self.graph: self.graph = Globals().getGraph(self.projectName)
        if not self.symbol: self.symbol = args[0]
        self.validateExistingSymbol(self.graph)
        self.newSymbol = args[1]
        
        status,self.newSymbol = validateSIDLType(self.newSymbol,
                                defaultPackage=self.symbol[0:self.symbol.rfind('.')], 
                                kind=self.kind, graph=self.graph)
        flag, v = self.graph.containsSIDLSymbol(self.newSymbol)
        if flag:
            err('[copy ' + self.kind + '] the specified SIDL symbol already exists: ' 
                + v.prettystr(), 4)
        
        print >> DEBUGSTREAM, 'Sidlclass: Copying ', self.symbol , 'to ', self.newSymbol
        #self.symbol = self.newSymbol
        return
    
# ------------------- Begin BVertex command interface --------------------------

    def create(self):
        """create class SIDL_SYMBOL [options] 
        """
        # Validate vertex and update the project graph
        project,graph = Globals().getProjectAndGraph(projectName=self.projectName)
        if not self.graph: self.graph=graph
        
        self.validateNewSymbol(self.graph)   # From BVertex  

        sidldir, sidlfiles = self.project.getLocationManager().getSIDLLoc(self)
        # Below: relative to project root
        self._b_sidlFile = os.path.join(sidldir, self.symbol + '.sidl') 
        
        return self._createOrChange()
    
    def copy(self):
        """copy component [options] FROM_SIDL_SYMBOL TO_SIDL_SYMBOL
        """

        copyVertex = Sidlclass('create', args=[self.newSymbol], project=self.project, modulePath=self.modulePath,
                               symbol=self.newSymbol, version=self.version, graph=self.graph)
        copyVertex.initCopy(self)

        # Need to import complete SIDL definition from copied class
        copyVertex.sidlImports = { self._b_sidlFile : ['%all'] }

        # settings from -l and -d are handled by copyVertex
        if self.options.copysrcimpl:
            copyVertex.implImports[self.symbol] = self._b_implSource[0:self._b_implSource.rfind('/')]

        return copyVertex.create()

    def change(self):
        """change class SIDL_SYMBOL [options] 

        """
        # Any new change-specific handling goes here or after the call to _createOrChange
        project, graph = Globals().getProjectAndGraph(self.projectName)
        if self.options.removeImplements:
            implemented = self._b_implements.keys()
            for remove in self.options.removeImplements:
                if remove not in implemented:
                    err(self.kind + ' ' + self.symbol + ' does not implement ' + remove)

            print >>DEBUGSTREAM, 'Removing symbols ' + str(self.options.removeImplements) + ' from ' + self.symbol + ' implementations'
            for remove in self.options.removeImplements:
                self.removeInEdge(remove, 'implements', graph)
                del self._b_implements[remove]
                if remove in self._b_externalSidlFiles:
                    del self._b_externalSidlFiles[remove]
                    project.cleanExternal(remove)

            print >>DEBUGSTREAM, "cleaning 'external' cache"
                
        retcode = self._createOrChange()

        self.prettystr()
        return retcode

    def display(self):
        """display class SIDL_SYMBOL
        """
        
        if self.displayAll:
            project, graph = Globals().getProjectAndGraph(projectName=self.projectName)
            if project:
                if self.options.mydirs:
                    dirs = []
                    dirs.extend(project.getLocationManager().getComponentLoc())
                    dirs.extend(project.getLocationManager().getSIDLDirs(self))
                    for v in project.getVertexList(kinds=[self.kind]):
                        if v._b_language in self.displaylangs:
                            dirs.append(project.getLocationManager().getImplLoc(v)[0])
                    dstr = ''
                    for d in dirs: dstr += os.path.join(project.getDir(),d) + ' ' 
                    print dstr
                if self.options.myfiles:
                    filestr = ''
                    for v in project.getVertexList(kinds=[self.kind]):
                        if v._b_language in self.displaylangs:
                            files = v._getMyUserFiles(project)
                            filestr += ' '.join(files)
                    print filestr
                if not (self.options.mydirs or self.options.myfiles):
                    for v in project.getVertexList(kinds=[self.kind]):
                        print v.prettystr()
        else:
            if self.options.mydirs:
                if self._b_language in self.displaylangs:
                    dirs = self.project.getLocationManager().getComponentLoc()
                    dirs.extend(self.project.getLocationManager().getSIDLDirs(self))
                    dirs.append(self.project.getLocationManager().getImplLoc(self)[0])
                    dstr = ''
                    for d in dirs: 
                        dstr += os.path.join(self.project.getDir(),d) + ' ' 
                    print dstr
            if self.options.myfiles:
                if self._b_language in self.displaylangs:
                    print ' '.join(self._getMyUserFiles(None))
            if not (self.options.mydirs or self.options.myfiles):
                return BVertex.display(self)

        return 0

    def whereis(self):
        return self.edit()

    def edit(self):
        '''edit class SIDL_SYMBOL options
        whereis class SIDL_SYMBOL options
        '''     
        print >>DEBUGSTREAM, self.action + ' ' + self.kind + ', name = ', self.symbol
        header = None
        source = None
        sidlfile = None
        makefile = None
        changed = False
        # My header and source filenames
        if self.options.editheader or self.options.editimpl:
            self._b_implHeader, self._b_implSource = self.getClassImplFilenames(self.symbol)
        if self._b_implHeader: 
            header = os.path.join(self.project.getDir(),self._b_implHeader)
        if self._b_implSource: 
            source = os.path.join(self.project.getDir(),self._b_implSource)
        if self.action == 'whereis':
            printonly=True
        else:
            printonly=False

            
        if self.options.editheader:
            if self._b_language.lower() in ['java', 'python', 'f77', 'f77_31']:
                err('Classes implemented in %s do not have a header or '
                    + 'module file.'%self._b_language)
            if not header:
                err('Cannot find header or module file : ' + str(header))
            print >>DEBUGSTREAM,  self.action + 'ing ' + header
            try:
                if self.options.touchsidl:
                    # since no afteredit fixups, treat as whereis.
                    # if we eventually discover some post-edit update is needed
                    # we will need to add more code here to do that instead of whereis.
                    changed = editFile(header, True, self.method)
                else:
                    changed = editFile(header, printonly, self.method)
            except Exception, e:
                print >> DEBUGSTREAM, str(e)
                err('Could not '+self.action+' the file %s: %s' % (header,str(e)))
        elif self.options.editimpl:
            if not source:
                err('Cannot find header or module file : ' + str(source))
            print >>DEBUGSTREAM,  self.action +'ing ' + source
            try:
                if self.options.touchsidl:
                    # since no afteredit fixups, treat as whereis.
                    # if we eventually discover some post-edit update is needed
                    # we will need to add more code here to do that instead of whereis.
                    changed = editFile(source, True, self.method)
                else:
                    changed = editFile(source, printonly, self.method)
            except:
                err('Could not edit the file %s' % source)
        elif self.options.touchsidl:
            # do everything we would do if the file had been edited with editfile
            sidlfile = os.path.join(self.project.getDir(), self._b_sidlFile)
            if not sidlfile:
                err('Cannot find SIDL file : ' + str(sidlfile))
            print >>DEBUGSTREAM, 'touching ' + sidlfile
            changed = True
        elif self.options.editvars:
            makefileInfo = self.project.getLocationManager().getUserBuildfilesLoc(self)
            
            # symbol/make.vars.user
            makefile = os.path.join(self.project.getDir(),
                                    os.path.join(makefileInfo[0], makefileInfo[1][2]))
            if not makefile:
                err('Cannot find makefile: ' + str(makefile))
            print >>DEBUGSTREAM, self.action+'ing ' + makefile
            try:
                changed = editFile(makefile, printonly, None)
            except:
                err('Could not edit the file %s' % makefile)
        elif self.options.editrules:
            makefileInfo = self.project.getLocationManager().getUserBuildfilesLoc(self)
            
            # symbol/make.rules.user
            makefile = os.path.join(self.project.getDir(),
                                    os.path.join(makefileInfo[0], makefileInfo[1][3]))
            if not makefile:
                err('Cannot find makefile: ' + str(makefile))
            print >>DEBUGSTREAM, self.action+'ing ' + makefile
            try:
                changed = editFile(makefile, printonly, None)
            except:
                err('Could not edit the file %s' % makefile)
        else:
            # Edit the SIDL file self.options.editsidl=True
            sidlfile = os.path.join(self.project.getDir(), self._b_sidlFile)
            if not sidlfile:
                err('Cannot find SIDL file : ' + str(sidlfile))
            print >>DEBUGSTREAM, self.action+'ing ' + sidlfile
            try:
                
                changed = editFile(sidlfile, printonly, None) ; 
            except:
                err('Could not edit the file %s' % sidlfile)

        # this check must be done for all kinds of edit, not just sidl files.
        if changed:
            target=sidlfile
            if not target:
                target=source
            if not target:
                target=header
            if not target:
                target=makefile
	
            # True for touch option or if md5 sum changed
            print >>DEBUGSTREAM, 'calling update builder for ' + target
            self.project.getBuilder().changed([self] + list(self.dependents()))
            self.project.getBuilder().update()

        return 0
   
# ------------------------------------------------
    def rename(self):
        """rename class OLD_SIDL_SYMBOL NEW_SIDL_SYMBOL
        """
        self._internalRename()
        self.saveProjectState(self.graph, graphviz=True)
        print self.prettystr()
        return 0
    
    def remove(self):
        """remove class SIDL_SYMBOL
        """
        # STATUS: needs testing
        
        project, pgraph = Globals().getProjectAndGraph(self.projectName)
        self.validateExistingSymbol(pgraph)

        print >>DEBUGSTREAM,'remove ' + self.kind + ', name = ', self.symbol
        dependents = list(self.dependents())

        # Remove the old SIDL file
        fileManager.rm(self._b_sidlFile)

        # Remove the impl dir, saving a copy in the trash
        dirname,flist=os.path.join(self.project.getLocationManager().getImplLoc(self))
        fileManager.rmdir(dirname, trash=True, info=True)
        
        # Remove build artifacts
        self.setAttr('removed',True)
        self.project.getBuilder().remove([self])
        # Regenerate the build files
        self.project.getBuilder().changed([self] + dependents)
        self.project.getBuilder().update()


        # Now change all references in dependent vertices
        for v in dependents:
            v.removeInternalSymbol(self.symbol)

        # Remove vertex from project graph, including all connected edges 
        pgraph.removeVertex(self)
                
        # Save project graph
        retcode = pgraph.save()
        print >>DEBUGSTREAM, 'remove ' + self.kind + ' returning with code', retcode
        return retcode       
    
    def prettystr(self):
        project, graph = Globals().getProjectAndGraph()
        s =  self.kind + ' ' + self.symbol + ' ' + self.version \
            + ' (' + self._b_language + ')'
        
        if len(self._b_implements) > 0:
            s+=  '\n\timplements interfaces:\n'
            for i in self._b_implements.keys(): 
                s +=  '\t  ' + i 
                if self._b_implements[i] != '%local%': 
                    extloc = project.getDefaultValue(i,'External')
                    if extloc: 
                        s += ', location = ' + project.getDefaultValue(i,'External')
                else: 
                    s += ', local'
                s += ' ' + '\n'

        if len(self._b_extends) > 0:
            s += '\n\textends class: ' + self._b_extends.keys()[0]                 
            if self._b_extends.values()[0] != '%local%': 
                s += ', location = ' \
                    + project.getDefaultValue(self._b_extends.keys()[0],'External')
            else: s += ', local'
            s += ' ' + '\n'
            
        otherdeps = self.getAttr('requires')
        if otherdeps:
            s += '\n\tdepends on these symbols:\n\t  ' + ', '.join(otherdeps)  + '\n'
            
        mysidldir, sidlfiles = project.getLocationManager().getSIDLLoc(self)
        s += '\n\tSIDL definition: ' + os.path.join(mysidldir,sidlfiles[0])
        
        myimpldir, impls = project.getLocationManager().getImplLoc(self)
        if not impls[0] or impls[0] == 'None': 
            s += '\n\timplementation:\t' + str(os.path.join(myimpldir, impls[1])) + '\n'
        else:
            files =[]
            for i in impls: files.append(os.path.join(myimpldir,i))
            s +=  '\n\timplementation:\n\t\t' + '\n\t\t'.join(files) + '\n'

        # Temporary for testing
        #s += "Extends hierarchy: " + str([v.symbol for v in self.walk(edgefilter=['extends'])]) + '\n'
        #s += "Implements hierarchy: " + str([v.symbol for v in self.walk(edgefilter=['implements'])]) + '\n'
        return s

    
    # ---------------- end of BVertex command interface implementations --------------------------
   
    def getClassImplFilenames(self, symbol, impldir=None):
        """ Set names of source and header impl files for this class based on
            the given symbol. All file names are relative to self.projectDir
        """
        implHeader=''
        if not self.project: self.project, graph = Globals().getProjectAndGraph()
        myimpldir, impls = self.project.getLocationManager().getImplLoc(self)
        if impldir is None: impldir = myimpldir
        if (self._b_language == 'python'):
            implSource = os.path.join(impldir, symbol.split('.')[-1] + '_Impl.py')
            return None, implSource

        if (self._b_language == 'java'):
            implSource = os.path.join(impldir, symbol.split('.')[-1] + '_Impl.java')
            return None, implSource
               
        implSource = symbol.replace('.','_') + '_Impl.' + \
                           lang_to_fileext(self._b_language)
        implSource = os.path.join(impldir, implSource)

        if (self._b_language.upper() =='F77' or self._b_language.upper() =='F77_31'):
            return None, implSource
        
        hext = lang_to_headerext(self._b_language)
        if (self._b_language.upper() == 'F90'):
            newImplHeaderFile = symbol.replace('.','_') + '_Mod.F90'
        else: 
            newImplHeaderFile = symbol.replace('.','_') + '_Impl.' + hext
            
        implHeader = os.path.join(impldir, newImplHeaderFile)
        return implHeader, implSource
        

    def genClassSidlString(self, extraSplicerComment=False):
        
        extendedClass = ''
        implementedInterfaces = []
        if self._b_extends: extendedClass = self._b_extends.keys()[0]
        if self._b_implements: implementedInterfaces = self._b_implements.keys()

        if self.kind == 'component':
            providesTypes = [x.getType() for x in self._b_provides]
            implementedInterfaces.insert(0,'gov.cca.Component')
            implementedInterfaces.insert(1,'gov.cca.ComponentRelease')
            implementedInterfaces.extend(list(providesTypes))
        
        indent = int(re.split('\W+', self.project.getDefaults().get('SIDL','tab_size'))[0])*' '
        level = 0
        buf = ''
        pkglist = self.symbol.split('.')[:-1]
        fullpkg = ''
        while(len(pkglist) > 0):
            pkg = pkglist.pop(0)
            fullpkg = (fullpkg + '.' + pkg).lstrip('.')
            nodeList = self.graph.findSymbol(fullpkg, kind='package')
            if (len(nodeList) == 0):
                err('Internal BOCCA error - missing package ' + fullpkg, 4)
            node = nodeList[0]
            buf += node.getCommentSplicerString(indentstr=indent*level, 
                                                extraSplicerComment=extraSplicerComment)
            buf += indent*level + 'package %s version %s {\n' % (pkg, node.version)
            pkg = pkg + '.'
            level = level + 1

        buf += self.getCommentSplicerString(indentstr=indent*level, 
                                            extraSplicerComment=extraSplicerComment)
        buf += indent * level + 'class %s ' %(self._b_className)
        if extendedClass:
            buf += ' extends %s \n' % (extendedClass)
        
        if len(implementedInterfaces) > 0 :
            if extendedClass: buf += indent * (level+2) 
            buf += 'implements-all ' + ', '.join(implementedInterfaces) 
            
        buf += '\n' + indent * level +'{\n'
        level += 1
        self.setAttr('methodsIndent',level)
        buf += self.getSIDLSplicerBeginString(indent * level, 
                                              tag = self.symbol + '.methods',
                                              extraSplicerComment=extraSplicerComment, 
                                              insertComment='Insert your ' \
                                                + self.kind + ' methods here') 
        buf += self.getSIDLSplicerEndString(indent * level, tag = self.symbol + '.methods')
        
        indentstr = indent * level 
        if self.kind == 'component': uses = [x.getType() for x in self._b_uses]
        else: uses = []

        depthstring = self.getDepthstring()
        sidllines = getSidl(self._b_language, indentstr, self.symbol, kind = self.kind, 
                            usesvalues = uses, requires = self.getAttr('requires'), depthstring=depthstring)
        if sidllines: buf += '\n\n'
        for i in sidllines:
            buf += i + '\n'

        # Generate a fake little method for making sure that all includes for symbols
        # this class/component is dependent on are automatically inserted
        
        
        level -= 1
        while (level >= 0):
            buf += indent*level + '}\n'
            level = level - 1
            
        buf += '\n'
        print >> DEBUGSTREAM , buf
        return buf

    def getDepthstring(self):
        """ empty for baseless classes, number for extending classes."""
        # Extends hierarchy:  str([v.symbol for v in self.walk(edgefilter=['extends'])]) 
        ancestor_count = len(self.walk(edgefilter=['extends']))
        if ancestor_count == 0:
            depthstring = ""
        else:
            depthstring = str(ancestor_count)
        return depthstring
    
    def createSIDL(self):
        if not self.project or not self.graph: 
            self.project, self.graph = Globals().getProjectAndGraph(self.projectName)
            
        buf = self.genClassSidlString(extraSplicerComment=True)

        if self.action == 'create' or self.action == 'rename' or \
                (self.action == 'change' and self.options.removeImplements):
            # force write of new sidl ahead of completing everything.
            fd = fileManager.open(os.path.join(self.project.getDir(), self._b_sidlFile), "w")
            fd.write(buf)
            fd.close()
        else:
            return self._mergeSIDLFileWithNewString()
            
        return 0

    def genClassImpl(self):
        if not self.project: self.project,graph=Globals().getProjectAndGraph()
        return self.project.getBuilder().genImpls(self)

# ------------------------------------------------    
    def spliceBoccaBlocks(self):
        impldir, flist = self.project.getLocationManager().getImplLoc(self)
        print >> DEBUGSTREAM, '**** in sidlclass spliceBoccaBlocks: ', \
            self.project.getDir(), impldir, flist
        implSourceFile =  os.path.join(self.project.getDir(), self._b_implSource)
        writer = BoccaWriterFactory().getWriter(self._b_language, 
                                                self._b_dialect, 
                                                kind = self.kind)
        
# Splice code into impl source file
# This happens differently on the creation of the class than
# any time afterward. 
        rejectSave = False
        if self.action == "create" or self.action == "add":
            sourceKey="DO-NOT-DELETE splicer"
            print >> DEBUGSTREAM, "## Initial splicing on ", sourceKey, "blocks"
        else:
            sourceKey=SourceWriter().protKey
            print >> DEBUGSTREAM, "## Resplicing on ", sourceKey, "blocks"


        replaceBlockList = []
        replaceBlockList.append(writer.getImplHeaderCode(self.symbol))
        replaceBlockList.append(writer.getConstructorCode(self.symbol))
        replaceBlockList.append(writer.getDestructorCode(self.symbol))
        reqs = self.getAttr('requires')
        if not reqs: nreqs=0
        else: nreqs=len(reqs)
        depthstring = self.getDepthstring()
        replaceBlockList.append(writer.getForceUsePortCode(self.symbol, nreqs, depthstring))
        
        # print >> DEBUGSTREAM, "GENERATED BLOCKS ##############", replaceBlockList
        
        print >> DEBUGSTREAM, 'Splicing Impl file ', implSourceFile
        replaceGiantList = ''.join(replaceBlockList)
        if BLOCKDUMP:
            print >> DEBUGSTREAM, "replaceGiantList"
            print >> DEBUGSTREAM, replaceGiantList
        Operations.mergeFromString(implSourceFile, replaceGiantList, 'REPLACE_BLOCKS', 
                                   targetKey = sourceKey,
                                   sourceKey = sourceKey,
                                   insertFirst = True, 
                                   dbg = WARN, 
                                   verbose = WARN, 
                                   dryrun = False, 
                                   rejectSave= rejectSave, 
                                   warn= WARN)
        return
        
# -----------------------------------------------------------------------------    
    def updateGraph(self):
        
        if self.action == 'create':
            self._b_packageName = self.symbol[0:self.symbol.rfind('.')]
            pkg = self.project.addNestedPackages(symbol=self._b_packageName)
            
            # Connect with parent package, this adds self to graph: 
            edge = BEdge(pkg, self, self.graph, action='contains')  
            self._b_implHeader, self._b_implSource = self.getClassImplFilenames(self.symbol)
        
        #  Check existence of interface nodes in project graph and add edges
        self.new_implements, vertices = \
            self._validateProjectSymbols(self.graph, self.new_implements, 
                                         kinds=['interface','port'])
            
        for ifaceNode in vertices:
            # Connect with implemented interface
            edge = BEdge(ifaceNode, self, graph=self.graph, action = 'implements')  
            
            # Add the new interfaces 
            self._b_implements.update(self.new_implements)
        
        # Check for existence of class/component nodes in project graph and add edges
        self.new_extends, vertices = \
            self._validateProjectSymbols(self.graph, self.new_extends, 
                                         kinds = ['class','component'])
        if vertices:
            # Connect with extended class
            edge = BEdge(vertices[0], self, graph = self.graph, action='extends')  
            if self._b_extends:
                self._b_extends.clear()   # Only one class can be extended
                self._b_extends = self.new_extends
                
        return
    
    def handleImports(self):
        self._b_implHeader, self._b_implSource = self.getClassImplFilenames(self.symbol)
        if self.getSIDLImports():
            retcode = self.handleSIDLImports(mergeBuildfiles=self.options.mergebuilds)
            if retcode is not 0:
                err('could not import one or more SIDL files')        
        
            # Update List of project classes and SIDL files in the build system
            self.project.getBuilder().changed([self] + list(self.dependents()))
            self.project.getBuilder().update()
                    
        if self.implImports:
            retcode = self._handleImplImports()
            if retcode is not 0:
                err('could not import one or more implementation files')
        return

    def graphvizString(self): 
        return 'shape=doubleoctagon color=firebrick1 fontname="Palatino-Italic"'

# -------------- Inherited "protected" methods

    def renameInternalSymbol(self, oldSymbol, newSymbol):
        '''Replaces any internal references to oldSymbol with newSymbol.'''
        
        project,graph = Globals().getProjectAndGraph(self.projectName)
        slist = graph.findSymbol(newSymbol)
        newvertex = slist[0] 
        
        if self._b_extends and oldSymbol in self._b_extends.keys():
            self._b_extends.clear()
            self._b_extends = newvertex
        elif self._b_implements and oldSymbol in self._b_implements.keys():
            self._b_implements[newSymbol] = newvertex._b_sidlFile
            del self._b_implements[oldSymbol]
        else:
            deps = self.getAttr('requires')
            print >> DEBUGSTREAM, 'data.requires = ', self.getAttr('requires')
            if (deps):
                if (oldSymbol in deps) :
                    deps.remove(oldSymbol)
                    deps.append(newSymbol)
                    self.setAttr('requires', deps)
        
        self._replaceSymbolInFiles(oldSymbol, newSymbol)

        return 0


    def removeInternalSymbol(self, symbol):
        ''' Removes any internal references to symbol.'''
        self.project,self.graph = Globals().getProjectAndGraph(self.projectName)
        
        if self._b_extends == symbol:
            self._b_extends = ''
        elif symbol in self._b_implements:
            del self._b_implements[symbol]
        else:
            return 0
        
        self._removeSymbolInFiles(symbol)

        self._mergeSIDLFileWithNewString()
        #self.genClassImpl() # superceded by mergeSIDLFileWithNewString method
        return 0
    
    def setASTNode(self, astNode):
        import parse.itools.elements as ast
        self.astNode = astNode
    
    #---------------------------------------------------------------------------------------
    # ------------------------- Private methods --------------------------------------------
    

    def _createOrChange(self):

        self.updateGraph()
        
        # Generate code
        self.handleNonInheritanceDependencies()   # in BVertex
        self.createSIDL()
        
        self.genClassImpl()

        self.project.getBuilder().changed([self])
        self.project.getBuilder().update(buildFilesOnly=True, quiet=True)
        
        self.spliceBoccaBlocks()
        self.handleImports()
        
        # Save the graph (including dot visualization)
        self.saveProjectState(self.graph, graphviz=True)
        
        return 0        
        
    
    def _defineImportArgs(self):
        self.parser.set_defaults(sidlimports=[], implimports=[], implexact=False, implexcludes=[], mergebuilds=True)
        self.parser.set_defaults(sidlimports=[], implimports=[]) ; # fixme why this line and the above both?
        self.parser.add_option('--import-sidl', dest='sidlimports', action='append', 
                               help='A SIDL file from which to import a specified '
                               + 'class or several classes, e.g., '
                               + '--import-sidl=pkg.MySolverClass,pkg.MyMatrixClass'
                               + '@/path/to/file.sidl. If no class is specified '
                               + '(only the SIDL filename is given), all methods '
                               + 'from interfaces and classes in the SIDL file '
                               + 'are imported into the specified project ' 
                               + self.kind + '.')
        self.parser.add_option('--no-merge-buildfiles', dest='mergebuilds', action='store_false',
                                help="If the SIDL being imported is from another bocca project, do "
                                + "not merge together build files.")
        self.parser.add_option('--import-impl', dest='implimports', action='append', 
                               help='A Babel-generated Impl file from which to '
                               + 'import method implementations from the '
                               + 'specified class or several classes (with '
                               + 'multiple --import-impl options), e.g., '
                               + '--import-impl="pkg.MyClass@/path/to/pkg_MyClass/". ')
        self.parser.add_option('--exclude-impl-symbols', dest='implexcludes', 
                               action="append", 
                               help='Exclude particular method implementations '
                               + 'from importation. If this option is not given, '
                               + 'a default set to exclude is read from '
                               + ' BOCCA/$PROJECT.defaults:exclude_from_import. '
                               + 'e.g., --exclude-impl-symbols="setServices '
                               + 'releaseServices". This option may be repeated.'
                               + ' To suppress the default and exclude no symbols, use '
                               + ' --exclude-impl-symbols=None')
        self.parser.add_option('--import-impl-exact', dest='implexact', 
                               action="store_true", 
                               help='All imported method implementations are '
                               + 'exactly preserved, ignoring anything newly '
                               + 'generated by bocca. Excluded symbols remain '
                               + 'excluded. If this option is not given, bocca-'
                               + 'generated implementations are appended and the '
                               + 'user may need to do manual clean up of the '
                               + 'resulting impl code.')

        pass
    
    def _processImportArgs(self):

        BVertex._processImportArgs(self)
            
        for sym in self.options.implimports:
            if sym.count('@') > 0: separatorSymbol = '@'
            else: separatorSymbol = ':'
            if sym.count(separatorSymbol) == 0:
                err('the --import-impl option requires a SIDL symbol and path to '
                    + 'its implementation, e.g., --import-impl="pkg.MyClass@'
                    + '/path/to/pkg_MyClass/"')
            symbol, implpath = sym.strip('"').split(separatorSymbol)
            if not os.path.exists(implpath) or not os.path.isdir(implpath):
                err('the path specified in the --import-impl option does not '
                    + 'exist or is not a directory: ' + implpath)
            
            self.implImports[symbol] = implpath

        pass
        
    def _handleImplImports(self):
        """ 
        This handles options (makes them unneeded for the most part) 
        differently if the input file is detected to be a bocca generated impl. 
        Specifically, methods listed in getReservedMethods are ignored in the 
        input file and blocks are replaced rather than merged since there's no 
        point in having both old bocca and new bocca code appended in one method 
        that contains bocca.protected. The reserved method exclusions are added 
        back in after all import options are processed.
        """
        from splicers.Operations import mergeFiles
        replaceIdentical = self.options.implexact
        for sym in self.implImports.keys():
            impldir = self.implImports[sym]
            # Assume that all impls (headers, modules, sources) are in the same directory (impldir)
            # The header and source filenames of the files to be imported
            saveimpldir = impldir
            if self._b_language in ['python', 'java']:                
                packages = sym.split('.')[:-1]
                for p in packages: impldir = os.path.join(impldir,p)
                 
            implHeader, implSource = self.getClassImplFilenames(sym,impldir=impldir)
            
            if not os.path.exists(implSource) and self._b_language in ['python', 'java']:
                # Perhaps the user gave a full path to the impls
                implHeader, implSource = self.getClassImplFilenames(sym,impldir=saveimpldir)
                impldir = saveimpldir

            # My header and source filenames
            self._b_implHeader, self._b_implSource = self.getClassImplFilenames(self.symbol)
            projDir = self.project.getDir()
            if self._b_implHeader: os.path.join(projDir,self._b_implHeader)
            if self._b_implSource: os.path.join(projDir,self._b_implSource)
            print >>DEBUGSTREAM,'--------------> importing from : ' \
                + str(implHeader), str(implSource)
            
            if not os.path.exists(implSource):
                err('could not find implementation source file to import: ' 
                    + implSource)
                
                # merge(append) source into target blocks of same name
                print " test drive merge unnested " 


            protKey=SourceWriter().protKey
            haveBoccaSource=isBoccaSource(implSource, protKey)
            # Get list of exclude symbols from defaults file
            excludeSyms = self.options.implexcludes
            if len(excludeSyms) == 0:
                if haveBoccaSource:
                    pass
                else:
                    excludestr = self.project.getDefaultValue('exclude_from_import', 
                                                              section='Project')
                    if excludestr: 
                        for e in excludestr.split(','): excludeSyms.append(e.strip())
            else:
                oldexcludeSyms = excludeSyms
                excludeSyms = []
                for i in oldexcludeSyms:
                    for j in i.split():
                        for k in j.split(','):
                            excludeSyms.append(k.strip())

            # Merge the implementation into this class's implementation.
            # As bocca.protected are no longer greedy about ctors,
            # importing bocca.protected is ok.
            srcKillBlockKeys=[]
            # srcKillBlockKeys.append(protKey)
            if haveBoccaSource:
                for i in getReservedMethods():
                    excludeSyms.append(i)
                replaceIdentical=True
            retcode = mergeFiles(srcName=implSource,
                                 targetName=self._b_implSource, 
                                 sourceKey='DO-NOT-DELETE splicer', 
                                 targetKey='DO-NOT-DELETE splicer',
                                 insertFirst=False, replaceIdentical=replaceIdentical,
                                 oldtype=sym, newtype=self.symbol, methodMatch=True,
                                 excludeSyms = excludeSyms, 
                                 srcKillBlockKeys=srcKillBlockKeys,
                                 dryrun=False, dbg=WARN, verbose=WARN, warn=WARN)
            if retcode is not 0:
                err('could not import implementation source: ' + implSource)
            
            # Splice the header, if any
            if not (implHeader is None or self._b_implHeader is None):
                if not os.path.exists(implHeader):
                    err('could not find implementation header or module file to import: ' + implHeader)
                            # Merge the implementation into this class's implementation
                retcode = mergeFiles(srcName=implHeader, 
                                     targetName=self._b_implHeader, 
                                     sourceKey='DO-NOT-DELETE splicer', 
                                     targetKey='DO-NOT-DELETE splicer', 
                                     insertFirst=False, replaceIdentical=replaceIdentical,
                                     oldtype=sym, newtype=self.symbol, methodMatch=True, 
                                     srcKillBlockKeys=srcKillBlockKeys,
                                     dryrun=False, dbg=WARN, verbose=WARN, warn=WARN)
                if retcode is not 0:
                    err('could not import implementation header or module: ' + implSource)  

            # Merge in makefiles if the import is from another bocca project
            if self.options.mergebuilds:
                externalProjectName, externalProjectDir = getProjectInfo(projectDir=impldir)

                if externalProjectName is not None and externalProjectDir is not None \
                        and externalProjectName != self.project.getName() and externalProjectDir != self.project.getDir():
                    localdir, buildfiles = self.project.getLocationManager().getUserBuildfilesLoc(self)
                    for buildfile in [os.path.join(localdir, f) for f in buildfiles]:
                        target = os.path.join(self.project.getDir(), buildfile)
                        source = os.path.join(externalProjectDir, buildfile)

                        print target+":"+source

                        if os.path.exists(source):
                            targetBackup = target+".bak"
                            if os.path.exists(targetBackup):
                                BFileManager().rm(targetBackup)
                            BFileManager().copyfile(target, targetBackup)
                            if not self.project.getBuilder().mergeBuildfiles(target, source, externalProjectName):
                                warn('Cannot merge incompatible buildfile '+source+' into '+target
                                     +' - merge manually if necessary')
                                BFileManager().rm(target)
                                BFileManager().copyfile(targetBackup, target)
                                BFileManager().rm(targetBackup)

                 
        return 0

    def _replaceSymbolInFiles(self, oldSymbol, newSymbol):
        
# Rename symbol in sidl file
# TODO: regenerate the SIDL
# FIXME : Is a simple sed approach enough?. or do we want to re-generate?
        if not self.project:
            self.project, graph = Globals().getProjectAndGraph(self.projectName)
        fd = fileManager.open(os.path.join(self.project.getDir(), self._b_sidlFile), "r")
        newBuf = fd.read()
        fd.close()
        newBuf = newBuf.replace(oldSymbol, newSymbol)
        fd = fileManager.open(os.path.join(self.project.getDir(), self._b_sidlFile), "w")
        fd.write(newBuf)
        fd.close()
        
# TODO: update the impls
# FIXME: Is a simple sed approach enough?. or do we want to re-generate?
        replaceList = [(oldSymbol, newSymbol)]
        replaceList.append((oldSymbol.replace('.', '_'), newSymbol.replace('.', '_')))
        replaceList.append((oldSymbol.replace('.', '::'), newSymbol.replace('.', '::')))

        fileList = [self._b_implSource]
        if (not self._b_language in ['f77' ,'python', 'f77_31'] ):
            fileList.append(self._b_implHeader)
        for f in fileList:
            print >> DEBUGSTREAM, 'Replacing %s with %s in %s' %(oldSymbol, newSymbol, f)
            fd = fileManager.open(os.path.join(self.project.getDir(), f), "r")
            oldBuf = fd.read()
            fd.close()
            for (old, new) in replaceList:
                oldBuf = oldBuf.replace(old, new)
            fd = fileManager.open(os.path.join(self.project.getDir(), f), "w")
            fd.write(oldBuf)
            fd.close()
        return 0
    
    def _internalRename(self):
        from copy import deepcopy
        oldSidlFile = self._b_sidlFile
        oldSymbol= self.symbol
        oldPackageName = self._b_packageName
        oldClassName = self._b_className
        oldImplSource = self._b_implSource
        oldImplHeader = self._b_implHeader
        oldCompDir = self.project.getLocationManager().getImplLoc(self)[0]
        oldself = self.clone()
        
        print >> DEBUGSTREAM, 'sidlclass::_internalRename() oldSidlFile = ', oldSidlFile, \
            '\nsidlclass::_internalRename() oldSymbol = ', oldSymbol, \
            '\nsidlclass::_internalRename() oldPackageName = ', oldPackageName, \
            '\nsidlclass::_internalRename() oldClassName = ', oldClassName, \
            '\nsidlclass::_internalRename() oldImplSource = ', oldImplSource, \
            '\nsidlclass::_internalRename() oldImplHeader = ', oldImplHeader
        
        self._b_packageName = self.newSymbol[0:self.newSymbol.rfind('.')]
        self._b_className = self.newSymbol.split('.')[-1]
        self._b_sidlFile = os.path.join("components", "sidl", self.newSymbol+'.sidl')
        
        print >> DEBUGSTREAM, "", \
            '\nsidlclass::_internalRename() self._b_packageName = ', self._b_packageName, \
            '\nsidlclass::_internalRename() self._b_className = ', self._b_className, \
            '\nsidlclass::_internalRename() self._b_sidlFile = ', self._b_sidlFile, \
            '\nsidlclass::_internalRename() self._b_implSource = ', self._b_implSource, \
            '\nsidlclass::_internalRename() self._b_implHeader = ', self._b_implHeader, \
            '\nsidlclass::_internalRename() self.newSymbol = ', self.newSymbol, \
            '\nsidlclass::_internalRename() self.project.getDir() = ', self.project.getDir()

        
        # Update the symbol in the vertex (updating all edges)    
        self.changeSymbol(self.newSymbol)
        self._b_implHeader, self._b_implSource = self.getClassImplFilenames(self.newSymbol)
        self.createSIDL()        # Generate empty new class sidl file
        
        # Splice method declarations (if any) from old sidl file to new one
        fd = fileManager.open(os.path.join(self.project.getDir(), self._b_sidlFile), "r")
        newBuf = fd.read()
        
        fd = fileManager.open(os.path.join(self.project.getDir(), oldSidlFile), "r")
        oldBuf = fd.read()
        
        # Temporary cludge until Ben's splicer is more user friendly
        newString = 'bocca.splicer.begin(%s.methods)' % (self.newSymbol)
        oldString = 'bocca.splicer.begin(%s.methods)' % (oldSymbol)
        oldBuf = oldBuf.replace(oldString, newString)
        newString = 'bocca.splicer.end(%s.methods)' % (self.newSymbol)
        oldString = 'bocca.splicer.end(%s.methods)' % (oldSymbol)
        oldBuf = oldBuf.replace(oldString, newString)
# FIXME: Do we replace symbols in user code?        
        oldBuf = oldBuf.replace(oldSymbol, self.newSymbol)
        newBuf = mySplicer(oldBuf, newBuf, 'bocca.splicer.begin(', 
                           'bocca.splicer.end(', mode='REPLACE')
        fd = fileManager.open(os.path.join(self.project.getDir(), self._b_sidlFile), "w")
        fd.write(newBuf)
        fd.close()
        
        # Generate new impls
        self.genClassImpl()
        
        # Splice old impls into new impls
        # Splice method implementation (if any) from old sidl file to new one
        fd = fileManager.open(os.path.join(self.project.getDir(), 
                                           self._b_implSource), "r")
        newBuf = fd.read()
        print>> DEBUGSTREAM, self.project.getDir(), oldImplSource
        fd = fileManager.open(os.path.join(self.project.getDir(), 
                                           oldImplSource), "r")
        oldBuf = fd.read()
        
        replaceList = [(oldSymbol, self.newSymbol)]
        replaceList.append((oldSymbol.replace('.', '_'), 
                            self.newSymbol.replace('.', '_')))
        replaceList.append((oldSymbol.replace('.', '::'), 
                            self.newSymbol.replace('.', '::')))

        for (old, new) in replaceList:
            oldBuf = oldBuf.replace(old, new)
        
        # Temporary cludge until Ben's splicer is more user friendly
        newBuf = mySplicer(oldBuf, newBuf, 'splicer.begin(', 
                           'splicer.end(', mode='REPLACE')
        fd = fileManager.open(os.path.join(self.project.getDir(), 
                                           self._b_implSource), "w")
        fd.write(newBuf)
        fd.close()
        
        if (not self._b_language.upper() in ['F77', 'PYTHON', 'JAVA']):
# Splice code into impl header file
            fd = fileManager.open(os.path.join(self.project.getDir(), 
                                               self._b_implHeader), "r")
            newBuf = fd.read()
            
            fd = fileManager.open(os.path.join(self.project.getDir(), 
                                               oldImplHeader), "r")
            oldBuf = fd.read()
            
            for (old, new) in replaceList:
                oldBuf = oldBuf.replace(old, new)
        
# Temporary cludge until Ben's splicer is more user friendly
            newBuf = mySplicer(oldBuf, newBuf, 'splicer.begin(', 
                               'splicer.end(', mode='REPLACE')
            print >> DEBUGSTREAM, newBuf
            fd = fileManager.open(os.path.join(self.project.getDir(), self._b_implHeader), "w")
            fd.write(newBuf)
        
# Update my dependents' internal symbols
        for node in self.dependents():
            node.renameInternalSymbol(oldSymbol, self.newSymbol)


        # Remove old sidl file
        try:
            fileManager.rm(oldSidlFile)
        except:
            warn('Could not remove ' + oldSidlFile)
            
        self.project.getBuilder().remove([oldself])
                
        self.project.getBuilder().changed([self] + list(self.dependents()))
        self.project.getBuilder().update(quiet=True)
        return

    def _removeSymbolInFiles(self, symbol):
# TODO: update the impls
# FIXME: Is a simple sed approach enough?. or do we want to re-generate?
        removeList = [symbol]
        removeList.extend([symbol.replace('.', '_'), symbol.replace('.','::')])

        fileList = [self._b_implSource]
        if self._b_language.upper() not in ['F77', 'python', 'java']:
            fileList.append(self._b_implHeader)
            
        # First, regenerate all generated code with the symbol removed
        
        # TODO: how should removal in user code be really handled???
        # below is the rename logic
        #for f in fileList:
        #    print >> DEBUGSTREAM, 'Removing %s in %s' %(symbol, f)
        #    fd = fileManager.open(os.path.join(self.project.getDir(), f), "r")
        #    oldBuf = fd.read()
        #    fd.close()
        #    for (old, new) in replaceList:
        #        oldBuf = oldBuf.replace(old, new)
        #    fd = fileManager.open(os.path.join(self.project.getDir(), f), "w")
        #    fd.write(oldBuf)
        #    fd.close()
        return 0
    
    def _getMyUserFiles(self, project=None, fullpath=True):
        # Get a list of user files (usually for revision control interactions)
        if not project:
            if not self.project: 
                project, graph = Globals().getProjectAndGraph(projectName=self.projectName)
            else: 
                project = self.project
        files = []
        sidldir, sidlfiles = project.getLocationManager().getSIDLLoc(self)
        impldir, implfiles = project.getLocationManager().getImplLoc(self)
        makedir, makefiles = project.getLocationManager().getUserBuildfilesLoc(self)
        if fullpath:
            for f in sidlfiles: files.append(os.path.join(project.getDir(),sidldir,f))
            for f in implfiles: 
                if f and f != 'None': files.append(os.path.join(project.getDir(),impldir,f))
            for f in makefiles: files.append(os.path.join(project.getDir(),makedir,f))
        else:
            for f in sidlfiles: files.append(os.path.join(sidldir,f))
            for f in implfiles: 
                if f and f != 'None': files.append(os.path.join(impldir,f))
            for f in makefiles: files.append(os.path.join(makedir,f))
        return files
    
    def _mergeSIDLFileWithNewString(self, replaceIdentical=False, targetFile=None):
        # Merge the original file with the newly generated SIDL (string) incorporating changes to parent interfaces   
        warn = False
        if 'BOCCA_DEBUG' in os.environ.keys():
            if os.environ['BOCCA_DEBUG'] == "1":
                warn = True    
                
        project,pgraph = Globals().getProjectAndGraph(self.projectName)    
        if not targetFile: targetFile = os.path.join(project.getDir(),self._b_sidlFile)
                
        sidlFile = os.path.join(project.getDir(),self._b_sidlFile)    
        result = Operations.mergeFileIntoString(targetName=targetFile, 
                                 targetString=self.genClassSidlString(),
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

        
if __name__ == "__main__":
    Sidlclass().usage()
