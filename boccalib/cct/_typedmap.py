
class TypedMap(dict):
  """ Extending hash for key: (type, value) with some conveniences.
Any function that causes a dict exception will for bogus input.
"""
  def __init__(self):
    dict.__init__(self)

  def getType(self, key):
    return self[key][0]

  def getValue(self,key):
    return self[key][1]

  def addVal(self, key, type, value):
    """ Ignores duplicate add calls. """
    if not self.has_key(key):
      self[key] = (type, value)
    return

  def setValue(self, key, type, value):
    """sets value if type matches or unknown."""
    if not self.has_key(key):
      self[key] = (type, value)
    else:
      if self[key][0] == type:
        self[key] = (type, value)

