
from cct._debug import *

class Nametab:
  """ Object to manage alias groups with very loose construction rules and no io.
Shovel in a raft of alias pairs and the canonical name for each groups is 
least name by alpha sort if more than two names in group, else it is first
from time of definition.
 """
  def __init__(self):
      self.names = dict()

  def addName(self, name):
      print >> DEBUGSTREAM, "nametab_addName:", name
      old = self.findGroup(name)
      if len(old) == 0:
          self.names[name] = [name]

  def printtab(self):
     print>> DEBUGSTREAM,  "nametab:", self.names

  def findGroup(self,name):
     print >> DEBUGSTREAM, "nametab_findGroup:", name
     result=[]
     if name in self.names.keys():
         result.append(name)
     else:
         for i in self.names.keys():
             if name in self.names[i]:
                 result.append(i)
     print >> DEBUGSTREAM, "nametab_findGroup result:", result
     return result       

  def addAlias(self, org, new):
      print >> DEBUGSTREAM, "nametab_addAlias:", org, new
      orgnames = self.findGroup(org)
      newnames = self.findGroup(new)
      if len(orgnames) < 1 and len(newnames) < 1:
          # both names new
          self.names[org]=[org,new]
          return
      # must merge newnames and orgnames
      result=[]
      for i in orgnames:
          prev = self.names[i]
          result.extend(prev)
      for k in newnames:
          prev = self.names[k]
          result.extend(prev)
      unique = dict()
      unique[org] = 1
      unique[new] = 1
      for k in result:
          unique[k] = 1
      newlist = unique.keys()
      newlist.sort()
      newkey= newlist[0]
      for i in orgnames:
          del self.names[i]
      for k in newnames:
          del self.names[k]
      self.names[newkey] = newlist
      return

  def canonicalName(self, name):
      print >> DEBUGSTREAM, "nametab_canonical:", name
      groups = self.findGroup(name)
      if len(groups) > 1:
          print >> DEBUGSTREAM, "Ambiguity canonicalizing name:", name, ".  In groups ", groups
          return groups[0]
      if len(groups) < 1:
          print >> DEBUGSTREAM, "Unknown name while canonicalizing name:", name
          return ""
      return groups[0]

if __name__ == "__main__":
  t=Nametab()
  t.addName("b")
  t.printtab()
  t.canonicalName("b")
  t.addAlias("c","d")
  t.printtab()
  t.addAlias("a","b")
  t.canonicalName("b")
  t.printtab()
  t.canonicalName("d")
  t.addAlias("c","b")
  t.printtab()
  t.canonicalName("d")
  t.canonicalName("q")
