#!/bin/sh
# This file documents the harness standard for the tests in this directory.
# This is separate from any python unit testing.
# Each test script will be in sh
# Each test script will be invoked with arguments
# 1: full path name of bocca executable.
# 2: full path name of the scratch dir to run in.
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
# Individual tests are responsible for optionally making
# subdirectories under scratch as desired.


echo "Beginning command line test set."
echo "Bocca tested is $1"
echo "Scratch dir is $2"
if test -z "$1"; then
	echo "FAIL"
	exit 1
fi
if test -z "$2"; then
	echo "FAIL"
	exit 1
fi
if ! test -x "$1"; then
	echo "missing bocca script"
	echo "FAIL"
	exit 1
fi
if ! test -d "$2"; then
	echo "missing scratch directory"
	echo "FAIL"
	exit 1
fi
echo "PASS"
exit 0
