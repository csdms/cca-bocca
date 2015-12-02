from parse.itools.elements import Class, Interface, Package, Type

class SIDL(object):
  def __init__(self):
    self.typeMap = self.createTypeMap()
    return

  def createTypeMap(self):

    typeMap = {}
    for typeName in ['bool', 'char', 'dcomplex', 'double', 'fcomplex', 'float', 'int', 'long', 'opaque', 'string', 'void']:
      sidlType = parse.itools.Type.Type()
      sidlType.setIdentifier(typeName)
      sidlType.setBaseType(1)
      typeMap[typeName] = sidlType
    return typeMap

  def getLoader(self, interface):
    for child in self.getBaseInterface(interface).getParent().getChildren():
      if child.getIdentifier() == 'Loader':
        return Class(child)
    raise RuntimeError('Could not find Loader using '+interface.getFullIdentifier())

  def getBasePackage(self, interface):
    return Package(self.getAncestor(interface, 'BaseInterface').getParent())

  def getBaseInterface(self, interface):
    return self.getAncestor(interface, 'BaseInterface')

  def getBaseException(self, exception):
    return self.getAncestor(exception, 'BaseException')

  def getException(self, interface):
    aPackage = self.getBasePackage(interface)
    for child in aPackage.getChildren():
      if child.getIdentifier() == 'ASEException':
        return Class(child)
    return None

  def getAncestor(self, interface, typeName):
    interface = Interface(interface)
    if interface.getFullIdentifier() == typeName:
      return interface
    parents = []
    if interface.isInstanceOf('parse.itools.Class'):
      from parse.itools.elements import Class
      parents.extend(parse.itools.Class.Class(interface).getInterfaces())
    parents.extend(interface.getParents())
    for parent in parents:
      base = self.getAncestor(parent, typeName)
      if base:
        return base
    return None
