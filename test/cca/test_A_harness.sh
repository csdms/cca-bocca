#!/bin/sh
# This file documents the harness standard for the tests in this directory.
# This is separate from any python unit testing.
# Each test script will be in sh
# Each test script will be invoked with arguments
# 1: full path name of bocca executable.
#
# Each test script should create their own scratch directory
# (normally a bocca project) with a name which is the 
# name of the script minus the trailing .sh and leading test_.
#
# Tests which require multiple projects should follow
# the naming convention and make projects below their
# named scratch.
#
# Each script will return 0 unless it detects an error.
# it is helpful, and required, that the printed output
# of each script will be a brief description followed by a
# line with PASS, FAIL, BROKEN, or PENDING.
# PASS/FAIL are obvious. BROKEN indicates something detected
# in preparing for the test that means the test can't be run.
# PENDING means the test failed in an expected way (usually
# for tests of features not yet implemented.
# Scripts here should be named so that alphabetical (ascii)
# ordered running makes sense, i.e. simpler tests first, if
# one test depends on the resulting structure of another.


echo "Beginning command line test set."
echo "Bocca tested is $1"
if test -z "$1"; then
	echo "FAIL"
	exit 1
fi
if ! test -x "$1"; then
	echo "missing bocca script"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
