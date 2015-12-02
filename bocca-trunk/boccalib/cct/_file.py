import os
# By default, Python deprecation warnings are disabled, define the CCA_TOOLS_DEBUG env. variable to enable
try:
    import warnings
    if not ('BOCCA_DEBUG' in os.environ.keys() and os.environ['BOCCA_DEBUG'] == '1'): 
        warnings.filterwarnings("ignore", category=DeprecationWarning)
except:
    pass


import sys, md5, shutil, traceback
from datetime import datetime
from time import strptime
from cct import menu

def BFileManager():
    ''' This helper method should be used for instantiating BFileManager_Singleton, 
    which is a singleton class that records file operations, making 
    them undoable. It must be used instead of the standard open method, e.g.,
    
    fileDescriptor = fileManager.open(name,'r+')
    
    Do not instantiate this class directly! Rather, use the helper 
    method BFileManager the same way you would call the constructor to 
    obtain the single instance, e.g.:
    
    fileManager = BFileManager()
    fileManager = BFileManager()
    
    would instantiate the BFileManager_Singleton exactly once.
    '''
    fm = None
    try:
        fm = BFileManager_Singleton()
    except BFileManager_Singleton, s:
        fm = s
    return fm

class BFileManager_Singleton:
    '''A singleton class that records file operations, making 
    them undoable. It must be used instead of the standard open method, e.g.,
    
    fileDescriptor = fileManager.open(name,'r+')
    
    Do not instantiate this class directly! Rather, use the helper 
    method BFileManager the same way you would call the constructor to 
    obtain the single instance, e.g.:
    
    fileManager = BFileManager()
    fileManager = BFileManager()
    
    would instantiate the BFileManager_Singleton exactly once.
    '''
    __single = None  # Used for ensuring singleton instance
    def __init__(self):
        if BFileManager_Singleton.__single:
            raise BFileManager_Singleton.__single 
        BFileManager_Singleton.__single = self
        self.fds = {}
        self.restore = []
        self.remove = []
        self.restore_dirs = []
        self.remove_dirs = []
        self.projectDir = None
        self.projectName = None
        pass
    
    def clear(self):
        self.fds.clear()
        self.restore = []
        self.remove = []
        self.remove_dirs = []
        self.restore_dirs = []
        self.updateProjectInfo()
        pass
    
    def setProjectName(self, name):
        self.projectName = name
        pass
    
    def setProjectDir(self, dir):
        self.projectDir = dir
        pass
        
    def open(self, name, mode, nobackup=False):
        '''Returns a file descriptor after opening the file.
        
        name : file name (full path)
        mode : file mode ('r', 'U', 'w', 'a', possibly with 'b' or '+' added)
        '''
        if name in self.fds.keys():
            if not self.fds[name][0].closed and self.fds[name][1] != mode: 
                self.fds[name][0].close()
            if self.fds[name][0].closed:
                try:
                    self.fds[name] = (open(name,mode), mode)
                except:
                    raise
            return self.fds[name][0]
        fd = None
        if name is None or name == '':
            self.err('BFileManager open: no filename given')
            raise IOError
        name = os.path.abspath(name)        
        self.updateProjectInfo()
        # Record the operation for use by undo and make any 
        # necessary backups.
        if not nobackup:
            if mode.count('w') + mode.count('a') + mode.count('+') > 0:
                # The file is being opened for writing, back it up if it already exists
                if os.path.exists(name) and os.path.isfile(name):
                    backup = self.getBackupName(name)
                    shutil.copyfile(name,backup)
                    self.restore.append(self.getRelativePath(name))
                else:
                    self.remove.append(self.getRelativePath(name))
        try:
            fd = open(name,mode)
        except:
            raise
        
        self.fds[name] = (fd,mode)
        return fd
        
    def close(self):
        '''Cleans up any backup files and closes the file'''
    
        for file in self.fds.keys():
            if not self.fds[file][0].closed: 
                try: self.fds[file][0].close()
                except: pass
        
        self.updateProjectInfo()
        
        # Clean up any backup files
        for f in self.restore + self.restore_dirs:
            backup = os.path.join(self.projectDir,self.getBackupName(f))
            if os.path.exists(backup): 
                if os.path.isfile(backup):
                    os.remove(backup)
                elif os.path.isdir(backup):
                    shutil.rmtree(backup,ignore_errors=True)
        return

    def rm(self, name, trash=True, nobackup=False):
        ''' Removes a file. 
        
        name : full path
        '''
        name = os.path.abspath(name)
        if not nobackup:
            self.updateProjectInfo()
            backup = self.getBackupName(name)
            try:
                shutil.copy2(name,backup)
            except IOError,e: 
                self.err('could not create backup of file ' + name +': ' + str(e)) 
            if trash: self.copyToTrash(name)
        try:
            if os.path.exists(name):
                os.remove(name)
        except IOError,e: 
            self.warn('could not remove file ' + name + ': ' + str(e))
        self.restore.append(self.getRelativePath(name))
        return
    
    def mkdir(self, path, noaction=False, nobackup=False):
        '''Create a directory.
        
        path : directory name (full path)
        '''
        path = os.path.abspath(path)
        if not noaction:
            try: os.mkdir(path)
            except: raise
        if not nobackup:
            self.updateProjectInfo()
            self.remove_dirs.append(self.getRelativePath(path))
        return
    
    def rmdir(self, path, trash=True, nobackup=False, info=False):
        '''Removes a directory, backing it up first so undo can be performed.
        
        path : directory name (full path)
        '''
        path = os.path.abspath(path)
        
        if trash: 
            self.copyToTrash(path, info)
        # Back up directory (for undo of local command in case of errors)
        if not nobackup:        
            self.updateProjectInfo()
            backup = self.getBackupName(path)
            try: os.rename(path,backup)
            except: self.err('could not back up directory: ' + path)
            self.restore_dirs.append(self.getRelativePath(path))
        if os.path.exists(path):
            try: shutil.rmtree(path)
            except: raise
        return
        
    def rename(self, path, newpath, trash=True, nobackup=False):
        ''' Rename a file or directory. 
        path : full path of original file/directory
        newpath : full path of new file/directory.
        '''
        path = os.path.abspath(path)
        if not os.path.exists(path):
            self.err('file/dir rename failed, invalid path encountered: ' + path)
        newpath = os.path.abspath(newpath)
        if os.path.exists(newpath):
            self.err('cannot rename, destination path already exists: ' + newpath)

        if not nobackup:
            self.updateProjectInfo()
            backup = self.getBackupName(path,fullpath=True)
            if os.path.isdir(path):
                try: 
                    shutil.copytree(path,backup)
                except IOError, e: 
                    self.err('rename could not backup directory ' + path + ': ' + str(e))
            else:
                try: shutil.copy2(path,backup)
                except IOError, e:
                    self.err('rename could not backup file ' + path + ': ' + str(e))
                if trash: self.copyToTrash(path)
        # do the rename
        try:
            os.rename(path,newpath)
        except:
            raise
        
        if not nobackup:
            if os.path.isdir(path):
                self.restore_dirs.append(self.getRelativePath(path))
                self.remove_dirs.append(self.getRelativePath(newpath))
            else:
                self.restore.append(self.getRelativePath(path))
                self.remove.append(self.getRelativePath(newpath))
        return
    
    def copyfile(self, path, newpath, nobackup=False):
        ''' Copy a file. 
        path : full path of original file
        newpath : full path of new file.
        '''
        path = os.path.abspath(path)
        if not os.path.exists(path):
            self.err('file copy failed, invalid path encountered: ' + path)
        newpath = os.path.abspath(newpath)
        if os.path.exists(newpath):
            self.err('cannot copy file, destination path already exists: ' + newpath)
        if not os.path.isfile(path):
            self.err("copy invoked on something that's not a file: " + path)
        dname = os.path.dirname(newpath)
        if not os.path.exists(dname):
            try: os.mkdir(dname)
            except: self.err("could not create directory: " + dname)
        if not nobackup: self.updateProjectInfo()

        c = os.path.commonprefix([path,newpath])
        if c.rstrip(os.path.sep) != self.projectDir:
            # Do not create backup of files outside the project, but add them to remove list
            if not nobackup: 
                self.remove.append(newpath)
                nobackup=True
        if not nobackup:
            backup = self.getBackupName(path)
            try: shutil.copy2(path,backup)
            except: 
                self.err('copy could not backup file: ' + path)
        try:
            shutil.copy2(path,newpath)
        except:
            raise
        if not nobackup:
            self.restore.append(self.getRelativePath(path))
        return    
    
    def undo(self):
        '''Undo all that was done since this file was opened. 
        If a file was created, it is removed. If a file 
        was opened as read-write or append, the backup for that
        file is restored.
        '''
        from cct._debug import DEBUGSTREAM
        print >>DEBUGSTREAM, 'BFileManager undo called. Removing the following files: ', self.remove, '. Restoring the following files: ', self.restore

        self.updateProjectInfo()
        # First, close any open files
        for file in self.fds.keys():
            if not self.fds[file][0].closed: self.fds[file][0].close()
            
        # Restore directories that were removed
        for d in self.restore_dirs:
            backup = self.getBackupName(d, fullpath=True)
            if os.path.exists(backup) and os.path.isdir(backup):
                try: os.rename(backup,os.path.join(self.projectDir,d))
                except: self.warn('could not restore back up copy of directory ' + d)
        
        # Restore any files and remove the backups 
        for f in self.restore:
            backup = self.getBackupName(f, fullpath=True)
            if os.path.exists(backup) and os.path.isfile(backup):
                shutil.copy2(backup,os.path.join(self.projectDir,f))
                os.remove(backup)
        
        # Remove newly created files
        for f in self.remove:
            fpath = os.path.join(self.projectDir,f)
            if os.path.exists(fpath):
                if os.path.isfile(fpath):
                    os.remove(fpath)
                else:
                    shutil.rmtree(fpath,ignore_errors=True)
        
        # Remove any created directories
        for d in self.remove_dirs:
            dpath = os.path.join(self.projectDir,d)
            if os.path.exists(dpath) and os.path.isdir(dpath):
                shutil.rmtree(dpath,ignore_errors=True)
        self.clear()
        return
    
    def writeStringToFile(self, filename, thestring):
        fd = self.open(filename,"w")
        fd.write(thestring)
        fd.close()
        # The fd will be closed at the end of the bocca command
        
    
#------------- Private methods
    def updateProjectInfo(self):
        from cct._util import Globals
        project = Globals().getProject(projectName=self.projectName)
        if project is not None: self.projectDir = project.getDir()
        pass
    
    def getBackupName(self,f, fullpath=True, prefix=None):
        '''Return the name of the backup file, using a relative path if fullpath is False,
        and the full path otherwise.'''
        if prefix == None: prefix = self.projectDir    
        if not f.startswith(os.path.sep): 
            # not a full path
            relpath = os.path.dirname(f)
        elif prefix != None and f.startswith(prefix): # fixme
            relpath = os.path.dirname(f).replace(prefix,'').lstrip(os.path.sep)
        else: relpath = ''

        fname = os.path.join(relpath,'.' + os.path.basename(f) + '.bocca.bak')
        if fullpath and prefix != None:  # fixme
            return os.path.join(prefix, fname)
        else:
            return fname
        
    def copyToTrash(self, f, info=False):
        '''Copy file f to the equivalent trash location.'''
        fname = os.path.basename(f)
        if self.projectDir is None:
            return 
        prefix = self.projectDir
        if not f.startswith(os.path.sep):
            # not a full path
            relpath = os.path.dirname(f)
        elif f.startswith(prefix):
            relpath = os.path.dirname(f).replace(prefix,'').lstrip(os.path.sep)
        else:
            return
        trashdir = os.path.join(prefix,'BOCCA','trash',relpath)
        if not os.path.exists(trashdir): os.makedirs(trashdir)
        trashname = os.path.join(trashdir, fname + '.' + str(datetime.now().isoformat()))
        
        if os.path.isdir(f):
            try: 
                shutil.copytree(f,trashname)
            except IOError, e: 
                self.err('could not backup directory to trash folder ' + f + ': ' + str(e))
            if info: print 'Bocca INFO: Removing directory %s (a backup is available in %s).' % (f,trashname)
        else:
            try: shutil.copy2(f,trashname)
            except IOError, e:
                self.err('could not backup file to trash folder ' + f + ': ' + str(e))
        return
        
    def getRelativePath(self, path, prefix=None):
        '''Return the relative path constructed by removing the prefix.'''
        if prefix == None: prefix = self.projectDir
        if prefix != None and path.startswith(prefix):
            relpath = path.replace(prefix,'').lstrip(os.path.sep)
        else: relpath = '' # fixme - is relpath of something with no project really empty string? -no, but we just don't back it up in that case
        return relpath

    def err(self, errmsg='',errcode=1):
        print >>sys.stderr, 'Bocca ERROR: ' + errmsg
        if 'BOCCA_DEBUG' in os.environ.keys() and os.environ['BOCCA_DEBUG'] == '1': 
            traceback.print_stack()
            self.undo()   # Restore files to original state (created files deleted, modified files restored from backups
            self.close()  # Just in case
            sys.exit(errcode)
            
    def warn(self, errmsg='',errcode=1):
        print >>sys.stderr, 'Bocca WARNING: ' + errmsg

"""
Re-implementation of md5sum in python
"""
def md5file(filename):
    """Return the hex digest of a file without loading it all into memory"""
    fh = open(filename)
    digest = md5.new()
    while 1:
        buf = fh.read(4096)
        if buf == "":
            break
        digest.update(buf)
    fh.close()
    return digest.hexdigest()

