""" Various err-handling related miscellanea
"""
import sys, os
import traceback
from cct._file import BFileManager
import cct._util

#--------------------------

def err(errmsg='',errcode=1):
    defaults = cct._util.Globals().getDefaults()
    use_colors = 'disabled'
    if defaults and defaults.has_option('Project','use_colors'): 
        use_colors = re.split('\W+',defaults.get('Project','use_colors'))[0]
    if use_colors == 'enabled':
        print >>sys.stderr, '\033[1;31m' + 'Bocca ERROR: ' + '\033[0m' + errmsg
    else: 
        print >>sys.stderr, 'Bocca ERROR: ' + errmsg
    if 'BOCCA_DEBUG' in os.environ.keys() and os.environ['BOCCA_DEBUG'] == '1': 
        traceback.print_stack()
    fm = BFileManager()
    fm.undo()   # Restore files to original state (created files deleted, modified files restored from backups
    fm.close()  # Just in case
    sys.exit(errcode)

def warn(errmsg='',errcode=1):
    msg = errmsg
    use_colors = 'disabled'
    defaults = cct._util.Globals().getDefaults()
    if defaults and defaults.has_option('Project','use_colors'): use_colors = re.split('\W+',defaults.get('Project','use_colors'))[0]
    if use_colors == 'enabled': print >>sys.stderr, '\033[1;31m' + 'Bocca WARNING: ' + '\033[0m' + errmsg
    else: print >>sys.stderr, 'Bocca WARNING: ' + errmsg

def exit(msg=''): 
    if msg != '': print >>sys.stdout, msg  
    fm = BFileManager()
    fm.close()
    sys.exit(0)
