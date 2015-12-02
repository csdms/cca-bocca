#! /usr/bin/env python
import sys

from distutils.core import setup
# for py 2.3, we may have to import from a local copy of the
# current distutils for 2.3 which supports package_data
# but is not widely packaged in 2.3-bearing versions of linux.


verbose=1

import os
import boccalib.fileutil
import scripts.gendoc

########################## main setup ######################

# Keep one simple restriction in mind and this setup
# script will stay very small-- any directory you want
# installed must contain a plain file or a subdirectory
# that contains a plain file. This is because package_data
# in distutils will not install an empty directory.

# base_files contains the subdirs of boccalib that are to be cloned
# into the installation, less version controls which may be loose.
base_files = [ "templates", "defaults" ]

# doc files contains the pydoc-generated html documentation
#os.execvp('scripts/gendoc.py',['gendoc.py'])
doc_files = []
for f in os.listdir('doc'):
    if f.endswith('.html'): doc_files.append(os.path.join('doc',f))

mydist = setup (name = "boccalib", version = "0.1",
       description = "Bocca utilities dispatcher",
       url="https://www.cca-forum.org/bugs/bocca",
       author="Bocca developers",
       author_email="bocca-dev@cca-forum.org",
       packages = ['boccalib', 
                   'boccalib.builders', 
                   'boccalib.cct', 
                   'boccalib.graph', 
                   'boccalib.graph.graphlib', 
                   'boccalib.parse',
                   'boccalib.parse.itools',
                   'boccalib.parse.itools',
                   'boccalib.parse.itools.visitor',
                   'boccalib.parse.ply',
                   'boccalib.splicers',
                   'boccalib.utils',
		   'boccalib.writers'],
       scripts = [ 'scripts/bocca', 
                   'scripts/clide', 
                   'scripts/cct', 
                   'scripts/bocca-demo-splicer' ,
                   'scripts/bocca-extract' ,
                   'scripts/bocca-merge' ],
# while package_data still contains executable scripts,
# we can't use distutils package_data.
#       package_data ={'boccalib': boccalib.fileutil.indexPlainFilesRelativeNoVC("boccalib", base_files) }
       data_files=[('share/doc', doc_files)]
      )

#
# If at some future point we're using package_data,
# the check below will prevent double installation.
# The version below is needed for python 2.3 in all cases.
if "install" in sys.argv:
    boccalib.fileutil.clonetree(mydist, "boccalib", base_files)
