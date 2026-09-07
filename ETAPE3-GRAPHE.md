# ETAPE3-GRAPHE — le graphe-grammaire : automates, fraction de Fux, sensibilité

*Daté du 2026-06-12. Étape 3 de la PASSATION : états + arêtes (R1/R2/R3/R5),
un automate par (timbre × récepteur), fraction de Fux récupérée (SPEC §6.3),
analyse de sensibilité τ_C/τ_F. Périmètre v1 inchangé : simultanéité, première
espèce, deux voix, compas d'une octave.*

Code : `graphe_grammaire.py` (gabarits = données, traçabilité du seuillage),
`rugosite.py` (le scalaire C, jamais mélangé à Φ), `etape3_fux.py` (harnais).
Rejouer : `python3 etape3_fux.py`.

---

## 1. Décisions de modélisation (déclarées)

1. **Grille d'états par colonne = pics locaux de C(i)** pour ce (timbre ×
   récepteur) — la « gamme de l'objet » (acquis Sethares) — puis gate R1
   (C ≥ τ_C). L'unisson est un état (pic de C).
2. **Cantus en cents, identique pour tous les timbres comparés** (ici le
   cantus dorien de Fux, 12-TET) ; le contrepoint choisit ses intervalles
   dans la grille du timbre. Isoler l'effet timbre dans le vertical/mouvement.
3. **Φ(unisson) := +∞ par convention déclarée** (la proxy exclut la
   self-coïncidence ; deux voix confondues SONT une). Conséquences : R2
   interdit toujours parallèle/direct vers l'unisson ; l'unisson admis est
   toujours état de frontière R3.
4. **Seuils illustratifs par schéma symétrique déclaré** (pas de
   cherry-picking) : τ_C = milieu du plus large plateau du timbre ; τ_F = même
   niveau RELATIF pour tous les timbres (0,226 × max Φ fini du timbre), fixé
   une fois sur le contrôle harmonique (milieu du plateau qui y reproduit
   Fux). Les seuils ne sont jamais figés : les plateaux complets sont la
   donnée (SPEC §7).
5. **Traçabilité** : chaque arête supprimée garde (mouvement, Φ d'arrivée,
   τ_F, paire de partiels dominante). Exemple sur l'harmonique : l'interdit
   d'arrivée directe sur la quinte est porté par la paire (3,2) — 3ᵉ
   harmonique du grave contre 2ᵉ de l'aigu, écart 0 c ; l'octave par (2,1).
   « Parce que tel fait spectral » est dans la structure.

## 2. Timbre harmonique + récepteur humain (contrôle) — fraction de Fux

Grille candidate (pics de C, Sethares, roll-off 1/k) : unisson, 387 (M3), 498
(P4), **618 (≈10/7, septimal)**, 702 (P5), 814 (m6), 884 (M6), **969 (≈7/4,
septimal)**, 1200 (P8). *Pas de pic de tierce mineure* (épaule, pas maximum).

| Règle de Fux (1re espèce) | Verdict | Détail |
|---|---|---|
| F2+F3 — pas de parallèles NI de directes vers unisson/quinte/octave | **RETROUVÉE, robuste** | plateau τ_F relatif 0,16 donne exactement {P5, P8} (+ unisson par convention) ; « pas de parallèles d'octave » seul tient sur 0,66 — la règle la plus robuste du système |
| F4 — commencer/finir sur unisson/octave | **RETROUVÉE, exacte** | frontières R3 = {0, 1200} (argmax Φ = octave) |
| F1 — inventaire vertical = consonances de Fux | **NON, à tout seuil** | meilleur recouvrement Jaccard 0,71 ({0, 702, 814, 884, 1200}) ; résidu en trois morceaux, voir ci-dessous |
| F5 — préférence du mouvement contraire | **gabarit imposé** | forme conçue à la main (CADRAGE §9), pas une découverte ; v1 n'ajuste que ses poids |

**Le résidu de F1, mesuré** (c'est la mesure de la convention que §6.3
demandait) :
1. **La quarte** : pic de C fort (0,71) → admise par le gate dès que les
   tierces le sont. Son interdiction par Fux n'est pas dans la rugosité — *de
   la convention (ou du principe manquant : la quarte est traitée par rapport
   à la BASSE dans la pratique, fait contrapuntique hors v1).*
2. **Les pics septimaux** (618 ≈ 10/7, 969 ≈ 7/4) : consonances réelles de
   Sethares pour un timbre 1/k à 10 partiels, absentes du système de Fux —
   *l'inventaire dérivé est « 7-limit », celui de la pratique est 5-limit ;
   l'écart mesure ce que l'histoire a filtré.*
3. **La tierce mineure manquante** (pas de pic) : la hiérarchie de C est trop
   plate dans cette zone pour le roll-off 1/k — *limite du modèle C (fragilité
   n°3 de la PASSATION : Sethares accepté comme socle, daté).*

Déviations du chemin légal vs la pratique (résidu côté arêtes) : unissons en
milieu de pièce (Fux les réserve aux extrémités — règle absente des gabarits
v1) ; usage des états septimaux. À retenir pour l'étape 4 (écoute) : c'est là
qu'on entendra si ces « légalités » fonctionnent.

## 3. Cloche Westerkerk (spectre publié) + humain — la grammaire déplacée

Grille candidate : unisson, **307 (m3 de cloche)**, 395 (M3), 702 (P5), 809
(m6), **886 (M6 de cloche — 2ᵉ consonance du timbre, C=0,94)**, 1020 (m7),
1200 (P8). Cohérence externe : Harrison & MacConnachie trouvent M3 devenue
dissonante sur carillon — notre 395 est le plus faible pic (C=0,452) ; la
force de la M6 vient de la paire nominal/tierce de la cloche.

Automate illustratif (mêmes règles de seuils que le contrôle) :

| | Harmonique | Cloche Westerkerk |
|---|---|---|
| États (R1) | 0, 387, 498, 618, 702, 814, 884, 969, 1200 | 0, **307**, 395, 702, 809, **886**, 1020, 1200 |
| Interdits de parallèles (R2) | **0, 702, 1200** | **0, 307, 886** |
| Frontières (R3) | **0, 1200** | **0, 307** |

**L'interdit de parallèles s'est déplacé : {unisson, quinte, octave} →
{unisson, tierce-de-cloche, sixte-de-cloche}.** « Pas de quintes parallèles »
devient, sur carillon, « pas de tierces mineures ni de sixtes majeures
parallèles ». Et les pièces commencent/finissent sur l'unisson ou la
tierce-de-cloche. C'est P5 traduit en grammaire opérante — la bifurcation du
CADRAGE §7, structurée.

**Fait structurel (formulation corrigée le 2026-06-12, voir note)** : aux
seuils déclarés, le cantus de Fux n'a aucune réalisation légale dans
l'automate v1 de la cloche, alors que son MIROIR en a une (unisson · P5 · m3 ·
unisson · P5 · unisson · P5 · unisson · P5 · m3 · unisson). Matrice de
contrôle complète (chemin légal ?) :

| | cantus de Fux | cantus miroir |
|---|---|---|
| grammaire harmonique | OUI | OUI |
| grammaire cloche (v1) | **NON** | OUI |

**Note de correction (2026-06-12, après relecture critique)** — la première
rédaction concluait « le matériau mélodique est timbre-relatif » ; c'était
SURINTERPRÉTÉ. Le balayage montre que le rejet est **indépendant de τ_F**
(il tient de τ_F=0,05 à 1,20) : ce n'est donc PAS le paysage de fusion R2 de
la cloche qui rejette le cantus. Le mécanisme réel est la conjonction de
trois choix v1 : (i) **R3-argmax strict** — la frontière de la cloche est
BASSE dans l'octave (307 c) ; (ii) **la convention Φ(unisson)=+∞** — toute
arrivée parallèle/directe à l'unisson est tuée, et en cadence descendante
l'unisson n'est approchable par aucun mouvement contraire ; (iii) **l'espace
d'action v1** — contrepoint au-dessus, compas ≤ octave, pas d'équivalence
d'octave. Une cadence descendante ne peut conclure sur un état de frontière
que par mouvement contraire DEPUIS EN DESSOUS ; sous 307 c il n'y a que
l'unisson, lui-même inaccessible. La grammaire harmonique échappe au problème
parce que sa frontière (l'octave) est HAUTE — l'arrivée M6→P8 par mouvement
contraire est précisément la clausule classique.

Énoncé défendable et retenu : **dans v1, la grammaire dérivée de la cloche
n'admet pas de cadence descendante** (sa conclusion naturelle est ascendante,
vers la tierce-de-cloche) — conséquence dérivée, testable à l'oreille à
l'étape 4. Ce qui dissoudrait le rejet, à tester comme variantes déclarées :
un R3 adouci (frontière = états à Φ ≥ fraction du max : 886 c entrerait, et
la cadence descendante 1020→886 par contraire existerait), un compas de
douzième, ou la voix de contrepoint EN DESSOUS du cantus. L'énoncé général
« un cantus écrit pour un timbre peut être rejeté par la grammaire d'un
autre » reste vrai comme POSSIBILITÉ démontrée dans v1, pas comme fait sur
les cloches.

## 4. Sensibilité : règles robustes / fragiles (extraits des plateaux)

- **Robustes** : « pas de parallèles d'octave » (harmonique, plateau relatif
  0,66) ; « l'interdit cloche contient la tierce-de-cloche » (plateau 0,62 —
  c'est le dernier interdit à disparaître quand τ_F monte) ; frontières
  harmoniques {0, 1200} (stables sur tout τ_C où l'octave est admise).
- **Moyennes** : {P5, P8} exactement (0,16) ; {m3, M6} de cloche exactement
  (0,12).
- **Fragiles** : l'inventaire F1 exact (n'existe à aucun τ_C) ; la frontière
  R3 de la cloche bascule 307 ↔ 886 selon τ_C (la tierce-de-cloche n'est un
  état que si τ_C < 0,452 ; au-dessus, c'est la sixte qui devient à la fois
  frontière et premier interdit) — même nuance substrat/saillance que
  l'argmax de l'étape 2, ici localisée dans les seuils.

## 5. Ce que l'étape NE conclut pas (honnêteté)

- R5 est un gabarit : la préférence du contraire est MISE, pas dérivée. Un
  second principe (au-delà de « fusion par symétrie ») reste à chercher pour
  la dériver — c'était anticipé par §6.3.
- Les chemins légaux n'ont pas encore SONNÉ. « Correct selon la grammaire » vs
  « fonctionne à l'oreille » est exactement l'étape 4, et c'est là que les
  résidus ci-dessus deviennent des données.
- La grammaire cloche hérite des nuances de l'étape 2 (profil d'amplitudes →
  hiérarchie des pics Φ) ; les plateaux en absorbent une partie, pas tout.

## 6. Langage (décision actée)

L'étape 3 est restée en Python (continuité avec les métriques et le matériau ;
règles-comme-données réalisées en structures déclaratives). **La question
Clojure est explicitement reportée à l'étape 4** — rendu/écoute — où Overtone
et le REPL deviennent l'argument réel (recompiler la grammaire à chaud en
entendant le résultat).
