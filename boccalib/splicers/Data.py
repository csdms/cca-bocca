""" attempt at porting cxx splicer args to python """
import sys
import os
from optparse import OptionParser
import cct._err, cct._debug, cct._validate
from cct._util import *
from cct._file import *

def cppSuppressions(vals):
    vals.commonSuppressions.append("_misc")
    vals.commonSuppressions.append("_inherits")
    vals.commonSuppressions.append("_ctor2")
    vals.commonSuppressions.append("_load")

def checkKeys(vals, prefix, defkey):
    if vals.sourceKey == "unset":
        vals.sourceKey = prefix + defkey
    if vals.targetKey == "unset":
        vals.targetKey = prefix + defkey

def setLangDefaults(vals, lang):
    defkey = " DO-NOT-DELETE splicer"
    boccakey = " DO-NOT-DELETE bocca.splicer"
    vals.commentBegin="";
    vals.commentEnd="";
    vals.killKeys=[]
    vals.killKeys.append("Insert-Code-Here");
    vals.killKeys.append("noImpl");
    vals.killKeys.append("This method has not been implemented");
    vals.killKeys.append("::sidl::NotImplementedException");
    vals.killKeys.append("    throw ex;");
    vals.killKeys.append("call sidl_NotImplementedException");
    vals.indent="  ";

    if lang == "sidl":
        vals.language = "sidl";
        checkKeys(vals,"//", boccakey)
        vals.blockFilePrefix=""
        vals.blockFileSuffix=".sidl.block"
        vals.spliceHeader="//"
        vals.commentBegin = "//";

    if lang == "cxx" or lang == "ucxx"  or lang == "CC"  or lang == "c++":
        vals.language = "cxx";
        checkKeys(vals,"//", defkey)
        vals.blockFilePrefix=""
        vals.blockFileSuffix=".hxx"
        vals.spliceHeader="//"
        vals.commentBegin="//"
        cppSuppressions(vals)

    if lang == "ocxx":
        vals.language = "cxx"
        checkKeys(vals,"//", defkey)
        vals.blockFilePrefix=""
        vals.blockFileSuffix=".hh"
        vals.spliceHeader="//"
        vals.commentBegin="//"
        cppSuppressions(vals)

    if lang == "c"  or  lang == "C":
        vals.language = "c"
        checkKeys(vals,"/*", defkey)
        vals.blockFilePrefix=""
        vals.blockFileSuffix=".h"
        vals.spliceHeader="/**/"
        vals.commentBegin=" /*"
        vals.commentEnd=" */"

    if lang == "f77"  or  lang == "F77"  or  lang == "fortran77" or lang == "f77_31":
        vals.language = "f77"
        checkKeys(vals,"!", defkey)
        vals.blockFilePrefix=""
        vals.blockFileSuffix=".f90.insert"
        vals.spliceHeader="CC"
        vals.indent = ""
        vals.commentBegin="!"

    if lang == "f90"  or  lang == "F90"  or  lang == "f95"  or  lang == "f03"  or  lang == "fortran"  or  lang == "fortran90":
        vals.language = "f90"
        checkKeys(vals,"!", defkey)
        vals.blockFilePrefix=""
        vals.blockFileSuffix=".f90.insert"
        vals.spliceHeader="!!"
        vals.commentBegin="!"

    if lang == "java"  or  lang=="Java":
        vals.language = "java"
        checkKeys(vals,"//", defkey)
        vals.blockFilePrefix=""
        vals.blockFileSuffix=".java.insert"
        vals.spliceHeader="//"
        vals.commentBegin="//"
        cppSuppressions(vals)

    if lang == "python"  or  lang == "Python":
        vals.language = "python"
        checkKeys(vals,"#", defkey)
        vals.blockFilePrefix=""
        vals.spliceHeader="##"
        vals.blockFileSuffix=".py.insert"
        vals.indent=""
        vals.commentBegin="#"


def usage(code, msg):
    print >> sys.stderr, msg
    exit(code)

def o_callback(option, opt, value, parser):
    parser.values.outputDirGiven=True
    parser.values.outputDir=value
    if value == None or len(value) < 1:
        raise OptionValueError("%s must be followed by a directory name" % opt)
    # here is not a correct place to check for existence in filesystem

def K_callback(option, opt, value, parser):
    parser.values.keepLines=True
    parser.values.genLines=False

def G_callback(option, opt, value, parser):
    parser.values.keepLines=False
    parser.values.genLines=True

def Y_callback(option, opt, value, parser):
    parser.values.dryrun=True
    parser.values.verbose=True

def c_callback(option, opt, value, parser):
    if value == None or len(value) < 1:
        raise OptionValueError("%s must be followed by a sidl method name" % opt)
    parser.values.commonSuppressions.append(value)
    
def x_callback(option, opt, value, parser):
    if value == None or len(value) < 1:
        raise OptionValueError("%s must be followed by a symbol fragment" % opt)
    parser.values.excludeSyms.append(value)
    
def m_callback(option, opt, value, parser):
    if value == None or len(value) < 1:
        raise OptionValueError("%s must be followed by a symbol fragment" % opt)
    parser.values.matchSyms.append(value)
    
def i_callback(option, opt, value, parser):
    if value == None or len(value) < 1:
        raise OptionValueError("%s must be followed by inputDir or RESET to empty the include path." % opt)
    if value == "RESET":
        parser.values.inputDirs=[]
    else:
        parser.values.inputDirs.append(value)
    
def kill_callback(option, opt, value, parser):
    if value == None or len(value) < 1:
        raise OptionValueError("%s must be followed by fragment to remove or RESET to empty the kill list." % opt)
    if value == "RESET":
        parser.values.killKeys=[]
    else:
        parser.values.killKeys.append(value)
    
def l_callback(option, opt, value, parser):
    if value == None or len(value) < 1:
        raise OptionValueError("%s must be followed by a sidl language name" % opt)
    parser.values.language=value
    setLangDefaults(parser.values, value)
    
def T_callback(option, opt, value, parser):
    if value == None or len(value) < 1:
        raise OptionValueError("%s must be followed by a file name" % opt)
    parser.values.outputFile=value
    parser.values.robMode=True
    
def F_callback(option, opt, value, parser):
    if value == None or len(value) < 1:
        raise OptionValueError("%s must be followed by a file name" % opt)
    parser.values.inputFile=value
    parser.values.robMode=True
    
def ft_callback(option, opt, value, parser):
    if value == None or len(value) < 1:
        raise OptionValueError("%s must be followed by a SIDL class name" % opt)
    parser.values.fromType=value
    
def tt_callback(option, opt, value, parser):
    if value == None or len(value) < 1:
        raise OptionValueError("%s must be followed by a SIDL class name" % opt)
    parser.values.toType=value
    

def parseargs(args):
    
    """ Returns 2-tuple {options args}
Exits nonzero if user gives bad input.
"""
    clusage="""
    resplice [options] implFile [spliceFile ...]

The first (insertion) mode replaces or inserts splices in implFile as follows:
If no options are given, the current directory is checked for blocks to be
inserted that match the blocks found in implFile.
If spliceFiles are given, they are read looking for blocks that
match the target key given.
Block files contain single blocks of code and no Key lines; they
are found by filename convention only.
Splice files contain complete splices with target Keys in place
and may be named in any way.
Any lines that are deleted from implFile get put in implFile.rej.

"""
    parser = OptionParser(clusage)
    parser.set_defaults(        outputDirGiven=False,    # dir from user?
        outputDir=".",    #  where it should go if not on top of source.
        outputFile="",    #  where it should go if not in .splice
        language="unset",    #  file type we're inserting to.
        inputFile="unset", # input file for rob mode, normally a positional arg.
        inputDirs=["."], #  source of splice blocks and possibly input
        sourceKey="unset",    #  splice delimiter including commenting
        targetKey="unset",    #  delimiter for insertions
        killKeys=[], #  matches for lines to delete before splicing.
        insertFirst=True, #  True: insert after sourceKey.begin; False: insert before sourceKey.end
        blockFilePrefix="",    #  block file prefix on sidl symbol
        blockFileSuffix="",    #  block file suffix on sidl symbol
        fromType="",    #  source splice sidl class name, if different from target.
        toType="",    #  target splice sidl class name, if different from source.
        methodMatch=False, # if a rename and totype, fromtype are specified.
        indent="",        #  indent before delimiters
        commentBegin="",  #  comment start, used in merge diffs
        commentEnd="",    #  if delimiter must be closed, use this.
        blocks=True,        #  search for block files or use splices only.
        duplicates=True,    #  allow dups in path or extra path checking.
        warnCommon=True,    #  True if we should warn about missing commonSuppressions
        warn=True,        #  True if we should warn about methods w/out splices
        warnExtra=False,        #  True if we should warn about splices w/o methods
        fatal=False,        #  True if warnings should be treated as errors
        dryrun=False,        #  True if we should be verbose and nondestructive
        verbose=False,        #  procedural narration.
        dbg=False,        #  True to get debugging spew
        rejectSave=True,    #  output to reject file
        keepLines=False,        #  keep #line from input if True.
        genLines=False,        #  generate c #lines based implFile location.
        spliceHeader="",    #  comment to make a line of.
        commonSuppressions=[], #  list of functions to ignore usually
        vpathDir="",    #  alternate source impl dir
        robMode = False, # ruby emulation
        matchSyms=[],    #  symbol fragments to match in from/source.
        excludeSyms=[],  #  symbol fragments to ignore in from/source.
        spliceFiles=[], #  optional splice files
        rejectLines=[], # deleted/replaced lines
        preserveProtected = True, # preserve bocca.protected blocks in target
        outputConflicts = False # flag for putting diff-style output in target for corner cases w/protected
       )


    parser.add_option("-D", "--output-dir", action="callback", callback=o_callback, type="string", help="Where to write the outputs; default is current directory.")

    parser.add_option("-c", "--suppress", action="callback", callback=c_callback, type="string", help="funcName : add funcName to the suppressed common warnings list.")

    parser.add_option("-l", "--language", action="callback", callback=l_callback, type="string", help="LANG : Where LANG is c,cxx,f90,f03,f77,f77_31,python,java,sidl. Default cxx.")

    parser.add_option("-k", "--kill-key", action="callback", callback=kill_callback, type = "string", help="killKey : Lines matching killKey(s) will be removed if a splice matching the symbol is available.")

    parser.add_option("-i", "--include", action="callback", callback=i_callback, type="string", help="inputDir or RESET: Where to find the input blocks.  Multiple -i options are allowed and they will be searched in the order of appearance. The default -i is the current directory. RESET empties the include path.")

    parser.add_option("-A", "--target-key", type="string", dest="targetKey", help="targetSpliceKey : The start word of the blocks to be edited.  The default targetSpliceKey is 'DO-NOT-DELETE splicer'.")
    parser.add_option("-B", "--source-key", type="string", dest="sourceKey", help="sourceSpliceKey : The start word ([a-zA-Z0-9.] are permitted characters) of the blocks in the input edits which are to be inserted. The default sourceSpliceKey matches that of babel 1.0 splicer blocks. The bocca insert keys vary.")

    parser.add_option("-p", "--block-file-prefix", type="string", dest="blockFilePrefix", help="blockFilePrefix : Block files to be inserted must match the pattern $blockFilePrefix$babel.impl.blockName$blockFileSuffix.")
    parser.add_option("-s", "--block-file-suffix", type="string", dest="blockFileSuffix", help="blockFileSuffix : as -p, but the suffix on input files.")
    parser.add_option("-f", "--output-file", type="string", dest="outputFile", help="output name if not same as input.")
    parser.add_option("-V", "--vpath", type="string", dest="vpathDir", help="srcDir : Directory other than . to find implFile in.")
    parser.add_option("-d", "--debug", action="store_true", dest="dbg", help="print debug output")
    parser.add_option("-b", "--insert-first", action="store_true", dest="insertFirst", help="insert at beginning of block (opposite is -e, last seen wins)")
    parser.add_option("-e", "--insert-last", action="store_false", dest="insertFirst", help="insert at end of block (opposite is -b, last seen wins)")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="print process narration")
    parser.add_option("-r", "--no-rejects", action="store_false", dest="rejectSave", help="If overwriting during splice, we put discarded text in output-file.rej. This option stops that.")
    parser.add_option("-G","--gen-lines", action="callback", callback=G_callback, help="Create line directives indicating origin of splice.  gen-lines and keep-lines are mutually exclusive. Last seen wins.")
    parser.add_option("-Y", "--dryrun", action="callback", callback=Y_callback, help="List what would be done, but don't do it.")
    parser.add_option("-X", "--fatal", action="store_true", dest="fatal", help="Treat warnings as errors.")
    parser.add_option("-C", "--nocommon", action="store_false", dest="warnCommon", help="Suppress warnings about blocks found in the input implFile that have no block insert provided and that are commonly unimplemented.")
    parser.add_option("-W", "--nowarn", action="store_false", dest="warn", help="Suppress warnings about all implFile blocks without an insertion.")
    parser.add_option("-P", "--noblocks", action="store_false", dest="blocks", help="Do not search for blocks, use only spliceFiles.")
    parser.add_option("-Q", "--noduplicates", action="store_false", dest="duplicates", help="Scan entire search path and warn about duplicate blocks.")
    parser.add_option("-R", "--noextra", action="store_true", dest="warnExtra", help="Warn about splices w/o methods")
    parser.add_option("-Z", "--robMode", action="store_true", dest="robMode", help="ruby splicer imitation")
    parser.add_option("-T", "--to", action="callback", type="string", callback=T_callback, help="target input/output file if robMode in effect.")
    parser.add_option("-F", "--from", action="callback", type="string", callback=F_callback, help="splice block input file if robMode in effect.")
    parser.add_option( "--from-type", action="callback", type="string", callback=ft_callback, help="sidl name of source class to be renamed before splicing")
    parser.add_option( "--to-type", action="callback", type="string", callback=tt_callback, help="sidl name of target class being spliced from a differently named source")
    parser.add_option("-m", "--match", action="callback", type="string", callback=m_callback, help="match : Merge all symbols containing match. Multiple use ok. Ignore nonmatching symbols.")
    parser.add_option("-x", "--exclude", action="callback", type="string", callback=x_callback, help="exclude : Exclude all symbols containing match. Multiple use ok. ")
    parser.add_option("--no-preserve", action="store_false", dest="preserveProtected", help="Overwrite bocca.protected blocks in target with protected blocks from source.")
    parser.add_option("--output-missing-protected-conflicts", action="store_true", dest="outputConflicts",
                      help="For bocca.protected blocks which only appear in source or target, print diff-style output for the containing key blocks.")


    options, args = parser.parse_args(args)
    if options.language == "unset":
        setLangDefaults(parser.values, "cxx")
    if (not options.fromType == "") and (not options.toType == ""):
        options.methodMatch = True
    return (options, args)
        
#------------------------------------------------
def validateOpts(opts):
    language = opts.language
    if not language in [ "C", "c" , "ucxx", "ocxx" , "cxx", "c++" , "uc++" , "CC", "f90", "f03", "f77", "f77_31" , "java" , "python", "sidl"]:
        print "Unknown output language: ", language
        return False
    if not opts.blocks  and  len(opts.spliceFiles) < 1:
        print "No blocks and no splices specified."
        return False;
    if len(opts.sourceKey) <1:
        print "Empty sourceKey not allowed."
        return False
    if len(opts.targetKey) < 1:
        print "Empty targetKey not allowed."
        return False;
    if not opts.preserveProtected and opts.outputConflicts:
        print "--no-preserve and --output-missing-protected-conflicts are incompatible options."
        return False
    return True;

#------------------------------------------------

def printopts(opt):
    print "outputDir= " , opt.outputDir
    print "outputFile= " , opt.outputFile
    print "language= " , opt.language
    print "inputFile= " , opt.inputFile
    print "sourceKey= " , opt.sourceKey
    print "targetKey= " , opt.targetKey
    print "killKeys= " , opt.killKeys
    print "insertFirst= " , opt.insertFirst
    print "blockFilePrefix= " , opt.blockFilePrefix
    print "blockFileSuffix= " , opt.blockFileSuffix
    print "indent= " , opt.indent
    print "commentBegin= ", opt.commentBegin
    print "commentEnd= " , opt.commentEnd
    print "blocks= " , opt.blocks
    print "duplicates= " , opt.duplicates
    print "warnCommon= " , opt.warnCommon
    print "warn= " , opt.warn
    print "warnExtra= " , opt.warnExtra
    print "fatal= " , opt.fatal
    print "dryrun= " , opt.dryrun
    print "verbose= " , opt.verbose
    print "dbg= " , opt.dbg
    print "rejectSave= " , opt.rejectSave
    print "keepLines= " , opt.keepLines
    print "genLines= " , opt.genLines
    print "inputDirs= " , opt.inputDirs
    print "spliceHeader= " , opt.spliceHeader
    print "matchSyms= " , opt.matchSyms
    print "excludeSyms= " , opt.excludeSyms
    print "commonSuppressions= " , opt.commonSuppressions
    print "vpathDir= " , opt.vpathDir
    print "robMode = " , opt.robMode 
    print "spliceFiles= " , opt.spliceFiles
    print "rejectLines= " , opt.rejectLines
    print "preserveProtected= ", opt.preserveProtected
    print "outputConflicts= ", opt.outputConflicts

#------------------------------------------------
def main(args):
    options, args = parseargs(args)
    print >> DEBUGSTREAM, "sopt remaining args " , str(args)
    if len(args) < 1:
        print >> DEBUGSTREAM, "sopt called without inputfile"
        return 1
    if len(options.inputFile) <1 :
        options.inputFile = args[0]
    if len(args) > 1:
        options.spliceFiles.extend(args[1:])

    printopts(options)

    return 0

if __name__ == "__main__":
    main(sys.argv)

