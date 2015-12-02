# by   Boyana Norris, Argonne National Laboratory, Mar. 2007.

'''Dispatcher for Bocca cct modules corresponding to command subjects.
This module is never invoked directly, the bocca script calls it after 
doing some validation and module path settings.
'''
import signal 
import sys, os
def signal_handler(signal, frame):
    print >>sys.stderr, 'Bocca ERROR: user interrupt'
    if 'BOCCA_DEBUG' in os.environ.keys() and os.environ['BOCCA_DEBUG'] == '1': 
        import traceback
        traceback.print_stack()
    try:
        fm = BFileManager()
        fm.undo()   # Restore files to original state (created files deleted, modified files restored from backups
        fm.close()  # Just in case
    except:
        pass
    sys.exit(1)
        
signal.signal(signal.SIGINT, signal_handler)

import imp, re
from cct._util import *
from cct._examples import exdispatchArgv
from cct.project import Project
    
def dispatch(argv,projectName,modulePath,boccaprog):
    ''' The bocca dispatcher. It takes the command line options, which are of the 
    form "action object options", where "action" is one of create/remove/change/rename (etc), and 
    "object" is what the action is applied to, e.g., project, interface, class, port, 
    component, library. The "options" are passed unchanged to the subject being dispatched to.
    '''
    
    sys.path.append(modulePath)
    cctModulePath = os.path.join(modulePath,'cct')
    sys.path.append(cctModulePath)
    
    import cct._modulePath
    cct._modulePath.setModulePath(modulePath)

    from _debug import DEBUGSTREAM
    
    verb = 'display'
    subject = 'help'
    helponly = True
    canWorkOutsideProject = True
    l = len(argv)
    if l < 1: verb = 'usage'
    if 'version' in argv:
        try:
            import boccaversion
        except:
            error('Could not import boccaversion module')
            sys.exit(1)
        print >> sys.stderr, boccaversion.__version__
        sys.exit(0)
        
    if l == 1 and argv[0] in ['display','update']: subject = 'project'  # just to be nice
    else: verb = 'usage'
    args = []
    
    # Get lists of known verbs and subjects
    (file,filename,description) = imp.find_module('cct',[modulePath])
    mod = imp.load_module('cct', file, filename, description)
    menu = getattr(mod, 'menu')
    action_menu = getattr(mod, 'action_menu')
    menu_aliases = getattr(mod, 'menu_aliases')

    helponly, args, verb, subject = processHelpArgs(argv, args, subject, verb, menu, action_menu, helponly)

    subject = subject.strip()

    theproject = None
    graph = None
    vertex = None
    
    # Do some nice conversions to make the command-line more user-friendly
    subject = canonicalizeSubject(subject)

    if verb not in ['usage','help']:
        graph, theproject = loadProject(projectName,theproject, modulePath, action=verb)
        if theproject: 
            if not os.path.exists(theproject.modulePath):
                theproject.modulePath = modulePath
            projectName = theproject.symbol
            print >>DEBUGSTREAM, "dispatcher loaded project " + projectName 

    if l >1 and theproject and argv[0] in ['display','config','update','edit']:
        if [a for a in argv[1:] if a.startswith('-')] == argv[1:]:
            if not helponly: subject = 'project'
            else:
                verb = 'display' 
                subject = 'help'
                args.append('project')
                
    # Check whether action exists and pass the ball to help
    # Show some meaningful help when invalid verb or subject are given
    if verb != 'usage' and verb not in action_menu:
        print >>DEBUGSTREAM, "verb not usage or in known actions:", verb
        # Check a few aliases for verbs before giving up
        if verb == 'add':
            verb = 'create'
            print >>DEBUGSTREAM, "found create alias add"
        elif verb == 'delete':
            print >>DEBUGSTREAM, "found remove alias delete"
            verb = 'remove'
        else:
            # Check for unique completions
            matches = []
            for a in action_menu:
                if a.startswith(verb): matches.append(a)
            if len(matches) == 1:
                verb = matches[0]
                print >>DEBUGSTREAM, "found fuzzy match to verb ", verb
            elif not helponly:
                # Give up
                print >>DEBUGSTREAM, "failed verb search", "assuming display help"
                args = [verb]
                verb = 'display'
                subject = 'help'
                helponly = True

        
    # TODO: this is just temporary, eventually config will be supported by subjects other than project, too
    if verb in ['config','update'] and not subject.strip(): subject = 'project'
        
    # If user specified a version, we need it to look up the symbol
    version = None
    if verb != 'change':
        for arg in argv:
            if arg.startswith('--version') or arg.startswith('-v'):
                if arg.count('=') > 0:
                    version=arg.split('=')[-1].strip()
                else:
                    ind = argv.index(arg)+1
                    if ind < len(argv):
                        version = argv[ind]

    print >> DEBUGSTREAM, 'verb = ' + verb + ', subject = ' + subject + ', args = ' + str(args)
    
    if verb == 'display' and subject in ['interfaces','ports','classes','sidlclasses','components','enums']:
        if subject.endswith('classes'): subject = 'sidlclass'
        else: subject = subject[:-1]
        
    elif not helponly and subject not in menu and subject not in menu_aliases:
        # First, try to be smart and bring up an existing vertex of whatever kind
        # without requiring the subject to be explicitly specified
        # If the subject was not in the menu, assume it's a (partial) SIDL Symbol and 
        # look for it in the existing project.
        print >> DEBUGSTREAM, 'trying fuzzy match of', subject, "in symbols (version =", version, ")"

        if theproject:
            if graph != None and vertex is None and verb != 'create':
                sym = subject
                vlist = graph.findSymbol(sym, kind='any', version=version)
                if len(vlist) == 0:
                    # Try with the last argument
                    sym = argv[-1]
                    vlist = graph.findSymbol(sym, kind='any', version=version)
                    if len(vlist) == 0 and verb in ['edit', 'whereis'] and len(argv) >= 2:
                        # check for the args begin 'symbol method'
                        sym = argv[-2]
                        vlist = graph.findSymbol(sym, kind='any', version=version)
                if len(vlist) == 1: 
                    vertex = vlist[0]
                    argv.remove(sym)
                    subject = vertex.kind
                    args = [vertex.symbol] + argv[1:]
                elif len(vlist) > 1:
                    msg = 'Multiple matches for symbol ' + subject + ':\n'
                    i = 1
                    for v in vlist:
                        msg += '\t' + str(i) + ': ' + v.prettystr() + '\n'
                        i += 1
                    err(msg)
                    
                if not vertex and subject != 'project':
                    # Could not figure out the vertex kind, display help
                    args = [subject]
                    verb = 'display'
                    subject = 'help'
                    helponly = True

    subject = canonicalizeSubject(subject)
    
    if theproject: print >> DEBUGSTREAM, 'dispatcher: project:', projectName, ', symbol=', str(theproject.symbol)
    print >> DEBUGSTREAM, 'verb: ', verb, ', subject: ', subject, ', args=', args, ',helponly=', helponly
    if helponly and subject != 'help': args.append('--help')

    # Dispatch to the relevant command
    if len(subject) > 0:
        # The convention for subjects is that they are implemented in 
        # a file subcmd.py using a class Subcmd (same as the module name, but capitalized).
        subcmdModuleName = subject.strip()
        subcmdClassName = subcmdModuleName.capitalize()

        try:
            (file,filename,description) = imp.find_module(subcmdModuleName,[cctModulePath])
            mod = imp.load_module(subcmdModuleName, file, filename, description)
        except ImportError:
            print >>DEBUGSTREAM, 'Cannot find code for "' + subcmdModuleName + '" in ' + cctModulePath
            error('the specified subject "' + subcmdModuleName + '" is not supported by Bocca.')
    
        subcmdClass = None
        try:
            subcmdClass = getattr(mod,subcmdClassName)
        except AttributeError:
            error('Cannot find code for class "' + subcmdClassName + '" in ' + cctModulePath)

        # The dispatcher always creates an instance of the subcmdClass (i.e., specific BVertex subclass).
        # Once instantiated successfully, the dispatcher then checks for a vertex of the specified 
        # type and SIDL symbol in the graph. If such a vertex is successfully found, the method
        # specified in "verb" is executed on the existing vertex, and the new vertex is simply 
        # abandoned to the garbage collector. If the project or graph is not available or 
        # the vertex cannot be found, the method specified by "verb" is invoked on the newly
        # instance.
        subcmdInst = None
        symbol, kind = None, None
       
        if subcmdClass is not None:
            if helponly or (subject != 'project' and theproject) or (theproject is None and subject == 'project' and verb == 'create'):
                if subject == 'project' and helponly and theproject and theproject.symbol not in args:
                    args.append(theproject.symbol)
                subcmdInst = subcmdClass(action=verb,args=args,project=theproject,modulePath=modulePath,version=version)
                if subcmdInst is None:
                    fileManager.undo()
                    fileManager.close()
                    error('[displatcher] could not create an instance of ' + subcmdClassName)
                symbol = subcmdInst.symbol
                kind = subcmdInst.kind
                if version is None: version = subcmdInst.version
            elif theproject is not None and subject=='project':
                # Work with loaded project
                theproject.setup(verb,args)
                vertex = theproject
            else:
                if not helponly:
                    error('cannot instantiate class "' + subcmdClassName + '" or load existing project. Make sure you are in a valid BOCCA project directory.')
        else:
            error('cannot instantiate class "' + subcmdClassName + '"')
 
        if theproject is not None: 
            fileManager.setProjectName(theproject.symbol)
            fileManager.setProjectDir(theproject.getDir())

        # Check to see if vertex is already in graph and if found, invoke verb on existing instance
        vlist=[]
        if graph != None and vertex is None and verb != 'create':
            vlist = graph.findSymbol(symbol, kind, version)
            if len(vlist) != 1: vertex = None
            else: vertex = vlist[0]
        if vertex is None:
            try:
                subcmdMethod = getattr(subcmdInst,verb)
            except:
                error('the specified subject (' + subject + ') does not support the requested action: ' + verb)
                sys.exit(1)
            vertex = subcmdInst
            print >>DEBUGSTREAM, 'dispatcher: created new vertex: ' + vertex.symbol + ', version', vertex.version
        else: 
            # Make sure that the unpickled vertex is set up properly with the current
            # command-line options and arguments (those are not pickled).
            saveSymbol = vertex.symbol
            # Note that handleArgs invokes the BVertex methods defineArgs, and processArgs
            vertex.modulePath = modulePath
            if theproject is not None and vertex.kind != 'project': 
                vertex.project = theproject
                vertex.handleArgs(args, action=verb)
                vertex.symbol = saveSymbol # prevent accidental (or intentional) overwrites of the SIDL symbol 
            if not vertex.project: vertex.project = theproject
            print >>DEBUGSTREAM, 'dispatcher: vertex.symbol after handleArgs ' + str(vertex.symbol)
            subcmdMethod = getattr(vertex,verb)
            

        print >>DEBUGSTREAM, 'dispatcher: about to execute "' + subject + '.' + verb  + '()" on symbol=' + vertex.symbol + ' with args ' + str(args)
        interrupted = False
        try:
            result = subcmdMethod()   # Run the method on the subject, return value is 0 upon success, non-zero otherwise
        except KeyboardInterrupt,e:
            # Handle interrupts gracefully (as opposed to croaking with a stack trace)
            interrupted = True
            
        if not interrupted and verb !='display':
            # Save defaults (some commands modify them, display never does)
            if vertex.project is not None:
                print >>DEBUGSTREAM, 'dispatcher: saving project defaults in ' + vertex.project.getAttr('defaultsFile')
                theproject.saveDefaults()
            
            # Note fileManager.undo() has been moved to the err() method in _err.py
            try:
                fileManager.close()     # close all files and clean backups if needed
            except IOError,e:
                error('failed to close files and/or clean up backups: ' + str(e))
                result = 1


        sys.exit(result) # This should never be reached if there was an error


def error(msg=''):
    print >> sys.stderr, 'Bocca ERROR: ' + msg
    sys.exit(1)

def loadProject(projectName, theproject, modulePath=None, action='__init__'):
    if theproject: return theproject.getGraph(), theproject
    # Get project name and dir from .bocca dir (if any)
    if not projectName:
        theproject, graph = Globals().getProjectAndGraph(modulePath=modulePath, action=action)
        if theproject: theproject.loadDefaults()
    elif validSubdir(projectName, os.getcwd()):
        theproject, graph = Globals().getProjectAndGraph(projectName, action=action)
        if theproject: theproject.loadDefaults()
    else:
        print >>DEBUGSTREAM, "dispatcher could not validate project directory and did not load project"
        return None, None
    return graph, theproject

def canonicalizeSubject(s):
    '''Given a subject, return a a cannonical name for that subject.'''
    if s == 'class': return 'sidlclass'
    else: return s
    
def processHelpArgs(argv, args, subject, verb, menu, action_menu, helponly):
    l = len(argv)

    # Try to provide help with different combinations of arguments
    if 'help' in argv or '-h' in argv or '--help' in argv:
        # Begin internal option (Issue29)
        if l == 2 and argv[0] == 'help' and argv[1] == '--keywords':
            buf = 'Bocca verbs:'
            for i in action_menu:
                buf += ' ' + i
            
            buf += '\nBocca subjects:'
            for i in menu:
                buf += ' ' + i
            
            print buf
            sys.exit(0)
        # End internal option
        
        if l >= 2 and argv[0] == 'help' and argv[1] == '--examples':
            sys.exit(exdispatchArgv(argv))
        # End internal option
        # Remove multiple 'help's
        
        tmpargv = []
        for a in argv:
            if a != 'help' and a != '-h' and a != '--help':
                tmpargv.append(a)
            
        
        if len(tmpargv) == 1:
            if tmpargv[0] in menu:
                # Get help on a subject
                subject = 'help'
                verb = 'display'
                args += tmpargv
            elif tmpargv[0] in action_menu:
                verb = tmpargv[0]
                if len(tmpargv) > 1:
                    args += tmpargv[1:]
                
                if verb in ['config','update']:
                    subject = 'project'
                
            else:
                args += tmpargv
        elif len(tmpargv) >= 2:
            verb = tmpargv[0]
            subject = tmpargv[1]
            args = ['--help']
        #subject = 'help'
        #verb = 'display'
        #args += tmpargv
        # End of help command handling
        
        
    # Handling for non-help commands
    else:
        helponly = False
        verb = argv[0]
        args = []
        if l > 1:
            if not argv[1].startswith('-'):
                subject = argv[1]
                if l > 2:
                    args = argv[2:]
                
            # If no subject given, automatically pick one for verbs that
            # can support a default subject, e.g., config (project).
            elif verb in ['config','update']:
                subject = 'project'
                args = argv[1:]
            
            else:
                args = argv[1:]
                
    return helponly, args, verb, subject

