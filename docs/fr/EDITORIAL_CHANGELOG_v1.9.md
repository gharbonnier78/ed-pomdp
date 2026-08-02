# ED-POMDP en clair - changelog éditorial v1.9

## Guide principal v1.9

- ajout d'une page liminaire de mode d'emploi et de terminologie ;
- mise à jour locale de la version et de l'avis éditorial sur la couverture ;
- conservation des pages 2 à 30 de la v1.8 ;
- retrait de l'ancienne Annexe G du guide principal.

## Companion avancé v1.0

- ajout de deux pages liminaires présentant le niveau, les prérequis et la terminologie ;
- reprise des pages 31 à 37 de la v1.8, correspondant à l'ancienne Annexe G.

## Volumétrie

- base v1.8 : 37 pages ;
- guide principal v1.9 : 31 pages ;
- companion avancé v1.0 : 9 pages.

## Périmètre scientifique

Ce changement est éditorial. Il ne modifie aucun résultat Step 2, aucune formule, aucun tableau, aucune figure, aucune disposition de claim ni aucun artefact scientifique.

## Sources et publication

La composition est décrite directement par les sources LaTeX dans `docs/fr/latex/`. Le document v1.8 hérité y sert de base afin d'éviter une reconstruction artificielle des pages qui ne changent pas.

La CI de publication a :

- compilé `main-guide.tex` et `companion.tex` avec LuaLaTeX ;
- publié les deux PDF destinés au reviewer dans `docs/fr/` ;
- vérifié les nombres de pages attendus ;
- généré `docs/fr/SHA256SUMS` ;
- supprimé le marqueur `.handoff-pending`.

Hashes SHA-256 publiés :

- base v1.8 : `7af6e07623b66412362c1a1c4c816b7e950d948fe36db11e4729715761162899` ;
- guide v1.9 : `d51e3b60b38e88425dfee40233933a0d3567b313dc4a9e44ae4ceb4720a1c622` ;
- companion v1.0 : `3f6981a7f1b880f3e548dda6c713534949ad77aa4c07222a3070cdb3a11820cb`.
