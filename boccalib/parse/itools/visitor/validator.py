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

class Validator:
  '''
  Verify correctness of the AST
  '''
  # Starting class methods section
  pass
  
  def __init__(self, IORself):
    self.__IORself = IORself
  
  def visitArray(self, node):
    '''
    Check that array is not nested
    '''
    if node.getType().isInstanceOf('ASE.Compiler.SIDL.Array'):
      raise RuntimeError('Array ' + node.getFullIdentifier() + ' cannot be nested')
  
  def visitIterator(self, node):
    '''
    Check that iterator is not nested
    '''
    if node.getType().isInstanceOf('ASE.Compiler.SIDL.Iterator'):
      raise RuntimeError('Iterator ' + node.getFullIdentifier() + ' cannot be nested')
  
  def visitEnumeration(self, node):
    '''
    Check that children are enumerators
    '''
    if not (node.getParent().isInstanceOf('ASE.Compiler.SIDL.Package')):
      raise RuntimeError('Enumeration ' + node.getFullIdentifier() + ' can only have a Package as a parent')
    for child in node.getChildren():
      if not (child.isInstanceOf('ASE.Compiler.SIDL.Enumerator')):
        raise RuntimeError('Enumeration ' + node.getFullIdentifier() + ' can only have Enumerators as children')
  
  def visitInterface(self, node):
    '''
    Check that parents are interfaces
    '''
    if not (node.getParent().isInstanceOf('ASE.Compiler.SIDL.Package')):
      raise RuntimeError('Interface ' + node.getFullIdentifier() + ' can only have a Package as a parent')
    for parent in node.getParents():
      if not (parent.isInstanceOf('ASE.Compiler.SIDL.Interface')):
        raise RuntimeError('Interface ' + node.getFullIdentifier() + ' can only have Interfaces as parents')
      if parent.isInstanceOf('ASE.Compiler.SIDL.Class'):
        raise RuntimeError('Interface ' + node.getFullIdentifier() + ' cannot have Classes as parents')
      if parent.isSame(node):
        raise RuntimeError('Interface ' + node.getFullIdentifier() + ' cannot have itself as a parent')
  
  def visitClass(self, node):
    '''
    Check that parents are classes
    Check that it only implements interfaces
    '''
    if not (node.getParent().isInstanceOf('ASE.Compiler.SIDL.Package')):
      raise RuntimeError('Class ' + node.getFullIdentifier() + ' can only have a Package as a parent')
    for parent in node.getParents():
      if not (parent.isInstanceOf('ASE.Compiler.SIDL.Class')):
        raise RuntimeError('Class ' + node.getFullIdentifier() + ' can only have Classes as parents')
      if parent.isSame(node):
        raise RuntimeError('Class ' + node.getFullIdentifier() + ' cannot have itself as a parent')
    for inf in node.getInterfaces():
      if inf.isInstanceOf('ASE.Compiler.SIDL.Class'):
        raise RuntimeError('Interface ' + inf.getFullIdentifier() + ' for Class ' + node.getFullIdentifier() + ' cannot also be a class')
  
  def visitMethod(self, node):
    '''
    Check that parent is an interface
    Check that children are parameters
    '''
    if not (node.getParent().isInstanceOf('ASE.Compiler.SIDL.Interface')):
      raise RuntimeError('Method ' + node.getFullIdentifier() + ' can only have an Interface as a parent')
    for child in node.getChildren():
      if not (child.isInstanceOf('ASE.Compiler.SIDL.Parameter')):
        raise RuntimeError('Method ' + node.getFullIdentifier() + ' can only have Parameters as children')
  # Ending class methods section
  pass
