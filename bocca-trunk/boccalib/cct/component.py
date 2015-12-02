from cct._debug import DEBUGSTREAM, WARN, BLOCKDUMP
from cct._util import fileManager, lang_to_fileext, lang_to_headerext, Globals
from graph.boccagraph import BEdge, SymbolError
from cct._err import err, warn
#from cct._validate import language as validateLang
from cct._typedmap import TypedMap
from cct.port import Port
from cct.sidlclass import Sidlclass 
import os
from writers.boccaWriterFactory import BoccaWriterFactory
from writers.sourceWriter import SourceWriter
from splicers import Source, Operations
from cct._component_callbacks import *
import sys

class Component(Sidlclass): 
    """Add new component to current project.
   
    """
    
    def __init__(self, action = '__init__', args = None, project = None, modulePath = None,
                 symbol=None, version='0.0', graph=None):
        '''bocca <verb> component [options] SIDL_SYMBOL
        
        <verb> is one of create, change, remove, rename, display. For documentation on
        specific verbs, use 'bocca help <verb> component'
        '''

        self.implImports = {}
        self.graph = graph
        self.displayAll = False          # Used in display
        self.newProvides = []            # List of PortInstance objects
        self.newUses = []                # List of PortInstance objects
        self.new_extends = {}            # Used in create and change
        self.new_implements = {}         # Used in create and change
        self.newComponentProperties = TypedMap() # Used in create and change
        self.newPortsProperties = dict() # Used in create and change
        self.newBasicParamPort = None    # Used in create and change
        self.newParameterPorts = dict()  # Used in create and change
        self._b_provides = []          # List of port instance objects
        self._b_uses = []       
        if (symbol == 'temp'): 
            Sidlclass.__init__(self, action = action, 
                               args = args, modulePath = modulePath, 
                               project = project, kind = 'component', 
                               symbol = symbol, version = version, graph = graph)
            return
        self._b_componentProperties = TypedMap()
        self._b_portsProperties = dict(); # key{portname}: value{TypedMap}
        # simple param port:
        self._b_basicParamPort = None; # if not none, provides typemap and port of user-specified name which is stored here
        # full parameter ports delegated from factory.
        self._b_parameterPorts = dict(); # key{portname}: value{paramportdesc}
       # List of port instance objects
        self.allPortsTypes=[]
        Sidlclass.__init__(self, action = action, 
                         args = args, modulePath = modulePath, 
                         project = project, kind = 'component', 
                         symbol = symbol, version = version, graph=graph)
        pass

    def initCopy(self, copiedComponent):
        # Hack to make copy work with updateGraph, which generates _b_provides/_b_uses
        self.newProvides = copiedComponent._b_provides
        self.newUses = copiedComponent._b_uses
        
        Sidlclass.initCopy(self, copiedComponent)
        pass
        
# ------------------------------------------------
    def defineArgs(self, action):
        '''Defines command line options and defaults for this command. This is 
           invoked in the constructor of the parent class Subcommand.
        '''
        if (action == 'create'):
            self.defineArgsCreate()
        elif action == 'copy':
            Sidlclass.defineArgsCopy(self)
        elif action == 'rename':
            pass
        elif action == 'display':
            Sidlclass.defineArgs(self, action)
        elif action == 'change':
            self.defineArgsChange()
        elif action == 'edit' or action == 'whereis':
            Sidlclass.defineArgs(self, action)
        elif action == 'remove':
            Sidlclass.defineArgsRemove(self)
        else:
            err('Component verb "' + action + '" NOT implemented yet.', 3)
        return
        
        
# ------------------------------------------------
    def defineCommonArgsCreateAndChange1(self):
        '''Defines options common to the create and change operations.'''
        self.parser.add_option("-p", "--provides", dest="providesPort", action="append",
                          help="ports PROVIDED by the component. A port is specified as "
                          + "PORT_TYPE@PORT_NAME, where PORT_TYPE is the fully qualified SIDL type of the provided port, "
                          + "and PORT_NAME is the name given to the provided port instance in the component code. "
                          + "Multiple ports can be specified using multiple --provides options."
                          + "Optionally, an external SIDL file name can be specified if the port is " 
                          + "not part of this project, e.g., PORT_TYPE@PORT_NAME@/path/to/portfile.sidl.")

        self.parser.add_option("-u", "--uses", dest="usesPort", action="append",
                          help="ports USED by the component. A port is specified as "                     
                          + "PORT_TYPE@PORT_NAME, where PORT_TYPE is the fully qualified SIDL type of the used port, "
                          + "and PORT_NAME is the name given to the used port instance in the component code. "
                          + "Multiple ports can be specified using multiple --uses options. "
                          + "Optionally, an external SIDL file name can be specified if the port is " 
                          + "not part of this project, e.g., PORT_TYPE@PORT_NAME@/path/to/portfile.sidl.")
        
        self.parser.add_option("-g", "--go", action="callback", type="string", callback=go_option_callback,
                          help="port type gov.cca.ports.GoPort is provided by the component. "
                          + "PORT_NAME must be specified; PORT_TYPE is omitted. "
                          + "Multiple requests for a GoPort will be ignored")
        

    def defineCommonArgsCreateAndChange2(self):
# Override help for -x option        
        self.parser.get_option('-x').help='path to external XML repositories containing ' \
        + 'specification of the ports (and/or interfaces) referenced  by the new component (or of ' \
        + 'symbols referenced by those ports). Multiple repositories can be used (separated by commas). ' \
        + 'Alternatively, multiple instances of the -x option can be used to specify multiple repositories ' \
        + 'paths.'

        self.parser.set_defaults(providesPorts=None,
                                 usesPorts=None,
                                 GoPortStatus=0)
        
    def defineArgsCreate(self):
        '''Defines command line options and defaults for the create action. 
        '''
        self.defineCommonArgsCreateAndChange1()
        Sidlclass.defineArgsCreate(self)
        self.defineCommonArgsCreateAndChange2()
        
        return
                               
    
    def defineArgsChange(self):
        '''Defines command line options and defaults for the change action.
        '''
        # Support all the creation options:
        self.defineCommonArgsCreateAndChange1()
        Sidlclass.defineArgsChange(self)
        self.defineCommonArgsCreateAndChange2()
        # Additional arguments specific to change
        
        # remove a port from this component
        self.parser.add_option("-d", "--delete", dest="deletePortName", action="append",
                          help="remove ports used or provided by the component given the port name (not SIDL symbol)."
                          + "Multiple ports can be specified using multiple --delete options.")
        return
        
    
# ------------------------------------------------
    def portArgsToDict(self, arg):
        """ Return dictionary of port arguments, where 
            Dictionary keys = Port Names
            Dictionary entries = Port Types
        """
        # Make sure we have a unified list of portType:portName pairs, possible
        # derived from multiple sub-lists on the command line
        # TODO: Check whether this way of specifying oprt arguments is too flexible.
        argList = ','.join(arg).split(',')
        d = {}
        for p in argList:
            l = p.split(':')
            if (len(l)!= 2):
                err("Invalid port specification : " + p +"\nPort specification of the form portType:portnAME", 2)
            if l[1] in d.keys():
                err("Duplicate specification of port name \"", p[1], "\"", 2)
            print >> DEBUGSTREAM, "port name = ", l[1]
            print >> DEBUGSTREAM, "port type = ", l[0]
            d[l[1]] = l[0]
        return d    
            
# ------------------------------------------------
    def processArgs(self, action):
        """ Dispatch argument processing based in required action
        """
        print >> DEBUGSTREAM, "Component called with options ", \
                              str(self.options) , " leaving args " , str(self.args)
        if (action == 'create'):
            self.processCreateArgs()
        elif (action == 'change'):
            self.processChangeArgs()
        elif (action == 'display'):
            Sidlclass.processDisplayArgs(self)
        elif (action == 'rename'):
            self.processRenameArgs()
        elif (action == 'edit' or action == 'whereis'):
            Sidlclass.processArgs(self, action)
        elif (action == 'remove'):
            Sidlclass.processRemoveArgs(self)
        elif (action == 'copy'):
            Sidlclass.processCopyArgs(self)
        else:
            err("Action "+ action + " NOT implemented yet", 3)
        return

# ------------------------------------------------
    def processCommonCreateAndChangeArgs(self):
        print >>DEBUGSTREAM, "component: processCommonCreateAndChangeArgs"
        options, args = self.options, self.args

        # print "UH_component:processCommonCreateAndChangeArgs"
        # dpathdata = self._processDpathOptions()
        # self._updateDpaths(dpathdata)

        # relocatd base call from end of method.
        Sidlclass.processCommonCreateAndChangeArgs(self)

        if options.usesPort:
            self.newUses = self._processSymbolAssociationOptions(options.usesPort, '--uses/-u')
                
        if options.providesPort:
            self.newProvides = self._processSymbolAssociationOptions(options.providesPort, '--provides/-p')
            
        print >>DEBUGSTREAM, "\nComponent: newProvides = ", self.newProvides, \
                            "\nComponent: newUses = ", self.newUses

        for newp in self.newUses + self.newProvides:
            for p in [x.getName() for x in self._b_uses + self._b_provides]:
                if p == newp.getName():
                    err('This component already uses or provides a port of this name: ' + str(p) 
                           + ' (port names must be unique within a component),')
        for newp in self.newProvides:
            for i in [x.getType() for x in self._b_provides] + self._b_implements.keys():
                if i == newp.getType():
                    err('This component already implements this interface or provides a port of this type: ' + str(i))
                    
            if [x.getType() for x in self.newProvides].count(newp) > 1:
                err('A port cannot be provided more than once: ' + str(newp))
                            
        # relocating base call to beginning of method
        
        return
        
    def processCreateArgs(self):
        """ Process command line arguments passed to the "component create" command
        """
        print >>DEBUGSTREAM, "component: processCreateArgs"
        Sidlclass.processCreateArgs(self)
        return
       
    def processChangeArgs(self):
        """Process command line arguments passed to the "component change" command
        """
        Sidlclass.processChangeArgs(self)

        return
    
    def processRenameArgs(self):
        """ Process command line arguments passed to the "component rename" command
        """
        Sidlclass.processRenameArgs(self)
        return    

# ------------------------------------------------

    def create(self):
        """create component [options] SIDL_SYMBOL
        """
        Sidlclass.create(self)
        return 0

    def copy(self):
        """copy component [options] FROM_SIDL_SYMBOL TO_SIDL_SYMBOL
        """

        copyVertex = Component('create', args=[self.newSymbol], project=self.project, modulePath=self.modulePath,
                               symbol=self.symbol, version=self.version, graph=self.graph)
        copyVertex.initCopy(self)


        # Need to import complete SIDL definition from copied class
        copyVertex.oldsymbol = self.symbol
        copyVertex.sidlImports = { self._b_sidlFile : ['%all'] }

        # settings from -l and -d are handled by copyVertex
        if self.options.copysrcimpl:
            copyVertex.implImports = { self.symbol : self._b_implSource[0:self._b_implSource.rfind('/')] }

        return copyVertex.create()

    def change(self):
        """change component SIDL_SYMBOL options
        """
        project,graph = Globals().getProjectAndGraph(self.projectName)
        
        # delete uses or provides port
        if self.options.deletePortName:
            allmyports = [x.getName() for x in self._b_provides + self._b_uses]
            for p in self.options.deletePortName:
                if p not in allmyports:
                    err('There is not port named ' + p + ' in this component.')
        
            for pname in self.options.deletePortName:
                for theport in self._b_uses + self._b_provides:
                    if pname == theport.getName():
                        # TODO: Make sure this port is not in the implements or provides list under more than one name 
                        # before deleting the type
                        ptype = theport.getType()
                        if [x.getType()==ptype for x in self._b_uses + self._b_provides].count(True) + self._b_implements.keys().count(ptype) <= 0:
                            # remove edge
                            self.removeInEdge(ptype, kind = 'port', graph=graph)
                            if location == '%external%':
                                # Remove external file name in project defaults file
                                if not self._findExternal(ptype): project.removeDefaultValue(ptype,'External')
                                print >>DEBUGSTREAM, 'Removed external port or interface: ' + ptype
                                if ptype in self._b_externalSidlFiles.keys(): del self._b_externalSidlFiles[ptype]   
                        try: 
                            if theport in self._b_uses: self._b_uses.remove(theport)
                            elif theport in self._b_provides: self._b_provides.remove(theport)
                        except: err('Could not remove port %s, port not used or provided in component %s' % (pname, self.symbol))     
            
        # Let class handle everything it can (it also calls the builder update method)
        Sidlclass.change(self)
        return 0
    
    def display(self):
        """display component SIDL_SYMBOL
        """
        return Sidlclass.display(self) 
    
# ------------------------------------------------
    def rename(self):
        """rename component OLD_SIDL_SYMBOL NEW_SIDL_SYMBOL
        """
        #return self.renameTarget._internalRename()
        Sidlclass.rename(self)
    
    def remove(self):
        """remove component SIDL_SYMBOL
        """
        return Sidlclass.remove(self)

    def whereis(self):
        '''whereis component SIDL_SYMBOL [optional method name] options
        '''
        return Sidlclass.whereis(self)

    def edit(self):
        '''edit component SIDL_SYMBOL [optional method name] options
        '''
        return Sidlclass.edit(self)
    
    def prettystr(self):
        project, graph = Globals().getProjectAndGraph()
        s =  self.kind + ' ' + self.symbol + ' ' + self.version + ' (' + self._b_language + ')'
        
        if len(self._b_provides) > 0:
            s+=  '\n\tprovides ports:\n'
            for i in self._b_provides: 
                s +=  '\t  ' + i.prettystr() + '\n'
        
        if len(self._b_uses) > 0:
            s+=  '\n\tuses ports:\n'
            for i in self._b_uses: 
                s +=  '\t  ' + i.prettystr() + '\n'
                        
        if len(self._b_implements) > 0:
            s+=  '\n\timplements interfaces:\n'
            for i in self._b_implements.keys(): 
                s +=  '\t  ' + i 
                if self._b_implements[i] != '%local%': s += ', location = ' + project.getDefaultValue(i,'External')
                else: s += ', local'
                s += ' ' + '\n'

        if len(self._b_extends) > 0:
            s += '\n\textends class: ' + self._b_extends.keys()[0]                 
            if self._b_extends.values()[0] != '%local%': s += ', location = ' + project.getDefaultValue(self._b_extends.keys()[0],'External')
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

# ------------------------------------------------

    def updateGraph(self):

        # Component-specific code:
        #  Check existence of interface nodes in project graph and add edges
        symdict={}
        for p in self.newProvides: symdict[p.getType()] = p.getLocation()
        fqsymboldict, vertices = self._validateProjectSymbols(self.graph, symbols=symdict, 
                                                           kinds=['interface','port']) # should it be just 'port'?
        for ifaceNode in vertices:
            edge = BEdge(ifaceNode, self, graph=self.graph, action = 'provides')  # Connect with implemented interface
        # Add the new ports 
        for p in self.newProvides: 
            p.setLocation(fqsymboldict[p.getType()])
        self._b_provides.extend(self.newProvides)
            
        print >>DEBUGSTREAM,'Provides ports: ', self._b_provides
        
        # Check for existence of class/component nodes in project graph and add edges
        symdict={}
        for p in self.newUses: symdict[p.getType()] = p.getLocation()
        fqsymboldict, vertices = self._validateProjectSymbols(self.graph, symbols=symdict, 
                                                              kinds = ['interface', 'port']) # should it be just 'port'?
        for ifaceNode in vertices:
            edge = BEdge(ifaceNode, self, graph=self.graph, action = 'uses')  # Connect with implemented interface
        # Add the new interfaces 
        for p in self.newUses:
            p.setLocation(fqsymboldict[p.getType()])
        self._b_uses.extend(self.newUses)
                
        #print 'DEBUG: newUses=', str(self.newUses), ', b_uses=', str(self._b_uses)
    
        Sidlclass.updateGraph(self)
        pass

        
    def renameInternalSymbol(self, oldSymbol, newSymbol):
        Sidlclass.renameInternalSymbol(self, oldSymbol, newSymbol)
        
        for p in self._b_provides + self._b_uses:
            if oldSymbol == p.getType():
                self._replaceSymbolInFiles(oldSymbol, newSymbol)
                p.setType(newSymbol)
                
# FIXME: We're doing this to check that the sed approach actually works. 
        self.genClassImpl()
        return 0
    
    def removeInternalSymbol(self, oldSymbol):
        ''' Removes any internal references to symbol.'''
        Sidlclass.removeInternalSymbol(self,oldSymbol)
        
        for p in self._b_provides:
            if oldSymbol == p.getType():
                self._removeSymbolInFiles(oldSymbol)
                self._b_provides.remove(p)

                
        for p in self._b_uses:
            if oldSymbol == p.getType():
                self._removeSymbolInFiles(oldSymbol)
                self._b_uses.remove(p)
               
        self.genClassImpl()
        return 0
                
# ------------------------------------------------    
    def spliceBoccaBlocks(self):
        impldir, flist = self.project.getLocationManager().getImplLoc(self)
        print >> DEBUGSTREAM, '**** in COMPONENT spliceBoccaBlocks: ', self.project.getDir(), impldir, str(flist)
        implSourceFile =  os.path.join(self.project.getDir(), self._b_implSource)
        writer = BoccaWriterFactory().getWriter(self._b_language, self._b_dialect)
        
# Splice code into impl source file
# This happens differently on the creation of the component than
# any time afterward. Afterward (except the addition of supported provides ports)
# we only resplice bocca-protected code, never user or default-suggested code.
        rejectSave = False
        replaceBlockList = []
            
        if self.action == "create" or self.action == "add":
            sourceKey="DO-NOT-DELETE splicer"
            print >> DEBUGSTREAM, "## Initial splicing on ", sourceKey, "blocks"
        else:
            sourceKey=SourceWriter().protKey
            print >> DEBUGSTREAM, "## Resplicing on ", sourceKey, "blocks"
            # if we never requested defaulted go, this will just be ignored during splice.
            replaceBlockList.append(writer.getGoCode(self.symbol, uses = self._b_uses))


        replaceBlockList.append(writer.getImplHeaderCode(self.symbol))
        replaceBlockList.append(writer.getConstructorCode(self.symbol))
        replaceBlockList.append(writer.getDestructorCode(self.symbol))
        replaceBlockList.append(writer.getSetServicesCode(self.symbol))
        replaceBlockList.append(writer.getAuxiliarySetServicesMethod(self.symbol, 
                                                              provides = self._b_provides, 
                                                              uses = self._b_uses))
        replaceBlockList.append(writer.getReleaseMethod(self.symbol))
        replaceBlockList.append(writer.getAuxiliaryReleaseServicesMethod(self.symbol, 
                                                              provides = self._b_provides, 
                                                              uses = self._b_uses))
        reqs = self.getAttr('requires')
        if not reqs: nreqs=len(self._b_uses)
        else: nreqs=len(reqs) + len(self._b_uses)
        depthstring = self.getDepthstring()
        replaceBlockList.append(writer.getForceUsePortCode(self.symbol,nreqs, depthstring))
        replaceBlockList.append(writer.getCheckExceptionMethod(self.symbol))
        
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

        # handle gocode, which is interesting:
        # if --go and component new, stick in splice wholesale.
        # if --go and component old but goport is new, stick in splice wholesale.
        # if --go and component old and goport was there before but now --go given,
        # print where the rejects go and splice in wholesale.
        if self.parser.values.GoPortStatus == 1:
            goBlockList = []
            goBlockList.append(writer.getGoCode(self.symbol,uses = self._b_uses))
            golist= ''.join(goBlockList)
            if BLOCKDUMP:
                print >> DEBUGSTREAM, "GOLIST"
                print >> DEBUGSTREAM, golist
            sourceKey="DO-NOT-DELETE splicer"
            gokillsubs=["Insert-Code-Here"]
            Operations.mergeFromString(implSourceFile, golist, 'REPLACE_BLOCKS', 
                                   targetKey = sourceKey,
                                   sourceKey = sourceKey,
                                   insertFirst = True, 
                                   dbg = WARN, 
                                   verbose = WARN, 
                                   dryrun = False, 
                                   replaceIdentical = False, 
                                   rejectSave= True, 
                                   warn= WARN,
                                   killSubstrings=gokillsubs)
        
        # if babel adds headers for f77 someday, this will need adjustment.
        if (self._b_language in ['f77', 'f77_31', 'python','java']):
            return
        
# Splice code into impl header file
        implHeaderFile =  os.path.join(self.project.getDir(), self._b_implHeader)
        print >> DEBUGSTREAM, 'Splicing Impl header file ', implHeaderFile
        codeBlock = writer.getHeaderCode(self.symbol)
        if BLOCKDUMP:
            print >> DEBUGSTREAM, codeBlock
        fd = open(implHeaderFile, "r")
        targetBuf  = fd.read()
        fd.close()
        Operations.mergeFromString(implHeaderFile, codeBlock, 'PREPEND_BLOCKS', 
                                   targetKey = sourceKey,
                                   sourceKey = sourceKey,
                                   insertFirst = True, 
                                   dbg = WARN, 
                                   verbose = WARN, 
                                   dryrun = False, 
                                   rejectSave= True, 
                                   warn= WARN)
        return

# --------------------------------------------------------------------------

    def graphvizString(self): 
        return 'shape=doubleoctagon color=turquoise3 fontname="Palatino-Italic"'


# ------------------------------------------------
# ---------------- PRIVATE methods

    def _internalRename(self):
        return Sidlclass._internalRename(self)       
        
if __name__ == "__main__":
    Component().usage()
