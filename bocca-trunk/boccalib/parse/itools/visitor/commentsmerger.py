import sys
from parse.itools.elements import *
from parse.itools.visitor.depthfirstvisitor import *
import parse.itools.ParameterAccessMode

class CommentsMerger(DepthFirstVisitor):
    '''
    Prints an AST to stdout as SIDL source
    '''
    # Starting class methods section
    pass
    
    def __init__(self, comments):
        self.comments = comments
        self.startlines = {}
        self.endlines = {}
        self.top_node = None
        DepthFirstVisitor.__init__(self)

    def addNode(self, node):
        lineno = node.getLineNumber()
        endlineno = node.getEndLineNumber()
        if lineno:
            if lineno not in self.startlines.keys():
                self.startlines[lineno] = []
            self.startlines[lineno].append(node)
        if endlineno:
            if endlineno not in self.endlines.keys():
                self.endlines[endlineno] = []
            self.endlines[endlineno].append(node)
        self.visitVertex(node)
        
    def visitPackage(self,node):
        self.addNode(node)

    def visitType(self,node):
        self.handleChildren(node)
        pass
        
    def visitEnumeration(self,node):
        self.addNode(node)
        
    def visitEnumerator(self,node):
        self.addNode(node)
        
    def visitArray(self,node):
        self.handleChildren(node)
        pass
        
    def visitInterface(self,node):
        self.addNode(node)
    
    def visitClass(self,node):
        self.addNode(node)
        
    def visitParameter(self,node):
        self.addNode(node)

    def visitMethod(self,node):
        self.addNode(node)
  
    def setTopNode(self,node):
        self.top_node = node
    
    def doMerge(self):
        allcomments = self.comments.getComments()
        startkeys = self.startlines.keys()
        startkeys.sort()
        endkeys = self.endlines.keys()
        endkeys.sort()
        
        # Try to determine what the closest (in terms of number of lines) AST element is.
        for commentEndLine in allcomments.keys():
            comments = allcomments[commentEndLine]   # list of (str,int) tuples contaning comments and their starting lines
            for comment in comments:
                commentStartLine = comment[1]
                #print 'Comment:\n' + comment[0]
                
                # Search elements after the comment
                line = commentEndLine  # the last comment line
                while line not in endkeys and line <= endkeys[-1]:
                    line += 1
                endline = line
                line = commentEndLine
                while line not in startkeys and line < endline:
                    line += 1
                if endline <= line: theline = endline
                else: theline = line
                
                #print 'comment lines: ' + str(commentStartLine) + '-' + str(commentEndLine)
                #print 'beforeline: ' + str(beforeline) + '    afterline: ' + str(afterline)

                # Associate the comment with the succeeding node
                if theline in endkeys:
                    node = self.endlines[theline][0]
                    if node.getLineNumber() == node.getEndLineNumber():
                        node.appendStartComment(comment[0])
                    else:
                        #print 'setting end comment for ' + str(node.getIdentifier())+ ', on lines ' + str(node.getLineNumber()) + '-' + str(node.getEndLineNumber())
                        #print 'comment: ' + comment[0]
                        #print '\n*********************************************************************'
                        node.appendEndComment(comment[0])
                elif theline in startkeys:
                    node = self.startlines[theline][0]
                    node.appendStartComment(comment[0])
                    
                # Check the special case of comments on the same line as }
                #if commentStartLine in endkeys:
                #    self.endlines[commentStartLine][0].appendEndComment(comment[0])

        return

            
            
            
            
        return
        
    def __repr__(self):
        return str(self.startlines)
        