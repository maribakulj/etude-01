# ETAPE4-ECOUTE — écoute de falsification : protocole et prédictions enregistrées

*Daté du 2026-06-12. Les stimuli sont générés et les prédictions ci-dessous
sont ENREGISTRÉES AVANT toute écoute par quiconque. L'auditeur (l'utilisateur)
est le tribunal ; ce document est la feuille d'expérience. Discipline : ne pas
lire les §3-§5 avant d'avoir noté les six fichiers.*

---

## 1. Protocole (à lire avant d'écouter — NE PAS lire plus loin)

- **Matériel** : casque ou bonnes enceintes, volume modéré. Fichiers mono par
  construction (la spatialisation séparerait les voix par un indice hors
  modèle).
- **Matériau** : 6 fichiers `stim_A.wav` … `stim_F.wav` (~13 s chacun).
  Chaque fichier : deux voix de MÊME timbre, note contre note (1re espèce),
  synthèse additive portant exactement les partiels d'un des deux modèles de
  l'étude.
- **La question, unique** : au fil de l'écoute, j'entends…
  **1 = une seule couche sonore** (les voix se confondent en un objet)
  … **5 = deux voix clairement indépendantes**.
  Noter un chiffre par fichier + tout moment où la perception bascule.
- **Ne PAS juger l'agrément** (beau/laid, doux/rêche). La rugosité n'est pas
  la fusion — l'hygiène C≠Φ vaut aussi à l'écoute. Un son peut être rêche ET
  à deux voix nettes, lisse ET fusionné.
- Ordre conseillé (v2) : E, A, C, D, F, B, puis réécoutes libres.
- **Noter les six chiffres avant de lire la suite.**

Grille : `A: _/5  B: _/5  C: _/5  D: _/5  E: _/5  F: _/5`

---

## 2. Correspondance des fichiers — **v2** (à lire APRÈS notation)

| Fichier | Timbre | Matériau | Statut grammatical |
|---|---|---|---|
| A | harmonique | quintes (702 c) parallèles, cantus Fux | **INTERDIT** par R2-harmonique |
| B | cloche Westerkerk | chemin légal dérivé (étape 3), cantus miroir | LÉGAL (grammaire cloche) |
| C | harmonique | tierces-de-cloche (307 c) parallèles, cantus Fux | légal sur harmonique (Φ≈0,02, creux de fusion) |
| D | cloche Westerkerk | tierces-de-cloche (307 c) parallèles, cantus Fux | **INTERDIT** par R2-cloche |
| E | harmonique | chemin légal dérivé (étape 3), cantus Fux | LÉGAL (grammaire harmonique) |
| F | cloche Westerkerk | quintes (702 c) parallèles, cantus Fux | ~légal sur cloche (Φ=0,287, juste sous le seuil) |

Croisements : **A↔F** = mêmes notes (quintes parallèles), timbre échangé ;
**D↔C** = mêmes notes (307 c parallèles), timbre échangé.

## 3. Prédictions enregistrées (avant écoute — lettres v2)

Forme faible suffisante : les ORDRES de séparabilité ci-dessous (pas d'écart
quantitatif exigé).

- **E1 (contrôle, le connu)** : A < E — les quintes parallèles fusionnent
  plus que le contrepoint légal, sur timbre harmonique. *Si E1 tombe, c'est
  Fux qu'on échoue à reproduire à l'écoute : chaîne de rendu ou Φ en cause.*
- **E2 (le neuf, intra-cloche)** : D < B — les tierces-de-cloche parallèles
  fusionnent plus que le contrepoint légal de la cloche.
- **E3 (croisement décisif)** : A < F — les MÊMES quintes parallèles
  fusionnent davantage sur timbre harmonique que sur cloche. *C'est l'interdit
  de quintes rendu timbre-dépendant, à l'oreille.*
- **E4 (croisement symétrique)** : D < C — les MÊMES tierces 307 c parallèles
  fusionnent davantage sur cloche que sur harmonique.

Confusions possibles, déclarées :
1. Sur F (307 c, harmonique), des battements peuvent rendre le son RÊCHE sans
   le fusionner — juger uniquement « une couche ou deux voix ».
2. La cloche tenue est un objet inhabituel ; comparer d'abord cloche↔cloche
   (A, C, E) avant les croisements.
3. Les chemins légaux (B, E) contiennent des unissons médians (résidu mesuré
   à l'étape 3) : la séparabilité s'y effondre LOCALEMENT par construction —
   l'unisson EST fusion dans le modèle. À noter à part, pas comme échec.

## 4. Ce qui ferait échouer quoi (falsification)

- **E3 et E4 tombent** → le déplacement de l'interdit n'a pas de réalité
  perceptive sur cette paire de timbres : P5 perceptif réfuté ; la
  grammaire-cloche redevient un objet formel (et le projet §8.3 enregistre son
  « résultat riche » : la coïncidence spectrale ne suffit pas à la fusion).
- **E1 tombe** → problème en amont (rendu ou Φ) ; tout le reste est suspendu.
- **Seuls E2/E4 tombent** → Φ prédit la fusion sur l'harmonique mais pas sur
  l'inharmonique : la borne de validité de la métrique est localisée — c'est
  une mesure, pas une défaite.

## 5. Verdict (à remplir après l'écoute)

Notes de l'auditeur : `A: _  B: _  C: _  D: _  E: _  F: _`
E1 (D<B) : __ ; E2 (A<E) : __ ; E3 (D<C) : __ ; E4 (A<F) : __
Commentaires libres (basculer, moments, timbre) :

## 6. Rejouer

`python3 etape4_stimuli.py` — graine fixe, stimuli reproductibles bit à bit ;
mapping dans `etape4_mapping.json`.

---

## 7. Journal daté

### 2026-06-12 (17 h) — première écoute (stimuli v1) : échec de plancher, consigné comme donnée

Retour de l'auditeur sur les stimuli v1 (spectres tenus, sans articulation) :
« ça ressemble à un son de synthé, je ne vois pas de différenciation de voix »
— y compris, donc, sur les stimuli LÉGAUX. Aucune notation rendue.

**Diagnostic** : le rendu statique littéral (tenue stationnaire, voix
synchrones, même timbre, mono) supprime tous les indices d'événement de la
scène auditive (attaques, décroissances) ; sans événements, il n'y a pas de
voix à séparer — effet de plancher, prédictions intestables. **C'est une
donnée, pas un simple bug** : l'idéalisation « simultanéité statique » de v1,
rendue telle quelle, ne produit même pas l'explanandum (des voix). Première
confirmation à l'oreille que la dimension temporelle n'est pas un raffinement
mais une précondition de la polyphonie — cohérent avec le différé « dynamique
temporelle » du CADRAGE §9, qui passe de « extension » à « nécessité » pour
toute écoute future.

**Correction v2, déclarée** : articulation par note IDENTIQUE pour les deux
voix et les deux timbres (attaque 15 ms, décroissance exponentielle globale
τ=0,9 s) — « globale » : tous les partiels décroissent ensemble, les rapports
d'amplitudes donc Φ restent exactement ceux du modèle à chaque instant
(vérifié : ratios identiques à ±1 % entre début et fin de note). Aucun indice
de ségrégation asymétrique ajouté : la seule chose qui distingue encore les
stimuli est (structure d'intervalles × timbre). Le timbre de cloche retrouve
au passage son identité perceptive (attaque-décroissance).

**Aveugle** : l'assignation v1 des lettres étant potentiellement compromise,
les lettres ont été RETIRÉES À NEUF en v2 (table §2 ci-dessus mise à jour).
Les prédictions E1-E4 sont inchangées sur le fond, lettres réassignées. Les
stimuli v1 ne sont pas conservés dans le dépôt (remplacés) ; leur génération
reste reproductible via l'historique git.
