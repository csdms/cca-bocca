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

class DependencyAnalyzer:
  '''
  Determine dependencies
  '''
  # Starting class methods section
  pass
  
  def __init__(self, IORself):
    self.__IORself = IORself
    import ASE.Compiler.SIDL.Attribute
    import ASE.Compiler.SIDL.Language
    self.SIDL = ASE.Compiler.SIDL.Language.SIDL()
    self.mark = ASE.Compiler.SIDL.Attribute.Attribute()
    self.mark.setName('ASE.Compiler.SIDL.DependencyAnalyzer.mark')
  
  def visitTypeUniverse(self, node):
    '''
    Record dependence on types
    '''
    node.addDependencies(node.getTypes())
  
  def visitArray(self, node):
    '''
    Record dependence on type
    '''
    type = node.getType()
    type.accept(self.__IORself)
    if type.isInstanceOf('ASE.Compiler.SIDL.TypeUniverse'):
      node.addDependencies(type.getDependencies())
    else:
      node.addDependencies([type])
  
  def visitIterator(self, node):
    '''
    Record dependence on type
    '''
    type = node.getType()
    type.accept(self.__IORself)
    if type.isInstanceOf('ASE.Compiler.SIDL.TypeUniverse'):
      node.addDependencies(type.getDependencies())
    else:
      node.addDependencies([type])
  
  def visitInterface(self, node):
    '''
    Record dependence on methods
    '''
    if node.hasAttribute(self.mark.getName()):
      return None
    node.addAttribute(self.mark)
    for parent in node.getParents():
      parent.accept(self.__IORself)
    node.addDependencies(node.getParents())
    self.__IORself.visitVertex(node)
    if node.getFullIdentifier() == 'ASE.BaseInterface':
      for method in node.getMethods():
        node.addDependencies([d for d in method.getDependencies()])
    else:
      for method in node.getMethods():
        node.addDependencies([d for d in method.getDependencies()])
  
  def visitClass(self, node):
    '''
    Record dependence on methods
    '''
    if node.hasAttribute(self.mark.getName()):
      return None
    node.addAttribute(self.mark)
    for parent in node.getParents():
      parent.accept(self.__IORself)
    node.addDependencies(node.getParents())
    for interface in node.getInterfaces():
      interface.accept(self.__IORself)
    node.addDependencies(node.getInterfaces())
    self.__IORself.visitVertex(node)
    for method in node.getMethods():
      node.addDependencies([d for d in method.getDependencies()])
  
  def visitParameter(self, node):
    '''
    Record dependence on type
    '''
    type = node.getType()
    type.accept(self.__IORself)
    if type.isInstanceOf('ASE.Compiler.SIDL.Array'):
      node.addDependencies(type.getDependencies())
    elif type.isInstanceOf('ASE.Compiler.SIDL.Iterator'):
      node.addDependencies(type.getDependencies())
    elif type.isInstanceOf('ASE.Compiler.SIDL.TypeUniverse'):
      node.addDependencies(type.getDependencies())
    else:
      node.addDependencies([type])
  
  def visitMethod(self, node):
    '''
    Record dependence on parameters
    '''
    import ASE.Compiler.SIDL.Parameter
    self.__IORself.visitVertex(node)
    if not (node.getReturnParameter() is None):
      node.getReturnParameter().accept(self.__IORself)
      node.addDependencies(node.getReturnParameter().getDependencies())
    for child in node.getChildren():
      node.addDependencies(ASE.Compiler.SIDL.Parameter.Parameter(child).getDependencies())
    node.addDependencies(node.getExceptions())
  # Ending class methods section
  pass
