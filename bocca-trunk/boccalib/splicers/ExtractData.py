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

def setLangDefaults(vals, lang):
    vals.commentEnd="";
    vals.killKeys=[]
    vals.killKeys.append("Insert-Code-Here");
    vals.killKeys.append("noImpl");
    vals.killKeys.append("This method has not been implemented");
    vals.killKeys.append("::sidl::NotImplementedException");
    vals.killKeys.append("    throw ex;");
    vals.killKeys.append("call sidl_NotImplementedException");
    vals.indent="  ";

    if lang == "cxx" or lang == "ucxx"  or lang == "CC"  or lang == "c++":
        vals.language = "cxx";
        vals.sourceKey="// DO-NOT-DELETE splicer";
        vals.targetKey="// DO-NOT-DELETE splicer";
        vals.blockFilePrefix="";
        vals.blockFileSuffix=".hxx.block";
        vals.spliceHeader="//";
        cppSuppressions(vals);

    if lang == "ocxx":
        vals.language = "cxx";
        vals.sourceKey="// DO-NOT-DELETE splicer";
        vals.targetKey="// DO-NOT-DELETE splicer";
        vals.blockFilePrefix="";
        vals.blockFileSuffix=".hh.block";
        vals.spliceHeader="//";
        cppSuppressions(vals);

    if lang == "c"  or  lang == "C":
        vals.language = "c";
        vals.sourceKey="/* DO-NOT-DELETE splicer";
        vals.targetKey="/* DO-NOT-DELETE splicer";
        vals.blockFilePrefix="";
        vals.blockFileSuffix=".h.block";
        vals.spliceHeader="/**/";
        vals.commentEnd=" */";

    if lang == "f77"  or  lang == "F77"  or  lang == "fortran77"  or  lang == "f77_31":
        vals.language = "f77";
        vals.sourceKey="C       DO-NOT-DELETE splicer";
        vals.targetKey="C       DO-NOT-DELETE splicer";
        vals.blockFilePrefix="";
        vals.blockFileSuffix=".f77.block";
        vals.spliceHeader="CC";
        vals.indent = "";

    if lang == "f90"  or  lang == "F90"  or  lang == "f95"  or  lang == "f03"  or  lang == "fortran"  or  lang == "fortran90":
        vals.language = "f90";
        vals.sourceKey="! DO-NOT-DELETE splicer";
        vals.targetKey="! DO-NOT-DELETE splicer";
        vals.blockFilePrefix="";
        vals.blockFileSuffix=".f90.block";
        vals.spliceHeader="!!";

    if lang == "xml":
        vals.language = "xml";
        vals.sourceKey="<!-- DO-NOT-DELETE splicer";
        vals.targetKey="<!-- DO-NOT-DELETE splicer";
        vals.blockFilePrefix="";
        vals.blockFileSuffix=".xml.block";
        vals.spliceHeader="##XML##";

    if lang == "java"  or  lang=="Java":
        vals.language = "java";
        vals.sourceKey="// DO-NOT-DELETE splicer";
        vals.targetKey="// DO-NOT-DELETE splicer";
        vals.blockFilePrefix="";
        vals.blockFileSuffix=".java.block";
        vals.spliceHeader="//";
        cppSuppressions(vals);

    if lang == "python"  or  lang == "Python" or lang == "tcsh" or lang == "csh" or lang == "sh" or lang == "bash":
        vals.blockFilePrefix=""
        vals.spliceHeader="##"
        vals.sourceKey="# DO-NOT-DELETE splicer"
        vals.targetKey="# DO-NOT-DELETE splicer"
        vals.indent=""
        vals.blockFileSuffix = lang+".block"
        vals.language = lang
        if lang == "Python" or lang == "python":
            vals.blockFileSuffix=".py.block"
            vals.language = "python"

    if lang == "sidl"  or  lang == "SIDL" or lang == "Sidl":
        vals.language = "sidl";
        vals.sourceKey="// DO-NOT-DELETE bocca.splicer";
        vals.targetKey="// DO-NOT-DELETE bocca.splicer";
        vals.blockFilePrefix="";
        vals.spliceHeader="////";
        vals.blockFileSuffix=".sidl.block";
        vals.indent="";


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
    

def parseargs(args):
    
    """ Returns 2-tuple {options args}
Exits nonzero if user gives bad input.
"""
    clusage="""
    bocca-extract [options] implFile

Extract splices with sourceKey from implFile and disposes of them as indicated by options.  By default output is one symbol per file to the output directory
in a filename derived from the symbol names and language.

"""
    parser = OptionParser(clusage)
    parser.set_defaults(        outputDirGiven=False,    # dir from user?
        outputDir=".",    #  where it should go if not on top of source.
        outputFile="",    #  where it should go if not in .splice
        language="unset",    #  file type we're inserting to.
        inputFile="unset", # input file for rob mode, normally a positional arg.
        inputDirs=["."], #  source of splice blocks and possibly input
        sourceKey="",    #  splice delimiter including commenting
        targetKey="",    #  delimiter for insertions
        killKeys=[], #  matches for lines to delete before splicing.
        insertFirst=True, #  True: insert after sourceKey.begin; False: insert before sourceKey.end
        blockFilePrefix="",    #  block file prefix on sidl symbol
        blockFileSuffix="",    #  block file suffix on sidl symbol
        indent="",        #  indent before delimiters
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
        extract=False,        #  True to get extract instead of insert.
        linesBefore=0,    #  how much before context to keep in extraction.
        linesAfter=0,        #  how much after context to keep in extraction.
        signatures=False,    #  try for sigs in extraction
        method=False,		# signature and -a per language.
        methodcomment=False,	# premethod comment block with signature
        singleFile=False,    #  output to single file
        rejectSave=True,    #  output to reject file
        keepLines=False,        #  keep #line from input if True.
        genLines=False,        #  generate c #lines based implFile location.
        matchSyms=[],    #  symbol fragments to match.
        spliceHeader="",    #  comment to make a line of.
        commonSuppressions=[], #  list of functions to ignore usually
        vpathDir="",    #  alternate source impl dir
        robMode = False, # ruby emulation
        spliceFiles=[], #  optional splice files
        rejectLines=[], # deleted/replaced lines
       )


    parser.add_option("-D", "--output-dir", action="callback", callback=o_callback, type="string", help="Where to write the outputs; default is current directory.")

    parser.add_option("-O", "--one-file", action="store_true", dest="singleFile", help="Put all extracted splices in outDir/inputFile.splices.")
    parser.add_option("-f", "--output-file", type="string", dest="outputFile", help="FILE : Override the output filename assumption.")
    parser.add_option("-l", "--language", action="callback", callback=l_callback, type="string", help="LANG : Where LANG is c,cxx,f90,f77,f77_31,python,java,sidl. Default cxx.")

    parser.add_option("-B", "--target-key", type="string", dest="sourceKey", help="sourceSpliceKey : The start word ([a-zA-Z0-9.] are permitted characters) of the block delimiters in the input to be extracted. The default sourceSpliceKey matches that of babel 1.0 splicer blocks.")
    parser.add_option("-F", "--from", type="string", dest="sourceKey", help="alias for -A.")
    parser.add_option("-A", "--source-key", type="string", dest="sourceKey", help="alias for -B.")

    parser.add_option("-a","--after", type="int", dest="linesAfter", help="number: How many lines after each splice to extract with the splice.")
    parser.add_option("-b","--before", type="int", dest="linesBefore", help="number: How many lines before each splice to extract with the splice.")
    parser.add_option("-S", "--signatures", action="store_true", dest="signatures", help="Attempt to extract signatures with splices.")
    parser.add_option("-M", "--method", action="store_true", dest="method", help="Attempt to extract entire method with splices. Implies appropriate -S, -a.")
    parser.add_option("-C", "--comment", action="store_true", dest="methodcomment", help="Attempt to extract comment block method with splices if -M or -S.")
    parser.add_option("-p", "--block-file-prefix", type="string", dest="blockFilePrefix", help="blockFilePrefix : Block files to be inserted must match the pattern $blockFilePrefix$babel.impl.blockName$blockFileSuffix.")
    parser.add_option("-s", "--block-file-suffix", type="string", dest="blockFileSuffix", help="blockFileSuffix : as -p, but the suffix on input files.")
    parser.add_option("-V", "--vpath", type="string", dest="vpathDir", help="srcDir : Directory other than . to find implFile in.")
    parser.add_option("-m", "--match", action="callback", type="string", callback=m_callback, help="symbol : Extract all symbols containing symbol. Multiple use ok.")
    parser.add_option("-K","--keep-lines", action="callback", callback=K_callback, help="Keep line directives found in input in extracted files.")
    parser.add_option("-G","--gen-lines", action="callback", callback=G_callback, help="Create line directives indicating origin of splice.  gen-lines and keep-lines are mutually exclusive. Last seen wins.")
    parser.add_option("-d", "--debug", action="store_true", dest="dbg", help="print debug output")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="print process narration")
    parser.add_option("-Y", "--dryrun", action="callback", callback=Y_callback, help="List what would be done, but don't do it.")
    parser.add_option("-X", "--fatal", action="store_true", dest="fatal", help="Treat warnings as errors.")


    options, args = parser.parse_args(args)
    if options.language == "unset":
        setLangDefaults(parser.values, "cxx")
    return (options, args)
        
#------------------------------------------------
def validateOpts(opts):
    language = opts.language
    if not language in [ "C", "c" , "ucxx", "ocxx" , "cxx", "c++" , "uc++" , "CC", "f90", "f77" , "f77_31" ,  "java" , "python", "sidl", "sh", "csh", "tcsh", "bash", "xml"]:
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
    return True;

#------------------------------------------------

def printopts(opt):
    print "outputDir= " , opt.outputDir
    print "outputFile= " , opt.outputFile
    print "language= " , opt.language
    print "inputFile= " , opt.inputFile
    print "sourceKey= " , opt.sourceKey
    print "killKeys= " , opt.killKeys
    print "insertFirst= " , opt.insertFirst
    print "blockFilePrefix= " , opt.blockFilePrefix
    print "blockFileSuffix= " , opt.blockFileSuffix
    print "indent= " , opt.indent
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
    print "extract= " , opt.extract
    print "linesBefore= " , opt.linesBefore
    print "linesAfter= " , opt.linesAfter
    print "signatures= " , opt.signatures
    print "method= " , opt.method
    print "methodcomment= " , opt.methodcomment
    print "singleFile= " , opt.singleFile
    print "rejectSave= " , opt.rejectSave
    print "keepLines= " , opt.keepLines
    print "genLines= " , opt.genLines
    print "inputDirs= " , opt.inputDirs
    print "matchSyms= " , opt.matchSyms
    print "spliceHeader= " , opt.spliceHeader
    print "commonSuppressions= " , opt.commonSuppressions
    print "vpathDir= " , opt.vpathDir
    print "robMode = " , opt.robMode 
    print "spliceFiles= " , opt.spliceFiles
    print "rejectLines= " , opt.rejectLines

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

