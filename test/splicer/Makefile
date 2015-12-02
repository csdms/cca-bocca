
DO=../../install/bin/resplice
BIN=../../install/bin
DDIR=../../scripts
DBIN=../install/bin
srcdir=.

new-demo:  rob-merge nest-merge extract-1 extract-2 extract-3 demo-1 extract-methods

check: all-check


help:
	$(BIN)/merge --help

ehelp:
	$(BIN)/extract --help

# rob mode
rob-merge:
	-$(RM) ccafe1_StarterComponent_Impl.cxx
	@cp $(srcdir)/impls1.0.0/ccafe1_StarterComponent_Impl.cxx .
	-@cp $(srcdir)/ccafe1.StarterComponent.setServices.gen .
	($(BIN)/bocca-merge --nowarn --to ccafe1_StarterComponent_Impl.cxx --from ccafe1.StarterComponent.setServices.gen )
	@diff --brief ccafe1_StarterComponent_Impl.cxx $(srcdir)/ccafe1_StarterComponent_Impl.cxx.overwrite.sample

rob-merge-2:
	-$(RM) ccafe1_StarterComponent_Impl.cxx
	@cp $(srcdir)/impls1.0.0/ccafe1_StarterComponent_Impl.cxx .
	-@cp $(srcdir)/ccafe1.StarterComponent.setServices.gen .
	($(BIN)/bocca-merge \
		--to ccafe1_StarterComponent_Impl.cxx \
		--from ccafe1.StarterComponent.setServices.gen \
		--match=dtor )
	@diff --brief ccafe1_StarterComponent_Impl.cxx $(srcdir)/ccafe1_StarterComponent_Impl.cxx.overwrite.sample

rob-rename:
	-$(RM) ccafe1_StarterComponent_Impl.cxx
	@cp $(srcdir)/impls1.0.0/ccafe1_StarterComponent_Impl.cxx .
	-@cp $(srcdir)/decaf.CrasherComponent.setServices.gen .
	($(BIN)/bocca-merge \
		--verbose \
		--nowarn \
		--no-rejects \
		--to ccafe1_StarterComponent_Impl.cxx \
		--to-type ccafe1.StarterComponent \
		--from decaf.CrasherComponent.setServices.gen \
		--from-type decaf.CrasherComponent \
	)
	@diff --brief ccafe1_StarterComponent_Impl.cxx $(srcdir)/ccafe1_StarterComponent_Impl.cxx.rename.sample

	
# nesting mode
nest-merge:
	-$(RM) ccafe1_StarterComponent_Impl.cxx
	@cp $(srcdir)/impls1.0.0/ccafe1_StarterComponent_Impl.cxx .
	(export PYTHONPATH=$(PYTHONPATH); $(BIN)/bocca-merge \
	--nowarn -B 'DO-NOT-EDIT bocca.splicer' \
	--to ccafe1_StarterComponent_Impl.cxx \
	--from $(srcdir)/ccafe1_StarterComponent_Impl.setServices.input)
	@diff --brief ccafe1_StarterComponent_Impl.cxx $(srcdir)/ccafe1_StarterComponent_Impl.cxx.insert.sample
	

# extract mode
extract-1:
	-$(RM) -r extracted_blocks_src ccaffeine_TypeMap_Impl.cxx ccaffeine_TypeMap_Impl.hxx
	-$(RM) -r extract-cxx.sample extract-hxx.sample
	-mkdir extracted_blocks_src
	tar xf extract.tar
	(cd extracted_blocks_src ; ../$(BIN)/bocca-extract \
	../impls1.0.0/ccaffeine_TypeMap_Impl.cxx)
	diff --brief -r extracted_blocks_src extract-cxx.sample

extract-2:
	-$(RM) -r extracted_blocks_single ccaffeine_TypeMap_Impl.cxx ccaffeine_TypeMap_Impl.hxx
	-$(RM) -r extract-cxx.sample extract-hxx.sample
	-mkdir extracted_blocks_single
	(cd extracted_blocks_single ; ../$(BIN)/bocca-extract \
		 --one-file \
		-f  ccaffeine_TypeMap_Impl.splices.all \
		../impls1.0.0/ccaffeine_TypeMap_Impl.cxx \
	)
	diff --brief -r extracted_blocks_single/ccaffeine_TypeMap_Impl.splices.all ccaffeine_TypeMap_Impl.splices.all.sample

extract-3:
	-$(RM) -r extracted_blocks_h ccaffeine_TypeMap_Impl.cxx ccaffeine_TypeMap_Impl.hxx
	-$(RM) -r extract-cxx.sample extract-hxx.sample
	-mkdir extracted_blocks_h
	tar xf extract.tar
	(cd extracted_blocks_h ; ../$(BIN)/bocca-extract  \
	../impls1.0.0/ccaffeine_TypeMap_Impl.hxx)
	diff -r extracted_blocks_h extract-hxx.sample
	
extract-4:
	-$(RM) -r extracted_blocks_src ccaffeine_TypeMap_Impl.cxx ccaffeine_TypeMap_Impl.hxx
	-$(RM) -r extract-cxx.sample extract-hxx.sample
	-mkdir extracted_blocks_src
	tar xf extract.tar
	(cd extracted_blocks_src ; ../$(BIN)/bocca-extract \
		--match=get \
	../impls1.0.0/ccaffeine_TypeMap_Impl.cxx)
	diff --brief -r extracted_blocks_src extract-cxx.sample

demo-1:
	(cd $(DDIR); $(DBIN)/bocca-demo-splicer )

extract-methods:
	(cd methods; ../$(BIN)/bocca-extract -O -G -C --method -lc -msetServices -fc.ssgc pytest_c_Impl.c)
	(cd methods; ../$(BIN)/bocca-extract -O --method -lc -msetServices -fc.ss pytest_c_Impl.c)
	(cd methods; ../$(BIN)/bocca-extract -O --method -lcxx -msetServices -fcxx.ss pytest_cxx_Impl.cxx)
	(cd methods; ../$(BIN)/bocca-extract -O --method -lpython -msetServices -fpython.ss p_Impl.py)
	(cd methods; ../$(BIN)/bocca-extract -O --method -lf77 -msetServices -ff77.ss pytest_g_Impl.f)
	(cd methods; ../$(BIN)/bocca-extract -O --method -lf90 -msetServices -ff90.ss pytest_f_Impl.F90)
	(cd methods; ../$(BIN)/bocca-extract -O --method -ljava -msetServices -fjava.ss Driver_Impl.java)
	(cd methods; diff java.ss java.ss.sample)
	(cd methods; diff python.ss python.ss.sample)
	(cd methods; diff cxx.ss cxx.ss.sample)
	(cd methods; diff c.ssgc c.ssgc.sample)
	(cd methods; diff c.ss c.ss.sample)
	(cd methods; diff f77.ss f77.ss.sample)
	(cd methods; diff f90.ss f90.ss.sample)

all-check:
	(export PYTHONPATH=$(PYTHONPATH); cd ../../install/lib*/python*/site-packages/boccalib/splicers; pychecker -# 140 *.py)

clean:
	$(RM) -r *.o *.out tmp extract-cxx* extract-hxx* *.diff *.splice *.rej fred ccafe1_StarterComponent_Impl.cxx extracted_blocks* ccaffeine_TypeMap_Impl.cxx ccaffeine_TypeMap_Impl.hx extract-cxx.sample extract-hxx.sample .*.bak methods/*.ss methods/*.ssgc

