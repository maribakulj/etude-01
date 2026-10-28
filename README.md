# Étude 01 — règles de mouvement contrapuntique dérivées d'un spectre

*État au 2026-10-28. Ce fichier dit ce qui est implémenté, ce qui ne l'est
pas, et à quel point les résultats tiennent. Il prime sur le ton des
documents d'étape quand ils divergent.*

## Ce que c'est

Une collection de scripts Python exploratoires qui testent une hypothèse :
**les interdits de mouvement parallèle du contrepoint (quintes, octaves)
pourraient suivre la fusion spectrale des intervalles, et donc changer avec le
timbre.** À partir d'un spectre (liste de partiels), les scripts calculent :

- C(i), la consonance de Sethares (rugosité de Plomp-Levelt) → les intervalles
  admis comme états (règle R1) ;
- Φ(i), un indice de coïncidence spectrale (formulation publiée, largeur
  σ = 6,83 c) → les intervalles vers lesquels le mouvement parallèle est
  interdit (règle R2, seuil τ_F) ;
- un automate (états × mouvements) et ses chemins légaux pour un cantus.

Ce n'est **pas** un paquet logiciel, ni un modèle formellement vérifié, ni
(encore) un résultat perceptif établi.

## Statut : implémenté / non implémenté

| Élément | Statut |
|---|---|
| Métriques C et Φ, auto-tests | implémenté (`metriques_fusion.py`) |
| Extraction de spectre depuis un WAV | implémenté, validé sur synthétique (`test_extraction.py`) |
| Grammaire R1/R2/R3/R5, automate, chemin légal | implémenté (`graphe_grammaire.py`) |
| Spectres réels | 2 : une dent de boîte à musique (cas dégénéré, sans objet) et une cloche de carillon (spectre publié, Harrison & MacConnachie 2024) |
| Diagramme de phase | 1 famille synthétique (corde raide), 1 schéma de seuils |
| Écoute | 1 auditeur, informé de la théorie, 4 essais à choix forcé |
| `lean-export/` | **échafaudage CI** (import Mathlib + deux `#check`) ; aucun énoncé du modèle n'y est formalisé |
| Tests automatisés | auto-tests et validation d'extraction ; pas de suite de tests unitaires |

## Limites connues (à lire avant tout résultat)

1. **Le cas harmonique est une calibration, pas une prédiction.** τ_F (0,226 ×
   max Φ fini du timbre) est le milieu de la fenêtre de seuils qui *reproduit*
   Fux sur le spectre harmonique (ETAPE3-GRAPHE.md §1.4). Cette fenêtre va de
   0,143 à 0,309 : en dessous, R2 interdit aussi les quartes et sixtes
   parallèles ; au-dessus, les quintes parallèles deviennent légales.
   Retrouver « quintes et octaves parallèles interdites » ne constitue donc
   **aucune preuve** que la fusion spectrale *cause* l'interdit historique. Le
   contenu non circulaire sur l'harmonique se réduit au classement
   Φ(P8) > Φ(P5) > Φ(P4) > Φ(M6) > Φ(M3), proche de la hiérarchie
   helmholtzienne des rapports simples, déjà connue.

2. **Le seul résultat hors calibration (la cloche) est en partie au bord de son
   plateau.** Avec le τ_F déclaré, la grammaire-cloche interdit les parallèles
   vers {unisson, 307 c, 886 c} et laisse passer quintes et octaves. Mais
   cet ensemble ne tient que pour τ_F ∈ [0,224 ; 0,346] : **0,002 sous** la
   valeur déclarée, P5 et P8 redeviennent interdites. Ce qui est robuste :
   la tierce mineure de cloche (307 c) a de loin le Φ le plus élevé
   (1,285 contre 0,445 pour la suivante) et reste interdite à tout seuil.
   « La cloche autorise les quintes parallèles » est fragile.

3. **Les bifurcations du diagramme de phase dépendent du seuil.** La 1re
   bifurcation à B ≈ 7,7e-3 ne tient que pour τ_F ≈ 0,20-0,25 ; ailleurs elle
   va de 9,4e-4 à 1,1e-1, et le nombre de bifurcations varie de 1 à 18
   sur τ_F ∈ [0,10 ; 0,40] (8 au seuil déclaré). La 1re bifurcation au seuil déclaré vient d'un état
   à 1274 c, dans la zone 1200-1400 c ouverte par l'extension déclarée du
   compas. « Bifurcation » y désigne un changement de cardinalité d'un
   ensemble seuillé, pas une transition de phase au sens physique.

4. **Φ n'est pas validé comme mesure de fusion perceptive.** Sa formulation est
   publiée (proxy de Milne, DECISION-PHI.md), mais σ = 6,83 c provient d'un travail sur l'affinité *mélodique*,
   pas sur la ségrégation de flux auditifs. Coïncidence spectrale ≠ fusion de
   deux voix.

5. **L'écoute est exploratoire.** 4/4 dans le sens prédit par un seul
   auditeur, informé de la théorie, sans répétition ni contrebalancement :
   sous hasard pur, 4/4 arrive une fois sur 16 (p ≈ 0,06). Aucun modèle
   concurrent (rugosité seule, par exemple) n'a fait de prédictions sur ces
   mêmes stimuli.

6. **Vocabulaire.** « Quasicristal spectral », « règles de sélection »,
   « transition de phase » sont, dans CADRAGE-v2.md, des **analogies**, pas
   des notions définies mathématiquement dans le code.

Les chiffres des points 1-3 sont produits par `python3 sensibilite_seuil.py`.

## Moratoire

Pas d'extension du modèle (nouvelles règles, nouveaux timbres, nouveaux
diagrammes) tant que l'hypothèse centrale n'a pas survécu à un test
indépendant. Le protocole de ce test est en brouillon :
[`PROTOCOLE-TEST-DECISIF.md`](PROTOCOLE-TEST-DECISIF.md).

## Reproduire

```bash
pip install -r requirements.txt
./reproduire.sh
```

Le script rejoue toutes les expériences commitées (~45 s) et écrit le journal
dans `journal_reproduction.txt`. Rejoué le 2026-10-28 avec les versions de
`requirements.txt` : les JSON et WAV régénérés sont identiques octet pour
octet à ceux du dépôt, et les verdicts sont inchangés. Les PNG diffèrent
seulement par le rendu de la version de matplotlib. `extraction_spectre.py`
et `segmentation_notes.py` ne sont pas rejoués sur les enregistrements bruts,
qui ne sont pas commités (cf. `materiau/README.md`).

## Documents (ordre de lecture)

1. `CADRAGE-v2.md` — la question et le cadrage (contient les analogies du point 6).
2. `PASSATION.md` — état initial et invariants.
3. `DECISION-PHI.md` — choix de la métrique Φ (étape 1).
4. `ETAPE2-PROTOCOLE.md` — spectres mesurés, verdicts P5 (étape 2).
5. `SPEC-v1-graphe-grammaire.md`, `ETAPE3-GRAPHE.md` — grammaire et automates (étape 3).
6. `ETAPE4-ECOUTE.md` — écoute de falsification informelle (étape 4).
7. `DIAGRAMME-PHASE.md` — balayage de l'inharmonicité.
8. `PROTOCOLE-TEST-DECISIF.md` — brouillon du test indépendant.
