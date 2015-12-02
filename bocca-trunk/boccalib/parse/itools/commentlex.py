#!/usr/bin/env python

# ----------------------------------------------------------------------
# ilex.py
#
# A lexer for SIDL.
# ----------------------------------------------------------------------

import parse.ply.lex as lex
from parse.itools.comments import Comments
from cct._err import err
import re

# TODO: handling for multiple C-style comments on the same line

class CommentLexer:
    
    # Tokens
    def __init__(self):
        self.fname = ''
        self.inside_comment = False
        self.comments = Comments()
        self.startLineNumber = -(1)
        self.comment = ''
        
    tokens = (
              'CODE',
            'COMMENT',
            'MULTILINE_COMMENT_BEGIN',
            'MULTILINE_COMMENT_END'
        )
    
    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'(\r\n)+|\n+'
        t.lexer.lineno += len(t.value)
 
    # Compute column. 
    #     input is the input text string
    #     token is a token instance
    def find_column(self,input,token):
        i = token.lexpos
        while i > 0:
            if input[i] == '\n' or input[i] == '\r\n': break
            i -= 1
        column = (token.lexpos - i)
        return column
    
    def set_filename(self,fname):
        self.filename = fname
        return 

    # Completely ignored characters
    t_ignore        = '\r\x0c'
    
    # Comments: TODO -- this is not really good for multi-line C-style comments
    def t_COMMENT(self,t):
        r'[ \t]*/\*[^\n]+\*/|.*//(.*)\n|"(\\.|[^"\\])*"\n'
        #r'/\*(.|\n)*?\*/|//(.*)|/\*[^*]*\*+([^/*][^*]*\*+)*/|"(\\.|[^"\\])*"'
        if self.inside_comment:  # Inside a multiline comment, don't treat this one as a separate comment
            self.comment += t.value.lstrip()
            if '\n' in t.value: t.lexer.lineno += 1
        else:
            self.comments.addComment(t.value.lstrip(), t.lexer.lineno, t.lexer.lineno)
            if '\n' in t.value: t.lexer.lineno += 1
            return t
        pass
    
    def t_MULTILINE_COMMENT_BEGIN(self,t):
        r'[ \t]*/\*.*\n'
        if self.inside_comment:
            print 'Warning: Nested comment found at line %s in %s, this is dangerous.' % (t.lexer.lineno, self.filename)
        
        #self.comments.addComment(t.value,t.lexer.lineno)
        self.startLineNumber = t.lexer.lineno
        self.comment = t.value.lstrip()
        expr=re.compile(r'\*/')
        if not expr.search(t.value):
            self.inside_comment = True
        t.lexer.lineno += 1
        return t

    def t_MULTILINE_COMMENT_END(self,t):
        r'.*\*/'
        self.inside_comment = False
        #t.value = self.comment 
        #print 'Multiline comment:\n', t.value
        self.comment += t.value.lstrip() + '\n'
        self.comments.addComment(self.comment,t.lexer.lineno, self.startLineNumber)
        #print 'Final multiline comment\n', t.value
        return t

    # All the code except whitespace and comments
    def t_CODE(self,t):
        r'[^(\/\/)\n]+.*\n'
        if self.inside_comment:
            self.comment += t.value.lstrip()
            #self.comments.addComment(t.value,t.lexer.lineno, t.lexer.lineno)
        t.lexer.lineno += 1
        pass
    
    # Error handling rule
    def t_error(self,t):
        col = self.find_column(t.lexer.lexdata,t)
        err("[SIDL parse] illegal character '%s' at line %s, column %s (%s)" % (t.value[0], t.lexer.lineno, col, str(t)))
        t.lexer.skip(1)
    
    # Return the comments in the instance of class Comments
    def getComments(self):
        return self.comments
    
    # reset
    def reset(self):
        self.lexer.lineno = 1
        self.comments.clear()
        
    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(object=self, **kwargs)
    
    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while 1:
            tok = self.lexer.token()
            if not tok: break
            print tok
             
    def doit(self,data):
        self.lexer.input(data)
        while 1:
            tok = self.lexer.token()
            if not tok: break
        return self.comments


#lexer = parse.ply.lex.lex(optimize = 0)
if __name__ == "__main__":
    import sys
    #lex.runmain(lexer)
    # Build the lexer and try it out
    l = CommentLexer()
    l.build(debug=1)           # Build the lexer
    for i in range(1, len(sys.argv)):
        print "About to lex %s" % sys.argv[i]
        f = open(sys.argv[i],"r")
        s = f.read()
        f.close()
        # print "Contents of %s: %s" % (sys.argv[i], s)
        if s == '' or s.isspace(): sys.exit(0)
        l.set_filename(sys.argv[i])
        l.test(s)
        print 'The resulting Comments instance:\n', l.comments

