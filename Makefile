DOCS = paper/main research_program/research_program survey/related_work reviewer/reviewer_companion ontology/evidence_ontology appendix/mathematical_appendix

.PHONY: all clean check
all:
	@for d in $(DOCS); do \
	  dir=$$(dirname $$d); base=$$(basename $$d); \
	  (cd $$dir && latexmk -pdf -interaction=nonstopmode -halt-on-error $$base.tex) || exit 1; \
	done

check:
	python3 scripts/check_package.py

clean:
	@for d in $(DOCS); do dir=$$(dirname $$d); base=$$(basename $$d); (cd $$dir && latexmk -C $$base.tex); done
