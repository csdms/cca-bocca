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

class TypeFinder:
  '''
  Finds a type specified by fully qualified identifier in the given tree
  '''
  # Starting class methods section
  pass
  
  def __init__(self, IORself):
    self.__IORself = IORself
    self.name = ''
    self.type = None
  
  def getName(self):
    '''
    Get the fully qualified type name
    '''
    return self.name
  
  def setName(self, name):
    '''
    Set the fully qualified type name
    '''
    self.name = name
  
  def hasType(self):
    '''
    Determine whether the type was found
    '''
    return not (self.type is None)
  
  def getType(self):
    '''
    Return the type
    '''
    return self.type
  
  def visitEnumeration(self, node):
    if node.getFullIdentifier() == self.name:
      self.type = node
  
  def visitInterface(self, node):
    if node.getFullIdentifier() == self.name:
      self.type = node
  
  def visitClass(self, node):
    if node.getFullIdentifier() == self.name:
      self.type = node
  # Ending class methods section
  pass
