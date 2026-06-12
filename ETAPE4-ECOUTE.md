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
- Ordre conseillé : B, A, D, F, C, E, puis réécoutes libres.
- **Noter les six chiffres avant de lire la suite.**

Grille : `A: _/5  B: _/5  C: _/5  D: _/5  E: _/5  F: _/5`

---

## 2. Correspondance des fichiers (à lire APRÈS notation)

| Fichier | Timbre | Matériau | Statut grammatical |
|---|---|---|---|
| A | cloche Westerkerk | tierces-de-cloche (307 c) parallèles, cantus Fux | **INTERDIT** par R2-cloche |
| B | harmonique | chemin légal dérivé (étape 3), cantus Fux | LÉGAL (grammaire harmonique) |
| C | cloche Westerkerk | quintes (702 c) parallèles, cantus Fux | ~légal sur cloche (Φ=0,287, juste sous le seuil) |
| D | harmonique | quintes (702 c) parallèles, cantus Fux | **INTERDIT** par R2-harmonique |
| E | cloche Westerkerk | chemin légal dérivé (étape 3), cantus miroir | LÉGAL (grammaire cloche) |
| F | harmonique | tierces-de-cloche (307 c) parallèles, cantus Fux | légal sur harmonique (Φ≈0,02, creux de fusion) |

Croisements : **D↔C** = mêmes notes (quintes parallèles), timbre échangé ;
**A↔F** = mêmes notes (307 c parallèles), timbre échangé.

## 3. Prédictions enregistrées (avant écoute)

Forme faible suffisante : les ORDRES de séparabilité ci-dessous (pas d'écart
quantitatif exigé).

- **E1 (contrôle, le connu)** : D < B — les quintes parallèles fusionnent
  plus que le contrepoint légal, sur timbre harmonique. *Si E1 tombe, c'est
  Fux qu'on échoue à reproduire à l'écoute : chaîne de rendu ou Φ en cause.*
- **E2 (le neuf, intra-cloche)** : A < E — les tierces-de-cloche parallèles
  fusionnent plus que le contrepoint légal de la cloche.
- **E3 (croisement décisif)** : D < C — les MÊMES quintes parallèles
  fusionnent davantage sur timbre harmonique que sur cloche. *C'est l'interdit
  de quintes rendu timbre-dépendant, à l'oreille.*
- **E4 (croisement symétrique)** : A < F — les MÊMES tierces 307 c parallèles
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
