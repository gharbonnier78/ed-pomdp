DOCS = \
	paper/main \
	paper/step2_closeout \
	paper/milestone2r_theory_claim_reset \
	research_program/research_program \
	survey/related_work \
	reviewer/reviewer_companion \
	reviewer/guide_fr_milestone2r \
	ontology/evidence_ontology \
	appendix/mathematical_appendix \
	identifiability/identifiability_note \
	benchmark/results/STEP_2_7_EXECUTIVE_STATUS_NOTE

.PHONY: all clean check

all:
	@for d in $(DOCS); do \
	  dir=$$(dirname $$d); base=$$(basename $$d); \
	  (cd $$dir && latexmk -pdf -interaction=nonstopmode -halt-on-error $$base.tex) || exit 1; \
	done

check:
	python3 scripts/check_current_status.py
	python3 scripts/check_package.py

clean:
	@for d in $(DOCS); do \
	  dir=$$(dirname $$d); base=$$(basename $$d); \
	  (cd $$dir && latexmk -C $$base.tex); \
	done
