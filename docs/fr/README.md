# Documents pédagogiques ED-POMDP en français

Deux documents sont proposés dans cette PR :

- [`ED_POMDP_En_Clair_FR_v1.9.pdf`](./ED_POMDP_En_Clair_FR_v1.9.pdf) - guide principal, annexes A à F ;
- [`ED_POMDP_Belief_to_Action_Companion_FR_v1.0.pdf`](./ED_POMDP_Belief_to_Action_Companion_FR_v1.0.pdf) - companion avancé reprenant l'ancienne Annexe G.

Les deux documents sont disponibles **uniquement en français**.

## Sources LaTeX

Les sources sont dans [`latex/`](./latex/) :

- `main-guide.tex` ;
- `companion.tex` ;
- `common.tex` ;
- `Makefile` ;
- `base/ED_POMDP_En_Clair_FR_v1.8.pdf`, publication héritée utilisée pour conserver les pages existantes.

Compilation locale :

```bash
cd docs/fr/latex
make
```

La CI [`build-french-editorial-pdfs.yml`](../../.github/workflows/build-french-editorial-pdfs.yml) compile les deux sources, vérifie les nombres de pages attendus, publie les PDF dans `docs/fr/` et régénère [`SHA256SUMS`](./SHA256SUMS).

## Vérification publiée

- base v1.8 : 37 pages ;
- guide principal v1.9 : 31 pages ;
- companion avancé v1.0 : 9 pages ;
- marqueur `.handoff-pending` supprimé après compilation réussie.

Le split est volontairement conservateur : le guide reprend les pages 2 à 30 de la v1.8 et le companion reprend les pages 31 à 37. Seules les pages liminaires et l'avis éditorial de couverture sont nouveaux.

Voir [`EDITORIAL_CHANGELOG_v1.9.md`](./EDITORIAL_CHANGELOG_v1.9.md) pour le détail destiné au reviewer.
