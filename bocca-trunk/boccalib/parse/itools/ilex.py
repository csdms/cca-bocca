#!/usr/bin/env python

# ----------------------------------------------------------------------
# ilex.py
#
# A lexer for SIDL.
# ----------------------------------------------------------------------

import re
import parse.ply.lex as lex
from cct._err import err

class ILexer:
    
    def __init__(self):
        self.currentline = ''
        
    # Reserved words
    reserved = (
        'ABSTRACT', 'ARRAY', 'BOOL', 'CHAR', 'CLASS', 'COLUMNMAJOR', 'COPY', 'DCOMPLEX', 'DOUBLE', 'ENUM', 'EXTENDS', 
        'FCOMPLEX', 'FINAL', 'FLOAT', 'FROM', 'IN', 'INT', 'INOUT', 'IMPLEMENTS', 'IMPLEMENTSALL', 'IMPORT', 
        'INTERFACE', 'ITERATOR', 'LOCAL', 'LONG', 'NONBLOCKING', 'ONEWAY', 'OPAQUE', 'ORDER', 'OUT', 'PACKAGE', 
        'PURE', 'RARRAY', 'REQUIRE', 'RESTRICT', 'RESULT', 'ROWMAJOR', 'STATIC', 'STRING', 'STRUCT', 'THROWS', 
        'VERSION', 'VOID',
        'AND', 'ELSE', 'ENSURE', 'FALSE', 'IFF', 'IMPLIES', 'INVARIANT', 'IS', 'MOD', 'NOT', 'NULL', 
        'OR', 'REM', 'TRUE', 'XOR'
        )
    

    tokens = reserved + (
        # Literals (scoped identifier, identifier, integer constant, float constant, string constant, char const)
        'SCOPEDID', 'ID', 'ICONST', # 'FCONST', 'SCONST', 'CCONST', 

        # Assignment
        'EQUALS',
    
        # Delimeters < > ( ) [ ] { } , . ; :
        'LT', 'GT',
        'LPAREN', 'RPAREN',
        'LBRACKET', 'RBRACKET',
        'LBRACE', 'RBRACE',
        'COMMA', 'SEMICOLON', 'COLON', 'DOT',

        )
    
    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        
        
    # Compute column. 
    #     input is the input text string
    #     token is a token instance
    def find_column(self,input,token):
        i = token.lexpos
        while i > 0:
            if input[i] == '\n': 
                break
            i -= 1
        column = (token.lexpos - i) 
        return column
                
 
    # Completely ignored characters
    t_ignore        = ' \r\t\x0c'
    # Assignment
    t_EQUALS        = r'='
    # Delimeters
    t_LT            = r'<'
    t_GT            = r'>'
    t_LPAREN        = r'\('
    t_RPAREN        = r'\)'
    t_LBRACKET      = r'\['
    t_RBRACKET      = r'\]'
    t_LBRACE        = r'\{'
    t_RBRACE        = r'\}'
    t_COMMA         = r','
    t_SEMICOLON     = r';'
    t_COLON         = r':'
    t_DOT           = r'\.'
    #t_ELLIPSIS = r'\.\.\.'
    # Operators
    t_BITWISE_AND   = r'&'
    t_BITWISE_XOR   = r'\^'
    t_EQ            = r'=='
    t_GE            = r'>='
    t_GT            = r'>'
    t_LE            = r'<='
    t_LT            = r'<'
    t_MINUS         = r'-'
    t_NE            = r'\!='
    t_BITWISE_OR    = r'\|'
    t_PLUS          = r'\+'
    t_POWER         = r'\*\*'
    t_SLASH         = r'/'
    t_STAR          = r'\*'
    t_TILDE         = r'~'
    t_LSHIFT        = r'<<<'
    t_RSHIFT        = r'>>>'
    
    # TODO: need to add numeric literals
    
    # Identifiers and reserved words
    global reserved_map
    reserved_map = { }
    for r in reserved:
        reserved_map[r.lower()] = r
    reserved_map['implements-all'] = 'IMPLEMENTSALL'
    reserved_map['row-major'] = 'ROWMAJOR'
    reserved_map['column-major'] = 'COLUMNMAJOR'
    
    def t_SCOPEDID(self,t):
        r'[A-Za-z_][\w_-]*(\.[A-Za-z_][\w_-]*)+'
        t.type = reserved_map.get(t.value, 'SCOPEDID')
        return t
    
    def t_ID(self,t):
        r'[A-Za-z_][\w_-]*'
        t.type = reserved_map.get(t.value, 'ID')
        return t
    
    # Integer literal 
    def t_ICONST(self,t): 
        r'[+-]?\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
        t.type = reserved_map.get(t.value, 'ICONST')
        return t
    
    # Floating literal
    #t_FCONST = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'
    
    # String literal
    #t_SCONST = r'\"([^\\\n]|(\\.))*?\"'
    
    # Character constant 'c' or L'c'
    #t_CCONST = r'(L)?\'([^\\\n]|(\\.))*?\''
    
    # Comments 
    def t_COMMENT(self,t):
        r'/\*(.|\n)*?\*/|//(.*)|/\*[^*]*\*+([^/*][^*]*\*+)*/|"(\\.|[^"\\])*"'
        newlines = t.value.count('\n')
        if newlines > 0: 
            t.value = newlines*'\n'
            return self.t_newline(t)
        pass
    
    # Error handling rule
    def t_error(self,t):
        col = self.find_column(t.lexer.lexdata,t)
        err("[SIDL parse] illegal character '%s' at line %s, column %s" % (t.value[0], t.lexer.lineno, col))
        t.lexer.skip(1)

    # reset
    def reset(self):
        self.lexer.lineno = 1
        
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


#lexer = parse.ply.lex.lex(optimize = 0)
if __name__ == "__main__":
    import sys
    #lex.runmain(lexer)
    # Build the lexer and try it out
    l = ILexer()
    l.build(debug=1)           # Build the lexer
    for i in range(1, len(sys.argv)):
        print "About to lex %s" % sys.argv[i]
        f = open(sys.argv[i],"r")
        s = f.read()
        f.close()
        # print "Contents of %s: %s" % (sys.argv[i], s)
        if s == '' or s.isspace(): sys.exit(0)
        l.test(s)

