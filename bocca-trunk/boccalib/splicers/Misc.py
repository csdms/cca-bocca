"""utility functions for drivers"""

import re
import Line
import os.path

# a test to determine if reversed() exists in this python interpreter.
try:
    reversedok=True
    l=[1,2,3]
    for ireversed in reversed(l):
        break
except:
    reversedok=False

def symbolContainsListItem(sym, matchSubs):
    """Is a element in the list a substring of the symbol?
@param symbol the string we want to find a match within
@param matchSubs the possible substrings to look for.
If matchSubs is the empty list, the result is always True, 
which may be counter intuitive. All strings match the null list.
null string entries of matchsubs are ignored.
"""
    if len(matchSubs) < 1: 
        # print "symbolContainsListItem: empty matchSubs. True"
        return True
    for match in matchSubs:
        if len(match) == 0:
            continue
        if sym.find(match) >= 0:
            # print "symbolContainsListItem: match of ", sym, "containing", match, "True"
            return True
        else:
            # print "symbolContainsListItem: no match of ", sym, "containing", match, "False"
            pass
    return False

def computeOutputFileName(inputFile, outputFile=None, outputDir=None):
    fname=""
    print "computeofn", "i=", inputFile, "o=", outputFile, "d=", outputDir
    if outputFile != None and len(outputFile) > 0:
        if os.path.isabs(outputFile):
            fname = outputFile
        else:
            fname = os.path.join(outputDir , outputFile)
    else:
        if os.path.isabs(inputFile):
            if outputDir != None:
                fname = outputDir + os.path.basename(inputFile)
            else:
                fname = inputFile
        else:
            if outputDir != None:
                fname = os.path.join(outputDir, inputFile)
            else:
                fname = inputFile
    return fname

def isCommon(sym, commonSuppressions):
    """returns True if symbol matches commonSuppressions entry."""
    method = Line.methodName(sym)
    if method in commonSuppressions:
        return True
    return False
    
def isKillable(line, killLineMatches, killBlockKeys, inKillBlock):
    for i in killKeys:
        if re.match(i, line):
            return True
    return False

if __name__ == "__main__":
    pass # need testing here
