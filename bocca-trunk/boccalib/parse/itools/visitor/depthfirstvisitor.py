from parse.itools.elements import *

class DepthFirstVisitor(Visitor):
    '''
    Traverses the AST in a depth first manner
    '''

    def __init__(self):
        Visitor.__init__(self)
    
    def traverseVertex(self, vertex):
        '''
        Traverse each edge of this vertex
        '''
        self.setVertexSeen(vertex, 1)
        if self.getReverseEdges():
            neighbors = [vertex.getParent()]
        else:
            neighbors = vertex.getChildren()
        for neighbor in neighbors:
            neighbor.accept(self)

