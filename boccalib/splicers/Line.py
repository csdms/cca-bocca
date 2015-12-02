import string
import time
import re
""" Miscellaneous lineoriented functions. """

def stringdate():
    """ return current time in a string"""
    t=time.localtime()
    s = time.strftime( "%a %b %d %H:%M:%S %Y", t)
    return s


def keyBegins(key,  line):
    """ return  true if line matches key and .begin("""
    search = key + ".begin\("
    if re.search(search, line) != None:
        return True
    return False


def keyEnds(key, line):
    """ return  true if line matches key and .end("""
    search = key + ".end\("
    if re.search(search, line) != None:
        return True
    return False


def symbolOf(line):
    """ extract first symbol in () on line, or "null" if none found."""
    symbol="null"
    x = re.search('\([^\(]*\)', line)
    if x != None:
        symbol = string.strip(x.group(),'()')
    else:
        print "Warning: Malformed symbol in line: \n\t", line
    return symbol

def cppDirective(line, ignoreNumLines=True):
    """ return true if looks like preprocessor other than #line."""
    tmp = string.strip(line)
    if len(tmp) > 0:
        if tmp[0] == '#':
            if ignoreNumLines and tmp[0:5] == "#line":
                return False
            return True
    return False

def matchedSymbolTail(sym, matchSyms):
    """ if the empty list is given, take it as * and all symbols match."""
    pmax = len(matchSyms)
    if pmax < 1:
        return True
    p = 0
    while p < pmax:
        rex = matchSyms[p]+'$'
        if re.search(rex, sym) != None:
            return True
        p += 1
    return False

def matchedSymbol(sym, matchSyms):
    """ if the empty list is given, take it as * and all symbols match."""
    pmax = len(matchSyms)
    if pmax < 1:
        return True
    p = 0
    while p < pmax:
        if re.search(matchSyms[p], sym) != None:
            return True
        p += 1
    return False

def addLineNumber(line, lines, fname, language, endtag=""):
    """ generate a line number in language format"""
    directive=""
    if language == "c"  or  language == "cxx"  or  language == "python":
        directive = "#line " + str(line) + " \""
    if language == "java":
        directive = "//LINE " + str(line)  + " \""
    if language == "f90"  or  language == "f77" or  language == "f77_31":
        directive = "C LINE " + str(line)  + " \""
    if directive == "":
        return
    directive += fname + "\" "  + endtag
    lines.append(directive)
    # print "addLineNumber appending", directive

def methodName(symbol):
    """return everything after the final . on the line, or
       everything if there is no dot."""
    x=symbol.split(".")
    return x[len(x)-1]

if __name__ == "__main__":
    print "testing stringdate"
    print stringdate()
    print "testing symbolOf"
    print symbolOf("sdfas(123abc)asfad(243)")
    print symbolOf("sdfas(")
    print "testing keyBegins"
    print keyBegins('foo', "asdf foo.begin(x) ")
    print keyBegins('bar', "asdf foo.begin(x) ")
    print "testing keyEnds"
    print keyEnds('foo', "asdf foo.end(x) " )
    print keyEnds('bar', "asdf foo.end(x) " )
    print "testing cppDirective"
    print cppDirective("#ifdef something")
    print cppDirective("#line 1")
    print cppDirective("#line 1",False)
    print "testing matchedSymbol"
    print matchedSymbol("fred",["joe", "bill", "fred"])
    print matchedSymbol("clark",["joe", "bill", "fred"])
    print matchedSymbol("clark",["ark", "bill", "fred"])
    print matchedSymbol("clark",[])
    print "testing addLineNumber"
    list=[]
    addLineNumber(2, list, "filename", "python")
    addLineNumber(27, list, "filename2", "f77")
    print list
    print "testing methodName"
    s=methodName("gov.cca.Foo._init")
    print s
