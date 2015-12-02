#!/usr/bin/env python

# -----------------------------------------------------------------------------
# iparse.py
#
# Simple parser for SIDL
# -----------------------------------------------------------------------------
import user
import ParameterAccessMode
from parse.itools.elements import *
from cct._err import err
from cct._debug import DEBUGSTREAM

import parse.ply.yacc
import parse.itools.ilex as lexer
import sys, os


from parse.itools.commentlex import CommentLexer
from parse.itools.comments import Comments

# Get the token map
tokens    = parse.itools.ilex.ILexer.tokens
baseTypes = {}

# specification:
def p_specification_1(t):
    'specification : package_specifier_list'
    spec = Specification()
    spec.setLineNumber(t.linespan(1)[0])
    spec.setEndLineNumber(t.linespan(1)[1])
    spec.addChildren(t[1])
    t[0] = spec

def p_specification_empty(t):
    'specification : empty'
    spec = Specification()
    spec.setLineNumber(t.linespan(1)[0])
    spec.setEndLineNumber(t.linespan(1)[1])
    t[0] = spec

# package-specifier-list
def p_package_specifier_list_1(t):
    'package_specifier_list : package_specifier_list package_specifier'
    t[0] = t[1] + [t[2]]

def p_package_specifier_list_2(t):
    'package_specifier_list : package_specifier'
    t[0] = [t[1]]


# top_level_package_specifier
def p_package_specifier(t):
    'package_specifier : final_attr_specifier PACKAGE ID version_specifier LBRACE definition_list RBRACE optional_semi'
    package = Package()
    package.setLineNumber(t.linespan(2)[0])
    package.setEndLineNumber(t.linespan(7)[1])
    if t[1]: package.setFinalAttr(True)
    package.setIdentifier(t[3])
    if t[6]:
        package.addChildren(t[6])
    package.setVersion(t[4])
    #package.setLastLineNumber(t.lexer.lastlineno)
    t[0] = package

# final package
def p_final_attr_specifier(t):
    'final_attr_specifier : FINAL'
    t[0] = t[1]

def p_final_attr_specifier_empty(t):
    'final_attr_specifier : empty'
    t[0] = ''
    
# version 
def p_version_specifier_1(t):
    'version_specifier : VERSION ICONST DOT ICONST DOT ICONST'
    t[0] = str(t[2]) + '.' + str(t[4]) + '.' + str(t[6])
    
def p_version_specifier_2(t):
    'version_specifier : VERSION ICONST DOT ICONST'
    t[0] = str(t[2]) + '.' + str(t[4]) 

def p_version_specifier_3(t):
    'version_specifier : VERSION ICONST'
    t[0] = str(t[2])
      
def p_version_specifier_empty(t):
    'version_specifier : empty'
    t[0] = ''
    
# definition-list
def p_definition_list_1(t):
    'definition_list : package_specifier definition_list'
    t[0] = [t[1]]+t[2]

def p_definition_list_2(t):
    'definition_list : enum_specifier definition_list'
    t[0] = [t[1]]+t[2]

def p_definition_list_3(t):
    'definition_list : interface_specifier definition_list'
    t[0] = [t[1]]+t[2]

def p_definition_list_4(t):
    'definition_list : class_specifier definition_list'
    t[0] = [t[1]]+t[2]

def p_definition_list_empty(t):
    'definition_list : empty'
    t[0] = []

# enum-specifier:
def p_enum_specifier_1(t):
    'enum_specifier : ENUM ID LBRACE enumerator_list RBRACE optional_semi'
    enum = Enumeration()
    enum.setLineNumber(t.linespan(1)[0])
    enum.setEndLineNumber(t.linespan(5)[1])
    enum.setIdentifier(t[2])
    if t[4]:
        enum.addChildren(t[4])
        enum.setContents(t.lexer.lexdata[t.lexpos(3)+1:t.lexpos(5)])
    t[0] = enum

def p_enum_specifier_2(t):
    'enum_specifier : ENUM LBRACE enumerator_list RBRACE optional_semi'
    enum = Enumeration()
    if t[3]:
        enum.addChildren(t[3])
    t[0] = enum

# enumerator_list:
def p_enumerator_list_1(t):
    'enumerator_list : enumerator'
    t[0] = [t[1]]

def p_enumerator_list_2(t):
    'enumerator_list : enumerator_list COMMA enumerator'
    if t[3]: 
        t[0] = t[1]+[t[3]]
    else:
        t[0] = t[1]
    
# enumerator:
def p_enumerator_1(t):
    'enumerator : ID'
    enum = Enumerator()
    enum.setLineNumber(t.linespan(1)[0])
    enum.setEndLineNumber(t.linespan(1)[1])
    enum.setIdentifier(t[1])
    t[0] = enum

def p_enumerator_2(t):
    '''enumerator : ID EQUALS ICONST'''
    enum = Enumerator()
    enum.setLineNumber(t.linespan(1)[0])
    enum.setEndLineNumber(t.linespan(3)[1])
    enum.setIdentifier(t[1])
    enum.setValue(int(t[3]))
    enum.setInitialized(1)
    t[0] = enum

def p_enumerator_empty(t):
    'enumerator : empty'
    t[0] = None

# interface-specifier
def p_interface_specifier_1(t):
    'interface_specifier : INTERFACE ID extends_specifier LBRACE declaration_list RBRACE optional_semi'
    interface = createInterface(t[2], t[3], t[5], t.linespan(1)[0], t.linespan(6)[1])
    t[0] = interface

def p_interface_specifier_2(t):
    'interface_specifier : INTERFACE ID LBRACKET ID RBRACKET extends_specifier LBRACE declaration_list RBRACE optional_semi'
    interface = createInterface(t[2], t[6], t[8], t.linespan(1)[0], t.linespan(9)[1], [t[4]])
    t[0] = interface

def createInterface(name, parents, methods, lineno, endlineno, templateIdentifiers = None):
    interface = Interface()
    interface.setLineNumber(lineno)
    interface.setEndLineNumber(endlineno)
    interface.setIdentifier(name)
    interface.setBaseType(0)
    if parents:
        interfaceObjs = []
        for name in parents:
            interf = Interface()
            interf.setParent(interface)
            interf.setIdentifier(name)
            interface.setBaseType(0)
            interfaceObjs.append(interf)
        interface.addParents(interfaceObjs)
    if methods:
        interface.addChildren(methods)
        for m in methods:
            for param in m.getChildren():
                type = param.getType()
                if isinstance(type,Type):
                    interface.addDependencies([type])
    if not templateIdentifiers is None:
        interface.setTemplateIdentifiers(templateIdentifiers)
    return interface

# extends-specifier
def p_extends_specifier(t):
    'extends_specifier : EXTENDS scoped_identifier_list'
    t[0] = t[2]

def p_extends_specifier_empty(t):
    'extends_specifier : empty'
    t[0] = []

# declaration-list
def p_declaration_list_1(t):
    'declaration_list : method declaration_list'
    t[0] = [t[1]]+t[2]

def p_declaration_list_empty(t):
    'declaration_list : empty'
    t[0] = []

# class-specifier
def p_class_specifier_1(t):
    'class_specifier : CLASS ID extends_specifier implements_list LBRACE class_declaration_list RBRACE optional_semi'
    t[0] = createClass(t[2], t[3], t[4], t[6], t.linespan(1)[0], t.linespan(7)[1])

def p_class_specifier_2(t):
    'class_specifier : CLASS ID LBRACKET ID RBRACKET extends_specifier implements_list LBRACE class_declaration_list RBRACE optional_semi'
    t[0] = createClass(t[2], t[6], t[7], t[9], t.linespan(1)[0], t.linespan(10)[1], [t[4]])

def createClass(name, parents, interfaces, methods, lineno, endlineno, templateIdentifiers = None, implementsAll=False):
    sclass = Class()
    sclass.setIdentifier(name)
    sclass.setLineNumber(lineno)
    sclass.setEndLineNumber(endlineno)
    sclass.setBaseType(0)
    if parents:
        parentObjs = []
        for name in parents:
            pclass = Class()
            pclass.setParent(sclass)
            pclass.setIdentifier(name)
            pclass.setBaseType(1)
            parentObjs.append(pclass)
        sclass.addParents(parentObjs)
    if interfaces:
        parentObjs = []
        for interface in interfaces:
            interface.setParent(sclass)
            if interface.getImplementsAll():
                sclass.addInterfacesAll([interface])
            else:
                sclass.addInterfaces([interface])
            parentObjs.append(interface)
        #sclass.addParents(parentObjs)
    if methods:
        sclass.addChildren(methods)
        for m in methods:
            for param in m.getChildren():
                type = param.getType()
                if isinstance(type,Type):
                    sclass.addDependencies([type])
    if not templateIdentifiers is None:
        sclass.setTemplateIdentifiers(templateIdentifiers)
    return sclass

# implements-specifiers
def p_implements_list_1(t):
    '''implements_list : IMPLEMENTS scoped_identifier_list implements_list'''
    interfaceObjs = []
    for name in t[2]:
        interface = Interface()
        interface.setIdentifier(name)
        interface.setBaseType(0)
        interface.setImplementsAll(False)
        interfaceObjs.append(interface)
    t[0] = interfaceObjs + t[3]

def p_implements_list_2(t):
    '''implements_list : IMPLEMENTSALL scoped_identifier_list implements_list'''
    interfaceObjs = []
    for name in t[2]:
        interface = Interface()
        interface.setIdentifier(name)
        interface.setBaseType(0)
        interface.setImplementsAll(True)
        interfaceObjs.append(interface)
    t[0] = interfaceObjs + t[3]

def p_implements_list_empty(t):
    'implements_list : empty'
    t[0] = []
   
# class-declaration-list
def p_class_declaration_list_1(t):
    'class_declaration_list : class_method class_declaration_list'
    t[0] = [t[1]]+t[2]

def p_class_declaration_list_2(t):
    'class_declaration_list : method class_declaration_list'
    t[0] = [t[1]]+t[2]

def p_class_declaration_list_empty(t):
    'class_declaration_list : empty'
    t[0] = []


# class-method
def p_class_method(t):
    'class_method : STATIC method'
    t[2].setStatic(1)
    t[0] = t[2]


# method
def p_method_1(t):
    'method : return_parameter_specifier ID LPAREN parameter_list RPAREN throws_specifier SEMICOLON'
    t[0] = createMethod(t[1], t[2], t[4], t[6], t.linespan(2)[0], t.linespan(7)[1])
    return

def p_method_2(t):
    'method : return_parameter_specifier ID LBRACKET evil_identifier RBRACKET LPAREN parameter_list RPAREN throws_specifier SEMICOLON'
    t[0] = createMethod(t[1], t[2], t[7], t[9], t.linespan(2)[0], t.linespan(10)[1], [t[4]])
    return    
                        
def createMethod(returnParameter, name, parameters, exceptions, lineno, endlineno, templateIdentifiers = None):
    #from parse.itools.CodePurpose import STUB, CARTILAGE, IOR

    method = Method()
    if not returnParameter is None:
        method.setReturnParameter(returnParameter)
        returnParameter.setParent(method)
    method.setIdentifier(name)
    method.setLineNumber(lineno)
    method.setEndLineNumber(endlineno)
    if parameters:
        method.addChildren(parameters)
    if exceptions:
        excs = []
        for id in exceptions:
            exception = Interface()
            exception.setParent(method)
            exception.setIdentifier(id)
            exception.setBaseType(0)
            excs.append(exception)
        method.addExceptions(excs)
    if not templateIdentifiers is None:
        method.setTemplateIdentifiers(templateIdentifiers)
    method.setVirtual(1)
    #method.setPurpose([STUB, CARTILAGE, IOR])
    return method

def p_return_parameter_specifier_1(t):
    '''return_parameter_specifier : type_attribute_list VOID'''
    parameter = Parameter()
    if t[1]: parameter.setLineNumber(t.linespan(1)[0])
    else: parameter.setLineNumber(t.linespan(2)[0])
    parameter.setEndLineNumber(t.linespan(2)[1])
    tp = Type()
    tp.setVoid(True)
    tp.setIdentifier(t[2])
    parameter.setIdentifier('')
    parameter.setType(tp)
    parameter.setTypeAttributes(t[1])
    parameter.setAccessMode(parse.itools.ParameterAccessMode.RETURN)
    t[0] = parameter

def p_return_parameter_specifier_2(t):
    '''return_parameter_specifier : type_attribute_list type_specifier'''
    parameter = Parameter()
    parameter.setIdentifier('_return_value')
    if t[1]: parameter.setLineNumber(t.linespan(1)[0])
    else: parameter.setLineNumber(t.linespan(2)[0])
    parameter.setEndLineNumber(t.linespan(2)[1])
    parameter.setType(t[2])
    parameter.setTypeAttributes(t[1])
    t[2].setParent(parameter)
    parameter.setAccessMode(parse.itools.ParameterAccessMode.RETURN)
    parameter.setRequired(1)
    t[0] = parameter

def p_return_parameter_specifier_3(t):
    '''return_parameter_specifier : type_attribute_list type_specifier COLON ID'''
    parameter = Parameter()
    parameter.setIdentifier(t[4])
    if t[1]: parameter.setLineNumber(t.linespan(1)[0])
    else: parameter.setLineNumber(t.linespan(2)[0])
    parameter.setEndLineNumber(t.linespan(4)[1])
    parameter.setTypeAttributes(t[1])
    parameter.setType(t[2])
    t[2].setParent(parameter)
    parameter.setAccessMode(parse.itools.ParameterAccessMode.RETURN)
    parameter.setRequired(1)
    t[0] = parameter


def p_type_attribute_list_1(t):
    'type_attribute_list : type_attribute_list type_attribute_specifier' 
    t[0] = t[1] + [t[2]]
    
def p_type_attribute_list_2(t):
    'type_attribute_list : type_attribute_specifier'
    t[0] = [t[1]]
    
def p_type_attribute_specifier(t):
    '''type_attribute_specifier : ONEWAY
                                | LOCAL
                                | STATIC
                                | ABSTRACT
                                | FINAL
                                | NONBLOCKING
                                | COPY
                                | empty'''
    t[0] = t[1]

def p_throws_specifier(t):
    'throws_specifier : THROWS scoped_identifier_list'
    t[0] = t[2]

def p_throws_specifier_empty(t):
    'throws_specifier : empty'
    t[0] = None

# parameter-list
def p_parameter_list_1(t): 
    'parameter_list : parameter COMMA parameter_list'
    t[0] = [t[1]]+t[3]

def p_parameter_list_2(t): 
    'parameter_list : parameter'
    t[0] = [t[1]]

def p_parameter_list_empty(t): 
    'parameter_list : empty'
    t[0] = []

def p_parameter(t):
    '''parameter : copy_parameter 
                    | nocopy_parameter'''
    t[0] = t[1]

def p_copy_parameter(t):
    'copy_parameter : COPY access_specifier type_specifier ID dimsizes_specifier'
    parameter = Parameter()
    parameter.setIdentifier(t[4])
    parameter.addTypeAttribute('copy')
    parameter.setLineNumber(t.linespan(1)[0])
    if t[5]: parameter.setEndLineNumber(t.linespan(5)[1])
    else: parameter.setEndLineNumber(t.linespan(4)[1])
    parameter.setType(t[3])
    if t[5]: parameter.setDimensionSizes(t[5])
    t[3].setParent(parameter)
    parameter.setAccessMode(int(t[2]))
    parameter.setRequired(1)
    t[0] = parameter
    
def p_nocopy_parameter(t):
    'nocopy_parameter : access_specifier type_specifier ID dimsizes_specifier'
    parameter = Parameter()
    parameter.setIdentifier(t[3])
    parameter.setLineNumber(t.linespan(1)[0])
    if t[4]: parameter.setEndLineNumber(t.linespan(4)[1])
    else: parameter.setEndLineNumber(t.linespan(3)[1])
    parameter.setType(t[2])
    if t[4]: parameter.setDimensionSizes(t[4])
    t[2].setParent(parameter)
    parameter.setAccessMode(int(t[1]))
    parameter.setRequired(1)
    t[0] = parameter

def p_access_specifier(t):
    '''access_specifier : IN
                                            | INOUT
                                            | OUT'''
    if t[1] == 'in':
        t[0] = ParameterAccessMode.IN
    elif t[1] == 'inout':
        t[0] = ParameterAccessMode.INOUT
    elif t[1] == 'out':
        t[0] = ParameterAccessMode.OUT
    else:
        raise RuntimeError('Invalid access specifier: '+t[1])
    
# type-specifier:
def p_type_specifier_1(t):
    '''type_specifier : BOOL
                                        | CHAR
                                        | DCOMPLEX
                                        | DOUBLE
                                        | FCOMPLEX
                                        | FLOAT
                                        | INT
                                        | LONG
                                        | OPAQUE
                                        | STRING
                                        | ID'''
    if t[1] in baseTypes:
        type = baseTypes[t[1]]
    else:
        type = Type()
        type.setIdentifier(t[1])
        type.setLineNumber(t.linespan(1)[0])
        type.setEndLineNumber(t.linespan(1)[1])
        type.setBaseType(1)
        baseTypes[t[1]] = type
    t[0] = type

def p_type_specifier_2(t):
    '''type_specifier : scoped_identifier'''
    type = Type()
    type.setIdentifier(t[1])
    type.setLineNumber(t.linespan(1)[0])
    type.setEndLineNumber(t.linespan(1)[1])
    t[0] = type

def p_type_specifier_3(t):
    '''type_specifier : array_specifier'''
    t[0] = t[1]

def p_type_specifier_4(t):
    '''type_specifier : iterator_specifier'''
    t[0] = t[1]

#  [ (PrimativeType() | ScopedID() ) #ScalarType
#    [ LOOKAHEAD(2) <COMMA> <INTEGER_LITERAL> #Dimension ]
#    [ <COMMA> ( "row-major" | "column-major" ) #Orientation ] 
# array-specifier
def p_array_specifier_1(t):
    '''array_specifier : ARRAY LT array_type_specifier GT
                        | RARRAY LT array_type_specifier GT'''
    if t[1] == 'rarray':
        array = Array(rarray=True)
    else:
        array = Array()
    array.setLineNumber(t.linespan(1)[0])
    array.setEndLineNumber(t.linespan(4)[0])
    if t[3]: 
        array.setType(t[3])
        t[3].setParent(array)
    else:
        tp = Type()
        tp.setGeneric(True)
        tp.setIdentifier('')
        array.setType(tp)

    t[0] = array
    
def p_array_specifier_2(t):
    '''array_specifier : ARRAY LT array_type_specifier array_dim_specifier orientation_specifier GT
                        | RARRAY LT array_type_specifier array_dim_specifier orientation_specifier GT'''
    if t[1] == 'rarray':
        array = Array(rarray=True)
    else:
        array = Array()
    array.setLineNumber(t.linespan(1)[0])
    array.setEndLineNumber(t.linespan(6)[1])
    if t[3]: 
        array.setType(t[3])
        t[3].setParent(array)
    else:
        tp = Type()
        tp.setGeneric(True)
        tp.setIdentifier('')
        array.setType(tp)
    array.setDimension(int(t[4]))
    if t[5]: array.setOrientation(t[5])
    t[0] = array

def p_array_type_specifier_1(t):
    'array_type_specifier : type_specifier'
    t[0] = t[1]

def p_array_type_specifier_empty(t):
    'array_type_specifier : empty'
    pass

def p_array_dim_specifier_1(t):
    'array_dim_specifier : COMMA ICONST'
    t[0] = int(t[2])
    
def p_array_dim_specifier_empty(t):
    'array_dim_specifier : empty'
    t[0] = 1

def p_dimsizes_specifier(t):
    'dimsizes_specifier : LPAREN param_dim_specifier_list RPAREN'
    t[0] = t[2]
    
def p_dimsizes_specifier_empty(t):
    'dimsizes_specifier : empty'
    t[0] = []

def p_param_dim_specifier_list_1(t):
    '''param_dim_specifier_list : param_dim_specifier COMMA param_dim_specifier_list'''
    t[0] = [t[1]] + t[3]
    
def p_param_dim_specifier_list_2(t):
    '''param_dim_specifier_list : param_dim_specifier'''
    t[0] = [t[1]]
    

def p_param_dim_specifier(t):
    '''param_dim_specifier : ICONST
                            | ID'''
    t[0] = t[1]
    
def p_orientation_specifier(t):
    '''orientation_specifier : COMMA ROWMAJOR
                            | COMMA COLUMNMAJOR'''
    t[0] = t[2]
    
def p_orientation_specifier_empty(t):
    'orientation_specifier : empty'
    t[0] = 'row-major'
    
# iterator-specifier
def p_iterator_specifier_1(t):
    'iterator_specifier : ITERATOR LT type_specifier GT'
    iterator = Iterator()
    iterator.setType(t[3])
    iterator.setLineNumber(t.linespan(1)[0])
    iterator.setEndLineNumber(t.linespan(4)[1])
    t[3].setParent(iterator)
    t[0] = iterator

# scoped-identifier-list
def p_scoped_identifier_list_1(t):
    'scoped_identifier_list : scoped_identifier_list COMMA scoped_identifier'
    t[0] = t[1]+[t[3]]

def p_scoped_identifier_list_2(t):
    'scoped_identifier_list : scoped_identifier'
    t[0] = [t[1]]

def p_scoped_identifier(t):
    '''scoped_identifier : SCOPEDID
                         | ID'''
    t[0] = t[1]

def p_evil_identifier(t):
    '''evil_identifier : ID
                    | ABSTRACT 
                    | ARRAY 
                    | BOOL 
                    | CHAR 
                    | CLASS 
                    | COLUMNMAJOR 
                    | COPY
                    | DCOMPLEX 
                    | DOUBLE 
                    | ENUM 
                    | EXTENDS 
                    | FCOMPLEX 
                    | FINAL 
                    | FLOAT 
                    | FROM
                    | IN 
                    | INT 
                    | INOUT 
                    | IMPLEMENTS 
                    | IMPLEMENTSALL 
                    | IMPORT 
                    | INTERFACE 
                    | ITERATOR 
                    | LOCAL
                    | LONG 
                    | NONBLOCKING
                    | ONEWAY
                    | OPAQUE 
                    | ORDER
                    | OUT 
                    | PACKAGE 
                    | PURE
                    | RARRAY 
                    | REQUIRE
                    | RESTRICT 
                    | RESULT
                    | ROWMAJOR 
                    | STATIC 
                    | STRING 
                    | STRUCT
                    | THROWS
                    | VERSION 
                    | VOID
                    | AND 
                    | FALSE
                    | ELSE 
                    | ENSURE 
                    | IFF 
                    | IMPLIES 
                    | INVARIANT 
                    | IS 
                    | MOD 
                    | NOT 
                    | NULL 
                    | OR 
                    | REM 
                    | TRUE
                    | XOR'''
    # This rule, as the name implies, is evil because it allows all reserved words to be 
    # used as identifiers and must thus be updated whenever reserved words change (hopefully not too 
    # often).
    t[0] =t[1]
        
def p_optional_semi(t):
    '''optional_semi : SEMICOLON 
                     | empty''' 
    pass

def p_empty(t):
    'empty : '
    pass

# Parse error
def p_error(t):
    line,col = find_column(t.lexer.lexdata,t)
    pos = (col-1)*' '
    err("[SIDL parsing] unexpected symbol '%s' at line %s, column %s:\n\t%s\n\t%s^" % (t.value, t.lexer.lineno, col, line, pos))

# Compute column. 
#     input is the input text string
#     token is a token instance
def find_column(input,token):
    i = token.lexpos
    startline = input[:i].rfind('\n')
    endline = startline + input[startline+1:].find('\n') 
    line = input[startline+1:endline+1]
    while i > 0:
        if input[i] == '\n': break
        i -= 1
    column = (token.lexpos - i)
    return line, column

# Driver (regenerates parse table)
def setup_regen(debug = 1, outputdir='.'):
    global parser
    
    # Remove the old parse table
    parsetabfile = os.path.join(os.path.abspath(outputdir),'parsetab.py')
    try: os.remove(parsetabfile)
    except: pass

    parser = parse.ply.yacc.yacc(debug=debug, optimize=1, tabmodule='parsetab', write_tables=1, outputdir=os.path.abspath(outputdir))

    return parser

# Driver (does not regenerate parse table)
def setup(debug = 0, outputdir='.'):
    global parser

    parser = parse.ply.yacc.yacc(debug = debug, optimize=1, write_tables=0)
    return parser


def removeCommentMarkers(comment):
    if comment.startswith('/*'):
        if not comment.endswith('*/'):
            raise RuntimeError('Invalid comment:\n'+comment)
        newComment = comment[2:-2]
    if comment.startswith('//'):
        newComment = comment[2:]
    newComment.strip()
    return newComment

if __name__ == '__main__':
    '''To regenerate the parse tables, invoke iparse.py with --regen as the last command-line
        option, for example:
            iparse.py somefile.sidl --regen
    '''
    import visitor.printer
    import visitor.commentsmerger
    import sys
    
    #import profile
    # Build the grammar
    #profile.run("yacc.yacc()")
    
    if sys.argv[-1] == '--regen':
        del sys.argv[-1]
        setup_regen(debug=0, outputdir=os.path.dirname(sys.argv[0]))
    else:
        setup()

    
    commentLex = CommentLexer()
    commentLex.build(optimize=1,lextab="commenttab")           # Build the lexer

    lex = parse.itools.ilex.ILexer()
    lex.build(optimize=1)                     # Build the lexer

    
    for i in range(1, len(sys.argv)):
        print >>DEBUGSTREAM, "[iparse] About to parse %s" % sys.argv[i]
        f = open(sys.argv[i],"r")
        s = f.read()
        f.close()
        # print "Contents of %s: %s" % (sys.argv[i], s)
        if s == '' or s.isspace(): sys.exit(0)
        if not s.endswith('\n'): 
            print 'Bocca WARNING: file does not end with newline.'
            s += '\n'

        commentLex.reset()
        commentLex.set_filename(sys.argv[i])
        comments = commentLex.doit(s)
        
        #print 'Comments: \n', comments
        
        lex.reset()
        ast = parser.parse(s, lexer=lex.lexer, debug=0)
        print >>DEBUGSTREAM, '[iparse] Successfully parsed %s' % sys.argv[i]

        commentsMerger = visitor.commentsmerger.CommentsMerger(comments)
        commentsMerger.setTopNode(ast)
        ast.accept(commentsMerger)
        commentsMerger.doMerge()
        
        printer = visitor.printer.Printer()
        ast.accept(printer)
