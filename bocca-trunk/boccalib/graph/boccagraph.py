#!/usr/bin/env python

# Bocca project internal representation graph datastructure
# Copyright (c) 2007, UChicago, LLC
# Operator of Argonne National Laboratory
#
# Creator: Boyana Norris
# Contributors:
#   Benjamin Allan, Sandia National Lab

"""A graph representation of SIDL-based CCA projects.

Each CCA project can be represented by using a graph data structure.
Nodes represent code entities (projects, libraries, interfaces, 
classes, ports, components), and edges represent dependencies
between them. Dependence is defined as follows: node B 
depends on node A if a modification of node A requires an 
action on node B. In the graph representation, a directed
edge A -> B means that B depends on A. The action on B after
modification of A is stored as an edge attribute on the edge A -> B.
Actions are generally code transformations, such as generating code 
from SIDL files or compiling sources into a library. Some edges resulting
from non-transformation dependencies e.g., including a header 
(represented by vertex A) without having to link to a corresponding 
library, do not have specific actions associated with them, but 
a change in the header will result in triggering all actions 
(if any) in the subgraph rooted at the header vertex A.

"""

import os, re, sys, imp, stat, random, graphlib.delegate
#import pickle
import cct._validate
import cPickle as pickle
from parse.boccaParse import OptionParser
from graphlib.graph import *
from cct._err import * 
from cct._debug import *
from cct._file import md5file
from cct._util import *
from cct._nametab import Nametab
from cct._portInstance import PortInstance
from boccaversion import bocca_version
from splicers._compat import * ; # for reversed(l) portability

class BVertex(Vertex):
    def __init__(self,  action='__init__', args = None, project = None, modulePath = None,
                 kind=None, symbol=None, version='0.0.0', graph = None):
        ''' bocca help <verb> <subject>   lists the help on a topic 
        bocca help                    lists the available verbs and subjects
        bocca display ports           lists the known port types.
        bocca display components      lists the known component types.
        '''

        '''Create a BVertex given its kind (package, class, interface, port, component, etc.), 
        SIDL symbol (if the vertex corresponds to a SIDL type, otherwise this is some sort of 
        identifying name), a string representing the version number, and a BGraph. 
        All arguments are optional.
        
        Note that the vertex is *not* added to the graph in this method. However, when a BEdge is
        created, all vertices are automatically added to the graph, if they are not already in it, 
        so it's rarely necessary to explicitly insert a vertex into the graph. 
        '''
        # This constructor should be invoked from subclasses, but it is strongly advised
        # that subclass constructors do not change the semantics.

        # This abstract superclass should never be instantiated, self should be a subclass instance
        print >> DEBUGSTREAM, "UH_BVERTEX_INIT", symbol

        self.modulePath = modulePath
        self.sidlnameregex=re.compile('\A[A-Za-z]+[A-Za-z0-9]*(\.[A-Za-z0-9]+)*\Z')

        if self.modulePath is not None: sys.path.append(self.modulePath)
        
        # The default action is '__init__' and is used only to obtain the 
        # general documentation for this class (the doc string immediately
        # after the __init__ method header. This documentation will be displayed when 
        # a user invokes 'bocca help subject' where subject is one 
        # of the BVertex subclasses. 
        if action is None: action = '__init__'
        if hasattr(self,action):
            self.parser = OptionParser(getattr(self, action).__doc__) 
        else:
            self.parser = OptionParser(getattr(self, '__init__').__doc__)
            if not kind:
                self.usage(exitcode=1, errmsg='Unknown symbol. SIDL spelling error?')         
            else:
                self.usage(exitcode=1, errmsg=kind + ' does not support the specified action: ' + action)         
        self.symbol = symbol 
        self.kind = kind
        if self.kind is None: self.kind = self.__class__.__name__.lower()
        self.data = {}
        self.options = None
        self.args = None
        self.version = '0.0'
        if version: self.version = version
        self.sidlImports = {}
        self.action = action
        
        self._b_externalSidlFiles={}
        
        # The following three data fields are used for imported SIDL
        self.astNode = None
        self.startComment = ''
        self.endComment = ''
        
        self.deps = {} # used for dependencies other than extension and implementation, key is symbol, value is sidl or xml file (or '%local%')
        self.rmdeps = []  # used for dependencies other than extension and implementation 

        if project is None and action == 'create' and self.kind == 'project':
            self.projectName = self.symbol
        elif project is not None:
            self.projectName = project.symbol
            # Load project bocca configuration from BOCCA/bocca.config
            project.defaults = cct._util.Globals().getDefaults(project.symbol, forceReload=True)

        self.project = project

        # map of  (aliased key, repositorypath value) valid after processAlii done.
        self.repoAliased = dict()

        # init host and user until overridden by alias or dpath options.
        from platform import uname
        from pwd import getpwuid
        self.host=uname()[1]
        self.user=getpwuid(os.getuid())[0]
        
        self.handleArgs(args,action)

        if self.symbol is None:
            # Try to get symbol from args (assuming it's the first argument)
            if self.args:
                self.symbol = self.args[0]
            elif kind == 'project' and project:
                return project
            else:
                err('[BVertex] Missing symbol name, make sure it is set from the command''s options.')

        # If --version/-v specified, set the version
        if not version:
            if self.kind == 'project': self.version = '0.0.0'
            else: self.version = '0.0'
                 
        if project != None:
            defaultPackage = None
            if project is not None: defaultPackage = project.getAttr('defaultPackage')
            if defaultPackage == None or defaultPackage == '': defaultPackage = self.projectName

            if self.symbol.count('.') == 0 and self.kind not in ['project', 'package']:
                if action == 'create' and self.kind != 'package': 
                    self.symbol = defaultPackage + '.' + self.symbol
                pgraph = Globals().getGraph(project.symbol)
                # First try to find the fully qualified symbol
                if pgraph is not None:
                    slist = pgraph.findSymbol(self.symbol,kind=self.kind,version=self.version)    
                    if len(slist) > 1:
                        err('Multiple matches for ' + self.kind + ' ' + self.symbol + ' found in this project. Please use a fully qualified SIDL symbol.')
                    elif len(slist) == 1:
                        self.symbol = slist[0].symbol

        # A dictionary of code blocks associated with a specific vertex type
        self.code = {}
        
        # Temporary storage of library names corresponding to this vertex
        self.libs = {'client':[], 'server':[]}
        
        Vertex.__init__(self, name=self.kind + '@' + self.symbol + '@' + self.version)

    # end __init__

    def initCopy(self, copiedVertex):
        self._b_externalSidlFiles = copiedVertex._b_externalSidlFiles
        # Non-_b_ data should be copied on a case-by-case basis depending on what
        # classes file here
        #self.data = copiedVertex.data  
        
    
    def changeSymbol(self, newSymbol=None, newVersion=None, inGraph=True):
        if not newSymbol and not newVersion: return
        p,g = cct._util.Globals().getProjectAndGraph(self.projectName)
        oldsymbol = self.symbol
        oldversion = self.version
        if newSymbol: self.symbol = newSymbol
        oldname = self.name
        if newVersion: self.version = newVersion
        self.name = self.kind + '@' + self.symbol + '@' + self.version
        self.project = p
        
        if g != None:
            if inGraph:
                if not oldname in g.v.keys():
                    raise SymbolError(oldsymbol, 'Symbol not found: ')
                # change vertex
                g.v.deleteItem(oldname)
                g.add_v(self)
        # change edges
        for e in self.in_e:
            if g != None: g.e.deleteItem(e.name)
            e.name = e.v[0].name + ':' + self.name
            e.v[1] = self
            if g != None: g.add_e(e)
        for e in self.out_e:
            if g != None: g.e.deleteItem(e.name)
            e.name = self.name + ':' + e.v[1].name
            e.v[0] = self
            if g != None: g.add_e(e)
        return 
    
    def handleArgs(self, args, action):
        # Define and process command line arguments -- the defineArgs and processArgs
        # are virtual methods that must be implemented by subclasses.
        print >>DEBUGSTREAM, '[BVertex] in handleArgs; action=',action,',args=', args

        if action and args != None:
            self.defineArgs(action)
            self.options, self.args = self.parser.parse_args(args)
            self.action = action
            self.processArgs(action)    # This is where we should set self.symbol from the args
# FIXME: Need a better way to handle (buildTemplate/codeTemplate) pair configuration
            self.templatePath = os.path.abspath(os.path.join(self.modulePath, 'templates', 'babel-1.0'))

    #----------------------------------------------------------------------------------
    # Begin methods that must be overridden by subclasses
    def createSIDL(self):
        '''Generate the sidl file(s) associated with the symbol of the vertex.
           The location manager abstraction in the builder is the recommended
           source of names for files. Non-generating vertices should return 0.
           @return 0 for success and nonzero for error; typically the error code
           comes from the filesystem or Babel.
        '''
        raise NotImplementedError

    #----------------------------------------------------------------------------------
    # Begin methods that can be overridden by subclasses

    #------------- Methods for defining and validation of command line arguments
    def defineArgs(self, action):
        """ Defines all command-line arguments for a subject.
        This is normally called by __init__ 
        """
        print >>DEBUGSTREAM, 'bvertex defineArgs'
        if self.__class__ is BVertex: raise NotImplementedError
        if not self.parser.has_option('--help'):
            self.parser.add_option("-h", "--help", dest="help", action="store_true",
                                   help="show the help message for this command and exit")
        if (action == 'remove' or action == 'rename') and not self.parser.has_option("--force"):
            self.parser.add_option("-f", "--force", dest="force", action="store_true",
                   help="Force the change without prompting for confirmation.")
        
        self.parser.set_defaults(help=False)
    
        return

    def processArgs(self, action):
        """ Validates and if necessary canonicalizes the command line arguments for
        this subject, which are parsed into self.options.
        It is very important to set self.symbol to the appropriate SIDL symbol or name.
        Exits nonzero if user gives bad input.
        """
        if self.__class__ is BVertex: raise NotImplementedError
        
        if hasattr(self.options,'help') and self.options.help:
            print getattr(self, action).__doc__
        if action == 'remove' or action == 'rename' and self.parser.has_option("--force"):
            self.parser.set_defaults(force=False)
        self.action = action
        
        return
       
    # ---------- Methods corresponding to bocca actions given on the command line
    def create(self):
        '''create SUBJECT [options] SIDL_SYMBOL
        
        Creates a new bocca entity based on the SUBJECT. Some SUBJECT examples 
        are project, package, interface, class, port, component.
        
        For more details on the creation of specific bocca entities, 
        try "bocca create SUBJECT --help" where SUBJECT is a specific bocca 
        entity name, e.g., component.
        '''
        if self.__class__ is BVertex: raise NotImplementedError
        return 1

    def copy(self):
        '''copy SUBJECT OLD_SIDL_SYMBOL NEW_SIDL_SYMBOL

        Copies an old bocca entity from OLD_SIDL_SYMBOL to NEW_SIDL_SYMBOL.
        The only supported SUBJECTs at this time are 'component' and 'class'.
        '''
        if self.__class__ is BVertex: raise NotImplementedError
    
    def change(self):
        '''change SUBJECT [options] SIDL_SYMBOL
        
        Changes some existing project element(s). Some SUBJECT examples
        are project, package, interface, class, port, component.

        For more details on changing specific bocca entities, 
        try "bocca change SUBJECT --help" where SUBJECT is a specific bocca 
        entity name, e.g., component.
        '''
        if self.__class__ is BVertex: raise NotImplementedError
        return 1
    
    def remove(self):
        '''remove SUBJECT [options] SIDL_SYMBOL

        Removes some existing project element(s). Some SUBJECT examples
        are project, package, interface, class, port, component.

        For more details on removing specific bocca entities, 
        try "bocca remove SUBJECT --help" where SUBJECT is a specific bocca 
        entity name, e.g., component.
        '''
        if self.__class__ is BVertex: raise NotImplementedError
        return 1
    
    def rename(self):
        '''rename SUBJECT [options] SIDL_SYMBOL NEW_SIDL_SYMBOL
        
        Renames some existing project element(s). Some SUBJECT examples
        are project, package, interface, class, port, component.

        For more details on renaming specific bocca entities, 
        try "bocca rename SUBJECT --help" where SUBJECT is a specific bocca 
        entity name, e.g., component.
        '''
        if self.__class__ is BVertex: raise NotImplementedError
        return 1
            
    def display(self):
        '''bocca display [SUBJECT] [SIDL_SYMBOL]
        
        Displays some existing project element(s). If no SUBJECT is given,
        the entire project is displayed. If a SUBJECT, e.g., port or component, is 
        specified but no specific port or component names given, all project
        elements of that kind are displayed. 
        '''
        if self.__class__ is BVertex: raise NotImplementedError
        retcode = 0
        project,pgraph = cct._util.Globals().getProjectAndGraph(self.projectName)
        v = pgraph.findSymbol(self.symbol,self.kind) 
        if len(v) > 0:
            for i in v: 
                print i.prettystr()
        else:
            err('[display ' + self.kind +  '] ' + self.kind + ' not found in current project.')
        return retcode
        
    def edit(self):
        '''bocca edit [options] SIDL_SYMBOL
         
        Open an editor for an editaable SIDL entity. For specific options, see
        bocca edit SUBJECT --help where SUBJECT can be interface, port, class, or component.
        '''
        if self.__class__ is BVertex: raise NotImplementedError
        return 1
    
    def config(self):
        '''bocca config [options]
        
        View or modify the contents of the project defaults file: <project dir>/BOCCA/<project name>.defaults
        '''
        if self.kind not in ['project']:
            err('The config command can only be used on a project, e.g., "bocca config project [options]"')
        return 1
    
    def update(self):
        '''bocca update [options]
        
        The update command supports options for updating or recovering the default build system files,
        generating sample cvs or svn commands (but not running cvs or svn), and other functionality 
        for managing bocca upgrades and interactions with revision control systems.  The 'update'
        verb is only available for projects. For information on specific options, run 
        bocca update project --help.
        '''
        if self.kind not in ['project']:
            err('The config command can only be used on a project, e.g., "bocca update project [options]"')
        return 1

    
    #------------------- End of actions interface
    
    # -------------- Various I/O methods which can be implemented by subclasses

    def _graphviz(self): return '"' + self.name + '"' + '[label="' + self.shortstr() + '",' + self.graphvizString() + '];\n'
    
    def graphvizString(self): return 'color=white'

    def __str__(self):
        ''' Default conversion to a string.'''
        if hasattr(self,'name'):
            (kind, symbol, version) = self.name.split('@')
            return '%s: %s %s' % (kind, symbol, self.data)  
        else:
            return '%s: %s %s' % ("unkind", "unnamed", self.data)  

    def prettystr(self):
        buf = self.kind + ' ' + self.symbol + ' version ' + self.version
        for j in self.data.keys():
            if j not in ['methodsIndent']:
                buf += '\n\t' + str(j) + ': ' + str(self.data[j])
        return buf
    
    def shortstr(self):
        '''Shorter string representation'''
        (kind, symbol, version) = self.name.split('@')
        return '%s: %s %s' % (kind, symbol, version)  
 
    def usage(self, exitcode=0, errmsg=None):
        if errmsg is not None:
            print >>sys.stderr, 'Bocca ERROR: ', errmsg
        self.parser.print_help()
        sys.exit(exitcode)
        return
    
    # ============ ASCII serialization and deserialization routines
    
    def serializeASCII(self, filedesc = None):
        '''Writes a complete ASCII representation of current object which 
        can be used to reconstruct the object by calling deserialize.
        Note that pickle is used during development for maintaining the 
        state of a project; this serialization will be used only rarely, i.e.,
        when migrating a project to a new environment or when merging projects. 
        '''
        classname = str(self.__class__)
        # Get rid of leading cct., just save pkgname.classname
        # Also add package if classname doesn't already contain it
        if classname.count('.') == 0:
            classname = classname.lower() + '.' + classname
        elif classname.count('cct.') > 0:
            classname = classname[classname.find('cct.')+4:len(classname)]
        itemlist = self._getSerializableFields()
        count = 0
        buf = ''
        for item in itemlist:
            buf += '%s=%s|' % (item,str(self.__dict__[item]))  # the separator is '|'
            count += 1

        # Now fields that start with _b_
        blist = []
        for member in self.__dict__.keys():
            if  member.startswith('_b_'):
                blist.append(member)

        blist.sort()
        for item in blist:
            buf += '%s=%s|' % (item, str(self.__dict__[item])) # the separator is '|'
            count += 1
        if buf.endswith('|'): buf = buf[:-1]   # For some reason rstrip wasn't working!
        buf  = '!vertex=' + classname + '\n' + 'count=' + str(count) + '|' + buf + '\n' 
        if filedesc: filedesc.write(buf)
        return buf

    def deserializeASCII(self, thestring, version=bocca_version, action='__init__'):
        '''Returns an instance of a specific vertex type configured with
        the information resulting from deserializing the thestring string. 
        The first line in the string contains "!vertex=NUMBER" where
        NUMBER is the number of subsequent entries corresponding to this vertex.
        '''
        backwardCompat = False
        if version != bocca_version:
            # Need to convert serialization produced with older bocca to current format
            try:
                method = getattr(self,'deserializeASCII_' + version.replace('.','_')) 
                backwardCompat = True
            except:
                if action != 'update':
                    print >>sys.stderr, 'Bocca ERROR: the project was created with a different version of Bocca (%s), you should run "bocca update -s"' % version
                    sys.exit(1)
        if backwardCompat and method:
            method(thestring)
        else:
            # Try to read it anyway, even if there is a version mismatch
            namevalpairs = thestring.strip().split('|')
            count = int(namevalpairs[0].split('=')[1])
            if len(namevalpairs) != count + 1:
                print >>sys.stderr, 'Bocca ERROR: the vertex string does not contain the expected number of entries for deserialization'
                sys.exit(1)
            for i in range(1,count+1): 
                #print 'nameval pair is ' + namevalpairs[i]
                item, val = namevalpairs[i].strip().split('=')
                if item in ['_b_uses', '_b_provides']:
                    self.__dict__[item] = []
                    tuple_array = deserializeASCII(val)
                    for tup in tuple_array:
                        p = PortInstance(typename=tup[0],name=tup[1],location=tup[2])
                        self.__dict__[item].append(p)
                else:
                    self.__dict__[item] = deserializeASCII(val)   # the deserialize val is implemented in utils.py

        return
    
    #----------- Methods from deserializing projects created with older versions of Bocca
    def deserializeASCII_0_4_0(self, thestring):
        namevalpairs = thestring.strip().split('|')
        count = int(namevalpairs[0].split('=')[1])
        usesPorts = {}
        providesPorts = {}
        usesLocations = {}
        providesLocations = {}
        if len(namevalpairs) != count + 1:
            err('BVertex: the string does not contain the expected number of entries for deserialization')
        for i in range(1,count+1): 
            #print 'nameval pair is ' + namevalpairs[i]
            item, val = namevalpairs[i].strip().split('=')
            if item in ['_b_usesPorts', '_b_usesLocations', '_b_providesPorts', '_b_providesLocations']:
                if item == '_b_usesPorts': usesPorts = deserializeASCII(val)
                if item == '_b_providesPorts': providesPorts = deserializeASCII(val)
                if item == '_b_usesLocations': usesLocations = deserializeASCII(val)
                if item == '_b_providesLocations': providesLocations = deserializeASCII(val)
            else:
                self.__dict__[item] = deserializeASCII(val)   # the deserialize val is implemented in utils.py
                
        # Create the new data structures
        for k, v in usesPorts.items():
            p = PortInstance(typename=v, name=k, location=usesLocations[v])
            self.__dict__['_b_uses'].append(p)  
        for k, v in providesPorts.items():
            p = PortInstance(typename=v, name=k, location=providesLocations[v])
            self.__dict__['_b_provides'].append(p)
        return
            
        

################################################################################# 
# ---- The following methods should in general not be overloaded by child classes
    
    def clone(self):
        '''This is not a full clone, just some of the basics for use in rename.'''
        newvertex = self.__class__(symbol=self.symbol,version=self.version,project=self.project)
        if self.kind in ['class', 'component', 'port', 'interface']: newvertex._b_sidlFile = self._b_sidlFile
        if self.kind in ['class','component']:
            newvertex._b_implements = self._b_implements
            newvertex._b_extends = self._b_extends
        if self.kind == 'component':
            newvertex._b_provides = self._b_provides
            newvertex._b_uses = self._b_uses
        return newvertex
        
    def renameInternalSymbol(self, oldsymbol, newsymbol):
        '''Replaces any internal references to oldsymbol with newsymbol.'''
        if self.__class__ is BVertex: raise NotImplementedError
        return 1

    def removeInternalSymbol(self, symbol):
        ''' Removes any internal references to symbol.'''
        if self.__class__ is BVertex: raise NotImplementedError
        return 1
   
    def validateNewSymbol(self, graph):
        '''Ensures that the current symbol is not already in the graph. Only fully qualified symbols are matched.
        '''
        if self.sidlnameregex.match(self.symbol) == None:
            err('[' + self.action + ' ' + self.kind + '] the specified symbol is not legal SIDL: ' + self.symbol, 4) 
        # If package not given, prepend default one
        if self.symbol.count('.') == 0 and self.kind != 'package': 
            self.symbol = self.project.getAttr('defaultPackage') + '.' + self.symbol
        if graph:
            flag, vertex = graph.containsSIDLSymbol(self.symbol)
            if flag:
                err('[' + self.action + ' ' + self.kind + '] the specified SIDL symbol already exists in this project:\n\n' + vertex.prettystr(), 4) 
        return
    
    def validateExistingSymbol(self, graph):
        '''Returns a fully qualified name and sets self.symbol to it if a unique match is found in the graph.
        '''
        if not self.symbol: self.symbol = self.args[0]
        if not graph: graph = Globals().getGraph(self.projectName)
        slist = graph.findSymbol(self.symbol, self.kind, self.version)
        if len(slist) == 0:
            err(self.kind + " symbol " + self.symbol + " version "+ self.version + " not found in project.", 3)
        elif len(slist) > 1:
            err('specified ' + self.kind + ', ' + self.symbol + ', is ambiguous, please use a fully qualified SIDL symbol.',3)
        else:
            self.symbol = slist[0].symbol
            print >>DEBUGSTREAM, 'validated symbol: ' + self.symbol
        return self.symbol
    
    def dependents(self,type=None):
        ''' Returns all vertices that depend on this vertex.
        @param type specifies the type of the dependence to consider, and must be one of:
             None (gets all dependents), extends, implements, uses, provides, requires, contains.'''
        graph = Globals().getGraph(self.projectName)
        if graph: return graph.breadth_first_search(self)[1:]
        else: return []
        
    def dependencies(self):
        ''' Returns all vertices on which this vertex depends.
        '''
        project,graph = Globals().getProjectAndGraph(self.projectName)
        if graph: return graph.breadth_first_search(self,reverse=True)[1:]
        else: return []
        

    def walk(self, edgefilter=[], reverse=True, depthfirst=True ):
        ''' Returns all vertices that this vertex depends on, but only with 
        the specified types of edges.
        @param edgefilter specifies the type of the dependence to consider, and can contain 
            extends, implements, uses, provides, requires, contains.
        @param reverse perform the search in reverse edge direction; default is True, meaning that 
            we will search among the ancestors of the vertex.
        @param depthfirst specify that a depth-first (as opposed to breadth-first) search should be performed.
            default is True.
        '''
        project, graph = Globals().getProjectAndGraph(self.projectName)
        if graph:
            if depthfirst: return graph.bocca_depth_first_search(start_v=self,reverse=reverse,actions=edgefilter)[1:]
            if not depthfirst: return graph.bocca_breadth_first_search(start_v=self,reverse=reverse,actions=edgefilter)[1:]
        else:
            return []

    def getAttr(self, key):
        if key in self.data.keys():
            return self.data[key]
        else:
            return None
        
    def setAttr(self, key, val):
        self.data[key] = val
        return self.data[key]
    
    def delAttr(self,key):
        if key in self.data.keys():
            del self.data[key]
        return
    
    def saveProjectState(self, graph, graphviz=True):
        '''Saves the project's graph in a pickle file. If graphviz is True, it also saves a dot file
        containing the GraphViz representation of the project graph. 
        '''
        if self.project:
            graph.saveGraphvizFile(os.path.join(self.project.getDir(),'BOCCA','graphics',self.projectName+'.dot'))
            graph.save()        
        return
    
    def getSIDLSplicerKey(self):
        return 'DO-NOT-DELETE bocca.splicer'
    
    def getSIDLSplicerBeginString(self, indentstr='', tag = None, extraSplicerComment = False, insertComment=''):
        if tag is None: tag = self.symbol
        thestring =  indentstr + '// ' + self.getSIDLSplicerKey() + '.begin(' + tag + ')\n' 
        if extraSplicerComment:
            thestring += indentstr + '\n// Insert-UserCode-Here {' + tag + '}'
            if insertComment: 
                thestring += ' (' + insertComment + ')'
            thestring += '\n'
        return thestring
            
    def getSIDLSplicerEndString(self, indentstr='', tag = None): 
        if tag is None: tag = self.symbol
        return indentstr  + '// ' + self.getSIDLSplicerKey() + '.end(' + tag + ')\n' 
        
    def getSIDLImports(self):
        return self.sidlImports
    
    def setSIDLImports(self, imports):
        self.sidlImports = imports

    def handleNonInheritanceDependencies(self):
        ''' Add or remove dependencies other than extension'''
        project, pgraph = Globals().getProjectAndGraph(self.projectName)
        # TODO: need to add external symbol handling (not just within project)
        if self.deps:
            print >> DEBUGSTREAM, self.deps
            dep = self.getAttr('requires')
            if not dep: dep = []
            for symbol, fname in self.deps.items():
                if fname == '%local%':
                    vlist = pgraph.findSymbol(symbol,kind='any')
                    if len(vlist) == 0:
                        if symbol.startswith('gov.cca.'):
                            from cct import interface
                            specversion = Globals().getCCAVars(projectName=project.getName())['CCASPEC_VERSION']
                            # TODO: for now we treat all CCA SIDL entities as interfaces
                            v = interface.Interface(action='create', symbol=symbol, version=specversion,
                                                        project=project, modulePath=self.modulePath, graph=pgraph)
                        else:
                            err('could not find symbol ' + symbol + ' on which ' + self.symbol + ' depends.')
                    else:
                        v = vlist[0]
                    edge = BEdge(v, self, pgraph, action='requires')
                    dep.append(v.symbol)
                if fname != '%local%':
                    dep.append(symbol)
                    self._b_externalSidlFiles[symbol] = fname
            self.setAttr('requires', dep)
            
        if self.rmdeps:
            # Remove dependencies
            dep = self.getAttr('requires')
            for s in self.rmdeps:
                if s.startswith(os.path.sep) and s.endswith('.sidl'):
                    if s in self._b_externalSidlFiles.values(): 
                        for k, v in self._b_externalSidlFiles.items():
                            if v == s:
                                del self._b_externalSidlFiles[k]
                                break
                    else: warn('specified file not found in this ' + self.kind + "'s dependencies")
                elif s in self._b_externalSidlFiles.keys():
                    dep.remove(s)
                    del self._b_externalSidlFiles[s]
                    project.cleanExternal(s)
                else:
                    vlist = pgraph.findSymbol(s,kind='any')
                    n = ''
                    if len(vlist) == 1: n = vlist[0].name
                    else: err('Symbol ' + s + ' is ambiguous or not found. Please specify a fully qualified SIDL symbol in the --remove-requires option.')
                    for edge in self.in_e:
                        fro,to = edge.name.split(':') 
                        if n == fro:
                            pgraph.removeEdge(edge)
                            dep.remove(n.split('@')[1])
            if dep:
                self.setAttr('requires', dep)
            else: 
                self.delAttr('requires')
        return
                    
    def handleSIDLImports(self, methods=None, replaceEnums=False, mergeBuildfiles=False):
        '''
        Import methods specified with the --import-sidl option into this interface.
        '''

        if not methods:
            from parse.itools.parser import Parser    
            from parse.itools.visitor.subtree import SubtreeImporter
        from parse.itools.visitor.printer import Printer
        from splicers.Operations import mergeFromString

        print >> DEBUGSTREAM, self.kind + ', handleSIDLImports: about to import from ' + str(self.getSIDLImports())
        
        retcode = 0
        project, pgraph = Globals().getProjectAndGraph(self.project.symbol)
        
        # Load some defaults
        # Create the beginning of the splicer block for the methods
        tabsize = self.project.getDefaultValue('tab_size', section='SIDL') 
        if tabsize: tab = int(tabsize)
        else: tab = '    '

        
        # Parse the SIDL files specified using the --import-sidl option and 
        # construct the strings containing methods declarations for each 
        # specified interface.
        if not methods:
            parser = Parser()
    
        sidlimports = self.getSIDLImports()
    
        for fileName in sidlimports.keys():
            if not methods:
                try:
                    ast = parser.parseFile(fileName, stripBocca=True)
                except:
                    err('could not parse ' + fileName + '. Please make sure that it contains valid SIDL (e.g., with babel -p).')
                #parser.printAST()
            
                # Import the various graph elements (subtreeVisitor creates the BVertex subclasses and appropriate edges)
                subtreeVisitor = SubtreeImporter(sidlimports[fileName], parentVertex=self, projectName = self.projectName)

                ast.accept(subtreeVisitor)
             
                packages    = subtreeVisitor.getPackages()  
                interfaces  = subtreeVisitor.getInterfaces()
                enums       = subtreeVisitor.getEnums()
                classes     = subtreeVisitor.getClasses()
                methods     = subtreeVisitor.getMethods()

            try: from cStringIO import StringIO
            except: from StringIO import StringIO
 
            #print ' All methods: ' + str(methods)
            
            # Handle package-level and project-level imports (recursively)
            # Process imported interfaces
            if self.kind in ['package', 'project', 'enum']:
                # Process imported interfaces and ports
                retcode = 0
                for k, i in interfaces.items():
                    mymethods = {}
                    if k not in methods.keys():
                        err('the specified SIDL interface, ' + str(k) + ', could not be imported. Make sure the symbol exists in the source SIDL file.')
                    mymethods[k] = methods[k]
                    i.setSIDLImports(sidlimports)
                    i.handleSIDLImports(mymethods, mergeBuildfiles=mergeBuildfiles)
                    # dependencies
                    extends = i.getAttr('extends')
                    if not extends: extends = {}
                    for p in i.getASTNode().getParentIds():
                        lst = pgraph.findSymbol(p)
                        if len(lst) == 1:
                            edge = BEdge(lst[0], i, pgraph, action='extends')
                            if lst[0].symbol not in extends.keys():
                                extends[lst[0].symbol] = '%local%'
                    i.setAttr('extends',extends)
                    for pnode in i.getASTNode().getDependencies():
                        parentid = pnode.getFullIdentifier()
                        lst = pgraph.findSymbol(parentid)
                        if len(lst) == 1: edge = BEdge(lst[0], i, pgraph, action='requires')
                    
                # Process imported enums
                for k, e in enums.items():
                    indentSize = e.symbol.count('.') + 1
                    indentstr = indentSize*tab*' '
                    
                    # Generate comment splicers for the enclosing content
                    commentsplicer =''
                    if e.getComment():
                        commentsplicer = e.getCommentSplicerString(indentstr=(indentSize-1)*tab*' ', initialNewline=False)
                    
                    if not e._b_sidlFile:
                        e._b_sidlFile = os.path.join(self.project.getLocationManager().getSIDLLoc(e)[0], e.symbol + '.sidl')
                    
                    print >> DEBUGSTREAM, e.symbol + ' importing enum into %s: ' % e._b_sidlFile 
    
                    importedEnumString = e.getASTNode().getContents().strip()
                    if not importedEnumString.endswith(','): importedEnumString += ','
                    enumentries = ''
                    for l in importedEnumString.split('\n'): enumentries += indentstr + l.strip() + '\n'

                    # The enum body
                    enumbodystr = commentsplicer 
                    enumbodystr += e.getSIDLSplicerBeginString(indentstr, tag=e.symbol + '.entries')        
                    enumbodystr += enumentries
                    enumbodystr += e.getSIDLSplicerEndString(indentstr, tag=e.symbol + '.entries') 
    
                    print >> DEBUGSTREAM, '--import-sidl, about to import enum into ' + e.symbol +': \n' + enumbodystr + '\n'
    
                    sidlfile = os.path.join(self.project.getDir(),e._b_sidlFile)
                    # Now import the methods
                    retcode = mergeFromString(targetName=sidlfile, srcString=enumbodystr, srcName=sidlfile, 
                                      targetKey=self.getSIDLSplicerKey(), sourceKey=self.getSIDLSplicerKey(), 
                                      methodMatch=True, 
                                      insertFirst=False, warn=WARN, replaceIdentical=replaceEnums, rejectSave=False)

                
                # Process imported classes
                for k, c in classes.items():
                    mymethods = {}
                    if k not in methods.keys():
                        err('the specified SIDL class, ' + str(k) + ', could not be imported. Make sure the symbol exists in the source SIDL file.')
                    mymethods[k] = methods[k]
                    c.setSIDLImports(sidlimports)
                    c.handleSIDLImports(mymethods, mergeBuildfiles=mergeBuildfiles)
                    # add dependencies (note that all except uses ports dependencies can be computed from the SIDL)
                    for pnode in c.getASTNode().getParents():
                        parentid = pnode.getFullIdentifier()
                        lst = pgraph.findSymbol(parentid)
                        if len(lst) == 1:
                            vertex = lst[0]
                            if vertex.kind in ['interface', 'port']:
                                if pnode in c.getASTNode().getInterfacesAll():
                                    edge = BEdge(vertex, c, pgraph, action='implements-all')
                                else:
                                    edge = BEdge(vertex, c, pgraph, action='implements')
                                if vertex.kind == 'port' and c.kind == 'component':
                                    portname = parentid.split('.')[-1]
                                    count = 0
                                    pname = portname
                                    while portname in c._b_providesPorts.keys():
                                        portname = pname + str(count)
                                        count += 1
                                    c._b_providesPorts[portname] = parentid
                                    c._b_providesLocations[parentid] = '%local%'
                                else:
                                    if parentid not in c._b_implements.keys():
                                        c._b_implements[parentid] = '%local%'
                            elif vertex.kind in ['class', 'component']:
                                edge = BEdge(vertex, c, pgraph, action='extends')
                                if parentid not in c._b_extends.keys():
                                    c._b_extends[parentid] = '%local%'

                        for pnode in c.getASTNode().getDependencies():
                            parentid = pnode.getFullIdentifier()
                            lst = pgraph.findSymbol(parentid)
                            if len(lst) == 1: edge = BEdge(lst[0], c, pgraph, action='requires')
                        
                return retcode

            # ---------------------------------------------------------
            # This handles importing of buildfiles
            if mergeBuildfiles:
                sidlDir = fileName[:fileName.rfind('/')]
                externalProjectName, externalProjectDir = getProjectInfo(projectDir=sidlDir)

                if externalProjectName is not None and externalProjectDir is not None \
                        and externalProjectName != self.project.getName() and externalProjectDir != self.project.getDir():
                    localdir, buildfiles = self.project.getLocationManager().getUserBuildfilesLoc(self)
                    for buildfile in [os.path.join(localdir, f) for f in buildfiles]:
                        target = os.path.join(self.project.getDir(), buildfile)
                        source = os.path.join(externalProjectDir, buildfile)
                        
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

            # ---------------------------------------------------------
            # The remainder of this method deals with importing methods
            
            # Configure the printer for the methods
            indentSize = self.getAttr('methodsIndent')
            if indentSize is None: indentSize = self.symbol.count('.') + 1
            
            # Generate comment splicers for the enclosing content
            commentsplicer =''
            if self.kind != 'package' and self.getComment():
                commentsplicer = self.getCommentSplicerString(indentstr=(indentSize-1)*tab*' ')
                
            for sym in methods.keys():
                if self.kind not in ['interface', 'port', 'class', 'component','package','project']:
                    err('trying to import SIDL methods into ' + self.kind + '; methods can only be imported into projects, packages, interfaces, ports, classes, or components')
                    
                if not self._b_sidlFile:
                    self._b_sidlFile = os.path.join(self.project.getLocationManager().getSIDLLoc(self)[0], self.symbol + '.sidl')
                

                print >> DEBUGSTREAM, self.symbol + ' importing methods into %s: '%self._b_sidlFile +  str(methods[sym])

                printer = Printer(outstream = StringIO(), tab = tab*' ', initialIndent = indentSize, 
                                  commentExcludeList=['bocca\.splicer','Insert your\s*\w* methods here'])
                indentstr = indentSize*tab*' '
                
                methodstr = commentsplicer
                
                # The methods string
                methodstr += self.getSIDLSplicerBeginString(indentstr, tag=sym + '.methods',  insertComment='Insert your ' + self.kind + ' methods here')                 
                for method in methods[sym]:
                    method.accept(printer)
                methodstr += printer.getOutStream().getvalue()
                methodstr += '\n' + self.getSIDLSplicerEndString(indentstr, tag=sym + '.methods') 

                print >> DEBUGSTREAM, '--import-sidl, about to import methods into ' + sym +': \n' + methodstr + '\n'

                sidlfile = os.path.join(self.project.getDir(),self._b_sidlFile)
                # Now import the methods
                retcode = mergeFromString(targetName=sidlfile, srcString=methodstr, srcName=sidlfile, 
                                  targetKey=self.getSIDLSplicerKey(), sourceKey=self.getSIDLSplicerKey(), 
                                  methodMatch=True, 
                                  insertFirst=False, warn=WARN, replaceIdentical=False, rejectSave=False)
        
        # TODO: check this with babel (using builder plugin)
    
        return retcode

    def getASTNode(self):
        return self.astNode
    
    def setASTNode(self, astNode):
        import parse.itools.elements as ast
        self.astNode = astNode
        self.setComment(astNode.getStartComment())
        self.endComment = astNode.getEndComment()
        pass 
    
    def setComment(self, comment):
        self.startComment = comment
        pass
    
    def getComment(self):
        return self.startComment
    
    def getCommentSplicerString(self, indentstr='', extraSplicerComment=False, initialNewline=True):
        buf =''
        if initialNewline: buf += '\n'
        buf += self.getSIDLSplicerBeginString(indentstr, tag = self.symbol + '.comment', 
                                              extraSplicerComment=extraSplicerComment, 
                                              insertComment='Insert your ' + self.kind + ' comments here') 
        if self.startComment: buf += self._indentComment(indentstr, self.startComment, prependNewline=False) +'\n'
        buf += self.getSIDLSplicerEndString(indentstr, tag = self.symbol + '.comment')
        return buf
    
    def removeInEdge(self, sidlsymbol, kind='any', graph=None):
        if not graph:
            project, graph = Globals().getProjectAndGraph(self.projectName)
        # remove edge
        vlist = graph.findSymbol(sidlsymbol, kind = kind)
        if vlist:
            for e in self.in_e:
                if vlist[0].name == e.v[0].name: 
                    print >>DEBUGSTREAM, 'BVertex: removing in edge: ' + str(e)
                    graph.removeEdge(e)
        return
    
    #------------------------- PRIVATE Methods ------------------------
    
    def _getSerializableFields(self):
        '''Return a list of field names (strings) that will be serialized with pickle 
        and with the portable serializer. In addtion to those, the class name is serialized
        and any field whose identifier starts with _b_.
        '''
        return ['name', 'symbol', 'kind', 'version', 'projectName', 'data', 'code']
    
    def _savePickle(self,filedesc,protocol=2):
        '''Given a filed escriptor of an open pickle file, 
        save everything necessary to recreate this vertex, omitting
        the edge list to avoid recursion.'''
        classname = str(self.__class__)
        # Get rid of leading cct., just save pkgname.classname
        # Also add package if classname doesn't already contain it
        if classname.count('.') == 0:
            classname = classname.lower() + '.' + classname
        elif classname.count('cct.') > 0:
            classname = classname[classname.find('cct.')+4:len(classname)]

        pickle.dump(classname, filedesc, protocol)   # Specific vertex class module name
        pickle.dump(self.name, filedesc, protocol)
        pickle.dump(self.symbol, filedesc, protocol)
        pickle.dump(self.kind, filedesc, protocol)
        pickle.dump(self.version, filedesc, protocol)
        pickle.dump(self.projectName, filedesc, protocol)
        pickle.dump(self.data, filedesc, protocol)
        pickle.dump(self.code, filedesc, protocol)
        # Now pickle any fields starting with _b_ :
        picklelist = []
        for member in self.__dict__.keys():
            if type(member) is str and member.startswith('_b_'):
                picklelist.append(member)
        pickle.dump(len(picklelist), filedesc, protocol)
        for item in picklelist:
            pickle.dump(item, filedesc, protocol)
            pickle.dump(self.__dict__[item], filedesc, protocol)

        # Edges are deliberately omitted to avoid recursion
        return

    def _loadPickle(self,filedesc):
        '''Given a file descriptor of an open pickle file, recover 
        all fields of this vertex except for the edge list (which 
        is reconstructed when the edges are unpickled.'''
        self.name = pickle.load(filedesc)
        self.symbol = pickle.load(filedesc)
        self.kind = pickle.load(filedesc)
        self.version = pickle.load(filedesc)
        self.projectName = pickle.load(filedesc)
        self.data = pickle.load(filedesc)
        self.code = pickle.load(filedesc)
        # Now load any fields starting with _b_ : 
        numberOfItems = pickle.load(filedesc)
        for i in range(0,numberOfItems):
            item = pickle.load(filedesc)
            self.__dict__[item] = pickle.load(filedesc)

        # Edges are deliberately omitted to avoid recursion
        return self

    # End methods that can be overridden by subclasses
    #----------------------------------------------------------------------------------
              
    def _defineDpathArgs(self):
        self.parser.add_option("--dpath", dest="set_query_path", action="store",
                               help="Reset the search path for external symbols in _depl.xml files with the file or directories given. Done before append, prepend. Do not mix append and prepend in the same command.")
        self.parser.add_option("--dpath-clear", dest="clear_query_path", action="store_true",
                               help="Remove the search path for _depl.xml files. Done before any other dpath actions.")
        self.parser.add_option("--dpath-append", dest="append_query_path", 
                               action="append",
                               help="Extend the search path for external symbols in _depl.xml files with the file or directory given.")
        self.parser.add_option("--dpath-prepend", dest="prepend_query_path", action="append",
                               help="Insert at front of the current search path for external symbols in _depl.xml.")
        self.parser.add_option("--dpath-user", dest="user_query_path", action="store",
                               help="Redefine the username to which other dpath options apply.")
        self.parser.add_option("--dpath-host", dest="host_query_path", action="store",
                               help="Redefine the hostname to which other dpath options apply.")
        self.parser.add_option("--dpath-show", dest="show_query_path", action="append",
                               help="--dpath-show[=FILTER] Show the search path for _depl.xml files, filtered by optional [USER]@[HOST] or ALL.")
        self.parser.add_option("--dpath-user-alias", dest="new_user_alias", action="append",
                               help="Define build-equivalent username for current username.")
        self.parser.add_option("--dpath-host-alias", dest="new_host_alias", action="append",
                               help="Define build-equivalent hostname for current hostname.")
        self.parser.add_option("--dpath-show-aliases", dest="show_alias", action="store_true",
                               help="Show equivalent repository names for current user and host.")
        self.parser.set_defaults(set_query_path="", append_query_path=[], prepend_query_path=[], clear_query_path=False, show_query_path=[], new_user_alias=[], new_host_alias=[], show_alias=False)

    def _processDpathOptions(self):
        """digest the path changing arguments and fetch up the show list. 
           when called, we don't know what the symbol may be yet.
           Switch handling is reordered to clears, sets, appends, prepends, show.
           @return (dpathdata tuple)"""

        print  >>DEBUGSTREAM, "_processDpathOptions#########################"
        reset=False
        pathsep=":"
        newpath=""
        appends =""
        prepends =""

        print  >>DEBUGSTREAM, "UH_procDpath"
        host=self.host
        user=self.user
        show=[]
        if self.parser.has_option("--dpath-show"):
            if self.options.user_query_path and len(self.options.user_query_path) > 0:
                user=self.options.user_query_path
            if self.options.host_query_path and len(self.options.host_query_path) > 0:
                host=self.options.host_query_path
            if self.options.clear_query_path:
                reset = True
            if self.options.set_query_path and len(self.options.set_query_path) > 0:
                newpath=self.options.set_query_path
                reset=True
            if self.options.append_query_path and len(self.options.append_query_path) > 0:
                appends = pathsep.join(self.options.append_query_path)
            if self.options.prepend_query_path and len(self.options.prepend_query_path) > 0:
                prepends = pathsep.join(reversed(self.options.prepend_query_path)) 
            show = self.options.show_query_path

        useralii=[]
        hostalii=[]
        showalii=False
        if self.parser.has_option("--dpath-user-alias"):
            useralii=self.options.new_user_alias
        if self.parser.has_option("--dpath-host-alias"):
            hostalii=self.options.new_host_alias
        if self.parser.has_option("--dpath-show-aliases"):
            showalii=self.options.show_alias
        return (user, host, pathsep, reset, newpath, prepends, appends, show, useralii, hostalii, showalii)

    def _addAliasDefault(self, section, aliaskind, org, new, myproj, defaults):
        """insert alias new for org in defaults file, which may be just initialized
as part of creating a new project or in existing project. key format is Alias.aliaskind=x.
If configparse allowed multiple instances of a key, we would put the alias name data in x."""
        newkey="Alias."+aliaskind +"&"+org+"&"+new
        if myproj:
            myproj.setDefaultValue(newkey,"x",section)
            return
        defaults.set(section, newkey, "x")
        return

    def _loadAliasTables(self, myproj, defaults):
        """ keys in defaults are UserAlias and HostAlias in RP section.
Aliasing keys are managed as unordered pairs, for easy merge and removal.
Values are placeholding only. @return usertab,hosttab"""
        print >>DEBUGSTREAM, "UH_loadAliasTables#########################"
        hosttab = Nametab()
        usertab = Nametab()
        if myproj:
            rkeys=myproj.getDefaultSectionKeys('RepositoryPaths')
        else:
            rkeys = defaults.options('RepositoryPaths')
        for i in rkeys:
            if i.startswith("Alias.User&"):
                (dummy, org, new) = i.split("&")
                usertab.addAlias(org, new)
            if i.startswith("Alias.Host&"):
                (dummy, org, new) = i.split("&")
                hosttab.addAlias(org, new)
        return (usertab, hosttab)

    def _loadRepoAliasing(self, user, host, myproj, defaults, usertab, hosttab):
        print >>DEBUGSTREAM, "UH_loadRepoAliasing#########################"
        pathsep = ':'
        usergroup=usertab.findGroup(user)
        hostgroup=hosttab.findGroup(host)
        print >>DEBUGSTREAM, "UH_loadRepoAliasing user", usergroup
        print >>DEBUGSTREAM, "UH_loadRepoAliasing host", hostgroup
        if myproj:
            rkeys=myproj.getDefaultSectionKeys('RepositoryPaths')
        else:
            rkeys = defaults.options('RepositoryPaths')
        repoPathAliasing = []
        for i in rkeys:
            if i.count("@")>0:
                orgkey = i
                if myproj:
                    value =  myproj.getDefaultValue(i,'RepositoryPaths')
                else:
                    value =  defaults.get('RepositoryPaths', i)
                (ouser, ohost, sym) = i.split("@")
                if ouser in usergroup:
                    ouser = user
                if ohost in hostgroup:
                    ohost = host
                aliasedkey="@".join([ouser, ohost, sym])
                repoPathAliasing.append([aliasedkey, orgkey, value])
        repoDict = dict()
        for i in repoPathAliasing:
            if repoDict.has_key(i[0]):
                tuple = repoDict.get(i[0])
                if i[0] == i[1]:
                    # priority in dict groups goes to org matching morphed
                    tuple.insert(i)
                else:
                    tuple.append(i)
            else:
                repoDict[i[0]] = [i]
        pathDict = dict()
        for i in repoDict.keys():
            values = []
            for j in repoDict[i]:
                values.append(j[2])
            value = pathsep.join(values)
            self.repoAliased[i] = value
                
        print >> DEBUGSTREAM, "UH_Loadedrepo:", self.repoAliased
    # end _loadAliasTables

    def _processAlii(self, myproj, defaults, user, host, useralii, hostalii, showalii):
        """process alias switches and return canonical, (user host). Nametabs are used for resolving
aliases, but all data is stored as Alias defaults pairwise to make version and multiuser merge 
of the defaults file easy."""
        print >>DEBUGSTREAM, "UH_processAlii#########################"
        if myproj:
            (usertab, hosttab) = self._loadAliasTables(myproj, defaults)
        else:
            if not defaults.has_section('RepositoryPaths'): defaults.add_section('RepositoryPaths')
            firstuser = user
            firsthost = host
            self._addAliasDefault('RepositoryPaths', 'User', firstuser, firstuser, myproj, defaults)
            self._addAliasDefault('RepositoryPaths', 'Host', firsthost, firsthost, myproj, defaults)
            (usertab, hosttab) = self._loadAliasTables(myproj, defaults)
        for i in useralii:
            usertab.addAlias(user, i)
            self._addAliasDefault('RepositoryPaths', 'User', user, i, myproj, defaults)
        for i in hostalii:
            hosttab.addAlias(host,i)
            self._addAliasDefault('RepositoryPaths', 'Host', host, i, myproj, defaults)
        user=usertab.canonicalName(user)
        host=hosttab.canonicalName(host)
        if showalii:
            print "Host equivalence table:"
            print hosttab.printtab()
            print "User equivalence table:"
            print usertab.printtab()
        self._loadRepoAliasing(user, host, myproj, defaults, usertab, hosttab)
        print  >>DEBUGSTREAM, "_processAlii returns:", user, host
        return (user, host)

    def _updateDpaths(self, dpathdata, sidlname="", defaults=None):
        """dpath data are stored in the RepositoryPaths (RP) section of the defaults file.
Data (for multiuser, version controlled portability) in the RP are keyed by user@host[@sidlname]. 
Resolution of external symbols by depl xml scanning should start with the paths keyed to the sidlname
for which the dependency information is needed with identically matched user@host. Then scan
additionally the project dpath user@host@<nosymbol>. If not resolved, lots of hints can be
issued (or warnings if indexed files have disappeared) based on matching user but trying other hosts
and (at lower priority) searching all other listed paths in unmatching user for the same host.
Ultimately, that can lead to bad suggestions but the user will have to update the dpaths to resolve
the problem.  """
        print >>DEBUGSTREAM, "_updateDpaths#########################"
        print >>DEBUGSTREAM,  self
        myproj, graph = Globals().getProjectAndGraph(projectName=self.projectName)
        if not defaults and myproj:
            """ should happen except in create project, where we send in the defaults"""
            defaults = myproj.getDefaults()
        if not defaults: 
            warn('Cannot load project defaults -- may not be able to resolve external dependencies')
            return

        (user, host, pathsep, reset, newpath, prepends, appends, showlist, useralii, hostalii, showalii) = dpathdata
        print >>DEBUGSTREAM, "ALIASES", useralii, hostalii
#fixme: uses aliases. call updateDpath from more places.
        print  >>DEBUGSTREAM, "UH_updateDpaths input", user, host
        (user, host) = self._processAlii(myproj, defaults, user, host, useralii, hostalii, showalii)
        # switch user, host to canonical values from alias system. usually identical
        print  >>DEBUGSTREAM, "UH_updateDpath from procesalii", user, host
        self.user = user
        self.host = host
        key="@".join((user,host,sidlname))
        path = None
        if myproj:
            path=myproj.getDefaultValueQuietly(key,'RepositoryPaths')
        if not path:
            path = ""
        if reset:
            path=newpath
        path = pathsep.join((prepends, path, appends))
        path=path.strip(pathsep)
        if myproj:
            myproj.setDefaultValue(key, path, 'RepositoryPaths')
        else:
            if not defaults.has_section('RepositoryPaths'): defaults.add_section('RepositoryPaths')
            defaults.set('RepositoryPaths', key, path)
        if myproj:
            for i in showlist:
                if i == None:
                    print key, "=", myproj.getDefaultValue(key,'RepositoryPaths')
                    continue
                if i == "":
                    print key, "=", myproj.getDefaultValue(key,'RepositoryPaths')
                    continue
                items = defaults.items('RepositoryPaths')
                for (name, val) in items:
                    if name.find(i) >=0 and name.endswith("@"+sidlname) :
                        print name,"=",val
        print  >>DEBUGSTREAM, "UH_updateDpaths######################### done"

    def _queryDpath(self, myproj, sidlname):
        """probably need to expand this, but for now @return tuple {BOOL, sidlfile, deplfile}
where the files have been checked for existence (but not correctness of sidl).
This should not be called before the vertex has its defaults loaded. It may be called
when no dpath options have been given.
BOOL will be true if resolved and false if not
"""
        print  >>DEBUGSTREAM, "UH_queryDpath", sidlname
        # these will be aliasresolved by the time this is called.
        host=self.host
        user=self.user
        # TODO override with dpath user and dpath host options if given.
        pathsep=':'
	resolved=False
	sidlfile="/undefined.sidl"
	deplfile="/undefined_depl.xml"
        if not myproj:
            return (resolved, sidlfile, deplfile)
        print  >>DEBUGSTREAM, "UH_queryDpath_Repo", self.repoAliased
        # lookup the dpaths associated with given symbol
        symkey="@".join((user,host,sidlname)) 
        projkey="@".join((user,host,""))
        path = None
        if self.repoAliased.has_key(symkey):
            sympath = self.repoAliased[symkey]
        else:
            sympath=""
        if self.repoAliased.has_key(projkey):
            projpath= self.repoAliased[projkey]
        else:
            projpath=""
        path = pathsep.join((sympath, projpath))
        path=path.strip(pathsep)
        print  >>DEBUGSTREAM, "_queryDpath got", path
        print  >>DEBUGSTREAM, "_queryDpath for keys", symkey, projkey
        
        # dig up the depl data for this vertex
        # this could be optimized to happen once and cache the index objects,
        # or perhaps someone with more clue will add graph nodes that don't
        # serialize.
        # rescanning xml dirs repeatedly might be kinda slow.
        args=[]
        if len(path) > 2:
            args.append("--dpath="+path)
        args.append("--debug")
        # args.append("--help")
        args.append(sidlname)
        print  >>DEBUGSTREAM, "args:", args
        from ccaxml2.CCAXMLQuery import CCAXMLQuery
        q = CCAXMLQuery()
        parser = q.initParser("called from bocca. no usage.")
        (qoptions, qargs) = parser.parse_args(args=args)
        print  >>DEBUGSTREAM, "args:",qargs
        print  >>DEBUGSTREAM, "opts:", qoptions

        err = q.load(qoptions, qargs)

        # query whatever we need.
        index = q.getIndex()
        symbol = index.getSymbol(sidlname)
        if not symbol:
            return (resolved, sidlfile, deplfile)
        sidlfile = symbol.getSidlFile()
        deplfile = symbol.getFilename()
        if sidlfile and deplfile:
            resolved = True
        # recursive data available includes many things(in package ccaxml2):
        # index.:
        #       findSymbolDependenciesLocations(self, sidlname, warn=False):
        #       findSymbolDependencies(self, sidlname, warn=False):
        #       findLinkFlags(self, sidlname, lang, linkage):
        #       findIncludeDirs(self, sidlname, lang):
        #       findSidlFileDependencies(self, sidlname):
        #       findAvailableBindings(self, sidlname, linkage, strict=False):
        # symbol.:
        #        getKind(self):
        #        getDependenceSymbols(self):
        #        getServerLib(self, linkage):
        #        getClientLib(self, lang, linkage):
        #        getClientSymbolPath(self, lang):

        #TODO: diagnostics based on near-misses in RepositoryPaths

# leftover from update : some of the iteration logic might be morphed to
# produce hints if the symbol isn't found under user@host@sym or user@host keys.
#       if myproj:
#           for i in showlist:
#               if i == None:
#                   print key, "=", myproj.getDefaultValue(key,'RepositoryPaths')
#                   continue
#               if i == "":
#                   print key, "=", myproj.getDefaultValue(key,'RepositoryPaths')
#                   continue
#               items = defaults.items('RepositoryPaths')
#               for (name, val) in items:
#                   if name.find(i) >=0 and name.endswith("@"+sidlname) :
#                       print name,"=",val
        print  >>DEBUGSTREAM, "_queryDpaths######################### done with"
        print  >>DEBUGSTREAM, (resolved, sidlfile, deplfile)
        return (resolved, sidlfile, deplfile)

    
    def _getExternalSIDLPath(self, sym):
        f = None
        files=None
        if not self.project:
            self.project, graph = Globals().getProjectAndGraph(projectName=self.projectName)
        defaults = self.project.getDefaults()
        if not defaults: warn('Cannot load project defaults -- may not be able to resolve external SIDL dependencies')
        if defaults.has_option('External',sym):
            files = defaults.get('External',sym)
        flist = []
        if files:
            for f in files.split(','):
                print >>DEBUGSTREAM, 'Checking external file: ' + f
                if not f or not os.path.exists(f):
                    warn('Could not find file path for external symbol ' + sym 
                         + ' in the project defaults External section. Use \n\tbocca config --set-var=External:' 
                         + sym + ' --val=/path/to/sidl/file\n to provide the location of the external SIDL file.')
                    if f: 
                        f = os.path.join(self.project.getDir(), 'external', 'sidl', os.path.basename(f))
                        warn('Using cached external SIDL file ' + f + ' (may be out of date).')
                if not f or not os.path.exists(f): 
                    err('Could not locate cached version of missing external SIDL file: ' + os.path.basename(f))
                
                flist.append(f)
            print >>DEBUGSTREAM, 'SIDL files for symbol ' + sym + ': ' + ','.join(flist)
            return ','.join(flist)
        else:
            return ''

    def _processSymbolAssociationOptions(self, optionval, optionstr='--extends/-e'):
        # --extends, --implements, --uses, --provides, --requires options processing
        # This is done for both create and change for interface, port, sidlclass, component
        parentSymbols = {}
        parentLocations = {}
        portInstanceList = []
        project, graph = Globals().getProjectAndGraph(projectName=self.projectName)
        if len(optionval) > 0:
            # Populate a dictionary of type names and optionally locations of extended types.
            for val in optionval:
                # Validate option string
                # Check for --
                if val.count("--") > 0:
                    self.usage(2,'invalid argument syntax (missing whitespace?) in ' + optionstr + ' option: %s' % val)

                (status,index) = cct._validate.validateSymbolOption(val)
                if  status != 0:
                    self.usage(2,'invalid option value substring for ' + optionstr + 'option: ' + val[index:len(val)])
                parentSymbolInfo = val.strip('"').strip()
                portname = ''
                filepath = '%local%'            
                # in-project is denoted %local%.
                # wired to external file is denoted with a fully qualified path name (nonportable).
                
                if parentSymbolInfo.count('@') > 0: separatorSymbol = '@'
                else: separatorSymbol = ':'
                
                separators = parentSymbolInfo.count(separatorSymbol)
                if separators > 0 and separatorSymbol == ':' :
                    warn('Use of : instead of @ for option field separators is deprecated: ' + parentSymbolInfo)
                
                # First of all, check for the presense of the symbol in the project
                sym = parentSymbolInfo.split(separatorSymbol)[0]
                slist = graph.findSymbol(sym)
                    
                if (separators > 1 and self.kind != 'component') or (separators > 2 and self.kind == 'component'):
                    self.usage(2,'invalid argument syntax in ' + optionstr + ' option: %s' % parentSymbolInfo)
            
                if separators == 2 and self.kind == 'component':
                    sidlname, portname, filepath = parentSymbolInfo.split(separatorSymbol)
                    if len(slist) == 1: filepath = '%local%'  # local symbol
                elif separators == 1:
                    if self.kind == 'component'  and (optionstr == '--uses/-u' or optionstr == '--provides/-p'):
                        # could be porttype:sidlfile or porttype:portname
                        sidlname, t2 = parentSymbolInfo.split(separatorSymbol)
                        if t2.lower().endswith('.sidl') or t2.lower().endswith('.xml') or t2.count(os.path.sep)>0:
                            if len(slist) == 1: filepath = '%local%'  # local symbol
                            else: filepath = t2
                        else:
                            portname = t2
                    else:
                        # sidl type and path to sidl or xml file
                        sidlname, filepath = parentSymbolInfo.split(separatorSymbol)
                        if len(slist) == 1: filepath = '%local%'
                elif separators == 0:
                    sidlname = parentSymbolInfo
                elif parentSymbolInfo.startswith('gov.cca'):
                    parentSymbols[parentSymbolInfo] = Globals().getCCAVars(projectName=self.projectName)['CCA_sidl']
                    filepath = parentSymbols[parentSymbolInfo]
                elif parentSymbolInfo.startswith('sidl.'):
                    # FIXME : when babel has a _sidl babel-config variable, use that
                    parentSymbols[parentSymbolInfo] = os.path.join(Globals().getCCAVars(projectName=self.projectName)['CCASPEC_BABEL_jardir'],'sidl.sidl')
                    filepath = parentSymbols[parentSymbolInfo]
                    
                                    
                if sidlname.count(',') > 0:
                    sidlnames = sidlname.strip('"').strip("'").split(',')
                else:
                    sidlnames = [sidlname]
                    
                # Check whether specified file exists
                # TODO: generalize this to handle URLs in addition to local files
                if filepath != '%local%':
                    for f in filepath.split(','):
                        if (not os.path.exists(f) or not os.path.isfile(f)):
                            self.usage(2,'Invalid path in ' + optionstr + ' option argument: ' + f)
                        elif not (f.lower().endswith('.sidl') or f.lower().endswith('.xml')):
                            # TODO: some more intelligent check (rather than just suffixes)    
                            # this should go in _utils.py, e.g., as a validateSIDLFile, validateXMLFile
                            self.usage(2,'File specified with ' + optionstr + ' option argument must be a valid SIDL or XML file: %s'%f)

                    # Store in project defaults.
                    defaults = project.getDefaults()

                    if defaults:
                        for sidlname in sidlnames:
                            if defaults.has_option('External',sidlname):
                                extfile = defaults.get('External',sidlname)
                                if extfile:
                                    # Check whether existing file is the same as the current one, print a warning if not
                                    if extfile != filepath:
                                        warn('Existing path for external symbol ' + sidlname + ' in ' + project.getDefaultsFilePath() + ' does not match the specified path: ' + extfile)
                            else:
                                project.setDefaultValue(sidlname, filepath, 'External')
                                #project.saveDefaults()
                                # Create a local copy (TODO -- move location in location manager)
                                for f in filepath.split(','):
                                    localpath = os.path.join(project.getDir(), 'external','sidl', os.path.basename(f))
                                    if os.path.exists(localpath): 
                                        osum= md5file(localpath)
                                        nsum= md5file(f)
                                        if nsum != osum:
                                            warn('Overwriting local copy of ' + f)
                                        else:
                                            print >> DEBUGSTREAM, "overwriting identical copy of " + f
                                        BFileManager().rm(localpath)
                                    BFileManager().copyfile(f, localpath, nobackup=True)

                for sidlname in sidlnames:
                    if filepath == '%local%' and (not (sidlname.startswith('gov.cca') or sidlname.startswith('sidl.'))): 
                        # Get fully qualified symbol name
                        # Try port first
                        vlist = graph.findSymbol(sidlname, kind='any')
                        if not vlist: 
                            print  >>DEBUGSTREAM, sidlname,"unknown, unless we figure out what to do with _queryDpath, which says:"
                            self._queryDpath(project, sidlname)
                            err('could not find specified symbol in the current project: ' + sidlname)
                        elif len(vlist) > 1:
                            err('the specified symbol, ' + sidlname + ', is ambiguous. Please use a fully qualified SIDL name.')
                        else:
                            sidlname = vlist[0].symbol
                            
                    if self.kind == 'component' and (optionstr == '--uses/-u' or optionstr == '--provides/-p'):
                        if not portname: portname = sidlname.split('.')[-1]
                        p = PortInstance(typename=sidlname, name=portname, location=filepath)
                        portInstanceList.append(p)
                    else:
                        parentLocations[sidlname] = filepath

        print >> DEBUGSTREAM, "Optionstr = ", optionstr
        if self.kind == 'component' and (optionstr == '--uses/-u' or optionstr == '--provides/-p'):
            return portInstanceList   # List of PortInstance objects
        else:
            return parentLocations    # Dictionary of locations indexed by sidl type
    
    def _validateProjectSymbols(self, graph, symbols, portnames={}, kinds=['interface','port']):
        '''Private method: look for a list of symbols in a graph and return a list with their fully qualified SIDL symbols.
        @param symbols a dictionary whose keys are the sidl symbols to search for '''
        newdict = {}
        vertexlist = []
        project, graph = Globals().getProjectAndGraph(projectName=self.projectName)
        for i in symbols.keys():

            # Check whether this interface is in the current project and if not, 
            # require the filename defining it (except for things in gov.cca namespace).
            ilist = []
            for kind in kinds:
                ilist += graph.findSymbol(i,kind) 
                
            if i.startswith('gov.cca.') or i.startswith('sidl.'):
                print >> DEBUGSTREAM, 'Extending a standard interface: ' + str(i)
                newdict[i] = symbols[i]
                # Find the vertex in the graph (if it exists) and create one if not;
                # For now we assume everything in gov.cca (that can be extended or implemented)
                # is an interface. 
                # TODO: This should be replaced by a real graph representation
                # produced by parsing cca.sidl
                # or eliminated by a full and proper handling of external dependencies
                tmpvlist = graph.findSymbol(i)
                if len(tmpvlist) > 1:
                    err('The project contains multiple matches for the SIDL symbol ' + i + '.\n'
                        +'Please make sure that you use the fully-qualified SIDL name.')
                elif len(tmpvlist) == 1:
                    vertexlist.append(tmpvlist[0])
                else: 
                    from cct import interface
                    specversion = Globals().getCCAVars(projectName=project.getName())['CCASPEC_VERSION']
                    iface = interface.Interface(action='create', symbol=i, version=specversion,
                                                project=project, modulePath=self.modulePath, graph=graph)
                    vertexlist.append(iface)
                
                continue

            if len(ilist) > 1:
                err('Multiple matching symbols found, please use a fully qualified SIDL symbol in the --extends  or --implements options')
            elif len(ilist) == 1:
                newdict[ilist[0].symbol] = symbols[i]
                vertexlist.append(ilist[0])
            elif symbols[i] != '%local%':
                filesok=True
                for f in symbols[i].split(','):
                    if not os.path.exists(f):
                        filesok=False
                if filesok:
                    newdict[i] = '%external%'
                    self._b_externalSidlFiles[i] = '%external%'   # no longer stores the actual file path -- this is now in projName.defaults
                    defaults = project.getDefaults()
                    if not defaults: err('Cannot load project defaults -- cannot store external SIDL dependencies')
                    defaults.set('External', i, symbols[i])
                    print >>DEBUGSTREAM, 'Adding external SIDL file for ' + i + ': ' + symbols[i]
                else:
                    err('The SIDL symbol ' + i + ' was not found in the current project.\n'
                        + 'It must be added to the project before it can be extended or implemented,'
                        + ' or the location of the external SIDL or XML file defining it must be specified, '
                        + 'for example, --extends=sidltype@/path/to/file.sidl or --provides=portname@porttype@/path/to/file.sidl, etc.')

        return newdict, vertexlist

    
    def _defineDependencyArgs(self):
        '''For dependencies other than extension and implementation.'''
        self.parser.add_option('--requires', dest='required_symbol', action='append', 
                               help='A SIDL symbol or a comma-separated list of SIDL symbols on which the ' 
                               + self.kind + ' depends (other than through extension or implementation, for example, '
                               + 'a symbol used as the type of one of the arguments in a method in the ' + self.kind + '.' 
                               + 'If the symbol is not in this project, a SIDL file name should be given, e.g., '
                               + '--requires=sidltype@/path/to/file.sidl.')
        
        self.parser.add_option('--remove-requires', dest='symbol_to_remove', action='append', 
                               help='Remove the dependency on the specified SIDL symbol or SIDL file (or a comma-separated list of symbols). '
                               + 'This affects only dependencies other than extension or implementation, for example, '
                               + 'a symbol used as the type of one of the arguments in a method in the ' + self.kind + '.')
        self.parser.set_defaults(required_symbol=[], symbol_to_remove=[])
        return
        
    def _processDependencyArgs(self):
        # Dependencies on other SIDL symbols within the project
        if self.options.required_symbol:
            self.deps = self._processSymbolAssociationOptions(self.options.required_symbol, '--requires')
            print >>DEBUGSTREAM, 'adding dependencies on the following project symbols: ' + str(self.deps)

        # Dependencies on other SIDL symbols within the project to remove
        if self.options.symbol_to_remove:
            self.rmdeps = []
            for s in self.options.symbol_to_remove:
                if s.count(',') > 0:
                    self.rmdeps.extend(s.split(','))
                else:
                    self.rmdeps.append(s)
            print >>DEBUGSTREAM, 'removing dependencies on the following project symbols: ' + str(self.rmdeps)
            
        return
      
    def _processImportArgs(self):
        sidlimports = {}
        for val in self.options.sidlimports:
            f = val.strip('"').strip()
            symbolList = []
            if f.count('@') > 0: separatorSymbol='@'
            else: separatorSymbol = ':'
            if f.count(separatorSymbol) == 1:
                symbols, fname = f.split(separatorSymbol)
                if symbols:
                    symbolList = []
                    for s in symbols.split(','):
                        symbolList.append(s.strip())
            elif f.count(separatorSymbol) > 1:
                err('incorrect syntax in import option, see "bocca help %s %s"' % (self.action,self.kind))
            else:
                fname = f
                symbolList = ['%all']
            if not os.path.exists(fname):
                err('could not find SIDL import file: ' + fname)
            
            sidlimports[fname] = symbolList
        self.setSIDLImports(sidlimports)
        pass
    
    def _indentComment(self,indentstr, comment,prependNewline=False):
        lst = comment.strip().split('\n')
        lst[0] = indentstr + lst[0] + '\n'
        if prependNewline: lst[0] = '\n' + lst[0]
        if len(lst) == 1: return lst[0]
        newcomment = lst[0]
        for l in lst[1:]:
            newcomment += indentstr + l + '\n'
        return newcomment
    
    def __getstate__(self):
        '''Need to break cycles to prevent recursion blowup in pickle.
        
        Dump everything except for edges.'''
        dcp = self.__dict__
        dcp['e'] = [] 
        #print 'BVertex __getstate__ called', dcp
        return dcp
    

    def _findExternal(self, ptype):
        project = Globals().getProject(self.projectName)
        allclasses = project.getVertexList(kinds=['component','class'])
        for v in allclasses:
            if v.symbol != self.symbol:
                if ptype in v._b_implements.keys(): 
                    return True
                if v.kind == 'component' and (ptype in [x.getType() for x in v._b_uses] + [y.getType() for y in v._b_provides]):
                    return True
        return False

    pass
    
        
    # ------------------ End of BVertex class ---------------------------
    
class BEdge(DirEdge):

    def __init__(self, v1, v2, graph=None, action='', name=None):
        if name is None:
            # generate as unique a name as possible
            name = v1.name + ':' + v2.name
        self.name = name
        print >>DEBUGSTREAM, "Creating edge from %s to %s" % (v1.name,v2.name)
        DirEdge.__init__(self, name, v1, v2)
        self.action = action

        if graph != None:
            if v1.name not in graph.v.keys(): graph.add_v(v1)
            if v2.name not in graph.v.keys(): graph.add_v(v2)
            if self.name not in graph.e.keys(): graph.add_e(self)

        pass
            
    def __str__(self):
        return '%s -> %s [%s]' % (str(self.v[0]), str(self.v[1]), self.action)

    def _savePickle(self,filedesc,protocol=2):
        '''Given a filed escriptor of an open pickle file, 
        save everything necessary to recreate this vertex, omitting
        the edge list to avoid recursion.'''
        pickle.dump(self.v[0].name, filedesc, protocol)
        pickle.dump(self.v[1].name, filedesc, protocol)
        pickle.dump(self.name, filedesc, protocol)
        pickle.dump(self.action, filedesc, protocol)
        # Only save the unique vertex names to avoid saving the same vertex multiple times
        return
    
    def serializeASCII(self):
        '''Serialize the edge in a portable ASCII way.
        '''
        buf = '!edge\n'
        buf += 'name=%s|srcvertex=%s|destvertex=%s|action=%s\n' % (self.name, self.v[0].name, self.v[1].name, self.action)
        return buf
    
    def deserializeASCII(self, thestring):
        # This method is not used at the moment -- the logic is in the BGraph deserializeASCII method
        namevalpairs = thestring.strip().split('|')
        if len(namevalpairs) != 4:
            err('BEdge: the serialized string contains fewer items than expected.')
        for v in namevalpairs:
            key,val = v.split('=')
            if key == 'name': name = val
            if key == 'srcvertex': self.v[0].name = val
            if key == 'destvertex': self.v[1].name = val
            if key == 'action': self.action = val
        return 0
    deserializeASCII = staticmethod(deserializeASCII)
    
    pass
    # ---------------------- end of class BEdge ----------------------
   
class BGraph(Graph):
    '''This class is for directed graphs with vertices of arbitrary type'''
    def __init__(self, name = None, path = None, modulePath = None):
        '''Create a graph'''
        Graph.__init__(self, name)
        self.path = path
        self.modulePath = modulePath
        self.defaults = None
        
        # This is simply a convenience field, so we don't have to hunt 
        # down the project vertex every time. The project field is not 
        # (and never should be) pickled.
        self.project = None 
        return

    def _loadVertexClass(self, vclassName, modulePath):
        vclassModuleName = vclassName[0:vclassName.rfind('.')]
        vclassName = vclassName[vclassName.rfind('.') + 1:len(vclassName)]
        (file, filename, description) = imp.find_module(vclassModuleName, [modulePath])
        mod = imp.load_module(vclassModuleName, file, filename, description)
        vclass = getattr(mod, vclassName)
        v = vclass(symbol='temp')
        return v

#    def __str__(self):
#        return 'DirectedGraph with '+str(len(self.vertices))+' vertices and '+str(reduce(lambda k,l: k+l, [len(edgeList) for edgeList in self.inEdges.values()], 0))+' edges'

    def save(self, saveASCII=True, filename=None, startvertex=None, compressed=False):
        '''Save graph to a file.'''
        
        self.saveASCII(filename)
        
        return 0
    
    def load(self, modulePath, filename=None, compressed=False):
        '''Load graph from a binary file, optionally in BZ2 compressed format'''
        if modulePath and os.path.exists(modulePath): 
            self.modulePath = modulePath
        else:
            print >>sys.stderr, 'Bocca ERROR: invalid module path, cannot load Bocca modules: ' + str(modulePath)
            sys.exit(1)
        if filename is None: 
            filename = os.path.join(self.path, '.bocca', self.name+'.pickle')
        try:
            fileSize = os.stat(filename)[stat.ST_SIZE]
        except os.error:
            fileSize=0
            print >>DEBUGSTREAM, "encountered 0-size pickle file"
            return 1
        self.clear()
        if fileSize > 0:
            if compressed:
                fin = BZ2File(filename, "r")
            else:
                fin = open(filename, "r")
            self.name = pickle.load(fin)
            print >>DEBUGSTREAM, 'loading graph ' + self.name + ' from pickle file.'
            projname, mypath = getProjectInfo(self.name)
            if mypath and os.path.exists(mypath): 
                self.path = mypath
            else: 
                print >>sys.stderr, 'Bocca ERROR: invalid project path, bocca commands must be executed inside a Bocca project.'
                sys.exit(1)
            # Number of vertices
            nv = pickle.load(fin)
            print >>DEBUGSTREAM, 'about to load ' + str(nv) + ' vertices.'
            # Unpickle and recreate all vertices, instantiating the appropriate vertex class
            for i in range(0,nv):
                # This entire nastiness is needed because pickle chokes when dumping vertex subclasses
                vclassName = pickle.load(fin)
                print >>DEBUGSTREAM, 'vertex class is ' + vclassName
                v = self._loadVertexClass(vclassName, modulePath)
                print >>DEBUGSTREAM, 'loaded vertex class ' 
                v = v._loadPickle(fin)
                print >>DEBUGSTREAM, 'Loaded vertex', v
                try:
                    self.add_v(v)
                except:
                    #warn('vertex already exists: ' + str(v))
                    pass
            # Now unpickle the edges. Currently only BEdge type is supported, but if eventual
            # subclasses need to be pickled, the same approach as for the vertices can be used
            ne = pickle.load(fin)
            for i in range(0,ne):
                v1name = pickle.load(fin)
                v2name = pickle.load(fin)
                edgeName = pickle.load(fin)
                edgeAction = pickle.load(fin)
                self.add_e(BEdge(v1=self.v[v1name], v2=self.v[v2name], action=edgeAction, name=edgeName))
            fin.close()
        return 0
    
    def saveASCII(self, filename = None):
        '''Save project state using an ASCII representation that is suitable for
        including in Makefiles and shell scripts'''
        if filename is None: 
            filename = os.path.join(self.path, 'BOCCA', self.name+'.dat')
        fout = fileManager.open(filename, "w")
        buf = '!graph=' + str(self.name) + '\n'
        buf += '!bocca_version=' + str(bocca_version) + '\n'
        for v in self.v.values():
            buf += v.serializeASCII()
        for e in self.e.values():
            buf += e.serializeASCII()
        buf += '\n'
        #print buf
        fout.write(buf)
        fout.close()
        return
    
    def loadASCII(self, modulePath, filename=None, action='__init__'):
        if filename is None: 
            filename = os.path.join(self.path, 'BOCCA', self.name+'.dat')
            print >>DEBUGSTREAM, 'Trying to load project information from ' + filename
        try:
            fileSize = os.stat(filename)[stat.ST_SIZE]
        except os.error:
            fileSize=0
            print >>DEBUGSTREAM, 'Project info file ' + filename + ' is empty.'
            return 1
        
        if modulePath and os.path.exists(modulePath): 
            self.modulePath = modulePath
        else:
            print >>sys.stderr, 'Bocca ERROR: invalid module path, cannot load Bocca modules: ' + str(modulePath)
            sys.exit(1)

        self.clear()
        
        if fileSize <= 0: 
            err('Could not load ASCII project information, file was empty: ' + filename)
        
        try:
            fin = open(filename, "r")
        except:
            err('Could not load ASCII project information from file: ' + filename)
            
        lines = fin.readlines()
        numlines = len(lines)
        boccaVersion = ''
        i = 0
        while i < numlines:
            val = ''
            if lines[i].startswith('!graph'):
                section, val = lines[i].split('=')
                self.name = val.strip()
                projname, mypath = getProjectInfo(self.name)
                if mypath: self.path = mypath
                else: 
                    print >>sys.stderr, 'Bocca ERROR: invalid project path, bocca commands must be executed inside a Bocca project.'
                    sys.exit(1)
                self.modulePath = self.modulePath.strip()
                modulePath = os.path.join(self.modulePath,'cct')
            elif lines[i].startswith('!bocca_version'):
                section, val = lines[i].split('=')
                boccaVersion = val.strip()
                # Check whether development version
            elif lines[i].startswith('!vertex'):
                if not boccaVersion: boccaVersion = '0.4.0'    # The only bocca release that doesn't record its version
                if not cct._validate.boccaVersion(boccaVersion):
                    print >>sys.stderr, 'Bocca ERROR: this version of Bocca (%s) is not compatible with the version used to create this project (%s).' % (bocca_version, boccaVersion)
                    sys.exit(1)
                vclassName = lines[i].split('=')[1].strip()
                v = self._loadVertexClass(vclassName, modulePath)
                i += 1
                #print 'current line: ' + lines[i]
                v.deserializeASCII(lines[i], boccaVersion,action)
                #print >>DEBUGSTREAM,'Deserialized vertex %s: '%v.symbol, v.serializeASCII()
                try:
                    self.add_v(v)
                except:
                    #warn('vertex already exists: ' + str(v))
                    pass
            elif lines[i].startswith('!edge'):
                i += 1
                namevalpairs = lines[i].strip().split('|')
                if len(namevalpairs) != 4:
                    err('BEdge: the serialized string contains fewer items than expected.')
                for v in namevalpairs:
                    key,val = v.split('=')
                    if key == 'name': edgeName = val
                    if key == 'srcvertex': v1name = val
                    if key == 'destvertex': v2name = val
                    if key == 'action': edgeAction = val
                # Recreate the edge (this also adds it to the graph)
                e = BEdge(v1=self.v[v1name], v2=self.v[v2name], graph=self, action=edgeAction, name=edgeName)

            i+= 1

        return 0
    
    def saveGraphvizFile(self, filename=None):
#        if filename is None: filename = str(self.name) + '.dot'
        pname, pdir = getProjectInfo(self.name)
        if filename is None: 
            filename = os.path.join(pdir, 'BOCCA','graphics',pname+'.dot')
        if not os.path.exists(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        fout = open(str(filename), "w")
        fout.write("digraph " + str(self.name) + " {")
        fout.write('\norientation=portrait; rankdir=LR;')
        fout.write('\nnode [ color=black\n style=filled\n fontname="Palatino"\n fontsize=12\n' +
                'shape = box\n color=lightgrey];\n')
        fout.write('edge [color=black, style=solid];\n')
        # TODO: makes this use one of the spanning tree algs instead of listing everything
        from graphlib.graph import bn_sorted
        for v in bn_sorted(self.v):
            fout.write(v._graphviz())
        for e in bn_sorted(self.e):
            fout.write('"' + e.v[0].name + '" -> "' + e.v[1].name + '"' + ' [color=cornflowerblue, label="' + str(e.action) + '", font="Palatino" fontsize=10, fontcolor=navyblue];\n')
        fout.write('label = "\\n\\nProject ' + str(self.name) + ' Diagram\\n";\n')
        fout.write('label = "Created with GraphViz by Bocca";\n')
        fout.write('fontsize=14;\n')            
        fout.write("}\n")
        fout.close()
        return
    
    def removeVertex(self, vertex):
        '''Delete all edges connected to the vertex, along with the vertex.'''
        for v in vertex.in_v:
            outedges = v.out_e
            for edge in outedges:
                if edge.v[1] == vertex: v.e.remove(edge)
        for edge in vertex.all_e:
            try: del self.e[edge.name]
            except: pass
        del self.v[vertex.name]
        return
    
    def removeEdge(self, edge):
        '''Remove edge from vertices to which it is attached.'''
        del self.e[edge.name]
        
    def addSubgraph(self, graph):
        '''Add the vertices and edges of another graph into this one'''
        map(self.add_v, graph.v)
        map(lambda v: apply(self.add_e, (v,) + v.all_e()), graph.v)
        return

    def removeSubgraph(self, graph):
        '''Remove the vertices and edges of a subgraph, and all the edges connected to it'''
        map(self.removeVertex, graph.v)
        return

    # Query interface
    def containsSIDLSymbol(self, symbol, version='0.0'):
        ''' Returns True if the fully qualified SIDL symbol name is present in the graph (regardless
        of the kind of vertex), False otherwise. At present the version argument is not considered 
        in the comparisons.'''
        for key in self.v.keys():
            (k,sym,ver) = key.split('@')
            if sym == symbol:
                return True, self.v[key]
        return False, None
        
    def findSymbol(self, symbol, kind='any', version=None):
        '''Returns a list containing exactly one vertex if the fully qualified SIDL symbol 
        is in the graph, or a list of vertices that are partial matches to a non-fully
        qualified SIDL symbol, otherwise returns None. If a short (not fully qualified) 
        symbol name is given, returns the corresponding vertex if no ambiguity is found, 
        and raises a SymbolError otherwise.
        '''
        found = []            
        sym = str(kind) + '@' + str(symbol)
        if version: sym += '@' + str(version)
        print >>DEBUGSTREAM, 'findSymbol ' + sym

        for key in self.v.keys():
        
            if sym == key:         # fully-qualified symbol given, including version number
                if not self.v[key].project: self.v[key].project = self.project
                return [self.v[key]]
            else:
                # This may be a partly qualified or a short symbol name (e.g., no version)
                for key in self.v.keys():
                    (k, sym, ver) = key.split('@')
    
                    # compare symbols
                    if sym.endswith(str(symbol)) and (k == str(kind) or str(kind) == 'any') and (ver == version or version is None):
                        if not self.v[key].project: self.v[key].project = self.project
                        dots = symbol.count('.')
                        symdots = sym.count('.')
                        if dots > 0 and symdots >= dots and symbol == '.'.join(sym.split('.')[symdots-dots:]):
                            #print '1. symbols ' + sym + ' and ' + symbol + ' match.'
                            found.append(self.v[key])
                        elif sym.split('.')[-1] == symbol:
                            found.append(self.v[key])
                            #print '2. symbols ' + sym + ' and ' + symbol + ' match.'

                if found: return found
        return found
        
    def renameVertex(self, vertex, newname):
        '''Rename a vertex and update all edges.'''
        
        if not vertex.name in self.v.keys():
            raise SymbolError(vertex.symbol, 'Symbol not found: ')
        # change vertex
        vertex.changeSymbol(newname)
        return
    
    def filter_copy(self, filterEdgesWithAction=None):
        newgraph = BGraph(self.name, self.path, self.modulePath)
        newgraph.v = VertexDict(newgraph)
        newgraph.e = EdgeDict()
        for k in self.v.keys():
            newgraph.v[k] = self.v[k].clone()
            newgraph.v[k].symbol = self.v[k].symbol
            newgraph.v[k].kind = self.v[k].kind
            newgraph.v[k].name = self.v[k].name
            newgraph.v[k].e = []
        for k in self.e.keys():
            v0 = newgraph.findSymbol(self.e[k].v[0],kind=self.e[k].v[0].kind)[0]
            v1 = newgraph.findSymbol(self.e[k].v[1],kind=self.e[k].v[1].kind)[0]
            newgraph.e[k] = BEdge(v0,v1,newgraph,action=self.e[k].action)

        if filterEdgesWithAction:
            found_ignore_action = False
            found_other_action = False
            for v in newgraph.v:
                for e in v.in_e:
                    if e.action == filterEdgesWithAction: found_ignore_action = True
                    else: found_other_action = True
                if found_ignore_action and found_other_action:
                    for e in v.in_e:
                        if e.action == filterEdgesWithAction:
                            newgraph.removeEdge(e)
        return newgraph
    
    def find_cycles(self):
        '''Return a depth-first search list of cycles, covering the full graph.
        A cycle is represented as a Set of one or more vertices. Only SIDL
        symbol kinds that can be units of compilation are included in the cycles
        (i.e., not project or package nodes).
        
        Each cycle is represented as a Set of Vertices.'''
        unprocessed = [self.project]
        visited = []
        cycle_candidates = Set()
        cycles = []       # A list of Sets
        cycleset = Set()  # A flat set to keep track of vertices that have 
                          # been identified as being in cycles
                          
                          
        print >>DEBUGSTREAM, "Entering boccagrpah.py: find_cycles()"
        while unprocessed:
            v = unprocessed.pop()
            if v not in visited:
                visited.append(v) 
                if v.kind in ['interface','class','port','component','enum']:    
                    cycle_candidates.add(v)

                if v.out_v: unprocessed.extend(v.out_v)

            if v in visited:
                # This could be a cycle
                # First, check whether this vertex is already present in another cycle
                
                #if v in [x for y in cycles for x in y]:

                if v in cycle_candidates:
                    #print '\n\n********* vertex in cycle candidates:', v.symbol
                    if v in cycleset:
                        # extend the existing cycle
                        for ind in range(0,len(cycles)):
                            if v in cycles[ind] and cycle_candidates:
                                # Expand cycles[ind] with current cycle
                                for c in cycle_candidates:
                                    cycles[ind].add(c)
                            
                                cycle_candidates = Set()
                                break
                    else:
                        # Figure out which vertices are in a cycle
                        cycle_candidates_copy = Set(cycle_candidates)
                        for w in cycle_candidates_copy:
                            incycle = False
                            for outvertex in w.out_v:
                                if outvertex in cycle_candidates:
                                    for invertex in w.in_v:
                                        # Thie vertex is in the cycle
                                        if invertex in cycle_candidates:
                                            incycle = True
                            if not incycle:
                                # Create a 1-vertex cycle (since we want full coverage)
                                #print '\n\n******* Creating 1-vertex cycle:', w.symbol
                                s = Set()
                                s.add(w)
                                cycles.append(s)                     
                                cycleset.add(w)  
                                cycle_candidates.remove(w)
                                
                        # A brand-new cycle has been detected, store it
                        if cycle_candidates:
                            cycles.append(cycle_candidates)
                            for t in cycle_candidates: cycleset.add(t)
                        cycle_candidates = Set()
                else:
                    # Create a 1-vertex cycle (since we want full coverage)
                    #print '\n\n****** Creating 1-vertex cycle:', v.symbol
                    s = Set()
                    s.add(v)
                    cycles.append(s)                     
                    cycleset.add(v)
                
        #for s in cycles:
        #    print 'Cycle: ', [v.symbol for v in s]
        
        return cycles
    
    #@staticmethod
    def bocca_breadth_first_search(start_v, reverse=False, actions=[]):
        '''
        Returns a breadth-first search list of vertices connected by edges of edgetype. Note that 
        this is less general than the graphlib graph breadth_first_search method used in 
        the BVertex dependents() and dependencies() methods.

        @param start_v the initial vertex
        @param reverse the order of the search
        @param edgetype a list of edge types to consider (the possible types are "extends", "implements", "requires", "contains")
        '''
        unprocessed = [start_v]
        visited = []
        while unprocessed:
            v = unprocessed.pop(0)
            if v not in visited:
                visited.append(v)
                if reverse: 
                    elist = []
                    for e in v.in_e:
                        if e.action in actions: elist.extend(e.src_v)
                    if elist: unprocessed.extend(elist)
                else: 
                    elist = []
                    for e in v.out_e:
                        if e.action in actions: elist.extend(e.dest_v)
                    if elist: unprocessed.extend(elist)
        return visited
    bocca_breadth_first_search = staticmethod(bocca_breadth_first_search)


    #@staticmethod
    def bocca_depth_first_search(start_v, visitor = None, reverse=False, actions=[]):
        '''
        Returns a depth-first search list of vertices connected by edges of edgetype. Note that 
        this is less general than the graphlib graph depth_first_search method.

        @param start_v the initial vertex
        @param visitor a flag indicating whether the visit() method should be called on the vertex.
        @param reverse the order of the search
        @param edgetype a list of edge types to consider (the possible types are "extends", "implements", "requires", "contains")
        '''
        unprocessed = [start_v]
        visited = []
        while unprocessed:
            v = unprocessed.pop(0)
            if v not in visited:
                if visitor:
                    v.visitor()
                visited.append(v)
                if reverse: 
                    elist = []
                    #print str(v)
                    for e in v.in_e:
                        if e.action in actions: elist.extend(e.src_v)
                    if elist: unprocessed.extend(elist)
                else: 
                    elist = []
                    for e in v.out_e:
                        if e.action in actions: elist.extend(e.dest_v)
                    if elist: unprocessed.extend(elist)
        return visited
    bocca_depth_first_search = staticmethod(bocca_depth_first_search)
    
    # ------------- End of class BoccaGraph ----------------

#-------------------- Exception classes ---------------------------------
class SymbolError(Exception):
    '''Error to use when symbol cannot be found or is ambiguous'''
    def __init__(self, symbol=None, msg=''):
        self.symbol = symbol
        self.msg = msg
            
    def __str__(self):
        return self.msg + repr(self.symbol)
        

