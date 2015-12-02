from _err import err
from _util import Globals

                
class PortInstance:
    '''Top-level class for storing SIDL type information'''
    
    def __init__(self, typename, name=None, location='%local%'):
        self._type = typename
        self._location = location
        if not name: 
            self._name = name.split('.')[-1]
        else:
            self._name = name
        pass
            
    def getName(self):
        return self._name
    
    def setName(self, name):
        self._name = name
          
    def getLocation(self):
        return self._location
    
    def setLocation(self, location):
        self._location = location
        
    def getType(self):
        return self._type

    def setType(self, typename):
        self._type = typename
        
    def __repr__(self):
        return "('%s','%s','%s')" % (self._type,self._name,self._location)
    
    def prettystr(self):
        s = ''
        s +=  '\t  ' + self._type  + ', port name: ' + self._name
        if self._location != '%local%':
            project, graph = Globals().getProjectAndGraph()
            s += ', location = ' + project.getDefaultValue(self._type,'External')
        else:
            s += ', local'
        return s
    
    
if __name__ == '__main__':
    # Local tests
    
    pi = PortInstance('pkg.MyPort', 'MyPortInstance1', '%local%')

    
