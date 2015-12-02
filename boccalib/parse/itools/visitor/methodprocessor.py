# Starting imports section
from parse.itools.elements import *
from parse.itools.visitor.depthfirstvisitor import *

class MethodProcessor(DepthFirstVisitor):
  '''
  Processing of methods for interfaces and classes, including:
  Determining full method lists
  Determining implemented methods for classes
  Adding special methods
  '''
  
  def __init__(self):
    DepthFirstVisitor.__init__(self)
  
  def visitInterface(self, node):
    '''
    Determine the full method list based upon parent interfaces
    '''
    if len(node.getMethods()):
      return None
    for interface in node.getParents():
      interface.accept(self)
      node.addMethods(interface.getMethods())
    node.addMethods(node.getChildren())
  
  def visitClass(self, node):
    '''
    Determine the full method list based upon parent classes and implemented interfaces
    Determine the implemented methods
    '''
    if len(node.getImplementedMethods()):
      return None

    implMethodNames = [m.getIdentifier() for m in node.getChildren()]
    for klass in node.getParents():
      klass.accept(self)
      implMethodNames.extend([m.getIdentifier() for m in klass.getMethods()])
    for interface in node.getInterfaces():
      interface.accept(self)
      node.addMethods(interface.getMethods())
      node.addImplementedMethods([m for m in interface.getMethods() if not (m.getIdentifier() in implMethodNames)])
    for klass in node.getParents():
      node.addMethods(klass.getMethods())
    node.addMethods(node.getChildren())
    node.addImplementedMethods(node.getChildren())
