#!/usr/bin/env python
""" A container of several higher-level splicing operations with policy
choices embedded.
   Author: Benjamin Allan
   Org:	Sandia National Laboratories, Livermore
   Date: 5/2006.
   License: GPLv2. Of course this doesn't affect the files that
	are processed by this utility.
"""
import sys
import os.path
from splicers import Source, Data, Misc, Block

def warnMessage(message, fatal=False):
    print "Warning: " , message
    if fatal:
        sys.exit(3)

def getSourceString(inputName, sourceKey, src, fatal=True, dontwarn=False, preserveProtected=False):
    sf = Source.Source()
    status, msg  = sf.loadString(inputName, sourceKey, src, dontwarn, preserveProtected=preserveProtected)
    if status:
        warnMessage(msg, fatal)
    return sf
# end getSourceString

def getSource(srcName, sourceKey, fatal=True, preserveProtected=False):
    sf = Source.Source()
    status, msg  = sf.loadFile(srcName, sourceKey, preserveProtected=preserveProtected)
    if status:
        warnMessage(msg, fatal)
    return sf
# end getSource

def findSplices(symbols, insertions, sf, verbose, methodMatch=False, oldtype="", newtype="", matchSyms=[], excludeSyms=[]):
    """ find blocks from prepared src matching symbols
given and add them to the symbol keyed insertions list.
@param sf Source from which to splice.
@param methodMatch if True, then rename matches from sf are done for symbols,
       taking symbol $oldtype.$method to match $newtype.$method. To insure
       correct operation, oldtype, newtype should be fully qualified sidl names.
@param matchSyms if given is a list of symbols to match in target and ignore all others.
"""

    checkMatchSym = (len(matchSyms) > 0)
    if verbose:
        print "findSplices: user match list=" , matchSyms
        print "findSplices: user exclude list=", excludeSyms
        if methodMatch:
            print "fromType = ", oldtype, "toType = ", newtype

    for j in symbols:

        if excludeSyms and len(excludeSyms) > 0 and Misc.symbolContainsListItem(j, excludeSyms):
            if verbose: print 'Matched excluded symbol, skipping: ' , j
            continue

        if checkMatchSym:
            if not Misc.symbolContainsListItem(j, matchSyms):
                if verbose:
                    print "No Match of " , j 
                continue
            else:
                if verbose:
                    print "Match of " , j 

        p = insertions.get(j, None)
        if methodMatch:
            jold = j.replace(newtype, oldtype)
        else:
            jold = j
        ins = sf.getBlock(jold)

        if ins != None:
            if verbose:
                print "found an insertion for " , j
            if p != None:
                # FIXME whine about duplicate.
                pass
            else:
                if methodMatch:
# this is cleaner in some sense (readonly treatment) but messes up warning management
                    if False:
                        # make a new block from body of old and symbol of new.
                        insfixed = Block.Block()
                        oldlines = ins.getLines()
                        newbegin=oldlines[0].replace(oldtype, newtype)
                        newend=oldlines[len(oldlines)-1].replace(oldtype, newtype)
                        newlines = [newbegin] + oldlines[1:len(oldlines)-2] + [newend ]
                        insfixed.init(ins.key(), newlines, ins.source(), ins.start() )
                        insertions[j] = insfixed
                        if verbose:
                            print "it is len " , len(newlines)
                    else:
                        # modify in place
                        oldlines = ins.getLines()
                        newbegin=oldlines[0].replace(oldtype, newtype)
                        newend=oldlines[len(oldlines)-1].replace(oldtype, newtype)
                        oldlines[0] = newbegin
                        oldlines[len(oldlines)-1] = newend
                        insertions[j] = ins
                else:
                    # transfer from sf to insertions
                    insertions[j] = ins
#end findSplices


def warnMissing( symbols, insertions, warn, warnCommon, commonSuppressions, fatal, matchSyms=[], excludeSyms=[]):
    if warn:
        for i in symbols:
            if not Misc.symbolContainsListItem(i, matchSyms):
                continue
            if len(excludeSyms) > 0 and Misc.symbolContainsListItem(i, excludeSyms):
                continue
            p = insertions.get(i, None)
            if  p == None and \
                (warnCommon or not Misc.isCommon(i, commonSuppressions)):
                msg = "No block or splice found for output symbol " + i
                warnMessage(msg,fatal)
# end warnMissing

def warnSubstitution( target, source ):
    targetSymbols = target.getProtectedSymbols()
    sourceSymbols = source.getProtectedSymbols()

    for sym in targetSymbols:
        if sym not in sourceSymbols:
            warnMessage("Protected symbol "+sym+" appears in target but not source: Overwriting")

    for sym in sourceSymbols:
        if sym not in targetSymbols:
            warnMessage("Protected symbol "+sym+" appears in source but not target: Inserting")

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def mergeFileIntoString(targetName, targetString, srcName, targetKey="DO-NOT-DELETE splicer", sourceKey="DO-NOT-DELETE splicer" , 
                        insertFirst=True, dbg=False , verbose=False, rejectSave=True, warn=True, fatal=True,  warnCommon=False, 
                        commonSuppressions=[], replaceIdentical=False):
    """ merge, a function for merging blocks from a named file into a string, overwriting the target string's blocks if appropriate.
@param targetName a name for error reporting purposes to describe the target string identity.
@param targetString the string to be spliced into from the blocks in the file.
@param srcName the filename to be read.
@param targetKey the splicer tag by which blocks are identified in the string.
@param sourceKey the splicer tag by which blocks are identified in the file.
@param insertFirst where splicing results in nested tags (srcKey != targetKey), blocks from the
       file are inserted ahead of existing block contents, else appended if false.
@param dbg emit various debugging info.
@param verbose narrate the process a bit.
@param rejectSave if true, create a $targetName.rej file of splices removed from string.
@param warn display complaints if appropriate.
@param fatal warnings should be treated as fatal, causing exit.
@param warnCommon if true, warn about unsupplied blocks in the commonSuppressions list.
@param commonSuppressions list of block names which normal people don't want to hear complaints for.
@return string with merged blocks from file, or the input string if something is amiss.
"""

    source = Source.Source()
    if dbg:
        print "loading file " , srcName
    source.loadFile(srcName, sourceKey)

    spliceTo = getSourceString(targetName, targetKey, targetString, fatal)
        
    (status, result) = mergeSourceToString(spliceTo, source, targetName, insertFirst, dbg, verbose, 
                                           rejectSave, warn, fatal,  warnCommon, commonSuppressions, replaceIdentical=replaceIdentical)
    if status:
        return result
    else: 
        return targetString

# end mergeFileIntoString


def mergeFiles(targetName, srcName, targetKey="DO-NOT-DELETE splicer", sourceKey="DO-NOT-DELETE splicer" , 
               insertFirst=True, dbg=False , verbose=False, dryrun=False, rejectSave=True, warn=True, fatal=True,  
               warnCommon=False, commonSuppressions=[], matchSyms=[], excludeSyms=[], methodMatch=False, 
               oldtype="", newtype="", replaceIdentical=True, killSubstrings=None, killBlockKeys=None, srcKillBlockKeys=None,
               preserveProtected=True, outputConflicts=False, commentBegin="", commentEnd=""):
    """ merge, a function for merging two files, the splices from one into the other, overwriting the target file's blocks and leaving the rubble in a .rej
file.
The splice algorithm is:
	Load outputfile, inputFile
	Identify input sections matching sourceKey and extract symbols
		from sourcekey.begin(symbol)/sourcekey.end(symbol) pairs.
		Errors if sections are not well-formed.
	Warn about multiple matches in blocks/splices.
	Warn about non-matches.
	Foreach matching section:
		Scan for targetKey splice, and if present replace it.
		If not found, insert block or splice first or last as given.
                Before scanning target, delete lines in it per killSubstrings and
		killBlockKeys. Default lists are available in Kills.py.
	Write output file if not dryrun.
"""
    source = Source.Source()
    if dbg:
        print "loading file " , targetName
    source.loadFile(targetName, targetKey, preserveProtected=preserveProtected)

    spliceFrom = getSource(srcName, sourceKey, preserveProtected=preserveProtected)
        
    return mergeSources(source, spliceFrom, targetName, srcName, insertFirst, dbg,
                        verbose, dryrun, rejectSave, warn, 
                        fatal, warnCommon, commonSuppressions, 
                        methodMatch=methodMatch, oldtype=oldtype, newtype=newtype, 
                        matchSyms=matchSyms, excludeSyms=excludeSyms, replaceIdentical=replaceIdentical,
                        killSubstrings=killSubstrings, killBlockKeys=killBlockKeys, srcKillBlockKeys=srcKillBlockKeys,
                        preserveProtected=preserveProtected, outputConflicts=outputConflicts, commentBegin=commentBegin,
                        commentEnd=commentEnd)

# end mergeFiles

# might better have been called mergeStringIntoFile.
#
def mergeFromString(targetName, srcString, srcName, targetKey="DO-NOT-DELETE splicer", sourceKey="DO-NOT-DELETE splicer" , 
                    insertFirst=True, dbg=False , verbose=False, dryrun=False, rejectSave=True, warn=True, fatal=True,  warnCommon=False, 
                    commonSuppressions=[], methodMatch=False, oldtype="", newtype="", replaceIdentical=True, srcKillBlockKeys=None, killSubstrings=None,
                    preserveProtected=False, outputConflicts=False):
    """ a function for merging srcString into target file, overwriting or inserting to the target 
file's blocks and leaving the rubble in a .rej file.
The splice algorithm is as mergeFiles.
Merging should not preserve by default - this wants to force all of the source into the target, and
additionally the source is generated by the appropriate version of bocca.
"""
    source = Source.Source()
    if dbg:
        print "loading file " , targetName
    source.loadFile(targetName, targetKey, preserveProtected)

    spliceFrom = getSourceString(srcName, sourceKey, srcString, fatal, preserveProtected=preserveProtected)
        
    return mergeSources(source, spliceFrom, targetName, srcName, insertFirst, dbg, verbose, dryrun, rejectSave, warn, fatal,  
                        warnCommon, commonSuppressions, replaceIdentical=replaceIdentical, 
                        srcKillBlockKeys=srcKillBlockKeys, killSubstrings=killSubstrings, preserveProtected=preserveProtected,
                        outputConflicts=outputConflicts)

# end mergeFromString


def createStubBlock(key, symbol, commentBegin, commentEnd):
    """ creates a stub block for the given key and symbol, indicating that information
    was preserved from the target into the merged file"""
    data = []
    data.append(key + ".begin(" + symbol + ")\n")
    data.append(commentBegin + "   --- BLOCK FOR " + key + "(" + symbol + ") PRESERVED IN OUTPUT " + commentEnd + "\n")
    data.append(key + ".end(" + symbol + ")\n")

    block = Block.Block()
    block.init(key, data, None, 0, None)

    return block

def substitute(toSource, fromSource, insertions, substitutions, rejectedProtected=None,
               insertFirst=True, verbose=False, replaceIdentical=True, commentBegin="",
               commentEnd=""):
    """ substitutes subblocks into containing blocks, returns those symbols in the substitutions
which were ignored"""
    # Copy, don't reference
    substitutionSymbols = substitutions[:]

    if verbose:
        print "Substituting for symbols: ", substitutionSymbols

    # Remove all symbols which appear in one or the other, but not both
    removeSymbols = []
    for symbol in substitutionSymbols[:]:
        if symbol not in toSource.getProtectedSymbols() or symbol not in fromSource.getProtectedSymbols():
            removeSymbols.append(symbol)
            substitutionSymbols.remove(symbol)
    if verbose:
        print "Removed exclusive symbols: ", removeSymbols

    for (sourceSymbol, sourceBlock) in insertions.iteritems():
        for substSymbol in sourceBlock.getSubsymbols():
            if substSymbol in substitutionSymbols:
                # Replace block in source
                protectedBlock = toSource.getProtectedBlock(substSymbol)
                sourceBlock.insertNested(protectedBlock, not insertFirst, rejectLines=rejectedProtected,
                                         replaceIdentical=replaceIdentical, requireSymbol=substSymbol)
                if verbose:
                    print "Inserted block with symbol ",substSymbol," into source block ",sourceSymbol

                # Insert stub in target
                targetBlock = toSource.getBlock(sourceSymbol)
                stubBlock = createStubBlock(protectedBlock.key(), substSymbol, commentBegin, commentEnd)
                targetBlock.insertNested(stubBlock, not insertFirst, replaceIdentical=replaceIdentical,
                                         requireSymbol=substSymbol)
                if verbose:
                    print "Inserted stub for symbol ",substSymbol," into target block ",sourceSymbol
            # end if
        # end for
    # end for
    return removeSymbols
#end substitute

def insertDiff(target, source, insertions, ignoredSubsymbols, commentBegin='', commentEnd='', verbose=False):
    """ inserts a diff of the form
<<<< target : line
  ...
========
>>>> source : line
  ...
into blocks which contain the given subsymbols."""

    for subsymbol in ignoredSubsymbols:
        for symbol in insertions.keys()[:]:
            targetBlock = target.getBlock(symbol)
            sourceBlock = source.getBlock(symbol)
            if subsymbol in targetBlock.getSubsymbols() or subsymbol in sourceBlock.getSubsymbols():
                if verbose:
                    print "Inserting diff into block with symbol ",symbol
                # Create the diff block
                blockData = []
                targetLines = targetBlock.getLines()
                sourceLines = sourceBlock.getLines()
                blockData.append(targetLines[0])
                blockData.append(commentBegin + "<<<< " + targetBlock.source() + ":" + str(targetBlock.start()) + commentEnd + "\n")
                # Skip the begin/end lines
                for line in targetLines[1:len(targetLines)-1]:
                    blockData.append(commentBegin + line.strip("\n") + commentEnd + "\n")
                blockData.append(commentBegin + "===============" + commentEnd + "\n")
                blockData.append(commentBegin + ">>>>" + sourceBlock.source() + ":" + str(sourceBlock.start()) + commentEnd + "\n")
                for line in sourceLines[1:len(sourceLines)-1]:
                    blockData.append(commentBegin + line.strip("\n") + commentEnd + "\n")
                # Closing line
                blockData.append(targetLines[len(targetLines)-1])

                # Replace block in insertions with the diff
                insertions[symbol] = Block.Block()
                insertions[symbol].init(targetBlock.key(), blockData, "internalDiff", sourceBlock.start(), [])
            # end if
        # end for
    # end for
#end insertDiff

def mergeSources(source, spliceFrom, targetName, srcName, insertFirst=True, dbg=False , verbose=False, dryrun=False, rejectSave=True, 
                 warn=True, fatal=True, warnCommon=False, commonSuppressions=[], methodMatch=False, oldtype="", newtype="", 
                 matchSyms=[], excludeSyms=[], replaceIdentical=True, killSubstrings=None, killBlockKeys=None, srcKillBlockKeys=None,
                 preserveProtected=False, outputConflicts=False, commentBegin="", commentEnd=""):
    """As mergeFiles, less the file-opening policies."""

    if verbose:
        print "processing insertions"
    symbols = source.getSymbols()
    result = 0

    insertions = {}
    spliceFrom.tagSymbols(1)

    findSplices( symbols, insertions, spliceFrom, verbose, methodMatch, oldtype, newtype, matchSyms, excludeSyms)

    # we can generate insertions in other ways; needn't be file readers.
    # see Source.loadList

    warnMissing(symbols, insertions, warn, warnCommon, commonSuppressions, False, matchSyms, excludeSyms)

    rejects=[]
    rejectedProtected=[]

    if preserveProtected:
        ignoredSubsymbols = substitute(source, spliceFrom, insertions, source.getProtectedSymbols(), rejectedProtected=rejectedProtected, 
                                       insertFirst=insertFirst, verbose=verbose, replaceIdentical=replaceIdentical, commentBegin=commentBegin,
                                       commentEnd=commentEnd)
        if outputConflicts:
            insertDiff(source, spliceFrom, insertions, ignoredSubsymbols, commentBegin, commentEnd, verbose)
        elif warn:
            warnSubstitution(source, spliceFrom)

    for first, second in insertions.iteritems():
        source.insert(first, second, insertFirst, rejects, verbose, replaceIdentical=replaceIdentical, 
                      killMatches=killSubstrings, killBlockKeys=killBlockKeys, srcKillBlockKeys=srcKillBlockKeys)
        second.setTag(0)
    #end for
    
    warnExtra(warn, spliceFrom, matchSyms, excludeSyms)

    if not source.write(outFileName=targetName, verbose=verbose, dryrun=dryrun, rejectSave=rejectSave, 
                        rejectLines=rejects):
        result = 1

    if rejectSave and preserveProtected and len(rejectedProtected) > 0 and srcName != '':
        protectedRejectFile = srcName + '.protected.rej'
        if not spliceFrom.writeRejects(protectedRejectFile, rejectedProtected, originalFile=srcName, verbose=verbose):
            result = 1
    
    return result

# end mergeSources

def mergeSourceToString(source, spliceFrom, targetName, insertFirst=True, dbg=False , verbose=False, rejectSave=False, 
                        warn=True, fatal=True, warnCommon=False, commonSuppressions=[], replaceIdentical=False,
                        preserveProtected=False):
    """As mergeFiles, less the file-opening policies and the file writing policies.
@param source a Source object to be modified.
@param spliceFrom a Source object to be searched for splices to apply.
@param targetName name for error message and .rej file purposes of the string.
@param insertFirst append/prepend for nested blocks.
@return (status, string) a string of the resulting source if status true."""

    if verbose:
        print "processing insertions"
    symbols = source.getSymbols()

    insertions = {}
    spliceFrom.tagSymbols(1)
    findSplices( symbols, insertions, spliceFrom, verbose)

    warnMissing(symbols, insertions, warn, warnCommon, commonSuppressions, False)

    rejects=[]
    rejectedProtected=[]

    if preserveProtected:
        substitute(source, spliceFrom, insertions, source.getProtectedSymbols(), 
                   insertFirst=insertFirst, verbose=verbose, replaceIdentical=replaceIdentical)
        if warn:
            warnSubstitution(source, spliceFrom)

    for first, second in insertions.iteritems():
        source.insert(first, second, insertFirst, rejects, verbose, replaceIdentical=replaceIdentical)
        second.setTag(0)
    
    warnExtra(warn, spliceFrom)

    return source.writeString(outFileName=targetName, verbose=verbose, rejectSave=rejectSave, rejectLines=rejects)

# end mergeSourceToString

def warnExtra(warn, src, matchSyms=[], excludeSyms=[]):
    if warn:
        extras = src.getTaggedSymbols(1)
        for i in extras:
            if not Misc.symbolContainsListItem(i, matchSyms):
                continue
            if len(excludeSyms) > 0 and Misc.symbolContainsListItem(i, excludeSyms):
                continue
            warnMessage("Unused splice from input: "+i, False)

def renameInFiles(targetName, srcName, targetKey="DO-NOT-DELETE splicer", sourceKey="DO-NOT-DELETE splicer", 
                  insertFirst=True, dbg=False , verbose=False, dryrun=False, rejectSave=True, 
                  warn=True, fatal=True,  warnCommon=False, commonSuppressions=[], oldtype="", newtype="" ):
    """ rename, a function for overwriting the target file's blocks with a set of blocks from
the source file that should have a matching set of symbols differing by a prefix  (sidl class).
oldtype and newtype are fully qualified, not partial names.
The targetfile contains blocks (most probably unpopulated, and to be replaced) tagged
with symbols derived from newtype.
The source file contains blocks tagged with symbols derived from oldtype.
"""

    source = Source.Source()
    if dbg:
        print "loading file " , targetName
    source.loadFile(targetName, targetKey)
        
    spliceFrom = getSource(srcName, sourceKey, warn)

    return renameSources(source, spliceFrom, targetName, insertFirst, dbg, verbose, dryrun, rejectSave, warn, fatal, warnCommon, commonSuppressions, oldtype, newtype)
    
# end renameInFiles

def renameFromFile(targetName, srcName, targetBuffer, targetKey="DO-NOT-DELETE splicer", sourceKey="DO-NOT-DELETE splicer", 
                   insertFirst=True, dbg=False , verbose=False, dryrun=False, rejectSave=True, 
                   warn=True, fatal=True,  warnCommon=False, commonSuppressions=[], oldtype="", newtype="" ):
    """  a function for creating the target file from a target buffer with blocks from
the source file that should have a matching set of symbols differing by a prefix  (sidl class).
oldtype and newtype are fully qualified, not partial names.
The targetBuffer contains blocks (most probably unpopulated, and to be replaced) tagged
with symbols derived from newtype.
The source file contains blocks tagged with symbols derived from oldtype.
"""

    if dbg:
        print "loading file " , targetName
    source = getSourceString(targetName, targetKey, targetBuffer)
        
    spliceFrom = getSource(srcName, sourceKey)
    return renameSources(source, spliceFrom, targetName, insertFirst, dbg, verbose, dryrun, rejectSave, warn, fatal, warnCommon, commonSuppressions, oldtype, newtype)

# end renameFromFile

def renameSources(source, spliceFrom, targetName, insertFirst=True, dbg=False , verbose=False, dryrun=False, rejectSave=True, warn=True, fatal=True,  
                  warnCommon=False, commonSuppressions=[], oldtype="", newtype=""):
    if verbose:
        print "processing renames"
    symbols = source.getSymbols()
    result = 0

    insertions = {}
    findSplices( symbols, insertions, spliceFrom, verbose, True, oldtype, newtype)
    spliceFrom.tagSymbols(1)
    # we can generate insertions in other ways; needn't be file readers.
    # see Source.loadList

    warnMissing(symbols, insertions, warn, warnCommon, commonSuppressions, False)

    rejects=[]
    for first, second in insertions.iteritems():
        source.replace(first, second, rejects, verbose)
        second.setTag(0)
    
    warnExtra(warn, spliceFrom)

    if not source.write(outFileName=targetName, verbose=verbose, dryrun=dryrun, rejectSave=rejectSave, rejectLines=rejects):
        result = 1
    
    return result
# end renameFromFile

def doBlockReplacements(targetName, replacementData, targetKey, sourceKey, methodMatch=False, oldtype="", newtype="", 
                        verbose=False, dryrun=False, rejectSave=True, insertFirst=True, dbg=False, warn=True, warnCommon=True, 
                        commonSuppressions=[]):
    """ Overwrite blocks with matching symbols in the target Source object.
replacementData is a multiline string.
If methodMatch is true, ignores, matches occurrences of 
symbol oldtype.$method to newtype.$method, for example in
renaming an impl from oldtype to newtype.
"""
    if dbg:
        print "loading file " , targetName
    source = getSource(targetName, targetKey, True)
        
    if verbose:
        print "processing insertions"
    symbols = source.getSymbols()
    result = 0

    insertions = {}
    spliceFrom = getSourceString("doBlockReplacements.spliceFrom", sourceKey, replacementData, True)
    findSplices( symbols, insertions, spliceFrom, verbose, methodMatch, oldtype, newtype)

    warnMissing(symbols, insertions, warn, warnCommon, commonSuppressions, False)

    rejects=[]

    for first, second in insertions.iteritems():
        source.insert(first, second, insertFirst, rejects, verbose)
    
    print targetName
    if not source.write(outFileName=targetName, verbose=verbose, dryrun=dryrun, rejectSave=rejectSave, rejectLines=rejects):
        result = 1
    
    return result

# doBlockReplacements


def doBlockInsertions(target, insertionData, insertFirst=True):
    """ Insert lines with matching symbols in the target Source object.
If insertFirst is true, existing code is prepended, else appended.
insertionData is a multiline string.
"""
    pass

if __name__ == "__main__":
    print >>sys.stderr, "Operations class has no main yet"
    sys.exit(1)
