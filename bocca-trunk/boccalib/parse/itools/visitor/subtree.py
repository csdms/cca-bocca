from parse.itools.elements import *
from parse.itools.visitor.depthfirstvisitor import *
from cct._util import Globals
from cct._err import err
from cct._debug import DEBUGSTREAM
import cct.interface, cct.port, cct.sidlclass, cct.component, cct.package, cct.enum
from graph.boccagraph import BEdge

class SubtreeImporter(DepthFirstVisitor):
    '''
    Return a subset of the AST as a list of all nodes at the requested level (package, interface, class, method).
    '''

    def __init__(self, symbollist, parentVertex, projectName=''):
        self.symbols = symbollist
        if '%all' in self.symbols: self.doAll = True
        else: self.doAll = False
        self.parentVertex = parentVertex   # The BVertex that invoked this visitor
        self.project, self.graph = Globals().getProjectAndGraph(projectName=projectName)
        self.methods = {}                # dictionary of method AST nodes indexed by BVertex symbol string
        self.interfaces = {}             # dictionary of cct.interface.Interface instances indexed by AST vertex ID
        self.enums = {}                  # dictionary of cct.enum.Enum instanaces indexed by AST vertex ID
        self.classes = {}                # dictionary of cct.sidlclass.Sidlclass instances indexed by AST vertex ID
        self.packages = {}               # dictionary of cct.package.Package instances indexed by AST vertex ID
        DepthFirstVisitor.__init__(self)

    def getMethods(self):
        return self.methods
    
    def getInterfaces(self):
        return self.interfaces
    
    def getEnums(self):
        return self.enums
    
    def getClasses(self):
        return self.classes
    
    def getPackages(self):
        return self.packages
    
    def visitPackage(self,node):
        parentid = ''
        if self.parentVertex.kind in['project','package']:   # The BVertex that invoked this visitor
            parent = node.getParent()
            if parent: parentid = parent.getFullIdentifier()        
            id = node.getFullIdentifier()
        if parentid:
            if self.matchPartialSymbols(id, self.symbols) or self.doAll:
                shortId = node.getIdentifier()
                if parentid in self.packages.keys():
                    pVertex = self.packages[parentid]
                else:
                    pVertex = self.parentVertex
                if self.parentVertex.kind == 'package':
                    newId = pVertex.symbol + '.' + shortId
                elif self.parentVertex.kind == 'project': 
                    newId = id
                else:
                    newId = shortId
                slist = self.graph.findSymbol(newId,kind='any')
                if len(slist) == 1 and slist[0].kind == 'package':
                    package = slist[0]
                    package.setASTNode(node)
                elif not slist:
                    package = cct.package.Package(action='create', args=[newId], version=node.getVersion(), project=self.project, 
                                                  modulePath=self.project.modulePath)
                    package.setASTNode(node)
                    package.create()
                    comment = node.getStartComment()
                    if comment: package.setComment(comment)
                else:
                    self._symbolConflictError(slist)
                edge = BEdge(pVertex, package, self.graph, action='contains')
                self.packages[id] = package

        self.visitVertex(node)
        pass
    
    def visitInterface(self,node):
        if self.parentVertex.kind in ['package','project']:
            parentid = node.getParent().getFullIdentifier()
            id = node.getFullIdentifier()
            if self.matchPartialSymbols(id, self.symbols) or self.doAll:
                shortId = node.getIdentifier()
                if parentid in self.packages.keys():
                    pVertex = self.packages[parentid]
                else:
                    if self.parentVertex.kind not in ['project','package']:
                        err('Interfaces can only be imported into Bocca packages')
                    pVertex = self.parentVertex
                    
                newId = pVertex.symbol + '.' + shortId
                if self.parentVertex.kind == 'project': 
                    newId = id
                slist = self.graph.findSymbol(newId,kind='any')
                if len(slist) == 1 and slist[0].kind in ['interface','port']:
                    interface = slist[0]
                    interface.setASTNode(node)
                elif not slist:    
                    if 'gov.cca.Port' in node.getParentIds():
                        interface = cct.port.Port(action='create', args=[newId], version=pVertex.version, project=self.project, 
                                                  modulePath=self.project.modulePath, graph=self.graph)
                    else:
                        interface = cct.interface.Interface(action='create', args=[newId], version=pVertex.version, project=self.project, 
                                                            modulePath=self.project.modulePath, graph=self.graph)
                    
                    interface.setASTNode(node)
                    interface.create()
                    comment = node.getStartComment()
                    if comment: interface.setComment(comment)
                    self.methods[newId]=[]
                else:
                    self._symbolConflictError(slist)
                edge = BEdge(pVertex, interface, self.graph, action='contains')
                self.interfaces[id] = interface

        self.visitVertex(node)
        pass
    
    def visitClass(self,node):
        if self.parentVertex.kind in ['package','project']:
            parentid = node.getParent().getFullIdentifier()
            id = node.getFullIdentifier()
            if self.matchPartialSymbols(id, self.symbols) or self.doAll:
                shortId = node.getIdentifier()
                if parentid in self.packages.keys():
                    pVertex = self.packages[parentid]
                else:
                    if self.parentVertex.kind not in ['project','package']:
                        err('Classes can only be imported into Bocca packages')
                    pVertex = self.parentVertex
    
                newId = pVertex.symbol + '.' + shortId
                if self.parentVertex.kind == 'project': 
                    newId = id
                slist = self.graph.findSymbol(newId,kind='any')
                if len(slist) == 1 and slist[0].kind in ['class','component']:
                    klass = slist[0]
                    klass.setASTNode(node)
                elif not slist:
                    if 'gov.cca.Component' in [p.getIdentifier() for p in node.getInterfacesAll()]:
                        klass = cct.component.Component(action='create', args=[newId], version=pVertex.version, project=self.project, 
                                                        modulePath=self.project.modulePath, graph=self.graph)
                    else:
                        klass = cct.sidlclass.Sidlclass(action='create', args=[newId], version=pVertex.version, project=self.project, 
                                                        modulePath=self.project.modulePath, graph=self.graph)
                    klass.setASTNode(node)
                    klass.create()
                    comment = node.getStartComment()
                    if comment: klass.setComment(comment)
                    self.methods[newId]=[]
                else:
                    self._symbolConflictError(slist)

                edge = BEdge(pVertex, klass, self.graph, action='contains')
                self.classes[id] = klass
                    
        self.visitVertex(node)
        pass
    
    def visitMethod(self,node):
        parent = node.getParent()
        if parent is None: print 'parent is None'
        if parent:
            parentid = parent.getFullIdentifier()
            if self.matchPartialSymbols(parentid, self.symbols)  or self.doAll:
                if self.parentVertex.kind in ['package','project'] and self.matchPartialSymbols(parentid, self.interfaces.keys()):
                    symbol = self.interfaces[parentid].symbol
                elif self.parentVertex.kind in ['package','project'] and self.matchPartialSymbols(parentid, self.classes.keys()):
                    symbol = self.classes[parentid].symbol
                elif self.parentVertex.kind in ['interface', 'port', 'class', 'component']:
                    symbol = self.parentVertex.symbol
                else:
                    err('cannot import methods into a ' + self.parentVertex.kind + ' (only into project, package, interface, port, class, or component)')
                        
                if not self.methods.has_key(symbol): self.methods[symbol]=[]
                if node not in self.methods[symbol]:
                    print >>DEBUGSTREAM,'adding method ' + node.getIdentifier() + ' to ' + symbol 
                    self.methods[symbol].append(node)

        self.visitVertex(node)
        pass
    
    def visitEnumeration(self, node):
        if self.parentVertex.kind in ['package','project','enum']:
            parentid = node.getParent().getFullIdentifier()
            id = node.getFullIdentifier()

            if self.matchPartialSymbols(id, self.symbols) or self.doAll:
                shortId = node.getIdentifier()
                if parentid in self.packages.keys():
                    pVertex = self.packages[parentid]
                else:
                    if self.parentVertex.kind not in ['package', 'project', 'enum']:
                        err('Enums can only be imported into Bocca packages')
                    pVertex = self.parentVertex
                    
                newId = pVertex.symbol + '.' + shortId
                if self.parentVertex.kind == 'project': 
                    newId = id
                slist = self.graph.findSymbol(newId, kind='any')
                if len(slist) == 1 and slist[0].kind == 'enum':
                    enum = slist[0]
                    enum.setASTNode(node)
                elif not slist:    
                    if self.parentVertex.kind != 'enum':
                        enum = cct.enum.Enum(action='create', args=[newId], version=pVertex.version, project=self.project,
                                             modulePath=self.project.modulePath, graph=self.graph)
                    else:
                        enum = self.parentVertex
                    
                    enum.setASTNode(node)
                    if len(node.getContents()): 
                        enum.genDummy = False
                    if self.parentVertex.kind != 'enum': 
                        enum.create()
                    comment = node.getStartComment()
                    if comment: enum.setComment(comment)
                else:
                    self._symbolConflictError(slist)
                edge = BEdge(pVertex, enum, self.graph, action='contains')
                self.enums[id] = enum

        self.visitVertex(node)
        pass        
    
    #---------------------- Private methods --------------------------------
    def _symbolConflictError(self, symlist):
        buf = ''
        for sym in symlist: 
            buf += str(sym) + ', '
        buf.rstrip(',')
        err('cannot import package into ' + self.parentVertex.symbol + ' due to a symbol conflict:\n' + buf)
        
    def matchPartialSymbols(self, sym, symlist):
        '''Return True if an elemeent in symlist matches a right substring of sym'''
        if sym in symlist:
            return True
        for s in symlist:
            if sym.endswith('.' + s):
                return True
        return False
        