""" Various utilities that don't fit elsewhere
"""
import os, stat, shutil, re

from cct._debug import *
from cct._err import *

#---------------------------------------------------------------------------
# Global singleton variables:

# File manager (singleton) -- use this to open all files to make actions undoable
from cct._file import BFileManager
fileManager = BFileManager()

#----- end global singleton variables:

def Globals():
    '''Helper function to ensure exactly one instance of the Globals_singleton class exists'''
    myglobals = None
    try:
        myglobals = Globals_Singleton()
    except Globals_Singleton, s:
        myglobals = s
    return myglobals

class Globals_Singleton:
    '''A singleton class in which to stash various useful global variables for bocca.
    Do not instantiate this class directly, rather use the Globals helper function,
    e.g., myglobals = Globals().
    '''
    __single = None  # Used for ensuring singleton instance
    def __init__(self):
        if Globals_Singleton.__single:
            raise Globals_Singleton.__single 
        Globals_Singleton.__single = self
        self.projects = {}  # A dictionary with key = projectName, val = project
        self.graphs = {} # A dictionary of loaded graphs
        self.cca_vars = {} # a dictionary with key = projectName, val - CCA_SPEC_BABEL_CONFIG vars
        self.dirsToAvoid = ['CVS', '.svn', 'autom4te.cache', 'trash']
        self.action = '__init__'
        self.known_packages = ['sidl.','cca.']  # The packages Bocca recognizes by default
        pass
    
    def getProjectAndGraph(self, projectName = None, forceReload=False, modulePath=None, action='__init__'):
        '''Returns a 2-tuple (project,graph) with the cached project and 
        corresponding graph. If the graph hasn't been loaded yet, it is loaded
        and cached and the values returned.
        '''
        if projectName in self.projects.keys() and projectName in self.graphs.keys() and not forceReload:
            # Return cached versions
            return self.projects[projectName], self.graphs[projectName]
        if not projectName:
            projectName,mydir = getProjectInfo()
            print >>DEBUGSTREAM, 'In getProjectAndGraph after getProjectInfo: ', projectName, mydir
        # If the project is already loaded return it, otherwise load it
        if projectName not in self.projects.keys() or forceReload:
            proj, graph = getProject(projectName,modulePath=modulePath, action=action)
            if proj is not None: self.projects[projectName] = proj
            else: return None, None
            if graph is not None: self.graphs[projectName] = graph
            else: return None, None
        return self.projects[projectName], self.graphs[projectName]
    
    def renameProject(self, projectName, newProjectName):
        modulePath = None
        if newProjectName in self.projects.keys():
            err('cannot rename project to ' + newProjectName + ': project already exists')
        if projectName in self.projects.keys() and projectName in self.graphs.keys():
            modulePath = self.graphs[projectName].modulePath
            del self.projects[projectName]
            del self.graphs[projectName]
        return self.getProjectAndGraph(newProjectName, modulePath=modulePath, forceReload=True)
    
    def getProject(self, projectName=None):
        '''Same as getProjectAndGraph except returns just the project.'''
        if projectName in self.projects.keys():
            return self.projects[projectName]
        return self.getProjectAndGraph(projectName)[0]
    
    def getGraph(self, projectName=None):
        '''Same as getProjectAndGraph except returns just the graph.'''
        if projectName in self.graphs.keys():
            return self.graphs[projectName]
        return self.getProjectAndGraph(projectName)[1]
    
    def getDefaults(self, projectName=None, forceReload=False):
        '''Returns the ConfigurationParser instance containing project defaults settings.'''
        
        project, graph = self.getProjectAndGraph(projectName)
        if project is None or projectName not in self.projects.keys():
            return None
        mydir = project.getDir()
        
        if not forceReload:
            # Return cached version
            return self.projects[projectName].getDefaults()
        
        # Reload the defaults file
        return self.projects[projectName].loadDefaults()
        
    def saveState(self, projectName=None):
        r = 0
        if projectName is not None:
            if projectName in self.projects.keys():
                return self.graphs[projectName].save()
        else:
            for g in self.graphs:
                r = g.save()
                if r != 0: return r
        return r
    
    def getKnownPackages(self, projectName=None, forceReload=False):
        if projectName in self.cca_vars.keys() and not forceReload:
            return self.known_packages
        project,graph = Globals().getProjectAndGraph(projectName)
        defaults = project.getDefaults()
        val = defaults.get('Bocca','known_packages')
        if val: self.known_packages = val.split(',')
        return self.known_packages

    def getCCAVars(self, projectName='', forceReload=False):
        if projectName in self.cca_vars.keys() and not forceReload:
            return self.cca_vars[projectName]
        
        project,graph = Globals().getProjectAndGraph(projectName)
        defaults = project.getDefaults()
        
        #print >>DEBUGSTREAM, '[_util Globals.getCCAVars] loaded defaults:' + str(defaults)
        defaults.write(DEBUGSTREAM)

        babel_config_bin = defaults.get('Babel', 'babel_config')
        if babel_config_bin.count('"') == 2: 
            babel_config_bin = babel_config_bin[babel_config_bin.find('"')+1:babel_config_bin.rfind('"')]
        print >>DEBUGSTREAM, '[_util Global.getCCAVars] babel_config_bin =', babel_config_bin

        cca_spec_bin = defaults.get('CCA', 'cca_spec_babel_config')
        if cca_spec_bin.count('"') == 2: 
            cca_spec_bin = cca_spec_bin[cca_spec_bin.find('"')+1:cca_spec_bin.rfind('"')]
        print >>DEBUGSTREAM, '[_util Global.getCCAVars] cca_spec_bin =', cca_spec_bin

        for config in [babel_config_bin, cca_spec_bin]:
            if os.path.exists(config):
                mode = os.stat(config)[stat.ST_MODE] 
                if os.path.isfile(config):
                    if not bool(mode & stat.S_IEXEC):
                        err('[_util: getCCAVars]: could not load settings from ' + config + ' (file not found or not executable).')
                else:
                    err('[_util: getCCAVars]: could not load settings from ' + config + ' (not a file).')
            else:
                err('[_util: getCCAVars]: could not load settings from ' + config + ' (file not found).')
        
        myvars={}
        f= os.popen(cca_spec_bin+' --dump')

        l = f.readline()
        while (l != ''):
            tokens = l.replace('\'', '').replace('"', '').strip().split('=', 1)
            if (len(tokens) == 2):
                myvars[tokens[0]] = tokens[1]
            elif (len(tokens) ==1):
                myvars[tokens[0]] = ''
            l = f.readline()
        f.close()
        
        # Add the cca.sidl file to the cca myvars (strangely enough, it's not available directly with cca-spec-babel-config
        myvars['CCA_sidl'] = os.path.join(myvars['CCASPEC_pkgdatadir'],'cca.sidl')

        # Add the version babel-config returns; for nightlies, this happens to be a date, and it's 
        # used in library names (fun!)
        f = os.popen(babel_config_bin + ' --version')
        if f: 
            myvars['babel_config_version'] = f.read().strip()
        else: 
            err('[_util: getCCAVars]: could not get version info by invoking ' + babel_config_bin + ' --version.')
        f.close()
        
        self.cca_vars[projectName] = myvars
        return myvars
        
    def getDirsToAvoid(self):
        return self.dirsToAvoid
    
    def setDirsToAvoid(self,dirs):
        self.dirsToAvoid = dirs
        return self.dirsToAvoid

#---------------------- end class Globals_Singleton ------------------

#---------------------------------------------------------------------
#  Various helpful methods:

def deserializeASCII(thestring):
    '''A deserialization method for basic objects 
    (not as general or efficient as pickle, but portable).
    Returns a dictionary of objects of the appropriate types.
    
    @param thestring: a string containing a list, a dictionary, a number, or a string
    '''
    import re
    s = cleanString(thestring)
    if not s: return ''
    
    # Lists
    if s.startswith('[') and s.endswith(']'):
        newlist = eval(s)
        if not newlist: return []
        else: return newlist 
        
    # Tuples
    if s.startswith('(') and s.endswith(')'):
        newtuple = eval(s)
        if not newtuple: return ()
        else: return newtuple
    
    # Dictionaries
    if s.startswith('{') and s.endswith('}'):
        newdict = eval(s)
        if not newdict: return {}
        else: return newdict 
        
    # Numbers
    intpattern = re.compile(r'[+-]?\d+')
    m = intpattern.match(s)
    if m: 
        (start, end) = m.span()
        if start == 0 and end == len(s):
            return int(s)
        
    # Bocca doesn't work with floats, but if at some point it does, make sure that version strings don't get converted to floats

    # Strings for everything else
    return cleanString(s)

def cleanString(s):
    newstr = s
    if s.__class__ == str:
        newstr = s.strip().strip("'").strip('"')
    return newstr

def findClosingElement(s, openchar='{', closechar='}'):
    newstr = s.strip()
    if s.startswith(openchar):
        rbindex = newstr.find(closechar)
        numnests = newstr[1:rbindex].count(openchar)
        n = 0
        curpos = rbindex +1
        while n < numnests:
            oldpos = curpos
            rbindex = newstr[curpos:].find(closechar)
            curpos += rbindex 
            n += 1
            numnests += newstr[oldpos:curpos+rbindex].count(openchar)
            #print 'numnests = ' + str(numnests), ', rbindex = ' + str(rbindex) + ', ' + newstr[:curpos+1]
 
        return curpos+1
    return -1
              
#-------------------------------------------------------------------------------
def ngrep(file, pattern):
    """
    Provide line numbers for matches in a file.
    The first argument is a file.
    The second is a regular expression.
    
    Usage
    -----
    Please see the regular expression syntax for the re module located here:
    http://docs.python.org/lib/re-syntax.html
    
    matches = grep("/home/joe", "stuff")

    => [1]
    
    @param filename
    @type string
    @param pattern: A pattern to match
    @type pattern: str
    @return: A list of line numbers. empty if there was any problem with the inputs or no match found.
    """
    matches = []
    import re
    
    if not os.path.exists(file): return matches
    
    try:
        f = open(file, "r")
    except:
        print "no open file -> []"
        return matches

    x = re.compile(pattern)
    i = 0
    for line in f:
        i += 1
        m = x.match(line)
        if m:
            matches.append( (i, line) )
    
    f.close()
    return matches

def getEditor():
    """ checks for:
env(BOCCA_EDITOR)
env(EDITOR)
# project default editor setting -- not implemented
vi
emacs
and then returns it if valid or None if a problem occurs.
"""
    args = []
    try:
      edit = os.environ["BOCCA_EDITOR"]
    except:
      try:
        edit = os.environ["EDITOR"]
      except:
        edit = "vi"
    args = edit.split()
    editor= args[0]
    return (editor, args)

def getEditorWaitFlag():
    """ We're not pychic, so if the user wants us not to wait (e.g. their
editor has an independent gui window), they can tell us not to with an
env var."""
    result=os.P_WAIT
    try: # if set, assume nowait
        dummy = os.environ["BOCCA_EDITOR_NOWAIT"]
        result = os.P_NOWAIT
    except:
        pass
 
    return result

def getSpliceBegins(filename, spliceName):
    """Always returns at least an empty list.
Find where splicename occurs in babel splicer tags in the file. 
Result may be nonunique. 
The result for the None splice name is a list containing 1.
"""
    x=[]
    if not filename:
        return x
    if not spliceName or len(spliceName) == 0:
        x.append(1)
        return x
    pattern= ".*DO-NOT-DELETE splicer.begin.*"+ spliceName + r"\).*"
    x=ngrep(filename,pattern)
    return x


def editFile(filename, printonly, spliceName):
    from cct._file import md5file
    
    changed = False
    if spliceName:
        starts = getSpliceBegins(filename, spliceName)
    if printonly:
        if spliceName:
            if len(starts) > 1:
                for i in starts:
                    print filename + ":" + str(i[0]) +":" + i[1] 
            else:
                print filename + ":" + str(starts[0][0])
        else:
            print filename 
        return changed
    else:
        print "Trying to edit file ", filename
    md5sum_before = md5file(filename)
    editor, userargs = getEditor()
    if editor == None:
        err("unable to find an editor for ", filename)
    if not filename or len(filename) <1:
        err("invalid filename: " + str(filename))
    if spliceName and len(starts) >0:
        offset = "+" + str(starts[0][0])
        userargs.append(offset)
    userargs.append(filename)
    wait=getEditorWaitFlag()
    
    # Create visible backup (the backup of the backup file is done automatically)
    if os.path.exists(filename+'.bak'):
        fileManager.rm(filename+'.bak')
    fileManager.copyfile(filename,filename+'.bak')
    
    os.spawnvp(wait, editor, userargs) # py 2.3 and later.
    md5sum_after = md5file(filename)
    if md5sum_before != md5sum_after:
        changed = True
    return changed
    
def getProject(projectName=None, modulePath=None, action='__init__'):
    '''Returns a 2-tuple, (CCAProject,BGraph) containing the Project
    vertex for the named project and the graph that contains it. If a name 
    is not specified, the project info in the current directory is 
    used. If multiple projects are found, an error is printed. 
    If this method is executed outside of a valid
    project directory, it returns None.
    '''
    from graph.boccagraph import BGraph

    pgraph = None
    project = None
    name,mydir = getProjectInfo(projectName)

    if not modulePath:
        import cct._modulePath
        modulePath = cct._modulePath.getModulePath()
    if not modulePath:
        print >> sys.stderr, '***Bocca ERROR: invalid module path, cannot load Bocca modules: ' + str(modulePath)
        if 'BOCCA_DEBUG' in os.environ.keys() and os.environ['BOCCA_DEBUG'] == '1': 
            import traceback
            traceback.print_stack()
    if mydir is not None:
        pgraph = BGraph(name=name,path=mydir, modulePath=modulePath)
        # Temporarily disabling the pickle while figuring out vertex save/load problems (using ascii in the meanwhile)
        #try:
        #    retcode = pgraph.load(modulePath=modulePath)   
        #except:
        #    retcode = 1
        #if retcode != 0:       
        #    warn('Loading from pickle failed, loading ASCII representation of project.')
        #    pgraph = BGraph(name=name,path=mydir, modulePath=modulePath)
        #    pgraph.loadASCII(modulePath=modulePath)
        
        pgraph.loadASCII(modulePath=modulePath, action=action)
              
        vlist = pgraph.findSymbol(name,kind='project')  # Project vertex 
        if not vlist:
            pgraph = BGraph(name=name,path=mydir, modulePath=modulePath)
            pgraph.loadASCII(modulePath=modulePath)
            vlist = pgraph.findSymbol(name,kind='project')  # Project vertex
        if vlist: project = vlist[0]
        else: 
            import traceback
            print >> sys.stderr, 'Bocca ERROR: could not load project.'
            if 'BOCCA_DEBUG' in os.environ.keys() and os.environ['BOCCA_DEBUG'] == '1': 
                traceback.print_stack()
            sys.exit(1)
        
        pgraph.project = project   # keep a reference in the graph for convenience (not pickled)
        project.setDir(pgraph.path)

        project.modulePath = pgraph.modulePath
       
    if project is not None:
        project.loadBuildTemplate()
        project.loadDefaults()
    return project,pgraph

def getProjectInfo(projectName=None, projectDir=None):
    '''Returns a 2-tuple containing the project name and directory when executed 
    within a valid project subdirectory or (None, None) if the directory (or current
    directory, when projectDir is None) is not a valid project directory or if 
    the project found does not match projectName (when projectName is not None).
    Exits with an error if projectName is None and multiple projects are found.
    '''
    currdir = ''
    if projectDir is None: currdir = str(os.getcwd())
    else: currdir = projectDir
    currdir=currdir.strip()
    name = projectName
    metadir = os.path.join(currdir,'BOCCA')
    if not os.path.exists(metadir): return None, None
    try:
        files = os.listdir(metadir)  
    except:
        return None,None

    count = 0
    for f in files:
        if f.startswith('Dir-'):
            name = re.sub(r'Dir-','',f)
            count = count + 1
            if projectName is None and count > 1:
                return err('Multiple projects found in this directory, a specific project name is required in order to load project information.')
            if projectName is not None and projectName != name:
                continue
            try:
                fin = open(os.path.join(currdir, 'BOCCA','Dir-' + name))
            except:
                return None,None
            relativePath = fin.readline()
            fin.close()
            relativePath = relativePath.strip()
            if relativePath != ".":
                mydir = currdir[:currdir.rfind(relativePath)]
            else:
                mydir = currdir
            return name,mydir
    return None,None
    
def addSubdir(projectName, relativePath):
    '''Add a subdirectory to a given project, creating metadata in .bocca.
        This can be invoked in any project subdirectory. Project is a 
        CCAProject instance.
    '''
    # Create hidden metadata directories (.bocca) whose contents would
    # normally *not* be under revision control
    project, graph = getProject(projectName)
    name, projectDir = project.getInfo()
    if name is not projectName: return 1
    
    dirToAdd = os.path.abspath(os.path.join(projectDir,relativePath))
    try:
        if not os.path.exists(dirToAdd): fileManager.mkdir(dirToAdd)
    except:
        return err('Could not create subdirectory ' + str(dirToAdd) + ' in project ' + projectName)
        
    addProjectMetadirs(projectName,dirToAdd,rootDir=projectDir)
    return 0
    
def validSubdir(projectName, relativePath):
    
    visibleMetadir = 'BOCCA'
    n, projectDir = getProjectInfo(projectName)
    #project, graph = getProject(projectName)
    if projectName is not None and n != projectName:
        warn('Invalid project name, cannot validate subdirectory.')
        return False
    
    projectName = n
    if projectName is None:
        return False
    
    if projectDir is None:
        warn('Cannot find project directory for project ' +  projectName + '.')
        return False
    
    # First get project path from top-level metadir
    topdirfile = os.path.join(projectDir,visibleMetadir,'Dir-'+projectName)
    if not os.path.exists(topdirfile):
        warn('Cannot validate top-level project directory, project metadata is missing or corrupted.')
        return False
    
    fin = open(topdirfile,"r")
    pDir = fin.readline().strip()  # get the project directory from the top-level BOCCA/Dir-ProjName file
    fin.close()
    if str(os.path.abspath(os.path.join(projectDir,pDir))) != str(os.path.abspath(projectDir)):
        warn('Cannot validate top-level project directory, project metadata is missing or corrupted.')
        return False
    
    # Check if the .bocca directory in relativePath contains a correct Dir-ProjName entry
    metadir = os.path.abspath(os.path.join(projectDir,relativePath))
    if metadir == projectDir: return True
    else: metadir = os.path.join(metadir,visibleMetadir)
    if not os.path.isdir(metadir):
        warn('Subdirectory ' + str(metadir) + ' doesn''t exist or is not a directory.')
        return False
    
    dirfile = os.path.join(metadir,'Dir-'+projectName)
    if not os.path.isfile(dirfile):
        warn('Project metafile ' + str(dirfile) + ' not found or is not a file.')
        return False
    
    # Check contents of dirfile
    fin = open(dirfile,"r")
    rdir = fin.readline().strip()
    fin.close()
    if not os.path.isdir(os.path.abspath(os.path.join(projectDir,rdir))):
        warn('Cannot validate project subdirectory ' + str(rdir) + ': inconsistent metadata.')
        return False
    
    return True

def addProjectMetadirs(projectName, topDir, rootDir):
    '''Create BOCCA metadata subdirectories in the project directory tree. 
    @param  projectName: Project name
    @param topDir: the top-most directory from which to descend when adding the metadirs
    @param rootDir: usually the top project directory'''
    os.path.walk(topDir,manageProjectMetadirsFunc,arg={'projectName':projectName,'rootDir':rootDir,'action':'add'})
    return
    
def removeProjectMetafiles(projectName, topDir, rootDir):
    os.path.walk(topDir,manageProjectMetadirsFunc,arg={'projectName':projectName,'rootDir':rootDir,'action':'rm'})
    return 

def manageProjectMetadirsFunc(arg,dirname,fnames):
    '''Visitor function to perform various file operations. Normally invoked by tree walkers,
    such as addProjectMetadirs and removeProjectMetafilles.
    '''
    dirsToAvoid = Globals().getDirsToAvoid()    
    dirs = dirname.split(os.path.sep)
    for d in dirsToAvoid:
        if d in dirs: return
    
    visibleMetadir=None
    hiddenMetadir=None
    action = arg['action']
    if action == 'add':
        if dirs[-1] == 'BOCCA' or dirs[-1] == '.bocca':
            return
        visibleMetadir = os.path.abspath(os.path.join(dirname,'BOCCA'))
        hiddenMetadir = os.path.abspath(os.path.join(dirname,'.bocca'))
    elif action == 'rm' or action == 'rmdir':
        if dirs[-1] == '.bocca': hiddenMetadir = dirname
        elif dirs[-1] == 'BOCCA': visibleMetadir = dirname
        else: return
 
    projName = arg['projectName']
    projDir = arg['rootDir']

    if dirname.startswith(projDir):
        relativePath = dirname.replace(projDir,'').lstrip(os.path.sep)
    else:
        relativePath = dirname

    if os.path.isabs(relativePath): 
        print 'Error: invalid relative path or absolute path outside project specified.'
        return
        
    if action == 'add':
        # Phasing out .bocca subdirectory -- will clean out completely in a later release (TODO)
        #try: fileManager.mkdir(hiddenMetadir)
        #except: print >> DEBUGSTREAM, ".bocca subdirectory found in " +  str(dirname) + " (that's ok)."
        try: fileManager.mkdir(visibleMetadir)
        except: print >> DEBUGSTREAM, "BOCCA subdirectory found in " + str(dirname) + " (that's ok)."
    elif action == 'rmdir':
        try: fileManager.rmdir(hiddenMetadir)
        except: print >> DEBUGSTREAM, "could not remove hidden metadir " + str(hiddenMetadir) + "(that's ok)."
        try: fileManager.rmdir(visibleMetadir)
        except: print >> DEBUGSTREAM, "could not remove visible metadir " + str(visibleMetadir) + "(that's ok)."
        return
        
    if relativePath.strip() is '': relativePath = '.'
    if visibleMetadir is not None:
        filename = os.path.join(visibleMetadir,'Dir-'+projName)
    else:
        return
    if action == 'add':
        try:
            fout = fileManager.open(filename, "w")
            fout.write(relativePath+'\n')
            fout.close()
        except IOError,e:
            err('could not create Bocca metafile ' + filename + ': ' + str(e))
    elif action == 'rm':
        try:
            fileManager.rm(filename, trash=False)
        except IOError,e:
            err('could not remove file ' + filename + ': ' + str(e))
    return
    
def mySplicer(source, destination, beginPat, endPat, mode='APPEND', arg=None):
    """ Splice blocks from source buffer to destination buffer. Blocks
        are matched based on the block beginning pattern (beginPat) and
        block termination pattern (endPat). 
        
        A none None value for arg restricts replacement to blocks bound by 
        beginPat(arg)
            
        endPat(arg)
        otherwise, all blocks matching any argument will be replaced.
    """
    
    s_begin = source.find(beginPat) # Example: bocca.protected.begin(
    d_text_begin = 0
    while (s_begin != -1):
        lpar = source.find('(', s_begin)
        rpar = source.find(')', lpar)
        splicerArg = source[lpar+1:rpar]
        s_text_begin = source.find('\n', rpar) +1
        endText = endPat.rstrip('(')+'(' + splicerArg + ')'
        s_end = source.find(endText, s_text_begin)
        s_text_end = source.rfind('\n', 0, s_end)
   
        beginText = beginPat.rstrip('(')+'(' + splicerArg +')'
        d_begin = destination.find(beginText, d_text_begin)
        d_text_begin = destination.find('\n', d_begin)+1
        d_end = destination.find(endText, d_begin)
        d_text_end = destination.rfind('\n', 0, d_end) 
   
        s_begin = source.find(beginPat, s_text_end)
        if (d_begin == -1):   # Target does not contain splicer block
            d_text_begin = 0
            continue
        
        if (arg != None and arg != splicerArg):
            continue
        
        if (mode == 'REPLACE')  :
            new_dest = destination[0:d_text_begin] + source[s_text_begin:s_text_end] + destination[d_text_end:]
        elif (mode == 'APPEND'):
            new_dest = destination[0:d_text_end] + source[s_text_begin:s_text_end] + destination[d_text_end:]
        elif (mode == 'PREPEND'):
            new_dest = destination[0:d_text_begin] + source[s_text_begin:s_text_end] + destination[d_text_begin:]
        elif (mode == 'DELETE'):
            new_dest = destination[0:d_text_begin] + destination[d_text_end:]
         
        destination = new_dest
      
    return destination

def isBoccaSource(filename, key):
    try:
        pattern=".*"+ key + ".*"
        x=ngrep(filename,pattern)
        if len(x) > 0:
            return True
        return False
    except:
        return False
 
# TODO: the methods below are not needed -- equivalent functionality is available in _validate.py
def lang_to_fileext(lang):
    if lang == "cxx" or  lang == "cxx_cio":
        return "cxx"
    elif lang == "java":
        return "java"
    elif lang == "c":
        return "c"
    elif lang == "f90":
        return "F90"
    elif lang == "f03":
        return "F03"
    elif lang == "f77":
        return "f"
    elif lang == "f77_31":
        return "f" ; # until babel gets fixed.
    else:
        return None
    return

def lang_to_headerext(lang):
    if lang == "cxx" or  lang == "cxx_cio":
        return "hxx"
    elif lang == "c":
        return "h"
    elif lang == "f90":
        return "F90"
    else:
        return None
    return

def getPythonVersion():
    import sys
    verstring = sys.version 
    if verstring:
        ver = verstring.split()[0]
        if ver.count('.') >= 2: return ver
        else: return ''
    else:
        return ''
    
def getHash(s):
    hash=''
    #Python version-dependent modules
    usehashlib=False
    pythonVersion = getPythonVersion()
    if pythonVersion:
        major,minor,patch=pythonVersion.split('.')
        if int(major) > 2 or int(minor) >= 5:
            usehashlib = True

    if usehashlib:
        from hashlib import md5
        hashed = md5()
    else:
        import md5
        hashed = md5.new()
        
    hashed.update(s)
    return str(hashed.hexdigest())
