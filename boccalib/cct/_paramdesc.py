def validtype(type, name):
  if type in [
'bool', 
'int', 
'long', 
'float', 
'double', 
'fcomplex', 
'dcomplex', 
'string', 
'array<bool>',
'array<int>',
'array<long>',
'array<float>',
'array<double>',
'array<fcomplex>',
'array<dcomplex>',
'array<string>'
]:
    return type

  if type == "integer": return "int"
  if type == "Int": return "int"
  if type == "Long": return "long"
  if type == "Float": return "float"
  if type == "Double": return "double"
  if type == "Fcomplex": return "fcomplex"
  if type == "Dcomplex": return "dcomplex"
  if type == "String": return "string"
  if type == "boolean": return "bool"
  if type == "Boolean": return "bool"
  if type == "Bool": return "bool"
  if type == "BoolArray": return "array<bool>"
  if type == "BooleanArray": return "array<bool>"
  if type == "IntArray": return "array<int>"
  if type == "LongArray": return "array<long>"
  if type == "FloatArray": return "array<float>"
  if type == "DoubleArray": return "array<double>"
  if type == "FcomplexArray": return "array<fcomplex>"
  if type == "DcomplexArray": return "array<dcomplex>"
  if type == "StringArray": return "array<string>"

  e = Exception("invalid parameter type for "+name+":" +type)
  raise e

def validname(name):
   if not name or name[0] == '_':
     e = Exception("parameter names must be defined and may not start with _")
     raise e
   return name

class Param:
  type=""
  name=""
  help=""
  prompt=""
  dflt=""
  lo=""
  hi=""
  choices=[]
  bounded=False
  enumerated=False

  def __init__(self, name, type, dflt, prompt, help, lo=None, hi=None, choices=None):
    self.type = validtype(type, name)
    self.name = validname(name)
    self.dflt = dflt
    self.prompt = prompt
    self.help = help
    if lo and hi and lo < hi:
      bounded = True
      self.lo = lo
      self.hi = hi
    if choices:
      enumerated = True
      self.choices = choices

  
class Group:
  name=""
  keys=[]

  def __init__(self,name):
    self.name = name

  def addKey(self, name):
    if not name in keys:
      keys.append(name)
  

class ParameterPortDesc(dict):
  """ Internal attributes all start with _. Rest are parameters.
The user gets the default "shared parameters" title and group
if they don't set a groupname first and a title sometime.
"""

  self["_currentgroup"] = "Shared Parameters"
  self["_title"] = self["_currentgroup"]
  self["_groups"] = []; # group names in order created.
  self["_groupdata"] = dict(); # groupname: Group pairs
  self["_keys"] = [] ; # in order added.


  def addParam(self, name, type, dflt, prompt, help, range, choices):
    if len(self["_groups"]) < 1:
      self.addGroup(self["_currentgroup"])

    if not name in self["_keys"]:
      p = Param(key, type, dflt, prompt, help, range[0], range[1], choices)
      self["_keys"].append(key)
      self[key] = p

    g = self["_groupdata"][ self["_currentgroup"] ]
    g.addKey(name)


  def addGroup(self, name):
    if not name in self[_groups]:
      self["_currentgroup"] = validname(name)
      g = Group(self["_currentgroup"])
      self["_groups"].append(self["_currentgroup"])
      self["_groupdata"][name] = g


  def setBatchTitle(self, title):
    self["_title"] =  title


  def getGroupNames(self):
    return self["_groups"]


  def getTitle(self):
    return self["_title"]


  def getGroup(self, groupname):
    return self["_groupdata"][groupname]

