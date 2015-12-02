# This files is processed whenever 'make install' is run in the bocca
# top-level bocca directory.

# Version number of the form x.y.z (set in configure.ac)
bocca_version="0.5.7"

# Latest revision number obtained with svn info -r HEAD
# set by both conigure and 'make/make install'
bocca_svn_revision="1818"

# Latest revision date  obtained with svn info -r HEAD
# set by both configure and 'make/make install'
bocca_svn_date="Thu Feb  3 15:19:05 CST 2011"

# Release name (string), again comes from configure
bocca_release="unstable"

__version__ = "bocca version %s\n" \
              "subversion revision > %s\n" \
              "last modified: %s\n" \
              "%s release\n" % (bocca_version, bocca_svn_revision, bocca_svn_date, bocca_release)

