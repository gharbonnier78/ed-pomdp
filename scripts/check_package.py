from pathlib import Path
import json, sys
root=Path(__file__).resolve().parents[1]
required=[
 'paper/main.pdf','research_program/research_program.pdf','survey/related_work.pdf',
 'reviewer/reviewer_companion.pdf','ontology/evidence_ontology.pdf','appendix/mathematical_appendix.pdf',
 'ontology/evidence_item.schema.json','README.md','CITATION.cff']
missing=[x for x in required if not (root/x).exists()]
if missing:
 print('Missing:',missing); sys.exit(1)
json.loads((root/'ontology/evidence_item.schema.json').read_text())
for p in [root/x for x in required if x.endswith('.pdf')]:
 if p.stat().st_size < 5000:
  print('Suspiciously small PDF',p); sys.exit(1)
print('Package check OK:',len(required),'required artifacts')
