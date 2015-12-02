
from parse.itools.visitor.visitor import Visitor
import parse.itools.ParameterAccessMode
import sets

class CompilerException(Exception):
    def __init__(self,value):
        self.parameter=value
    def __str__(self):
        return repr(self.parameter)
        
class Vertex:
    '''
    A generic node in the SIDL AST
    '''
    # Starting class methods section
    pass
    
    def __init__(self, parent=None):
        if parent is not None:
            self.identifier = parent.identifier
        else:
            self.identifier = None
        self.dependencies = sets.Set()
        self.attributes = []
        self.parent = parent
        self.children = []
        self.lineNumber = -(1)
        self.endLineNumber = -(1)
        self.comments = []            # NOT USED AT THE MOMENT
        self.startComment = ''
        self.endComment = ''
    
    def clone(self):
        '''
        Return an empty object of the same type
        '''
        return Vertex()
    
    def copy(self):
        '''
        Return a deep copy of this subtree
        '''
        root = Vertex()
        root.setIdentifier(self.getIdentifier())
        root.setAttributes(self.getAttributes())
        root.setLineNumber(self.getLineNumber())
        root.setComments(self.getComments())
        root.setChildren([child.copy() for child in self.getChildren()])
        return root
    
    def isInstanceOf(self, typename):
        '''
        Return true if I am an instsance of the type given by typename.
        '''
        if str(self.__class__) == typename:
            return True
        else:
            return False
        
    def accept(self, visitor):
        '''
        Support the visitor pattern for traversal.
        '''
        visitor.visitVertex(self)
    
    def getIdentifier(self):
        '''
        Retrieve the identifier associated with this vertex
        '''
        return self.identifier
    
    def setIdentifier(self, identifier):
        '''
        Assign the identifier associated with this vertex
        '''
        self.identifier = identifier
    
    def getAttributes(self):
        '''
        Get attribute list for this element
        '''
        return self.attributes
    
    def setAttributes(self, attributes):
        '''
        Set attribute list for this element
        '''
        self.attributes = attributes
    
    def hasAttribute(self, name):
        '''
        Determine whether an attribute is present on this vertex
        '''
        for attribute in self.attributes:
            if attribute.getName() == name:
                return 1
        return 0
    
    def addAttribute(self, attribute):
        '''
        Add attribute to this vertex
        '''
        for attr in self.attributes:
            if attr.getName() == attribute.getName():
                self.attributes.remove(attribute)
        self.attributes.append(attribute)
    
    def deleteAttribute(self, name):
        '''
        Remove an attribute on this vertex
        Throws an exception if the attribute does not exist
        '''
        for attribute in self.attributes:
            if attribute.getName() == name:
                return self.attributes.remove(attribute)
        e = parse.itools.CompilerCompilerException.CompilerException()
        e.setMessage('Attribute does not exist: ' + name)
        raise e
    
    def getAttribute(self, name):
        '''
        Get an attribute on this vertex
        Throws an exception if the attribute does not exist
        '''
        for attribute in self.attributes:
            if attribute.getName() == name:
                return attribute
        e = CompilerException()
        e.setMessage('Attribute does not exist: ' + name)
        raise e
    
    def getParent(self):
        '''
        Retrieve the parent of this vertex
        '''
        return self.parent
    
    def setParent(self, parent):
        '''
        Assign the parent of this vertex
        '''
        self.parent = parent
    
    def getChildren(self):
        '''
        Retrieve the children of this vertex
        '''
        return self.children
    
    def setChildren(self, children):
        '''
        Set the children of this vertex
        '''
        self.children = list(children)
        for child in children:
            child.setParent(self)
    
    def addChildren(self, children):
        '''
        Add children to this vertex (duplicates allowed)
        '''
        for child in children:
            if child:
                self.children.append(child)
                child.setParent(self)
    
    def removeChildren(self, children):
        '''
        Remove children from this vertex
        Throws an exception if any child does not exist
        '''
        for child in children:
            if child in self.children:
                self.children.remove(child)
                child.setParent(None)
            else:
                e = parse.itools.CompilerException()
                e.setMessage('Child does not exist: ' + str(child))
                raise e
    
    def getLineNumber(self):
        '''
        Retrieve the line number associated with this vertex
        '''
        return self.lineNumber
    
    def setEndLineNumber(self, lineNumber):
        '''
        Set the last line number associated with this vertex
        '''
        self.endLineNumber = lineNumber
        
    def getEndLineNumber(self):
        '''
        Retrieve the last line number associated with this vertex
        '''
        return self.endLineNumber
    
    def setLineNumber(self, lineNumber):
        '''
        Set the line number associated with this vertex
        '''
        self.lineNumber = lineNumber
    
    def getComments(self):
        '''
        Retrieve the comments of this vertex
        '''
        return self.comments
    
    def setComments(self, comments):
        '''
        Set the children of this vertex
        '''
        self.comments = list(comments)
    
    def addComments(self, comments):
        '''
        Add comments to this vertex (duplicates allowed)
        '''
        self.comments.extend(comments)
        
    def getStartComment(self, appendNewLine = True):
        '''
        Return the start comment associated with this vertex
        '''
        if not appendNewLine or self.startComment is '' or self.startComment.endswith('\n'):
            return self.startComment
        else:
            return self.startComment + '\n'
    
    def setStartComment(self, comment):
        '''
        Set the start comment associated with this vertex
        '''
        self.startComment = comment
    
    def getEndComment(self, appendNewLine = True):
        '''
        Return the end comment associated with this vertex
        '''
        if not appendNewLine or self.endComment is '' or self.endComment.endswith('\n'):
            return self.endComment
        else:
            return self.endComment + '\n'
    
    def setEndComment(self, comment):
        '''
        Set the end comment associated with this vertex
        '''
        self.endComment = comment
        
    def appendStartComment(self, comment):
        if comment.endswith('\n'):
            self.startComment += comment
        else:
            self.startComment += comment + '\n'
    
    def appendEndComment(self, comment):
        if comment.endswith('\n'):
            self.endComment += comment
        else:
            self.endComment += comment + '\n'
        
    def removeComments(self, comments):
        '''
        Remove comments from this vertex
        Throws an exception if a comment does not exist
        '''
        for comment in comments:
            if comment in self.comments:
                self.comments.remove(comment)
            else:
                e = parse.itools.CompilerException()
                e.setMessage('Comment does not exist: ' + str(comment))
                raise e
    
    def getFullIdentifier(self):
        '''
        Retrieve the fully qualified identifier associated with this node
        '''
        return self.identifier
    
    def getDependencies(self):
        '''
        Retrieve nodes on which this node depends
        '''
        return list(self.dependencies)
    
    def setDependencies(self, dependencies):
        '''
        Set nodes on which this node depends
        '''
        self.dependencies = sets.Set([dep for dep in dependencies])
    
    def addDependencies(self, dependencies):
        '''
        Add nodes on which this node depends
        '''
        self.dependencies.update([dep for dep in dependencies])
    
    def removeDependencies(self, dependencies):
        '''
        Remove nodes on which this node depends
        Throws an exception if a dependency does not exist
        '''
        for dependency in dependencies:
            if dependency in self.dependencies:
                self.dependencies.remove(dependency)
            else:
                e = parse.itools.CompilerException()
                e.setMessage('Dependency does not exist: ' + dependency.getIdentifier())
                raise e
            
    def __repr__(self):
        return self.getIdentifier()
    # Ending class methods section
    pass

class Specification(Vertex):
    '''
    The smallest unit SIDL code for a file
    '''
    
    def __init__(self):
        Vertex.__init__(self)
    
    def accept(self, visitor):
        '''
        Overridden to dispatch correctly
        '''
        visitor.visitSpecification(self)
    # Ending class methods section
    pass


class Type(Vertex):
    '''
    Any SIDL type
    '''
    
    def __init__(self):
        self.baseType = 0
        self.generic = False
        self.void = False
        Vertex.__init__(self)
    
    def accept(self, visitor):
        '''
        Overridden to dispatch correctly
        '''
        visitor.visitType(self)
    
    def copy(self):
        '''
        Need to override this
        '''
        root = parse.itools.Type.Type()
        root.setIdentifier(self.getIdentifier())
        root.setAttributes(self.getAttributes())
        root.setLineNumber(self.getLineNumber())
        root.setComments(self.getComments())
        root.setChildren([child.copy() for child in self.getChildren()])
        root.setBaseType(self.getBaseType())
        return root
    
    def getFullIdentifier(self):
        '''
        Need to override this to calculate the fully qualified type name
        '''
        id = self.getIdentifier()
        if id.count('.') > 0: return id
        if not self.getBaseType():
            # TODO fix this to use the symbol table once it exists
            parent = self.getParent()
            if parent is not None:
                if not parent.isInstanceOf('parse.itools.elements.Method'):
                   return parent.getFullIdentifier() + '.' + id

        return id
    
    def getBaseType(self):
        '''
        Get flag indicating whether this is a base type
        '''
        return self.baseType
    
    def setBaseType(self, baseType):
        '''
        Set flag indicating whether this is a base type
        '''
        self.baseType = baseType

    def getGeneric(self):
        '''
        Return the flag indicating whether this is a generic type (True or False)
        '''
        return self.generic
                
    def setGeneric(self, val):
        '''
        Set flag indicating whether this is a generic type (True or False)
        '''
        self.generic = val
    
    def getVoid(self):
        '''
        Return the flag indicating whether this is a void type (True or False)
        '''
        return self.void
                
    def setVoid(self, val):
        '''
        Set flag indicating whether this is a void type (True or False)
        '''
        self.void = val
    # Ending class methods section
    pass

class Array(Type):
    '''
    A SIDL array
    '''
    def __init__(self, rarray=False):
        self.identifier = 'array'
        self.rarray = False
        if rarray: 
            self.identifier = 'rarray'
            self.rarray = True
        self.type = None
        self.dimension = -(1)
        self.rarray = rarray
        self.orientation = 'row-major'
        Type.__init__(self)
    
    def accept(self, visitor):
        '''
        Overridden to dispatch correctly
        '''
        visitor.visitArray(self)
    
    def getFullIdentifier(self):
        '''
        Need to override this to calculate the fully qualified type name
        '''
        if self.getIdentifier() is None:
            return 'array of ' + self.getType().getFullIdentifier()
        else:
            return self.getIdentifier()
    
    def getType(self):
        '''
        Retrieve the element type
        '''
        return self.type
    
    def setType(self, type):
        '''
        Set the element type
        '''
        self.type = type
    
    def getOrientation(self):
        '''
        Retrieve the array's orientation: row-major or col-major
        '''
        return self.orientation
    
    def setOrientation(self, orientation):
        '''
        Set the orientation of the array: row-major or col-major
        '''
        self.orientation = orientation
        
    def getDimension(self):
        '''
        Retrieve the array dimension
        '''
        return self.dimension
    
    def setDimension(self, dimension):
        '''
        Set the array dimension
        '''
        self.dimension = dimension
    
    def isRarray(self):
        return self.rarray
    
    def setRarray(self, val):
        self.rarray = val
    
    # Ending class methods section
    pass

class Comment(Vertex):
    '''
    A SIDL comment
    '''
    def __init__(self):
        self.comment = ''
        Vertex.__init__(self)

    def getComment(self):
        '''
        Get the comment string
        '''
        return self.comment
    
    def setComment(self, comment):
        '''
        Set the comment string
        '''
        self.comment = comment
    # Ending class methods section
    pass


class Enumeration(Type):
    '''
    A SIDL enumeration
    '''
    
    def __init__(self):
        self.setBaseType(0)
        self.initialized = 0
        self.contents = ''
        Type.__init__(self)
    
    def accept(self, visitor):
        '''
        Overridden to dispatch correctly
        '''
        visitor.visitEnumeration(self)
    
    def copy(self):
        '''
        Need to override this
        '''
        root = parse.itools.Enumeration.Enumeration()
        root.setIdentifier(self.getIdentifier())
        root.setAttributes(self.getAttributes())
        root.setLineNumber(self.getLineNumber())
        root.setComments(self.getComments())
        root.setChildren([child.copy() for child in self.getChildren()])
        root.setInitialized(self.getInitialized())
        return root
    
    def getInitialized(self):
        '''
        Retrieve the flag indicating whether the enumeration values are specified
        '''
        return self.initialized
    
    def setInitialized(self, initialized):
        '''
        Set the flag indicating whether the enumeration values are specified
        '''
        self.initialized = initialized
        
    def setContents(self, contentstring):
        '''
        Save the entire contents (for convenience)
        The Enumerator instances are saved as AST children.
        '''
        self.contents = contentstring
        
    def getContents(self):
        '''
        Return the contents as a string (for convenience)
        '''
        return self.contents
    
    # Ending class methods section
    pass

class Enumerator(Vertex):
    '''
    A component of a SIDL enumeration
    '''

    def __init__(self):
        self.value = 0
        self.initialized = 0
        Vertex.__init__(self)
    
    def accept(self, visitor):
        '''
        Overridden to dispatch correctly
        '''
        visitor.visitEnumerator(self)
    
    def copy(self):
        '''
        Need to override this
        '''
        root = parse.itools.Enumerator.Enumerator()
        root.setIdentifier(self.getIdentifier())
        root.setAttributes(self.getAttributes())
        root.setLineNumber(self.getLineNumber())
        root.setComments(self.getComments())
        root.setChildren([child.copy() for child in self.getChildren()])
        root.setInitialized(self.getInitialized())
        root.setValue(self.getValue())
        return root
    
    def getInitialized(self):
        '''
        Retrieve the flag indicating whether the entry had an initializer
        '''
        return self.initialized
    
    def setInitialized(self, initialized):
        '''
        Set the flag indicating whether the entry had an initializer
        '''
        self.initialized = initialized
    
    def getValue(self):
        '''
        Retrieve the entry value
        '''
        return self.value
    
    def setValue(self, value):
        '''
        Set the entry value
        '''
        self.value = value
    # Ending class methods section
    pass

class Class(Type):
    '''
    A SIDL class
    The children of this node are methods defined in the class
    The parents are now superclasses
    '''

    def __init__(self):
        self.parents = []
        self.interfaces = []
        self.interfaces_all = []
        self.implementedMethods = []
        self.methods = []
        self.templateIds = []
        Type.__init__(self)
    
    def getParents(self):
        '''
        Retrieve the superclasses of this class
        '''
        return self.parents

    def getParentIds(self):
        lst = []
        for p in self.parents:
            lst.append(p.getFullIdentifier())
        return lst
        
    def setParents(self, parents):
        '''
        Set the superclasses of this class
        '''
        self.parents = list(parents)
    
    def addParents(self, parents):
        '''
        Add superclasses to this class
        '''
        self.parents.extend(parents)
    
    def removeParents(self, parents):
        '''
        Remove superclasses from this class
        Throws an exception if a parent does not exist
        '''
        for parent in parents:
            if parent in self.parents:
                self.parents.remove(parent)
            else:
                e = parse.itools.CompilerException()
                e.setMessage('Parent does not exist: ' + parent.getIdentifier())
                raise e

    def getTemplateIdentifiers(self):
        '''
        Get the identifiers which are quantified over types
        '''
        return self.templateIds
    
    def setTemplateIdentifiers(self, templateIds):
        '''
        Set the identifiers which are quantified over types
        '''
        self.templateIds = templateIds
    
    def accept(self, visitor):
        '''
        Overridden to dispatch correctly
        '''
        visitor.visitClass(self)
    
    def getInterfaces(self):
        '''
        Retrieve the interfaces implemented by this class
        '''
        return self.interfaces 
    
    def setInterfaces(self, interfaces):
        '''
        Set the interfaces implemented by this class
        '''
        self.interfaces = list(interfaces)
    
    def getInterfacesAll(self):
        '''
        Retrieve the interfaces implemented by this class using the 'implements-all' directive
        '''
        return self.interfaces_all
    
    def setInterfacesAll(self, interfaces):
        '''
        Set the interfaces fully implemented by this class
        '''
        self.interfaces_all = list(interfaces)
    
    def addInterfaces(self, interfaces):
        '''
        Add to the interfaces implemented by this class
        '''
        self.interfaces.extend(interfaces)

    def addInterfacesAll(self, interfaces):
        '''
        Add to the interfaces fully implemented by this class
        '''
        self.interfaces_all.extend(interfaces)
        
    def removeInterfaces(self, interfaces):
        '''
        Remove from the interfaces implemented by this class
        Throws an exception if an interface does not exist
        '''
        for interface in interfaces:
            if interface in self.interfaces:
                self.interfaces.remove(interface)
            elif interface in self.interfaces_all:
                self.interfaces_all.remove(interface)
            else:
                e = CompilerException()
                e.setMessage('Interface does not exist: ' + interface.getIdentifier())
                raise e
    
    def getMethods(self):
        '''
        Retrieve the union of all methods supported by this interface
        '''
        return self.methods
    
    def setMethods(self, methods):
        '''
        Set the union of all methods supported by this interface
        '''
        self.methods = list(methods)
    
    def addMethods(self, methods):
        '''
        Add to the union of all methods supported by this interface
        Method uniqueness is decided only the the method name, keeping the most recent one
        '''
        for method in methods:
            for m in self.methods:
                if m.getIdentifier() == method.getIdentifier():
                    self.methods.remove(m)
                    break
            self.methods.append(method)
    
    def removeMethods(self, methods):
        '''
        Remove from the union of all methods supported by this interface
        Throws an exception if a method does not exist
        '''
        for method in methods:
            for m in self.methods:
                if m.getIdentifier() == method.getIdentifier():
                    self.methods.remove(m)
                    break
    def getImplementedMethods(self):
        '''
        Retrieve the set of methods implemented by this class
        '''
        return self.implementedMethods
    
    def setImplementedMethods(self, methods):
        '''
        Set the set of methods implemented by this class
        '''
        self.implementedMethods = methods
    
    def addImplementedMethods(self, methods):
        '''
        Add to the set of methods implemented by this class
        Method uniqueness is decided only the the method name, keeping the oldest one
        '''
        for method in methods:
            found = 0
            for m in self.implementedMethods:
                if m.getIdentifier() == method.getIdentifier():
                    found = 1
                    break
            if not (found):
                self.implementedMethods.append(method)
    
    def removeImplementedMethods(self, methods):
        '''
        Remove from the set of methods implemented by this class
        Throws an exception if a method does not exist
        '''
        for implementedMethod in methods:
            if implementedMethod in self.implementedMethods:
                self.implementedMethods.remove(implementedMethod)
            else:
                e = CompilerException()
                e.setMessage('Implemented method does not exist: ' + implementedMethod.getIdentifier())
                raise e
    # Ending class methods section
    pass


class Interface(Type):
    '''
    A SIDL interface
    The children of this node are methods defined in the interface
    '''
    # Starting class methods section
    pass
    
    def __init__(self):
        self.parents = []
        self.methods = []
        Type.__init__(self)
        self.implementsall = False
    
    def accept(self, visitor):
        '''
        Overridden to dispatch correctly
        '''
        visitor.visitInterface(self)
    
    def getParents(self):
        '''
        Retrieve the superinterfaces of this interface
        '''
        return self.parents
    
    def getParentIds(self):
        lst = []
        for p in self.parents:
            lst.append(p.getFullIdentifier())
        return lst
    
    def setParents(self, parents):
        '''
        Set the superinterfaces of this interface
        '''
        self.parents = list(parents)
    
    def addParents(self, parents):
        '''
        Add superinterfaces to this interface
        '''
        self.parents.extend(parents)
    
    def removeParents(self, parents):
        '''
        Remove superinterfaces from this interface
        Throws an exception if a parent does not exist
        '''
        for parent in parents:
            if parent in self.parents:
                self.parents.remove(parent)
            else:
                e = parse.itools.CompilerException()
                e.setMessage('Parent does not exist: ' + parent.getIdentifier())
                raise e
    
    def getMethods(self):
        '''
        Retrieve the union of all methods supported by this interface
        '''
        return self.methods
    
    def setMethods(self, methods):
        '''
        Set the union of all methods supported by this interface
        '''
        self.methods = list(methods)
    
    def addMethods(self, methods):
        '''
        Add to the union of all methods supported by this interface
        Method uniqueness is decided only the the method name, keeping the most recent one
        '''
        for method in methods:
            for m in self.methods:
                if m.getIdentifier() == method.getIdentifier():
                    self.methods.remove(m)
                    break
            self.methods.append(method)
    
    def removeMethods(self, methods):
        '''
        Remove from the union of all methods supported by this interface
        Throws an exception if a method does not exist
        '''
        for method in methods:
            for m in self.methods:
                if m.getIdentifier() == method.getIdentifier():
                    self.methods.remove(m)
                    break
    
    # These are only used in temporary interface objects in Class
    def getImplementsAll(self):            
        return self.implementsall
    def setImplementsAll(self, val):
        self.implementsall = val
    
    # Ending class methods section
    pass

class Iterator(Vertex):
    '''
    A SIDL iterator
    '''

    def __init__(self):
        self.setIdentifier('iterator')
        self.type = None
        Vertex.__init__(self)
    
    def accept(self, visitor):
        '''
        Overridden to dispatch correctly
        '''
        visitor.visitIterator(self)
    
    def getFullIdentifier(self):
        '''
        Need to override this to calculate the fully qualified type name
        '''
        if self.getIdentifier() is None:
            return 'iterator over ' + self.getType().getFullIdentifier()
        else:
            return self.getIdentifier()
    
    def getType(self):
        '''
        Retrieve the element type
        '''
        return self.type
    
    def setType(self, type):
        '''
        Set the element type
        '''
        self.type = type
    # Ending class methods section
    pass

class Method(Vertex):
    '''
    A SIDL method
    The children of this node are the method parameters
    '''
    
    def __init__(self):
        self.returnParameter = None
        self.exceptions = []
        self.isStatic = 0
        self.isInternal = 0
        self.templateIds = []
        self.isVirtual = 0
        self.purpose = []
        Vertex.__init__(self)
    
    def getTemplateIdentifiers(self):
        '''
        Get the identifiers which are quantified over types
        '''
        return self.templateIds
    
    def setTemplateIdentifiers(self, templateIds):
        '''
        Set the identifiers which are quantified over types
        '''
        self.templateIds = templateIds
    
    def accept(self, visitor):
        '''
        Overridden to dispatch correctly
        '''
        visitor.visitMethod(self)
    
    def getFullIdentifier(self):
        '''
        Need to override this to calculate the fully qualified method name
        '''
        id = self.getIdentifier()
        parent = self.getParent()
        if not (parent is None):
            return parent.getFullIdentifier() + '.' + id
        return id
    
    def getReturnParameter(self):
        '''
        Retrieve the return parameter
        '''
        return self.returnParameter
    
    def setReturnParameter(self, parameter):
        '''
        Set the return parameter
        '''
        self.returnParameter = parameter
    
    def getExceptions(self):
        '''
        Retrieve the exceptions thrown by the method
        '''
        return self.exceptions
    
    def setExceptions(self, exceptions):
        '''
        Set the exceptions thrown by the method
        '''
        self.exceptions = [exception for exception in exceptions]
    
    def addExceptions(self, exceptions):
        '''
        Add to the exceptions thrown by the method
        '''
        self.exceptions.extend(exceptions)
    
    def removeExceptions(self, exceptions):
        '''
        Remove from the exceptions thrown by the method
        Throws an exception if an exception does not exist
        '''
        for exception in exceptions:
            if exception in self.exceptions:
                self.exceptions.remove(exception)
            else:
                e = CompilerException()
                e.setMessage('Exception does not exist: ' + exception.getIdentifier())
                raise e
    
    def getStatic(self):
        '''
        Retrieve the flag indicating whether the method is static
        '''
        return self.isStatic
    
    def setStatic(self, isStatic):
        '''
        Set the flag indicating whether the method is static
        '''
        self.isStatic = isStatic
    
    def getInternal(self):
        '''
        Retrieve the flag indicating whether the method is not present in the SIDL interface
        '''
        return self.isInternal
    
    def setInternal(self, isInternal):
        '''
        Set the flag indicating whether the method is not present in the SIDL interface
        '''
        self.isInternal = isInternal
    
    def getVirtual(self):
        '''
        Retrieve the flag indicating whether this method may be inherited, or must be implemented by every class
        '''
        return self.isVirtual
    
    def setVirtual(self, isVirtual):
        '''
        Set the flag indicating whether this method may be inherited, or must be implemented by every class
        '''
        self.isVirtual = isVirtual
    
    def getPurpose(self):
        '''
        NOTICE: These should be parse.itools.CodePurpose when this gets fixed
        Retrieve the list of purposes for which this method is defined
        '''
        return self.purpose
    
    def setPurpose(self, purpose):
        '''
        Set the list of purposes for which this method is defined
        '''
        self.purpose = list(purpose)
    
    def addPurpose(self, purpose):
        '''
        Add purposes in which the method is defined
        '''
        self.purpose.extend(purpose)
    
    def removePurpose(self, purpose):
        '''
        Remove purposes in which the method is defined
        Throws an exception if a purpose does not exist
        '''
        for p in purpose:
            if p in self.purpose:
                self.purpose.remove(p)
            else:
                e = CompilerException()
                e.setMessage('Purpose does not exist: ' + p.getIdentifier())
                raise e
    
    def getInParameters(self):
        '''
        Retrieve the parameters whose values will be read on input
        '''
        import parse.itools.ParameterAccessMode
        inParameters = []
        for child in self.getChildren():
            parameter = parse.itools.Parameter.Parameter(child)
            mode = parameter.getAccessMode()
            if (mode == parse.itools.ParameterAccessMode.IN or mode == parse.itools.ParameterAccessMode.INOUT):
                inParameters.append(parameter)
        return inParameters
    
    def getOutParameters(self):
        '''
        Retrieve the parameters which will return values, including the return value
        '''
        import parse.itools.ParameterAccessMode
        outParameters = []
        if not (self.getReturnParameter() is None):
            outParameters.append(self.getReturnParameter())
        for child in self.getChildren():
            parameter = parse.itools.Parameter.Parameter(child)
            mode = parameter.getAccessMode()
            if (mode == parse.itools.ParameterAccessMode.OUT or mode == parse.itools.ParameterAccessMode.INOUT):
                outParameters.append(parameter)
        return outParameters
    
    # Ending class methods section
    pass

class Package(Vertex):
    '''
    A SIDL namespace
    '''
    
    def __init__(self,parent=None):
        self.templateIds = []
        self.version = None
        self.final = False
        Vertex.__init__(self,parent)
    
    def getVersion(self):
        '''
        Get the version number
        '''
        return self.version
    
    def setVersion(self, version):
        '''
        Set the version number
        '''
        self.version = version
        
    def getTemplateIdentifiers(self):
        '''
        Get the identifiers which are quantified over types
        '''
        return self.templateIds
    
    def setTemplateIdentifiers(self, templateIds):
        '''
        Set the identifiers which are quantified over types
        '''
        self.templateIds = templateIds
        
    def getFinalAttr(self):
        '''
        Return True if package is final
        '''
        return self.final
    
    def setFinalAttr(self, val):
        '''
        Set the package final attribute to True or False
        '''
        self.final = val
    
    def accept(self, visitor):
        '''
        Overridden to dispatch correctly
        '''
        visitor.visitPackage(self)
    
    def getFullIdentifier(self):
        '''
        Need to override this to calculate the fully qualified package name
        '''
        id = self.getIdentifier()
        parent = self.getParent()
        if (not (parent is None) and parent.isInstanceOf('parse.itools.elements.Package')):
            return parent.getFullIdentifier() + '.' + id
        return id

    # Ending class methods section
    pass

class Parameter(Vertex):
    '''
    A SIDL method parameter
    '''

    def __init__(self):
        self.type = None
        self.accessMode = parse.itools.ParameterAccessMode.IN
        self.isRequired = 0
        self.dimsizes = []
        self.typeAttr = []
        self.copy = False
        Vertex.__init__(self)
    
    def accept(self, visitor):
        '''
        Overridden to dispatch correctly
        '''
        visitor.visitParameter(self)
    
    def getType(self):
        '''
        Retrieve the parameter type
        '''
        return self.type
    
    def setType(self, type):
        '''
        Set the parameter type
        '''
        self.type = type
    
    def getAccessMode(self):
        '''
        Retrieve the access mode
        '''
        return self.accessMode
    
    def setAccessMode(self, mode):
        '''
        Set the access mode
        '''
        self.accessMode = mode
    
    def getRequired(self):
        '''
        Retrieve the flag indicating whether the parameter is required in a call
        '''
        return self.isRequired
    
    def setRequired(self, isRequired):
        '''
        Set the flag indicating whether the parameter is required in a call
        '''
        self.isRequired = isRequired
    
    def getDimensionSizes(self):
        '''
        Return a list containing the extents in the array in each dimension
        '''
        return self.dimsizes
    
    def setDimensionSizes(self, dimsizelist):
        '''
        Set the list containing the extents in the array in each dimension
        '''
        # TODO check the dimensions 
        self.dimsizes = dimsizelist
        
        
    def getTypeAttributes(self):
        '''
        Return the type attributes list
        '''
        return self.typeAttr
    
    def setTypeAttributes(self, attlist):
        '''
        Set the list of type attributes for this type
        '''
        self.typeAttr = attlist
    
    def addTypeAttribute(self, attr):
        '''
        Add the specified type attribute to the list of attributes for this type
        '''
        if attr not in self.typeAttr:
            self.typeAttr.append(attr)
            
    # Ending class methods section
    pass

class TypeUniverse(Vertex):
    '''
    A set of SIDL types
    '''
    def __init__(self):
        self.types = []
        Vertex.__init__(self)
    
    def accept(self, visitor):
        '''
        Overridden to dispatch correctly
        '''
        visitor.visitTypeUniverse(self)
    
    def getTypes(self):
        '''
        Retrieve the universe of types
        '''
        return self.types
    
    def setTypes(self, types):
        '''
        Set the universe of types
        '''
        self.types = list(types)
    
    def addTypes(self, types):
        '''
        Augment the universe of types
        '''
        self.types.extend(types)
    
    def removeTypes(self, types):
        '''
        Diminish the universe of types
        Throws an exception if a type does not exist
        '''
        for type in types:
            if type in self.types:
                self.types.remove(type)
            else:
                e = parse.itools.CompilerException()
                e.setMessage('Type does not exist: ' + type.getIdentifier())
                raise e
    # Ending class methods section
    pass
