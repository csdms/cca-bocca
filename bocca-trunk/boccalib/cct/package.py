'''Package BVertex subclass for representing SIDL packages.'''
import os, sys, cct._err, cct._debug
from cct._util import *
from graph.boccagraph import BVertex, BEdge

class Package(BVertex):
    def __init__(self, action = '__init__', args = None, project = None, modulePath = None,
                 symbol=None, version='0.0', graph=None):
        '''bocca <verb> package [options] SIDLNAME
        
        <verb> is one of create, change, remove, rename, display. For documentation on
        specific verbs, use 'bocca help <verb> package'
        '''
        BVertex.__init__(self,action,args,project,modulePath,'package',symbol,version,graph)
        return
    
    def __str__(self):
        (kind,symbol,version) = self.name.split('@')
        return '%s: %s %s' % (kind, symbol, version)  

    def graphvizString(self): return 'shape=invhouse, color=cornflowerblue'

    def serialize(self, filedesc):
        '''Writes a complete ASCII representation of current object which 
        can be used to reconstruct the object by calling deserialize.'''
        #TODO
        return

    def deserialize(self, sstr):
        '''Returns an instance of a Package configured with
        the information resulting from deserializing the sstr string.'''
        #TODO
        return

    def defineArgs(self,action):
        if action == 'create' or action == 'change':
            self._defineImportArgs()
            self._defineCommonCreateAndChangeArgs()
        elif action == 'display':
            pass
        elif action == 'change':
            self._defineCommonCreateAndChangeArgs()
        else:
            err('Package verb "' + action + '" NOT implemented yet.', 3)
        return

    def processArgs(self,action):
        if action == 'create' or action == 'change':
            if len(self.args) < 1:
                self.usage(exitcode=4,errmsg='[' + self.action + ' package]: A package name is required, see "bocca help ' + action + ' package"')
            self.symbol = self.args[-1]
            if self.options.sidlimports:
                self._processImportArgs()
            
            self._processCommonCreateAndChangeArgs(action)
        elif action == 'display':
            self.symbol = self.args[-1]
        else:
            err('Package verb "' + action + '" NOT implemented yet.', 3)

        return
    
    def create(self):
        """ create package SIDL_SYMBOL [options]
        """
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        self.validateNewSymbol(pgraph)  # From BVertex
 
        if self.options.version:
            self.changeSymbol(newVersion=self.options.version, inGraph=False)

        print >>DEBUGSTREAM,'create ' + self.kind + ', name = ', self.symbol, ', version = ', self.version

        if self.options.version:
            pkg = project.addNestedPackages(symbol=self.symbol,version=self.version,g=pgraph)
            
        if pkg.symbol != self.symbol:
            edge = BEdge(pkg, self, pgraph)  # Connect with parent package, this adds self to graph
        
        if self.sidlImports: self.handleSIDLImports(mergeBuildfiles=self.options.mergebuilds)

        self.saveProjectState(pgraph, graphviz=True)
            
        print >>DEBUGSTREAM, 'create ' + self.kind + ' ' + self.name + ' returning with code 0'
        return 0

    def change(self):
        '''change package SIDL_SYMBOL [options]
        '''
        # Check whether component already exists in project
        project,pgraph = Globals().getProjectAndGraph(self.projectName)
        self.validateExistingSymbol(pgraph)
            
        if self.sidlImports: self.handleSIDLImports(self.options.mergebuilds)
        
        if self.options.version:
            self.changeSymbol(newVersion=self.options.version)
        
        self.project.getBuilder().changed([self] + list(self.dependents()))
        self.project.getBuilder().update(genSIDL=True)

        self.saveProjectState(pgraph, graphviz=True)
            
        print >>DEBUGSTREAM, 'change ' + self.kind + ' ' + self.name + ' returning with code 0'

        return 0
        
    def display(self):
        ''' display package SIDL_SYMBOL
        '''
        return BVertex.display(self)

#--------------------------------------------------------------------------------------------------
# ----------------------------- PRIVATE methods ---------------------------------------------------

    def _defineImportArgs(self):
        self.parser.set_defaults(sidlimports=[], mergebuilds=True)
        self.parser.add_option('--import-sidl', dest='sidlimports', action='append', 
                               help='A SIDL file from which to import a specified interface or several interfaces, ' 
                               + 'e.g., --import-sidl="pkg.MySolverInterface,pkg.MyMatrixInterface@/path/to/file.sidl". ' 
                               + 'If no interface is specified (only the SIDL filename is given), all packages from '
                               + 'the SIDL file are imported into the specified project ' + self.kind + '.')
        self.parser.add_option('--no-merge-buildfiles', dest='mergebuilds', action='store_false',
                                help="If the SIDL being imported is from another bocca project, do "
                                + "not merge together build files.")
        pass
    
    
    def _defineCommonCreateAndChangeArgs(self):
        self.parser.set_defaults(version='0.0')
        self.parser.add_option('-v','--version', dest='version', action='store', 
                               help='Specify the version of the package; the default is 0.0')
        pass
    
    
    def _processCommonCreateAndChangeArgs(self, action):
        if self.options.version:
            # Validate the version number
            from cct._validate import validateVersionNumber
            if not validateVersionNumber(self.options.version):
                err('Invalid version format. Valid formats are #.# or #.#.#, where # represents a number')
        pass
