LATEX=lualatex
FLAGS=-interaction=nonstopmode -halt-on-error

all: ../ED_POMDP_En_Clair_FR_v1.9.pdf ../ED_POMDP_Belief_to_Action_Companion_FR_v1.0.pdf

../ED_POMDP_En_Clair_FR_v1.9.pdf: main-guide.tex common.tex base/ED_POMDP_En_Clair_FR_v1.8.pdf
	$(LATEX) $(FLAGS) -jobname=ED_POMDP_En_Clair_FR_v1.9 main-guide.tex
	$(LATEX) $(FLAGS) -jobname=ED_POMDP_En_Clair_FR_v1.9 main-guide.tex
	mv ED_POMDP_En_Clair_FR_v1.9.pdf $@

../ED_POMDP_Belief_to_Action_Companion_FR_v1.0.pdf: companion.tex common.tex base/ED_POMDP_En_Clair_FR_v1.8.pdf
	$(LATEX) $(FLAGS) -jobname=ED_POMDP_Belief_to_Action_Companion_FR_v1.0 companion.tex
	$(LATEX) $(FLAGS) -jobname=ED_POMDP_Belief_to_Action_Companion_FR_v1.0 companion.tex
	mv ED_POMDP_Belief_to_Action_Companion_FR_v1.0.pdf $@

clean:
	rm -f *.aux *.log *.out *.toc *.pdf
