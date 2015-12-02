
import os, sys
import cct._err, cct._debug, cct._validate
from cct._util import *
from cct._file import *

from graph.boccagraph import *
from cct.interface import *


class Enum(Interface):
    def __init__(self, action = '__init__', args = None, project = None, modulePath = None,
                 symbol=None, version='0.0', graph=None):
        '''bocca <verb> enum [options] SIDL_SYMBOL
        
        <verb> is one of create, change, remove, rename, display. For documentation on
        specific verbs, use 'bocca help <verb> enum'
        '''

        self.genDummy = True
        Interface.__init__(self,action,args,project,modulePath,symbol,version,graph,kind='enum')

        # Use self.setAttr(key,value) to set various port-specific attributes. 
        # Alternatively, use field names that start with _b_, e.g., self._b_includePath
        # This will ensure that these fields are saved when the project state is saved.
        return 
        
    def defineArgs(self,action):
        if action == 'create':
            self._defineImportArgs()        # in BVertex
        elif action in ['change', 'display', 'edit', 'rename', 'remove', 'whereis', 'copy']:
            Interface.defineArgs(self, action)
        else:
            err(self.kind + ' verb "' + action + '" NOT implemented yet.', 3)
        return
    
    def processArgs(self, action):
        """ Validates and if necessary canonicalizes the command line arguments for
        this subject, which are parsed into self.options.
        Exits nonzero if user gives bad input.
        """
        if action == 'create':
            if len(self.args) < 1:
                self.usage(exitcode=4,errmsg='[create ' + self.kind 
                           + '] A SIDL ' + self.kind 
                           + ' name (e.g. packageName.enumSidlSymbol) is required for '
                           + self.kind + ' creation.')

                self.symbol = self.args[0]
            if self.options.sidlimports:
                self._processImportArgs()
                self.genDummy = False
        elif action in ['change', 'display', 'edit', 'rename', 'remove', 'whereis', 'copy']:
            Interface.processArgs(self, action)        
        return 
    
    def graphvizString(self): return 'shape=trapezium color=yellow fontname="Palatino-Italic"'

    def create(self):
        """ create enum SIDL_SYMBOL 
        
        Creates an enum with the name SIDL_SYMBOL. If SIDL_SYMBOL is not fully 
        qualified, e.g., MyEnum instead of somepackage.MyEnum, the enum will be added 
        to the default package for the project, usually the same as the project name.        
        """
        return Interface.create(self) 

    def copy(self):
        pgraph = Globals().getGraph(self.projectName)
        copyVertex = Enum('create', [self.newsymbol], project=self.project, modulePath=self.modulePath,
                          symbol=self.newsymbol, version=self.version, graph=pgraph)
        Interface.initCopy(copyVertex, self)

        copyVertex.oldsymbol = self.symbol
        copyVertex.sidlImports = { self._b_sidlFile : ['%all'] }
        
        return copyVertex.create()
    
    def change(self):
        """change port [options] SIDL_SYMBOL

        """
        return Interface.change(self)

    def display(self):
        """display port SIDL_SYMBOL
        
        """
        return Interface.display(self)

    def whereis(self):
        '''whereis port SIDL_SYMBOL options
        '''     
        return Interface.whereis(self)

    def edit(self):
        '''edit port SIDL_SYMBOL options
        '''     
        return Interface.edit(self)
   
    def remove(self):
        """remove port [options] SIDL_SYMBOL

        Remove the specified port from the project.
        """
        return Interface.remove(self)
    
    def rename(self):
        """rename port [options] SIDL_SYMBOL NEWSIDL_SYMBOL
        
        Rename the port specified with the SIDL symbol SIDL_SYMBOL to NEWSIDL_SYMBOL.
        The SIDL file containing the port definition is also renamed.
        """
        return Interface.rename(self)

        
# -------------- Inherited "protected" methods

    def createSIDLString(self, sidlFileName, project, pgraph, extraSplicerComment=False):
        '''Create a list of lines that will go in the SIDL file.'''
        symbols = self.symbol.split('.')
        nsyms = len(symbols)
        shortEnumName = symbols[-1]

        pkg = pgraph.findSymbol(symbol=symbols[0],kind='package')
        if len(pkg) != 1:
            errmsg = 'missing or ambiguous package name encountered: ' + symbols[0] 
            if len(pkg) > 1: errmsg += '(possibilties are ' + str(pkg) + ')'
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
        buf += self.getCommentSplicerString(indentstr=indent*tab, extraSplicerComment=extraSplicerComment)
        buf += indent*tab + 'enum ' + shortEnumName + '\n'     
            
        indent = save_indent

        buf += indent*tab + '{\n'
        indent += 1
        indentstr = indent*tab 
        self.setAttr('methodsIndent', indent)

        if self.genDummy:
            icomment='Insert your ' + self.kind + ' entries here'
        else:
            icomment=""

        buf += self.getSIDLSplicerBeginString(indentstr, tag = self.symbol + '.entries', 
                                              extraSplicerComment=extraSplicerComment, 
                                              insertComment=icomment) 
        if self.genDummy:
            buf += indent*tab + 'dummy, ' + '\n'     
                       
        buf += self.getSIDLSplicerEndString(indentstr, tag = self.symbol + '.entries') 
            
        indent -= 1
        buf += indent * tab + '}\n'
        
        for i in range(1,nsyms-1):
            indent -= 1
            buf += indent*tab + '}\n'
        indent = 0
        buf += '}\n'
        
        print >>DEBUGSTREAM, buf
               
        return buf
    
    def renameInternalSymbol(self, oldsymbol, newsymbol):
        '''Replaces any internal references to oldsymbol with newsymbol.'''
        return Interface.renameInternalSymbol(self,oldsymbol,newsymbol)
    
    def removeInternalSymbol(self,symbol):
        '''Removes all references to symbol.'''
        return Interface.removeInternalSymbol(self,symbol)
