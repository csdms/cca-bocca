# Starting imports section
pass
import ASE.BaseException
import ASE.BaseInterface
import ASE.Compiler.CompilerException
import ASE.Compiler.SIDL.Array
import ASE.Compiler.SIDL.Class
import ASE.Compiler.SIDL.DepthFirstVisitor
import ASE.Compiler.SIDL.Enumeration
import ASE.Compiler.SIDL.Enumerator
import ASE.Compiler.SIDL.Interface
import ASE.Compiler.SIDL.Iterator
import ASE.Compiler.SIDL.Method
import ASE.Compiler.SIDL.Package
import ASE.Compiler.SIDL.Parameter
import ASE.Compiler.SIDL.Specification
import ASE.Compiler.SIDL.Type
import ASE.Compiler.SIDL.TypeUniverse
import ASE.Compiler.Vertex
# Ending imports section
pass
# Starting static methods section
pass
# Ending static methods section
pass

class Resolver:
  '''
  Name resolution within a set of ASTs
  '''
  # Starting class methods section
  pass
  
  def __init__(self, IORself):
    self.__IORself = IORself
    import ASE.Compiler.SIDL.Attribute
    self.mark = ASE.Compiler.SIDL.Attribute.Attribute()
    self.mark.setName('ASE.Compiler.SIDL.Resolver.mark')
  
  def resolve(self, vertex, root):
    '''
    Resolve "node" to its actual referent in the AST
    The "root" argument is an optional AST for resolving "node"
    '''
    import ASE.Compiler.SIDL.Type
    if ASE.Compiler.SIDL.Type.Type(vertex).getBaseType():
      return vertex
    elif vertex.isInstanceOf('ASE.Compiler.SIDL.Array'):
      import ASE.Compiler.SIDL.Array
      array = ASE.Compiler.SIDL.Array.Array(vertex)
      array.setType(self.resolve(array.getType(), root))
      return vertex
    elif vertex.isInstanceOf('ASE.Compiler.SIDL.Iterator'):
      import ASE.Compiler.SIDL.Iterator
      iterator = ASE.Compiler.SIDL.Iterator.Iterator(vertex)
      iterator.setType(self.resolve(iterator.getType(), root))
      return vertex
    idChain = vertex.getIdentifier().split('.')
    (scope, name) = (idChain[:-(1)], idChain[-(1)])
    if scope:
      vertex = self.differentPackageResolve(root, scope, name)
    else:
      vertex = self.samePackageResolve(vertex, name)
    if vertex:
      return vertex
    raise RuntimeError('Could not resolve ' + str(idChain))
  
  def visitSpecification(self, node):
    '''
    Resolve global classes needed for code generation
    '''
    self.baseInterface = self.resolveInterface('ASE.BaseInterface', node)
    self.baseClass = self.resolveInterface('ASE.BaseClass', node)
    self.baseException = self.resolveInterface('ASE.BaseException', node)
    self.__IORself.visitVertex(node)
  
  def visitTypeUniverse(self, node):
    '''
    Resolve types in the universe
    '''
    types = []
    for type in node.getTypes():
      types.append(self.resolve(type, self.getRoot(node)))
    node.setTypes(types)
  
  def visitInterface(self, node):
    '''
    Resolve parents, then recurse into them
    '''
    if node.hasAttribute(self.mark.getName()):
      return None
    node.addAttribute(self.mark)
    parents = []
    for parent in node.getParents():
      parents.append(self.resolve(parent, self.getRoot(node)))
    if (not (parents) and not (node == self.baseInterface)):
      parents.append(self.baseInterface)
    node.setParents(parents)
    for parent in node.getParents():
      parent.accept(self.__IORself)
    self.__IORself.visitVertex(node)
  
  def visitClass(self, node):
    '''
    Resolve parents and interfaces, then recurse into them
    '''
    if node.hasAttribute(self.mark.getName()):
      return None
    node.addAttribute(self.mark)
    root = self.getRoot(node)
    parents = []
    for parent in node.getParents():
      parents.append(self.resolve(parent, root))
    if (not (parents) and not (node == self.baseClass)):
      parents.append(self.baseClass)
    node.setParents(parents)
    interfaces = []
    for interface in node.getInterfaces():
      interfaces.append(self.resolve(interface, root))
    node.setInterfaces(interfaces)
    for parent in node.getParents():
      parent.accept(self.__IORself)
    for interface in node.getInterfaces():
      interface.accept(self.__IORself)
    self.__IORself.visitVertex(node)
  
  def visitMethod(self, node):
    '''
    Resolve return type and exceptions
    Add SIDL.BaseException by default
    '''
    if not (node.getReturnParameter() is None):
      node.getReturnParameter().accept(self.__IORself)
    exceptions = []
    for exception in node.getExceptions():
      exceptions.append(self.resolve(exception, self.getRoot(node)))
    if not (self.baseException in exceptions):
      exceptions.append(self.baseException)
    for exception in exceptions:
      exception.accept(self.__IORself)
    node.setExceptions(exceptions)
    self.__IORself.visitVertex(node)
  
  def visitEnumeration(self, node):
    '''
    Initialize enumeration values
    '''
    if node.getInitialized():
      return None
    values = []
    for child in node.getChildren():
      enumerator = ASE.Compiler.SIDL.Enumerator.Enumerator(child)
      if enumerator.getInitialized():
        value = enumerator.getValue()
        if value in values:
          raise RuntimeError('Repeated enumeration value ' + str(value) + ' for "' + enumerator.getIdentifier() + '" in ' + node.getFullIdentifier())
        values.append(value)
    values.sort()
    for child in node.getChildren():
      enumerator = ASE.Compiler.SIDL.Enumerator.Enumerator(child)
      if not (enumerator.getInitialized()):
        if len(values):
          value = values[-(1)] + 1
        else:
          value = 0
        if value in values:
          raise RuntimeError('Invalid processing of enumeration')
        values.append(value)
        enumerator.setValue(value)
        values.append(value)
    node.setInitialized(1)
  
  def visitParameter(self, node):
    '''
    Resolve the parameter type
    '''
    typeNode = self.resolve(node.getType(), self.getRoot(node))
    node.setType(typeNode)
    if not (typeNode.isInstanceOf('ASE.Compiler.SIDL.Interface')):
      typeNode.accept(self.__IORself)
  # Ending class methods section
  pass
  
  def getRoot(self, vertex):
    '''
    Return the root of the tree containing vertex
    '''
    root = vertex
    while root.getParent():
      root = root.getParent()
    return root
  
  def findPackage(self, root, packageName):
    '''
    Search for the package in root breadth first, returning None if it is not present
    '''
    if (root.isInstanceOf('ASE.Compiler.SIDL.Specification') or root.isInstanceOf('ASE.Compiler.SIDL.Package')):
      if root.getIdentifier() == packageName:
        return root
      else:
        for child in root.getChildren():
          node = self.findPackage(child, packageName)
          if node:
            return node
    return None
  
  def findType(self, package, typeName):
    '''
    Locate a type in "package", returning None if it is not found
       - This function does not handle nested packages
    '''
    for child in package.getChildren():
      if typeName == child.getIdentifier():
        return child
    return None
  
  def differentPackageResolve(self, root, scope, name):
    trees = list(self.__IORself.getRepository())
    if root:
      trees.append(root)
    packageRoot = root
    for tree in trees:
      for packageName in scope:
        package = self.findPackage(tree, packageName)
        if package:
          packageRoot = package
        else:
          packageRoot = None
          break
      if packageRoot:
        vertex = self.findType(packageRoot, name)
        if vertex:
          return vertex
    if not (packageRoot):
      raise RuntimeError('Could not resolve ' + name + ' in ' + str(scope))
    return None
  
  def samePackageResolve(self, vertex, name):
    '''
    The type must lie in same package as the referrer
       - Assume the given vertex has the referrer as its parent so the nearest enclosing package is reached
    '''
    root = vertex
    while not (root.isInstanceOf('ASE.Compiler.SIDL.Package')):
      root = root.getParent()
    return self.findType(root, name)
  
  def resolveInterface(self, identifier, root):
    vertex = ASE.Compiler.SIDL.Interface.Interface()
    vertex.setIdentifier(identifier)
    vertex.setBaseType(0)
    return self.__IORself.resolve(vertex, root)
