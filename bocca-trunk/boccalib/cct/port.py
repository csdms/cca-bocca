
import os, sys
import cct._err, cct._debug, cct._validate
from cct._util import *
from cct._file import *

from graph.boccagraph import *
from cct.interface import *


class Port(Interface):
    def __init__(self, action = '__init__', args = None, project = None, modulePath = None,
                 symbol=None, version='0.0', graph=None):
        '''bocca <verb> port [options] SIDL_SYMBOL
        
        <verb> is one of create, change, remove, rename, display. For documentation on
        specific verbs, use 'bocca help <verb> port'
        '''

        Interface.__init__(self,action,args,project,modulePath,symbol,version,graph,kind='port')

        # Use self.setAttr(key,value) to set various port-specific attributes. 
        # Alternatively, use field names that start with _b_, e.g., self._b_includePath
        # This will ensure that these fields are saved when the project state is saved.
        return 
        
    def defineArgs(self,action):
        if action in ['change', 'create', 'display', 'edit', 'rename', 'remove', 'whereis', 'copy']:
            Interface.defineArgs(self,action)
        else:
            err('Port verb "' + action + '" NOT implemented yet.', 3)

        return

    def processArgs(self, action):
        """ Validates and if necessary canonicalizes the command line arguments for
        this subject, which are parsed into self.options.
        Exits nonzero if user gives bad input.
        """
        if action == 'create':
            # Use the interface arguments, and append gov.cca.Port to self.options.extends
            # Add --extends option for gov.cca.Port
            self.options.sidlsymbol_and_location.append('gov.cca.Port')
            Interface.processArgs(self, action) 
            # TODO: process port-specific (not interface) options here
            
        elif action in ['change', 'display', 'edit', 'rename', 'remove', 'whereis', 'copy']:
            Interface.processArgs(self, action)        
        return 
    
    def graphvizString(self): return 'shape=hexagon color=yellow fontname="Palatino-Italic"'

    def create(self):
        """ create port SIDL_SYMBOL {--extends/-e SIDL_SYMBOL} 
        
        Creates an interface with the name INTERFACE, optionally extending SIDL_SYMBOL.
        PORTINTERFACE and SIDL_SYMBOL are both SIDL types. If PORTINTERFACE is not fully 
        qualified, e.g., MyPort instead of somepackage.MyPort, the port will be added 
        to the default package for the project, usually the same as the project name.        
        """
        return Interface.create(self) 

    def copy(self):
        """copy port [options] FROM_SIDL_SYMBOL TO_SIDL_SYMBOL
        """
        
        # Needs its own copy function since the correct class has to be created
        pgraph = Globals().getGraph()
        copyVertex = Port('create', [self.newsymbol], project=self.project, modulePath=self.modulePath,
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
    def renameInternalSymbol(self, oldsymbol, newsymbol):
        '''Replaces any internal references to oldsymbol with newsymbol.'''
        return Interface.renameInternalSymbol(self,oldsymbol,newsymbol)
    
    def removeInternalSymbol(self,symbol):
        '''Removes all references to symbol.'''
        return Interface.removeInternalSymbol(self,symbol)
