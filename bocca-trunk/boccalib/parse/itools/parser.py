import os, sys

from parse.itools.elements import Vertex
from parse.itools.commentlex import CommentLexer
from parse.itools.ilex import ILexer
from cct._err import err
from cct._debug import DEBUGSTREAM

class Parser:
    '''
    A SIDL parser
    '''
  
    def __init__(self, debug = 0, outputdir='.'):
        import parse.itools.iparse
        self.parser = parse.itools.iparse.setup(debug=debug, outputdir=outputdir)
    
        self.commentLex = CommentLexer()
        self.commentLex.build(optimize=1,lextab="parse.itools.commenttab" )          # Build the lexer

        self.lex = ILexer()
        self.lex.build(optimize=1, lextab=os.path.join("parse.itools.lextab"))       # Build the lexer

    def printAST(self):
        '''Print the parsed ast (mainly used for debugging)'''
        from parse.itools.visitor.printer import Printer
        printer = Printer()
        self.ast.accept(printer)
  
    def parse(self, buf, filename=''):
        '''
        Parse the buffer and return an AST object
        '''
        if buf == '' or buf.isspace(): return None
    
        if not buf.endswith('\n'): 
            print >>sys.stderr, 'Bocca WARNING: file does not end with newline.'
            buf += '\n'

        # First pass to get all comments
        self.commentLex.reset()
        self.commentLex.set_filename(filename)
        comments = self.commentLex.doit(buf)
    
        # Second pass: everything but the comments
        self.lex.reset()
        self.ast = self.parser.parse(buf)
        print >>DEBUGSTREAM, '[iparse] Successfully parsed buffer'

        # Merge comments into the AST
        from parse.itools.visitor.commentsmerger import CommentsMerger
        commentsMerger = CommentsMerger(comments)
        commentsMerger.setTopNode(self.ast)
        self.ast.accept(commentsMerger)
        commentsMerger.doMerge()
        
        from parse.itools.visitor.methodprocessor import MethodProcessor
        methodProcessor = MethodProcessor()
        self.ast.accept(methodProcessor)

        self.parser.restart()
        return self.ast
  
    def parseFile(self, filename, stripBocca=False):
        '''
        Parse the file and return an AST object
        '''
        if not os.path.exists(filename):
            err('[SIDL parser] file not found: ' + filename)
        self.filename = filename
        f = file(filename)
        s = f.read()
        f.close()
        # Strip bocca splice delimiters and protected blocks from old text
        if (stripBocca):
            lineList = s.split('\n')
            noBoccaList = [ l for l in lineList if l.find('DO-NOT-DELETE bocca.splicer.') == -1]
            inProtected=False
            noBlockList=[]
            for l in noBoccaList:
                if inProtected:
                    if l.find("DO-NOT-DELETE bocca.protected.end") != -1:
                        inProtected = False
                    continue
                else:
                    if l.find("DO-NOT-DELETE bocca.protected.begin") != -1:
                        inProtected = True
                        continue
                noBlockList.append(l)

            if inProtected:
                err('[SIDL parser] unterminated bocca.protected block in input.')
                
            s = '\n'.join(noBlockList)
        return self.parse(s)

