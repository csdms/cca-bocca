""" Example is the vertex type implemented in this script. 
It implements the interface in BVertex, which consists of a 
number of actions (create, remove, etc.) and internal functions 
needed for processing command line arguments.

The naming conventions for the Python module (this file) and 
the class it contains are as follows:
     - Use all lowercase letters for the file (module) name
     - Use the same name for the class, but capitalized, e.g., 
     file package.py contains class Package

This script must not be called directly from a command line;
it must be dispatched through bocca and registered in the
menu in boccalib/cct/__init__.py. The name of this script (less .py) 
should be the name registered in the aforementioned cct menu.
"""

import os, sys

from cct._validate import *
from cct._util import *
from cct._file import *
from cct._debug import *

from cct._err import *
from graph.boccagraph import *

from cct._examples import *

class Example(BVertex):
    def __init__(self, action='__init__', args = None, project = None, modulePath = None,
                 symbol=None, version='0.0', graph=None):
        """
        action example [arguments]
        
        Perform the specified action on the example. Sample actions include
        create, remove, rename, display. For a complete list of actions, see
        bocca help.
      
        The example subject is a prototype stub for bocca extensions. To get examples
        of bocca commands, try one of:
		"bocca help --examples action"
		"bocca help --examples subject"
	or to dump all the examples;
		"bocca help --examples"
        """
        # It is best to leave the __init__ method very minimal to avoid 
        # interfering with its loading of the project state, e.g.:
        BVertex.__init__(self,action,args,project,modulePath,'example',symbol,version,graph)
        
        # After the BVertex constructor (above) returns, we should have valid:
        # self.symbol : the name of the current object, for SIDL types, the fully qualified SIDL type
        # self.kind : the current vertex kind, this is usually the same as the module name, e.g., port
        # self.version : the version number, default is usually '0.0'
        # self.modulePath : path to installed boccalib modules
        # self.parser : an instance of OptionsParser
        # self.options : the command line options for this instance (already parsed)
        # self.args : list of arguments remaining after the command-line options have been parsed
        # self.projectName : the name of this project
        # self.data : a dictionary of attributes, access it with self.getAttr, self.setAttr methods only!
        #             self.data is the best place to stash any info about the current vertex, as it will
        #             be pickled/unpickled automatically. Make sure you don't put references to other 
        #             graph elements here (to avoid recursion)
        
        # Optionally set some attributes specific to this vertex type. Any type
        # value can be used, not just strings.
        self.setAttr('somekey','someval')
        
        # Alternatively, use field names that start with _b_, e.g., self._b_includePath
        # This will ensure that these fields are saved when the project state is saved.
        # PLEASE do not add things that are already available in BVertex or can be easily 
        # obtained with one of the methods in _util.py.
        self._b_somefield = 'somevalue'
        return 
        
    #-------------------------------------------------------
    # This is where we define subject options for example   
    # Thie method is automatically invoked from the superclass constructor.  
    # It is assumed that self.project is available to use inside this method.  
    def defineArgs(self, action):
        """Defines command line options and defaults for this command. This is 
        invoked in the constructor of the parent class Subcommand.
        The string action argument is one of create, change, display, remove, rename.
        """

        # We can also retrieve values from bocca.config, e.g., self.project.defaults.get('Babel','default_language')
        if action == 'create':
            self.parser.set_defaults(abool=True, astring='.', avar='_unset')
        
            self.parser.add_option('-n', '--nocrap', action='store_false', dest='abool', help=' turn of something on by default')
        elif action == 'change':
            elf.parser.add_option('-a', '--string', dest='astring', help='a string value')

            self.parser.add_option('-v', '--var', dest='avar', help='string we compute later if not given')
        #elif action == 'display':
        #elif action == 'rename':
        #elif action == 'remove':
        # etc...
        
        return
    
    #-------------------------------------------------------
    # This is where we process subject options for example       
    # Thie method is automatically invoked from the superclass constructor.  
    # It is assumed that self.project, self.options, and self.args are available 
    # to use inside this method. The self.symbol field is not yet available 
    # and must be set in this method.
    def processArgs(self, action):
        """ Validates and if necessary canonicalizes the command line arguments for
        this subject, which are parsed into self.options.
        Exits nonzero if user gives bad input.
        """
 
        # The most relevant variables here are:
        #
        # self.parser : an instance of OptionsParser
        # self.options : the command line options for this instance (already parsed)
        # self.args : list of arguments remaining after the command-line options have been parsed
        
        # The only requirement for the implementation is that self.symbol is set to
        # the SIDL symbol or appropriate name of this vertex. While frequently
        # the name of the object (port, component, project, etc.) is the very last
        # argument (as in the example here), this is not a requirement -- as long 
        # as it is possible to obtain it somehow, it must be set in this method.
        if len(self.args) > 0:
            self.symbol = self.args[-1]
        else:
            # This should almost never be the case, usually the command line includes the name
            # of the project entity on which to operate
            self.symbol = 'example'  
            
        if len(self.args) < 1:
            self.usage(exitcode=2, errmsg='[create example] An arg is required for example\nbocca help action example')

        # Argument processing can be action-specific if different actions have different 
        # command-line arguments.
        if action == 'create' or action == 'change':
            if self.options.avar == '_unset':
                self.options.avar = 'foo'
        elif action == 'change':
            if self.options.anothervar == '_unset':
                self.options.anothervar = 'bar'
        # etc. for the other actions
        
        return

#----------------------------------------------------------
#-- Various methods from the BVertex interface which are used
#-- for different types of serialization. Only the 
#-- serialize and deserialize methods are required, the rest
#-- can be implemented only if one desires to override the 
#-- default implementations in BVertex.

    #-----------------------------------------------------------
    # Pickle methods must be overridden any time there are new 
    # fields added to a subclass that are not in BVertex
    def _savePickle(self,filedesc,protocol=2):
        """Given a filed escriptor of an open pickle file, 
        save everything necessary to recreate this vertex (except fields that 
        can result in recursion. Always call the superclass method first."""
        BVertex.savePickle(self,filedesc,protocol)
        # Now pickle any fields that are in this class but not the superclass, e.g.,
        # pickle.dump(self.myfield, filedesc, protocol)
        return

    def _loadPickle(self,filedesc):
        """Given a file descriptor of an open pickle file, recover 
        all fields of this vertex except for the edge list or any other
        potentially recursive references. Always call the superclass method first."""
        BVertex.loadPickle(self,filedesc)
        # Unpickle any fields that are in this class but not in the superclass (in 
        # the same order in which they were pickled in savePickle, e.g.,
        # self.myfield = pickle.load(filedesc)
        return

#-----------------------------------------------------------
#-- The following two methods deal with ASCII serialization (separate from pickle)
    def serialize(self):
        """Writes a complete ASCII representation of current object which 
        can be used to reconstruct the object by calling deserialize.
        Note that pickle is used during development for maintaining the 
        state of a project; this serialization will be used only rarely, i.e.,
        when migrating a project to a new environment or when merging projects. 
        Every subclass must implement this method."""
        if self.__class__ is BVertex:
            raise NotImplementedError
        return

    def deserialize(self, sstr):
        """Returns an instance of a specific vertex type configured with
        the information resulting from deserializing the sstr string. 
        Every subclass must implement this method."""
        if self.__class__ is BVertex: raise NotImplementedError
        return

    
#-------------------------------------------------------
#-- The remaining methods all implement the various actions
#-- that can be performed on this object as defined in the BVertex
#-- superclass. These correspond to the action in 'bocca action example [args]' 
#-- and are automatically invoked by the cct.dispatcher dispatch method.
    def create(self):
        """ create example [options] arg1 [args] 
        """
        result = 0

        # See comment in __init__ method for available variables
        
        # This is how the graph can be obtained. The graph is loaded from the pickle
        # file by the dispatcher, so the getGraph() operation is very lightweight.
        project, graph = Globals().getProjectAndGraph(self.projectName)
        
        # If needed the project name and top-level directory can be otained with
        projectName = project.getName()
        projectDir = project.getDir()
        
        
        if projectName is None: 
            # Note that the err method calls sys.exit(errcode) after cleaning up any 
            # files that were open with BFileManager().open() 
            err('[create example] No project found in this directory.',errcode=2)

        print >> DEBUGSTREAM, 'example called with options ', str(self.options) , ' leaving args ' , str(self.args)
        
        # ========================= Creating subdirectories ============================= 
        # If at any point you wish to create a project subdirectory, always use addSubdir 
        # with a path relative to the top-level project directory.
        # retcode = addSubdir(name,'dir/subdir')
        # 
        # ============================== Opening files ================================== 
        # To open files, always use
        # fd = BFileManager.open(filename,mode)
        # instead of the standard fd = open(filename, mode)
        
        
        # TODO:
        #
        # everything. first check for all but init is always to validate
        # the project being acted on.

         
        # Make sure to save the project graph if it was modified.
        graph.save()
 
        return result

        
    def change(self):
        """change example [options] arg

        """
        # See comment in __init__ method for available variables
        # Implementation of change functionality here
        result = 0
        return result
   
    def remove(self):
        """remove example [options] arg

        """       
        # See comment in __init__ method for available variables
        # Implementation of remove functionality here
        result = 0
        return result
    
    def rename(self):
        """rename example [options] arg1 arg2

        """
        # See comment in __init__ method for available variables
        # Implementation of rename functionality here
        result = 0
        return result
 
    def display(self):
        """display example arg

        """
        # Implementation of display functionality if something different than the 
        # default is desired, otherwise leave as is.
        return BVertex.display(self)
 
 #--------------------------------------------------------------------
 #--- The following BVertex methods should rarely need to be overriden.
 #--- The default implementations are usually sufficient.
 
    # Produce a custom string for the attributes (the things in square brackets [] after
    # the vertex name) of this vertex in Graphviz dot file.
    # This is a name=value comma-separated list, see the Graphviz documentation for details.
    def graphvizString(self): return 'shape=box, color=pink\n'

    # Generate a string representation of this type object (if different from the default BVertex one)
    def __str__(self):
        """ Default conversion to a string."""
        (kind, symbol, version) = self.name.split('@')
        return '%s: %s %s' % (kind, symbol, self.data) 

    # Generate a shorter string (if different from impl in BVertex)
    def shortstr(self):
        """Generate a brief string suitable for output in graphical, i.e., dot output"""
        (kind,symbol,version) = self.name.split('@')
        return '%s %s' % (kind,symbol)

# This module should not be invoked directly
if __name__ == '__main__':
    # Note that it's sufficient to use the superclass usage() implementation, there
    # shouldn't be a need to customize this for subjects as it extracts all the 
    # information it needs from the self.parser OptionsParser instance.
    example(args=sys.argv, project=getProject()).usage()
