import imp, sys, os
import cct._debug
from graph.boccagraph import *


class Help(BVertex):
    '''
Usage: bocca [options] <verb> <subject> [subject options] [subject args]

Options:

    --project PROJECTNAME
    -p PROJECTNAME
        Give the project to which the verb will be applied.
        The project must already exist in the local directory.
        Normally there is only one project per directory and -p may be omitted.

    --version, -V      Print the version numbers and exit.
    --debug, -d        Turn on debugging prints.    
    --help, -h         Print this message and exit.

    The "help" verb dispatches into the help subsystem, e.g., "bocca help create project".
'''
    def __init__(self, action = None, args = None, project = None, modulePath = None,
                 symbol=None, version='0.0', graph=None):
        """
        bocca help <subject>    lists the help on a subject
        bocca help              lists the available subjects
        """
            
        (file,filename,description) = imp.find_module('cct',[modulePath])
        mod = imp.load_module('cct', file, filename, description)
        self.menu = getattr(mod, 'menu')
        self.action_menu = getattr(mod, 'action_menu')

        if action == 'usage':
            exit(self.usage())
        
        if action not in self.action_menu:
            err(self.usage("unrecognized verb: " + action))

        BVertex.__init__(self,action,args,project,modulePath,'help',symbol,version,graph)
        pass
    
    def defineArgs(self, action):
        return 

    def processArgs(self, action):
        self.symbol = 'help'  # dummy symbol since this is never going to be added to graph
        return 
    
    def create(self):
        print BVertex.create.__doc__

    def change(self):
        print BVertex.change.__doc__
        
    def remove(self):
        print BVertex.remove.__doc__

    def rename(self):
        print BVertex.rename.__doc__

    def edit(self):
        print BVertex.edit.__doc__

    def config(self):
        print BVertex.config.__doc__
        
    def update(self):
        print BVertex.update.__doc__
                                  
    def display(self):
        """
        bocca help <verb> <subject> lists the help on a verb and a subject
        bocca help <subject>        lists the help on a subject
        bocca help                  lists the available subjects
        """
        print >> DEBUGSTREAM, '[help] display() args = ' + str(self.args)
        l = len(self.args)
        if l < 1:
            print self.usage()
            return 0
        
        print >> DEBUGSTREAM, '[help] display() args = ' + str(self.args)
        
        self.menu.append('sidlclass')   # equivalend to 'class'
        if l < 1 or l > 2 or (l == 1 and self.args[0] not in self.menu and self.args[0] not in self.action_menu):
            err(self.usage("help requested for unknown subject or verb:  " + self.args[0]),1)
                
        cctModPath = os.path.join(self.modulePath, 'cct')
        sys.path.append(cctModPath)
        
        if l == 1:
            if self.args[0] in self.menu: 
                subject = self.args[0]
                if subject == 'class': subject = 'sidlclass'
                verb = '__init__'
            elif self.args[0] in self.action_menu:
                subject = 'BVertex'
                verb = self.args[0]
        else:
            subject = self.args[1]
            verb = self.args[0]
            
        print >> DEBUGSTREAM, '[help] verb: ', verb
        print >> DEBUGSTREAM, '[help] subject: ', subject
        
        if (subject in self.menu or subject == 'BVertex'):
            if (verb == '__init__' or verb in self.action_menu):
                cmdClassName = subject.capitalize()
                if subject != 'BVertex':
                    try:
                        (f,p,d) = imp.find_module(subject)
                        m = imp.load_module(subject,f,p,d)
                    except ImportError:
                        err('Cannot find code for \"' + subject + "\" in " + cctModPath)
                    try:
                        cmdClass = getattr(m, cmdClassName)
                    except AttributeError:
                        err('Cannot find code for \"' + subject + "\" in " + cctModPath)
                    cmdInstance = cmdClass(symbol='temp',action=verb)
                else:
                    cmdInstance = BVertex(symbol='temp',action=verb)
                cmdInstance.usage(exitcode=0)
            else:
                print self.usage('Bocca Error: help requested for unknown verb: ' + subject)
                return 1
        else:
            if subject in self.action_menu:
                print self.usage('Bocca Error: ' + subject + ' is a <verb>, not a <subject> (order matters).')
                return 1
            else:
                print self.usage('Bocca Error: help requested for unknown subject or verb: ' + subject)
                return 1
        return 0
    
    def usage(self, errmsg=''):
        msg = errmsg + self.__doc__ 
        msg += "\nThe known verbs are:\n" 
        for i in self.action_menu: msg += '\t' + i + '\n'
        msg += "\nThe known subjects are:    \n"
        for i in self.menu: msg += '\t' + i + '\n'
        msg += '\nTry "bocca help", "bocca help <subject>", or "bocca help <verb> <subject>" for detailed usage.'
        msg += '\nFor a list of top-level bocca options, use "bocca --help"'
        msg += '\nFor a compact list of all verbs and subjects, use "bocca help --keywords"'
        msg += '\nFor examples beyond the help info, use "bocca help --examples [action] [subject]"'
        return msg

