import os

# Get a recursive list of files without any version control dirs.
# as seen from rootdir of the dirs/files named in inputlist.
# Newer versions of python have fancy support for this, but we
# want 2.4 python to work. Directories are not returned.
def indexPlainFilesRelativeNoVC(rootdir, inputList, ignorelist=[]):
    files = []
    curdir=os.getcwd()
    if os.path.isdir(rootdir):
        os.chdir(rootdir)
    else:
        exit(1)
    for top in inputList:
        stack = [ top ]
        while stack:
            directory = stack.pop()
            for file in os.listdir(directory):
                if file == ".svn" or file == "CVS" or file == ".cvsignore":
                    continue
                fullname = os.path.join(directory, file)
                if not os.path.isdir(fullname) and not os.path.islink(fullname):
                    if not fullname in ignorelist:
                        files.append(fullname)
                if os.path.isdir(fullname) and not os.path.islink(fullname):
                    stack.append(fullname)
    os.chdir(curdir)
    return files

from distutils.core import setup
from distutils import dir_util,file_util
#
# workaround lack of package_data in py 2.3 distutils.
# mydist is the setup() result.
# pkg is the package name under which base_dirs dirs exist,
# assumed to exist in the same dir as the setup file.
# base_dirs is the dirs to be cloned.
# Note that unlike pa
def clonetree(mydist, pkg, base_dirs, ignorelist=[]):
    wheretoinstall = mydist.command_obj['install'].install_purelib
    filenames=indexPlainFilesRelativeNoVC(pkg, base_dirs)
    target=os.path.join(wheretoinstall,pkg)
    for filename in filenames:
        dir = os.path.dirname(filename)
        targetdir=os.path.join(target,dir)
        if not os.path.exists(targetdir):
            os.makedirs(targetdir)
        file_util.copy_file(os.path.join(pkg,filename), targetdir)

#
# check to see if the named dir exists in the install tree.
# mydist is the setup() result.
#
def dirinstalled(mydist, dir):
    wheretoinstall = mydist.command_obj['install'].install_purelib
    target = os.path.join(wheretoinstall,dir)
    if os.path.exists(target) and os.path.isdir(target):
        return True
    return False
