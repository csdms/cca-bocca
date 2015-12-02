import os.path
from cct._err import err
from cct._util import *
import Line
import Block

class Source:
    """Object representing a source file or other lines potentially containing splicer blocks.
This is where we keep track of line numbers, sidl symbols, etc on top of the 
simple Block abstraction.
"""

# Whenever using this class, we recommend going through the
# function interface, not accessing data members directly.
# We make no promises that the data members will remain the
# same across versions.
    def __init__(self):
        self.fin = "" # infile
# outfile
        self.out = ""
# input chunked up by key matches or lack thereof into blocks.
        self.sections = []
# symbols found in key matches.
        self.symbols = [] 
        self.protectedSymbols = []
# which segment each symbol is found in. dictionary keyed by symbol to index into sections.
        self.symbolIndex = dict()
        self.protectedSymbolIndex = dict()
# how many splices were performed.
        self.nsplices = 0
# num how many lines were read.
        self.num=0

    # internal use only
    def beginChunk(self, lineList):
        """start recording a chunk into reference linelist."""
        del lineList[0:len(lineList)] # just clear the old linelist content

    # internal use only
    def endChunk(self, key, blockStart, lineList, line, inputfilename, subsymbols=[], protected=False):
        """ finish recording a chunk and save data.
            string key, int blockStart, reference linelist """
        symbol = "null"
        if key != "null":
            symbol = Line.symbolOf(line)
            if not protected and symbol in self.symbols:
                print "Warning: duplicate block for symbol ", symbol, " ignored at line ", str(blockStart)
                return
            elif protected and symbol in self.protectedSymbols:
                print "Warning: duplicate block for protected symbol ",symbol,"ignored at line ", str(blockStart)
                return
            if not protected:
                self.symbolIndex[symbol] = len(self.sections)
                self.symbols.append(symbol)
            else:
                self.protectedSymbolIndex[symbol] = len(self.sections)
                self.protectedSymbols.append(symbol)
        block = Block.Block()
        block.init(key, lineList, inputfilename, blockStart, subsymbols)
        self.sections.append(block)
 
    # public use
    def loadString(self, input, key, linebuf, warn=True, preserveProtected=False):
        """Load a string as a source. Either this or load[List,File] may be called once per SourceFile object. 
        input is an identifier string, normally a filename, that might be useful in error messages. 
        key is the splicing generic prefix tag (not per-sidl-symbol), and linebuf is the data string with embedded newlines."""
	return self.loadList(input, key, linebuf.splitlines(), warn, preserveProtected)

    # public use
    def loadList(self, input, key, lines, warn=True, preserveProtected=False):
        """Load a list of lines as a source. Either this or load may be called once per SourceFile object. 
        input is an identifier string, normally a filename, that might be useful in error messages. 
        key is the splicing generic prefix tag (not per-sidl-symbol), and lines is the data."""

        chunk = []
        protectedChunk = [] # protected blocks need a separate chunk
        subsymbols = [] # Symbols designating substitution blocks
        nokey = "null"
        protectedKey = "bocca.protected"
        message = "Block still unended at end of file."
        self.num = 0
        blockStart = 1
        protectedBlockStart = 0
        seek_begin = True # true while not in key'd block
        protected_block = False # true while in bocca.protected
        for line in lines:
            self.num += 1
            if seek_begin:
                if Line.keyEnds(key, line):
                    seek_begin = False
                    message = "Block end found before beginning."
                    break
                # outside a key block, start block, or append old.
                if Line.keyBegins(key, line):
                    seek_begin = False
                    self.endChunk( nokey, blockStart, chunk, line, input, protected=False) # save old if any
                    blockStart = self.num
                    self.beginChunk( chunk) # start new if any
                    chunk.append(line)
                else:
                    chunk.append(line)
            elif protected_block:
                # inside a protected block
                if Line.keyBegins(protectedKey, line) or Line.keyBegins(key, line):
                    message = "Block begin found inside bocca.protected"
                    break
                if Line.keyEnds(protectedKey, line):
                    protectedChunk.append(line)
                    chunk.append(line)
                    self.endChunk( protectedKey, protectedBlockStart, protectedChunk, line, input, protected=True)

                    subsymbols.append(Line.symbolOf(line))
                    protected_block = False;
                else:
                    # Chunk contains content of subblocks; will be replaced/stubbed if necessary when
                    # performing substitution
                    protectedChunk.append(line)
                    chunk.append(line)
            else:
                # inside  a key block
                if Line.keyBegins(key,line): # warn unended block
                    message = "Block begin found inside another."
                    break
                if Line.keyEnds(key,line):
                    seek_begin = True
                    chunk.append(line)
                    self.endChunk( key, blockStart, chunk, line, input, subsymbols, protected=False) # save key block
                    subsymbols = []
                    blockStart = self.num+1 # start new block
                    self.beginChunk( chunk)
                elif preserveProtected and Line.keyBegins(protectedKey, line):
                    # Begin the protected block
                    protectedBlockStart = self.num
                    self.beginChunk(protectedChunk)
                    protectedChunk.append(line)
                    chunk.append(line)
                    protected_block = True;
                else:
                    chunk.append(line)
            # end else
        # end for
        if not seek_begin:
            print "In ", input, ":", message, " at line ", self.num
            if len(chunk) > 0:
                print "Current block started at line ", blockStart, ":"
                print "\t", chunk[0]
            return (1, message)
        if len(chunk) > 0:
            self.endChunk( nokey, blockStart, chunk, line, input)
        if len(self.symbolIndex) < 1 and warn:
            print "Warning: no blocks in ", input, " for key ", key

        return (0, "ok")
    # end loadlist

    # public use
    def loadFile(self, input, key, preserveProtected=False):
        """Load a file as a set of blocks chunked up by key. returns (0, "ok") or (1, "errmsg"). If you don't have a file but have a list of lines, use loadList instead. """
        self.fin = input
        self.nsplices = 0
        try:
            f = fileManager.open(input, 'r')
            lines = f.readlines()
            f.close()
        except IOError, e:
            err('Error loading file ' + str(input) + '(' +  str(e) +')' )
        return self.loadList(input, key, lines, preserveProtected=preserveProtected)

    # public use
    def getSymbols(self):
        """ return the list of symbols defined in this source."""
        return self.symbols
    # end getSymbols

    # public use
    def getProtectedSymbols(self):
        """ return the list of protected symbols in key blocks for this source."""
        return self.protectedSymbols
    # end getProtectedSymbols

    # public use
    def getBlock(self, symbol):
        """ return the Block for the symbol given. Symbol given should be among those found
in getSymbols. """
        if symbol in self.symbolIndex:
            pos = self.symbolIndex[symbol]
            block = self.sections[pos]
            return block
        return None
    # end getBlock

    # public use
    def getProtectedBlock(self, symbol):
        """ return the protected block for the given protected symbol.  Should be in protectedSymbols."""
        if symbol in self.protectedSymbols:
            pos = self.protectedSymbolIndex[symbol]
            block = self.sections[pos]
            return block
        return None
    # end getProtectedBlock

    #public use
    def tagSymbol(self, symbol, tag):
        block = self.getBlock(symbol)
        block.setTag(tag)

    # public use
    def tagSymbols(self, tag):
        for symbol in self.symbols:
            self.tagSymbol(symbol, tag)
        
    def getTaggedSymbols(self, tag):
        result=[]
        for symbol in self.symbols:
            block = self.getBlock(symbol)
            if block.getTag() == tag:
                result.append(symbol)
        return result
        
    # public use
    def insert(self, symbol, splice, insertFirst, rejects, verbose=False, replaceIdentical=True, killMatches=None, killBlockKeys=None, srcKillBlockKeys=None):
        """ merge the given splice to ours of the same symbol"""
        block = self.getBlock(symbol)
        if block == None or splice == None:
            if verbose:
                print "Warning: odd processing null splice for symbol: ", symbol
            return
        if verbose:
            print "Inserting ", symbol, " from ", splice.source(),":",splice.start()
        atEnd = not insertFirst
        block.insertNested(splice, atEnd, rejects, replaceIdentical=replaceIdentical, killMatches=killMatches, killBlockKeys=killBlockKeys, srcKillBlockKeys=srcKillBlockKeys)
        self.nsplices += 1
    # end insert()

    # public use
    def replace(self, symbol, splice, rejects, verbose=False):
        """ merge the given splice to ours of the same symbol"""
        block = self.getBlock(symbol)
        if block == None or splice == None:
            print "Warning: odd processing null splice for symbol: ", symbol
            return
        if verbose:
            print "Inserting ", symbol, " from ", splice.source(),":",splice.start()
        block.replace(splice, rejects, keepDelimiters=True)
        self.nsplices += 1
    # end replace()

    # public use
    def completedSplices(self):
        """ get number of splices successfully inserted."""
        return self.nsplices

    # public use 
    def writeString(self, outFileName, verbose=False, rejectSave=True, rejectFileName="", rejectLines =[]):
        """return string representation of file for other's to output. outFileName is used to write rejects if specified or to issue error messages.
@return (status, resultString) where if status is True, string will be valid and if false, the input
source was apparently empty."""
        fname = outFileName
        writeRejects = (rejectSave and rejectLines != None)
        if writeRejects:
            rname = fname + ".rej"
            if len(rejectFileName) > 0:
                rname = rejectFileName
        if self.nsplices < 1:
            if verbose:
                print "Nothing new to write to ", fname
            if self.num < 1:
                print "Nothing old to copy to ", fname
                print "Reading ", self.fin, " failed?" 
                return (False, "")
        if verbose:
            if writeRejects:
                print "Writing rejects to ", rname
            print "Writing to string for ", fname
        if True: 
            outlist = []
            if writeRejects:
                try:
                    rejfile = fileManager.open(rname,"w")
                except:
                    err('splicer could not open rejects file for writing: ' + rname)
            for i in self.sections:
                isProtected = False
                for s in self.protectedSymbols:
                    if i == self.getProtectedBlock(s):
                        isProtected = True
                        break
                if isProtected:
                    continue
                lines = i.getLines() 
                for p in lines:
                    outlist.append( p.strip("\n") )
            stringified = "\n".join(outlist)
            if writeRejects:
                date = Line.stringdate()
                print >> rejfile, "#FROM %s on %s" % (fname, date)
                for p in rejectLines:
                    print >> rejfile , p.strip("\n")
            if verbose:
                if writeRejects:
                    print " Finished ", rname
                print " Finished ", fname
            return (True, stringified)
        else:
            print "Error writing for "+ fname
            return (False, "")
    # end writeString

    # public use 
    def write(self, outFileName, verbose=False, dryrun=False, rejectSave=True, rejectFileName="", rejectLines =[]):
        """return true if succeeds writing to output file named."""
        fname = outFileName
        writeRejects = (rejectSave and rejectLines != None and len(rejectLines) > 0)
        if writeRejects:
            rname = fname + ".rej"
            if len(rejectFileName) > 0:
                rname = rejectFileName
        if self.nsplices < 1:
            if verbose:
                print "Nothing new to write to ", fname
            if self.num < 1:
                print "Nothing old to copy to ", fname
                print "Reading ", self.fin, " failed?" 
                return False
        if dryrun:
            return True
        if True: 
            outfile = None
            try:
                outfile = fileManager.open(fname,"w")
            except IOError,e:
                err('splicer could not open file for writing: ' + fname + '; ' + str(e))
            for i in self.sections:
                # Kludge to get around printing protected symbols in the merged file.
                isProtected = False
                for s in self.protectedSymbols:
                    if i == self.getProtectedBlock(s):
                        isProtected=True
                        break
                if isProtected:
                    continue

                lines = i.getLines()
                # print "writing section ", i.key(), " len = ", len(lines)
                for p in lines:
                    print >> outfile, "%s" % p.strip("\n")
            if writeRejects:
                if not self.writeRejects(rname, rejectLines, originalFile=outFileName, verbose=verbose, dryrun=dryrun):
                    return False
            if verbose:
                if writeRejects:
                    print " Finished ", rname
                print " Finished ", fname

            outfile.close()
            return True
        else:
            print "Error writing for "+ fname
            return False
    # end write

    def writeRejects(self, rejectFileName, rejectLines='', originalFile='', verbose=False, dryrun=False):
        if len(rejectLines) == 0:
            print "No rejection information to put into " + rejectFileName
            return False
        if dryrun:
            print "Dry run: Not writing to " + rejectFileName
            # For a dry run, don't do anything
            return True
        if verbose:
            print "Writing rejects to: " + rejectFileName
        outfile = None
        try:
            outfile = fileManager.open(rejectFileName,'w')
        except IOError, e:
            err('splicer could not open reject file %s for writing: %s' % (rejectFileName, str(e)))
        if len(originalFile) > 0:
            date = Line.stringdate()
            print >> outfile, "# Rejects FROM %s on %s" % (originalFile, date)
        for p in rejectLines:
                print >> outfile, p.strip("\n")
        if verbose:
            print "Finished writing rejects: " + rejectFileName
        return True
        
    # end writeRejects

    # private use
    def updateAfterCount(self, opts, symbol):
        if not Line.matchedSymbolTail(symbol, opts.matchSyms):
            # here we assume the real symbol block comes last. works for uses in f90
            return 0
        if opts.language in ['cxx','python','f77','f90','java']:
            if (opts.linesAfter < 1):
                return 1
        if opts.language in ['c']:
            if (opts.linesAfter < 2):
                return 2
        return opts.linesAfter
    # end updateAfterCount


    # private use
    def writeBlock(self, before, fs, after, opts, append):
        """process a block with -B -A or --signature options.
# return 0 if ok, nonzero otherwise
# @param before the block ahead of this one or none if this is first.
# @param fs the current block to print.
# @param after the block after this one or none if this is last.
# @param opts handling flags for lines.
# @param append[0] an in-out integer array with one element. it tracks
# how many blocks have been written in the single file case.
"""
        lines = fs.getLines()
        pos = 0
        symbol = Line.symbolOf(lines[pos])
        if symbol == "null":
            return 1
        if not Line.matchedSymbol(symbol, opts.matchSyms):
            return 0
        # compute before lines
        pre = opts.linesBefore
        post = opts.linesAfter 
        if (opts.signatures or opts.method) and before != None:
            post = self.updateAfterCount(opts, symbol) 
            pre = before.computeSignature( symbol, opts.language, opts.sourceKey, opts.methodcomment)
        outlines = []
        if pre > 0 and before != None:
            blines = before.getLines()
            blen = len(blines)
            while blen > 0 and pre > 0:
                outlines.append(blines[blen-1])
                blen -= 1
                pre -= 1
            outlines.reverse()
        # copy main segment
        if opts.genLines:
            endtag=""
            if opts.method:
                endtag="/* This line not in actual source */"
            Line.addLineNumber(fs.start(), outlines, fs.source(), opts.language, endtag )
        while pos < len(lines):
            outlines.append(lines[pos])
            pos += 1
        pos = 0
        # compute after
        if post > 0 and after != None:
            alines = after.getLines()
            n = 0
            while n < len(alines) and post > 0:
                outlines.append(alines[n])
                n += 1
                post -= 1

        # write
        if len(outlines) < 1:
            return 1
        flags = "w"
        if opts.singleFile:
            if append[0]:
                flags= "a"
            if len(opts.outputFile):
                fname = os.path.join(opts.outputDir, opts.outputFile)
            else:
                fname = os.path.join(opts.outputDir, opts.inputFile)
                fname += ".splice"
        else:
            fname = os.path.join(opts.outputDir, opts.blockFilePrefix)
            # print "Writing block for ", symbol, fname
            fname = fname + symbol + opts.blockFileSuffix
            # print "Writing block for ", symbol, fname
        try:
            outfile = open(fname,flags)
            if opts.singleFile and append[0] and len(opts.spliceHeader) > 0 and (not opts.method):
                w = 0
                delta = len(opts.spliceHeader)
                while w < 72:
                    outfile.write("%s" % opts.spliceHeader)
                    w += delta
                outfile.write("\n")
            j = 0
            while j < len(outlines): 
                if opts.keepLines or opts.genLines or outlines[j][0:5] != "#line":
                    print >> outfile, outlines[j].strip("\n")
                j+= 1
            append[0] += 1
            return 0
        except:
            print "Error writing block for ", symbol
            return 1
    # end writeBlock

    def  writeExtracts(self, sourceKey, opts):
        """return 0 if succeeds, nonzero if fails."""
        append = [0]
        slen = len(self.sections)
        i = 0
        while i < slen:
            before = None
            after = None
            fs = self.sections[i]
            if fs.key() == sourceKey:
                if i>0:
                    before = self.sections[i-1]
                if i < (slen-1):
                    after = self.sections[i+1]
                err = self.writeBlock(before, fs, after, opts, append)
                if err:
                    return err
            i += 1
        return 0
    # end writeExtracts
               
if __name__ == "__main__":
    pass
# put some test stuff here

