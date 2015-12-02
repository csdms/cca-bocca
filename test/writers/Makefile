
DBIN=../../scripts
srcdir=.
prefix=/home/baallan/cca/install/t0645
prefix=/home/baallan/cca/build/bocca/trunk/install
prefix=/home/baallan/cca/install/v1

BASEPATH=$(prefix)/lib/python2.5/site-packages
BASEPATH=$(prefix)/lib/python2.3/site-packages
BASEPATH=$(prefix)/lib64/python2.5/site-packages
BASEPATH=$(prefix)/lib/python2.4/site-packages

PYTHONPATH=$(BASEPATH)/boccalib:$(BASEPATH)/boccalib/cct

demo: writers

check: all-check

writers:
	( export PYTHONPATH=$(PYTHONPATH); \
	for i in c cxx f77 f90 java python; do \
		$(DBIN)/demo-writers $$i > $$i.demo-writers.out; \
	done)

all-check:
	(export PYTHONPATH=$(PYTHONPATH); cd ../../install/lib*/python*/site-packages/boccalib/writers; pychecker -# 40 *.py)

clean:
	$(RM) *demo-writers.out

