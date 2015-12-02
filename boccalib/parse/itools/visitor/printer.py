import sys, re
from parse.itools.elements import *
from parse.itools.visitor.depthfirstvisitor import *
import parse.itools.ParameterAccessMode

class Printer(DepthFirstVisitor):
    '''
    Prints an AST to stdout as SIDL source
    '''
    # Starting class methods section
    pass
    
    def __init__(self, tab='    ', outstream = sys.stdout, initialIndent=0, commentExcludeList=[]):
        self.tab = tab
        self.indentSize = initialIndent
        self.output = outstream
        self.packages = []
        self.declOnly = [0]
        self.commentExcludes = commentExcludeList
        DepthFirstVisitor.__init__(self)
        
    def setOutStream(self, outstream):
        self.output = outstream
        
    def getOutStream(self):
        return self.output
    
    def getTab(self):
        '''
        Retrieve the tab string
        '''
        return self.tab
    
    def setTab(self, tab):
        '''
        Set the tab string
        '''
        self.tab = tab
    
    def getIndentSize(self):
        '''
        Retrieve the number of tabs of the current indent
        '''
        return self.indentSize
    
    def setIndentSize(self, indentSize):
        '''
        Set the number of tabs of the current indent
        Throws an exception on a negative indent size
        '''
        self.indentSize = indentSize
    
    def increaseIndent(self):
        '''
        Increase the index size by one
        '''
        self.indentSize += 1
    
    def decreaseIndent(self):
        '''
        Decrease the index size by one
        Throws an exception on a negative indent size
        '''
        self.indentSize -= 1
        if self.indentSize < 0:
            raise RuntimeError('Indent size decreased below zero: ' + str(self.indentSize))
    
    def indent(self):
        '''
        Output the current indent (the indent size in tabs)
        '''
        for i in range(self.getIndentSize()):
            self.write(self.getTab())
    
    def getIndentString(self):
        istr = ''
        for i in range(self.getIndentSize()):
            istr += self.tab
        return istr
    
    def write(self, s):
        '''
        Output a string
        '''
        self.output.write(s)
    
    def println(self, s):
        '''
        Output a string, properly indented and followed by a newline
        '''
        self.indent()
        self.write(s)
        self.write('\n')
    
    def visitPackage(self, node):
        self.packages.append(node)
        templateIds = node.getTemplateIdentifiers()
        self.writeStartComment(node)
        self.indent()
        self.write('package ' + node.getIdentifier())
        if len(templateIds):
            self.write('[')
            for (t, id) in enumerate(templateIds):
                if t > 0:
                    self.write(', ')
                self.write(id)
            self.write(']')
        version = node.getVersion()
        if version:
            self.write(' version ' + str(version) + ' ')
        self.write(' {\n')
        self.increaseIndent()
        children = node.getChildren()
        for (e, child) in enumerate(children):
            if e > 0:
                self.write('\n')
            child.accept(self)
        self.decreaseIndent()
        self.writeEndComment('}',node)
        self.packages.pop()
    
    def visitType(self, node):
        if node.getBaseType():
            self.write(node.getIdentifier())
        else:
            self.write(self.getQualifiedName(node))
    
    def visitTypeUniverse(self, node):
        if self.declOnly[-(1)]:
            self.write(self.getQualifiedName(node))
            return None
        self.indent()
        self.write('universe ' + node.getIdentifier() + ' {')
        for (t, type) in enumerate(node.getTypes()):
            if t > 0:
                self.write(', ')
            type.accept(self)
        self.write('};\n')
    
    def visitEnumeration(self, node):
        if self.declOnly[-(1)]:
            self.write(self.getQualifiedName(node))
            return None
        self.writeStartComment(node,prependNewline=False)
        self.indent()
        self.write('enum ' + node.getIdentifier())
        self.write(' {')
        self.increaseIndent()
        for (e, child) in enumerate(node.getChildren()):
            endcomment = child.getEndComment()
            if e > 0:
                self.write(', ')
            child.accept(self)
            self.write(endcomment)
        self.write('\n')
        self.decreaseIndent()
        self.writeEndComment('};', node)
    
    def visitEnumerator(self, node):
        self.writeStartComment(node,prependNewline=True)
        if node.getInitialized():
            self.indent()
            self.write(node.getIdentifier() + ' = ' + str(node.getValue()))
        else:
            self.indent()
            self.write(node.getIdentifier())
    
    def visitArray(self, node):
        if node.isRarray():
            self.write('rarray<')
        else:
            self.write('array<')
        self.pushDeclOnly()
        node.getType().accept(self)
        self.popDeclOnly()
        if node.getDimension() > 0:
            self.write(', ' + str(node.getDimension()))
        self.write('>')
    
    def visitIterator(self, node):
        self.write('iterator<')
        self.pushDeclOnly()
        node.getType().accept(self)
        self.popDeclOnly()
        self.write('>')
    
    def visitInterface(self, node):
        if self.declOnly[-(1)]:
            self.write(self.getQualifiedName(node))
            return None

        self.writeStartComment(node,prependNewline=False)
        self.indent()
        self.write('interface ' + node.getIdentifier())
        parents = node.getParents()
        if len(parents):
            self.write(' extends ')
            for i in range(len(parents)):
                if i > 0:
                    self.write(', ')
                self.write(self.getQualifiedName(parents[i]))
        self.write(' {\n')
        self.increaseIndent()
        self.visitVertex(node)
        self.decreaseIndent()
        self.writeEndComment('}',node)
    
    def visitClass(self, node):
        if self.declOnly[-(1)]:
            self.write(self.getQualifiedName(node))
            return None
        self.writeStartComment(node)
        self.indent()
        self.write('class ' + node.getIdentifier())
        parents = node.getParents()
        if (len(parents) and not (parents[0].getFullIdentifier() == 'BaseClass')):
            self.write(' extends ')
            for i in range(len(parents)):
                if i > 0:
                    self.write(', ')
                self.write(self.getQualifiedName(parents[i]))
        interfaces = node.getInterfaces()
        interfaces_all = node.getInterfacesAll()
        if len(interfaces_all):
            extraindent = ''
            if len(parents): 
                self.write('\n')
                self.indent()
                extraindent = 2*self.getTab()
            self.write(' implements-all ')
            for i in range(len(interfaces_all)):
                if i > 0:
                    self.write(', ')
                self.write(self.getQualifiedName(interfaces_all[i]))            
        if len(interfaces):
            extraindent = ''
            if len(interfaces_all) or len(parents): 
                self.write('\n')
                self.indent()
                extraindent = 2*self.getTab()
            self.write(extraindent + ' implements ')
            for i in range(len(interfaces)):
                if i > 0:
                    self.write(', ')
                self.write(self.getQualifiedName(interfaces[i]))
        self.write(' {\n')
        self.increaseIndent()
        self.visitVertex(node)
        self.decreaseIndent()
        self.writeEndComment('}', node)
    
    def visitParameter(self, node):
        type = node.getType()
        mode = node.getAccessMode()
        typeAttrs = node.getTypeAttributes()
        for attr in node.getTypeAttributes():
            if attr: self.write(attr + ' ')
        if mode == parse.itools.ParameterAccessMode.IN:
            self.write('in ')
        elif mode == parse.itools.ParameterAccessMode.INOUT:
            self.write('inout ')
        elif mode == parse.itools.ParameterAccessMode.OUT:
            self.write('out ')
        elif mode == parse.itools.ParameterAccessMode.RETURN:
            pass
        else:
            raise RuntimeError('Invalid parameter access mode: ' + str(mode))
        self.pushDeclOnly()
        type.accept(self)
        self.popDeclOnly()
        if (not (type.getBaseType()) and type.getIdentifier() == 'void'):
        #if type.getIdentifier() is not 'void':
            if mode == parse.itools.ParameterAccessMode.RETURN:
                if node.getIdentifier() is not '_return_value':
                    self.write(node.getIdentifier())
        elif mode != parse.itools.ParameterAccessMode.RETURN:
            self.write(' ' + node.getIdentifier())
        dimsizes = node.getDimensionSizes()
        if dimsizes:
            self.write('(' + ','.join(dimsizes) + ')')
    
    def visitMethod(self, node):
        templateIds = node.getTemplateIdentifiers()

        self.writeStartComment(node)
        self.indent()
        if not (node.getReturnParameter() is None):
            self.pushDeclOnly()
            node.getReturnParameter().accept(self)
            self.popDeclOnly()
        else:
            self.write('void')
        self.write(' ' + node.getIdentifier())
        if len(templateIds):
            self.write('[')
            for (t, id) in enumerate(node.getTemplateIdentifiers()):
                if t > 0:
                    self.write(', ')
                self.write(id)
            self.write(']')
        self.write('(')
        for (c, child) in enumerate(node.getChildren()):
            if c > 0:
                self.write(', ')
            child.accept(self)
        self.write(')')
        exceptions = self.getDeclaredExceptions(node)
        if len(exceptions) > 0:
            self.write(' throws ')
            for (e, exc) in enumerate(exceptions):
                if e > 0:
                    self.write(', ')
                self.write(self.getQualifiedName(exc))
        self.write(';\t')
        self.writeEndComment('', node)
    # Ending class methods sec
    
    def indentComment(self,comment,prependNewline=True):
        lst = comment.strip().split('\n')
        indentstr = self.getIndentString()
        lst[0] = indentstr + lst[0] + '\n'
        if prependNewline: lst[0] = '\n' + lst[0]
        if len(lst) == 1: return lst[0]
        newcomment = lst[0]
        for l in lst[1:]:
            newcomment += indentstr + l + '\n'
        return newcomment
    
    def writeStartComment(self, node, prependNewline=False):
        startComment = self.processComment(node.getStartComment())
        # Remove comment lines contaning strings from the exclude list
        if startComment is not '':
            self.write('\n' + self.indentComment(startComment,prependNewline))
        else:
            self.write('\n')
        pass
            
    def writeEndComment(self, text, node, prependNewline=False):
        endComment = self.processComment(node.getEndComment().lstrip())
        if re.search(r'splicer\.end',endComment):
            # This is yucky but necessary since splicer end comments actually come just before an element's end
            self.increaseIndent()
            self.write(self.indentComment(endComment,prependNewline=True))
            self.decreaseIndent()
            self.indent()
            self.write(text + '\n')
            return
        
        if endComment is not '':
            if prependNewline:
                indentstr = self.getIndentString()
                self.write('\n' + indentstr + text + self.indentComment(endComment,prependNewline=True))
            else:
                self.indent()
                self.write(text + '\t' + endComment)
        else:
            self.indent()
            self.write(text + '\n')
        pass
    
    def processComment(self, comment):
        ''' Remove comment lines contaning strings from the exclude list'''
        if not self.commentExcludes: return comment
        newcomment = ''
        lines = comment.split('\n')
        pattern = re.compile('|'.join(self.commentExcludes))
        for l in lines:
            if l.strip() == '': continue
            if pattern.search(l) is None:
                newcomment += l + '\n'
        if not newcomment.endswith('\n'): newcomment += '\n'
        return newcomment
                
    def pushDeclOnly(self, declOnly = 1):
        self.declOnly.append(declOnly)
        return 
    
    def popDeclOnly(self):
        return self.declOnly.pop()
    
    def getQualifiedName(self, vertex, packageName = None, throws=False):
        '''
        Return the full identifier, unless the type is defined in the given package, when we return just the identifier
        '''
        return vertex.getIdentifier()   # TODO  Fix this when symbol resolution  is implemented
        if packageName is None:
            packageName = self.packages[-(1)].getFullIdentifier()
        name = vertex.getIdentifier()
        qualifiedName = vertex.getFullIdentifier()
        if qualifiedName == packageName + '.' + name:
            qualifiedName = name
        return qualifiedName
    
    def getDeclaredExceptions(self, method):
        '''
        Return all declared exceptions
        '''
        exceptions = []
        for exception in method.getExceptions():
            exceptions.append(exception)
        return exceptions
    