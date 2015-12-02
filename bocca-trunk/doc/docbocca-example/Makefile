# this makefile requires bash to work

BOCCABIN=/tmp/btt3/bin


all:
	(export PATH=$(BOCCABIN):$(PATH); bin/doc-bocca docbocca)

clean:
	$(RM) -r defaults.gp errfct.eps gnuplot.tmp ls.output shEsc.tmp sinc.eps *.dvi mex.pstex  tmp.tex *.output *.out *.log *.aux *.inp *.toc scratch gen tmp unified docbocca docbocca.pdf first.sh

.PHONY: test
