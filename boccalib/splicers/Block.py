
import Line, Misc, Kills
from _compat import *

class Block:
    """ A block is a set of lines that begins with a line:
	key.begin(symbol)
and ends with a line 
	key.end(symbol)
where both are wrapped in language specific comment marks.
Lines surrounded with other keys except this key
may be embedded in a block, but they are not themselves
block-ified and they may not be well-formed pairs, unique, etc.
"""

# Whenever using this class, we recommend going through the
# function interface, not accessing data members directly.
# We make no promises that the data members will remain the
# same across versions.

    def __init__(self):
# the interesting data -- a list of lines
        self.data = []
# the key this block is based on. "null" for plain text.
        self.prefix = ""
# the file this block came from in original form.
        self.file = ""
# the line in the original it started from.
        self.startlinenum = 0
# substitution symbols in the block.
        self.subsymbols = []
# a marker tag for client stack style use.
	self.tag=0

    def init(self, key, lines, source, start, subsymbols):
        """ key - the key or empty string for this block.
 lines - the list of lines for this block.
 source - the filename or empty string the lines come from.
 start - the line number the lines start at in the file.
"""
# do data by copy, not reference.
        # print 'Block filled: ', source, " ", key, " ", str(start), " ", lines
        self.data.extend( lines)
        self.prefix = key
        self.file = source
        self.startlinenum = start
        self.subsymbols = subsymbols
        return

    def setTag(self, tag):
        self.tag = tag

    def getTag(self):
        return self.tag

    def getLines(self, excludeDelimiters=False):
        """ return a the lines for this block, which should be treated read-only.
If the block has a key, then the delimiters can be excluded from the returned lines
by sending excludeDelimiters=True"""
        if excludeDelimiters and self.key() != "null" > 0:
            result = self.data[1:len(self.data)-1]
            return result
        else:
            return self.data

    def getSubsymbols(self):
        return self.subsymbols;

    def key(self):
        return self.prefix

    def source(self):
        return self.file

    def start(self):
        return self.startlinenum

    def killLines(self, rejectLines, killMatches, killBlockKeys, verbose=False):
        """ Delete the matching lines from self.data and return.
@param rejectLines destination for killed lines, if to be saved.
@param killMatches list of matching patterns. matching any pattern kills a line.
@param killBlockKeys well-formed blocks matching any key in this list are killed.
@return nothing.
"""
        if killMatches == None and killBlockKeys == None:
            return
        # first kill block pass
        if not killBlockKeys == None and len(killBlockKeys) > 0:
            for key in killBlockKeys:
                status, span = self.findKeyRanges( key )
                if not status == 0: 
                    continue
                if len(span) < 2:
                    continue
                while len(span) > 1:
                    if verbose:
                        print "start span = ", span
                    start = span[len(span)-2]
                    stop = span[len(span)-1]
                    if not rejectLines == None:
                        for dead in self.data[start:stop+1]:
                            rejectLines.append(dead);
                    del self.data[start:stop+1]
                    span = span[0:len(span)-1]
                    if verbose:
                        print "end span = ", span
        if not killMatches == None and len(killMatches) > 0:
            index = 0
            for k in self.data:
                if Misc.symbolContainsListItem(k, killMatches):
                    rejectLines.append(k)
                    del self.data[index]
                else:
                    index += 1
            

    def insertNested(self, block, atEnd, rejectLines=None, replaceIdentical=True, killMatches=None, killBlockKeys=None, srcKillBlockKeys=None, requireSymbol=None):
        """ Replace or insert/append a nested block according to its key in this block. In the degenerate case of this block having the identical key, this block is replaced.  returns 0 if ok, nonzero and prints a message otherwise. If replaceIdentical false, identical keys allowed and join instead of replace per atEnd.
 @param bool atEnd - if the block inserted is not previously existing,
 insert vs append is controlled by setting atEnd=0 for insert and nonzero for append.
@param rejectLines will have appended lines deleted from this block, if it is
supplied.
@param killMatches list of string matches. matching any pattern kills a line in self.
@param killBlockKeys well-formed blocks in self matching any key in this list are killed.
@param srcKillBlockKeys kills are done to source block before insertion to self.
"""
        if killBlockKeys == None:
            killBlockKeys=Kills.killBlockKeys
     #    if srcKillBlockKeys == None:
     #        srcKillBlockKeys=Kills.srcKillBlockKeys
        if killMatches == None:
            killMatches=Kills.cxxKillKeys
        junk = []
        block.killLines(junk, killMatches, srcKillBlockKeys)
        self.killLines(rejectLines, killMatches, killBlockKeys)
        status, span = self.findKeyRanges( block.key(), requireSymbol )
        if status:
            print span 
            return status
        if len(span) > 2:
            print "multiple matches found in block insertion"
            return 2
        # block already exists.
        if len(span) == 2:
            if replaceIdentical:
                start = span[0]
                end = span[1]
                if rejectLines != None:
                    rejectLines.extend(self.data[start : end+1])
                del self.data[start : end+1]
                for k in reversed(block.getLines()):
                    self.data.insert(start, k)
                return 0
            else:
                full=block.getLines()
                reduced = full[1:len(full)-1]
                if not atEnd or len(self.data) < 3:
                    for k in reversed(reduced):
                        self.data.insert(1,k)
                else: 
                    end = len(self.data) - 1
                    for k in reversed(reduced):
                        self.data.insert(end, k)
                return 0
        # block inserted is new
        if not atEnd or len(self.data) < 3:
            for k in reversed(block.getLines()):
                self.data.insert(1,k)
        else: 
            end = len(self.data) - 1
            for k in reversed(block.getLines()):
                self.data.insert(end, k)
        return 0
# end insertNested

    def replace(self, block, rejectLines=None, keepDelimiters=False):
        """ Replace a blocks contents. returns 0 if ok, nonzero and 
prints a message otherwise.
@param rejectLines will have old lines deleted from this block, if it is
supplied.
"""
        status, span = self.findKeyRanges( block.key())
	if keepDelimiters:
            delimStart=1
            delimEnd=-1
        else:
            delimStart=0
            delimEnd=0
        if status:
            print span 
            return status
        if len(span) > 2:
            print "multiple matches found in block replacement"
            return 2
        if span[0] != 0:
            print "unexpected block structure in replace call"
            return 3
        if len(span) == 2:
            start = span[0] + delimStart
            end = span[1] + delimEnd
            if rejectLines != None:
                rejectLines.extend(self.data[start : end+1])
            del self.data[start : end+1]
            for k in reversed(block.getLines(keepDelimiters)):
                self.data.insert(start, k)
            return 0
# fixme test. inserting still?
        if len(self.data) < 3:
            for k in reversed(block.getLines(keepDelimiters)):
                self.data.insert(1,k)
        else: 
            end = len(self.data) - 1
            for k in reversed(block.getLines(keepDelimiters)):
                self.data.insert(end, k)
        return 0

    def findKeyRanges(self, key, requireSymbol=None):
        """ Return the ndex of start and end lines matching the key given, if any.
 Used to find well-formed embedded blocks. As there may be more than one embedded, 
 result is a list. Illformed embedded blocks will cause an early exit, warnings,
 status, {index1, index2, ...} = findKeyRanges... 
 status == 0 --> ok; status != 0 --> result is error string instead of list.
"""
# state is 0 if outside keyblock and 1 if inside
        state=0
        index = 0
        result = []
        for s in self.data:
            if Line.keyBegins(key,s) and (not requireSymbol or Line.symbolOf(s) == requireSymbol):
                if not state:
                    result.append(index)
                    state = 1
                else:
                    return (1, "begin encountered twice without end for key " + key + " at line " + str(index))
            if Line.keyEnds(key,s) and (not requireSymbol or Line.symbolOf(s) == requireSymbol):
                if state:
                    result.append(index)
                    state = 0
                else:
                    return (1, "end encountered without begin for key " + 
                            key + " at line " + str(index))
            index += 1
        return( 0, result )

    def killMatches(self, matchTest, rejectLines=[]):
        """ removes all lines from data for which matchTest returns true.
This is the basis of default exception removal in impl code.
If rejectLines is supplied, the caller can put rejects someplace handy for the user.
"""
        index = 0
        for k in self.data:
            if apply(matchTest(k)):
                rejectLines.append(k)
                del self.data[index]
            else:
                index += 1

    def computeSignature(self, symbol, language, sourcekey, withcomment=False):
        """return attempted guess at the number of lines at the end of the
block that constitute a babel impl method signature.
The block being checked is the block before the block with the symbol code body.
@param language one of python, java, c, cxx, f77, f90. 
@param sourceKey the key, not symbol, of interest.
@param withcomment try to include the comment block if any.
"""
        result = 0
        lines = self.getLines()
        p = len(lines)-1
        if p < 1:
            return 0
        line = lines[p]
        if language == "python":
            while p >= 0 and line[0:4] != "####" and line[0:6] != "  def " and \
                  not Line.keyEnds(sourcekey, line) and \
                  not Line.keyBegins(sourcekey,line):
                # break on 2 blank lines
                if len(line) == 0:
                    q = p -1
                    if q >= 0 and len(lines[q]) == 0:
                        break
                # else keep line, move on to next
                result += 1
                p -= 1
                line = lines[p]
            result += 1 ; # include '  def ' line.
            # python comment blocks are embedded, not extra.
        if language == "java":
            while p > 0 and len(line) != 0 and \
                line[0:6] != "import" and \
                line[0:8] != "  public" and \
                line[0:4] != "////" and \
                line[0:3] != "/**" and \
                line[0:5] != "   */" and \
                line[0:8] != "  static" and \
                not Line.keyEnds(sourcekey, line) and \
                not Line.keyBegins(sourcekey,line):
                result += 1
                p -= 1
                line = lines[p]
            result += 1 ; # include '  public' line.
            if withcomment:
                while p > 0 and len(line) != 0 and \
                    line[0:5] != "  /**" and \
                    not Line.keyEnds(sourcekey, line) and \
                    not Line.keyBegins(sourcekey,line):
                    result +=1
                    p -= 1
                    line = lines[p]

        if language == "c" or language == "cxx":
            while p > 0 and \
                not Line.cppDirective(line) and \
                line[0:15] != "// user defined" and \
                line[0:15] != "// static class"  and \
                line[0:3] != "/**"  and \
                line[0:3] != " */"  and \
                line[0:5] != "   */"  and \
                line[0:22] != "// special constructor"  and \
                line[0:22] != "// speical constructor" and \
                line[0:1] != "}"  and \
                line[0:8] != "////////"  and \
                line[0:8] != "/**//**/" and \
                not Line.keyEnds(sourcekey, line) and \
                not Line.keyBegins(sourcekey,line):

                # two blank lines, or 1 if _tail symbol
                if len(line) == 0:
                    mname = Line.methodName(symbol)
                    if mname[0] == "_":
                        break
                    q = p-1
                    if q >= 0 and len(lines[q]) == 0:
                        break
                # else keep line and move on
                result += 1
                p -= 1
                line = lines[p]
            if withcomment:
                while p > 0 and len(line) != 0 and \
                    line[0:5] != "  /**" and \
                    line[0:2] != "/*" and \
                    not Line.keyEnds(sourcekey, line) and \
                    not Line.keyBegins(sourcekey,line):
                    result +=1
                    p -= 1
                    line = lines[p]
                result += 1 ; # include '(  )/*(*)' line.

        if language == "f77" or language == "f77_31":
            while p > 0 and \
                line[0:19] != "        subroutine " and \
                line[0:4] != "CCCC" and \
                not Line.keyEnds(sourcekey, line) and \
                not Line.keyBegins(sourcekey,line):

                # break on 2 blank lines
                if len(line) == 0:
                    q = p -1
                    if q >= 0 and len(lines[q]) == 0:
                        break
                # else keep line and move on
                result += 1
                p -= 1
                line = lines[p]
            result += 1 ; # include subroutine
            if withcomment:
                while p > 0 and len(line) != 0 and \
                    line[0:15] != "C       Method:" and \
                    not Line.keyEnds(sourcekey, line) and \
                    not Line.keyBegins(sourcekey,line):
                    result +=1
                    p -= 1
                    line = lines[p]

        # if language == "f90":
        if language in ('f90', 'f03'):
            while p > 0 and \
                line[0:21] != "recursive subroutine " and \
                line[0:5] != "!!!!" and \
                not Line.keyEnds(sourcekey, line) and \
                not Line.keyBegins(sourcekey,line):

                # break on 2 blank lines
                if len(line) == 0:
                    q = p -1
                    if q >= 0 and len(lines[q]) == 0:
                        break
                # else keep line and move on
                result += 1
                p -= 1
                line = lines[p]
            result += 1 ; # include subroutine
            if withcomment:
                while p > 0 and len(line) != 0 and \
                    line[0:9] != "! Method:" and \
                    not Line.keyEnds(sourcekey, line) and \
                    not Line.keyBegins(sourcekey,line):
                    result +=1
                    p -= 1
                    line = lines[p]

        return result
    # end computeSignature 



if __name__ == "__main__":
    pass
